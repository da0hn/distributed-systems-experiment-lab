# Proposta 3 — O livro-razão do veredito

Um veredito cujo insumo viveu só em memória é alegação, e não evidência: nesta aposta,
tudo que entra na produção dele vira linha durável no schema `lab_plane`, apensável e
nunca reescrita, e o veredito é materializado ao lado da extensão exata do livro-razão de
onde saiu — o que ela otimiza é auditabilidade e sobrevivência a queda, inclusive à queda
proposital que a etapa 6 provoca no próprio instrumento.

Isto é proposta, e não decisão. O dono da forma vigente continua sendo
[`schemas/lab-plane.md`](../../../architecture/schemas/lab-plane.md#o-schema-do-instrumento-lab_plane).

## O problema que este modelo resolve

O schema está vazio, e a única tabela decidida para ele segue sem forma escolhida
([`schemas/README.md`](../../../architecture/schemas/README.md#o-que-muda-esta-pasta)).
Enquanto isso, todo insumo do veredito viveria só em memória: `commits`, coincidências,
descartes e a soma do predicado. Um reinício no meio da execução os apaga sem sinal, e a
etapa 6 mata o `lab-plane` de propósito
([ADR-0017](../../../adr/0017-a-persistencia-antecipada-do-log-de-observacoes-e-o-buffer-que-a-alimenta.md#contexto)).
A guarda de contiguidade de LSN que o oráculo DEVE cumprir antes de somar
([ADR-0013](../../../adr/0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md#decisão))
agrava o caso: ela é prova sobre um stream que ninguém guardou, logo presumida em vez de
provada. Aqui cada insumo é linha que permanece, e cada contagem é projeção dela.

## O modelo

Dez tabelas, todas em `lab_plane`. Nenhuma chave estrangeira atravessa schema, e nenhum
outro schema entra neste canvas. Os identificadores vão em inglês
([ADR-0008](../../../adr/0008-os-dois-planos-em-processos-separados.md#decisão)).

![O livro-razão do veredito](diagramas/proposta-3-livro-razao-do-veredito-1.excalidraw.svg)

## O que o diagrama não expressa

- **Ordem da chave composta.** O discriminador vem sempre primeiro — `(execution_id,
  ordinal)` e `(execution_id, lsn)` —, pelo mesmo motivo do lado medido: o prefixo de
  instante do UUIDv7 põe toda inserção no fim da B-tree, e toda leitura do livro-razão é
  por execução.
- **Índice.** `erDiagram` não expressa nenhum, e dois são aditivos: `(execution_id,
  kind)` sobre `boundary_record`, porque `commits` conta um `kind` só entre dez; e
  `(processing_execution_id, classification)` sobre `discarded_event`, porque o relatório
  separa higiene de invalidação.
- **Ausência de `DEFAULT`.** Nenhuma coluna tem. Todo instante vem do adaptador de
  relógio, e `execution_id` vem da aplicação, e não de `gen_random_uuid()`: o mesmo valor
  precisa ser escrito como `partition_id` do outro lado da fronteira, e um default deste
  schema não alcança o outro.
- **Ausência de trigger.** Nenhuma linha do livro-razão é atualizada, então um trigger de
  `updated_at` não teria o que atualizar. As duas materializações nascem uma vez, depois
  do fim da execução.
- **Ausência de chave estrangeira.** `run.serves_execution_id` e
  `boundary_record.fault_point_ordinal` referenciam sem constraint, e a órfã é verificada
  em vez de impedida. O motivo aqui não é o lock na janela medida, porque o livro-razão
  escreve fora dela: é ordem de chegada. Um evento de CDC PODE chegar depois de a
  execução deixar a lista de ativas, e uma constraint recusaria exatamente a linha que
  prova a higiene.

## Decisões assumidas

| O que assumi                                                                                           | Alternativa que ficou de fora                                  | O que muda se a pessoa decidir o contrário                                                                                                                     |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `execution_id` é UUIDv7 atribuído pela aplicação                                                       | `gen_random_uuid()` no banco, ou derivar da semente            | com geração no banco, o valor não alcança `sut.partition_id` e o consumidor perde o que traduzir; derivado da semente, duas execuções da mesma semente colidem |
| a lista de execuções ativas é projeção de `run` mais `run_lifecycle_event`                             | uma coluna `status` em `run`, atualizada a cada transição      | com `status`, a linha passa a ser reescrita, o livro-razão deixa de ser apensável, e a saída da lista some do registro                                         |
| o livro-razão guarda só a fronteira que entra no veredito                                              | persistir aqui as 900 a 1500 observações da execução           | vira segunda cópia integral do log, torna o `lab-journal` redundante e dobra o I/O que o ADR-0017 já admite                                                    |
| o persistidor drena o **mesmo** buffer em memória do ADR-0017                                          | buffer próprio, ou escrita síncrona dentro do passo            | a escrita síncrona põe I/O na janela medida; um segundo buffer dobra o que uma queda perde e faz o runtime enfileirar duas vezes                               |
| a contiguidade é provada por encadeamento, em `cdc_event.preceding_lsn`                                | aritmética sobre o LSN, ou confiança no transporte             | o LSN é deslocamento em bytes, e não sucessor; sem elo, um buraco fica indistinguível de um evento grande                                                      |
| `verdict` guarda a extensão do livro-razão que ele leu                                                 | guardar só o número do veredito                                | sem a extensão, a re-derivação não sabe se leu mais ou menos que a original, e a conferência não conclui nada                                                  |
| coincidência é projeção de `WINDOW_OPENED`/`WINDOW_CLOSED`, sem tabela de pares                        | materializar os pares coincidentes                             | o número de pares é quadrático no número de tentativas, e ele é recomputável; materializar troca prova por espaço                                              |
| o reinício apensa `LEDGER_RESUMED` a toda execução que ainda estava ativa                              | reconstruir a lista em silêncio                                | sem a marca, o buraco deixado pelo buffer perdido fica invisível, e vira o falso negativo silencioso que o repositório recusa                                  |
| o ordinal é atribuído pelo escritor, em memória                                                        | `bigserial`, ou `nextval` no `DEFAULT`                         | `nextval` é valor gerado pelo banco, e o ordinal entra na prova de completude que sustenta o veredito                                                          |
| `run` carrega o nível de isolamento e a estratégia da **própria** execução                             | um nível e uma estratégia por experimento                      | um nível por experimento não representa o controle negativo rodando sob nível diferente do medido                                                              |
| `experiment_ref` é referência opaca, sem forma e sem constraint                                        | modelar a definição de experimento aqui                        | onde a definição vive não está decidido; se ela vier para cá, `run` deixa de ser a declaração e vira a definição                                               |
| os tipos SQL do instrumento são `uuid`, `bigint`, `int`, `text`, `numeric`, `boolean` e `timestamptz`  | qualquer outro conjunto, `numeric` para contagem inclusive     | nenhum tipo deste lado foi decidido; trocar o conjunto muda o `erDiagram` e nada mais deste desenho                                                            |
| `discarded_event` guarda uma linha por descarte, e não um contador                                     | um contador por classificação, incrementado                    | o contador reescreve linha e perde o `lsn` de cada descarte, que é o que permite auditar uma invalidação depois                                                |

## Trade-offs

- Ganha-se **veredito re-derivável e contiguidade provada**; custa-se **I/O do
  instrumento no mesmo PostgreSQL do sistema medido**, a perturbação que o ADR-0017 já
  nomeia nas
  [negativas](../../../adr/0017-a-persistencia-antecipada-do-log-de-observacoes-e-o-buffer-que-a-alimenta.md#negativas).
- Ganha-se **a lista de execuções ativas sobrevivendo ao reinício**; custa-se **uma
  projeção a manter no caminho de todo evento de CDC**, que só a réplica única do
  [ADR-0012](../../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)
  permite guardar em memória.
- Ganha-se **o evento auditável, com o discriminador como chegou ao lado do traduzido**,
  na tradução de ponto único do
  [ADR-0015](../../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#o-nome-assimétrico-do-discriminador-e-a-tradução-num-ponto-único);
  custa-se **uma sombra dos dados do sistema medido dentro do schema do instrumento**.
- Ganha-se **nenhuma linha reescrita**; custa-se **o livro-razão crescer por tentativa, e
  nada aqui decidir quando ele é podado**.

## O que esta proposta NÃO decide

A forma do `lab_journal`, nem onde a definição de experimento vive. O formato do
relatório, nem como os formatos de veredito convivem nele. A capacidade do buffer e a
vazão da thread de publicação, que o
[ADR-0017](../../../adr/0017-a-persistencia-antecipada-do-log-de-observacoes-e-o-buffer-que-a-alimenta.md#negativas)
deixa sem número e este desenho herda. O tipo do evento de bloqueio no conjunto fechado
do [ADR-0007](../../../adr/0007-o-log-de-observacoes-forma-ordem-e-onde-vive.md#a-forma-de-um-evento):
`BUFFER_BLOCKED` é `kind` deste livro-razão, e não tipo daquele conjunto. Quando o
livro-razão é podado, e por quem. Nenhuma migração nasce desta proposta.

## Perguntas que ela levanta

**A colisão com regra aprovada por pessoa, e ela é dupla.** A `R6` de
[distinção entre higiene e invalidação](../../../features/distincao-entre-higiene-e-invalidacao/feature-card.md#regras-de-negócio)
diz que a tabela de execuções ativas NÃO DEVE registrar o que uma execução mediu. Este
desenho mantém a letra: `run` e `run_lifecycle_event` não carregam medida nenhuma, e toda
medida vive em tabelas separadas. Ele colide com o motivo que a própria regra invoca — o
[ADR-0011](../../../adr/0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#histórico-de-execução-dentro-do-lab-plane)
descartou histórico de execução dentro do `lab-plane`, e um livro-razão do veredito é
histórico de execução dentro do `lab-plane`. Não resolvo nenhuma das duas.

**A proveniência sobrevive à transcrição?** O
[ADR-0013](../../../adr/0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md#decisão)
fixou que a proibição alcança fonte produzida pelo instrumento, e que o WAL não é uma
delas. `cdc_event` é cópia do WAL escrita pelo instrumento. Se o oráculo somar dali, ele
soma de uma tabela que o instrumento escreveu, e nenhum documento diz se a proveniência
do WAL sobrevive à transcrição.

**O elo de contiguidade existe?** `preceding_lsn` pressupõe que o conector exponha o LSN
do evento imediatamente anterior. As
[negativas do ADR-0012](../../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#negativas)
registram que nem a sobrevivência do próprio LSN ao transporte foi provada por teste. Se
o elo não existir, a coluna não é escrevível como desenhada.
