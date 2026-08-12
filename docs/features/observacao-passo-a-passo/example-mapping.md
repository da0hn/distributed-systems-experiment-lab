# Example Mapping — Observação passo a passo

Companheiro de [`feature-card.md`](feature-card.md). As regras vêm do
[`ADR-0001`](../../adr/0001-o-passo-como-unidade-de-execucao.md), `Aceito`.

## História

> Como quem monta um experimento, preciso que o runtime pare, falhe e observe **entre**
> dois passos de uma operação, para que a intercalação e a falha sejam endereçáveis por
> nome em vez de dependerem do escalonador do sistema operacional.

## Regras e exemplos

### R1 — O runtime chama o passo; o passo não chama o runtime

- **Exemplo 1.1** — O corpo de `select-resource` executa `SELECT` e devolve os fatos
  `version=1` e `rowsAffected=1`. Ele não sabe que existe uma fronteira depois dele.
- **Contraexemplo 1.2** — Um corpo de passo que chame o escalonador para se bloquear é
  system under test invadindo o Lab Plane, e invalida a medida. A separação precisa ser
  imposta por teste, porque os dois planos vivem na mesma JVM.

### R3 e R4 — O endereço de uma fronteira

- **Exemplo 3.1** — `("select-resource", saída, tentativa 1)` resolve para a fronteira de
  saída do passo rotulado `select-resource`, na primeira tentativa.
- **Exemplo 4.1, borda** — `AFTER_READ` é aceito quando a operação tem **um** passo de
  tipo `READ`. Numa operação com dois, a plataforma recusa em vez de escolher um deles.
- **Exemplo 4.2, erro** — `AFTER_READ` sem seletor de tentativa é recusado em qualquer
  operação que possa tentar mais de uma vez. Não há valor padrão.
- **Exemplo 4.3, erro** — Um endereço que cite `select-resurce` (rótulo com erro de
  digitação) é recusado antes de qualquer execução. A parada é ruidosa por decisão.
- **Exemplo 4.4, o buraco conhecido** — Renomear `select-resource` e atribuir esse mesmo
  rótulo a **outro** passo faz o endereço resolver para o passo errado, sem erro nenhum.
  É [`Q-0001-1`](../../questions/Q-0001-1.md), e nenhum mecanismo o cobre hoje.

### R5 — A ordem das duas consultas na fronteira

- **Exemplo 5.1** — Uma fronteira com barreira e falha declaradas bloqueia o worker
  primeiro e falha depois de liberá-lo.
- **Exemplo 5.2, por que a ordem importa** — Na ordem inversa, um worker que precisasse
  chegar à barreira morreria antes, e os outros esperariam por alguém que nunca chega.
- **Exemplo 5.3, o inverso não está resolvido** — Um worker que falha na saída do passo
  N nunca chega à entrada do passo N+1. Um escalonador que o espere trava a execução
  inteira. É [`Q-0001-4`](../../questions/Q-0001-4.md), encaminhada à decisão da forma
  do escalonador.

### R6 e R7 — O escopo pertence a um worker e a uma tentativa

- **Exemplo 6.1** — Um campo `private Map<String, Object> cache` numa definição de
  operação é rejeitado pela análise estática, antes de qualquer execução.
- **Exemplo 7.1, concorrência** — O worker 2 tenta ler o escopo criado pelo worker 1. O
  runtime rejeita e a mensagem nomeia o passo em que ocorreu.
- **Contraexemplo 7.2, a lacuna** — Um repositório injetado que guarde um `Map` como
  cache passa pelas três camadas: a definição não tem estado mutável, a análise fica
  verde, e o escopo continua íntegro. Os workers compartilham por ele assim mesmo, e o
  laboratório produz atualizações perdidas dentro do próprio instrumento. É
  [`Q-0001-2`](../../questions/Q-0001-2.md).

### R9 — O commit não é um passo

- **Exemplo 9.1** — `BEFORE_COMMIT` é a última fronteira dentro do escopo transacional;
  `AFTER_COMMIT` é a primeira depois dele.
- **Exemplo 9.2, consistência** — Uma falha injetada em `AFTER_COMMIT` acontece com a
  transação já aplicada. É esse par — commit aplicado, operação reportando falha — que a
  etapa 6 estuda, e é por isso que o oráculo do ADR-0002 conta `commits` e não `sucessos`.

### R10 — A prova de equivalência entre resoluções

- **Exemplo 10.1** — `increment` em alta resolução emite `SELECT` e `UPDATE`. O mesmo
  `increment` como método `@Transactional` emite os dois statements, na mesma ordem, com
  os mesmos valores ligados. Os traços são iguais e a cláusula de honestidade fica
  liberada para aquela operação.
- **Exemplo 10.2, erro** — Os dois braços divergem na posição 2. O CI falha nomeando a
  operação e a posição.
- **Exemplo 10.3, borda** — Um traço com os mesmos statements em **ordem diferente** é
  diferente. A comparação é por sequência, não por conjunto.
- **Exemplo 10.4, cobertura** — Para `allocate`, o conjunto de entradas amostradas tem
  três ramos: a alocação cabe, atinge a capacidade exata, e excede.
- **Exemplo 10.5, o que a prova não vê** — Trocar `value + 1` por `value + 2` no passo
  `COMPUTE` não altera statement nenhum quando o parâmetro entra como marcador. Num
  laboratório de contadores, o `COMPUTE` **é** a lógica.

### R11 — A cláusula de honestidade

- **Exemplo 11.1** — Uma atualização perdida produzida com barreiras aparece também sob
  carga alta, sem barreiras. O experimento vale.
- **Exemplo 11.2, o que ela pega** — Uma anomalia que apareça só com barreiras indica que
  o runtime fabricou o fenômeno.
- **Nota** — O [`ADR-0004`](../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md)
  subsumiu esta regra: a execução medida roda sem agendamento, e a cláusula fica
  atendida por construção. R11 continua valendo com o alcance que o ADR-0004 lhe deu.

## Perguntas em aberto

| #   | Pergunta                                                                                                                                                                                         | Origem                                                                                                                                                                                                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P1  | Como o replay sabe que o **corpo** de um passo mudou, com o rótulo intacto?                                                                                                                      | [`Q-0001-1`](../../questions/Q-0001-1.md)                                                                                                                                                                |
| P2  | Um rótulo reciclado faz o endereço resolver para o passo errado, em silêncio. Quem impede?                                                                                                       | [`Q-0001-1`](../../questions/Q-0001-1.md)                                                                                                                                                                |
| P3  | O que impede um colaborador injetado de compartilhar estado entre workers?                                                                                                                       | [`Q-0001-2`](../../questions/Q-0001-2.md)                                                                                                                                                                |
| P4  | Como um worker que morreu notifica o escalonador?                                                                                                                                                | [`Q-0001-4`](../../questions/Q-0001-4.md)                                                                                                                                                                |
| P5  | "Relógio injetável" e "aleatoriedade semeada" viram regra executável como?                                                                                                                       | [`Q-0002-1`](../../questions/Q-0002-1.md)                                                                                                                                                                |
| P6  | O que obriga um passo a reportar a chave de contenção?                                                                                                                                           | [`Q-0004-2`](../../questions/Q-0004-2.md)                                                                                                                                                                |
| P7  | O tipo de passo é conjunto fechado. Acrescentar `PUBLISH` na etapa 5 muda o quê?                                                                                                                 | nova, 2026-08-01                                                                                                                                                                                         |
| P8  | Qual é o comportamento quando dois passos declaram o mesmo rótulo? R2 exige unicidade e nenhum documento diz o que acontece quando ela é violada.                                                | nova, 2026-08-01                                                                                                                                                                                         |
| P9  | Qual é a capacidade do buffer em memória que o runtime usa para publicar a observação de forma assíncrona? Ela decide com que frequência um worker bloqueia sob carga alta, e nenhum ADR a fixa. | [ADR-0014](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#negativas)                                                                                              |
| P10 | Que tipo o evento de bloqueio do buffer carrega? O conjunto de tipos do log é fechado em quatro valores, e nenhum deles nomeia este bloqueio.                                                    | [ADR-0014](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#negativas), [E-61](../../adr/fila-de-decisoes.md#e-61--que-tipo-o-evento-de-bloqueio-de-buffer-carrega) |

## Adiado de propósito

| Item                                | Gatilho que o retoma                                |
|-------------------------------------|-----------------------------------------------------|
| Formato interno da injeção de falha | a etapa 6, quando `BEFORE_PUBLISH` precisar existir |
| Tipos `PUBLISH`, `CONSUME`, `ACK`   | a etapa 5, quando a operação virar mensagem         |

**Dois itens saíram desta tabela em 2026-08-06, retomados antes do gatilho previsto.**

*Onde o log de observações é persistido* aguardava um experimento que derrubasse o
processo. Foi retomado antes por outro caminho: o `lab-journal` nasceu como serviço
próprio, com schema próprio, e as observações atravessam para ele ao vivo — R12 do
[Feature Card](feature-card.md).

*Mecanismo de streaming para a UI* aguardava a primeira execução longa demais para
polling. Foi retomado junto: o frontend lê histórico e streaming do `lab-journal`, e não
do Lab Plane.

## O que não virou cenário, e por quê

R2 (rótulo único, tipo fechado, corpo opaco) é estrutural: ela descreve a forma de uma
definição, e a violação é pega por P8, que ainda não tem resposta.

R8 (toda observação carrega a tentativa) vira asserção dentro de outros cenários, não um
cenário próprio — um cenário que só verifique a presença de um campo testa estrutura,
não comportamento.
