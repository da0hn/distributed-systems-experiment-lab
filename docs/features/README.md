# Capacidades

As capacidades do laboratório, especificadas por Feature Card e Example Mapping. Os
quatro `behavior.feature` existem na árvore e estão **inativos** — a subseção do índice
diz por quê.

O processo está em [`../specification-process.md`](../specification-process.md).

## Índice

| Capacidade                                                                         | O que ela responde                                                       | Origem                                                                                          | Regras               | Estado                         |
|------------------------------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|----------------------|--------------------------------|
| [observacao-passo-a-passo](observacao-passo-a-passo/feature-card.md)               | como parar, falhar e observar **entre** dois passos de uma operação      | [`ADR-0001`](../adr/0001-o-passo-como-unidade-de-execucao.md), `Aceito`                         | 12, todas `pendente` | especificado, não implementado |
| [execucao-de-experimento](execucao-de-experimento/feature-card.md)                 | o que um resultado zero significa, e quando ele é defeito do instrumento | [`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md), `Aceito` | 14, todas `pendente` | especificado, não implementado |
| [deteccao-de-atualizacao-perdida](deteccao-de-atualizacao-perdida/feature-card.md) | quantos incrementos se perderam, e sob qual proteção — E1 e E3           | [`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`                      | 18, todas `pendente` | especificado, não implementado |
| [deteccao-de-protecao-inerte](deteccao-de-protecao-inerte/feature-card.md)         | por que uma proteção pode estar presente e não proteger nada — E5        | [`ADR-0002`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md), `Aceito`                      | 8, todas `pendente`  | especificado, não implementado |

**Nenhuma capacidade está implementada, e isso não quer dizer que não haja código.** Há
um esqueleto executável: ele compila, empacota e sobe contra PostgreSQL, e **não tem
uma única regra de negócio dentro**. A árvore versionada é a prova do que existe; este
índice é o dono do que cada capacidade cobre, e a coluna `Regras` é a dona de quantas
regras cada uma tem.

**Nenhuma regra foi aprovada por pessoa.** Aprova-se a **regra** e não o card, pela
decisão `B-3`, de 2026-08-05, e uma regra `pendente` NÃO DEVE virar cenário Gherkin. O
mesmo raciocínio alcança qualquer conversão automática do card para fora daqui.

### Os quatro `behavior.feature` estão inativos

Os arquivos ficam na árvore e **não** são especificação viva: nenhuma regra que eles
cobrem tem `Aprovada por` preenchido, e o cabeçalho de cada um declara isso. Enquanto
valer, nenhum cenário deles sustenta teste ou código.

Eles voltam ao conjunto ativo **regra a regra**, e não de uma vez: quando uma pessoa
aprovar uma regra, os cenários que ela sustenta deixam de ser inativos. Até lá nada é
migrado nem apagado.

## Por que quatro cards, e não cinco

O MVP tem quatro experimentos, e os cards **não** são um por experimento. Um card cobre um
**oráculo**, porque é o oráculo que define o comportamento observável:

- E1 e E3 compartilham o oráculo exato do contador. O E3 varia a estratégia sobre a mesma
  carga, e isso não muda o que é medido. Um card só.
- E5 tem um oráculo diferente — um predicado sobre um conjunto, não uma contagem. Card
  próprio.
- E2 deixou de ser experimento. O [`ADR-0004`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-e2-deixa-de-ser-um-experimento-do-mvp)
  o rebaixou a execução de controle positivo, e ele vive dentro de
  [execucao-de-experimento](execucao-de-experimento/feature-card.md).

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
