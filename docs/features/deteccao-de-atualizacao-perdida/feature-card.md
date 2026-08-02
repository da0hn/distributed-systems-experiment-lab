# Feature Card — Detecção da atualização perdida

Estado: `especificado, não implementado` · Origem: [`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`

Cobre os experimentos **E1** (`lost-update-none`) e **E3** (`lost-update-strategies`).
Os dois compartilham o mesmo oráculo; o E3 varia a estratégia sobre a mesma carga.

## Problema e resultado esperado

Duas operações leem um contador, calculam e gravam. Uma sobrescreve a outra, sem exceção,
log ou rastro. O engenheiro continua sem saber **quanto** se perde, e sob qual proteção.

Resultado esperado: uma contagem exata de incrementos perdidos, não um predicado que pode
ou não ter sido violado.

## Atores e gatilho

Workers do Control Plane executam `increment(resourceId)` concorrentemente. O oráculo lê o
banco antes do primeiro worker e depois do último. Gatilho: uma execução de experimento
sobre `increment`.

## Escopo

O domínio mínimo de duas entidades. A operação `increment`. O oráculo exato. A escolha do
denominador. A separação entre `commits` e `sucessos`. A comparação entre quatro
estratégias sobre a mesma carga.

## Fora de escopo

**A coluna `version` não existe no esquema.** Ela é a solução do fenômeno, e a regra
pedagógica exige o problema antes; quem a acrescenta é a decisão de estratégias de
concorrência. O esboço do ADR-0001 lê uma coluna que o esquema não tem, e ele não é
normativo.

Nível de isolamento, classificação do veredito zero e formato curva estão em outros cards
ou na fila.

## Regras de negócio

| # | Regra | Evidência |
|---|---|---|
| R1 | O domínio tem duas entidades e nenhum nome de negócio: `Resource(id, value, capacity)` e `Allocation(id, resource_id, amount)`. Nenhuma outra coluna entra no MVP. | ADR-0002:87-92 |
| R2 | O esquema **NÃO DEVE** carregar uma coluna `version`. | ADR-0002:94-95 |
| R3 | O identificador **DEVE** ser gerado pela aplicação a partir da semente. O esquema **NÃO DEVE** usar `SERIAL`, `IDENTITY`, `nextval` nem valor padrão do banco. | ADR-0002:124-126 |
| R4 | O identificador **DEVE** ser função da semente e **NÃO DEVE** ser função do instante da execução. Duas execuções da mesma semente produzem os mesmos identificadores. | ADR-0002:128-130 |
| R5 | O oráculo produz uma contagem: `perdidas = commits − (value_final − value_inicial)`. | ADR-0002:135-139 |
| R6 | `commits` é o número de passagens pela fronteira `AFTER_COMMIT`, contadas **por tentativa**. | ADR-0002:141 |
| R7 | O denominador **DEVE** ser `commits`. Ele **NÃO DEVE** ser o número de operações submetidas nem o de operações que reportaram sucesso. | ADR-0002:145-148 |
| R8 | `sucessos` conta as execuções de operação que reportaram sucesso. A diferença `commits − sucessos` mede o dual write. | ADR-0002:171-173 |
| R9 | Os dois oráculos consultam o PostgreSQL. Nenhum deles **DEVE** derivar o estado final do log de observações. | ADR-0002:214-217 |
| R10 | O E1 **precisa falhar**. Se `value` final for igual a 100, a carga é insuficiente e nenhum resultado posterior significa alguma coisa. | plano:397-398 |
| R11 | Cada worker tem sua própria conexão. O pool **DEVE** ser maior que o número de workers, e isso **DEVE** ser verificado, não presumido. | plano:579-582 |

O diagrama das duas contagens está no [Example Mapping](example-mapping.md).

## Integrações e contratos afetados

`increment` emite `SELECT` e `UPDATE` contra `resource`. O oráculo emite um `SELECT` do
Lab Plane depois da quiescência. **Não existe DDL nem contrato de esquema** — ver
`Q-INT-5` em [`integrations.md`](../../architecture/integrations.md).

## Riscos e decisões pendentes

| Questão | O que está em jogo |
|---|---|
| calibração | qual estratégia não perde incremento nenhum ainda não foi decidido |
| `Q-0002-4` | ninguém estabelece o estado inicial; R4 faz o identificador da semente colidir com as linhas da execução anterior |
| `Q-0001-2` | um colaborador injetado com estado compartilhado fabrica a perda dentro do instrumento, e o resultado é indistinguível de uma perda real |
| `Q-0002-3` | o oráculo lê o estado final quiescente, e não serve a violação transitória |

## Critérios de pronto

R1 a R11 verificadas por teste. O E1 produz `perdidas > 0` de forma repetida sob a carga
declarada. R7 é testada com o caso que a distingue: uma tentativa que commitou e reportou
falha entra na contagem; uma que esgotou as tentativas, não.

## Links

[Example Mapping](example-mapping.md) · [BDD](behavior.feature) ·
[`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md) ·
[`execucao-de-experimento`](../execucao-de-experimento/feature-card.md)
