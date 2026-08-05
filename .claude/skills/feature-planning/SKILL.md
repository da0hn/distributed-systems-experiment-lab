---
name: feature-planning
description: "Plan new features, behavior changes, and implementation updates for this laboratory. Use automatically whenever the user asks to plan, refine, scope, design, estimate, or prepare implementation work, including a new feature, experiment, API, event, integration, behavior change, planejamento, plano de implementação, nova feature, refinamento, or design técnico."
---

# Planeje a funcionalidade

Use este fluxo antes de propor tarefas de implementação. Aplique-o também quando
o pedido atualizar uma capacidade existente.

Não crie arquivos de modelo em docs. Use os modelos versionados em references/.

## Leia antes de escrever

Leia, nesta ordem:

1. AGENTS.md na raiz.
2. docs/specification-process.md.
3. docs/features/README.md.
4. docs/contracts/README.md e docs/architecture/integrations.md.
5. O plano, os cards, os contratos e o código relacionados ao pedido.

Use código, configuração e testes como evidência. Cite o arquivo e a linha para
cada fato existente. Escreva Pergunta em aberto quando a evidência não existir.
Nunca transforme uma hipótese em fato.

Registre cada objeção, alternativa descartada ou pendência no Example Mapping no
mesmo turno em que surgir. Quando for ADR, use a skill adr (.claude/skills/adr/).

## Use o template obrigatório

Leia o template antes de criar ou atualizar o artefato. Mantenha todas as seções
obrigatórias. Escreva Não se aplica — <motivo> quando uma seção não se aplicar.
Não remova uma seção para caber no limite; divida a capacidade ou o documento.

| Artefato              | Template                                                    |
|-----------------------|-------------------------------------------------------------|
| Feature Card          | references/feature-card.md                                  |
| Example Mapping       | references/example-mapping.md                               |
| BDD                   | references/behavior.feature                                 |
| Matriz de integrações | references/integrations.md                                  |
| OpenAPI               | references/openapi.yaml                                     |
| AsyncAPI              | references/asyncapi.yaml                                    |
| JSON Schema           | references/json-schema.json                                 |
| Desenho completo      | references/implementation-plan.md                           |
| ADR                   | delegado à skill adr — .claude/skills/adr/references/adr.md |

Todos os templates necessários ficam na pasta desta skill, exceto o ADR, que vive na
skill adr.

## Classifique a mudança

1. Trate comportamento observável como Feature Card.
2. Trate alternativa durável, restrição futura e trade-off como ADR.
3. Trate interface entre processos como contrato.
4. Trate mudança local e reversível como tarefa, sem ADR.

Não escreva um ADR por reflexo. Não altere ADR aceito. Quando uma decisão bloquear
o escopo, registre a pergunta e use AskUserQuestion antes de escolher por conta
própria.

Quando a mudança exigir ADR, acione a skill adr antes de criar, aceitar, substituir
ou subsumir uma decisão.

## Gere os artefatos

### Feature Card

Crie ou atualize docs/features/<slug>/feature-card.md para cada capacidade. Um
card cobre uma capacidade, não uma classe, rota ou tarefa.

Limite: 5.500 caracteres, sem contar a quebra final. Divida a capacidade se o
limite não bastar.

### Example Mapping

Crie ou atualize docs/features/<slug>/example-mapping.md. Inclua casos de fronteira,
falha, repetição, concorrência, idempotência e consistência quando forem relevantes.

Limite: 4.500 caracteres, sem contar a quebra final. Não converta uma regra em
debate para Gherkin.

### BDD

Crie ou atualize docs/features/<slug>/behavior.feature depois de estabilizar as
regras. Use Gherkin em português e inclua # language: pt. Descreva somente o
comportamento externo. Um cenário não cita classe, tabela ou coluna.

Para cada regra, escreva no máximo o fluxo principal, uma falha relevante e um
caso de borda que mude o resultado. Marque cenários sem teste como @teste-ausente.

Limite: 3.500 caracteres, sem contar a quebra final.

### APIs, eventos e integrações

Atualize docs/architecture/integrations.md quando a mudança confirmar uma
fronteira. Mantenha a matriz com origem, destino, tipo, operação ou tópico,
finalidade, contrato, autenticação, confiabilidade e evidência. Diferencie fato,
hipótese e decisão pendente.

Limite: 12.000 caracteres por arquivo. Divida a matriz por fronteira antes de
ultrapassar o limite.

Crie ou atualize um contrato somente quando a interface existir no código ou for
entregue na mesma mudança:

- Use OpenAPI para API HTTP.
- Use AsyncAPI para mensageria e eventos.
- Use JSON Schema para payload que atravesse fronteira sem contrato maior.

Para eventos, declare tipo, produtor, consumidores conhecidos, canal, esquema,
versão, correlação, idempotência, ordenação, retry, DLQ e entrega somente quando
houver evidência ou decisão. Diferencie comando de evento de domínio.

Não crie diretório vazio, contrato de intenção ou campo preenchido por analogia.
Não repita em Markdown o que o contrato formal já define.

### Artefatos excepcionais

Crie um documento de desenho completo somente para alto risco, vários processos ou
mudança de contrato com consumidor conhecido. Use
docs/features/<slug>/implementation-plan.md e limite-o a 7.000 caracteres.

Crie ADR somente quando os critérios do repositório forem atendidos. Limite um ADR
novo a 9.000 caracteres. Use a skill adr, que contém references/adr.md e
references/adr-lifecycle.md.

Qualquer outro Markdown persistente criado por este fluxo tem limite de 4.000
caracteres. Um índice atualizado não é um artefato novo; acrescente apenas o link e
uma frase de contexto.

## Escreva com os princípios de ASD-STE100

Escreva em português do Brasil. Aplique os princípios de linguagem controlada do
ASD-STE100; não alegue conformidade literal, pois a especificação controla inglês.

- Use uma frase para uma ideia e voz ativa.
- Use verbo preciso. Diga quem faz a ação e qual resultado ocorre.
- Coloque a condição antes da ação que ela controla.
- Use no máximo 20 palavras por frase e três frases por parágrafo.
- Use um termo técnico por conceito. Defina sigla na primeira ocorrência.
- Evite sinônimos para o mesmo conceito, abreviação sem definição, jargão, metáfora,
  advérbio vago e qualificadores sem medida.
- Prefira listas para sequências e tabelas para regras combinatórias.
- Use DEVE, NÃO DEVE, DEVERIA e PODE apenas para requisito normativo.
- Declare número, limite, unidade, ator e condição quando eles mudarem o resultado.

## Valide antes de encerrar

1. Confirme que o card não duplica o contrato ou o ADR.
2. Confirme que toda pergunta em aberto aparece no Example Mapping.
3. Confirme que cada cenário BDD vem de exemplo estabilizado.
4. Confirme links relativos, evidências e atualização dos índices necessários.
5. Execute o verificador para todo artefato criado ou editado:

~~~powershell
python "${CLAUDE_SKILL_DIR}/scripts/check_artifact_limits.py" --root . --file <arquivo> [--file <arquivo> ...]
~~~

Resolva toda violação antes de apresentar o plano. Se um limite impedir clareza,
divida o artefato. Não aumente o limite.

## Entregue o planejamento

Apresente, nesta ordem:

1. Capacidade e resultado esperado.
2. Evidências encontradas e perguntas em aberto.
3. Artefatos criados ou atualizados.
4. Contratos e fronteiras afetados.
5. Tarefas de implementação em ordem de dependência.
6. Riscos, testes e validações.

Não inicie a implementação sem aprovação explícita, salvo se o usuário pedir
planejamento e implementação no mesmo pedido.
