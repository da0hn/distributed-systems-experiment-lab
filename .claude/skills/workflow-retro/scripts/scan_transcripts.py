#!/usr/bin/env python3
"""Conta sinais mecanicos de atrito nos transcritos de sessao do Claude Code.

A saida e indicio, e nao conclusao. Leia o trecho citado antes de propor um patch.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit", "mcp__idea__apply_patch"}
CORRECTION_MARKERS = (
    "nao ", "não ", "errado", "na verdade", "ja falei", "já falei", "de novo",
    "sempre ", "nunca ", "corrija", "corrige", "refaça", "refaca", "esqueceu",
    "pare de", "evite", "deveria ter", "nao era", "não era", "voce errou",
    "você errou", "isso esta errado", "isso está errado",
)
SHORT_PROMPT_CHARS = 400
LONG_ANSWER_CHARS = 1200


def slug_for(root: Path) -> str:
    """Reproduz o nome de pasta que o Claude Code deriva do diretorio do projeto."""
    return str(root).replace(":", "-").replace("\\", "-").replace("/", "-")


def find_transcripts_dir(root: Path, explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.is_dir():
            raise ValueError(f"Diretorio de transcritos ausente: {explicit}")
        return explicit
    base = Path.home() / ".claude" / "projects"
    if not base.is_dir():
        raise ValueError(f"Diretorio de projetos ausente: {base}")
    exact = base / slug_for(root)
    if exact.is_dir():
        return exact
    tail = root.name
    matches = [
        item for item in base.iterdir() if item.is_dir() and item.name.endswith(tail)
    ]
    if len(matches) == 1:
        return matches[0]
    raise ValueError(
        f"Nao foi possivel derivar o diretorio de transcritos de {root}. "
        "Informe --transcripts."
    )


def iter_records(path: Path):
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def blocks_of(record: dict) -> list[dict]:
    message = record.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if isinstance(content, list):
        return [block for block in content if isinstance(block, dict)]
    return []


def text_of(blocks: list[dict]) -> str:
    texts = [block.get("text", "") for block in blocks if block.get("type") == "text"]
    return "\n".join(texts)


def looks_like_correction(text: str) -> bool:
    stripped = text.strip()
    if not stripped or stripped.startswith("<") or len(stripped) > SHORT_PROMPT_CHARS:
        return False
    lowered = stripped.lower()
    return any(marker in lowered for marker in CORRECTION_MARKERS)


def scan(path: Path, report: dict) -> None:
    session = path.stem
    last_answer_chars = 0
    edits: Counter[str] = Counter()
    for record in iter_records(path):
        if record.get("isMeta") or record.get("isSidechain"):
            continue
        if record.get("isCompactSummary"):
            report["compactacoes"][session] += 1
        kind = record.get("type")
        blocks = blocks_of(record)
        if kind == "assistant":
            for block in blocks:
                if block.get("type") == "tool_use":
                    name = block.get("name", "")
                    target = (block.get("input") or {}).get("file_path")
                    if name in EDIT_TOOLS and isinstance(target, str):
                        edits[target] += 1
            last_answer_chars = len(text_of(blocks))
        elif kind == "user":
            for block in blocks:
                if block.get("type") == "tool_result" and block.get("is_error"):
                    raw = block.get("content")
                    if not isinstance(raw, str):
                        raw = json.dumps(raw, ensure_ascii=False)
                    detail = raw
                    report["erros"][detail.strip()[:160]].append(session)
            prompt = text_of(blocks)
            if looks_like_correction(prompt) and last_answer_chars >= LONG_ANSWER_CHARS:
                report["correcoes"].append((session, " ".join(prompt.split())[:160]))
            if prompt.strip():
                last_answer_chars = 0
    for target, count in edits.items():
        if count >= 3:
            report["retrabalho"][target].append((session, count))


def emit(report: dict, limit: int) -> None:
    print("== Erros de ferramenta (tipo 2) ==")
    ranked = sorted(report["erros"].items(), key=lambda item: -len(item[1]))
    for detail, sessions in ranked[:limit] or []:
        print(f"  {len(sessions)}x | {len(set(sessions))} sessao(oes) | {detail}")
    if not ranked:
        print("  nenhum")

    print("\n== Retrabalho de artefato (tipo 1) ==")
    ranked = sorted(report["retrabalho"].items(), key=lambda item: -len(item[1]))
    for target, hits in ranked[:limit] or []:
        total = sum(count for _, count in hits)
        print(f"  {target} | {total} edicoes em {len(hits)} sessao(oes)")
    if not ranked:
        print("  nenhum")

    print("\n== Candidatos a correcao explicita (tipo 3) ==")
    for session, prompt in report["correcoes"][-limit:] or []:
        print(f"  {session[:8]} | {prompt}")
    if not report["correcoes"]:
        print("  nenhum")

    print("\n== Compactacao de contexto (tipo 6) ==")
    total = sum(report["compactacoes"].values())
    print(f"  {total} compactacao(oes) em {len(report['compactacoes'])} sessao(oes)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Conta sinais de atrito nos transcritos de sessao."
    )
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--transcripts", type=Path, default=None)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        directory = find_transcripts_dir(args.root.resolve(), args.transcripts)
    except ValueError as error:
        print(f"ERRO: {error}", file=sys.stderr)
        return 1

    cutoff = time.time() - args.days * 86400
    files = [
        item
        for item in sorted(directory.glob("*.jsonl"))
        if item.stat().st_mtime >= cutoff
    ]
    if not files:
        print(f"Nenhum transcrito nos ultimos {args.days} dias em {directory}.")
        return 0

    report = {
        "erros": defaultdict(list),
        "retrabalho": defaultdict(list),
        "correcoes": [],
        "compactacoes": Counter(),
    }
    for path in files:
        try:
            scan(path, report)
        except OSError as error:
            print(f"ERRO: {error}", file=sys.stderr)

    print(f"Fonte: {directory}")
    print(f"Sessoes lidas: {len(files)} (ultimos {args.days} dias)\n")
    emit(report, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
