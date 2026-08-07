# AGENTS.md — trabalhando dentro de `docs/`

Instruções operacionais para editar esta pasta. O contexto do projeto está no
[`AGENTS.md` da raiz](../AGENTS.md); o mapa da pasta está em [`README.md`](README.md).

## A regra que vale antes de qualquer outra

> **Nada que importa pode existir apenas na conversa.**

O contexto é limpo entre sessões. Toda objeção, alternativa descartada ou pendência é
escrita no arquivo **no mesmo turno em que é
levantada**, antes de responder ou perguntar
qualquer coisa. Uma objeção que fica só no chat desaparece no próximo compact, em silêncio.

O destino depende do artefato: `## Questões em aberto` do ADR, ou a seção de perguntas
em aberto do `example-mapping.md`.

## `features/` é fonte de verdade, junto dos ADRs

Decidido em 2026-08-06. Um card não é resumo nem índice: **ele carrega tudo o que uma
consulta precisa**, e quem o lê não deveria ter de abrir o ADR para saber o que o sistema
faz. Por isso uma decisão arquitetural que mude comportamento entrega **ADR e card no
mesmo commit** — um ADR que nasce sozinho deixa o repositório afirmando duas coisas
contraditórias, e a regra `B-4` já proíbe card que contradiga ADR aceito.

A divisão de trabalho não muda: o ADR diz **por que** e o card diz **o quê**. O que muda é
que a segunda metade deixou de ser opcional.

## O que nunca é editado

| Alvo                           | Por quê                                                                                |
|--------------------------------|----------------------------------------------------------------------------------------|
| `adr/arquivo/**`               | registra o que se pensava naquela data; editar apaga a evidência                       |
| o **corpo** de um ADR `Aceito` | para mudar a decisão, escreva um ADR novo e marque o antigo `Substituído por ADR-NNNN` |

Corpo é tudo a partir da primeira seção `##`. Um ADR `Proposto` **pode** ser editado.
Hoje **nenhum** ADR da série corrente está nesse estado: os oito estão `Aceito`, e o
corpo de nenhum deles pode ser editado.

**O cabeçalho de um ADR aceito é editável num caso só, desde 2026-08-04.** Quando um ADR
posterior o substitui, o emenda ou subsome uma regra dele, o ADR alterado recebe `Última
atualização` e `Alterado por`, no mesmo commit em que o ADR novo nasce. A regra completa
está em [`adr/README.md`](adr/README.md), seção "O rastro de alterações, emendado em
2026-08-04"; a **emenda** entrou em 2026-08-05, pela decisão `A1`, e está descrita em
[`adr/README.md`](adr/README.md#a-emenda-terceira-forma-ao-lado-da-substituição-e-da-subsunção).

**O adendo é a única alteração que acrescenta seção, e ele nasceu em 2026-08-05.** Ele
serve a um caso só: um ADR aceito que cita um documento que vai deixar de existir. O
adendo entra como **última seção** do arquivo, datado, e incorpora a afirmação que a
citação sustentava — nunca o parágrafo de origem. O corpo permanece byte a byte, e por
isso ele não é edição: nada do que se pensava naquela data é apagado. A regra está em
[`adr/README.md`](adr/README.md#o-adendo-quarta-forma-e-a-única-que-acrescenta-seção).
Nenhuma outra alteração de ADR aceito é permitida.

## Qual artefato criar

```mermaid
flowchart TD
  P["o que preciso registrar?"] --> Q1{"descreve o que o<br/>sistema faz, e é<br/>verificável?"}
  Q1 -->|" sim "| FC["Feature Card<br/>+ Example Mapping"]
  Q1 -->|" não "| Q2{"tem alternativa<br/>plausível e impacto<br/>arquitetural duradouro?"}
  Q2 -->|" sim "| ADR["ADR"]
  Q2 -->|" não "| NADA["não vira documento<br/>registre no artefato<br/>que já existe"]
  FC --> Q3{"a regra ainda<br/>está em debate?"}
  Q3 -->|" sim "| EX["fica como exemplo<br/>e pergunta em aberto"]
  Q3 -->|" não "| BDD["vira cenário Gherkin"]
```

O teste que separa os dois primeiros:

| Pergunta                                                | Sim → ADR | Sim → Feature Card |
|---------------------------------------------------------|-----------|--------------------|
| Existe alternativa que alguém defenderia com argumento? | sim       | —                  |
| A escolha restringe o que se pode construir depois?     | sim       | —                  |
| A frase descreve o que o sistema faz, e é verificável?  | —         | sim                |
| Um teste poderia falhar por causa dela?                 | —         | sim                |

Uma regra que caiba nas duas colunas indica um ADR carregando comportamento: escreva o
ADR com o porquê, o card com o quê, e faça o card citar o ADR por arquivo e linha.

## Feature Card

Caminho: `features/<slug>/feature-card.md`. Slug em kebab-case, nomeando a capacidade.

Seções obrigatórias, nesta ordem: problema e resultado esperado; atores e gatilho;
escopo; fora de escopo; regras de negócio; integrações e contratos afetados; riscos e
decisões pendentes; critérios de pronto; links.

- **Máximo 5.500 caracteres de prosa.** Um card acima disso cobre mais de uma capacidade
  — divida. O corte sai da prosa, **nunca da evidência**.

  **Diagrama, bloco de código e tabela não entram na contagem.** A regra vale para todo
  artefato `.md` com limite, e entrou em 2026-08-06. Os três são densos em caracteres e
  pobres em prosa: um `flowchart` de dez nós custa mais que a seção que ele ilustra.
  Contá-los punia exatamente o que estas instruções exigem — todo fluxo vai **também**
  como Mermaid, e toda regra vai em tabela com evidência e com quem a aprovou —, e o
  corte acabava saindo do diagrama ou da citação.

  **Quem conta é o script, e não um comando de shell montado à mão:**

  ```bash
  python .claude/skills/feature-planning/scripts/check_artifact_limits.py \
    --root . --file docs/features/<slug>/feature-card.md
  ```

  Ele imprime a contagem de prosa e, entre parênteses, o tamanho bruto. A medição
  anterior era em palavras, com um `sed` que trocava `|` por espaço sem remover o
  conteúdo da célula — ela descontava a moldura da tabela e cobrava o texto dentro dela.
- **Um card cobre uma capacidade**, nunca um endpoint, uma classe ou uma tarefa técnica.
- **Um card por oráculo, não por experimento.** É o oráculo que define o comportamento
  observável. E1 e E3 partilham o oráculo exato e vivem num card só.
- **Toda regra leva evidência** com arquivo e linha, numa coluna própria da tabela.
- **Toda regra leva quem a aprovou**, numa segunda coluna própria, ao lado da evidência.
  É a decisão `B-3`, de 2026-08-05: aprova-se a **regra**, e não o card. Uma regra nasce
  `pendente` e só uma pessoa a tira desse estado. O card **NÃO DEVE** ganhar estado nem
  ato de aprovação — ele é o continente, e muda a cada exemplo novo.
- **Uma regra `pendente` NÃO DEVE virar cenário Gherkin.** Escrever Gherkin sobre regra
  não aprovada congela a versão errada dela, pelo mesmo motivo que vale para regra em
  debate.
- **Um card NÃO PODE contradizer um ADR aceito.** Pela decisão `B-4`, de 2026-08-05, a
  contradição **é** decisão arquitetural nova: ela entra na
  [fila de decisões](adr/fila-de-decisoes.md) no mesmo turno em que é vista, e o ADR que
  sair dela emenda, substitui ou ratifica o antigo. O card é alinhado ao que o ADR
  disser. O processo está em
  [`specification-process.md`](specification-process.md#quem-aprova-o-que-decidido-em-2026-08-05).
- Um diagrama pesado demais para o card vai para o `example-mapping.md`, e o card faz
  link. **O motivo mudou:** desde que diagrama não conta caracteres, mover um deixou de
  liberar orçamento — o que se ganha é foco, porque o card carrega o que uma consulta
  precisa, e o Example Mapping carrega o que uma discussão precisa.
- Ao criar um card, acrescente a linha correspondente em [`features/README.md`](features/README.md)
  e em [`README.md`](README.md), seção `## Estado da especificação`.

## Example Mapping

Caminho: `features/<slug>/example-mapping.md`. **Não tem limite de tamanho**, decidido em
2026-08-06: ele cresce por exemplo acrescentado, e acrescentar exemplo é o trabalho dele
— um teto transformaria "achei mais um contraexemplo" em "preciso apagar um dos antigos".
É o único artefato de `features/` sem freio, e o custo está aceito.

Quatro blocos obrigatórios — história, regras, exemplos concretos, perguntas em aberto —
e um quinto para o que foi **adiado de propósito**, com o gatilho que o retoma.

- Os exemplos existem para revelar o que a regra não disse: fronteira, erro, autorização,
  repetição, concorrência, idempotência e consistência. Um exemplo que apenas reafirma a
  regra em outras palavras não acrescenta nada.
- Use **contraexemplo** para registrar o que a regra deixa passar. É onde as lacunas do
  repositório ficam visíveis.
- Feche com uma seção **"O que não virou cenário, e por quê"**. Ela impede que uma regra
  omitida do Gherkin pareça esquecimento.

## BDD

Caminho: `features/<slug>/behavior.feature`.

- Cabeçalho `# language: pt`, e um comentário dizendo de onde as regras vêm.
- **Comportamento externo e observável.** Nome de classe, de tabela e de coluna não
  aparecem num cenário; o veredito, a contagem e a recusa aparecem.
- Poucos cenários. Por regra: o fluxo principal, uma falha relevante, e um caso de borda
  quando ele mudar o resultado.
- **Só exemplo estabilizado vira cenário.** Regra em debate fica no Example Mapping.
  Escrever Gherkin sobre regra em debate congela a versão errada dela.
- Todo cenário leva a tag `@teste-ausente` enquanto não houver teste que o verifique.
  Quando o teste existir, troque a tag pelo identificador dele.
- **Nenhuma dependência de BDD entra no projeto por causa disso.**

## Contratos

Caminho: `contracts/openapi/` e `contracts/asyncapi/`.

- **Um contrato é criado quando a interface
  existir**, nunca antes. Hoje nenhuma existe, e
  por isso os dois diretórios **não** foram criados.
- **Não crie diretório
  vazio.** Uma pasta `openapi/` sem conteúdo afirma que existem APIs
  a documentar. O repositório já pagou por esse erro com o `services/` de pastas com
  nome de dono, apagado em `83fcfc9`.
- O que estiver formalizado num contrato **NÃO DEVE** ser repetido em Markdown.
- Ao criar o primeiro, atualize [`contracts/README.md`](contracts/README.md), que hoje
  lista os gatilhos de cada um.

## Integrações

Caminho: `architecture/integrations.md`.

- A matriz separa **fato** de
  **hipótese**. Fato é verificável hoje, na árvore versionada
  ou num repositório externo nomeado. Hipótese é descrita em documento de planejamento e
  nada a implementa.
- **Nunca promova hipótese a fato sem evidência
  nova.** Hoje há uma integração real, e ela
  está quebrada: o ArgoCD do homelab aponta para um `deploy/` que não existe.
- Perguntas de integração recebem identificador `Q-INT-N`.

## ADR

Caminho: `adr/NNNN-titulo-em-kebab-case.md`. Para planejar um ADR no Claude Code, use
a skill `adr`. Ela contém o template e o ciclo de vida, e é acionada tanto por
`feature-planning` quanto por `domain-modeling`. O [`adr/README.md`](adr/README.md)
mantém as convenções, o índice e o histórico da série.

## Glossário de domínio

Caminho: `CONTEXT.md`, criado de forma preguiçosa quando o primeiro termo se
cristalizar. Para manter o glossário no Claude Code, use a skill `domain-modeling`. Ela
desafia termo ambíguo, cruza a linguagem com o código e atualiza o arquivo no mesmo
turno em que um termo é resolvido — nunca em lote. O formato está em
`.claude/skills/domain-modeling/references/context-format.md`.

## Convenções de escrita

As convenções gerais estão no [`AGENTS.md` da raiz](../AGENTS.md), seção `## Convenções
de escrita, válidas em todo documento`, e a lista de palavras proibidas em
[`adr/README.md`](adr/README.md). Elas valem aqui sem alteração.

Dois pontos que só aparecem nesta pasta:

- **Todo fluxo descrito em prosa vai também como diagrama
  Mermaid**, junto do parágrafo que
  o descreve. `sequenceDiagram` para ordem no tempo, `flowchart` para topologia e
  hierarquia. Excalidraw só para o que o Mermaid não expressa, exportado como
  `.excalidraw.svg` em [`diagrams/`](diagrams/).
- **Um diagrama que não acrescenta nada à prosa fica de
  fora.** Repetir a mesma informação
  em duas formas não é redundância útil quando as duas dizem exatamente o mesmo.

## Antes de encerrar uma edição

- Toda afirmação relevante tem evidência com caminho e linha. O que não pôde ser
  confirmado está como `Pergunta em aberto`, não como fato.
- Os links relativos resolvem. Um link entre níveis de diretório erra com facilidade —
  `docs/architecture/integrations.md` apontando para `../README.md` resolve para
  `docs/README.md`, e não para a raiz.
- `check_artifact_limits.py` passa nos artefatos alterados. Ele mede prosa: diagrama,
  bloco de código e tabela não entram na contagem de nenhum `.md`.
- A capacidade nova aparece nos dois índices: [`features/README.md`](features/README.md) e
  [`README.md`](README.md).
- `git add` apenas dos arquivos relacionados, e um único commit em Conventional Commits (skill `commit`).
