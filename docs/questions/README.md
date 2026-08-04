# Questões

Questões levantadas durante o debate de um ADR da série corrente, cuja resposta pertence a
uma decisão diferente da que as levantou. Cada uma vive num arquivo próprio nesta pasta,
para que uma decisão futura, um Feature Card ou um Example Mapping possa referenciá-la
diretamente, sem depender de uma âncora dentro de `adr/README.md`.

O processo de debate que produz uma questão está descrito em
[`adr/README.md`](../adr/README.md#processo-de-debate). Este arquivo documenta apenas o
que acontece **depois** que uma questão nasce.

## De onde uma questão vem

Uma questão nasce na seção `## Questões em aberto` de um ADR ainda `Proposto`. Se a
resposta pertence a outra decisão, ela recebe status `encaminhado` e, no ato da aceitação
do ADR de origem, é transportada para um arquivo nesta pasta — **inteira, não resumida**.
O ADR de destino precisa nascer com o problema que motivou a entrada dele na
[fila de decisões](../adr/README.md#fila-de-decisões). Um resumo é a mesma perda, mais
devagar.

## Identificador

Cada questão recebe um identificador `Q-NNNN-K`: `NNNN` é o ADR de origem, `K` é o
número que a questão tinha na seção `## Questões em aberto` dele. Os dois são congelados
no ato da aceitação, e o identificador nunca é reutilizado. **Cite uma questão por esse
identificador**, nunca por "a questão K do ADR-NNNN" — aquela seção deixa de existir
quando o ADR é aceito, e a citação passaria a apontar para nada.

## Ciclo de vida

Uma questão nasce com status `pendente`. Ela **não** é apagada quando alguém a resolve: o
status passa a `resolvida por ADR-NNNN`, e o arquivo dela abre nomeando a subseção do ADR
onde a decisão está. O enunciado permanece porque ele registra o que estava em jogo antes
da decisão — e é isso que um leitor futuro não consegue reconstruir a partir do ADR de
destino.

O custo dessa escolha é que o índice abaixo cresce e passa a listar questão viva ao lado
de questão morta. A coluna `Status` é a única marca que as separa, e ela é obrigatória
por isso.

O enunciado transportado é reescrito num ponto só, no momento em que o arquivo é criado:
as referências internas ao ADR de origem. "Este ADR", "aqui" e "a questão 3" não
significam nada fora do documento em que foram escritas, e passam a nomear o ADR e o
identificador.

## Índice

| ID                        | Questão                                                                           | Origem   | Destino na fila              | Status                 |
|---------------------------|-----------------------------------------------------------------------------------|----------|------------------------------|------------------------|
| [`Q-0001-1`](Q-0001-1.md) | O endereço da fronteira precisa sobreviver à edição da operação                   | ADR-0001 | o log de observações         | `pendente`             |
| [`Q-0001-2`](Q-0001-2.md) | O compartilhamento por colaborador injetado continua sem guarda                   | ADR-0001 | estratégias de concorrência  | resolvida por ADR-0006 |
| [`Q-0001-3`](Q-0001-3.md) | O critério de igualdade entre dois traços de SQL não está definido                | ADR-0001 | o domínio mínimo             | resolvida por ADR-0002 |
| [`Q-0001-4`](Q-0001-4.md) | O escalonador precisa de um protocolo de desistência                              | ADR-0001 | a forma do escalonador       | resolvida por ADR-0005 |
| [`Q-0002-1`](Q-0002-1.md) | A comparação por valor depende de regras que nenhum teste verifica                | ADR-0002 | arquitetura mínima e guardas | `pendente`             |
| [`Q-0002-2`](Q-0002-2.md) | Quem declara que a execução terminou, e o oráculo lê antes ou depois disso        | ADR-0002 | a forma do escalonador       | resolvida por ADR-0005 |
| [`Q-0002-3`](Q-0002-3.md) | Os dois oráculos descrevem apenas o estado final quiescente                       | ADR-0002 | os dois formatos de veredito | `pendente`             |
| [`Q-0002-4`](Q-0002-4.md) | O estado inicial não é estabelecido por ninguém                                   | ADR-0002 | Experiment                   | `pendente`             |
| [`Q-0003-1`](Q-0003-1.md) | Um worker que nunca chega trava o agendamento, e a recusa por texto não o alcança | ADR-0003 | a forma do escalonador       | resolvida por ADR-0005 |
| [`Q-0003-2`](Q-0003-2.md) | Um agendamento sobre uma tentativa que talvez não ocorra                          | ADR-0003 | a forma do escalonador       | resolvida por ADR-0005 |
| [`Q-0003-3`](Q-0003-3.md) | Duas execuções do mesmo experimento não têm critério de igualdade                 | ADR-0003 | o log de observações         | `pendente`             |
| [`Q-0003-8`](Q-0003-8.md) | O `N` declarado antes não fecha com uma estratégia que retenta                    | ADR-0003 | Experiment                   | `pendente`             |
| [`Q-0004-2`](Q-0004-2.md) | Nada obriga o passo a reportar a chave de contenção                               | ADR-0004 | arquitetura mínima e guardas | `pendente`             |
| [`Q-0004-3`](Q-0004-3.md) | Comparar janelas exige um instante comparável entre workers                       | ADR-0004 | o log de observações         | `pendente`             |
| [`Q-0004-4`](Q-0004-4.md) | A regra de parada colide com a exigência de nascer entregando                     | ADR-0004 | entrega contínua no homelab  | `pendente`             |
| [`Q-0004-5`](Q-0004-5.md) | O terceiro formato de veredito precisa caber ao lado dos dois já previstos        | ADR-0004 | os dois formatos de veredito | `pendente`             |
| [`Q-0004-8`](Q-0004-8.md) | O limite `3/N` pressupõe ensaios independentes                                    | ADR-0004 | os dois formatos de veredito | `pendente`             |
| [`Q-0005-1`](Q-0005-1.md) | O critério de "falha não recuperada pela estratégia" não está definido            | ADR-0005 | estratégias de concorrência  | resolvida por ADR-0006 |
