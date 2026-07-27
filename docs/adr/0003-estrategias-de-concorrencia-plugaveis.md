# ADR-0003: Estratégias de concorrência plugáveis

- **Estado:** Proposto
- **Data:** 2026-07-26
- **Etapa do roadmap:** 1
- **Relacionado:** ADR-0001, ADR-0002, ADR-0004, ADR-0006, ADR-0007

## Contexto

O ADR-0001 define uma invariante e dois modelos de verificação (`MATERIALIZED` e
`DERIVED`). O ADR-0002 define quatro origens que atacam a invariante de formas
diferentes. O laboratório precisa comparar mecanismos de proteção.

Comparar significa: executar o **mesmo** cenário, com a **mesma** carga e a **mesma**
semente de aleatoriedade, trocando apenas o mecanismo. Se o cenário mudar junto com o
mecanismo, a comparação não vale.

## Problema

Um mecanismo de concorrência normalmente está espalhado pelo código: uma anotação na
entidade, um `SELECT ... FOR UPDATE` no repositório, um índice único na migração, um
`try/catch` no serviço.

Se o mecanismo estiver espalhado, trocá-lo exige alterar código e reiniciar com uma
build diferente. A comparação vira um exercício de branches, não um experimento.

A pergunta é: como tornar o mecanismo de concorrência um **dado de configuração**, e
não uma característica do código?

## Decisão

O `Resource` declara uma estratégia de concorrência. A estratégia é um **atributo do
recurso**, gravado no banco, escolhido no momento da criação. Um experimento pode
criar dois recursos com estratégias diferentes e submetê-los à mesma carga.

O laboratório implementa **nove estratégias**, em dois grupos.

### Grupo 1 — exclusão mútua (resolvem escrita concorrente)

| Estratégia | Mecanismo | Protege contra | Não protege contra |
|---|---|---|---|
| `NONE` | nenhum | nada | tudo — **grupo de controle** |
| `ATOMIC_UPDATE` | `UPDATE ... SET x = x - n WHERE x >= n` | escrita concorrente, sem retry | reentrega (não é idempotente); escrita absoluta; `DERIVED` |
| `OPTIMISTIC` | coluna `version`, comparada no `UPDATE` | escrita concorrente na mesma linha | fato fora de ordem; **`DERIVED`** |
| `PESSIMISTIC` | `SELECT ... FOR UPDATE` | escrita concorrente; write skew se travar a linha do recurso | fato fora de ordem; custo de contenção |
| `SINGLE_WRITER` | todas as escritas passam por um dono eleito | tudo, por serialização | disponibilidade; o dono é ponto único |
| `PARTITION_KEY` | escritas do mesmo recurso vão para a mesma partição | tudo, por afinidade | rebalanceamento de partição |

### Grupo 2 — filtragem de mensagem (resolvem reentrega e ordenação)

| Estratégia | Mecanismo | Protege contra | Não protege contra |
|---|---|---|---|
| `IDEMPOTENCY_KEY` | tabela de chaves já vistas | retentativa do mesmo comando | comandos distintos concorrentes |
| `UNIQUE_CONSTRAINT` | índice único no banco | duplicata do mesmo fato | reordenação |
| `SEQUENCE_GUARD` | rejeita fato com timestamp lógico menor que o já aplicado | fato fora de ordem | escrita concorrente sem sequência |

### A estratégia `NONE` é obrigatória

`NONE` não é um erro nem um estado provisório. É o **grupo de controle**. Sem ela, o
laboratório não consegue provar que houve um problema para resolver.

O resultado esperado de todo experimento é: `NONE` viola a invariante, a estratégia
sob teste não viola. Se `NONE` **não** violar, o experimento não tem carga suficiente
e o resultado das outras estratégias não significa nada.

### `ATOMIC_UPDATE` separa atomicidade de idempotência

```sql
UPDATE resource SET available = available - 4
 WHERE id = ? AND available >= 4;
```

Esta consulta é correta sob qualquer nível de concorrência, sem `@Version`, sem
`FOR UPDATE`, sem retry. Ela é a solução mais barata que existe para o modelo
`MATERIALIZED` com comandos de delta.

Ela **não é idempotente**. O ADR-0007 estabelece que tudo no laboratório opera sob
*at-least-once*. Se o mesmo comando for reentregue, o decremento acontece duas vezes.
Nenhum erro é lançado. A invariante formal (`available >= 0`) continua satisfeita —
o que quebra é a correspondência entre `available` e as alocações que existem de fato.

Esse resultado é o motivo de `ATOMIC_UPDATE` estar na lista. Ele demonstra que
**atomicidade e idempotência são eixos ortogonais**. Optimistic lock tem o mesmo
defeito: ele detecta escrita concorrente, mas se a mesma mensagem for reprocessada
após o commit, a versão já avançou e o segundo decremento é aceito.

Nenhuma estratégia do Grupo 1 resolve reentrega. Isso é competência do Grupo 2.

### A matriz `capacityModel` × estratégia

O ADR-0001 define dois modelos de verificação. Cada célula abaixo é um experimento do
ADR-0004.

| Estratégia | `MATERIALIZED` | `DERIVED` |
|---|---|---|
| `NONE` | viola — lost update | viola — write skew |
| `ATOMIC_UPDATE` | protege | não se aplica — não há linha para decrementar |
| `OPTIMISTIC` | protege | **não protege** ⭐ |
| `PESSIMISTIC` | protege | protege apenas se travar a linha do `resource` |
| `SINGLE_WRITER` | protege | protege |
| `PARTITION_KEY` | protege | protege |
| Grupo 2 (todas) | ortogonal — não resolve concorrência | ortogonal |

⭐ **`DERIVED` + `OPTIMISTIC` não protege nada.** Inserir uma `allocation` não
incrementa a `version` do `resource`. Não existe linha compartilhada para versionar. A
anotação está presente, nenhuma exceção é lançada, e a invariante quebra. É a
**proteção presente e inerte** — o resultado mais valioso do laboratório.

### O limite de todas as nove estratégias

O ADR-0002 decidiu que o Agent reporta capacidade total, e que essa capacidade pode
encolher abaixo do que já está alocado. Quando isso acontece, a invariante do ADR-0001
é violada **sem nenhuma concorrência**.

Nenhuma estratégia desta lista resolve esse caso. Não há corrida para serializar, não
há duplicata para filtrar, não há ordem para restaurar. Existe apenas um fato
verdadeiro que torna o passado inválido.

Isso não é uma lacuna do ADR-0003. É o resultado que delimita seu escopo: **exclusão
mútua e consistência não são a mesma coisa**. As nove estratégias protegem o momento
da escrita. A convergência depois de um fato externo é competência do Reconciler e do
estado `OVERCOMMITTED`, não de lock.

`SEQUENCE_GUARD` continua sendo necessário para o Agent, mas por outro motivo: um
relato antigo de capacidade maior, chegando depois de um recente, restauraria
capacidade que não existe mais.

### Onde a estratégia vive

A estratégia é uma **porta** no domínio. As implementações são adaptadores na
infraestrutura. O domínio conhece a interface, nunca a implementação.

```
domain/
  ConcurrencyStrategy          (porta — interface, sem Spring, sem JPA)
  ConcurrencyStrategyType      (enum)
  CapacityModel                (enum — ADR-0001)
infrastructure/concurrency/
  AtomicUpdateStrategy         (adaptador)
  OptimisticStrategy
  PessimisticStrategy
  SequenceGuardStrategy
  ...
```

O ADR-0006 define a guarda ArchUnit que impede o domínio de importar a
infraestrutura.

### Ordem de implementação

Nove estratégias são muitas para a Etapa 1. A entrega é incremental, e cada estratégia
entra na etapa em que seu contexto já existe:

| Etapa | Estratégias | Motivo |
|---|---|---|
| 1 | `NONE`, `ATOMIC_UPDATE`, `OPTIMISTIC`, `PESSIMISTIC` | só precisam do banco |
| 3 | `IDEMPOTENCY_KEY`, `UNIQUE_CONSTRAINT`, `SEQUENCE_GUARD` | precisam de mensageria e do Inbox (ADR-0007) |
| 5 | `SINGLE_WRITER`, `PARTITION_KEY` | precisam de múltiplas réplicas |

## Questões em aberto

Duas questões surgiram durante o debate do ADR-0001 e ainda não têm decisão.

### 1. Um campo ou dois?

Os dois grupos são ortogonais. Eles **se compõem**, não se substituem. Um recurso
realista usaria `OPTIMISTIC` **e** `IDEMPOTENCY_KEY` ao mesmo tempo.

Um campo `concurrencyStrategy` único não expressa isso. As opções são:

- dois campos: `concurrencyStrategy` (Grupo 1) e `messageFilterStrategy` (Grupo 2)
- um campo do tipo lista: `strategies: [OPTIMISTIC, IDEMPOTENCY_KEY]`
- manter um campo só e aceitar que combinações não são testáveis

### 2. `SERIALIZABLE` é uma estratégia?

O ADR-0001 estabelece que a proteção correta para o modelo `DERIVED` é o nível de
isolamento `SERIALIZABLE`, com retry no SQLSTATE `40001`. Isso não aparece na lista
acima.

Nível de isolamento é propriedade da transação, não do recurso. Mas o PostgreSQL
permite defini-lo por transação, então ele **poderia** virar uma décima estratégia.
Contra: ele muda a semântica de toda a transação, não só da verificação da invariante.

## Consequências

### Positivas

- Trocar a estratégia é mudar um campo. Nenhuma build nova. Nenhum deploy novo.
- Duas estratégias podem coexistir no mesmo processo, ao mesmo tempo, sob a mesma
  carga. Isso elimina a variável "o ambiente estava diferente".
- A matriz vira uma suíte de testes. Cada célula "não protege contra" é um experimento
  com falha esperada. Um experimento que **deveria** falhar e passa indica erro no
  laboratório.
- A separação em dois grupos torna explícito que lock e idempotência resolvem
  problemas diferentes. Essa confusão é comum e cara.

### Negativas

- O código do caso de uso fica mais indireto. Uma chamada a `strategy.execute(...)` é
  menos legível que um `SELECT ... FOR UPDATE` explícito. Este custo é aceito de
  propósito: o laboratório troca legibilidade local por comparabilidade.
- Algumas estratégias não são puramente de código. `UNIQUE_CONSTRAINT` exige um índice
  no banco. `PARTITION_KEY` exige configuração do broker. A abstração vaza. Isso
  precisa ser documentado por estratégia, não escondido.
- Nove adaptadores é bastante superfície para manter. A ordem de implementação
  incremental mitiga, mas não elimina.

### Neutras

- Nem toda estratégia se aplica a toda origem de escrita. `SEQUENCE_GUARD` só faz
  sentido para fatos com sequência (Agent). A matriz origem × estratégia tem células
  vazias, e isso é informação, não defeito.

## Alternativas consideradas

### Alternativa A — um serviço por estratégia

Cada estratégia vira um deploy separado, selecionado por roteamento.

**Descartada.** Multiplica o custo operacional por nove. Introduz a variável
"ambiente diferente" exatamente onde o laboratório precisa eliminá-la.

### Alternativa B — estratégia escolhida por perfil do Spring

Um perfil por estratégia, escolhido na inicialização.

**Descartada.** Impede que duas estratégias coexistam na mesma execução. Todo
experimento exigiria duas execuções, em momentos diferentes, com condições de máquina
diferentes. A comparação perderia validade.

### Alternativa C — estratégia por requisição (cabeçalho HTTP)

O cliente escolhe a estratégia a cada chamada.

**Descartada.** A estratégia é uma propriedade do dado protegido, não da chamada. Duas
chamadas concorrentes com estratégias diferentes sobre o mesmo recurso produzem um
resultado sem significado — a proteção mais fraca vence, e o experimento não mede
nada.

## Quando esta decisão deixa de valer

Reveja esta decisão se o custo de manter nove adaptadores superar o valor da
comparação. O sinal concreto: uma estratégia que fica seis meses sem aparecer em
nenhum experimento. Ela deve ser removida, não mantida por simetria.
