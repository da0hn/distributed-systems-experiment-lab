#!/usr/bin/env python3
"""Validate the character budgets for feature-planning artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


# O `example-mapping.md` NAO tem limite, por decisao de 2026-08-06. Ele cresce por
# exemplo acrescentado, e acrescentar exemplo e' o trabalho dele — um teto ali
# transforma "achei mais um contraexemplo" em "preciso apagar um dos antigos", que e'
# o oposto do que o artefato existe para fazer. O texto de `docs/AGENTS.md` ja dizia
# isso; quem estava fora de sincronia era este script.
LIMITS_BY_NAME = {
    "feature-card.md": 5500,
    "behavior.feature": 3500,
    "implementation-plan.md": 7000,
}
LIMITS_BY_PATH = {
    Path("docs/architecture/integrations.md"): 12000,
}
# Isento por nome. Sem esta linha o `example-mapping.md` cairia no MARKDOWN_LIMIT
# generico de 4000, que e' mais apertado do que o teto que a decisao removeu.
EXEMPT_BY_NAME = {"example-mapping.md"}
MARKDOWN_LIMIT = 4000
ADR_LIMIT = 12000
CONTRACT_LIMIT = 16000

# Um ADR e' `docs/adr/NNNN-titulo.md`. O indice e o historico congelado de
# `docs/adr/arquivo/**` vivem na mesma pasta e nao sao documentos de decisao
# unica: o indice cresce por construcao a cada ADR novo, e o arquivo morto nao
# pode ser encolhido. Decisao `C-7`, em
# `docs/adr/arquivo/proposta-2026-08-03/decisoes-pendentes.md`.
ADR_FILENAME = re.compile(r"^\d{4}-.+\.md$")

# Os quatro primeiros ADRs foram escritos sob outra pratica e tem cerca de 35 mil
# caracteres. O corpo de um ADR aceito nao pode ser editado, entao eles nunca
# caberao em limite nenhum. Isenta-los evita um verificador permanentemente
# vermelho, que deixa de ser lido. Decisao `C-7`.
ADR_LEGACY = {"0001", "0002", "0003", "0004"}

# Em todo artefato Markdown com limite, diagrama, bloco de codigo e tabela NAO
# entram na contagem. Os tres sao densos em caracteres e pobres em prosa: um
# `flowchart` de dez nos custa mais que a secao que ele ilustra. Conta-los punia
# justamente o que as convencoes exigem — todo fluxo vai tambem como Mermaid, e
# toda regra vai em tabela com evidencia — e o corte acabava saindo do diagrama ou
# da citacao. O limite passa a medir prosa, que e' o unico lugar onde encher
# linguica e' possivel.
#
# Vale so para `.md`. O `behavior.feature` fica de fora porque em Gherkin a tabela
# `Exemplos:` e' o cenario, e nao ilustracao dele; descontá-la esvaziaria o limite.
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1


def prose_only(text: str) -> str:
    """Remove blocos cercados e linhas de tabela, que nao entram na contagem."""
    kept: list[str] = []
    fence: Optional[str] = None
    for line in text.split("\n"):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                continue
            if is_table_row(line):
                continue
            kept.append(line)
        elif match and match.group(1)[0] == fence:
            fence = None
    return "\n".join(kept)


def counts_prose_only(relative_path: Path) -> bool:
    return relative_path.suffix == ".md"


def parse_limit(value: str) -> tuple[Path, int]:
    try:
        raw_path, raw_limit = value.rsplit("=", 1)
        limit = int(raw_limit)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Use <caminho>=<limite-positivo>."
        ) from error
    if not raw_path or limit <= 0:
        raise argparse.ArgumentTypeError(
            "Use <caminho>=<limite-positivo>."
        )
    return Path(raw_path), limit


def resolve_inside(root: Path, relative_path: Path) -> Path:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"Fora da raiz: {relative_path}") from error
    return candidate


def default_limit(relative_path: Path) -> Optional[int]:
    """Devolve o limite do arquivo, ou None quando ele e' isento."""
    if relative_path.name in EXEMPT_BY_NAME:
        return None
    if relative_path in LIMITS_BY_PATH:
        return LIMITS_BY_PATH[relative_path]
    if relative_path.name in LIMITS_BY_NAME:
        return LIMITS_BY_NAME[relative_path.name]
    if relative_path.parts[:2] == ("docs", "adr"):
        if not ADR_FILENAME.match(relative_path.name):
            return None
        if relative_path.name[:4] in ADR_LEGACY:
            return None
        return ADR_LIMIT
    if relative_path.suffix in {".yaml", ".yml", ".json"}:
        return CONTRACT_LIMIT
    if relative_path.suffix == ".md":
        return MARKDOWN_LIMIT
    raise ValueError(f"Sem limite definido para: {relative_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida limites de caracteres dos artefatos de planejamento."
    )
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--file", action="append", dest="files", required=True, type=Path)
    parser.add_argument(
        "--limit",
        action="append",
        default=[],
        type=parse_limit,
        metavar="CAMINHO=LIMITE",
        help="Sobrescreve o limite de um arquivo especifico.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    overrides = {path: limit for path, limit in args.limit}
    failed = False

    for requested in args.files:
        relative_path = requested if not requested.is_absolute() else requested.relative_to(root)
        try:
            file_path = resolve_inside(root, relative_path)
            if not file_path.is_file():
                raise ValueError(f"Arquivo ausente: {relative_path}")
            limit = overrides.get(relative_path, default_limit(relative_path))
            raw = file_path.read_text(encoding="utf-8").strip()
            total = len(raw)
            if counts_prose_only(relative_path):
                size = len(prose_only(raw).strip())
                detail = f" (prosa; {total} com diagrama, codigo e tabela)"
            else:
                size = total
                detail = ""
            if limit is None:
                print(f"ISENTO: {relative_path} — {size} caracteres, sem limite{detail}")
                continue
            state = "OK" if size <= limit else "EXCEDE"
            print(f"{state}: {relative_path} — {size}/{limit} caracteres{detail}")
            failed = failed or size > limit
        except (OSError, ValueError) as error:
            print(f"ERRO: {error}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
