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

# Isento por caminho, e cada entrada diz por que. Ate 2026-08-07 estes arquivos
# eram isentos por acidente: o ramo de `docs/adr/` respondia "isto e' um ADR?", e o
# caso negativo caia num `return None` que ninguem decidiu — a fila, com 119 mil
# caracteres de prosa, e o indice, com 22 mil, nunca foram medidos por causa dele.
# A pessoa decidiu em 2026-08-07 que a isencao passa a ser declarada, com o motivo
# escrito, e que o ramo deixa de isentar por omissao.
EXEMPT_BY_PATH = {
    # A fila existe so para rastrear pendencia, e por isso e' a unica excecao ao
    # principio de fonte unica: ela fala do que outros documentos vao possuir. Ela
    # cresce por decisao enfileirada e encolhe por lapide, e um teto ali obrigaria
    # a apagar pendencia viva para caber.
    Path("docs/adr/fila-de-decisoes.md"),
    # O indice cresce por ADR aceito, como o `example-mapping.md` cresce por
    # exemplo. Um teto ali obrigaria a omitir ADR do inventario, que e' o oposto do
    # que o arquivo existe para fazer.
    Path("docs/adr/README.md"),
    # Os dois `AGENTS.md` sao instrucao, e nao artefato de planejamento: o harness os
    # carrega inteiros antes de existir qualquer consulta, e o que eles carregam e'
    # guardrail — a regra que o agente precisa ANTES de saber o que procurar. Cortar
    # prosa deles para caber num teto apaga guardrail, e nao redundancia.
    #
    # A isencao e' declarada, e nao herdada. Ate ela existir, esses arquivos so
    # escapavam porque o workflow `docs` media apenas `docs/adr/[0-9]*.md`, e ninguem
    # havia medido os dois. Medidos, deram 21.322 caracteres de prosa na raiz e 11.665
    # em `docs/`, ambos contra o generico de 4.000 — a distancia mostra que o teto
    # generico nunca descreveu este tipo de arquivo.
    #
    # O que NAO esta isento e' a duplicacao: o roteamento documental tem um dono unico,
    # `docs/README.md`, que cai no generico como qualquer outro Markdown.
    Path("AGENTS.md"),
    Path("docs/AGENTS.md"),
}

# `docs/adr/arquivo/` e' registro congelado do que se pensou naquela data, e o
# `AGENTS.md` proibe edita-lo. Um teto sobre o que nao pode ser editado so produz
# vermelho permanente, que e' o mesmo argumento da isencao dos quatro ADRs legados.
ARCHIVE_ROOT = Path("docs/adr/arquivo")

# Um arquivo marcado como inativo nao guia ninguem, e o limite existe para manter
# prosa viva focada. A pessoa decidiu em 2026-08-07 isenta-lo enquanto a marca
# estiver la, e a isencao e' reversivel por construcao: apagar o cabecalho devolve o
# teto no mesmo instante, sem ninguem precisar lembrar de mexer neste script.
#
# Sem ela, a propria marcacao punia quem a cumpriu: o cabecalho custa cerca de 290
# letras, e foi ele que levou `deteccao-de-protecao-inerte/behavior.feature` de 3299
# para 3588 contra um teto de 3500. O arquivo reprovava por ter sido marcado.
#
# A marca e' procurada so no comeco do arquivo, para que a expressao citada dentro
# de um cenario, de uma tabela ou de um paragrafo nao isente nada.
INACTIVE_MARKER = "ARQUIVO INATIVO"
INACTIVE_SCAN = 600
MARKDOWN_LIMIT = 4000
ADR_LIMIT = 12000
CONTRACT_LIMIT = 16000

# Este script e' a UNICA declaracao de limite do repositorio. As skills que dependem
# dele NAO DEVEM repetir numero nenhum: um numero copiado para uma skill envelhece na
# primeira decisao que o mude, e foi assim que `feature-planning/SKILL.md` passou a
# cobrar 4500 do `example-mapping.md` depois de o teto do Example Mapping ser removido,
# e a medir o Feature Card por um criterio ja trocado por outro.
#
# A auditoria de 2026-08-06 (achado A-14) pediu um teste que comparasse o limite
# declarado na skill com o aplicado aqui. A guarda abaixo faz o inverso, e de
# proposito: em vez de detectar a divergencia, ela impede que exista uma segunda
# declaracao. Ela roda em toda invocacao, e nao so quando alguem lembra.
#
# A lista cobre so os arquivos que delegam limite a este script. Um teto que este
# script nao aplica — o orcamento de tamanho das proprias skills, em
# `workflow-retro/SKILL.md` — nao entra aqui, porque ele nao tem nada com que divergir.
INSTRUCTIONS_WITHOUT_LIMITS = (
    Path(".claude/skills/feature-planning/SKILL.md"),
    Path(".claude/skills/adr/SKILL.md"),
    Path(".claude/agents/adr-writer.md"),
    Path(".claude/agents/adr-reviewer.md"),
)

# Duas formas de declarar limite em prosa: um numero seguido de "caracteres", ou a
# palavra "limite" seguida de um numero na mesma frase. O `[^.\n]` para no primeiro
# ponto, o que mantem URL e numero de versao fora do alcance. "88 colunas" e
# "RFC 2119" nao sao limite de artefato e nao casam.
DECLARED_LIMIT_PATTERNS = (
    re.compile(r"\d[\d.\s]*caracteres"),
    re.compile(r"(?i)limit\w*[^.\n]{0,60}?\d[\d.]{2,}"),
)

# Um ADR e' `docs/adr/NNNN-titulo.md`. O indice e o historico congelado de
# `docs/adr/arquivo/**` vivem na mesma pasta e nao sao documentos de decisao
# unica: o indice cresce por construcao a cada ADR novo, e o arquivo morto nao
# pode ser encolhido. Decisao `C-7`, em
# `docs/adr/arquivo/proposta-2026-08-03/decisoes-pendentes.md`.
ADR_FILENAME = re.compile(r"^\d{4}-.+\.md$")

# Os quatro primeiros ADRs foram escritos sob outra pratica e tem cerca de 35 mil
# caracteres, e eles nunca caberao em limite nenhum. Isenta-los evita um
# verificador permanentemente vermelho, que deixa de ser lido. Decisao `C-7`.
#
# A imutabilidade do corpo foi revogada em 2026-08-07, e a isencao continua: o
# que a revogacao autoriza e' o **patch**, que conserta citacao, caminho e erro
# material. Encolher a prosa desses quatro seria reescrever o argumento, que o
# patch NAO DEVE tocar. O limite so os alcanca por um ADR novo que os substitua.
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

# `## Patches aplicados` e' obrigatoria em todo ADR desde 2026-08-07, e ela e' a
# ultima secao do arquivo. Nada dali para baixo entra na contagem: a secao e'
# livro-razao de manutencao, e nao argumento.
#
# Sem esta isencao, tornar a secao obrigatoria estouraria o limite de todo ADR
# que estivesse perto dele — foi o que aconteceu com os ADRs 0011 e 0012, que
# passaram de ~11.990 para ~12.265 caracteres so por ganha-la. E a saida seria
# encolher a prosa de um ADR aceito, que e' exatamente o que um patch NAO DEVE
# fazer: o limite empurraria para a reescrita do argumento.
PATCH_LEDGER = "## Patches aplicados"


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Devolve as linhas de prosa com o numero que elas tem no arquivo original."""
    kept: list[tuple[int, str]] = []
    fence: Optional[str] = None
    for number, line in enumerate(text.split("\n"), start=1):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                continue
            if line.strip() == PATCH_LEDGER:
                break
            if is_table_row(line):
                continue
            kept.append((number, line))
        elif match and match.group(1)[0] == fence:
            fence = None
    return kept


def prose_only(text: str) -> str:
    """Remove blocos cercados e linhas de tabela, que nao entram na contagem."""
    return "\n".join(line for _, line in prose_lines(text))


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
    if relative_path in EXEMPT_BY_PATH:
        return None
    if ARCHIVE_ROOT in relative_path.parents:
        return None
    if relative_path in LIMITS_BY_PATH:
        return LIMITS_BY_PATH[relative_path]
    if relative_path.name in LIMITS_BY_NAME:
        return LIMITS_BY_NAME[relative_path.name]
    # So o nome numerado identifica um ADR. O que nao for cai no limite generico
    # abaixo, e nao mais num `return None` — a isencao agora e' declarada acima.
    if relative_path.parts[:2] == ("docs", "adr") and ADR_FILENAME.match(relative_path.name):
        if relative_path.name[:4] in ADR_LEGACY:
            return None
        return ADR_LIMIT
    if relative_path.suffix in {".yaml", ".yml", ".json"}:
        return CONTRACT_LIMIT
    if relative_path.suffix == ".md":
        return MARKDOWN_LIMIT
    raise ValueError(f"Sem limite definido para: {relative_path}")


def audit_skill_declarations(root: Path) -> list[str]:
    """Devolve os limites que reapareceram numa skill ou agente, com o trecho."""
    offences: list[str] = []
    for relative_path in INSTRUCTIONS_WITHOUT_LIMITS:
        skill_file = root / relative_path
        if not skill_file.is_file():
            continue
        text = skill_file.read_text(encoding="utf-8")
        for number, line in prose_lines(text):
            for pattern in DECLARED_LIMIT_PATTERNS:
                match = pattern.search(line)
                if match:
                    offences.append(
                        f"{relative_path.as_posix()}:{number} — {match.group(0).strip()}"
                    )
                    break
    return offences


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

    offences = audit_skill_declarations(root)
    if offences:
        print(
            "ERRO: uma instrucao voltou a declarar limite. Este script e' a unica "
            "declaracao — apague o numero de la e mande rodar o verificador.",
            file=sys.stderr,
        )
        for offence in offences:
            print(f"  {offence}", file=sys.stderr)
        failed = True

    for requested in args.files:
        relative_path = requested if not requested.is_absolute() else requested.relative_to(root)
        try:
            file_path = resolve_inside(root, relative_path)
            if not file_path.is_file():
                raise ValueError(f"Arquivo ausente: {relative_path}")
            limit = overrides.get(relative_path, default_limit(relative_path))
            raw = file_path.read_text(encoding="utf-8").strip()
            # Um `--limit` explicito vence a isencao: quem o passou quer medir.
            inactive = (
                limit is not None
                and relative_path not in overrides
                and INACTIVE_MARKER in raw[:INACTIVE_SCAN]
            )
            if inactive:
                limit = None
            total = len(raw)
            if counts_prose_only(relative_path):
                size = len(prose_only(raw).strip())
                detail = f" (prosa; {total} com diagrama, codigo e tabela)"
            else:
                size = total
                detail = ""
            if limit is None:
                motivo = " (inativo)" if inactive else ""
                print(
                    f"ISENTO: {relative_path} — {size} caracteres, "
                    f"sem limite{motivo}{detail}"
                )
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
