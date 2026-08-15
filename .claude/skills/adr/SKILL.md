---
name: adr
description: "Template e ciclo de vida de Architecture Decision Records deste laboratório. NÃO use automaticamente ao decidir algo: no modo vigente, uma decisão arquitetural é apresentada na conversa e vai para o código. Só invoque quando a pessoa pedir explicitamente para registrar um ADR."
---

> **AVISO DE PROCESSO REVOGADO.** O modo de trabalho vigente deste repositório é
> **implementação primeiro**, e está em [`AGENTS.md`](../../../AGENTS.md) — ele prevalece
> sobre tudo o que esta página descreve. O ciclo abaixo **NÃO DEVE ser iniciado por
> iniciativa própria**: ele só roda quando a pessoa o pedir pelo nome, nesta sessão, em
> palavras. Pendência de definição vai para o `docs/backlog.md`, em uma linha, e não
> vira documento.

> **`docs/` FOI REFATORADA, e a estrutura agora é fechada.** Cinco pastas —
> `architecture/`, `adr/`, `features/`, `contracts/` e `diagrams/` — mais `README.md`,
> `roadmap.md`, `data-dictionary.md` e `backlog.md`. Nenhum caminho novo é inventado,
> e vários arquivos que esta página cita já não existem: `specification-process.md`,
> `fila-de-decisoes.md`, `plano-do-laboratorio.md`, `CONTEXT.md`, `questions/` e
> `audits/`. O índice da pasta é `docs/README.md`.

> **`docs/adr/` ESTÁ CONGELADO.** Nenhum ADR novo nasce ali, e nenhum ADR existente é
> editado, emendado, patcheado, adendado, dividido ou substituído. O template e o ciclo
> de vida abaixo descrevem um processo que não roda mais.

# ADR

Skill única para template e ciclo de vida de ADR neste repositório. A skill
feature-planning a aciona ao classificar uma mudança como decisão arquitetural; a skill
domain-modeling a aciona ao oferecer um ADR durante o refinamento do glossário. Nenhuma
das duas mantém template ou regra de ciclo de vida próprios — as duas delegam para esta
skill.

## Leia antes de escrever

1. `docs/adr/README.md` — convenções de escrita, estados e numeração.
2. `../../../docs/fila-de-decisoes.md` — a fila única, e o que cada linha destrava.
3. `references/adr.md` — o template obrigatório.
4. `references/adr-lifecycle.md` — o que fazer antes de criar, enquanto proposto, ao
   aceitar e depois de aceito.

## Quando uma decisão merece ADR

**Escrever ADR não é obrigatório, e o ADR nasce `Aceito`.** Regra adotada em 2026-08-04.
O que se enfileira é decisão, e não ADR. Avalie a escolha já tomada pela pessoa contra os
quatro critérios abaixo: se atender, escreva o ADR com estado `Aceito`; se não atender, o
destino é um artefato de `docs/features/`, definido pela skill `feature-planning`.

Os quatro critérios de `docs/adr/README.md` valem juntos:

- possui alternativas plausíveis;
- tem impacto arquitetural duradouro;
- cria restrições futuras;
- representa um trade-off importante.

Decisão trivial não vira ADR. Escolher o nome de uma variável, a versão de patch de uma
biblioteca ou o formato de um log não atende a nenhum dos quatro critérios.

Se a decisão descreve o que o sistema faz — e é verificável por teste — não é ADR: é
comportamento, e vai para o Feature Card. O teste completo dessa fronteira está em
`docs/specification-process.md`, seção "ADR — só decisão arquitetural durável".

## A escrita roda em sub-agente, e passa por revisão

**Delegue a redação do arquivo a um sub-agente, em background.** Regra adotada em
2026-08-04, e o dono dela é
[`specification-process.md`](../../../docs/specification-process.md#redação-e-revisão-independente-de-especificação). A
sessão principal conduz a decisão e obtém a escolha explícita; o sub-agente recebe a
escolha já feita e escreve o ADR.

**O par não é específico de ADR desde 2026-08-10.** Ele escreve especificação, e o ADR é
um dos artefatos que ela PODE gerar — o par anterior, `adr-writer` e `adr-reviewer`, foi
substituído. Os dois agentes são registrados, e NÃO DEVE-se usar um `general-purpose`
genérico:

- **`feature-writer`** (`.claude/agents/feature-writer.md`, modelo Sonnet) redige e
  corrige. Ele escreve o ADR **só quando o prompt o nomear**.
- **`feature-reviewer`** (`.claude/agents/feature-reviewer.md`, modelo Opus) revisa e
  devolve uma lista numerada de defeitos. Ele não tem `Write` nem `Edit`, de propósito.

Depois que o escritor devolver o arquivo, rode o revisor de forma síncrona. **A réplica é
condicional:** um `SEM DEFEITOS` encerra o ciclo sem réplica nenhuma. Enquanto a resposta
for uma lista, mande-a de volta ao escritor com `SendMessage`, que preserva o contexto
dele. Pare na terceira réplica e leve o que sobrou ao usuário. O contrato do loop — o que
o escritor recebe, o que ele NÃO DEVE fazer, e quem decide quando não converge — está em
[`specification-process.md`](../../../docs/specification-process.md#redação-e-revisão-independente-de-especificação).

O sub-agente NÃO DEVE escolher entre alternativas nem fechar lacuna sozinho. Uma lacuna
encontrada durante a redação vira linha em
`../../../docs/fila-de-decisoes.md`.

## Use o template obrigatório

Leia `references/adr.md` antes de criar ou atualizar um ADR. Mantenha todas as seções
obrigatórias. Escreva "Não se aplica — <motivo>" quando uma seção não se aplicar.

**Esta skill não declara o tamanho de um ADR.** Quem declara é
[`check_artifact_limits.py`](../feature-planning/scripts/check_artifact_limits.py),
que mede prosa e desconta diagrama, bloco de código e tabela. Rode-o em vez de
estimar; ele recusa esta skill se um número reaparecer aqui.

## Siga o ciclo de vida

Leia `references/adr-lifecycle.md` antes de criar, aceitar, substituir, subsumir ou
patchar uma decisão.

- Um ADR por vez. Nunca crie rascunhos antecipados ou em lote.
- Registre toda objeção, alternativa descartada ou pendência em "## Questões em aberto" no
  mesmo turno em que surgir.
- Nenhum ADR é aceito por omissão. Exija aprovação explícita da pessoa responsável.
- **A imutabilidade do corpo de um ADR aceito foi revogada em 2026-08-07.** Seis formas
  o alteram — substituição, subsunção, emenda, adendo, divisão e **patch** —, cada uma com
  gatilho e limite próprios, e nenhuma outra é permitida. As cinco primeiras exigem um ADR
  novo; o patch não, mas ele NÃO DEVE alterar a decisão nem o argumento que a sustentava, e
  NÃO DEVE existir sem a linha dele em `## Patches aplicados`, no mesmo commit. A regra
  completa está em `docs/adr/README.md`, seção "A revogação da imutabilidade, decidida em
  2026-08-07", e em "A divisão de um ADR aceito, decidida em 2026-08-11". Aplique-a a
  partir de lá.
- Um ADR aceito continua não sendo **apagado**, e continua não mudando de decisão sem
  ADR novo.

## Convenções de escrita

RFC 2119 traduzida em caixa alta, ~88 colunas, um conceito com um nome só, diagrama
Mermaid junto de todo fluxo descrito, sem emojis e sem linguagem de marketing. A lista
completa, incluindo as palavras proibidas, está em `docs/adr/README.md`, seção
"## Convenções".
