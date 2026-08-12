# Feature Card — Observação passo a passo de uma operação

Estado: `especificado, não implementado` · Origem: [
`ADR-0001`](../../adr/0001-o-passo-como-unidade-de-execucao.md), `Aceito`

## Problema e resultado esperado

Um método Java comum não tem fronteira observável entre a leitura e a escrita. Sem ela,
três exigências ficam sem mecanismo: pausar um worker entre `READ` e `WRITE`, falhar num
ponto nomeado como `AFTER_COMMIT`, e emitir um registro por passo para a timeline.

Resultado esperado: o runtime para, falha e observa **entre** dois passos consecutivos,
sem que o código da operação saiba disso.

## Atores e gatilho

Quem declara a operação escreve a sequência de passos. O runtime a constrói e a executa.
Escalonador e injetor de falha são consultados em cada fronteira. Gatilho: o runtime
inicia uma tentativa.

```mermaid
sequenceDiagram
    participant RT as runtime (lab-plane)
    participant ES as escalonador
    participant FI as injetor de falha
    participant PS as passo (system-under-test)
    participant BUF as buffer em memória
    participant RB as RabbitMQ
    participant LJ as lab-journal
    Note over RT: fronteira = rótulo, lado (entrada ou saída)<br/>e seletor de tentativa
    RT ->> ES: consulta a fronteira
    ES -->> RT: libera ou retém
    RT ->> FI: consulta a mesma fronteira
    FI -->> RT: injeta ou não
    RT ->> BUF: enfileira a observação, com o número da tentativa
    Note over BUF: cheio, o buffer bloqueia o worker,<br/>e o bloqueio vira observação
    BUF ->> RB: thread separada publica, fora da janela medida
    RB ->> LJ: consome, persiste e só então emite
    RT ->> PS: chama o passo, por rede
    PS -->> RT: retorno opaco
    Note over RT, PS: o passo nunca chama o runtime
```

## Escopo

A operação como sequência ordenada e finita de passos nomeados. O endereço canônico de
uma fronteira. A ordem das duas consultas nela. A emissão de observações. O escopo
transacional por `TransactionTemplate`. O eixo de resolução. A prova de equivalência.

## Fora de escopo

A linguagem do agendamento está em
[`ADR-0003`](../../adr/0003-a-linguagem-do-agendamento.md), `Aceito`, e a forma do
escalonador em [`ADR-0005`](../../adr/0005-a-forma-do-escalonador.md), `Aceito`. O
contrato de retentativa está em
[`ADR-0006`](../../adr/0006-a-forma-da-estrategia-de-concorrencia.md#decisão), `Aceito`,
e quantas vezes uma estratégia retenta segue em
[`Q-0003-8`](../../questions/Q-0003-8.md). O formato interno da injeção de falha não tem
decisão registrada, e este card não o decide.

## Regras de negócio

| #   | Regra                                                                                                                                                                                                     | Evidência                                                                                                                                                                                                                                                                   | Aprovada por |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| R1  | O runtime chama o passo. O passo **NÃO DEVE** chamar o runtime.                                                                                                                                           | [ADR-0001, Decisão](../../adr/0001-o-passo-como-unidade-de-execucao.md#decisão)                                                                                                                                                                                             | pendente     |
| R2  | Cada passo carrega rótulo único na operação, tipo de conjunto fechado (`READ`, `COMPUTE`, `WRITE`) e corpo opaco. O runtime **NÃO DEVE** gerar, interpretar ou analisar o SQL.                            | [ADR-0001, Decisão](../../adr/0001-o-passo-como-unidade-de-execucao.md#decisão)                                                                                                                                                                                             | pendente     |
| R3  | O endereço de uma fronteira é a tripla (rótulo, entrada\|saída, seletor de tentativa). O seletor **NÃO DEVE** ter valor padrão.                                                                           | [ADR-0001, A fronteira](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-fronteira)                                                                                                                                                                                     | pendente     |
| R4  | A plataforma **DEVE** recusar endereço que não resolva para passo nenhum, e **DEVE** recusar nome abreviado quando o tipo aparecer mais de uma vez.                                                       | [ADR-0001, A fronteira](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-fronteira)                                                                                                                                                                                     | pendente     |
| R5  | Em cada fronteira o runtime consulta o escalonador **e depois** o injetor de falha, nesta ordem.                                                                                                          | [ADR-0001, A fronteira](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-fronteira)                                                                                                                                                                                     | pendente     |
| R6  | Uma definição de operação **NÃO DEVE** guardar estado mutável. Um teste executável **DEVE** rejeitar campo não final, campo de tipo mutável e `static` mutável.                                           | [ADR-0001, A definição de operação é uma fábrica](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-definição-de-operação-é-uma-fábrica-e-o-runtime-é-dono-do-ciclo-de-vida)                                                                                             | pendente     |
| R7  | O escopo de execução carrega worker e tentativa. O runtime **DEVE** rejeitar acesso vindo de outro worker, nomeando o passo.                                                                              | [ADR-0001, A definição de operação é uma fábrica](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-definição-de-operação-é-uma-fábrica-e-o-runtime-é-dono-do-ciclo-de-vida)                                                                                             | pendente     |
| R8  | Toda observação **DEVE** carregar o número da tentativa.                                                                                                                                                  | [ADR-0001, A observação](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-observação)                                                                                                                                                                                   | pendente     |
| R9  | `COMMIT` é o retorno do callback do `TransactionTemplate`, não um passo. `AFTER_COMMIT` é a primeira fronteira depois do escopo.                                                                          | [ADR-0001, A transação é demarcada através do Spring](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-transação-é-demarcada-através-do-spring-não-no-lugar-dele)                                                                                                       | pendente     |
| R10 | Um teste executável **DEVE** provar que as duas resoluções emitem o mesmo traço de SQL numa execução sem concorrência. Sem esse teste, a cláusula de honestidade **NÃO DEVE** ser considerada satisfeita. | [ADR-0001, A equivalência entre as duas resoluções](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-equivalência-entre-as-duas-resoluções-é-provada-por-teste)                                                                                                         | pendente     |
| R11 | Toda anomalia reproduzida com barreiras **DEVE** aparecer também sem barreiras, sob carga alta.                                                                                                           | [ADR-0001, A cláusula de honestidade](../../adr/0001-o-passo-como-unidade-de-execucao.md#a-cláusula-de-honestidade)                                                                                                                                                         | pendente     |
| R12 | As observações **DEVEM** atravessar para o `lab-journal` ao vivo, evento por evento, pelo broker que o ADR-0012 introduziu. O Lab Plane **NÃO DEVE** acumulá-las para enviar ao fim da execução.          | [ADR-0010, Decisão](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão); [ADR-0014, O evento sai do passo pelo broker](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#o-evento-sai-do-passo-pelo-broker) | pendente     |

O critério de igualdade entre dois traços foi fixado depois, pelo
[`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#o-critério-de-igualdade-entre-dois-traços-de-sql).

## Integrações e contratos afetados

Um passo emite SQL real contra o PostgreSQL, numa transação real. **Não há contrato
formalizado**, e `esquemas.md` não é um — ele é dono da forma, e diz isso de si mesmo. A
forma de `resource` e `allocation` vive
[lá](../../architecture/esquemas.md#o-schema-do-sistema-medido-sut), e a migração que a
aplica ainda não foi escrita — ver `Q-INT-5` em
[`integrations.md`](../../architecture/integrations.md#perguntas-em-aberto).

**Cada observação é enfileirada num buffer em memória no instante em que nasce, e uma
thread separada a publica no broker do**
[`ADR-0012`](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md),
mecanismo fixado pelo
[`ADR-0014`](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#o-runtime-publica-por-um-buffer-em-memória-numa-thread-separada).
Se o buffer encher, o worker bloqueia e o próprio bloqueio vira observação no log — é o
enfileiramento, e não a travessia de rede, que permanece na janela medida. O
`lab-journal` é serviço próprio, com schema próprio, e o Lab Plane não escreve no schema
dele por acesso direto. **Nenhum contrato formaliza essa travessia** — a forma concreta
do registro persistido é pergunta em aberto do
[`ADR-0016`](../../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md#negativas),
que é quem decide o que o `lab-journal` grava.

## Riscos e decisões pendentes

| Questão                                                  | O que está em jogo                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`Q-0001-1`](../../questions/Q-0001-1.md)                | o corpo de um passo muda com o rótulo intacto, e o replay mede outra operação em silêncio; quatro candidatas de mecanismo, nenhuma escolhida                                                                                                                                                                                                                                                                                   |
| [`Q-0002-1`](../../questions/Q-0002-1.md)                | "relógio injetável" e "aleatoriedade semeada" são texto, não regra executável; uma chamada a `Instant.now()` faz R10 reprovar um par correto, de forma intermitente                                                                                                                                                                                                                                                            |
| [`Q-0004-2`](../../questions/Q-0004-2.md)                | nada obriga um passo a reportar a chave de contenção                                                                                                                                                                                                                                                                                                                                                                           |
| o buffer assíncrono tira a emissão do caminho bloqueante | o [`ADR-0014`](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#o-runtime-publica-por-um-buffer-em-memória-numa-thread-separada) fixa o mecanismo: o worker só bloqueia quando o buffer enche, e o bloqueio vira observação; fora disso, o broker PODE duplicar, reordenar ou perder mensagem sem LSN para deduplicar                                                                     |
| [`Q-0004-3`](../../questions/Q-0004-3.md), a contagem    | se a contagem de coincidências do ADR-0004 ler este log e uma observação se perder em trânsito, a contagem cai a zero e produz `protegido` sobre banco violado — [`ADR-0014`](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#negativas) registra a lacuna e não a fecha                                                                                                                 |
| [`Q-0004-3`](../../questions/Q-0004-3.md), o instante    | o instante de ocorrência e a monotonicidade dele seguem sem decisão — [`ADR-0016`](../../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md#negativas) tira o relógio da **ordem** do log, e não do registro de cada evento                                                                                                                                                                                              |
| a capacidade do buffer em memória                        | não foi fixada — [`ADR-0014`](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#negativas) registra a lacuna, e ela decide com que frequência um worker bloqueia sob carga alta                                                                                                                                                                                                            |
| o tipo do evento de bloqueio do buffer                   | o diagrama de "Atores e gatilho" mostra o bloqueio virando observação, mas o conjunto de tipos do log é fechado em quatro valores e nenhum deles nomeia este bloqueio — [`ADR-0014`](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md#negativas) registra a lacuna, aberta na linha [`E-61`](../../adr/fila-de-decisoes.md#e-61--que-tipo-o-evento-de-bloqueio-de-buffer-carrega) da fila |

## Critérios de pronto

R1 a R12 verificadas por teste. R4, R6 e R7 produzem recusa que nomeia o culpado — o
endereço, o campo ou o passo. A prova de R10 existe para `increment` e para `allocate`.

## Links

- [Example Mapping](example-mapping.md) · [Cenários BDD](behavior.feature)
- [`ADR-0001`](../../adr/0001-o-passo-como-unidade-de-execucao.md) — a decisão e as seis
  alternativas descartadas
- [`plano-do-laboratorio.md`, seção 2](../../plano-do-laboratorio.md#2-a-abstração-central-uma-operação-é-uma-sequência-de-passos-nomeados)
