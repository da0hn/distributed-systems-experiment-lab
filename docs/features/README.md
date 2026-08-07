# Capacidades

As capacidades do laboratório, especificadas por Feature Card, Example Mapping e Gherkin.

O processo está em [`../specification-process.md`](../specification-process.md).

## Índice

| Capacidade                                                                         | O que ela responde                                                       | Origem                                                                                          | Estado                         |
|------------------------------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|--------------------------------|
| [observacao-passo-a-passo](observacao-passo-a-passo/feature-card.md)               | como parar, falhar e observar **entre** dois passos de uma operação      | [`ADR-0001`](../adr/0001-o-passo-como-unidade-de-execucao.md), `Aceito`                         | especificado, não implementado |
| [execucao-de-experimento](execucao-de-experimento/feature-card.md)                 | o que um resultado zero significa, e quando ele é defeito do instrumento | [`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md), `Aceito` | especificado, não implementado |
| [deteccao-de-atualizacao-perdida](deteccao-de-atualizacao-perdida/feature-card.md) | quantos incrementos se perderam, e sob qual proteção — E1 e E3           | [`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`                      | especificado, não implementado |
| [deteccao-de-protecao-inerte](deteccao-de-protecao-inerte/feature-card.md)         | por que uma proteção pode estar presente e não proteger nada — E5        | [`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`                      | especificado, não implementado |

**Nenhuma capacidade está implementada, e desde 2026-08-06 isso deixou de significar que
não há código.** O esqueleto existe: `git ls-files` retorna 158 arquivos, dos quais 27 são
de linguagem, build ou configuração de infraestrutura. Ele compila, empacota e sobe contra
PostgreSQL — e **não tem uma única regra de negócio dentro**. Nenhuma tabela existe: as
três migrações `V1` criam apenas o schema de cada serviço. Os `.feature` continuam sendo
especificação viva, e cada cenário está marcado com `@teste-ausente`.

**As 48 regras das quatro capacidades estão `pendente`.** Nenhuma foi aprovada por pessoa.
Pela decisão `B-3`, de 2026-08-05, aprova-se a **regra** e não o card — e uma regra
`pendente` NÃO DEVE virar cenário Gherkin. O mesmo raciocínio alcança qualquer conversão
automática do card para fora daqui.

## Por que quatro cards, e não cinco

O MVP tem quatro experimentos, e os cards **não** são um por experimento. Um card cobre um
**oráculo**, porque é o oráculo que define o comportamento observável:

- E1 e E3 compartilham o oráculo exato do contador. O E3 varia a estratégia sobre a mesma
  carga, e isso não muda o que é medido. Um card só.
- E5 tem um oráculo diferente — um predicado sobre um conjunto, não uma contagem. Card
  próprio.
- E2 deixou de ser experimento. O [`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md):272-276
  o rebaixou a execução de controle positivo, e ele vive dentro de
  [execucao-de-experimento](execucao-de-experimento/feature-card.md).

## Capacidade conhecida e não especificada

**E4 — `optimistic-under-contention`, o veredito em formato curva.**

O E4 está no MVP (`../plano-do-laboratorio.md`:441-449) e **não tem card**. O motivo é
que o formato de veredito dele não foi decidido: a fila de decisões enfileira "os dois
formatos de veredito" na posição 9, e três questões encaminhadas mudam o escopo daquela
decisão antes que ela seja tomada — [`Q-0002-3`](../questions/Q-0002-3.md) acrescenta o
eixo pontual contra contínuo no tempo, [`Q-0004-5`](../questions/Q-0004-5.md) acrescenta
um terceiro formato, e [`Q-0004-8`](../questions/Q-0004-8.md) pergunta o que a incerteza
publicada afirma.

O que existe hoje sobre o E4 é o estímulo (`OPTIMISTIC` fixo, workers de 2 a 50) e a forma
esperada do resultado (correção verde, retries crescendo mais rápido que linearmente,
throughput com pico e queda). Não existe regra sobre como uma curva é declarada,
comparada ou reprovada.

**Um card escrito agora seria majoritariamente pergunta em aberto.** Ele será escrito
quando a decisão dos formatos de veredito for tomada.

## O que estes cards não cobrem

Nenhum card trata de entrega, empacotamento ou pipeline. Isso não é capacidade do
laboratório — é como ele chega ao cluster. A matriz está em
[`../architecture/integrations.md`](../architecture/integrations.md), e a decisão está
enfileirada em [`../adr/README.md`](../adr/README.md).

Os 42 fenômenos do escopo total não têm card. Só o MVP tem, e o MVP é inteiramente do
grupo A.
