#!/usr/bin/env python3
"""Recusa identificador repetido na fila de decisões.

Nasceu do fecho de `E-73`, em 2026-08-12. `E-62` e `E-63` nomearam duas linhas
cada um: os dois pares nasceram no mesmo dia, em worktrees que corriam em
paralelo, e a mesclagem juntou os quatro sem que nada acusasse a colisão.

**A colisão é silenciosa porque a âncora continua resolvendo.** O slug GFM
carrega o título inteiro, e não só o identificador, de modo que dois headings
com o mesmo `E-NN` produzem endereços distintos e o `check_citations.py` passa
nos dois. O que quebra é a citação por IDENTIFICADOR — "a linha `E-62`" deixa
de nomear uma linha —, e é assim que este repositório cita a fila em prosa, no
`AGENTS.md` e nos ADRs.

Uma regra, e nenhuma além dela: **um identificador tem no máximo UM enunciado.**
Um enunciado é o heading `#### `E-NN` — <título>`, com travessão; um fecho é o
heading `#### `E-NN` fecha <...>`, e um identificador pode ter vários.

**Fecho sem enunciado NÃO é defeito, e a primeira versão deste script errou
nisso.** Ele acusou doze, e os doze eram poda executada corretamente: a fila
apaga a narrativa quando a linha fecha e deixa só o fecho, por decisão. Uma
regra que não distingue poda de renumeração esquecida produz doze vermelhos
falsos e treina quem lê a ignorar o verdadeiro. Os órfãos passaram a ser
contados e mostrados, e não reprovam.

O script NÃO confere numeração contígua. Buraco na sequência é normal: um
identificador reservado e não usado não quebra citação nenhuma, e exigir
contiguidade obrigaria a renumerar por estética, que é exatamente o custo que
o fecho de `E-73` aceitou pagar uma vez e não quer repetir.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_QUEUE = Path("docs/fila-de-decisoes.md")

# `### ` ou `#### `, seguido do identificador entre crases. O restante da linha
# decide se é enunciado ou fecho.
HEADING = re.compile(r"^#{3,4}\s+`(E-\d+)`\s*(.*)$")

# O travessão que separa o identificador do título de um enunciado. Aceita o
# travessão longo e o hífen, porque a fila usa o longo e um deslize com hífen
# não deveria virar fecho por acidente.
ENUNCIADO = re.compile(r"^[—-]\s*\S")


def scan(text: str) -> tuple[dict[str, list[tuple[int, str]]], list[tuple[int, str, str]]]:
    """Devolve os enunciados por identificador, e os fechos como lista."""
    enunciados: dict[str, list[tuple[int, str]]] = defaultdict(list)
    fechos: list[tuple[int, str, str]] = []
    for number, line in enumerate(text.split("\n"), 1):
        match = HEADING.match(line)
        if not match:
            continue
        identifier, rest = match.group(1), match.group(2).strip()
        if ENUNCIADO.match(rest):
            enunciados[identifier].append((number, rest))
        else:
            fechos.append((number, identifier, rest))
    return enunciados, fechos


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recusa identificador repetido na fila de decisões."
    )
    parser.add_argument("--root", default=".", help="Raiz do repositório.")
    parser.add_argument(
        "--file",
        default=str(DEFAULT_QUEUE),
        help="Caminho da fila, relativo à raiz.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    queue = root / args.file
    if not queue.is_file():
        print(f"ERRO: fila não encontrada: {args.file}", file=sys.stderr)
        return 1

    with io.open(queue, encoding="utf-8") as handle:
        text = handle.read()

    enunciados, fechos = scan(text)
    defeitos: list[str] = []

    for identifier, ocorrencias in sorted(enunciados.items()):
        if len(ocorrencias) > 1:
            onde = ", ".join(f"linha {n}" for n, _ in ocorrencias)
            defeitos.append(
                f"`{identifier}` nomeia {len(ocorrencias)} linhas ({onde}). "
                "Citar por identificador deixou de ser possível."
            )
            for number, titulo in ocorrencias:
                defeitos.append(f"    {number}: {titulo}")

    # Fecho sem enunciado é o estado NORMAL de uma linha podada, e por isso é
    # contado e não acusado. Ver o cabeçalho deste arquivo.
    orfaos = [f for f in fechos if f[1] not in enunciados]

    total = sum(len(v) for v in enunciados.values())
    resumo = (
        f"{total} enunciado(s), {len(fechos)} fecho(s), "
        f"{len(orfaos)} fecho(s) de linha podada"
    )
    if defeitos:
        for defeito in defeitos:
            print(defeito)
        print()
        print(f"{resumo}; {len(defeitos)} defeito(s).")
        return 1

    print(f"{resumo}; nenhum identificador repetido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
