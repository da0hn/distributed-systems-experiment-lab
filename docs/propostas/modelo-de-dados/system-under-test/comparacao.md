# Comparação das três propostas de modelo de dados do `sut`

As três propostas desta pasta foram escritas em isolamento, cada uma sem conhecer as
outras. Este arquivo as põe lado a lado, e não escolhe nenhuma. O dono da forma vigente
continua sendo
[`schemas/sut.md`](../../../architecture/schemas/sut.md#o-schema-do-sistema-medido-sut).

## O eixo real da escolha

As três concordam em quase tudo que costuma ser debatido: nenhuma chave estrangeira,
nenhum `DEFAULT`, nenhum trigger, nenhum `CHECK` que recuse a anomalia, chave composta
com o discriminador primeiro, e o oráculo lendo só o WAL. O que as separa é anterior a
isso, e é uma pergunta só: **qual contaminação da medida é inaceitável.** Para a
proposta 1, é toda estrutura que exista para medir, e por isso o instrumento paga tudo.
Para a proposta 2, é o veredito que só existe como escalar agregado, e por isso ela paga
um `INSERT` dentro da transação medida. Para a proposta 3, é o schema que muda entre
duas execuções comparadas, e por isso ela paga tudo na primeira migração. As três
definições são legítimas e mutuamente exclusivas: satisfazer uma piora as outras por
construção. Escolher é dizer qual fidelidade vale mais — a do sistema medido, a da
evidência, ou a da comparação.

## O que cada uma decide diferente

| O que muda                                  | Proposta 1 — o domínio nu                                                                                                  | Proposta 2 — o rastro append-only                                                                                                   | Proposta 3 — o catálogo de mecanismos                                                                        |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| tabelas no schema                           | `resource` e `allocation`                                                                                                  | as duas, mais `state_change`, `resource_projection` e `lease`                                                                       | as duas, mais `outbox`, `inbox`, `lease` e `resource_projection`                                             |
| colunas novas em `resource`                 | `version`, e só quando a estratégia `OPTIMISTIC` chegar                                                                    | `version`, na mesma condição                                                                                                        | `version` e `fence_token`, as duas já no seeding, inertes em zero                                            |
| quando o schema muda                        | a cada experimento que exigir mecanismo novo                                                                               | uma vez; o rastro serve a todos os grupos                                                                                           | nunca depois da primeira migração — é o ponto da proposta                                                    |
| quem paga o custo de observar               | o instrumento, em código, um fenômeno por vez                                                                              | a transação medida, com um `INSERT` por escrita commitada                                                                           | quem lê a migração, e o stream, em relações a mais                                                           |
| o que entra na transação medida             | nada além do domínio                                                                                                       | a linha do rastro, sempre                                                                                                           | nada, enquanto o mecanismo estiver inerte                                                                    |
| violação transitória e trajetória do estado | invisíveis, como as [negativas do ADR-0002](../../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#negativas) já aceitam | reconstruíveis pelo par `observed`/`written` de linhas vizinhas                                                                     | invisíveis, como na proposta 1                                                                               |
| segunda medida de `commits`                 | não existe; o número continua só do instrumento                                                                            | a contagem das linhas do rastro, vinda das escritas reais                                                                           | não existe                                                                                                   |
| grupo C, escrita parcial                    | outbox e inbox nascem na migração do experimento que os estuda                                                             | `resource_projection` com a posição aplicada; sem outbox e sem inbox                                                                | `outbox` com `published_at` anulável, e `inbox` cuja chave primária **é** a deduplicação                     |
| grupo E, posse no tempo                     | lease e token nascem na migração do experimento                                                                            | `lease`, e o `fencing_token` apresentado também vai no rastro                                                                       | `lease`, e o maior token visto guardado em `resource.fence_token`                                            |
| marca de fim da janela medida               | `capacity = 0`, escrita pelo sistema medido fora da janela                                                                 | não escolhida                                                                                                                       | não escolhida                                                                                                |
| índices aditivos                            | um, `(partition_id, resource_id)` sobre `allocation`                                                                       | o mesmo, e nenhum sobre o rastro                                                                                                    | dois: o mesmo, e `(partition_id, published_at)` sobre `outbox`, não parcial                                  |
| relações na publicação de CDC               | duas, e a publicação nem entra na migração do `sut`                                                                        | cinco                                                                                                                               | seis, todas                                                                                                  |
| coluna anulável                             | nenhuma                                                                                                                    | `fencing_token`, e ela viaja vazia fora do grupo E                                                                                  | `published_at`, e a transição de nulo para instante é o evento do relay                                      |
| o que ela assume, e as outras não           | que a linha órfã é verificável no stream, e que o `UPDATE` traz `capacity` quando só `value` mudou                         | que uma linha escrita na mesma transação prova o que aquela transação **leu**, coisa que a identidade de réplica cheia não provaria | que a operação medida nunca emite `SELECT *` nem nomeia coluna que não usa; sem essa regra, "inerte" é falso |
| onde ela colide com a regra pedagógica      | em nada, exceto por `version`                                                                                              | no rastro, que nenhum sistema ingênuo escreveria                                                                                    | seis vezes, e a própria proposta o declara e diz o que paga                                                  |

## O que cada uma torna fácil, e o que torna caro

**Proposta 1.** Ela torna fácil defender qualquer resultado: o sistema medido é
indistinguível de um sistema ingênuo, e ninguém pode alegar que a estrutura produziu o
fenômeno. O caro vem depois: cada fenômeno novo custa código no instrumento, cada
mecanismo custa migração própria, e o schema medido vira a soma de muitas migrações de
experimento — a variável escondida que a proposta 3 existe para eliminar.

**Proposta 2.** Ela torna fácil o diagnóstico: a perda deixa de ser diferença de dois
escalares e passa a ser um par vizinho em que `observed` não é o `written` do
antecessor. Torna fácil a calibração ganhar um segundo testemunho. O caro é o mais
difícil de aceitar das três: o rastro entra na transação que o experimento mede, e
alonga a janela entre a leitura e o commit para **mais** anomalia. O número absoluto de
perdas deixa de ser comparável ao de um laboratório sem rastro.

**Proposta 3.** Ela torna fácil a comparação que o
[ADR-0004](../../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-zero-é-classificado-e-a-classificação-tem-quatro-valores)
torna obrigatória: o grupo de controle roda contra os mesmos bytes das demais
estratégias. Torna fácil observar todo mecanismo do roadmap pelo WAL. O caro tem duas
faces. Quem abrir a migração encontra seis soluções antes de ter visto anomalia nenhuma.
E a palavra "inerte" depende de uma regra que hoje é texto, e não guarda executável: se
um único statement emitir `SELECT *`, a coluna entra no traço de SQL e o argumento cai.

## As perguntas que sobrevivem a qualquer escolha

Estas continuam abertas depois da escolha.

- **`version` está no esquema, ou chega com a estratégia?** As três a desenham em
  `resource`, e a forma vigente não a tem. Quem a introduz é o ADR de estratégias de
  concorrência, a quem o
  [ADR-0002](../../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#decisão) delegou
  também a política que a lê.
- **O que um evento de `UPDATE` carrega sob a identidade de réplica padrão?** As três
  dependem disso por caminhos diferentes, e é fato sobre o PostgreSQL.
- **O que "contiguidade de LSN" significa sobre um stream filtrado?** A guarda do
  [ADR-0013](../../../adr/0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md#decisão)
  exige conferi-la antes de somar, e LSN é deslocamento em bytes, e não contador.
- **O transporte preserva a fronteira e a ordem interna da transação?** As três precisam
  disso para atribuir eventos a uma tentativa.
- **Onde a linha órfã é verificada?** O
  [ADR-0015](../../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#sem-chave-estrangeira-em-allocationresource_id)
  a deixou aberta para uma coluna; as propostas 2 e 3 a multiplicam sem respondê-la.
- **Qual é a forma da marca de fim da janela medida?** Só a proposta 1 escolhe uma, por
  conta própria.
- **Quem apaga as linhas de uma execução encerrada, e quando?** As três declaram não
  decidir isso.
- **Qual oráculo lê o que não é `resource` nem `allocation`?** Rastro, projeção, outbox,
  inbox e posse não têm oráculo decidido, e a composição dos formatos de veredito segue
  [aberta](../../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#o-que-este-adr-não-decide).
