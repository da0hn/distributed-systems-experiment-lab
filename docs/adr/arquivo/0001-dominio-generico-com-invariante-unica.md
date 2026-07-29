# ADR-0001: Domínio genérico de recursos com invariante única

- **Estado:** Proposto
- **Data:** 2026-07-26
- **Etapa do roadmap:** 0
- **Relacionado:** ADR-0002, ADR-0003, ADR-0004

## Contexto

O Distributed Consistency Lab não é uma aplicação de negócio. O objetivo é estudar
consistência em sistemas distribuídos. O laboratório precisa de um domínio para
existir, mas o domínio não é o objeto de estudo.

A maioria dos temas do laboratório é independente do domínio. Outbox, inbox, retry,
DLQ, deduplicação, observabilidade, chaos e Kubernetes funcionam igual em qualquer
domínio. Apenas seis temas dependem do domínio:

- contenção de escrita
- ordenação de fatos
- CQRS e defasagem de leitura
- saga e compensação
- consistência eventual visível ao usuário
- backpressure

## Problema

Duas forças estão em conflito.

**Força 1 — um domínio de negócio real custa caro.** Um domínio como venda de
ingressos traz regras de preço, promoção, reembolso e fiscal. Essas regras consomem
tempo de implementação. Elas não ensinam nada sobre consistência.

**Força 2 — um domínio sem regra nenhuma não serve.** Concorrência só é observável
quando existe uma invariante que pode ser violada. Um campo com `@Version` num objeto
sem regra não protege nada. Sem invariante, um teste de concorrência não tem veredito:
não existe estado "errado" para detectar.

A pergunta é: qual é o menor domínio que ainda produz bugs de consistência reais?

## Decisão

O domínio é a **gestão de recursos distribuídos**.

Um `Resource` tem uma capacidade. Alocações consomem capacidade. O laboratório
mantém **uma única invariante**:

```
Para todo Resource:
    Σ(alocações ativas) ≤ capacidade
    capacidade disponível ≥ 0
```

Essa invariante é a única regra de negócio do laboratório. Nenhuma outra regra é
adicionada sem um ADR novo.

Todo experimento tem o mesmo veredito: **a invariante foi violada?** A resposta é
binária e verificável por consulta SQL, sem julgamento humano.

### A invariante tem dois modelos de verificação

Declarar a invariante não basta. **Como ela é verificada** determina quais bugs o
laboratório consegue produzir. Existem dois modelos, e o `Resource` declara qual usa:

```
Resource {
  capacity
  concurrencyStrategy: NONE | OPTIMISTIC | PESSIMISTIC | ...   (ADR-0003)
  capacityModel:       MATERIALIZED | DERIVED
}
```

As duas tabelas existem nos dois modelos. O que muda é **qual consulta decide**.

```sql
resource   { id, capacity, available, version }   -- 'available' só é fonte de verdade em MATERIALIZED
allocation { id, resource_id, amount, status }
```

#### `MATERIALIZED` — a verdade é o contador na linha do recurso

```sql
UPDATE resource SET available = available - 4
 WHERE id = ? AND available >= 4;
-- 0 linhas afetadas = capacidade insuficiente
```

A linha lida e a linha escrita são a mesma. O lock de linha do PostgreSQL protege sem
esforço adicional.

#### `DERIVED` — a verdade é a soma das alocações ativas

```sql
SELECT sum(amount) FROM allocation WHERE resource_id = ? AND status = 'ACTIVE';
-- se soma + amount <= capacity:
INSERT INTO allocation (resource_id, amount, status) VALUES (?, ?, 'ACTIVE');
```

A leitura toca as linhas de `allocation`. A escrita **cria uma linha nova**. Não há
sobreposição. Nada conflita. Duas transações concorrentes leem o mesmo valor, ambas
concluem que cabe, e a soma final viola a invariante.

**`SELECT ... FOR UPDATE` não resolve o modelo `DERIVED`.** Não existe linha para
travar: a linha que quebra a invariante ainda não existe no momento da leitura.

### Por que os dois modelos, e não um

Cada modelo produz uma família de anomalia diferente:

| | `MATERIALIZED` | `DERIVED` |
|---|---|---|
| Bug característico | lost update | **write skew com phantom** |
| Lock de linha protege | sim | **não** |
| `UPDATE` atômico resolve | sim, em uma linha de SQL | não se aplica |
| Optimistic lock no `resource` protege | sim | **não** — ver abaixo |
| Exige `SERIALIZABLE` ou lock artificial | não | sim |
| Sofre *drift* (contador diverge da soma real) | sim | não — só existe uma verdade |
| Custo de ler a capacidade | O(1) | O(n) alocações |

O modelo `DERIVED` é o único que produz **write skew** no sentido estrito: a condição
violada é sobre um *conjunto*, não sobre um registro. Essa é a única família de
anomalia que lock de linha não alcança. As saídas reais são três, cada uma com custo
próprio:

1. **`SERIALIZABLE`** — o SSI do PostgreSQL detecta a dependência rw e aborta uma das
   transações com SQLSTATE `40001`. Exige retry na aplicação.
2. **Materializar o conflito** — `SELECT ... FROM resource WHERE id = ? FOR UPDATE`
   antes da soma, criando artificialmente uma linha compartilhada para travar.
   Funciona sob `READ COMMITTED`. Serializa todas as escritas daquele recurso.
3. **Voltar ao modelo `MATERIALIZED`** — é o que sistemas reais fazem.

Isso revela por que sistemas de produção denormalizam contadores mesmo sabendo que é
redundante: a denormalização não é otimização de leitura. É a criação de um **ponto de
serialização**.

### O experimento que só existe com os dois modelos

A combinação `DERIVED` + `OPTIMISTIC` **não protege nada**. Inserir uma `allocation`
não incrementa a `version` do `resource` — não existe linha compartilhada para
versionar. A anotação está presente, o desenvolvedor acredita estar protegido, nenhuma
exceção é lançada, e a invariante quebra.

Esta é a **proteção presente e inerte**. Nenhum teste de unidade a detecta. É o
resultado mais valioso que este laboratório pode produzir, e ele é impossível sem o
modelo `DERIVED`.

A matriz `capacityModel` × `concurrencyStrategy` (ADR-0003) tem outras células com
resultado não óbvio. Cada célula é um experimento do ADR-0004.

## Consequências

### Positivas

- O veredito de qualquer experimento é objetivo. Uma query decide se a estratégia
  funcionou.
- A mesma invariante produz **duas famílias de anomalia** conforme o modelo de
  verificação: lost update em `MATERIALIZED`, write skew em `DERIVED`. Isso dobra o
  espaço de experimentos sem adicionar regra de negócio.
- O tempo de implementação vai para infraestrutura de consistência, não para regra
  de negócio.
- O domínio é entendível em uma frase. Isso reduz o custo de explicar qualquer
  experimento.
- O custo marginal do segundo modelo é baixo: as duas tabelas existem de qualquer
  forma. O modelo `MATERIALIZED` precisa de `allocation` para auditoria e para o
  Reconciler detectar drift.

### Negativas

- **A matriz de teste dobra.** Todo cenário passa a ter duas execuções. Isso é
  mitigado pelo ADR-0004, que torna um experimento um arquivo JSON — mas o tempo de
  execução da suíte cresce de verdade.
- **Dois adaptadores de repositório na Etapa 1.** O caso de uso não pode conhecer o
  modelo: ele chama uma porta, e o adaptador escolhido decide a consulta. Isso é mais
  indireção logo no início do projeto.
- O domínio é abstrato. Ele não gera intuição de negócio. Quem lê o código não
  reconhece o problema de imediato, como reconheceria em "reserva de assento".
- O laboratório não exercita modelagem de domínio rica. Value objects, políticas e
  especificações aparecem pouco. DDD tático fica sub-representado.
- Um único agregado limita os cenários de consistência **entre** agregados. A saga
  precisa de mais de um recurso para ser interessante (ver ADR-0008).

### Neutras

- O nome "recurso" é genérico de propósito. Ele pode representar CPU, GPU, licença,
  vaga ou cota. A representação não muda o comportamento do sistema.

### Dependência que esta decisão cria

A origem **Reconciler** do ADR-0002 só tem propósito no modelo `MATERIALIZED`. Ela
existe para corrigir *drift*, e drift só existe quando há estado duplicado. No modelo
`DERIVED` não há o que reconciliar.

Consequência: experimentos com Reconciler exigem `capacityModel: MATERIALIZED`. Esta é
uma célula vazia legítima da matriz, não uma lacuna.

> **Nota de revisão (ADR-0002).** Esta consequência não vale mais. O ADR-0002 deu ao
> Reconciler um segundo papel — resolver sobrecomprometimento depois de o Agent
> reduzir a capacidade — que existe nos dois `capacityModel`. A decisão deste ADR não
> muda; apenas esta consequência foi superada.

## Alternativas consideradas

### Alternativa A — domínio de negócio realista (venda de ingressos)

Um marketplace de eventos ao vivo. Assentos, reservas, expiração de carrinho,
pagamento.

**Descartada.** O domínio traz regras que não ensinam sobre consistência: cálculo de
preço, taxa de conveniência, política de reembolso, mapa de assentos. Estimativa: mais
da metade do código seria regra de negócio. O laboratório teria menos experimentos
pelo mesmo esforço.

Observação: esse domínio é melhor para **demonstrar** o laboratório a terceiros. A
invariante escolhida aqui é isomórfica a "não vender o mesmo assento duas vezes". Se
no futuro for necessário demonstrar o laboratório, basta renomear os conceitos.

### Alternativa B — recurso genérico sem invariante

Um objeto com campos arbitrários, atualizado por várias origens. Sem regra de
negócio.

**Descartada.** Sem invariante não existe erro para detectar. Um `lost update` num
campo sem regra é indistinguível de um `last-write-wins` intencional. O laboratório
não teria como provar que uma estratégia de concorrência é melhor que outra.

Este é o erro mais comum em laboratórios de concorrência: adicionar `@Version` a uma
entidade e concluir que o problema está resolvido, sem nunca ter tido um problema.

### Alternativa C — apenas o modelo `MATERIALIZED`

Uma Etapa 1 mais enxuta. O contador na linha do recurso, com lost update como bug
principal.

**Descartada.** Adia indefinidamente o write skew — a única anomalia que lock de linha
não resolve, e a que mais aparece em incidentes reais. Pior: torna impossível o
experimento da proteção inerte (`DERIVED` + `OPTIMISTIC`), que é o resultado mais
contraintuitivo do laboratório.

O argumento de economia também é fraco: o schema é o mesmo nos dois modelos.

### Alternativa D — apenas o modelo `DERIVED`

Uma única fonte de verdade, sem estado duplicado, sem possibilidade de drift.

**Descartada.** É a modelagem mais correta, e por isso mesmo produz menos bugs para
estudar. Ela elimina a origem Reconciler do ADR-0002, elimina o cenário de drift, e
força `SERIALIZABLE` com retry já na Etapa 1 — antes de o laboratório ter observabilidade
para entender o que o retry está fazendo.

### Alternativa E — várias invariantes desde o início

Capacidade, mais cota por tenant, mais janela de tempo, mais prioridade.

**Descartada por ora.** Cada invariante adicional multiplica os cenários de teste. O
laboratório precisa primeiro provar que consegue proteger **uma**. Invariantes
adicionais podem ser introduzidas depois, cada uma com seu ADR, quando existir um
experimento que as exija.

## Quando esta decisão deixa de valer

Reveja esta decisão se os experimentos começarem a repetir o mesmo veredito sem
informação nova. Isso indica que a invariante única esgotou o espaço de cenários.
O sinal concreto: três experimentos seguidos cujo resultado foi previsível antes da
execução.

Reveja o suporte a dois modelos se uma das colunas da matriz `capacityModel` ×
`concurrencyStrategy` ficar sem nenhum experimento ativo. Um modelo sem uso é custo de
manutenção sem retorno.
