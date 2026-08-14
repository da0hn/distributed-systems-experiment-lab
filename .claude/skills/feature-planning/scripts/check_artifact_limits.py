#!/usr/bin/env python3
"""Validate the character budgets for feature-planning artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


# As CLASSES de artefato, e o teto de cada uma. A pessoa decidiu em 2026-08-12,
# no fecho do orçamento de prosa: o teto passa a ser propriedade da CLASSE, e não
# do caminho. A diferença é o que acontece com um arquivo novo — antes ele caía no
# genérico de 4.000 até alguém escrever uma entrada para ele, e agora ele cai na
# classe que o padrão de caminho o alcança.
#
# `None` significa isento, e cada isenção carrega o motivo dela abaixo. O que a
# decisão substituiu foi o regime de isenção uma a uma, cujo defeito era o critério
# ficar implícito na soma das justificativas: cada entrada dizia por que aquele
# arquivo escapava, e nenhuma dizia contra o que a próxima seria conferida.
CLASS_LIMITS = {
    # Instrução: os dois `AGENTS.md`, os `.claude/agents/*.md` e os
    # `.claude/skills/**/*.md`. O harness os carrega inteiros antes de existir
    # qualquer consulta, e o que eles carregam é guardrail — a regra que o agente
    # precisa ANTES de saber o que procurar. Cortar prosa deles apaga guardrail, e
    # não redundância.
    #
    # O teto genérico foi calibrado para o Feature Card, onde o excesso é sinal de
    # que a capacidade cobre demais e o caminho é dividi-la. Um arquivo de instrução
    # não se divide: um `feature-writer` partido em dois produz um escritor que
    # ignora metade das regras. A pessoa decidiu isentá-los em 2026-08-10, depois de
    # medi-los entre 5.394 e 21.322 caracteres contra o genérico de 4.000.
    #
    # A isenção NÃO alcança a guarda de `INSTRUCTIONS_WITHOUT_LIMITS`: esses
    # arquivos continuam proibidos de declarar limite próprio, e essa checagem roda
    # à parte.
    "instrução": None,
    # Índice e inventário: `docs/*/README.md`. Eles crescem por ENTRADA — um ADR
    # aceito, uma capacidade especificada, um contrato nascido, uma questão
    # encaminhada —, e a prosa em volta não cresce junto. Um teto ali obrigaria a
    # omitir do inventário, que é o oposto do que o arquivo existe para fazer, e a
    # omissão seria invisível: ninguém sente falta do que nunca foi listado.
    #
    # A pessoa isentou `docs/adr/README.md` em 2026-08-07, `docs/features/README.md`
    # em 2026-08-10 e `docs/contracts/README.md` em 2026-08-11, cada um depois de
    # estourar por acréscimo de LINHA DE TABELA, e não por prosa nova. A classe
    # generaliza os três, e alcança o índice de questões e o próximo que nascer.
    #
    # `docs/README.md` NÃO é desta classe: ele é roteador, tem dono único do
    # roteamento documental e cai no genérico como qualquer outro Markdown.
    "índice": None,
    # A fila existe só para rastrear pendência, e por isso é a única exceção ao
    # princípio de fonte única: ela fala do que outros documentos vão possuir. Ela
    # cresce por decisão enfileirada e encolhe por lápide, e um teto ali obrigaria a
    # apagar pendência viva para caber. A pessoa isentou em 2026-08-07.
    "fila": None,
    # `docs/adr/arquivo/**` é registro congelado do que se pensou naquela data, e o
    # `AGENTS.md` proíbe editá-lo. Um teto sobre o que não pode ser editado só produz
    # vermelho permanente, que deixa de ser lido.
    "arquivo congelado": None,
    # O `example-mapping.md` cresce por exemplo acrescentado, e acrescentar exemplo é
    # o trabalho dele — um teto ali transforma "achei mais um contraexemplo" em
    # "preciso apagar um dos antigos". Decisão de 2026-08-06.
    "example mapping": None,
    # Os quatro primeiros ADRs foram escritos sob outra prática, têm cerca de 35 mil
    # caracteres, e nunca caberão em limite nenhum. A imutabilidade do corpo foi
    # revogada em 2026-08-07 e a isenção continua: o que a revogação autoriza é o
    # PATCH, e encolher a prosa desses quatro seria reescrever o argumento, que o
    # patch NÃO DEVE tocar. Decisão `C-7`.
    "adr legado": None,
    # Um ADR carrega uma decisão, o argumento dela e as alternativas descartadas.
    # Estourar é sinal de que ele cobre mais de uma decisão, e a saída é a DIVISÃO —
    # sexta forma do lifecycle desde 2026-08-11 —, e não afrouxar a régua. Foi
    # exatamente esse argumento que descartou "teto próprio para o ADR-0014" em
    # 2026-08-11, e ele vale para a classe inteira.
    "adr": 12000,
    # O ADR-0015 é o único com teto próprio dentro da classe, e o motivo é o par que
    # ele forma com o dono da forma das tabelas: ele roteia a FORMA para lá e
    # continua carregando a DECISÃO — chave, discriminador e colunas de tempo —, de
    # modo que paga o custo de prosa das duas coisas. Os 12.000 não previram esse
    # roteamento. A pessoa decidiu em 2026-08-11, e a folga é estreita de propósito.
    "adr com roteamento de forma": 12600,
    # Contrato formal. O número entra na classe pelo formato, e não pelo caminho.
    "contrato": 16000,
    # O plano não é inventário: ele cresce por prosa analítica, e não por entrada.
    # Mas ele também não se divide sem quebrar as âncoras que ADRs e cards citam
    # nele. O teto próprio devolve significado ao vermelho — o `EXCEDE` permanente de
    # 48.269 contra 4.000 treinava todo mundo a ignorá-lo. O número é deliberadamente
    # apertado: o plano passa agora, e reprova de novo se crescer. Decidido em
    # 2026-08-11.
    "plano analítico": 50000,
    # `docs/architecture/**`. Esta classe cresce por FRONTEIRA documentada e por
    # ausência sustentada com evidência, e não por capacidade — a régua do Feature
    # Card não a descreve. O número herda o teto que a pessoa deu a `integrations.md`
    # em decisão anterior, e vale agora para a pasta inteira.
    "arquitetura": 12000,
    # Um card acima do limite cobre mais de uma capacidade, e o caminho é dividi-la.
    # O corte sai da prosa, NUNCA da evidência.
    "feature card": 5500,
    # Ancorado no teto do Feature Card em 2026-08-12, e a âncora é imperfeita de
    # propósito: o card mede só prosa, e a classe `bdd` mede tudo — em Gherkin a
    # tabela `Exemplos:` é o cenário, e não ilustração dele. O aperto é o sinal. O
    # 3500 anterior foi calibrado antes de qualquer card ter dezenove regras
    # aprovadas; com elas, ele cobrava menos de um cenário por regra.
    "bdd": 5500,
    "plano de implementação": 7000,
    # `docs/propostas/**`. Uma proposta de modelagem cresce por DECISÃO ASSUMIDA, e
    # assumir decisão é o trabalho dela — a pessoa exigiu que o modelo represente o
    # sistema na versão final, o que obriga cada proposta a escolher o que ainda não foi
    # decidido e a declarar cada escolha. O teto do genérico media outra coisa: ele é
    # calibrado para o Feature Card, cujo estouro significa "cobre mais de uma
    # capacidade". Aqui o estouro não significa isso — uma proposta cobre um schema, e
    # dividi-la produziria "parte 1" e "parte 2" sem costura natural, o que piora o
    # debate em vez de melhorá-lo.
    #
    # A saída NÃO é isentar, e o precedente seguido é o do `plano analítico`: um teto
    # deliberadamente apertado devolve significado ao vermelho, enquanto um `EXCEDE`
    # permanente treina todo mundo a ignorá-lo. O número passa por folga estreita a
    # maior proposta escrita até agora, e reprova de novo se ela crescer.
    "proposta de modelagem": 11000,
    # Tudo o que nenhuma classe acima alcança. Calibrado para o Feature Card.
    "genérico": 4000,
}

# TRIAGEM. A pessoa pôs uma condição ao estender a medição a todo `.md` sob `docs/`,
# em 2026-08-12, na letra: os arquivos que JÁ ultrapassavam "devem ser avaliados caso
# a caso". Estes são os que excedem a classe que os alcança e cuja classe própria
# ainda não foi decidida. Enquanto estiverem aqui o script os reporta como `TRIAGEM`
# e NÃO reprova — estender o alcance é o que PRODUZ esta lista, e nenhum arquivo sai
# dela sem decisão escrita.
#
# Isto NÃO é isenção em massa, e a diferença é que uma isenção não tem fim previsto
# e esta lista tem: cada entrada some quando a classe dela for decidida, e a lista
# vazia é o estado final.
#
# Um eixo que a triagem precisa, medido em 2026-08-12: um arquivo pode ter crescido
# porque alguém ESCREVEU, ou porque alguém MOVEU um bloco de um arquivo isento para
# um medido. O `specification-process.md` foi de 18.493 para 22.510 sem que uma frase
# fosse escrita — os 4.017 são a seção de redação e revisão independente, realocada
# do `AGENTS.md`. Punir esse salto como inchaço puniria exatamente o movimento certo.
TRIAGE_PENDING = {
    # Glossário de domínio. Mede mais de nove vezes o genérico, e a classe dele não
    # foi decidida: ele cresce por termo resolvido, o que o aproxima de inventário,
    # e carrega doutrina de vocabulário, o que o aproxima de instrução.
    Path("docs/CONTEXT.md"),
    # Processo de especificação. Cresce por regra de processo decidida, e recebeu em
    # 2026-08-12 um bloco inteiro vindo do `AGENTS.md`, que era isento.
    Path("docs/specification-process.md"),
    # Excede a classe `arquitetura` por 314 caracteres. Ele é a matriz de fronteiras,
    # e cresce por fronteira; se a classe descreve mal a matriz, ou se a matriz é que
    # precisa encolher, não foi decidido.
    Path("docs/architecture/integrations.md"),
    # Auditoria. Ela é registro DATADO de um exame, e não prosa viva: cada achado
    # carrega a data em que foi verdade. Encolhê-la apaga evidência, que é o mesmo
    # argumento de `docs/adr/arquivo/**` — se é a mesma classe daquele, ou uma classe
    # própria com teto, ninguém decidiu.
    Path("docs/audits/2026-08-06-coerencia-e-limites-documentais.md"),
    # Uma questão encaminhada cresce por objeção registrada, e o índice de questões
    # já é isento como inventário. Se a questão individual é da mesma classe que o
    # índice dela, ou do genérico que a alcança hoje, não foi decidido. Esta é a
    # única das trinta e tantas que excede, e por 282 caracteres.
    Path("docs/questions/Q-0001-1.md"),
}

# Classificadores, em ordem de precedência: o PRIMEIRO que casar decide a classe.
# A ordem importa — `docs/adr/arquivo/**` precisa vir antes de `docs/adr/[0-9]*.md`,
# e o nome de arquivo precisa vir antes do padrão de pasta.
INSTRUCTION_NAMES = {"AGENTS.md", "CLAUDE.md"}
INSTRUCTION_ROOTS = (Path(".claude/agents"), Path(".claude/skills"))
ARCHIVE_ROOT = Path("docs/adr/arquivo")
QUEUE_PATH = Path("docs/fila-de-decisoes.md")
PLAN_PATH = Path("docs/plano-do-laboratorio.md")
ADR_ROUTING_FORM = Path(
    "docs/adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md"
)
ARCHITECTURE_ROOT = Path("docs/architecture")
PROPOSALS_ROOT = Path("docs/propostas")
ROUTER_PATH = Path("docs/README.md")

CLASS_BY_NAME = {
    "feature-card.md": "feature card",
    "behavior.feature": "bdd",
    "implementation-plan.md": "plano de implementação",
    "example-mapping.md": "example mapping",
}

# Um arquivo marcado como inativo não guia ninguém, e o limite existe para manter
# prosa viva focada. A pessoa decidiu em 2026-08-07 isentá-lo enquanto a marca
# estiver lá, e a isenção é reversível por construção: apagar o cabeçalho devolve o
# teto no mesmo instante, sem ninguém precisar lembrar de mexer neste script.
#
# Sem ela, a própria marcação punia quem a cumpriu: o cabeçalho custa cerca de 290
# letras, e foi ele que levou `deteccao-de-protecao-inerte/behavior.feature` de 3299
# para 3588 contra um teto de 3500. O arquivo reprovava por ter sido marcado.
#
# A marca é procurada só no começo do arquivo, para que a expressão citada dentro
# de um cenário, de uma tabela ou de um parágrafo não isente nada.
INACTIVE_MARKER = "ARQUIVO INATIVO"
INACTIVE_SCAN = 600

# Este script é a ÚNICA declaração de limite do repositório. As skills que dependem
# dele NÃO DEVEM repetir número nenhum: um número copiado para uma skill envelhece na
# primeira decisão que o mude, e foi assim que `feature-planning/SKILL.md` passou a
# cobrar 4500 do `example-mapping.md` depois de o teto do Example Mapping ser removido,
# e a medir o Feature Card por um critério já trocado por outro.
#
# A auditoria de 2026-08-06 (achado A-14) pediu um teste que comparasse o limite
# declarado na skill com o aplicado aqui. A guarda abaixo faz o inverso, e de
# propósito: em vez de detectar a divergência, ela impede que exista uma segunda
# declaração. Ela roda em toda invocação, e não só quando alguém lembra.
#
# A lista cobre só os arquivos que delegam limite a este script. Um teto que este
# script não aplica — o orçamento de tamanho das próprias skills, em
# `workflow-retro/SKILL.md` — não entra aqui, porque ele não tem nada com que divergir.
INSTRUCTIONS_WITHOUT_LIMITS = (
    Path(".claude/skills/feature-planning/SKILL.md"),
    Path(".claude/skills/adr/SKILL.md"),
    Path(".claude/agents/feature-writer.md"),
    Path(".claude/agents/feature-reviewer.md"),
    Path(".claude/agents/artifact-verifier.md"),
)

# Duas formas de declarar limite em prosa: um número seguido de "caracteres", ou a
# palavra "limite" seguida de um número na mesma frase. O `[^.\n]` para no primeiro
# ponto, o que mantém URL e número de versão fora do alcance. "88 colunas" e
# "RFC 2119" não são limite de artefato e não casam.
DECLARED_LIMIT_PATTERNS = (
    re.compile(r"\d[\d.\s]*caracteres"),
    re.compile(r"(?i)limit\w*[^.\n]{0,60}?\d[\d.]{2,}"),
)

# Um ADR é `docs/adr/NNNN-titulo.md`. O índice e o histórico congelado de
# `docs/adr/arquivo/**` vivem na mesma pasta e não são documentos de decisão
# única: o índice cresce por construção a cada ADR novo, e o arquivo morto não
# pode ser encolhido. Decisão `C-7`, em
# `docs/adr/arquivo/proposta-2026-08-03/decisoes-pendentes.md`.
ADR_FILENAME = re.compile(r"^\d{4}-.+\.md$")

# Os quatro primeiros ADRs foram escritos sob outra prática e têm cerca de 35 mil
# caracteres, e eles nunca caberão em limite nenhum. Isentá-los evita um
# verificador permanentemente vermelho, que deixa de ser lido. Decisão `C-7`.
#
# A imutabilidade do corpo foi revogada em 2026-08-07, e a isenção continua: o
# que a revogação autoriza é o **patch**, que conserta citação, caminho e erro
# material. Encolher a prosa desses quatro seria reescrever o argumento, que o
# patch NÃO DEVE tocar. O limite só os alcança por um ADR novo que os substitua.
ADR_LEGACY = {"0001", "0002", "0003", "0004"}

# Em todo artefato Markdown com limite, diagrama, bloco de código e tabela NÃO
# entram na contagem. Os três são densos em caracteres e pobres em prosa: um
# `flowchart` de dez nós custa mais que a seção que ele ilustra. Contá-los punia
# justamente o que as convenções exigem — todo fluxo vai também como Mermaid, e
# toda regra vai em tabela com evidência — e o corte acabava saindo do diagrama ou
# da citação. O limite passa a medir prosa, que é o único lugar onde encher
# linguiça é possível.
#
# Vale só para `.md`. O `behavior.feature` fica de fora porque em Gherkin a tabela
# `Exemplos:` é o cenário, e não ilustração dele; descontá-la esvaziaria o limite.
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")

# `## Patches aplicados` é obrigatória em todo ADR desde 2026-08-07, e ela é a
# última seção do arquivo. Nada dali para baixo entra na contagem: a seção é
# livro-razão de manutenção, e não argumento.
#
# Sem esta isenção, tornar a seção obrigatória estouraria o limite de todo ADR
# que estivesse perto dele — foi o que aconteceu com os ADRs 0011 e 0012, que
# passaram de ~11.990 para ~12.265 caracteres só por ganhá-la. E a saída seria
# encolher a prosa de um ADR aceito, que é exatamente o que um patch NÃO DEVE
# fazer: o limite empurraria para a reescrita do argumento.
PATCH_LEDGER = "## Patches aplicados"

# O cabeçalho de um ADR — título, `Estado`, `Data`, `Etapa`, `Relacionado`,
# `Última atualização` e `Alterado por` — sai da contagem desde 2026-08-10. Ele é
# livro-razão de manutenção, como `## Patches aplicados`, e cresce por alteração
# sofrida, e não por argumento escrito.
#
# A decisão veio de o problema acontecer duas vezes com o mesmo arquivo. Em 2026-08-07,
# tornar `## Patches aplicados` obrigatória empurrou os ADRs 0011 e 0012 para cima do
# teto, e a saída foi descontar a seção. Em 2026-08-10 o ADR-0011 recebeu emenda do
# ADR-0014 e estourou de novo, agora pelas duas linhas de cabeçalho que toda emenda
# obriga — cerca de trezentas letras, quase todas dentro de um link.
#
# A alternativa era encolher a prosa de um ADR aceito, e ela é proibida: não está entre
# as formas de alterar um ADR aceito, e o patch NÃO DEVE tocar argumento. Sem o
# desconto, o teto empurraria para exatamente o que o lifecycle proíbe.
#
# As formas são as de `docs/adr/README.md` e de `.claude/skills/adr/references/
# adr-lifecycle.md`, seção "Depois de aceito", e este comentário NÃO as conta de
# propósito. Até 2026-08-11 ele dizia "as cinco formas", e a lista já era outra: o
# campo `Alterado por` do template passara a aceitar um valor a mais. Um número de
# formas escrito fora do dono da lista envelhece na primeira forma nova, e envelhece
# em silêncio — não há verificador que confira contagem em comentário de código.
#
# Vale só para ADR: num Feature Card o texto antes do primeiro `##` carrega escopo e
# origem, que são prosa de verdade.
SECTION_HEADING = re.compile(r"^##\s+\S")


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1


def is_adr(relative_path: Path) -> bool:
    """Um ADR é `docs/adr/NNNN-titulo.md`. O índice e o arquivo morto não são."""
    return (
        relative_path.parts[:2] == ("docs", "adr")
        and ADR_FILENAME.match(relative_path.name) is not None
    )


def first_section_line(text: str) -> int:
    """A linha, base zero, do primeiro `## `. Devolve zero quando não houver."""
    fence: Optional[str] = None
    for index, line in enumerate(text.split("\n")):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                continue
            if SECTION_HEADING.match(line):
                return index
        elif match and match.group(1)[0] == fence:
            fence = None
    return 0


def prose_lines(text: str, skip_header: bool = False) -> list[tuple[int, str]]:
    """Devolve as linhas de prosa com o número que elas têm no arquivo original."""
    kept: list[tuple[int, str]] = []
    fence: Optional[str] = None
    start = first_section_line(text) if skip_header else 0
    for number, line in enumerate(text.split("\n"), start=1):
        if number <= start:
            continue
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


# O alvo de um link não é prosa, e contá-lo mede o continente em vez do conteúdo.
# A prova apareceu quando a fila saiu de `docs/adr/` para `docs/`: os links para ela
# ganharam `../`, três letras cada, e o ADR-0019 estourou o teto em exatamente quinze
# — cinco links vezes três. Nenhuma palavra foi escrita. Pior, o conserto seria
# impossível: reduzir o corpo de um ADR aceito não é forma permitida pelo lifecycle,
# e o arquivo ficaria acima do teto para sempre por ter mudado de vizinho.
#
# O que fica na contagem é o texto visível do link, que é o que alguém lê.
LINK_TARGET = re.compile(r"\[([^\]]*)\]\([^)\s]*(?:\s+\"[^\"]*\")?\)")


def prose_only(text: str, skip_header: bool = False) -> str:
    """Remove blocos cercados, linhas de tabela e o alvo dos links."""
    body = "\n".join(line for _, line in prose_lines(text, skip_header))
    return LINK_TARGET.sub(r"\1", body)


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


def classify(relative_path: Path) -> str:
    """Devolve a CLASSE do artefato. O primeiro classificador que casar decide."""
    if relative_path.name in INSTRUCTION_NAMES:
        return "instrução"
    if any(root in relative_path.parents for root in INSTRUCTION_ROOTS):
        return "instrução"
    if ARCHIVE_ROOT in relative_path.parents:
        return "arquivo congelado"
    if relative_path == QUEUE_PATH:
        return "fila"
    if relative_path == PLAN_PATH:
        return "plano analítico"
    if relative_path == ADR_ROUTING_FORM:
        return "adr com roteamento de forma"
    if relative_path.name in CLASS_BY_NAME:
        return CLASS_BY_NAME[relative_path.name]
    # O índice é `docs/<pasta>/README.md`. O roteador `docs/README.md` fica fora de
    # propósito: ele NÃO DEVE carregar inventário, e por isso cai no genérico.
    if (
        relative_path.name == "README.md"
        and relative_path != ROUTER_PATH
        and Path("docs") in relative_path.parents
    ):
        return "índice"
    # Depois do índice de propósito: o `README.md` de `docs/propostas/` é inventário, e
    # inventário é isento pela classe `índice`. O que esta linha alcança é a proposta em
    # si e a comparação entre elas.
    if PROPOSALS_ROOT in relative_path.parents:
        return "proposta de modelagem"
    if ARCHITECTURE_ROOT in relative_path.parents:
        return "arquitetura"
    if is_adr(relative_path):
        if relative_path.name[:4] in ADR_LEGACY:
            return "adr legado"
        return "adr"
    if relative_path.suffix in {".yaml", ".yml", ".json"}:
        return "contrato"
    return "genérico"


def default_limit(relative_path: Path) -> Optional[int]:
    """Devolve o teto da classe do arquivo, ou None quando a classe é isenta."""
    artifact_class = classify(relative_path)
    if artifact_class not in CLASS_LIMITS:
        raise ValueError(f"Classe sem teto declarado: {artifact_class}")
    return CLASS_LIMITS[artifact_class]


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
        help="Sobrescreve o limite de um arquivo específico.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    overrides = {path: limit for path, limit in args.limit}
    failed = False

    offences = audit_skill_declarations(root)
    if offences:
        print(
            "ERRO: uma instrução voltou a declarar limite. Este script é a única "
            "declaração — apague o número de lá e mande rodar o verificador.",
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
            # Um `--limit` explícito vence a isenção: quem o passou quer medir.
            inactive = (
                limit is not None
                and relative_path not in overrides
                and INACTIVE_MARKER in raw[:INACTIVE_SCAN]
            )
            if inactive:
                limit = None
            total = len(raw)
            if counts_prose_only(relative_path):
                header = is_adr(relative_path)
                size = len(prose_only(raw, skip_header=header).strip())
                sem = "diagrama, código, tabela e cabeçalho" if header else \
                    "diagrama, código e tabela"
                detail = f" (prosa; {total} com {sem})"
            else:
                size = total
                detail = ""
            artifact_class = classify(relative_path)
            if limit is None:
                motivo = " (inativo)" if inactive else ""
                print(
                    f"ISENTO: {relative_path} — {size} caracteres, "
                    f"classe {artifact_class}{motivo}{detail}"
                )
                continue
            if size > limit and relative_path in TRIAGE_PENDING:
                # A condição que a pessoa pôs em 2026-08-12: quem já excedia quando
                # o alcance foi estendido é avaliado caso a caso, e não reprova até
                # a classe dele ser decidida.
                print(
                    f"TRIAGEM: {relative_path} — {size}/{limit} caracteres, "
                    f"classe {artifact_class} a decidir{detail}"
                )
                continue
            state = "OK" if size <= limit else "EXCEDE"
            print(
                f"{state}: {relative_path} — {size}/{limit} caracteres, "
                f"classe {artifact_class}{detail}"
            )
            failed = failed or size > limit
        except (OSError, ValueError) as error:
            print(f"ERRO: {error}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
