#!/usr/bin/env python3
"""Verifica as citações de evidência dos documentos do repositório.

Duas formas convivem, por decisão `C-1` em `docs/architecture/decisoes-pendentes.md`:

- âncora nomeada, `arquivo.md#slug`, a forma canônica desde 2026-08-05;
- número de linha, `arquivo.md:N` ou `arquivo.md:N-M`, forma legada que
  permanece dentro dos ADRs aceitos, cujo corpo não pode ser editado.

O verificador reporta defeito objetivo, e nunca julgamento: alvo inexistente,
linha citada além do fim do alvo, e âncora que não corresponde a título nenhum.
Ele NÃO verifica se o conteúdo da linha sustenta a afirmação, porque isso exige
leitura.

O slug segue o GitHub Flavored Markdown, por decisão `C-1a`: minúsculas, espaço
vira hífen, pontuação é removida, acento é preservado.
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
# `[texto](#slug)`, a âncora interna de um documento para si mesmo. Ela NÃO é
# verificada — o padrão acima exige o `.md` antes do `#` —, e por isso só
# aparece no modo de consulta, onde uma redução precisa dela.
INTERNAL_ANCHOR = re.compile(r"\]\(#([^\s)]+)\)")
# Um ADR abreviado: `0008-...md`, sem o prefixo da pasta.
ADR_ABBREVIATION = re.compile(r"^(\d{4})-")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


class Defect(NamedTuple):
    source: Path
    line_number: int
    citation: str
    reason: str


class Reference(NamedTuple):
    """Uma citação que aponta para um heading, do ponto de vista do alvo."""

    source: Path
    line_number: int
    slug: str
    internal: bool
    frozen: bool


def outside_fences(text: str) -> Iterable[tuple[int, str]]:
    """Cada linha fora de bloco cercado, com o número dela."""
    in_fence = False
    for number, raw in enumerate(text.splitlines(), 1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield number, raw


def sources_of(root: Path) -> list[Path]:
    return sorted(root.glob("docs/**/*.md")) + sorted(root.glob("*.md"))


def gfm_slug(heading: str) -> str:
    """Reproduz a regra de slug do GitHub Flavored Markdown."""
    text = heading.strip().lower()
    # A marcação inline não entra no slug: o GitHub usa o texto renderizado.
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "").replace("_", "_")
    # Mantém letra (inclusive acentuada), dígito, espaço, hífen e underscore.
    kept = [c for c in text
            if c.isalnum() or c in {" ", "-", "_"} or unicodedata.combining(c)]
    return "".join(kept).replace(" ", "-")


def headings_of(path: Path) -> list[str]:
    slugs: list[str] = []
    seen: dict[str, int] = {}
    text = path.read_text(encoding="utf-8", errors="replace")
    for _, raw in outside_fences(text):
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
    # Abreviação de ADR: `0008-...md` resolve pelo prefixo, dentro da pasta
    # candidata. A forma abreviada é usada no próprio `docs/adr/`.
    #
    # A pasta escrita na citação é preservada: `arquivo/0007-...md` procura em
    # `<base>/arquivo/`, e nunca em `<base>/`. Sem isso, um ADR arquivado resolve
    # para o ADR de mesmo número da série corrente, que é outro documento.
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
    for number, raw in outside_fences(text):
        for match in ANCHOR_CITATION.finditer(raw):
            target, slug = match.group(1), match.group(2)
            citation = f"{target}#{slug}"
            resolved = resolve(target, source, root)
            if resolved is None:
                yield Defect(source, number, citation, "alvo inexistente")
                continue
            if slug not in headings_of(resolved):
                yield Defect(source, number, citation,
                             "âncora não corresponde a título nenhum do alvo")

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
                             f"linha citada além do fim: o alvo tem {total}")


def references_to(target: Path, root: Path) -> dict[str, list[Reference]]:
    """Quem cita cada heading de `target`, em todo o corpus.

    Duas formas contam. A citação externa, `arquivo.md#slug`, partindo de
    qualquer documento. E a âncora interna, `[texto](#slug)`, dentro do próprio
    alvo — que o verificador não acusa, e cuja remoção quebra link em silêncio.

    `docs/adr/arquivo/**` entra na varredura de propósito. A verificação o
    ignora porque a citação que parte de lá é inconsertável; é exatamente por
    ser inconsertável que ela é a que mais exige lápide.
    """
    frozen_root = root / "docs" / "adr" / "arquivo"
    found: dict[str, list[Reference]] = {}
    for source in sources_of(root):
        frozen = frozen_root in source.parents
        text = source.read_text(encoding="utf-8", errors="replace")
        for number, raw in outside_fences(text):
            for match in ANCHOR_CITATION.finditer(raw):
                if resolve(match.group(1), source, root) != target:
                    continue
                found.setdefault(match.group(2), []).append(
                    Reference(source, number, match.group(2), False, frozen))
            if source != target:
                continue
            for match in INTERNAL_ANCHOR.finditer(raw):
                found.setdefault(match.group(1), []).append(
                    Reference(source, number, match.group(1), True, frozen))
    return found


def report_references(target: Path, root: Path, slug: Optional[str]) -> int:
    """Imprime quem cita os headings do alvo. Consulta, e nunca veredito."""
    found = references_to(target, root)
    if slug is not None:
        found = {slug: found.get(slug, [])}
    existing = set(headings_of(target))
    shown = target.relative_to(root).as_posix()
    total = sum(len(refs) for refs in found.values())
    print(f"{shown}: {len(found)} heading(s) citado(s), {total} citação(ões).")
    print("Apague um heading desta lista e a citação quebra. Deixe lápide.\n")
    for name in sorted(found):
        ausente = "" if name in existing else "   (AUSENTE do alvo)"
        print(f"  #{name}{ausente}")
        for ref in sorted(found[name], key=lambda r: (r.source, r.line_number)):
            origem = ref.source.relative_to(root).as_posix()
            marcas = []
            if ref.internal:
                marcas.append("interna, não verificada pelo CI")
            if ref.frozen:
                marcas.append("arquivo congelado, inconsertável")
            sufixo = f"   [{'; '.join(marcas)}]" if marcas else ""
            print(f"      {origem}:{ref.line_number}{sufixo}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verifica as citações de evidência dos documentos."
    )
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Arquivo com defeitos conhecidos e aceitos, um por linha, no "
             "formato `caminho-da-origem:citação`. A linha da origem NÃO entra "
             "na chave: ela muda a cada edição do arquivo, e uma baseline que "
             "envelhece a cada commit não serve para nada. Linhas iniciadas "
             "por # são comentário.",
    )
    parser.add_argument(
        "--quem-cita",
        dest="quem_cita",
        metavar="ALVO",
        help="Consulta, e não verificação: responde quem cita cada heading de "
             "ALVO, que é `caminho/arquivo.md` ou `caminho/arquivo.md#slug`. "
             "Rode ANTES de reduzir um documento, para saber onde a lápide é "
             "obrigatória. Nada é gravado: a resposta é recalculada a cada "
             "execução, e por isso não existe derivado a envelhecer.",
    )
    args = parser.parse_args()

    root = args.root.resolve()

    if args.quem_cita is not None:
        written, _, slug = args.quem_cita.partition("#")
        # A consulta não parte de documento nenhum: o caminho é escrito pela
        # pessoa, relativo a raiz ou a `docs/`. A origem fictícia só entrega a
        # raiz como pasta de partida, e os outros candidatos de `resolve`
        # cobrem o resto.
        target = resolve(written, root / "consulta-sem-origem.md", root)
        if target is None:
            print(f"alvo inexistente: {written}", file=sys.stderr)
            return 2
        return report_references(target, root, slug or None)
    accepted: set[str] = set()
    if args.baseline is not None and args.baseline.is_file():
        for raw in args.baseline.read_text(encoding="utf-8").splitlines():
            entry = raw.strip()
            if entry and not entry.startswith("#"):
                accepted.add(entry)

    # `docs/adr/arquivo/**` nunca é editado: ele registra o que se pensava
    # naquela data, e editar apaga a evidência (`docs/AGENTS.md`, seção "O que
    # nunca é editado"). As citações que PARTEM de lá apontam para um mundo
    # que mudou, e são inconsertáveis por construção — acusá-las deixa o
    # verificador permanentemente vermelho, que é o mesmo argumento com que
    # `C-7` isentou os quatro ADRs legados. Citação que APONTA para lá
    # continua verificada normalmente.
    morto = root / "docs" / "adr" / "arquivo"
    sources = sorted(root.glob("docs/**/*.md")) + sorted(root.glob("*.md"))
    vivos = [s for s in sources if morto not in s.parents]
    defects = [d for source in vivos for d in inspect(source, root)]

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
    print(f"\n{len(vivos)} arquivo(s) varrido(s); "
          f"{len(remaining)} defeito(s) não aceito(s).")
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
