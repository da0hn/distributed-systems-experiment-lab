# Feature Card — Distinção entre higiene e invalidação

Estado: `especificado, não implementado` · Origem:
[`ADR-0012`](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md),
`Aceito`

Cobre o consumidor do broker do `lab-plane`, comum aos dois oráculos já especificados
([ADR-0013, Decisão](../../adr/0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md#decisão)).

## Problema e resultado esperado

O `lab-plane` consome eventos de CDC pelo broker que o
[ADR-0012](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)
instala no caminho do veredito. O transporte PODE duplicar, reordenar ou perder mensagem,
e a mesma instância é a peça que o grupo B sabota de propósito
([ADR-0012, Negativas](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#negativas)).
Um evento PODE chegar fora de ordem, atrasado, ou depois de a execução que o produziu já
ter terminado.

O consumidor responde, para cada evento que descarta: ele invalida o veredito de uma
execução em curso, ou é resíduo inofensivo de janela já fechada? A resposta depende de
saber quais execuções estão ativas — sem essa lista, um descarte silencioso PODE esconder
corrupção real. A distinção só se sustenta se um `lab-plane` souber quais execuções
estão ativas, e com duas réplicas uma delas não sabe: é por isso que a réplica única
deixou de ser preferência e virou condição do veredito confiável.

```mermaid
flowchart TD
    EV["evento chega ao<br/>consumidor do broker"] --> R{"discriminador de execução<br/>reconhecido como ativo?"}
    R -->|" sim, e pertence à<br/>execução em curso "| OK["processado normalmente"]
    R -->|" não, mas consta<br/>como ativo na tabela "| INV["invalidação:<br/>a execução é corrompida"]
    R -->|" não, e a execução<br/>já está encerrada "| HIG["higiene:<br/>descarte silencioso"]
    INV --> CNT["contado no relatório"]
    HIG --> CNT
```

## Atores e gatilho

- O **consumidor do broker**, dentro do `lab-plane`, que filtra por execução
  ([ADR-0012, Decisão](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)).
- A **tabela de execuções ativas**, primeira tabela do schema `lab_plane`, hoje vazio de
  propósito. A lista vive em tabela, e não em memória, porque todo deploy é ele próprio
  um reinício do processo: em memória a resposta some no reinício, e a execução seguinte
  passa a descartar às cegas.

Gatilho: o consumidor descarta um evento cujo discriminador de execução não corresponde
à execução que ele processa agora.

## Escopo

- Classificar cada evento descartado em dois casos: higiene (execução encerrada) ou
  invalidação (execução ativa e não reconhecida).
- A consulta à tabela de execuções ativas que sustenta a classificação.
- A contagem de todo evento descartado, qualquer que seja o caso.
- A distinção vale para os dois oráculos já especificados — o WAL é fonte legítima para
  os dois
  ([ADR-0013, Decisão](../../adr/0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md#decisão)).

## Fora de escopo

- A forma da tabela de execuções ativas — colunas, chave e migração. `Pergunta em
  aberto`: a escolha de guardar a lista em tabela não fixou coluna nenhuma.
- O valor do limite de espera de R7, o escopo dele (por execução ou global), e a
  distinção entre cancelamento e abandono no registro. `Pergunta em aberto`: um número
  escrito aqui seria decisão que ninguém tomou, e o cancelamento e o abandono tiram a
  linha da lista sem que se tenha decidido se o registro guarda por qual dos dois.
- A réplica única como garantia formal de entrega — o `DEVE` mudou de lugar e vira
  critério de aceite da issue #2 do homelab
  ([ADR-0019](../../adr/0019-a-entrega-sai-do-deploy-e-a-imagem-ganha-tag-semantica.md#a-réplica-única-do-lab-plane-passa-a-ser-critério-de-aceite-na-issue-2)).
- A contiguidade de LSN e o reconhecimento da marca de fim do oráculo do predicado —
  `R8`/`R9` de
  [deteccao-de-protecao-inerte](../deteccao-de-protecao-inerte/feature-card.md#regras-de-negócio).
- O transporte do evento pelo broker, e a preservação do LSN —
  [ADR-0012](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md)
  e
  [ADR-0014](../../adr/0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md).

## Regras de negócio

| #  | Regra                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Evidência                                                                                                                                                                                                                          | Aprovada por          |
|----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| R1 | Um evento cujo discriminador de execução pertence a uma execução **ativa** e não reconhecida DEVE invalidar essa execução.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | [ADR-0012, Decisão](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)                                                                                                                         | pessoa, em 2026-08-12 |
| R2 | Um evento cujo discriminador de execução pertence a uma execução **encerrada** DEVE ser descartado em silêncio — higiene, sem invalidar veredito nenhum.                                                                                                                                                                                                                                                                                                                                                                                                                                                            | [ADR-0012, Decisão](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)                                                                                                                         | pessoa, em 2026-08-12 |
| R3 | O consumidor DEVE contar todo evento que descarta, tanto por higiene quanto por invalidação.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | [ADR-0012, Decisão](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)                                                                                                                         | pessoa, em 2026-08-12 |
| R4 | A lista de quais execuções estão ativas DEVE viver numa tabela do schema `lab_plane` — a primeira tabela daquele schema, hoje vazio de propósito.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Em memória, a lista some num reinício, e a execução seguinte descarta às cegas.                                                                                                                                                    | pessoa, em 2026-08-12 |
| R5 | O `lab-plane` DEVE rodar em réplica única, condição do veredito confiável: com duas réplicas, cada uma vê o backlog da outra, e nenhuma sabe dizer qual das duas causas produziu o descarte. O mecanismo exato continua `Pergunta em aberto`, dependente de qual sink do RabbitMQ recebe os eventos (Example Mapping, P6).                                                                                                                                                                                                                                                                                          | [ADR-0012, Decisão](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão), [ADR-0012, Consequências](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#consequências) | pessoa, em 2026-08-12 |
| R6 | A tabela de execuções ativas NÃO DEVE registrar o que uma execução mediu. Ela guarda só o estado corrente do filtro, e não é o histórico de execução que o ADR-0011 recusou manter aqui.                                                                                                                                                                                                                                                                                                                                                                                                                            | [ADR-0011, Histórico de execução dentro do `lab-plane`](../../adr/0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#histórico-de-execução-dentro-do-lab-plane)                                                | pessoa, em 2026-08-12 |
| R7 | Uma execução DEVE sair da lista de execuções ativas do `lab_plane` por exatamente três caminhos, e por nenhum outro: a sentinela de fim, que passa a remover a linha; o limite de espera, disparado pelo adaptador de relógio do `lab-plane`; ou o cancelamento explícito pela pessoa, no frontend. O limite de espera DEVE usar o adaptador de relógio injetável — a exceção dada a um limite que não entra em veredito NÃO é aplicada aqui, por assimetria de risco: aplicar a regra a um limite que não precisava custa um adaptador, e não aplicá-la a um que precisava quebra a reprodutibilidade em silêncio. | [AGENTS.md, regras estruturais](../../../AGENTS.md#regras-estruturais-que-valem-sempre)                                                                                                                                            | pessoa, em 2026-08-12 |

## Integrações e contratos afetados

O transporte do
[ADR-0012](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)
é compartilhado pelos dois oráculos. A tabela de execuções ativas é DDL de um único
serviço, e DDL NÃO É contrato
([specification-process.md, Contratos](../../specification-process.md#contratos--só-o-que-existe)):
a forma dela vai para
[`schemas/lab-plane.md`](../../architecture/schemas/lab-plane.md#o-schema-do-instrumento-lab_plane) quando a
pendência fechar, nunca neste card. Nenhum contrato OpenAPI ou AsyncAPI nasce daqui.

## Riscos e decisões pendentes

- `Pergunta em aberto`: a forma da tabela, e os detalhes de R7 — seguem no
  [Example Mapping](example-mapping.md#perguntas-em-aberto).
- A réplica única não tem garantia formal aqui — vira critério de aceite da issue #2 do
  `homelab-infrastructure`, não linha de fila (ver "Fora de escopo").

## Critérios de pronto

- R1 a R7 verificadas por teste.
- **R1 pela injeção**: evento com discriminador ativo e não reconhecido invalida a
  execução.
- **R2 pela retenção**: evento com discriminador encerrado é descartado, e o veredito já
  fechado permanece intacto.
- **R3 pela contagem**: todo descarte aparece no relatório, com o motivo — higiene ou
  invalidação.
- **R5 pela ausência de segunda réplica, condicionada ao fecho da issue #2** (ver "Fora
  de escopo"): até lá, nenhuma configuração sobe duas réplicas do `lab-plane`, e a
  garantia formal permanece `Pergunta em aberto`.

## Links

- [Example Mapping](example-mapping.md), com o diagrama de R7
- [ADR-0012](../../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md),
  `Aceito` — a distinção nasce na `## Decisão` dele
- [`deteccao-de-protecao-inerte`](../deteccao-de-protecao-inerte/feature-card.md) —
  mesmo consumidor
