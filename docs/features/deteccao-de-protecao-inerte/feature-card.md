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

- **Workers do system under test** — executam `allocate(resourceId, amount)`.
- **O oráculo do predicado** (Lab Plane) — avalia `Σ amount ≤ capacity` depois do fim, e
  **NÃO DEVE** emitir `SELECT` no schema do sistema medido, desde o
  [`ADR-0010`](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md).

Gatilho: uma execução de experimento sobre a operação `allocate`.

**De onde este oráculo obtém `Σ amount` não está decidido, e o E5 não roda até que
esteja.** Somar eventos de `INSERT` vindos do WAL é reconstruir um total a partir de um
stream — exatamente o que a regra `R5` proíbe. A saída exige decidir o alcance daquela
proibição, e enquanto isso não acontecer este oráculo não tem fonte nenhuma.

## Escopo

A operação `allocate`. O oráculo do predicado de capacidade. A verdade derivada, que é a
soma das alocações e não uma coluna. O nível de isolamento como eixo de variação do
mesmo experimento.

## Fora de escopo

O oráculo exato do contador está em
[`deteccao-de-atualizacao-perdida`](../deteccao-de-atualizacao-perdida/feature-card.md).
A semântica de cada estratégia de concorrência pertence à decisão que ainda não foi
tomada.

## Regras de negócio

| #  | Regra                                                                                                                                                                                     | Evidência         | Aprovada por |
|----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|--------------|
| R1 | `Σ amount` das linhas de `Allocation` de um recurso é a **verdade derivada**. `capacity` é o limite dela. A verdade não é um contador na linha do recurso.                                | ADR-0002:97-99    | pendente     |
| R2 | `allocate(resourceId, amount)` lê a soma das alocações, compara com `capacity` e insere quando couber.                                                                                    | ADR-0002:119-120  | pendente     |
| R3 | O oráculo avalia `Σ amount ≤ capacity` para cada recurso depois do fim da execução, e **NÃO DEVE** emitir `SELECT` no schema do sistema medido. De onde vem `Σ amount` segue sem decisão. | ADR-0010, Decisão | pendente     |
| R4 | O veredito é booleano, e a violação **DEVE** carregar os dois números: a soma obtida e a capacidade declarada.                                                                            | ADR-0002:187-188  | pendente     |
| R5 | O oráculo **NÃO DEVE** derivar o estado final do log de observações do Lab Plane. Se a proibição alcança somar eventos de `INSERT` vindos do WAL não foi decidido.                        | ADR-0002:214-217  | pendente     |
| R6 | O conjunto de entradas amostradas para `allocate` **DEVE** conter os três ramos do predicado: a alocação cabe, atinge a capacidade exata, e excede.                                       | ADR-0002:263-266  | pendente     |
| R7 | O mesmo experimento **DEVE** ser comparado sob `READ COMMITTED`, `REPEATABLE READ` e `SERIALIZABLE`. Só o terceiro aborta uma das transações, com SQLSTATE `40001`.                       | plano:472-474     | pendente     |

O diagrama que mostra por que travar a linha do recurso não ajudaria está no
[Example Mapping](example-mapping.md).

## Integrações e contratos afetados

`allocate` emite um `SELECT sum` e um `INSERT` contra `allocation` — isso é o domínio do
sistema medido, e não mudou. **O oráculo não emite `SELECT`**: o schema do
`system-under-test` é inacessível ao Lab Plane, sem `GRANT` cruzado. **A fonte que
substitui aquele `SELECT sum` não existe ainda.** **Não existe DDL nem contrato de
esquema** — ver `Q-INT-5` em [`integrations.md`](../../architecture/integrations.md).

O nível de isolamento é parâmetro da execução, e nada hoje o declara.

## Riscos e decisões pendentes

**O nível de isolamento não tem lugar na fila de decisões.** O E5 varre três níveis, e
nenhuma linha da fila nomeia esse parâmetro. Três destinos são possíveis, e a escolha
não foi feita — [`../../adr/README.md`](../../adr/README.md):240-269.

**A distinção que o E5 existe para mostrar corre risco de ser apagada.** Uma estratégia é
código da aplicação e muda o SQL emitido. Um nível de isolamento é propriedade da
transação e muda o que o banco faz com o **mesmo** SQL. Tratar o isolamento como mais um
valor da mesma enumeração apagaria a diferença.

**[`Q-0002-3`](../../questions/Q-0002-3.md)** — o oráculo descreve o estado final
quiescente, e serve ao E5 porque uma alocação excedente não sai da tabela.

**O E5 está bloqueado pela fonte do oráculo.** O
[`ADR-0010`](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md)
retirou o `SELECT sum` do Lab Plane e não pôs nada no lugar. Enquanto o alcance da regra
`R5` não for decidido, este oráculo **não tem fonte**, e `R3` não pode ser verificada.

## Critérios de pronto

R1, R2 e R4 a R7 verificadas por teste. **R3 fica bloqueada** — sem fonte declarada para
`Σ amount`, não há o que testar. O E5 produz `Σ = 12 > capacity = 10` sem
exceção nenhuma, com `OPTIMISTIC` ativo. A varredura dos três níveis produz uma tabela em
que apenas `SERIALIZABLE` registra aborto com SQLSTATE `40001`. R5 é testada pela
negativa: o `lab_plane` não tem `GRANT` no schema do `system-under-test`, e um `SELECT`
cruzado **falha** por permissão.

## Links

- [Example Mapping](example-mapping.md) · [Cenários BDD](behavior.feature)
- [`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md) · [`plano-do-laboratorio.md`](../../plano-do-laboratorio.md), seção 6, E5
- [`ADR-0010`](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md), `Aceito` — retirou o `SELECT sum` deste oráculo
- [`execucao-de-experimento`](../execucao-de-experimento/feature-card.md) — o ciclo que consome este oráculo
