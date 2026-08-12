#!/usr/bin/env python3
"""Compara nome de tabela entre os `erDiagram` e as migrações Flyway.

A pasta `docs/architecture/schemas/` é a dona única da forma das tabelas,
por decisão de 2026-08-11 registrada no ADR-0015, com a granularidade que
o fecho de `E-78` mudou em 2026-08-12 — de um arquivo para um diretório.

Ser dono da forma cria uma divergência possível: o desenho e o `CREATE TABLE`
são dois lugares, e nada impede que um mude sem o outro. Este verificador
fecha isso pelo único eixo que uma máquina consegue conferir sem interpretar
— o **nome da tabela**.

Ele NÃO compara coluna, tipo, chave nem índice. `erDiagram` não expressa
índice, e o diagrama anota por comentário o que não tem sintaxe para dizer;
comparar isso exigiria leitura, e leitura é trabalho de revisão humana.

A associação entre um diagrama e o serviço dele é descoberta, e não
declarada: o heading que abre cada diagrama nomeia o schema entre crases, e o
schema aparece nas migrações em `SCHEMA <nome>` ou em `CREATE TABLE
<schema>.<tabela>`. Uma tabela de-para neste arquivo seria um terceiro lugar
onde a topologia vive, que é exatamente o defeito que a pasta existe para não
ter. Por isso o nome do arquivo dentro dela também não é declarado aqui: todo
`.md` da pasta é lido, e quem não tiver `erDiagram` sob heading com schema
simplesmente não contribui.

A baseline carrega divergência **deliberada**, e cada bloco dela nomeia a
decisão que a autorizou. Uma entrada que deixou de corresponder a divergência
nenhuma é reportada como obsoleta e reprova: baseline morta é silenciamento
sem dono, e ela some do radar no dia em que passa a esconder outra coisa.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# `# O schema do sistema medido, `sut`` — o nome do schema vem entre crases,
# e é o último do heading porque o texto antes dele é prosa. O nível varia:
# era `##` quando os dois schemas dividiam um arquivo, e virou `#` quando cada
# um ganhou o seu, pelo fecho de `E-78`.
HEADING_WITH_SCHEMA = re.compile(r"^#{1,3}\s+.*`([a-z_][a-z0-9_]*)`\s*$")
FENCE_OPEN = re.compile(r"^\s*(```|~~~)\s*mermaid\s*$")
FENCE_CLOSE = re.compile(r"^\s*(```|~~~)\s*$")
ER_DIAGRAM = re.compile(r"^\s*erDiagram\s*$")
# `resource {`, a entidade que abre bloco de atributos.
ENTITY_BLOCK = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*\{")
# `NOME_DE_TABELA_NAO_DECIDIDO`, a entidade sem bloco.
ENTITY_BARE = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*$")
# `resource ||--o{ allocation : "aloca"`.
RELATION = re.compile(r"^\s*([A-Za-z_][\w-]*)\s+\S*--\S*\s+([A-Za-z_][\w-]*)\s*:")
# `SCHEMA sut` cobre `CREATE SCHEMA` e `COMMENT ON SCHEMA`.
SQL_SCHEMA = re.compile(r"\bSCHEMA\s+([a-z_][a-z0-9_]*)", re.IGNORECASE)
SQL_TABLE = re.compile(
    r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
    r"(?:([a-z_][a-z0-9_]*)\.)?([a-z_][a-z0-9_]*)",
    re.IGNORECASE,
)
MIGRATIONS = "*/src/main/resources/db/migration/*.sql"


class Divergence(NamedTuple):
    key: str
    reason: str


def sources(source: Path) -> list[Path]:
    """Os arquivos a ler: os `.md` da pasta, ou o próprio arquivo dado."""
    if source.is_dir():
        return sorted(source.glob("*.md"))
    return [source]


def diagrams(source: Path) -> dict[str, set[str]]:
    """Devolve, por schema, o conjunto de entidades desenhadas.

    O schema vem do heading mais recente que termine em nome entre crases; um
    bloco mermaid sem heading assim acima dele é ignorado, porque não há a quem
    compará-lo. Um mesmo schema desenhado em dois arquivos da pasta soma as
    entidades dos dois, e não reclama: a pasta é a dona, e não cada arquivo.
    """
    found: dict[str, set[str]] = {}
    for arquivo in sources(source):
        _le(arquivo, found)
    return found


def _le(source: Path, found: dict[str, set[str]]) -> None:
    schema: str | None = None
    inside = is_er = False
    depth = 0
    for raw in source.read_text(encoding="utf-8").splitlines():
        if not inside:
            heading = HEADING_WITH_SCHEMA.match(raw)
            if heading:
                schema = heading.group(1)
            if FENCE_OPEN.match(raw):
                inside, is_er, depth = True, False, 0
            continue
        if FENCE_CLOSE.match(raw):
            inside = False
            continue
        if ER_DIAGRAM.match(raw):
            is_er = True
            if schema is not None:
                found.setdefault(schema, set())
            continue
        if not is_er or schema is None:
            continue
        if depth:
            # Dentro de um bloco de atributos: nome de coluna não é tabela.
            depth -= raw.count("}")
            continue
        block = ENTITY_BLOCK.match(raw)
        if block:
            found[schema].add(block.group(1))
            depth = 1 - raw.count("}")
            continue
        relation = RELATION.match(raw)
        if relation:
            found[schema].update(relation.groups())
            continue
        bare = ENTITY_BARE.match(raw)
        if bare:
            found[schema].add(bare.group(1))


def migrations(root: Path) -> tuple[dict[str, set[str]], dict[str, set[Path]]]:
    """Devolve, por schema, as tabelas criadas e os arquivos que o mencionam."""
    tables: dict[str, set[str]] = {}
    files: dict[str, set[Path]] = {}
    for sql in sorted(root.glob(MIGRATIONS)):
        text = sql.read_text(encoding="utf-8")
        # O comentário de uma migração cita o caminho de outra, e o `--` do SQL
        # não impede que um `CREATE TABLE` de exemplo caia aqui. Nenhuma linha
        # comentada entra na conta.
        code = "\n".join(
            line.split("--", 1)[0] for line in text.splitlines()
        )
        mentioned = {m.group(1).lower() for m in SQL_SCHEMA.finditer(code)}
        for match in SQL_TABLE.finditer(code):
            schema, table = match.group(1), match.group(2)
            if schema is None:
                # Sem qualificação, a tabela pertence ao único schema que a
                # migração menciona. Com dois ou nenhum, não há como saber, e
                # adivinhar aqui produziria divergência falsa.
                if len(mentioned) != 1:
                    continue
                schema = next(iter(mentioned))
            key = schema.lower()
            tables.setdefault(key, set()).add(table.lower())
            mentioned.add(key)
        for schema in mentioned:
            files.setdefault(schema, set()).add(sql)
            tables.setdefault(schema, set())
    return tables, files


def compare(
    drawn: dict[str, set[str]],
    created: dict[str, set[str]],
    where: dict[str, set[Path]],
) -> list[Divergence]:
    out: list[Divergence] = []
    for schema in sorted(drawn):
        if schema not in where:
            out.append(Divergence(
                f"schema-sem-migração:{schema}",
                f"o diagrama desenha o schema `{schema}`, e nenhuma migração "
                f"Flyway o menciona",
            ))
            continue
        tables = created.get(schema, set())
        for entity in sorted(drawn[schema]):
            if entity.lower() not in tables:
                out.append(Divergence(
                    f"só-no-diagrama:{schema}.{entity}",
                    "desenhada no `erDiagram` e ausente da migração",
                ))
        for table in sorted(tables):
            if table not in {e.lower() for e in drawn[schema]}:
                out.append(Divergence(
                    f"só-na-migração:{schema}.{table}",
                    "criada pela migração e ausente do `erDiagram`",
                ))
    for schema in sorted(set(created) - set(drawn)):
        for table in sorted(created[schema]):
            out.append(Divergence(
                f"só-na-migração:{schema}.{table}",
                f"criada pela migração, e o schema `{schema}` não tem diagrama "
                f"em `docs/architecture/schemas/`",
            ))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compara nome de tabela entre os `erDiagram` de "
                    "`docs/architecture/schemas/` e as migrações Flyway.",
    )
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument(
        "--source",
        type=Path,
        help="o dono da forma: a pasta, ou um arquivo dela. Por omissão, "
             "`docs/architecture/schemas/` sob a raiz.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="divergências deliberadas, uma por linha, no formato que este "
             "script imprime. Linha iniciada por `#` é comentário.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    source = args.source or root / "docs" / "architecture" / "schemas"
    if not (source.is_dir() or source.is_file()):
        print(f"fonte inexistente: {source}", file=sys.stderr)
        return 2

    drawn = diagrams(source)
    if not drawn:
        print(f"nenhum `erDiagram` sob heading com schema em {source}",
              file=sys.stderr)
        return 2
    created, where = migrations(root)
    divergences = compare(drawn, created, where)

    accepted: dict[str, bool] = {}
    if args.baseline is not None and args.baseline.is_file():
        for raw in args.baseline.read_text(encoding="utf-8").splitlines():
            entry = raw.strip()
            if entry and not entry.startswith("#"):
                accepted[entry] = False

    remaining = []
    for divergence in divergences:
        if divergence.key in accepted:
            accepted[divergence.key] = True
        else:
            remaining.append(divergence)

    for divergence in remaining:
        print(f"DIVERGÊNCIA: {divergence.key} — {divergence.reason}")
    stale = sorted(key for key, seen in accepted.items() if not seen)
    for key in stale:
        print(f"BASELINE OBSOLETA: {key} — a divergência deixou de existir, e "
              f"a entrada precisa sair da baseline")

    waived = sum(1 for seen in accepted.values() if seen)
    if waived:
        print(f"\n{waived} divergência(s) deliberada(s) na baseline.")
    print(f"\n{len(drawn)} schema(s) desenhado(s); "
          f"{len(remaining)} divergência(s) não aceita(s); "
          f"{len(stale)} entrada(s) obsoleta(s) na baseline.")
    return 1 if remaining or stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
