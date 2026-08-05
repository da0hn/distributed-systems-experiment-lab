#!/usr/bin/env python3
"""Verifica as citacoes de evidencia dos documentos do repositorio.

Duas formas convivem, por decisao `C-1` em `docs/architecture/decisoes-pendentes.md`:

- ancora nomeada, `arquivo.md#slug`, a forma canonica desde 2026-08-05;
- numero de linha, `arquivo.md:N` ou `arquivo.md:N-M`, forma legada que
  permanece dentro dos ADRs aceitos, cujo corpo nao pode ser editado.

O verificador reporta defeito objetivo, e nunca julgamento: alvo inexistente,
linha citada alem do fim do alvo, e ancora que nao corresponde a titulo nenhum.
Ele NAO verifica se o conteudo da linha sustenta a afirmacao, porque isso exige
leitura.

O slug segue o GitHub Flavored Markdown, por decisao `C-1a`: minusculas, espaco
vira hifen, pontuacao e' removida, acento e' preservado.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable, NamedTuple, Optional

# `arquivo.md:12` e `arquivo.md:12-30`.
LINE_CITATION = re.compile(r"(?<![\w/])([\w./-]+\.md):(\d+)(?:-(\d+))?")
# `arquivo.md#slug-do-titulo`. O slug aceita acento, por `C-1a`.
ANCHOR_CITATION = re.compile(r"(?<![\w/])([\w./-]+\.md)#([^\s`\)\]\|,;]+)")
# Um ADR abreviado: `0008-...md`, sem o prefixo da pasta.
ADR_ABBREVIATION = re.compile(r"^(\d{4})-")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


class Defect(NamedTuple):
    source: Path
    line_number: int
    citation: str
    reason: str


def gfm_slug(heading: str) -> str:
    """Reproduz a regra de slug do GitHub Flavored Markdown."""
    text = heading.strip().lower()
    # A marcacao inline nao entra no slug: o GitHub usa o texto renderizado.
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "").replace("_", "_")
    # Mantem letra (inclusive acentuada), digito, espaco, hifen e underscore.
    kept = [c for c in text
            if c.isalnum() or c in {" ", "-", "_"} or unicodedata.combining(c)]
    return "".join(kept).replace(" ", "-")


def headings_of(path: Path) -> list[str]:
    slugs: list[str] = []
    seen: dict[str, int] = {}
    in_fence = False
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(raw)
        if not match:
            continue
        base = gfm_slug(match.group(2))
        if not base:
            continue
        count = seen.get(base, 0)
        seen[base] = count + 1
        slugs.append(base if count == 0 else f"{base}-{count}")
    return slugs


def resolve(target: str, source: Path, root: Path) -> Optional[Path]:
    """Resolve o alvo citado contra a pasta da origem, docs/ e a raiz."""
    candidates = [source.parent / target, root / "docs" / target, root / target]
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    # Abreviacao de ADR: `0008-...md` resolve pelo prefixo, dentro da pasta
    # candidata. A forma abreviada e' usada no proprio `docs/adr/`.
    #
    # A pasta escrita na citacao e' preservada: `arquivo/0007-...md` procura em
    # `<base>/arquivo/`, e nunca em `<base>/`. Sem isso, um ADR arquivado resolve
    # para o ADR de mesmo numero da serie corrente, que e' outro documento.
    abbreviation = ADR_ABBREVIATION.match(Path(target).name)
    if abbreviation is None:
        return None
    prefix = abbreviation.group(1)
    written_folder = Path(target).parent
    bases = [source.parent, root / "docs" / "adr", root / "docs", root]
    for base in bases:
        folder = base / written_folder
        if not folder.is_dir():
            continue
        matches = sorted(folder.glob(f"{prefix}-*.md"))
        if len(matches) == 1:
            return matches[0].resolve()
    return None


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8", errors="replace").splitlines())


def inspect(source: Path, root: Path) -> Iterable[Defect]:
    text = source.read_text(encoding="utf-8", errors="replace")
    in_fence = False
    for number, raw in enumerate(text.splitlines(), 1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        for match in ANCHOR_CITATION.finditer(raw):
            target, slug = match.group(1), match.group(2)
            citation = f"{target}#{slug}"
            resolved = resolve(target, source, root)
            if resolved is None:
                yield Defect(source, number, citation, "alvo inexistente")
                continue
            if slug not in headings_of(resolved):
                yield Defect(source, number, citation,
                             "ancora nao corresponde a titulo nenhum do alvo")

        for match in LINE_CITATION.finditer(raw):
            target = match.group(1)
            start = int(match.group(2))
            end = int(match.group(3)) if match.group(3) else start
            citation = match.group(0)
            resolved = resolve(target, source, root)
            if resolved is None:
                yield Defect(source, number, citation, "alvo inexistente")
                continue
            total = line_count(resolved)
            if max(start, end) > total:
                yield Defect(source, number, citation,
                             f"linha citada alem do fim: o alvo tem {total}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verifica as citacoes de evidencia dos documentos."
    )
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Arquivo com defeitos conhecidos e aceitos, um por linha, no "
             "formato `caminho-da-origem:citacao`. A linha da origem NAO entra "
             "na chave: ela muda a cada edicao do arquivo, e uma baseline que "
             "envelhece a cada commit nao serve para nada. Linhas iniciadas "
             "por # sao comentario.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    accepted: set[str] = set()
    if args.baseline is not None and args.baseline.is_file():
        for raw in args.baseline.read_text(encoding="utf-8").splitlines():
            entry = raw.strip()
            if entry and not entry.startswith("#"):
                accepted.add(entry)

    sources = sorted(root.glob("docs/**/*.md")) + sorted(root.glob("*.md"))
    defects = [d for source in sources for d in inspect(source, root)]

    remaining, waived = [], []
    for defect in defects:
        source = defect.source.relative_to(root).as_posix()
        key = f"{source}:{defect.citation}"
        label = f"{source}:{defect.line_number}:{defect.citation}"
        (waived if key in accepted else remaining).append((label, defect))

    for label, defect in remaining:
        print(f"DEFEITO: {label} — {defect.reason}")
    if waived:
        print(f"\n{len(waived)} defeito(s) conhecido(s) e aceito(s) na baseline.")
    print(f"\n{len(sources)} arquivo(s) varrido(s); "
          f"{len(remaining)} defeito(s) nao aceito(s).")
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
