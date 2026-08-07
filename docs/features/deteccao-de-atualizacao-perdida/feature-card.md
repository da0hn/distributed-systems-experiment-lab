# Feature Card — Detecção da atualização perdida

Estado: `especificado, não implementado` · Origem: [`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`

Cobre os experimentos **E1** (`lost-update-none`) e **E3** (`lost-update-strategies`).
Os dois compartilham o mesmo oráculo; o E3 varia a estratégia sobre a mesma carga.

## Problema e resultado esperado

Duas operações leem um contador, calculam e gravam. Uma sobrescreve a outra, sem exceção,
log ou rastro. O engenheiro continua sem saber **quanto** se perde, e sob qual proteção.

Resultado esperado: uma contagem exata de incrementos perdidos, não um predicado que
pode ou não ter sido violado.

## Atores e gatilho

Workers do system under test executam `increment(resourceId)` concorrentemente. O oráculo
lê o WAL do sistema medido por replicação lógica e **NÃO DEVE** emitir `SELECT` no schema
dele, desde o
[`ADR-0010`](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md).
`value_final` é o último valor de `resource.value` visto no stream. `value_inicial` vem da
**mesma** fonte: antes de cada execução o estado inicial é inserido, não pressuposto, e
esse `INSERT` é capturado como qualquer outro evento. Gatilho: uma execução de experimento
sobre `increment`.

## Escopo

O domínio mínimo de duas entidades. A operação `increment`. O oráculo exato. A escolha
do denominador. A separação entre `commits` e `sucessos`. A comparação entre quatro
estratégias sobre a mesma carga.

## Fora de escopo

**A coluna `version` não existe no esquema hoje.** O [`ADR-0006`](../../adr/0006-a-forma-da-estrategia-de-concorrencia.md),
`Aceito`, decide que `OPTIMISTIC` a exige, mas a migração real nasce só quando a
arquitetura mínima existir (fila, posição 10) — ver R15. O esboço do ADR-0001 lê a
coluna antes disso, e não é normativo.

O SQL exato de cada uma das quatro estratégias e o mapa completo de exceção → retry
ficam para quando o código existir; o ADR-0006 fixa só o contrato (R12 a R16). Nível de
isolamento, classificação do veredito zero e formato curva estão em outros cards.

## Regras de negócio

| #   | Regra                                                                                                                                                                             | Evidência         | Aprovada por |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|--------------|
| R1  | O domínio tem duas entidades e nenhum nome de negócio: `Resource(id, value, capacity)` e `Allocation(id, resource_id, amount)`. Nenhuma outra coluna entra no MVP.                | ADR-0002:87-92    | pendente     |
| R2  | O esquema **NÃO DEVE** carregar uma coluna `version`.                                                                                                                             | ADR-0002:94-95    | pendente     |
| R3  | O identificador **DEVE** ser gerado pela aplicação a partir da semente. O esquema **NÃO DEVE** usar `SERIAL`, `IDENTITY`, `nextval` nem valor padrão do banco.                    | ADR-0002:124-126  | pendente     |
| R4  | O identificador **DEVE** ser função da semente e **NÃO DEVE** ser função do instante da execução. Duas execuções da mesma semente produzem os mesmos identificadores.             | ADR-0002:128-130  | pendente     |
| R5  | O oráculo produz uma contagem: `perdidas = commits − (value_final − value_inicial)`.                                                                                              | ADR-0002:135-139  | pendente     |
| R6  | `commits` é o número de passagens pela fronteira `AFTER_COMMIT`, contadas **por tentativa**.                                                                                      | ADR-0002:141      | pendente     |
| R7  | O denominador **DEVE** ser `commits`. Ele **NÃO DEVE** ser o número de operações submetidas nem o de operações que reportaram sucesso.                                            | ADR-0002:145-148  | pendente     |
| R8  | `sucessos` conta as execuções de operação que reportaram sucesso. A diferença `commits − sucessos` mede o dual write.                                                             | ADR-0002:171-173  | pendente     |
| R9  | O oráculo **DEVE** obter `value_final` do WAL do sistema medido, por replicação lógica. Ele **NÃO DEVE** emitir `SELECT` no schema dele nem derivar estado do log de observações. | ADR-0010, Decisão | pendente     |
| R17 | `value_final` é o último valor de `resource.value` visto no stream, e a comparação só ocorre depois de o stream alcançar o LSN do commit final.                                   | ADR-0010, Decisão | pendente     |
| R18 | O estado inicial **DEVE** ser inserido antes de cada execução, e não pressuposto, para que `value_inicial` venha do mesmo stream que `value_final`.                               | `O20`, 2026-08-05 | pendente     |
| R10 | O E1 **precisa falhar**. Se `value` final for igual a 100, a carga é insuficiente e nenhum resultado posterior significa alguma coisa.                                            | plano:397-398     | pendente     |
| R11 | Cada worker tem sua própria conexão. O pool **DEVE** ser maior que o número de workers, e isso **DEVE** ser verificado, não presumido.                                            | plano:579-582     | pendente     |
| R12 | O Lab Plane trata a estratégia como rótulo opaco. Nenhum componente **DEVE** inspecioná-lo ou ramificar por ele.                                                                  | ADR-0006, Decisão | pendente     |
| R13 | Cada estratégia responde "há outra tentativa?" a partir da exceção recebida. Uma exceção não reconhecida **DEVE** receber resposta não.                                           | ADR-0006, Decisão | pendente     |
| R14 | `PESSIMISTIC` é controle positivo: suas coincidências **DEVEM** ser zero em toda execução.                                                                                        | ADR-0006, Decisão | pendente     |
| R15 | `ATOMIC_UPDATE` é a estratégia de calibração exigida pelo ADR-0002 R3.                                                                                                            | ADR-0006, Decisão | pendente     |
| R16 | Uma estratégia **PODE** exigir coluna além das cinco do ADR-0002; a migração nasce no mesmo commit que a introduz no código.                                                      | ADR-0006, Decisão | pendente     |

O diagrama das duas contagens está no [Example Mapping](example-mapping.md).

## Integrações e contratos afetados

`increment` emite `SELECT` e `UPDATE` contra `resource` — isso é o domínio do sistema
medido, e não mudou. **O oráculo não emite `SELECT` nenhum.** Ele consome uma conexão de
replicação lógica sobre o WAL, e o schema do `system-under-test` permanece inacessível a
ele: não há `GRANT` cruzado. O transporte entre o WAL e o oráculo — conector, broker,
filtro por execução — é decisão própria, que depende desta. **Não existe DDL nem contrato
de esquema** — ver `Q-INT-5` em [`integrations.md`](../../architecture/integrations.md).

## Riscos e decisões pendentes

| Questão                                     | O que está em jogo                                                                                                |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| [`Q-0002-4`](../../questions/Q-0002-4.md)   | ninguém estabelece o estado inicial; R4 faz o identificador da semente colidir com as linhas da execução anterior |
| [`Q-0002-3`](../../questions/Q-0002-3.md)   | o oráculo lê o estado final quiescente, e não serve a violação transitória                                        |
| [`Q-0003-8`](../../questions/Q-0003-8.md)   | quantas vezes `OPTIMISTIC` tenta de novo sob exceção reconhecida não tem limite definido                          |
| o alcance da proibição de derivar de stream | `value_final` é lido do stream sem somar; se a proibição do ADR-0002 o alcança, R9 cai com ele                    |
| a emissão ao vivo das observações           | cada travessia até o `lab-journal` entra na janela medida; o buffer local não foi avaliado                        |

## Critérios de pronto

R1 a R18 verificadas por teste. O E1 produz `perdidas > 0` de forma repetida sob a carga
declarada. R7 é testada com o caso que a distingue: uma tentativa que commitou e
reportou falha entra na contagem; uma que esgotou as tentativas, não. R9 é testada pela
negativa: o `lab_plane` não tem `GRANT` no schema do `system-under-test`, e um `SELECT`
cruzado **falha** por permissão em vez de retornar linha.

## Links

[Example Mapping](example-mapping.md) · [BDD](behavior.feature) ·
[`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md) ·
[`ADR-0010`](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md),
`Aceito` — a fonte do oráculo ·
[`ADR-0006`](../../adr/0006-a-forma-da-estrategia-de-concorrencia.md), `Aceito` ·
[`execucao-de-experimento`](../execucao-de-experimento/feature-card.md)
