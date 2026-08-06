---
name: adr
description: Template e ciclo de vida de Architecture Decision Records (ADR) deste laboratório. Use sempre que uma decisão precisar virar ADR — ao planejar uma feature, ao refinar o modelo de domínio, ou quando o usuário pedir para registrar, aceitar, substituir ou subsumir uma decisão arquitetural.
---

# ADR

Skill única para template e ciclo de vida de ADR neste repositório. A skill
feature-planning a aciona ao classificar uma mudança como decisão arquitetural; a skill
domain-modeling a aciona ao oferecer um ADR durante o refinamento do glossário. Nenhuma
das duas mantém template ou regra de ciclo de vida próprios — as duas delegam para esta
skill.

## Leia antes de escrever

1. `docs/adr/README.md` — convenções de escrita, estados e numeração.
1. `docs/adr/fila-de-decisoes.md` — a fila única, e o que cada linha destrava.
2. `references/adr.md` — o template obrigatório.
3. `references/adr-lifecycle.md` — o que fazer antes de criar, enquanto proposto, ao
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
2026-08-04, registrada em `CLAUDE.md`. A sessão principal conduz a decisão e obtém a
escolha explícita; o sub-agente recebe a escolha já feita e escreve o ADR.

Os dois agentes são registrados, e NÃO DEVE-se usar um `general-purpose` genérico:

- **`adr-writer`** (`.claude/agents/adr-writer.md`, modelo Haiku) redige e corrige.
- **`adr-reviewer`** (`.claude/agents/adr-reviewer.md`, modelo Opus) revisa e devolve uma
  lista numerada de defeitos. Ele não tem `Write` nem `Edit`, de propósito.

Depois que o escritor devolver o arquivo, rode o revisor de forma síncrona. Enquanto a
resposta não for `SEM DEFEITOS`, mande a lista de volta ao escritor com `SendMessage`,
que preserva o contexto dele. Pare na terceira rodada e leve o que sobrou ao usuário. O
detalhe do loop está em `CLAUDE.md`, seção "Os dois agentes registrados, e o loop entre
eles".

O sub-agente NÃO DEVE escolher entre alternativas nem fechar lacuna sozinho. Uma lacuna
encontrada durante a redação vira linha em `docs/architecture/decisoes-pendentes.md`.

## Use o template obrigatório

Leia `references/adr.md` antes de criar ou atualizar um ADR. Mantenha todas as seções
obrigatórias. Escreva "Não se aplica — <motivo>" quando uma seção não se aplicar. Limite:
9.000 caracteres por ADR novo.

## Siga o ciclo de vida

Leia `references/adr-lifecycle.md` antes de criar, aceitar, substituir ou subsumir uma
decisão.

- Um ADR por vez. Nunca crie rascunhos antecipados ou em lote.
- Registre toda objeção, alternativa descartada ou pendência em "## Questões em aberto" no
  mesmo turno em que surgir.
- Nenhum ADR é aceito por omissão. Exija aprovação explícita da pessoa responsável.
- Nunca edite ou apague um ADR aceito. Para mudar a decisão, crie um ADR novo.

## Convenções de escrita

RFC 2119 traduzida em caixa alta, ~88 colunas, um conceito com um nome só, diagrama
Mermaid junto de todo fluxo descrito, sem emojis e sem linguagem de marketing. A lista
completa, incluindo as palavras proibidas, está em `docs/adr/README.md`, seção
"## Convenções".
