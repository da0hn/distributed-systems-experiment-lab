# Capacidades

As capacidades do laboratório, especificadas por Feature Card e Example Mapping. Quais
`behavior.feature` são especificação viva, e qual segue inativo, é da subseção do
índice — este parágrafo não os reconta.

O processo está em [`../specification-process.md`](../specification-process.md).

## Índice

| Capacidade                                                                                           | O que ela responde                                                                             | Origem                                                                                                                                   | Regras                       | Estado                         |
|------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|--------------------------------|
| [observacao-passo-a-passo](observacao-passo-a-passo/feature-card.md)                                 | como parar, falhar e observar **entre** dois passos de uma operação                            | [`ADR-0001`](../adr/0001-o-passo-como-unidade-de-execucao.md), `Aceito`                                                                  | 12, todas aprovadas          | especificado, não implementado |
| [execucao-de-experimento](execucao-de-experimento/feature-card.md)                                   | o que um resultado zero significa, e quando ele é defeito do instrumento                       | [`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md), `Aceito`                                          | 17, 15 aprovadas, 2 pendente | especificado, não implementado |
| [deteccao-de-atualizacao-perdida](deteccao-de-atualizacao-perdida/feature-card.md)                   | quantos incrementos se perderam, e sob qual proteção — E1 e E3                                 | [`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`                                                               | 19, todas aprovadas          | especificado, não implementado |
| [deteccao-de-protecao-inerte](deteccao-de-protecao-inerte/feature-card.md)                           | por que uma proteção pode estar presente e não proteger nada — E5                              | [`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`                                                               | 11, todas aprovadas          | especificado, não implementado |
| [streaming-e-replay-do-log-de-observacoes](streaming-e-replay-do-log-de-observacoes/feature-card.md) | como a tela vê o histórico completo e o que acontece ao vivo, sem perder nem repetir evento    | [`ADR-0016`](../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md), `Aceito`                                                      | 7, todas aprovadas           | especificado, não implementado |
| [distincao-entre-higiene-e-invalidacao](distincao-entre-higiene-e-invalidacao/feature-card.md)       | se um evento atrasado do broker invalida o veredito, ou é resíduo inofensivo de janela fechada | [`ADR-0012`](../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md), `Aceito`                                       | 7, todas aprovadas           | especificado, não implementado |
| [comparacao-entre-niveis-de-isolamento](comparacao-entre-niveis-de-isolamento/feature-card.md)       | quais níveis de isolamento protegem a invariante do E5, e a que custo                          | [`E-87`, fecho](../adr/fila-de-decisoes.md#e-87-fecha-em-card-novo-para-a-comparação-entre-níveis-de-isolamento-escolhida-em-2026-08-12) | 3, todas pendente            | especificado, não implementado |

**Nenhuma capacidade está implementada, e isso não quer dizer que não haja código.** Há
um esqueleto executável: ele compila, empacota e sobe contra PostgreSQL, e **não tem
uma única regra de negócio dentro**. A árvore versionada é a prova do que existe; este
índice é o dono do que cada capacidade cobre, e a coluna `Regras` é a dona de quantas
regras cada uma tem.

**Setenta e uma regras foram aprovadas por pessoa**, todas em 2026-08-12 exceto a
`R19` de [deteccao-de-atualizacao-perdida](deteccao-de-atualizacao-perdida/feature-card.md#regras-de-negócio),
de 2026-08-06
([E-76, fecho](../adr/fila-de-decisoes.md#e-76-fecha-em-a-regra-desce-para-o-feature-card-escolhida-em-2026-08-12)).
Cinco cards têm a coluna `Regras` marcando `todas aprovadas`; a de
`execucao-de-experimento` passa a misturar aprovada e pendente, pelas `R16` e `R17`
que o [`ADR-0018`](../adr/0018-cada-controle-roda-sob-o-seu-proprio-nivel.md)
acrescentou — as quinze regras dela já aprovadas continuam contadas nas setenta e uma.

**O critério foi a procedência, e ele separou dois grupos.** Sessenta e sete regras
apenas transcrevem decisão que já vivia em ADR aceito, em fecho da fila ou em guardrail
da raiz — aprová-las confirmou a fidelidade da transcrição, sem redecidir o mérito. As
outras três não tinham dono a montante, e **cada uma exigiu que a pessoa decidisse
antes**, no mesmo dia:

| Regra                                              | O que faltava                                                                 | Onde foi decidido                                                                                                                   |
|----------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `R18` de `deteccao-de-atualizacao-perdida`         | de onde vem `value_inicial`, já que a única evidência era o arquivo congelado | [`E-86`](../adr/fila-de-decisoes.md#e-86-fecha-em-o-estado-inicial-é-escrito-com-a-captura-aberta-escolhida-em-2026-08-12)          |
| `R7` de `deteccao-de-protecao-inerte`              | onde vive o nível de isolamento, que o ADR-0002 recusa por escrito decidir    | [`E-87`](../adr/fila-de-decisoes.md#e-87-fecha-em-card-novo-para-a-comparação-entre-níveis-de-isolamento-escolhida-em-2026-08-12)   |
| `R4` de `streaming-e-replay-do-log-de-observacoes` | como o fim de uma execução chega ao `lab-journal` e ao frontend               | [`E-88`](../adr/fila-de-decisoes.md#e-88-fecha-em-evento-terminal-pelo-broker-e-o-stream-fecha-depois-dele-escolhida-em-2026-08-12) |

**O fecho de `E-87` também criou a capacidade
[comparacao-entre-niveis-de-isolamento](comparacao-entre-niveis-de-isolamento/feature-card.md)**,
com três regras, todas `pendente` — a primeira capacidade deste índice cujas regras
ainda não têm `Aprovada por` preenchido.

Aprova-se a **regra** e não o card, pela decisão `B-3`, de 2026-08-05. **A frase que
dizia que nenhuma regra aprovada tinha ganhado cenário deixou de valer em 2026-08-12**,
quando a comparação cenário a cenário foi feita — o que ela achou está na seção abaixo.
As três regras da comparação entre níveis seguem sem cenário, e por motivo próprio:
elas são `pendente`, e uma regra `pendente` NÃO DEVE virar cenário Gherkin
([`docs/AGENTS.md`](../AGENTS.md#feature-card)).

### Qual `behavior.feature` é especificação viva

Um `.feature` é especificação viva quando **cada** regra que ele cobre tem
`Aprovada por` preenchido, e o cabeçalho `ARQUIVO INATIVO` é o que declara o
contrário. A volta é **por arquivo**, e não regra a regra: uma regra aprovada entre
quatro não reativa nada. Aprovação parcial mantém o arquivo inativo e libera escrever
cenário apenas sobre a regra aprovada — são dois efeitos distintos, e confundi-los
reativa arquivo não conferido. O dono da regra é
[`../specification-process.md`](../specification-process.md#o-feature-inativo-e-como-ele-volta-ao-conjunto-ativo).

**A comparação cenário a cenário foi feita em 2026-08-12**, e três arquivos voltaram
ao conjunto ativo. Ela não foi cosmética: três cenários saíram, cada um com o motivo
escrito no Example Mapping da capacidade. Dois afirmavam comportamento que nenhuma
regra aprovada sustenta, e um afirmava DDL, que não é comportamento externo.

O `behavior.feature` de
[execucao-de-experimento](execucao-de-experimento/feature-card.md) segue inativo, e o
motivo agora é o da própria regra: as `R16` e `R17` que o
[`ADR-0018`](../adr/0018-cada-controle-roda-sob-o-seu-proprio-nivel.md) acrescentou
nasceram `pendente`.

## Os cards não são um por experimento

O MVP tem quatro experimentos, e a tabela acima tem mais cards do que isso — quantos, quem
diz é a tabela, e este parágrafo não a reconta. **Dois** deles cobrem um **oráculo**,
porque é o oráculo que define o comportamento observável, e os dois nascem do
[`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md):

- E1 e E3 compartilham o oráculo exato do contador. O E3 varia a estratégia sobre a mesma
  carga, e isso não muda o que é medido. Um card só —
  [deteccao-de-atualizacao-perdida](deteccao-de-atualizacao-perdida/feature-card.md).
- E5 tem um oráculo diferente — um predicado sobre um conjunto, não uma contagem. Card
  próprio, [deteccao-de-protecao-inerte](deteccao-de-protecao-inerte/feature-card.md).

**Os demais não cobrem oráculo nenhum**, e cada um tem outra origem, como a coluna
`Origem` da tabela mostra.
[observacao-passo-a-passo](observacao-passo-a-passo/feature-card.md) cobre o mecanismo de
parar, falhar e observar entre dois passos, pelo
[`ADR-0001`](../adr/0001-o-passo-como-unidade-de-execucao.md).
[execucao-de-experimento](execucao-de-experimento/feature-card.md) cobre o que um
resultado zero significa, pelo
[`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md) — e
o E2 vive dentro dele, porque aquele mesmo ADR
[o rebaixou](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-e2-deixa-de-ser-um-experimento-do-mvp)
a execução de controle positivo, e ele deixou de ser experimento.

O terceiro deles é
[streaming-e-replay-do-log-de-observacoes](streaming-e-replay-do-log-de-observacoes/feature-card.md),
que especifica o mecanismo pelo qual o `lab-journal` entrega o log de observações ao
frontend — histórico completo e apêndice ao vivo pelo mesmo `GET /stream` —, decidido
pelo [`ADR-0016`](../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md). É
comportamento do próprio instrumento, e não do sistema medido nem de um oráculo.

O quarto é
[distincao-entre-higiene-e-invalidacao](distincao-entre-higiene-e-invalidacao/feature-card.md),
que especifica como o consumidor do broker do `lab-plane` classifica um evento
descartado — higiene de janela fechada, ou invalidação de execução ainda ativa —,
decidido pelo
[`ADR-0012`](../adr/0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md).
Também é comportamento do instrumento, comum aos dois oráculos já especificados
([`ADR-0013`](../adr/0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md#decisão)).

O quinto é
[comparacao-entre-niveis-de-isolamento](comparacao-entre-niveis-de-isolamento/feature-card.md),
que também não cobre oráculo próprio: ele reusa o oráculo do experimento subjacente —
hoje, o predicado do E5 — e acrescenta o eixo do nível de isolamento ao relatório, pelo
fecho de
[`E-87`](../adr/fila-de-decisoes.md#e-87-fecha-em-card-novo-para-a-comparação-entre-níveis-de-isolamento-escolhida-em-2026-08-12).

## Capacidade conhecida e não especificada

**E4 — `optimistic-under-contention`, o veredito em formato curva.**

O E4 está no MVP
([`../plano-do-laboratorio.md`](../plano-do-laboratorio.md#e4--optimistic-under-contention))
e **não tem card**, porque o formato de veredito dele não foi decidido.

**A composição global dos formatos de veredito não foi decidida, e esta seção é o dono
dessa afirmação.** O que está decidido é o formato local de cada oráculo já
especificado, e nada além disso: a contagem exata do contador, pelo
[`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#o-oráculo-exato); o
predicado booleano da capacidade, pelo
[`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#o-oráculo-do-predicado);
e a taxa de violação com limite superior de confiança, pelo
[`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-veredito-de-uma-execução-medida-é-uma-taxa).

**Quantos formatos existem ao todo, como eles convivem e o que um relatório publica
continua aberto.** Nenhum documento deste repositório enumera esse conjunto, e um que o
enumere está errado enquanto a decisão não for tomada. Questões encaminhadas mudam o
escopo dela antes que seja tomada: [`Q-0002-3`](../questions/Q-0002-3.md) acrescenta o
eixo pontual contra contínuo no tempo, [`Q-0004-5`](../questions/Q-0004-5.md) acrescenta
um formato que não é caso particular dos outros, e
[`Q-0004-8`](../questions/Q-0004-8.md) pergunta o que a incerteza publicada afirma. Cite
cada questão pelo identificador que o
[índice de questões](../questions/README.md#identificador) define.

O que existe hoje sobre o E4 é o estímulo (`OPTIMISTIC` fixo, workers de 2 a 50) e a
forma esperada do resultado (correção verde, retries crescendo mais rápido que
linearmente, throughput com pico e queda). Não existe regra sobre como uma curva é
declarada, comparada ou reprovada.

**Um card escrito agora seria majoritariamente pergunta em aberto.** Ele será escrito
quando a decisão dos formatos de veredito for tomada.

## O que estes cards não cobrem

Nenhum card trata de entrega, empacotamento ou pipeline. Isso não é capacidade do
laboratório — é como ele chega ao cluster. A matriz está em
[`../architecture/integrations.md`](../architecture/integrations.md), e a forma da
entrega continua sem decisão tomada.

Os itens do escopo total não têm card. Só o MVP tem, e o MVP é inteiramente do grupo A.
O catálogo deles é do [plano do laboratório](../plano-do-laboratorio.md).
