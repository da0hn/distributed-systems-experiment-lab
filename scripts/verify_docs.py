#!/usr/bin/env python3
"""Porta única de verificação da documentação: quatro checagens, uma execução.

Duas delas NÃO são implementadas aqui, e isso é a decisão central deste arquivo:

    citações       delegada a `scripts/check_citations.py`
    limites        delegada a `check_artifact_limits.py`, da skill
    tabelas        nativa
    fim de linha   nativa

A delegação não é economia de código. O `check_artifact_limits.py` declara ser a
ÚNICA declaração de limite do repositório e mantém uma guarda que persegue
qualquer segunda declaração — um teto reescrito aqui divergiria na primeira
decisão que mudasse a classe de um artefato, e divergiria em silêncio. A mesma
razão vale para a política de citação `C-1`: quem sabe o que é um alvo, uma
âncora GFM e um ADR abreviado é aquele script, e um segundo resolvedor
discordaria dele em algum caso de borda que ninguém testaria.

O que sobra para este arquivo é o que ainda não tinha dono. As duas verificações
nativas nasceram de estrago observado, e não de higiene abstrata: um script de
reformatação converteu um arquivo inteiro de LF para CRLF sem que o diff
acusasse, e um outro desalinhou o padding de tabelas contando bytes onde devia
contar caracteres.

O que este script NÃO faz, de propósito: conferir se o conteúdo da linha citada
sustenta a afirmação que a cita. Nenhuma citação deste repositório declara o
trecho esperado — `arquivo.md:12` é só o número —, e não há contra o que
conferir. Verificar isso exige leitura, e leitura não é trabalho de verificador.

Três modos:

    python scripts/verify_docs.py
        Varre a árvore inteira. É o modo da linha de comando e o do CI.

    python scripts/verify_docs.py --file A.md --file B.md
        Verifica só os arquivos indicados. É como o `artifact-verifier` recebe
        trabalho, e por isso é o modo do ciclo de especificação.

    python scripts/verify_docs.py --hook
        Lê no stdin o JSON de um hook `PostToolUse`, verifica SÓ o arquivo
        tocado e sai com 2 quando encontra defeito — o código que faz o Claude
        Code devolver o stderr ao agente, para conserto no mesmo turno.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Iterable, NamedTuple, Optional

CITATIONS_SCRIPT = Path("scripts/check_citations.py")
CITATIONS_BASELINE = Path("scripts/citations-baseline.txt")
LIMITS_SCRIPT = Path(
    ".claude/skills/feature-planning/scripts/check_artifact_limits.py"
)
# A baseline das duas verificações NATIVAS. As delegadas têm a sua, e ela é do
# verificador que é dono delas — uma segunda lista de tolerâncias para citação
# divergiria da primeira no primeiro defeito aceito por só uma das duas.
BASELINE = Path("scripts/verify-docs-baseline.txt")

# `docs/adr/arquivo/**` registra o que se pensava naquela data, e o `AGENTS.md`
# proíbe editá-lo. Um defeito de forma ali é inconsertável por construção, e
# acusá-lo deixa o verificador permanentemente vermelho — o mesmo argumento com
# que `C-7` isentou os quatro ADRs legados do limite.
FROZEN = Path("docs/adr/arquivo")

# O bloco cercado sai da varredura de tabelas: um `flowchart` do Mermaid e um
# exemplo de saída de terminal contêm pipes que não são coluna de nada.
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
# `---`, `:---`, `---:` e `:---:`, com ou sem espaço em volta.
SEPARATOR_CELL = re.compile(r"^\s*:?-+:?\s*$")


class Defect(NamedTuple):
    path: Path
    line: Optional[int]
    reason: str
    # A chave da baseline. O número da LINHA fica de fora de propósito: ele muda a
    # cada edição do arquivo, e uma baseline que envelhece a cada commit não serve
    # para nada. É a mesma escolha que o `check_citations.py` já tinha feito.
    key: str

    def render(self, root: Path) -> str:
        shown = self.path.relative_to(root).as_posix()
        where = f"{shown}:{self.line}" if self.line else shown
        return f"DEFEITO: {where} — {self.reason}"


def defect(check: str, path: Path, root: Path, line: Optional[int], reason: str,
           key_reason: Optional[str] = None) -> Defect:
    # A chave nomeia a VERIFICAÇÃO que a produziu. Sem isso, a guarda de entrada
    # obsoleta de cada checagem lê as entradas da outra como órfãs, e as duas
    # reprovam uma à outra — que foi exatamente o que aconteceu na primeira
    # execução com baseline.
    shown = path.relative_to(root).as_posix()
    return Defect(path, line, reason, f"{check}::{shown}:{key_reason or reason}")


def load_baseline(path: Optional[Path]) -> set[str]:
    if path is None or not path.is_file():
        return set()
    entries = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        entry = raw.strip()
        if entry and not entry.startswith("#"):
            entries.add(entry)
    return entries


def apply_baseline(
    check: str, defects: list[Defect], accepted: set[str], root: Path, scoped: bool
) -> tuple[list[str], bool]:
    """Separa o que a baseline aceita do que ela não alcança.

    Uma entrada da baseline que não casa com nada REPROVA — a linha autoriza uma
    tolerância que já foi resolvida, e deixá-la ali esconderia a próxima
    ocorrência do mesmo defeito. A guarda só vale na varredura completa: no modo
    escopado, o script vê um arquivo só, e as outras entradas não deixaram de
    casar — elas apenas não foram olhadas.
    """
    remaining = [d for d in defects if d.key not in accepted]
    waived = len(defects) - len(remaining)
    linhas = [d.render(root) for d in remaining]
    if waived:
        linhas.append(f"{waived} defeito(s) conhecido(s) e aceito(s) na baseline.")
    obsolete: set[str] = set()
    if not scoped:
        owned = {k for k in accepted if k.startswith(f"{check}::")}
        obsolete = owned - {d.key for d in defects}
        for entry in sorted(obsolete):
            linhas.append(f"BASELINE OBSOLETA: {entry} — já não ocorre; apague a linha")
    return linhas, bool(remaining) or bool(obsolete)


class Outcome(NamedTuple):
    name: str
    failed: bool
    report: str


# --------------------------------------------------------------------------
# As duas verificações delegadas
# --------------------------------------------------------------------------


def run_delegate(name: str, command: list[str], root: Path) -> Outcome:
    """Roda um verificador que já existe e repassa a saída dele, literal.

    A saída NÃO é reformatada nem resumida. Quem lê o relatório precisa poder
    reconhecer a mensagem do verificador original para saber onde consertar, e
    um agregador que reescreve a mensagem alheia cria um segundo vocabulário
    para o mesmo defeito.
    """
    # No Windows, um Python filho com a saída redirecionada para um pipe escreve
    # na codepage do console — cp1252 — e não em UTF-8. Cada `ç` de mensagem em
    # português volta como byte solto e derruba a decodificação. `PYTHONIOENCODING`
    # corrige na origem: o filho passa a escrever UTF-8, em vez de o agregador
    # tolerar bytes quebrados e exibir defeito ilegível.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    try:
        finished = subprocess.run(
            command, cwd=root, capture_output=True, text=True,
            encoding="utf-8", env=env,
        )
    except OSError as error:
        return Outcome(name, True, f"ERRO: não foi possível executar — {error}")
    saida = (finished.stdout or "").strip()
    erro = (finished.stderr or "").strip()
    partes = [p for p in (saida, erro) if p]
    return Outcome(name, finished.returncode != 0, "\n".join(partes))


def check_citations(root: Path, scope: Optional[list[Path]]) -> Outcome:
    command = [
        sys.executable,
        CITATIONS_SCRIPT.as_posix(),
        "--root",
        ".",
        "--baseline",
        CITATIONS_BASELINE.as_posix(),
    ]
    if scope is not None:
        markdown = [p for p in scope if p.suffix == ".md"]
        if not markdown:
            return Outcome("citações", False, "nada a verificar neste arquivo.")
        for path in markdown:
            command += ["--file", path.relative_to(root).as_posix()]
    return run_delegate("citações", command, root)


def measured_files(root: Path) -> list[Path]:
    """Os artefatos que o medidor de limites alcança.

    O CI mede `docs/**/*.md`. O `behavior.feature` entra aqui também: o medidor
    já carrega a classe `bdd` com teto próprio, e até agora nada a exercia — o
    teto existia e ninguém o media.
    """
    found = sorted(root.glob("docs/**/*.md"))
    found += sorted(root.glob("docs/**/behavior.feature"))
    return found


def check_limits(root: Path, scope: Optional[list[Path]]) -> Outcome:
    alvos = measured_files(root) if scope is None else [
        p for p in scope if p in set(measured_files(root))
    ]
    if not alvos:
        return Outcome("limites", False, "nada a medir neste arquivo.")
    command = [sys.executable, LIMITS_SCRIPT.as_posix(), "--root", "."]
    for path in alvos:
        command += ["--file", path.relative_to(root).as_posix()]
    outcome = run_delegate("limites", command, root)
    if scope is not None:
        return outcome
    # Na árvore inteira o medidor imprime uma linha por arquivo, e cento e tantas
    # linhas de `OK` afogam o que importa. O relatório completo continua a uma
    # chamada de distância; aqui fica o que exige ação e a contagem do resto.
    linhas = outcome.report.splitlines()
    ruido = [l for l in linhas if l.startswith(("OK:", "ISENTO:"))]
    resto = [l for l in linhas if not l.startswith(("OK:", "ISENTO:"))]
    resumo = f"{len(ruido)} arquivo(s) dentro do teto ou isento(s)."
    return Outcome("limites", outcome.failed, "\n".join([*resto, resumo]).strip())


# --------------------------------------------------------------------------
# Tabelas: o padding conta CARACTERES, e nunca bytes
# --------------------------------------------------------------------------


def cell_width(cell: str) -> int:
    """A largura de uma célula, em caracteres — a unidade que o alinhamento vê.

    Duas armadilhas moram nesta função, e as duas produzem tabela torta que
    parece certa na tela de quem a escreveu.

    A primeira é o byte. `len(b"não")` é 4 e `len("não")` é 3, e um script que
    mede o buffer em vez do texto pede um caractere a mais de padding para toda
    célula acentuada. Em português isso alcança quase toda linha de tabela.

    A segunda é a forma de normalização. `ã` tem duas representações Unicode: um
    ponto de código só (NFC) ou `a` seguido do til combinante (NFD). As duas se
    desenham iguais e `len` devolve 3 e 4. O NFD chega por editor de outra
    plataforma e por copiar-e-colar, e sem a normalização o verificador
    acusaria uma tabela visualmente perfeita.

    A terceira é o escape, e ela é a mesma família das outras duas um nível
    adiante: a barra invertida de `\\|` ocupa um caractere na fonte e NENHUM na
    tela, porque o renderizador a consome. Alinhar pelo texto de fonte deixa
    torta a linha que precisou escapar um pipe — e é justamente a linha que
    ninguém confere, porque ela parece a mais complicada da tabela.
    """
    text = unicodedata.normalize("NFC", cell)
    return len(text) - text.count("\\|")


def split_cells(line: str) -> list[str]:
    """As células BRUTAS entre os pipes, com o padding preservado.

    O padding é justamente o que se quer medir, então nada de `strip`. O `\\|`
    escapado é conteúdo de célula, e não fronteira de coluna.
    """
    body = line.strip()[1:-1]
    cells: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body) and body[index + 1] == "|":
            current.append("\\|")
            index += 2
            continue
        if char == "|":
            cells.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    cells.append("".join(current))
    return cells


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return len(stripped) > 1 and stripped.startswith("|") and stripped.endswith("|")


def table_blocks(text: str) -> Iterable[list[tuple[int, str]]]:
    """Cada sequência contígua de linhas de tabela, fora de bloco cercado."""
    fence: Optional[str] = None
    block: list[tuple[int, str]] = []
    for number, line in enumerate(text.split("\n"), 1):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                if block:
                    yield block
                    block = []
                continue
        elif match and match.group(1)[0] == fence:
            fence = None
            continue
        if fence is not None:
            continue
        if is_table_line(line):
            block.append((number, line))
        elif block:
            yield block
            block = []
    if block:
        yield block


def inspect_tables(path: Path, root: Path) -> list[Defect]:
    text = path.read_text(encoding="utf-8", errors="replace")
    defects: list[Defect] = []
    for block in table_blocks(text):
        # Uma tabela é cabeçalho mais separador. Duas linhas soltas iniciadas por
        # pipe não são tabela nenhuma, e exigir padding delas inventaria defeito.
        if len(block) < 2:
            continue
        separator = split_cells(block[1][1])
        if not all(SEPARATOR_CELL.match(cell) for cell in separator):
            continue
        rows = [(number, split_cells(line)) for number, line in block]
        expected = len(rows[0][1])
        ragged = [(n, c) for n, c in rows if len(c) != expected]
        if ragged:
            for number, cells in ragged:
                defects.append(defect(
                    "tabelas", path, root, number,
                    f"a linha tem {len(cells)} coluna(s), e o cabeçalho da "
                    f"tabela tem {expected} — há um pipe sem escapar na célula",
                    f"linha de {len(cells)} colunas em tabela de {expected}",
                ))
            # Com o número de colunas divergente, comparar largura por índice
            # alinharia colunas diferentes e produziria uma cascata de defeito
            # inventado. O conserto é a contagem, e ele vem primeiro.
            continue
        for column in range(expected):
            larguras = {cell_width(cells[column]) for _, cells in rows}
            if len(larguras) == 1:
                continue
            alvo = max(larguras)
            for number, cells in rows:
                atual = cell_width(cells[column])
                if atual == alvo:
                    continue
                defects.append(defect(
                    "tabelas", path, root, number,
                    f"coluna {column + 1} com {atual} caractere(s), e a mais "
                    f"larga da tabela tem {alvo}",
                    # A chave nomeia a COLUNA e a largura da tabela, e não a
                    # largura da célula torta. Assim uma tolerância cobre as
                    # dezenove linhas de uma mesma coluna numa entrada só, e uma
                    # tabela NOVA no mesmo arquivo — que terá outra largura — não
                    # é mascarada pela linha que tolerou a antiga.
                    f"coluna {column + 1} em tabela de largura {alvo}",
                ))
    return defects


def check_tables(
    root: Path, scope: Optional[list[Path]], accepted: set[str]
) -> Outcome:
    alvos = scope if scope is not None else sorted(root.glob("docs/**/*.md")) + \
        sorted(root.glob("*.md"))
    alvos = [p for p in alvos if p.suffix == ".md" and not is_frozen(p, root)]
    defects = [d for path in alvos for d in inspect_tables(path, root)]
    linhas, failed = apply_baseline(
        "tabelas", defects, accepted, root, scope is not None)
    linhas.append(
        f"{len(alvos)} arquivo(s) varrido(s); {len(defects)} defeito(s) de padding."
    )
    return Outcome("tabelas", failed, "\n".join(linhas))


# --------------------------------------------------------------------------
# Fim de linha
# --------------------------------------------------------------------------


def is_frozen(path: Path, root: Path) -> bool:
    return (root / FROZEN) in path.parents


def tracked_files(root: Path) -> list[Path]:
    """Os arquivos versionados, pelo git.

    A varredura parte do git, e não do disco: `.venv/`, `node_modules/` e
    `target/` carregam milhares de arquivos que não são deste repositório, e um
    CRLF dentro de uma dependência não é defeito de ninguém aqui.

    `--others --exclude-standard` acrescenta o que ainda NÃO foi adicionado ao
    índice, respeitando o `.gitignore`. Sem ele a varredura completa não via
    arquivo recém-criado — e um arquivo recém-criado por script é justamente
    onde o CRLF aparece. O defeito era observável: um arquivo novo em CRLF
    passava na árvore inteira e só era pego pelo hook, que olha o caminho
    tocado em vez de perguntar ao índice.
    """
    finished = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root, capture_output=True,
    )
    if finished.returncode != 0:
        return []
    nomes = finished.stdout.decode("utf-8", errors="replace").split("\0")
    return [root / name for name in nomes if name]


def has_crlf(path: Path) -> Optional[int]:
    """Quantas quebras CRLF o arquivo tem, ou None quando ele é binário.

    A leitura é em BYTES de propósito. Aberto em modo texto, o Python traduz
    `\\r\\n` para `\\n` na entrada e o verificador não veria nada — que é a mesma
    razão pela qual o `git` com `core.autocrlf=input` mostra um diff limpo para
    um arquivo que está CRLF no disco. O estrago é invisível justamente para as
    duas ferramentas com que se costuma procurá-lo.
    """
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw[:8000]:
        return None
    return raw.count(b"\r\n")


def check_line_endings(
    root: Path, scope: Optional[list[Path]], accepted: set[str]
) -> Outcome:
    alvos = tracked_files(root) if scope is None else scope
    defects: list[Defect] = []
    varridos = 0
    for path in alvos:
        if not path.is_file():
            continue
        count = has_crlf(path)
        if count is None:
            continue
        varridos += 1
        if count:
            defects.append(defect(
                "fim-de-linha", path, root, None,
                f"{count} quebra(s) de linha em CRLF; o repositório é LF",
                # A CONTAGEM fica fora da chave: ela muda a cada linha escrita no
                # arquivo, e uma tolerância que se desfaz por edição de conteúdo
                # acusaria o arquivo errado.
                "CRLF",
            ))
    linhas, failed = apply_baseline(
        "fim-de-linha", defects, accepted, root, scope is not None)
    linhas.append(
        f"{varridos} arquivo(s) de texto varrido(s); {len(defects)} com CRLF."
    )
    return Outcome("fim de linha", failed, "\n".join(linhas))


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------


def verify(
    root: Path, scope: Optional[list[Path]], accepted: set[str]
) -> list[Outcome]:
    return [
        check_citations(root, scope),
        check_limits(root, scope),
        check_tables(root, scope, accepted),
        check_line_endings(root, scope, accepted),
    ]


def write_baseline(root: Path, path: Path) -> int:
    """Congela o estado atual das duas verificações nativas.

    A baseline existe porque um verificador que nasce vermelho em seis arquivos
    quentes é um verificador que se aprende a ignorar — foi o argumento com que
    `C-7` isentou os ADRs legados do limite, e ele vale igual aqui. O que ela
    NÃO é: perdão permanente. Cada linha é uma dívida nomeada, e a guarda de
    entrada obsoleta obriga a apagá-la assim que o defeito for consertado.
    """
    alvos = sorted(root.glob("docs/**/*.md")) + sorted(root.glob("*.md"))
    defects = [
        d for p in alvos if p.suffix == ".md" and not is_frozen(p, root)
        for d in inspect_tables(p, root)
    ]
    for candidate in tracked_files(root):
        if candidate.is_file() and has_crlf(candidate):
            defects.append(defect("fim-de-linha", candidate, root, None, "CRLF"))
    chaves = sorted({d.key for d in defects})
    cabecalho = [
        "# Defeitos de forma conhecidos e aceitos, um por linha.",
        "#",
        "# Gerado por `python scripts/verify_docs.py --atualizar-baseline`, e",
        "# consultado pelas duas verificações NATIVAS: tabelas e fim de linha. As",
        "# outras duas têm baseline própria, do verificador que é dono delas.",
        "#",
        "# O número da linha NÃO entra na chave: ele muda a cada edição do",
        "# arquivo, e uma baseline que envelhece a cada commit não serve para nada.",
        "#",
        "# Uma entrada que deixe de casar com um defeito REPROVA a verificação. Uma",
        "# linha que autoriza uma tolerância já resolvida esconderia a próxima",
        "# ocorrência do mesmo defeito, que é o oposto do que a baseline existe",
        "# para fazer. Consertou, apague a linha.",
        "",
    ]
    path.write_text("\n".join(cabecalho + chaves) + "\n", encoding="utf-8",
                    newline="\n")
    return len(chaves)


def render(outcomes: list[Outcome], stream) -> None:
    for outcome in outcomes:
        estado = "DEFEITO" if outcome.failed else "ok"
        print(f"== {outcome.name} == [{estado}]", file=stream)
        print(outcome.report or "(sem saída)", file=stream)
        print(file=stream)
    print("resumo:", file=stream)
    for outcome in outcomes:
        print(f"  {outcome.name:<14} {'DEFEITO' if outcome.failed else 'ok'}",
              file=stream)


def hook_target(root: Path) -> Optional[Path]:
    """O arquivo que a ferramenta acabou de tocar, vindo do JSON no stdin.

    Devolve None quando não há o que verificar — stdin vazio, JSON quebrado,
    ferramenta sem caminho, ou caminho fora deste repositório. Nenhum desses é
    defeito de documentação, e nenhum deles pode reprovar uma edição.
    """
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (json.JSONDecodeError, OSError):
        return None
    tool_input = payload.get("tool_input") or {}
    written = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not written:
        return None
    try:
        candidate = Path(written).resolve()
        candidate.relative_to(root)
    except (OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verifica citações, limites, tabelas e fim de linha."
    )
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=BASELINE,
        help="Defeitos de forma conhecidos e aceitos, das duas verificações "
             "nativas. As delegadas usam a baseline do verificador dono delas.",
    )
    parser.add_argument(
        "--atualizar-baseline",
        dest="atualizar",
        action="store_true",
        help="Reescreve a baseline com o estado atual da árvore e sai. Use ao "
             "adotar o verificador, e NUNCA para calar um defeito recém-criado.",
    )
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        default=[],
        type=Path,
        metavar="CAMINHO",
        help="Verifica só os arquivos indicados, em vez da árvore inteira. "
             "Repetível. É a forma como o `artifact-verifier` recebe trabalho: "
             "uma lista de caminhos alterados. A guarda de baseline obsoleta "
             "NÃO roda neste modo — as outras entradas não deixaram de casar, "
             "elas apenas não foram olhadas.",
    )
    parser.add_argument(
        "--hook",
        action="store_true",
        help="Lê o JSON de um hook `PostToolUse` no stdin e verifica só o "
             "arquivo tocado. Sai com 2 quando há defeito, que é o código com "
             "que o Claude Code devolve o stderr ao agente.",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    if args.files and args.hook:
        print("ERRO: --file e --hook são modos distintos; use um deles.",
              file=sys.stderr)
        return 1

    if args.atualizar:
        total = write_baseline(root, root / args.baseline)
        print(f"{args.baseline.as_posix()}: {total} defeito(s) congelado(s).")
        return 0

    accepted = load_baseline(root / args.baseline)

    if not args.hook:
        scope: Optional[list[Path]] = None
        if args.files:
            scope = []
            for written in args.files:
                candidate = (root / written).resolve()
                try:
                    candidate.relative_to(root)
                except ValueError:
                    print(f"ERRO: fora da raiz: {written}", file=sys.stderr)
                    return 1
                if not candidate.is_file():
                    print(f"ERRO: arquivo ausente: {written}", file=sys.stderr)
                    return 1
                # O arquivo congelado é pedido junto quando alguém passa o que o
                # `git status` devolveu. Ignorá-lo em silêncio seria esconder que
                # ele não foi medido; dizer que foi seria mentira.
                if is_frozen(candidate, root):
                    print(f"IGNORADO: {written} — arquivo congelado, não é medido")
                    continue
                scope.append(candidate)
            if not scope:
                print("nada a verificar.")
                return 0
        outcomes = verify(root, scope, accepted)
        render(outcomes, sys.stdout)
        return 1 if any(o.failed for o in outcomes) else 0

    target = hook_target(root)
    if target is None or is_frozen(target, root):
        return 0
    try:
        outcomes = verify(root, [target], accepted)
    except Exception as error:  # noqa: BLE001
        # Uma falha DESTE script não pode barrar a edição de ninguém. O código 1
        # mostra o erro à pessoa sem devolver nada ao agente; o 2, que barra, é
        # reservado para defeito de documentação de verdade.
        print(f"verify_docs falhou: {error}", file=sys.stderr)
        return 1
    if not any(o.failed for o in outcomes):
        return 0
    render([o for o in outcomes if o.failed], sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
