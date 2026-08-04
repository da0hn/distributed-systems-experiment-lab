# Feature Card — Detecção de proteção presente e inerte

Estado: `especificado, não implementado` · Origem: [`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`

Cobre o experimento **E5** (`write-skew-inert-protection`).

## Problema e resultado esperado

Um engenheiro ativa optimistic locking e acredita estar protegido. Duas transações
individualmente válidas leem a mesma soma, cada uma conclui que cabe uma alocação, e as
duas inserem. Nenhuma sobrescreve a outra — não há atualização perdida. A soma passa da
capacidade, **nenhuma exceção é lançada**, e a anotação continua lá.

O resultado esperado é a plataforma mostrar que "ter uma estratégia de concorrência" e
"estar protegido" são coisas diferentes. Nenhum teste de unidade detecta essa diferença.

## Atores e gatilho

- **Workers do Control Plane** — executam `allocate(resourceId, amount)`.
- **O oráculo do predicado** (Lab Plane) — avalia `Σ amount ≤ capacity` depois do fim.

Gatilho: uma execução de experimento sobre a operação `allocate`.

## Escopo

A operação `allocate`. O oráculo do predicado de capacidade. A verdade derivada, que é a
soma das alocações e não uma coluna. O nível de isolamento como eixo de variação do mesmo
experimento.

## Fora de escopo

O oráculo exato do contador está em
[`deteccao-de-atualizacao-perdida`](../deteccao-de-atualizacao-perdida/feature-card.md).
A semântica de cada estratégia de concorrência pertence à decisão que ainda não foi
tomada.

## Regras de negócio

| # | Regra | Evidência |
|---|---|---|
| R1 | `Σ amount` das linhas de `Allocation` de um recurso é a **verdade derivada**. `capacity` é o limite dela. A verdade não é um contador na linha do recurso. | ADR-0002:97-99 |
| R2 | `allocate(resourceId, amount)` lê a soma das alocações, compara com `capacity` e insere quando couber. | ADR-0002:119-120 |
| R3 | O oráculo avalia `Σ amount ≤ capacity` para cada recurso, com um `SELECT sum` emitido pelo **Lab Plane** depois do fim da execução. | ADR-0002:186-188 |
| R4 | O veredito é booleano, e a violação **DEVE** carregar os dois números: a soma obtida e a capacidade declarada. | ADR-0002:187-188 |
| R5 | O oráculo consulta o PostgreSQL. Ele **NÃO DEVE** derivar o estado final do log de observações. | ADR-0002:214-217 |
| R6 | O conjunto de entradas amostradas para `allocate` **DEVE** conter os três ramos do predicado: a alocação cabe, atinge a capacidade exata, e excede. | ADR-0002:263-266 |
| R7 | O mesmo experimento **DEVE** ser comparado sob `READ COMMITTED`, `REPEATABLE READ` e `SERIALIZABLE`. Só o terceiro aborta uma das transações, com SQLSTATE `40001`. | plano:472-474 |

O diagrama que mostra por que travar a linha do recurso não ajudaria está no
[Example Mapping](example-mapping.md).

## Integrações e contratos afetados

`allocate` emite um `SELECT sum` e um `INSERT` contra `allocation`. O oráculo emite um
`SELECT sum` do Lab Plane. **Não existe DDL nem contrato de esquema** — ver `Q-INT-5` em
[`integrations.md`](../../architecture/integrations.md).

O nível de isolamento é parâmetro da execução, e nada hoje o declara.

## Riscos e decisões pendentes

**O nível de isolamento não tem lugar na fila de decisões.** O E5 varre três níveis, e
nenhuma linha da fila nomeia esse parâmetro. Três destinos são possíveis, e a escolha não
foi feita — [`../../adr/README.md`](../../adr/README.md):240-269.

**A distinção que o E5 existe para mostrar corre risco de ser apagada.** Uma estratégia é
código da aplicação e muda o SQL emitido. Um nível de isolamento é propriedade da
transação e muda o que o banco faz com o **mesmo** SQL. Tratar o isolamento como mais um
valor da mesma enumeração apagaria a diferença.

**[`Q-0002-3`](../../questions/Q-0002-3.md)** — o oráculo descreve o estado final
quiescente, e serve ao E5 porque uma alocação excedente não sai da tabela.

## Critérios de pronto

R1 a R7 verificadas por teste. O E5 produz `Σ = 12 > capacity = 10` sem exceção nenhuma,
com `OPTIMISTIC` ativo. A varredura dos três níveis produz uma tabela em que apenas
`SERIALIZABLE` registra aborto com SQLSTATE `40001`.

## Links

- [Example Mapping](example-mapping.md) · [Cenários BDD](behavior.feature)
- [`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md) · [`plano-do-laboratorio.md`](../../plano-do-laboratorio.md), seção 6, E5
- [`execucao-de-experimento`](../execucao-de-experimento/feature-card.md) — o ciclo que consome este oráculo
