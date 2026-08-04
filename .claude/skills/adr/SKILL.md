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

1. `docs/adr/README.md` — convenções de escrita, estados, numeração e a fila de decisões.
2. `references/adr.md` — o template obrigatório.
3. `references/adr-lifecycle.md` — o que fazer antes de criar, enquanto proposto, ao
   aceitar e depois de aceito.

## Quando uma decisão merece ADR

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
