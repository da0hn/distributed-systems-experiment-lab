# Fila de decisões

Fila única deste repositório. Criada em 2026-08-05 pela decisão `B-1`, registrada em
[`arquivo/proposta-2026-08-03/decisoes-pendentes.md`](arquivo/proposta-2026-08-03/decisoes-pendentes.md).

Antes dela existiam duas listas do mesmo tipo de coisa, e a sobreposição era medida: os
três primeiros assuntos da rodada de arquitetura vinham colados numa linha só da fila
derivada do plano. Enquanto foram duas, uma decisão PODE ter sido tomada numa e reaberta
na outra.

## O que esta fila enfileira

**Decisão, e não ADR.** Desde 2026-08-04, o artefato que uma linha gera é escolhido no
momento em que a decisão é tomada, e não antes: ADR quando a escolha atender aos quatro
critérios de [`README.md`](README.md#uma-decisão-merece-adr-quando), artefato de
[`../features/`](../features/README.md) quando não atender. Uma linha PODE gerar os dois,
e PODE não gerar ADR nenhum.

```mermaid
flowchart LR
  L["linha desta fila:<br/>problema, alternativas"] --> E["a pessoa escolhe"]
  E --> T{"atende aos quatro<br/>critérios de ADR?"}
  T -->|" sim "| ADR["ADR, criado já Aceito"]
  T -->|" não "| ART["artefato de features/,<br/>contrato ou tarefa"]
  ADR --> F["a linha fecha,<br/>citando o artefato"]
  ART --> F
```

**A poda não acontece antes da decisão.** A pendência de podar as linhas que são
comportamento disfarçado de arquitetura fechou em 2026-08-05, pela decisão `B-2`, por
subsunção: podar hoje é escolher o artefato antes da decisão, que é o oposto da regra
acima. A poda acontece uma linha por vez, quando a pessoa escolhe.

## Como citar uma linha desta fila

**Pelo nome, nunca pela posição.** A posição muda quando uma decisão entra no meio, e
uma citação por posição continua válida depois da inserção — passando a apontar para
outra decisão.

**Por âncora nomeada, nunca por número de linha.** É a decisão `C-1`, de 2026-08-05, com
o slug do GitHub Flavored Markdown fixado por `C-1a`. O verificador
[`scripts/check_citations.py`](../../scripts/check_citations.py) confere as duas formas.

Os números de ADR **não** estão atribuídos nas linhas abertas. Um número é atribuído
quando o ADR é escrito — atribuir antes cria buracos na sequência quando a ordem muda.

## As decisões derivadas do plano

Ordem derivada de [`../plano-do-laboratorio.md`](../plano-do-laboratorio.md). A coluna
`Ordem` é posição na fila, e ela muda.

| Ordem | Decisão                                                      | Estado                                   |
|-------|--------------------------------------------------------------|------------------------------------------|
| 1     | **O passo como unidade de execução, observação e injeção**   | `Aceito` — ADR-0001                      |
| 2     | **O domínio mínimo: contador e predicado de capacidade**     | `Aceito` — ADR-0002                      |
| 3     | **O estatuto da barreira e o diagnóstico da não ocorrência** | `Aceito` — ADR-0004                      |
| 4     | **A linguagem do agendamento**                               | `Aceito` — ADR-0003                      |
| 5     | **A forma do escalonador**                                   | `Aceito` — ADR-0005                      |
| 6     | **Estratégias de concorrência como dado, não como branch**   | `Aceito` — ADR-0006                      |
| 7     | **O log de observações: forma, ordem e onde vive**           | `Aceito` — ADR-0007                      |
| 8     | **Experiment: definição, semente, hipótese e asserções**     | aberta                                   |
| 9     | **Os dois formatos de veredito: booleano e curva**           | aberta                                   |
| 10    | **Arquitetura mínima, stack e guardas executáveis**          | **parcialmente consumida** pelo ADR-0008 |
| 11    | **Entrega contínua no homelab desde o dia zero**             | aberta                                   |

O porquê de cada posição, as questões que cada linha carrega e o histórico de como a
fila chegou a esta ordem estão em [`README.md`](README.md#índice) e nos próprios ADRs. As três
linhas abertas levam o detalhe abaixo.

**Posição 8 — Experiment.** Precisa resolver a tensão entre o Designer na interface e a
definição versionada. [`Q-0002-4`](../questions/Q-0002-4.md) pede aqui o ciclo de vida de
uma execução, [`Q-0003-8`](../questions/Q-0003-8.md) o que `N` conta, e
[`Q-0001-1`](../questions/Q-0001-1.md) a identidade de versão de uma operação.

**Posição 9 — os dois formatos de veredito.** Se ficar para depois, o grupo D não cabe
na arquitetura. [`Q-0002-3`](../questions/Q-0002-3.md) acrescenta o eixo pontual contra
contínuo no tempo, e [`Q-0003-3`](../questions/Q-0003-3.md) pede o que "mesma taxa"
significa numa execução medida.

**Posição 10 — arquitetura mínima.** O
[ADR-0008](0008-os-dois-planos-em-processos-separados.md) fixou dois processos separados
e o pacote raiz. Restam o build, o número de módulos e a guarda que
[`Q-0002-1`](../questions/Q-0002-1.md) pede para as três regras hoje textuais.

**Posição 11 — entrega contínua.** O serviço precisa nascer entregando; a linha ratifica
ou emenda a ADR 0017 do homelab.

## As decisões da rodada de arquitetura de 2026-08-03

Sessenta e seis linhas com identificador `D-*`, agrupadas por bloco. O agrupamento
**não** é o documento que cada assunto vai gerar: esse só existe depois da escolha.

**Três linhas já fecharam** — `D-ARQ-05`, `D-ARQ-06` e `D-ARQ-01`, todas pelo
[ADR-0008](0008-os-dois-planos-em-processos-separados.md). **Quatro mais** — as do Bloco
4 — fecharam em 2026-08-04, e o debate delas vive **neste arquivo** desde 2026-08-07,
quando [`../CONTEXT.md`](../CONTEXT.md) voltou a ser só glossário. **Uma quinta**,
`D-DAT-05`, fechou em 2026-08-05.

### Bloco 0 — sem estas seis, nenhuma linha de código é escrita

São as que a fila de [`README.md`](README.md) enfileira nas
posições 10 e 11, e a exigência de nascer entregando as torna as primeiras.

| ID         | Decisão                                  | Recomendação da proposta                          | Onde                                                                                                         |
|------------|------------------------------------------|---------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| `D-ARQ-05` | mecanismo de módulo do primeiro artefato | Maven multi-módulo, quatro módulos, mais ArchUnit | [`arquivo/proposta-2026-08-03/modulos-e-fronteiras.md`](arquivo/proposta-2026-08-03/modulos-e-fronteiras.md) |
| `D-ARQ-12` | Maven contra Gradle                      | emendar a ADR 0017 do homelab para Maven          | [`arquivo/proposta-2026-08-03/entrega-continua.md`](arquivo/proposta-2026-08-03/entrega-continua.md)         |
| `D-ARQ-06` | pacote raiz e idioma dos identificadores | `dev.da0hn.lab`, região no primeiro segmento      | [`arquivo/proposta-2026-08-03/modulos-e-fronteiras.md`](arquivo/proposta-2026-08-03/modulos-e-fronteiras.md) |
| `D-ARQ-15` | a forma do `deploy/` no primeiro commit  | `deploy/` mínimo agora, uma réplica               | [`arquivo/proposta-2026-08-03/entrega-continua.md`](arquivo/proposta-2026-08-03/entrega-continua.md)         |
| `D-ARQ-14` | o que o pipeline executa                 | só guardas e provas; experimento sob demanda      | [`arquivo/proposta-2026-08-03/entrega-continua.md`](arquivo/proposta-2026-08-03/entrega-continua.md)         |
| `D-DAT-04` | ferramenta de migração                   | Flyway com SQL versionado                         | [`arquivo/proposta-2026-08-03/modelo-de-dados.md`](arquivo/proposta-2026-08-03/modelo-de-dados.md)           |

**`D-ARQ-05` e `D-ARQ-06` estão fechadas** pelo
[ADR-0008](0008-os-dois-planos-em-processos-separados.md), `Aceito` em
2026-08-04. A escolha não foi a recomendação da linha: o mecanismo de módulo é a
**fronteira de processo**, e não Maven multi-módulo. O pacote raiz `dev.da0hn.lab` com a
região no primeiro segmento foi aceito como recomendado, com os identificadores
**todos** em inglês. As duas linhas permanecem na tabela para que o histórico da
recomendação não se perca.

`D-ARQ-12` é a única com custo fora deste repositório: ela emenda um documento
`Aceito` do [`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure).
`D-ARQ-15` fecha o `ComparisonError` que o ArgoCD reporta hoje, e a separação por
processo muda a forma que ela precisa declarar.

### Bloco 1 — destravam o esquema e a primeira migração

| ID         | Decisão                                       | Recomendação da proposta                 |
|------------|-----------------------------------------------|------------------------------------------|
| `D-DAT-01` | tipo e derivação da coluna de identidade      | `bigint` ordinal da semente              |
| `D-DAT-02` | chave estrangeira de `allocation.resource_id` | sem FK no MVP                            |
| `D-DAT-03` | índice sobre `allocation(resource_id)`        | criar, e registrar o plano efetivo       |
| `D-DAT-05` | como o banco volta ao ponto de partida        | decidida em 2026-08-05: não há reset     |
| `D-DOM-14` | dono da identidade derivada da semente        | o experimento publica; o domínio consome |
| `D-DOM-13` | o esquema compartilhado entre os dois planos  | Shared Kernel com contrato verificável   |

`D-DAT-02` tem a justificativa mais afiada da rodada: com chave estrangeira, o
`INSERT` de uma alocação toma `FOR KEY SHARE` na linha do recurso e conflita com
o `FOR UPDATE` do `PESSIMISTIC` — uma restrição de integridade mudaria o
fenômeno medido.

`D-DAT-05` recomendava `TRUNCATE` antes de cada execução até 2026-08-05, quando uma
quarta candidata entrou — pôr a execução na chave primária, preservando todo o
histórico — e `P-DAT-9` mostrou que a objeção de `Q-0002-4` contra preservar linhas
entre execuções não se sustenta sobre nenhum dos dois critérios de igualdade aceitos.
**O usuário decidiu na mesma data: não há reset.** A chave primária das duas tabelas
passa a incluir um discriminador UUIDv7, gerado pelo Lab Plane e propagado a tudo que o
sistema medido publica, com o crescimento das tabelas aceito. A linha permanece aqui
para que o histórico da recomendação não se perca; a decisão e o que ela deixa em aberto
estão em [`arquivo/proposta-2026-08-03/modelo-de-dados.md`](arquivo/proposta-2026-08-03/modelo-de-dados.md), seção 7, `D-DAT-05`, `P-DAT-10` e
`P-DAT-11`.

### Bloco 2 — destravam o E1 e a etapa 1

| ID         | Decisão                                  | Recomendação da proposta                            |
|------------|------------------------------------------|-----------------------------------------------------|
| `D-ARQ-04` | modelo de thread do worker               | threads de plataforma no MVP                        |
| `D-ARQ-07` | o que verifica cada classe de regra      | compilação para região; ArchUnit para o resto       |
| `D-ARQ-08` | onde vivem o relógio e a fonte semeada   | isenção posicional, sem anotação de supressão       |
| `D-ARQ-09` | a forma da guarda da chave de contenção  | recusa na primeira passagem                         |
| `D-DAT-08` | como o nível de isolamento é aplicado    | `TransactionTemplate`, pelo runtime                 |
| `D-DAT-09` | verificação de "uma conexão por worker"  | tamanho de pool mais asserção de PID distinto       |
| `D-DOM-07` | `Allocation` é agregado próprio          | agregado próprio                                    |
| `D-DOM-08` | onde vive `Σ amount ≤ capacity`          | no oráculo, como invariante observada               |
| `D-DOM-15` | quais fronteiras a stack materializa     | só system under test / Lab Plane, imposta por teste |
| `D-UI-02`  | onde o frontend renderiza                | exportação estática                                 |
| `D-UI-03`  | framework de componentes                 | shadcn/ui sobre Radix                               |
| `D-UI-04`  | eixo padrão da timeline                  | posição no log, com arestas causais                 |
| `D-UI-06`  | teto de eventos no navegador             | paginação contra o servidor                         |
| `D-UI-07`  | autenticação e autoria                   | nenhuma, declarada; autoria vinda do commit         |
| `D-UI-08`  | o que o `POST` cria                      | a sequência de execuções, não uma                   |
| `D-UI-09`  | mecanismo de streaming                   | SSE, com limiar numérico proposto                   |
| `D-UI-10`  | idempotência de iniciar execução         | chave obrigatória do cliente                        |
| `D-UI-11`  | vocabulário do contrato                  | português, igual ao glossário                       |
| `D-UI-12`  | compatibilidade e enumeração do veredito | enumeração aberta, cliente falha fechado            |

`D-ARQ-07` e `D-ARQ-08` são a resposta proposta a
[`Q-0002-1`](../questions/Q-0002-1.md), que pede a guarda executável das três
regras hoje textuais. `D-ARQ-09` responde
[`Q-0004-2`](../questions/Q-0004-2.md).

`D-DOM-07` e `D-DOM-08` carregam a descoberta conceitual da rodada: **o
agregado clássico do DDD é antipadrão aqui.** Um `Resource` que impusesse
`Σ amount ≤ capacity` na fronteira transacional tornaria o E5 irreproduzível,
pelo mesmo argumento com que o ADR-0002 descartou a constraint no banco —
confundir observar com impedir (`0002-...md:566-574`).

### Bloco 3 — pertencem a um ADR já enfileirado, e a recomendação é não decidir agora

| ID         | Decisão                                  | Destino na fila de ADRs                                       |
|------------|------------------------------------------|---------------------------------------------------------------|
| `D-DOM-06` | o que `N` conta                          | Experiment, posição 8; [`Q-0003-8`](../questions/Q-0003-8.md) |
| `D-DOM-09` | se `Experimento` é raiz das execuções    | Experiment, posição 8                                         |
| `D-DAT-07` | onde vive a definição de experimento     | Experiment, posição 8                                         |
| `D-UI-01`  | fonte de verdade da definição            | Experiment, posição 8                                         |
| `D-DOM-05` | se `veredito` vira quatro termos         | formatos de veredito, posição 9                               |
| `D-DOM-16` | se o modelo reserva lugar para a curva   | formatos de veredito, posição 9                               |
| `D-DOM-10` | se o log é agregado próprio              | gatilho na etapa 6                                            |
| `D-DOM-12` | se a injeção de falha é contexto próprio | gatilho na etapa 6                                            |

Aprovar qualquer uma destas **antecipa um ADR enfileirado**, e é a forma mais
provável de esta rodada causar dano. A recomendação de cada uma é adiar.

Duas das oito são decisões de vocabulário, e o debate delas foi trazido de
[`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07, quando o glossário voltou a ser só
glossário. A tabela das seis decisões de vocabulário está no
[Bloco 4](#bloco-4--vocabulário-decidível-a-qualquer-momento-e-barato). **`D-DOM-05` e
`D-DOM-06` continuam abertas**, e nada abaixo as fecha: o que veio do glossário é o
enunciado, as alternativas e a recomendação de cada uma.

#### D-DOM-05 — Se `verdict` vira quatro termos

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção `D-DOM-05`, que
lá virou lápide. O texto é o de lá, com o nível de título rebaixado.

**O problema.** `verdict` nomeia a taxa de violação (`0004:112-113`), o rótulo da
classificação do zero (`0004:206-218`), o booleano do predicado de capacidade
(`0002:186-190`) e a curva do grupo D, que não tem forma decidida (`plano:226-229`).

**Alternativa A — quatro termos distintos.** A favor: cada formato ganha nome, e a
tabela comparativa do E3 deixa de misturar coisas diferentes na mesma coluna. Contra:
antecipa a decisão da posição 9 da fila, que é justamente sobre como os formatos
convivem.

**Alternativa B — um termo com formato declarado.** A favor: o glossário fica estável
enquanto a decisão dos formatos não é tomada, e o relatório declara o formato ao lado do
número. Contra: quem lê um relatório precisa ler duas coisas para entender uma.

**Alternativa C — adiar até a fila resolver.** A favor: nenhum termo nasce antes da
decisão que o fixa. Contra: os quatro Feature Cards já usam a palavra, e o adiamento
mantém a ambiguidade em documentos vivos.

**Recomendação.** Alternativa B, com revisão obrigatória quando a decisão dos dois
formatos de veredito for tomada.

**Se a escolha for outra.** Com a alternativa A, o E4 ganha vocabulário antes de ter
card, e o motivo registrado em `features/README.md:35-51` deixa de valer.

#### D-DOM-06 — O que `N` conta

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção `D-DOM-06`, que
lá virou lápide. O texto é o de lá, com o nível de título rebaixado e o caminho de
`Q-0003-8` reescrito de `docs/` para `docs/adr/`. A frase "este glossário não escolhe"
fala de [`../CONTEXT.md`](../CONTEXT.md), e não desta fila.

**O problema.** [`Q-0003-8`](../questions/Q-0003-8.md) mostra que as duas leituras de `N`
quebram em pontos diferentes. Se `N` conta `attempt` do ADR-0001, ele inclui retries, e
o número de retries é resultado da execução. Se conta `operation execution`, a taxa de
aborto deixa de enxergar o trabalho descartado, que é o que ela existe para mostrar.

**Alternativa A — `N` conta `attempt` do ADR-0001.** A favor: é a leitura literal de
`launched attempt` no ADR-0004. Contra: sob `OPTIMISTIC` o número não é declarável antes
de executar, e o E3 e o E4 rodam `OPTIMISTIC`.

**Alternativa B — `N` conta `operation execution`.** A favor: é declarável antes.
Contra: a taxa de aborto de uma execução que falha duas vezes e comete na terceira é
zero, e a justificativa do ADR-0004 diz que essa taxa existe para mostrar o trabalho
descartado.

**Alternativa C — dois números, um declarado e um observado.** A favor: cada um mede o
que sabe medir. Contra: exige um ADR que substitua a contagem de um ADR aceito, e
`Q-0003-8` registra essa possibilidade sem escolhê-la.

**Recomendação.** Manter a pergunta aberta e citá-la por `Q-0003-8` até a decisão
`Experiment`. Este glossário não escolhe.

**Se a escolha for outra.** Qualquer das três muda o significado da taxa de aborto na
tabela comparativa do E3, que é um resultado já especificado em Feature Card.

### Bloco 4 — vocabulário, decidível a qualquer momento e barato

**As quatro estão fechadas desde 2026-08-04.** As escolhas e as consequências de cada
uma vivem **aqui**, nas quatro seções ao fim deste bloco. Elas moravam em
[`../CONTEXT.md`](../CONTEXT.md), seção "As seis decisões de vocabulário", e vieram para
cá em 2026-08-07: o glossário guarda hoje o estado de cada termo e uma lápide por
decisão, e não o debate.

| ID         | Decisão                                             | Escolha                                                 | Seguiu a recomendação? |
|------------|-----------------------------------------------------|---------------------------------------------------------|------------------------|
| `D-DOM-01` | qual sentido `execução` carrega sozinha             | `run` no experimento, `operation execution` na operação | sim                    |
| `D-DOM-02` | separar `system under test` de execução de controle | renomear para `system under test`                       | **não**                |
| `D-DOM-03` | se `barreira` continua na linguagem                 | aposentar, com citação histórica permitida              | sim                    |
| `D-DOM-04` | os dois sentidos de `estratégia`                    | `strategy` e `strategy label`                           | sim                    |

`D-DOM-03` foi executada no mesmo turno: os oito pontos de
[`arquivo/proposta-2026-08-03/mensageria.md`](arquivo/proposta-2026-08-03/mensageria.md) que usavam `barreira` como termo passaram a dizer
`restrição de precedência` ou `espera`, e o mérito de `D-MSG-11` não mudou.

`D-DOM-02` foi decidida contra a recomendação, e abriu duas perguntas que a alternativa
A não tratava: se `Lab Plane` acompanha a renomeação, e se ela alcança as 95 ocorrências
em texto editável ou só o glossário. As duas estão na seção
[`D-DOM-02`](#d-dom-02--como-separar-control-plane-de-control-run) ao fim deste bloco,
trazida de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07.

**Pergunta em aberto.** Qual artefato registra estas quatro? O processo de
[`README.md`](README.md) prevê ADR ou artefato de
[`../features/`](../features/README.md), e vocabulário não é nem um nem outro — ele vive
no glossário, por instrução de [`../AGENTS.md`](../AGENTS.md), seção `## Glossário de
domínio`. `D-DOM-02` é a que mais puxa para ADR: ela renomeia um termo presente em
quatro ADRs aceitos, e o rastro de alterações adotado em 2026-08-04 obrigaria a carimbar
os quatro.

Estas quatro existem porque **os ADRs aceitos já colidem entre si no
vocabulário**. Decidi-las é barato agora e caro depois de existir código.

**A contra-avaliação sustenta este bloco.** Ele é "o único bloco aprovável como está"
([`arquivo/proposta-2026-08-03/contra-avaliacao.md`](arquivo/proposta-2026-08-03/contra-avaliacao.md), linhas 430 a 434), porque as quatro
colisões são reais entre ADRs aceitos, independem da fila e ficam caras depois de
existir código. Nenhuma das quatro pode ser resolvida editando um ADR.

Dois fatos levantados em 2026-08-04, antes de qualquer escolha.

**O glossário já aplicou a recomendação de `D-DOM-03` sem a decisão existir.**
[`../CONTEXT.md`](../CONTEXT.md), linha 355, marca `barrier` como `aposentado`, e a
tabela de estados daquele arquivo (linha 49) reserva esse rótulo para o que "existiu em
ADR aceito e foi retirado da linguagem por outro ADR". A recomendação virou texto antes
de virar escolha. Se a decisão for outra, aquela entrada muda junto, e o registro disso
não pode depender da memória de quem editou.

**Aprovar `D-DOM-03` obriga reescrever [`arquivo/proposta-2026-08-03/mensageria.md`](arquivo/proposta-2026-08-03/mensageria.md) no mesmo
turno.** A palavra é termo vivo e normativo ali:
`arquivo/proposta-2026-08-03/mensageria.md:520`, `:539`, `:548-553`, `:805` e `:1034-1054`,
inclusive no enunciado e nas três alternativas de `D-MSG-11`. A ressalva está em [`arquivo/proposta-2026-08-03/contra-avaliacao.md`](arquivo/proposta-2026-08-03/contra-avaliacao.md), linhas 143
a 145; o inventário de linhas é novo.

#### As seis decisões de vocabulário

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção
`## As seis decisões de vocabulário`, que lá virou lápide. A tabela cobre as seis, e por
isso fica aqui: as quatro fechadas são deste bloco, e `D-DOM-05` e `D-DOM-06` estão no
[Bloco 3](#bloco-3--pertencem-a-um-adr-já-enfileirado-e-a-recomendação-é-não-decidir-agora),
onde o debate das duas também foi absorvido.

Quatro foram tomadas em 2026-08-04, e três delas seguiram a recomendação. A quarta,
`D-DOM-02`, foi decidida **contra** a recomendação, e as consequências disso estão
escritas na seção dela.

| ID       | Decisão                                          | Escolha                                                        | Estado                          |
|----------|--------------------------------------------------|----------------------------------------------------------------|---------------------------------|
| D-DOM-01 | Se `run` e `execution` nomeiam níveis diferentes | `run` no experimento, `operation execution` na operação        | decidida, como recomendado      |
| D-DOM-02 | Como separar `Control Plane` de `control run`    | renomear `Control Plane` para `system under test`              | decidida, contra a recomendação |
| D-DOM-03 | Se `barrier` continua na linguagem               | aposentar, com citação histórica permitida                     | decidida, como recomendado      |
| D-DOM-04 | Como nomear os dois sentidos de `strategy`       | `strategy` no system under test, `strategy label` no Lab Plane | decidida, como recomendado      |
| D-DOM-05 | Se `verdict` vira quatro termos                  | —                                                              | em aberto                       |
| D-DOM-06 | O que `N` conta                                  | —                                                              | em aberto                       |

As duas em aberto continuam exigindo aprovação humana pelo mesmo motivo de antes:
`D-DOM-05` depende dos formatos de veredito, que estão na fila, e `D-DOM-06` pode exigir
um ADR que substitua a contagem do ADR-0004.

#### D-DOM-01 — Se `run` e `execution` nomeiam níveis diferentes

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção `D-DOM-01`, que
lá virou lápide. O texto é o de lá, com o nível de título rebaixado; "este glossário"
nomeia [`../CONTEXT.md`](../CONTEXT.md), e não esta fila.

**O problema, e o que a conversão muda nele.** Em português a palavra `execução` nomeava
duas coisas. O ADR-0001 a usa para a invocação de uma operação por um worker
(`:152-154`). Os ADRs 0003, 0004 e 0005 a usam para uma das quatro passagens de um
experimento (`0003:154-157`, `0004:21`, `0005:60-61`). As duas conviviam em parágrafos
vizinhos, e "o veredito da execução" mudava de referente conforme quem lesse.

O inglês tem duas palavras para isso. Este glossário dá `run` ao nível do experimento —
`measured run`, `control run`, `negative control`, `positive control`, `calibration` — e
`operation execution` ao nível do worker. A palavra `execution` sozinha deixa de ter
dono.

**A colisão se dissolve, e a decisão não.** Essa separação é a alternativa B do
enunciado original, agora escrita no próprio vocabulário em vez de numa convenção de
prosa. Ela continua exigindo aprovação porque **muda a leitura de sete ADRs aceitos**:
onde eles escrevem `execução` sozinha, é preciso saber qual dos dois níveis está em
jogo, e a tabela de de/para não desfaz essa ambiguidade — ela só nomeia o destino de
cada sentido.

**Alternativa A — usar `execution` nos dois níveis, com qualificador obrigatório.** A
favor: espelha o corpus português linha a linha, e a regra é verificável por busca de
texto. Contra: reintroduz em inglês uma colisão que a língua não obriga, e o
qualificador some na primeira frase escrita com pressa.

**Alternativa B — `run` no experimento, `execution` na operação.** A favor: é o uso
majoritário dos ADRs 0003 a 0005, inclusive em títulos de seção, e o inglês torna a
regra lexical em vez de convencional. Contra: `execution scope`, `execution runtime` e
`operation execution` ficam no nível do worker, e quem leu o corpus português precisa
aprender de que lado cada composto está.

**Alternativa C — reservar `run` para a operação e `execution` para o experimento.** A
favor: nenhuma. Contra: contraria o uso dos três ADRs mais recentes e o sentido comum de
`run` em Java, onde `Runnable.run` é a unidade de trabalho.

**Recomendação.** Alternativa B. O corpus já a pratica, e ela não exige contrariar
nenhum texto aceito.

**Se a escolha for outra.** Com a alternativa A, todo Feature Card e todo diagrama
passam a carregar o qualificador. Com a alternativa C, o ADR-0005 fica com o contador de
ativos pendurado num referente que a linguagem deixou de nomear.

**Decisão tomada em 2026-08-04: alternativa B.** `run` nomeia o nível do experimento e
`operation execution` nomeia o nível do worker. A palavra `execution` sozinha NÃO DEVE
ser usada sem qualificador em documento novo. As entradas deste glossário já praticam a
escolha, e nenhuma delas muda.

**A consequência que não estava escrita.** Os sete ADRs aceitos escrevem `execução`
sozinha, e nenhum pode ser editado. A tabela de de/para nomeia o destino de cada
sentido, e não desfaz a ambiguidade dentro daqueles textos. Quem ler um ADR aceito
continua precisando decidir, pelo contexto, qual dos dois níveis está em jogo.

#### D-DOM-02 — Como separar `Control Plane` de `control run`

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção `D-DOM-02`, que
lá virou lápide. O texto é o de lá, com o nível de título rebaixado e os caminhos
relativos reescritos de `docs/` para `docs/adr/`. **"Este glossário", "este arquivo" e
"a entrada `Lab Plane` deste glossário" nomeiam [`../CONTEXT.md`](../CONTEXT.md)**, e
não esta fila.

**O problema.** `Control Plane` é o sistema sob teste (`plano:550-555`). `control run` é
um artefato do Lab Plane que existe para interpretar um resultado (`0004:29-30`). Um
leitor que encontre "o controle violou" precisa de contexto externo para saber de qual
dos dois se fala. A tradução não ajuda: em inglês a palavra colidente é `control`, e ela
está nos dois termos.

**Alternativa A — renomear `Control Plane`.** A favor: `system under test` já circula no
corpus e diz exatamente a mesma coisa sem a palavra ambígua. Contra: o nome está no
`AGENTS.md` da raiz, no plano e em cinco ADRs aceitos, e a renomeação invalidaria as
citações por linha que este repositório exige.

**Alternativa B — renomear `control run`.** A favor: o termo é mais novo e tem menos
ocorrências. Contra: ele vem do vocabulário de método experimental, onde `negative
control` e `positive control` são os nomes canônicos, e trocá-los apagaria a analogia
que sustenta a decisão do ADR-0004.

**Alternativa C — manter os dois, e preferir `system under test` na prosa.** A favor:
nenhum ADR é contrariado, e a prosa deixa de usar a palavra ambígua no sentido de plano.
Contra: os diagramas continuam rotulando a caixa como `Control Plane`, e a ambiguidade
sobrevive na leitura de um diagrama isolado.

**Recomendação.** Alternativa C, com `Control Plane` reservado para o par de planos em
diagramas.

**Se a escolha for outra.** Com a alternativa A, o `AGENTS.md` da raiz e a matriz de
integrações mudam junto. Com a alternativa B, o ADR-0004 fica lido com um vocabulário
que ele não usa.

**Decisão tomada em 2026-08-04: alternativa A, contra a recomendação.** O termo do
sistema medido passa a ser `system under test`, e `Control Plane` deixa de ser o nome
dele. A escolha é legítima e o custo dela é o que a própria alternativa A nomeia: as
citações por linha continuam válidas, e os textos que elas apontam continuam dizendo
`Control Plane`.

**O alcance medido em 2026-08-04.** A contagem de ocorrências, por leitura direta:

| Onde                                    | Editável? | Ocorrências |
|-----------------------------------------|-----------|-------------|
| ADR-0001, ADR-0002, ADR-0006, ADR-0008  | não       | 18          |
| `plano-do-laboratorio.md`               | sim       | 4           |
| `AGENTS.md` da raiz                     | sim       | 2           |
| dois Feature Cards e um Example Mapping | sim       | 3           |
| nove documentos de `architecture/`      | sim       | 69          |
| este glossário                          | sim       | 17          |

**São quatro ADRs, e não cinco.** O enunciado da alternativa A dizia "cinco ADRs
aceitos". A contagem verificada é quatro: ADR-0001, ADR-0002, ADR-0006 e ADR-0008. O
ADR-0005 usa apenas `Lab Plane`.

**`Lab Plane` NÃO acompanha a renomeação**, decidido em 2026-08-04. O nome nunca
carregou a palavra ambígua `control`, e renomeá-lo seria mudança estética sobre cinco
ADRs aceitos. O par deixa de ser simétrico de propósito: `system under test` de um lado,
`Lab Plane` do outro. Um leitor de diagrama isolado descobre o motivo na entrada
`Lab Plane` deste glossário.

**A renomeação alcança todo o texto editável**, decidido em 2026-08-04. As 95 ocorrências
em 15 arquivos foram convertidas no mesmo turno. Três classes de ocorrência **não**
foram tocadas, e a distinção é o que separa renomear de falsificar:

| O que não mudou                                   | Por quê                                             |
|---------------------------------------------------|-----------------------------------------------------|
| as 18 ocorrências nos ADRs 0001, 0002, 0006, 0008 | ADR aceito não tem o corpo editado                  |
| a citação literal do ADR-0006, neste arquivo      | reescrever o que está entre aspas falsifica a fonte |
| o enunciado histórico desta seção `D-DOM-02`      | ele registra o problema como ele era                |

**O risco de desalinhamento, medido.** A contra-avaliação registra que edição em massa
desloca citações `arquivo:linha` em silêncio
([`arquivo/proposta-2026-08-03/contra-avaliacao.md`](arquivo/proposta-2026-08-03/contra-avaliacao.md),
seção `R12`). A conversão foi feita por substituição dentro da linha, sem inserir nem
remover linha nenhuma, e a contagem de linhas de cada arquivo foi conferida antes e
depois. Nenhuma citação externa se deslocou.

**Pergunta em aberto.** Os nomes de pacote propostos em
[`arquivo/proposta-2026-08-03/modulos-e-fronteiras.md`](arquivo/proposta-2026-08-03/modulos-e-fronteiras.md),
linhas 86 a 89 — `controlplane.dominio`, `controlplane.operacao`, `controlplane.estrategia`,
`controlplane.persistencia` — carregam o termo aposentado. Eles são proposta de uma
linha que continua aberta, e o ADR-0008 fixou só o pacote raiz. Renomeá-los é decisão da
arquitetura mínima, e não desta.

#### D-DOM-03 — Se `barrier` continua na linguagem

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção `D-DOM-03`, que
lá virou lápide. O texto é o de lá, com o nível de título rebaixado e os caminhos
relativos reescritos de `docs/` para `docs/adr/`; "a entrada dele acima" nomeia a entrada
`barrier` de [`../CONTEXT.md`](../CONTEXT.md). A **Pergunta em aberto** do fim já tem
questão própria, [`Q-0020`](../questions/Q-0020.md).

**O problema.** O ADR-0001 pressupõe `barreira` como termo (`:36`). O ADR-0003 retira o
estatuto: "a barreira deixa de ser um termo próprio: o que existe é a restrição de
precedência" (`:43-45`). O ADR-0004 mantém a palavra num título de seção, "A barreira é
o controle positivo" (`:247`). O plano e o briefing a usam sem qualificação.

**Alternativa A — aposentar a palavra.** A favor: é o que o ADR-0003 decidiu, e a
convenção do repositório exige um nome por conceito. Contra: quebra a leitura do
briefing e do cenário 25, que é o pedido original do usuário.

**Alternativa B — manter como sinônimo de `precedence constraint`.** A favor: nenhum
texto existente precisa ser relido. Contra: contraria uma decisão aceita, e o
repositório trata dois nomes para o mesmo conceito como defeito.

**Alternativa C — manter só em citação histórica.** A favor: preserva as referências ao
briefing sem introduzir sinônimo vivo. Contra: exige que quem escreve saiba distinguir
citação de uso, e a distinção não é verificável por teste.

**Recomendação.** Alternativa A, com a alternativa C como regra de citação.

**Se a escolha for outra.** Com a alternativa B, o glossário passa a ter dois nomes para
`precedence constraint`, e a convenção do `adr/README.md` deixa de valer.

**Decisão tomada em 2026-08-04: alternativa A, com a alternativa C como regra de
citação.** `barrier` está `aposentado`, e a entrada dele acima deixa de ser aplicação
antecipada da recomendação para ser registro da decisão. A palavra PODE aparecer em
citação de um ADR aceito, do plano ou do briefing, e NÃO DEVE aparecer como termo em
documento novo.

**A consequência executada no mesmo turno.**
[`arquivo/proposta-2026-08-03/mensageria.md`](arquivo/proposta-2026-08-03/mensageria.md)
usava `barreira` como termo vivo e normativo em oito pontos, inclusive no enunciado e nas
três alternativas de `D-MSG-11`. A ressalva estava em
[`arquivo/proposta-2026-08-03/contra-avaliacao.md`](arquivo/proposta-2026-08-03/contra-avaliacao.md),
linhas 143 a 145. Aqueles pontos passaram a dizer `restrição de precedência`, e o mérito
de `D-MSG-11` não mudou: a colisão continua sendo entre o que o escalonador segura e o
relógio que o broker não deixa injetar.

**Pergunta em aberto.** A palavra sobrevive em doze outros arquivos editáveis, e a
decisão nomeou `mensageria.md` apenas. O plano do laboratório a usa 15 vezes; os Feature
Cards e os Example Mappings, 8; `arquitetura-alvo.md`, `contratos-de-api.md` e
`interface-web.md`, de uma a três cada. Parte é citação legítima — o plano cita o
briefing, e o card de `execucao-de-experimento` cita o ADR-0001. Parte é termo vivo,
como em `arquivo/proposta-2026-08-03/arquitetura-alvo.md:390` e
`arquivo/proposta-2026-08-03/modulos-e-fronteiras.md:207`. Separar as duas exige leitura
caso a caso, e não foi feita.

#### D-DOM-04 — Como nomear os dois sentidos de `strategy`

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção `D-DOM-04`, que
lá virou lápide. O texto é o de lá, com o nível de título rebaixado; "a entrada
`strategy label`" é a de [`../CONTEXT.md`](../CONTEXT.md).

**O problema.** O ADR-0006 nomeia a colisão e a deixa aberta: "Duas coisas têm o mesmo
nome. No Control Plane, a estratégia é a composição de passos de `increment` [...] No
Lab Plane, é um rótulo na declaração do experimento" (`:30-36`).

**Alternativa A — dois nomes.** A favor: o Lab Plane fica proibido de ramificar por um
conceito que ele não tem, e a regra vira verificável. Contra: acrescenta um termo ao
glossário para descrever o mesmo dado visto de dois lados.

**Alternativa B — um nome com qualificador em cada uso.** A favor: nenhum termo novo.
Contra: o qualificador some na primeira frase que alguém escreve com pressa, e a
proibição do ADR-0006 depende exatamente dessa distinção.

**Alternativa C — manter a ambiguidade.** A favor: é o estado atual, e o ADR-0006
funciona assim. Contra: a regra "nenhum componente do Lab Plane inspeciona o rótulo" é
difícil de testar quando o rótulo e a implementação partilham o nome.

**Recomendação.** Alternativa A: `strategy` para a composição de passos, `strategy
label` para o dado de configuração.

**Se a escolha for outra.** Com a alternativa C, a guarda que impede o Lab Plane de
ramificar precisa nomear classes, e não conceitos.

**Decisão tomada em 2026-08-04: alternativa A.** `strategy` nomeia a composição de
passos do sistema medido; `strategy label` nomeia o dado opaco de configuração que o Lab
Plane carrega. A entrada `strategy label` deixa de ser `proposto` e passa a
`estabelecido`.

**O que a escolha torna verificável.** A proibição do ADR-0006 — nenhum componente do Lab
Plane inspeciona o rótulo — vira uma regra sobre tipos, e não sobre intenção. Um
componente do Lab Plane que receba `strategy` em vez de `strategy label` é um defeito
que a compilação ou uma guarda ArchUnit consegue apontar. Qual das duas a impõe é
decisão da arquitetura mínima, em `D-ARQ-07`.

### Bloco 5 — etapa 4 e adiante, sem gatilho disparado hoje

| ID         | Decisão                                      | Etapa | Recomendação da proposta                 |
|------------|----------------------------------------------|-------|------------------------------------------|
| `D-ARQ-01` | seguir o gatilho ou antecipar serviços       | 4     | seguir o gatilho                         |
| `D-ARQ-03` | onde o Lab Plane vive com dois processos     | 4     | decidir quando a etapa 4 tiver gatilho   |
| `D-ARQ-11` | PostgreSQL dedicado ou compartilhado         | 0     | dedicado                                 |
| `D-ARQ-13` | experimento destrutivo sob `selfHeal`        | 6     | matar a operação, preservando o processo |
| `D-ARQ-10` | Toxiproxy                                    | —     | emendar a ADR 0017 e retirar             |
| `D-DAT-06` | onde o log durável vive                      | 6     | instância separada da medida             |
| `D-DAT-10` | o que do log entra no Git                    | 6     | relatório mais eventos restritos         |
| `D-DAT-11` | instância e `wal_level` se o CDC entrar      | —     | dedicada                                 |
| `D-UI-05`  | onde vive o desenho pedagógico               | 1     | só no controle positivo                  |
| `D-UI-13`  | como o relatório chega a `docs/experiments/` | 1     | download e commit por pessoa             |

`D-ARQ-01` é a decisão que responde diretamente à instrução de usar
microsserviços: a proposta recomenda **seguir o gatilho**, isto é, começar com um
artefato e decompor quando o experimento `JVM_LOCK` ficar vermelho com duas
instâncias. Aprovar o contrário é legítimo e tem custo nomeado no documento.

**`D-ARQ-01` está fechada, contra a recomendação**, pelo
[ADR-0008](0008-os-dois-planos-em-processos-separados.md). A decomposição deixou
de esperar o gatilho da etapa 4: os dois planos rodam em processos separados desde o dia
zero. `D-ARQ-03` continua aberta e muda de sentido — ela deixa de perguntar onde o Lab
Plane vive quando existirem dois processos e passa a perguntar o que muda quando o
system under test ganhar a segunda instância.

### Bloco 6 — mensageria, etapa 5 e adiante

Nenhuma destas tem gatilho disparado hoje. Elas existem para que a etapa 5 não
comece sem desenho, e **nenhuma delas deve ser construída antes do gatilho**.

| ID         | Decisão                                      | Recomendação da proposta                    |
|------------|----------------------------------------------|---------------------------------------------|
| `D-MSG-01` | gatilho concreto que libera o RabbitMQ       | broker real, pelo mecanismo da reentrega    |
| `D-MSG-02` | como uma entrega duplicada é contada         | contagem nova de comandos distintos aceitos |
| `D-MSG-03` | quem carimba os atributos de extensão        | o runtime, na fronteira                     |
| `D-MSG-04` | modo do binding CloudEvents e versão do AMQP | binário sobre 0-9-1, mapeamento declarado   |
| `D-MSG-05` | que recursos do broker ficam desligados      | nenhum DLX e nenhum limite até a etapa 8    |
| `D-MSG-06` | confirmação de publicador                    | ligada, com braço de comparação desligado   |
| `D-MSG-07` | se o broker é fonte legítima do oráculo      | é fonte só depois da quiescência            |
| `D-MSG-08` | ciclo de vida de uma reentrega               | execução nova, com ADR novo sobre o log     |
| `D-MSG-09` | quem cria e destrói a topologia              | por execução                                |
| `D-MSG-10` | se o CDC com Debezium entra                  | **não entra**; gatilhos registrados         |
| `D-MSG-11` | barreira contra o limite de confirmação      | declarar o limite por execução e reportá-lo |

`D-MSG-05` é a que mais contraria a intuição: a proposta recomenda **desligar**
DLX e limite de entregas até a etapa 8, porque com eles ligados os cenários 18 e
19 não têm o que mostrar. É a regra pedagógica aplicada à configuração do broker.

`D-MSG-10` é a resposta à instrução sobre Debezium. O argumento decisivo não é de
custo: o CDC **apaga os pontos `BEFORE_PUBLISH` e `AFTER_PUBLISH` do ADR-0001**,
porque sem passo `PUBLISH` na operação a etapa 6 perde o gatilho que o plano lhe
dá (`../plano-do-laboratorio.md:609`). Os dois gatilhos que criariam o CDC estão
registrados em [`arquivo/proposta-2026-08-03/mensageria.md`](arquivo/proposta-2026-08-03/mensageria.md).

### As duas linhas sem bloco, classificadas em 2026-08-05

`D-ARQ-02` e `D-DOM-11` têm seção própria no documento-fonte e não apareciam em bloco
nenhum: é a diferença entre 64 e 66 que a decisão `B-5` fechou. **As duas continuam
abertas** — `B-5` classificou, e não decidiu.

| ID         | Decisão                               | Assunto                     | Onde                                                                                                                                                          |
|------------|---------------------------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `D-ARQ-02` | onde a interface web é construída     | Entrega contínua no homelab | [`arquivo/proposta-2026-08-03/arquitetura-alvo.md`](arquivo/proposta-2026-08-03/arquitetura-alvo.md#d-arq-02--onde-a-interface-web-é-construída-e-empacotada) |
| `D-DOM-11` | se o escalonamento é contexto próprio | Bloco 4, vocabulário        | [`arquivo/proposta-2026-08-03/modelo-de-dominio.md`](arquivo/proposta-2026-08-03/modelo-de-dominio.md#d-dom-11--se-o-escalonamento-é-contexto-próprio)        |

`D-ARQ-02` entrou em "Entrega contínua no homelab" porque fixa o `Dockerfile` e o número
de imagens do dia zero. `D-DOM-11` entrou no Bloco 4 porque ela nomeia um contexto de
vocabulário: `scheduling` é um dos seis contextos propostos, listados abaixo em
[Os contextos propostos](#os-contextos-propostos). **A justificativa mudou de evidência
em 2026-08-07, e não de conclusão**: até aquela data ela dizia que
[`../CONTEXT.md`](../CONTEXT.md) carregava o termo `scheduling` como `proposto` por
`D-DOM-11`, e o termo saiu do glossário junto com os outros cinco contextos. A
classificação da linha não muda, e ela continua aberta.

### Os contextos propostos

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção
`### Os contextos propostos`, que lá virou lápide. O texto é o de lá, com os caminhos
relativos reescritos de `docs/` para `docs/adr/`; "nesta proposta" nomeia a proposta de
vocabulário do glossário. **Nenhum dos seis tem decisão**, e absorver o texto não fecha
linha nenhuma. A entrada `observed invariant`, que vivia sob o mesmo título, **ficou** no
glossário: ela é termo, e não contexto.

Os seis nomes abaixo nascem nesta proposta e nomeiam bounded contexts, não módulos nem
processos. O desenho está em
[`arquivo/proposta-2026-08-03/modelo-de-dominio.md`](arquivo/proposta-2026-08-03/modelo-de-dominio.md).

**measured domain** — `proposto` (`D-DOM-07`)
O contexto do system under test: `Resource`, `Allocation`, `increment`, `allocate` e as
estratégias. Ele não conhece as palavras experimento, veredito nem coincidência.

**execution runtime** — `proposto` (`D-DOM-12`)
O contexto que constrói e executa as sequências de passos, cria o escopo de execução e
emite observações.

**scheduling** — `proposto` (`D-DOM-11`)
O contexto que declara e executa o agendamento: papel, carga, restrição de precedência,
encontro, chegada, travessia, término e desistência.

**observation record** — `proposto` (`D-DOM-10`)
O contexto do log e da timeline. Ele adota o vocabulário do runtime e do escalonamento
sem acrescentar significado.

**diagnosis** — `proposto` (`D-DOM-08`)
O contexto dos oráculos, das contagens, da janela de exposição, das coincidências e da
classificação do zero.

**experiment definition** — `proposto` (`D-DOM-09`), sem dono decidido
O contexto que declara o que uma execução roda antes de rodar. A decisão está na fila,
posição 8.

**Pergunta em aberto: dois dos seis identificadores não batem com o documento-fonte.** A
lista acima dá `D-DOM-07` a `measured domain` e `D-DOM-12` a `execution runtime`, e
[`arquivo/proposta-2026-08-03/modelo-de-dominio.md`](arquivo/proposta-2026-08-03/modelo-de-dominio.md)
enuncia `D-DOM-07` como "`Allocation` é agregado próprio ou membro de `Resource`" e
`D-DOM-12` como "Se a injeção de falha é contexto próprio" — que é um contexto sem nome
nesta lista. Os outros quatro correspondem. Qual das duas atribuições vale **não foi
decidido**, e este registro não a decide.

### O agrupamento por assunto

A tabela abaixo agrupa as linhas por assunto, e não por bloco. Ela existe porque os três
primeiros assuntos vinham colados numa linha só da fila derivada do plano: a posição 10.

| Assunto                                        | Linhas                                                                                          |
|------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Experimento: definição, semente, ciclo de vida | Bloco 3, mais `D-DAT-05`, `D-UI-08` e `D-UI-10`                                                 |
| Formatos de veredito                           | `D-DOM-05` e `D-DOM-16`                                                                         |
| A forma do artefato compilável                 | `D-ARQ-05`, `D-ARQ-06`, `D-ARQ-04`                                                              |
| A guarda executável das três regras            | `D-ARQ-07`, `D-ARQ-08`, `D-ARQ-09`, `D-DOM-15`                                                  |
| O esquema e a primeira migração                | `D-DAT-01` a `D-DAT-04`, `D-DAT-08`, `D-DAT-09`, `D-DOM-07`, `D-DOM-08`, `D-DOM-13`, `D-DOM-14` |
| Entrega contínua no homelab                    | `D-ARQ-12`, `D-ARQ-14`, `D-ARQ-15`, `D-ARQ-10`, `D-ARQ-11`, `D-ARQ-13`, `D-ARQ-02`              |
| Vocabulário                                    | Bloco 4, mais `D-DOM-11`, com destino em [`../CONTEXT.md`](../CONTEXT.md)                       |
| Mensageria, sem gatilho hoje                   | Bloco 6                                                                                         |
| Interface web                                  | `D-UI-02` a `D-UI-13`, menos as que o Bloco 3 absorve                                           |

## A ordem da arquitetura mínima e da entrega contínua está sob tensão

O laboratório é entregue no cluster do
[`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure), e a
exigência é que um serviço **nasça já entregando** — pipeline e CI/CD no mesmo commit
que cria o módulo, não retrofitados depois.

Isso não move o passo: o formato dele não afeta o que o pipeline empacota. Mas move a
arquitetura mínima e a entrega contínua para **junto do primeiro módulo compilável**, e
as decisões entre o domínio mínimo e os vereditos deixam de ser pré-requisito de
escrever código de esqueleto. O `Dockerfile` e o `deploy/kustomization.yaml` fixam o
número de módulos e a forma do artefato — que é o conteúdo da arquitetura mínima.

A entrega contínua tem uma particularidade que nenhuma outra tem: **parte dela já foi
tomada fora deste repositório.** A ADR 0017 do homelab, aceita em 2026-07-26, escolheu
Gradle, Toxiproxy e "microsserviços JVM" para este laboratório, dois dias antes do
replanejamento que descartou a arquitetura de serviços. Ratificar ou emendar é decisão
consciente e explícita. O inventário completo do que sobrevive e do que colide está em
[`../plano-do-laboratorio.md`](../plano-do-laboratorio.md), seção 12.

## A5 — a sigla `SUT` no código, decidida em 2026-08-05

**Trazido de [`../CONTEXT.md`](../CONTEXT.md) em 2026-08-07**, da seção
[`## A sigla SUT no código, decidida em 2026-08-05`](../CONTEXT.md#a-sigla-sut-no-código-decidida-em-2026-08-05).
**A regra ficou lá**, porque o
[ADR-0009](0009-a-classificacao-do-dual-write-e-a-regiao-de-pacote.md) aponta para o
glossário como fonte dela: em prosa, `system under test` por extenso; em identificador de
código, `sut`. O que veio para cá é o que a fila é dona — a **justificativa** da separação
e as **alternativas descartadas**. "Esta seção", "o glossário" e "este glossário" abaixo
nomeiam [`../CONTEXT.md`](../CONTEXT.md).

**Por que a separação precisou ser declarada.** A escolha do pacote se justifica dizendo
que o glossário já define o termo por extenso, enquanto a entrada `system under test`
lista `SUT` sob `_Evite_`, "por ser sigla sem expansão". Sem esta seção, o ADR que fixa
o pacote e o glossário nascem se contradizendo — e a contradição estaria dentro de um ADR
aceito, onde ninguém pode corrigi-la.

Descartadas: rever o nome do pacote, por reabrir uma decisão do dia anterior e trazer de
volta três alternativas já descartadas; e registrar como pergunta em aberto, por fazer o
ADR nascer carregando contradição conhecida com este glossário.

**Uma premissa do parágrafo acima caiu em 2026-08-07, e a decisão não.** "Onde ninguém
pode corrigi-la" valia enquanto o corpo de um ADR aceito era imutável; hoje um erro
material de texto é corrigível por patch, pela decisão registrada em
[A imutabilidade do corpo de um ADR aceito, revogada em 2026-08-07](#a-imutabilidade-do-corpo-de-um-adr-aceito-revogada-em-2026-08-07).
O que
`A5` escolheu continua valendo, e o texto de 2026-08-05 fica como está.

## O Lote E, enumerado em 2026-08-06

Os Lotes A a D fecharam pendências de **processo**: onde a fila vive, quem aprova o quê,
como uma citação é escrita, o que acontece com a rodada de arquitetura arquivada. Nenhum
deles destrava uma linha de código. **Este destrava, e é o único que destrava.**

O Lote E é a interseção de três coisas que a fila tinha separadas: a posição 10
(arquitetura mínima), a posição 11 (entrega contínua) e o Bloco 1 (esquema e primeira
migração). A exigência de nascer entregando as junta — o `Dockerfile` e o
`deploy/kustomization.yaml` fixam a forma do artefato, e a forma do artefato **é** o
conteúdo da arquitetura mínima.

### Os dois grupos, e a ordem entre eles

O grupo I produz um repositório que compila, empacota e é reconciliado pelo ArgoCD, com
zero regra de negócio dentro. O grupo II produz a primeira migração e as duas tabelas.
Os dois são sequenciais e não concorrentes: o grupo II precisa do build escolhido em
`E-1` para ter onde pôr o arquivo de migração.

```mermaid
flowchart LR
    I["grupo I<br/>o artefato que nasce entregando<br/>E-1 a E-6"]
    II["grupo II<br/>o esquema e a primeira migração<br/>E-7 a E-13"]
    C1["primeiro commit:<br/>compila, empacota,<br/>ArgoCD verde"]
    C2["segundo commit:<br/>resource e allocation,<br/>semeadura"]
    E1["E1 executável:<br/>o laboratório detecta"]
    I --> C1
    C1 --> II
    II --> C2
    C2 --> E1
```

**O grupo I não espera o grupo II, e essa é a única razão de existirem dois.** Um
repositório que compila e é reconciliado, sem tabela nenhuma, já apaga o
`ComparisonError` que o cluster reporta hoje e prova a esteira inteira. Adiar o primeiro
commit até o esquema estar decidido acopla a prova da esteira à discussão de chave
primária, que não tem relação nenhuma com ela.

### Grupo I — sem estas seis, não existe `pom.xml`

| ID    | Decisão                                          | Origem     | Recomendação da proposta              |
|-------|--------------------------------------------------|------------|---------------------------------------|
| `E-1` | build: Maven contra Gradle                       | `D-ARQ-12` | emendar a ADR 0017 para Maven         |
| `E-2` | quantos artefatos executáveis, e quantos módulos | `D-ARQ-05` | **vencida** pelo ADR-0008; ver abaixo |
| `E-3` | a forma do `deploy/` no primeiro commit          | `D-ARQ-15` | `deploy/` mínimo agora, uma réplica   |
| `E-4` | o que o pipeline executa                         | `D-ARQ-14` | só guardas e provas                   |
| `E-5` | PostgreSQL dedicado contra compartilhado         | `D-ARQ-11` | dedicado ao namespace do laboratório  |
| `E-6` | onde a interface web é construída                | `D-ARQ-02` | exportação estática na mesma imagem   |

As alternativas de cada uma, com o argumento a favor e contra, estão em
[`entrega-continua.md`](arquivo/proposta-2026-08-03/entrega-continua.md#d-arq-12--maven-contra-gradle)
para `E-1`, `E-3`, `E-4` e `E-5`, e em
[`arquitetura-alvo.md`](arquivo/proposta-2026-08-03/arquitetura-alvo.md#d-arq-02--onde-a-interface-web-é-construída-e-empacotada)
para `E-6`.

### Grupo II — sem estas sete, não existe a primeira migração

| ID     | Decisão                                          | Origem     | Recomendação da proposta              |
|--------|--------------------------------------------------|------------|---------------------------------------|
| `E-7`  | ferramenta de migração                           | `D-DAT-04` | Flyway com SQL versionado             |
| `E-8`  | tipo e derivação da identidade do recurso        | `D-DAT-01` | `bigint` ordinal da semente           |
| `E-9`  | chave estrangeira de `allocation.resource_id`    | `D-DAT-02` | sem FK no MVP                         |
| `E-10` | índice sobre `allocation(resource_id)`           | `D-DAT-03` | criar, e registrar o plano efetivo    |
| `E-11` | quem deriva a identidade a partir da semente     | `D-DOM-14` | a definição publica, o domínio deriva |
| `E-12` | a guarda do filtro por discriminador             | `P-DAT-12` | nenhuma; a escolha não foi feita      |
| `E-13` | quem gera o UUIDv7, contra as regras estruturais | `P-DAT-10` | nenhuma; a tensão não foi fechada     |

`E-7` a `E-11` estão em
[`modelo-de-dados.md`](arquivo/proposta-2026-08-03/modelo-de-dados.md#d-dat-04--ferramenta-de-migração)
e em
[`modelo-de-dominio.md`](arquivo/proposta-2026-08-03/modelo-de-dominio.md#d-dom-14--quem-é-dono-da-identidade-derivada-da-semente).
`E-12` e `E-13` estão na seção
[`Perguntas em aberto`](arquivo/proposta-2026-08-03/modelo-de-dados.md#perguntas-em-aberto)
do mesmo documento, e **nunca estiveram em bloco nenhum** — elas nasceram como
consequência de `D-DAT-05`, decidida em 2026-08-05, depois de os blocos existirem.

### Seis achados do levantamento, e nenhum deles é opinião

**A recomendação de `D-ARQ-12` ficou órfã.** Ela argumentava a favor de Maven porque
`D-ARQ-05` propunha a fronteira entre regiões como dependência declarada entre módulos
Maven. O [ADR-0008](0008-os-dois-planos-em-processos-separados.md) decidiu **contra**
essa proposta: a fronteira é o processo, e não o módulo. O apoio técnico da recomendação
caiu junto, e o que resta a favor de Maven é de governança — a escolha por Gradle na ADR
0017 foi feita como detalhe de contexto de uma decisão de CI/CD, sem debate aqui.

**A recomendação de `D-ARQ-15` está vencida na letra.** Ela diz `Deployment` de **uma**
réplica, e foi escrita em 2026-08-03. O ADR-0008 é de 2026-08-04 e põe os dois planos em
processos separados — o `deploy/` nasce com **dois** `Deployment`, o que o próprio ADR
registra nas consequências. A escolha entre as três alternativas não muda; o manifesto
que a alternativa 1 descreve muda.

**`D-ARQ-05` já foi respondida para o mecanismo, e não para a contagem.** O ADR-0008
fixou a fronteira (processo) e as quatro regiões de pacote. Ele **não** fixou quantos
módulos de build existem nem quantos artefatos executáveis são publicados. Dois
processos exigem no mínimo dois executáveis; se `shared` é um módulo próprio, ou se os
quatro pacotes vivem em dois módulos, continua aberto. É `E-2`, e ela é a linha nova
deste lote.

**O argumento contra `bigint` em `D-DAT-01` caiu.** Ele era a colisão entre duas
execuções da mesma semente. `D-DAT-05` pôs um discriminador UUIDv7 de execução na chave
primária das duas tabelas, e a colisão deixou de existir — o próprio texto da decisão
registra que `D-DAT-01` permanece, com o discriminador como segunda coluna da chave e
não como substituição. `E-8` é hoje mais barata do que era quando foi enunciada.

**`D-DOM-13` é subsumida por `E-7`.** Ela pergunta se o Shared Kernel entre os dois
planos ganha contrato verificável, e recomenda que sim, deixando a forma "para quem
decide o esquema". Escolher uma ferramenta de migração com SQL versionado **é** essa
forma: o arquivo de migração passa a ser o contrato, e o Markdown não pode repeti-lo. A
linha fecha quando `E-7` fechar, sem decisão própria.

**`P-DAT-12` é o item mais perigoso do lote, e ele não estava em lista nenhuma.** Sem
reset, uma consulta que esqueça o filtro por discriminador soma linhas de execuções
anteriores ao `value_final` do oráculo exato, e o veredito sai errado **sem sintoma**.
Com `TRUNCATE` o mesmo esquecimento era inofensivo, porque não havia outra execução no
banco. A decisão de 2026-08-05 trocou dois riscos ruidosos por um silencioso, e nada
hoje obriga o filtro.

### O que este lote NÃO inclui, de propósito

- **As guardas executáveis** de [`Q-0002-1`](../questions/Q-0002-1.md) — `D-ARQ-07`,
  `D-ARQ-08` e `D-ARQ-09`. Elas pertencem ao Bloco 2, e nenhuma linha de código as
  espera: uma regra sem código para vigiar não tem o que verificar.
- **O modelo de thread do worker** (`D-ARQ-04`) e **o nível de isolamento**
  (`D-DAT-08`), que o E1 exige e o esqueleto não.
- **As dezenove linhas de interface web** do Bloco 2, menos `E-6`, que entra só porque
  fixa o número de imagens do `Dockerfile`.

### As decisões do grupo I, em 2026-08-06

| ID    | Escolha                                                          | Seguiu a recomendação? |
|-------|------------------------------------------------------------------|------------------------|
| `E-1` | Maven, emendando a ADR 0017 do homelab                           | sim                    |
| `E-2` | três módulos e dois executáveis, com o nome corrigido para `sut` | parcialmente           |
| `E-3` | **adiada**, por escolha explícita                                | —                      |
| `E-5` | PostgreSQL compartilhado do homelab, com schema por aplicação    | **não**                |
| `E-7` | Flyway, fechada por consequência de `E-5`                        | sim                    |

**`E-1` — Maven.** A emenda à ADR 0017 do `homelab-infrastructure` é custo aceito, e ela
é o único item deste lote com efeito fora deste repositório. `Q-INT-4` fecha com ela.

**`E-2` — o nome `control-plane` estava vencido, e a pergunta o repetiu.** A
[emenda do ADR-0009](0009-a-classificacao-do-dual-write-e-a-regiao-de-pacote.md) trocou
a região `dev.da0hn.lab.controlplane` por `dev.da0hn.lab.sut`, e `D-DOM-02` aposentou
`Control Plane` da linguagem. O módulo é `sut`, e não `control-plane`. A sigla é
permitida em identificador de código pela decisão `A5`, registrada em
[`../CONTEXT.md`](../CONTEXT.md#a-sigla-sut-no-código-decidida-em-2026-08-05) — em prosa
continua `system under test` por extenso.

**`E-3` — adiada.** O `ComparisonError` no ArgoCD permanece, e a exigência da ADR 0017
de nascer entregando fica pendente junto. A linha continua aberta nesta fila; nada mais
neste lote depende dela, porque o build e o esquema não leem o `deploy/`.

### `E-5`, decidida contra a recomendação, e o que ela arrasta

A escolha é a alternativa 2 de `D-ARQ-11`: **o PostgreSQL que o homelab já opera na
Camada 6**, com desenvolvimento local num contêiner. **Cada aplicação aplica a própria
migração, no próprio schema.**

```mermaid
flowchart TB
    subgraph HL["homelab, Camada 6"]
        PG[("PostgreSQL compartilhado")]
        SL["schema do Lab Plane"]
        SS["schema do system under test"]
        PG --- SL
        PG --- SS
    end
    LP["lab-plane<br/>Flyway próprio"]
    ST["sut<br/>Flyway próprio"]
    LP -->|" migra "| SL
    ST -->|" migra "| SS
    LP -.->|" SELECT do oráculo,<br/>após a quiescência "| SS
```

**Ela fecha uma pergunta em aberto do ADR-0008.** Aquele ADR registra que a escolha
entre schema separado e dois bancos na mesma instância não fora feita, e que ela decide
permissão e espaço de nomes — nunca contaminação da medida, porque dois schemas do mesmo
cluster compartilham buffer pool, WAL, checkpointer, autovacuum e a tabela de locks. A
escolha é **schemas separados na mesma instância**.

**O custo nomeado pela própria alternativa passa a valer.** A contenção de conexões, de
CPU e de I/O atravessa a fronteira do banco lógico. O relatório de todo experimento
DEVE registrar que a medida foi feita num banco com vizinhos; sem isso, dois relatórios
com o mesmo veredito afirmam coisas diferentes. `Q-INT-3` fecha com a alternativa 2 e
esta obrigação.

**Ela dá forma concreta a `D-DOM-13`.** O Shared Kernel entre os planos deixa de ser
abstrato: o oráculo do Lab Plane lê as tabelas do schema do system under test, então o
papel do Lab Plane precisa de `USAGE` naquele schema e `SELECT` nas duas tabelas. A
fronteira que `Q-INT-5` pedia com forma verificável é uma concessão de permissão, e ela
é declarável e testável.

**Ela fecha `E-7` por consequência.** Migração por aplicação exige ferramenta de
migração, e a escolha é Flyway com SQL versionado — um arquivo por decisão aceita, nunca
editado depois de aplicado. Com isso `D-DOM-13` fecha junto: o arquivo de migração passa
a ser o contrato, e o Markdown não pode repeti-lo.

**Ela acrescenta um artefato que este repositório declara não ter.** Um contêiner local
significa `compose.yaml` versionado, e o [`../../AGENTS.md`](../../AGENTS.md) afirma hoje
que não existe `docker-compose.yml` nem comando de execução. A afirmação deixa de valer
no commit que criar o arquivo, e o texto muda junto.

**Pergunta em aberto: o Lab Plane não tem tabela nenhuma hoje.** O
[ADR-0007](0007-o-log-de-observacoes-forma-ordem-e-onde-vive.md) mantém o log em memória
e fixa a etapa 6 como o gatilho da persistência durável. Um Flyway no `lab-plane` no dia
zero teria zero migrações. Se o módulo já carrega a ferramenta com o diretório vazio, ou
se ela entra quando a primeira tabela existir, **não foi decidido**.

### A segunda rodada do grupo I mudou o desenho, em 2026-08-06

Três respostas fecharam linha, e duas abriram decisão que a fila mantinha adiada de
propósito. O registro é literal, antes de qualquer escolha nova.

| ID     | Escolha                                                        | Efeito                                 |
|--------|----------------------------------------------------------------|----------------------------------------|
| `E-4`  | o pipeline constrói a imagem e atualiza o `deploy/`; nada mais | contraria a alternativa 1 em parte     |
| `E-6`  | frontend em contêiner próprio, React                           | contraria a recomendação de `D-ARQ-02` |
| `E-14` | o `lab-plane` tem base própria desde o dia zero                | linha nova; antecipa `D-DAT-07`        |
| `E-15` | serviço próprio para o histórico de execução                   | linha nova, **em aberto**              |

**`E-4` — o experimento sai do pipeline, e a interface o aciona.** A parte que coincide
com a recomendação é a que importa: nenhum experimento roda no CI, então o veredito
probabilístico nunca pinta a build de vermelho. A parte nova é que guardas, provas e
testes **também** ficaram de fora do enunciado, e isso ainda não foi confirmado.

**`E-4` colide com o mecanismo da ADR 0017 do homelab.** Aquele documento fixa **ArgoCD
por polling**, com intervalo de cerca de três minutos: o workflow da `master` bumpa
a tag da imagem nos manifests Kustomize de `deploy/`, e o ArgoCD percebe sozinho. Não há
notificação do pipeline para o ArgoCD. "Avisar" exigiria webhook ou credencial de
escrita no painel do homelab — que é a mesma objeção com que `D-ARQ-13` descartou a
alternativa 3. O efeito prático é o mesmo, e o mecanismo é outro.

**`E-6` — três imagens no dia zero.** A escolha é a alternativa 2 de `D-ARQ-02`, contra
a recomendação. O custo nomeado passa a valer: o workflow ganha uma segunda matriz de
build, e a frase do plano segundo a qual a interface é servida pela própria aplicação
deixa de ser verdadeira. O framework de componentes fica em aberto — é `D-UI-03`, ainda
na fila.

**`E-14` — a base do `lab-plane` antecipa uma decisão do Bloco 3.** Guardar "as
configurações do experimento e as execuções solicitadas" põe a definição de experimento
numa tabela. `D-DAT-07` e `D-UI-01` perguntam exatamente onde essa definição vive, e a
recomendação das duas é **não decidir agora**, porque elas pertencem ao ADR de
Experiment — a posição 8 desta fila.

A tensão é real e está escrita desde o replanejamento: o
[`../../AGENTS.md`](../../AGENTS.md) diz que `experiments/` guarda definições, que
`docs/experiments/` guarda resultados, e que **os dois entram no Git** — juntos, o
histórico vira um caderno de laboratório. Uma definição que só existe numa linha de
tabela não é versionada, não aparece em diff e não sobrevive a um banco recriado.

```mermaid
flowchart LR
    G["experiments/<br/>definição versionada"]
    DB[("base do lab-plane<br/>execução solicitada")]
    UI["frontend<br/>o usuário aciona"]
    RUN["execução medida"]
    G -->|" importada "| DB
    UI -->|" solicita "| DB
    DB --> RUN
    RUN -->|" relatório "| G
```

O desenho acima é **uma** saída, e não a decidida: a definição continua versionada e é
importada; o banco guarda a **execução solicitada**, que é dado de operação e não de
especificação. Registrado como possibilidade, e a escolha pertence a `E-14`.

**`E-15` — o serviço de histórico não tem decisão, e o argumento a favor é forte.**
Ele é o mesmo do [ADR-0008](0008-os-dois-planos-em-processos-separados.md), aplicado um nível
abaixo: quem consulta não pode compartilhar destino com quem mede. Uma consulta da
interface sobre o histórico, dentro do processo que executa o experimento, perturba a
medida pelo mecanismo que aquele ADR nomeia — pausa de GC, pool esgotado, contenção.

O argumento contra também é do repositório: o
[ADR-0007](0007-o-log-de-observacoes-forma-ordem-e-onde-vive.md) mantém o log em memória
e fixa a **etapa 6** como o gatilho da persistência durável. Um serviço de histórico
hoje antecipa esse gatilho, e a regra estrutural exige nomear a limitação concreta que
a peça nova resolve antes de ela entrar.

### A terceira rodada, em 2026-08-06: duas linhas fechadas e a nomenclatura

| ID     | Escolha                                              | Seguiu a recomendação? |
|--------|------------------------------------------------------|------------------------|
| `E-4`  | build, testes e guardas; depois imagem e bump da tag | sim                    |
| `E-14` | a definição de experimento vive **só no banco**      | **não**                |

**`E-4` fecha.** O workflow compila, roda os testes com Testcontainers e as guardas
executáveis, publica a imagem no GHCR e bumpa a tag nos manifests de `deploy/`. Nenhum
experimento roda no CI. Uma imagem publicada é uma imagem que passou nas provas exigidas
por ADR aceito, e o veredito probabilístico nunca pinta a build de vermelho.

**`E-14` fecha contra a recomendação, e fecha três linhas de outros blocos junto.**
`D-DAT-07`, `D-UI-01` e a tensão 1 do plano perguntam a mesma coisa: onde vive a
definição de experimento. A resposta é a tabela, e o Designer na interface passa a ser
a fonte. As três saem da posição 8 desta fila.

**O que a escolha custa, nomeado.** O [`../../AGENTS.md`](../../AGENTS.md) afirma que
`experiments/` guarda definições, que `docs/experiments/` guarda resultados e que os
dois entram no Git — "juntos, o histórico vira um caderno de laboratório". A metade das
definições deixa de valer: elas não aparecem em diff, não são revisadas em PR e não
sobrevivem a um banco recriado. O texto muda no commit que criar a tabela.

**Um desenho em que o custo desaparece, registrado como possibilidade.** Se o relatório
de execução que vai para `docs/experiments/` **incorporar a definição completa que foi
usada**, o Git volta a guardar tudo que reproduz a execução — só que como parte do
resultado, e não como fonte. A definição deixa de ser artefato a sincronizar e passa a
ser um campo do relatório, o que elimina a pergunta de qual representação manda.
A escolha entre isto e um relatório que só cite a definição por identificador **não foi
feita**.

```mermaid
flowchart LR
    UI["frontend<br/>o usuário define"]
    DB[("base do lab-plane<br/>definição e execução")]
    RUN["execução medida"]
    REL["docs/experiments/<br/>relatório versionado"]
    UI --> DB
    DB --> RUN
    RUN --> REL
    DB -.->|" a definição usada,<br/>copiada para dentro "| REL
```

#### A nomenclatura dos módulos e dos serviços

Levantada na mesma rodada, e ela ainda não fechou.

**`system-under-test` como nome de módulo, `sut` como segmento de pacote.** A separação
já existe e é a decisão `A5`, em
[`../CONTEXT.md`](../CONTEXT.md#a-sigla-sut-no-código-decidida-em-2026-08-05): em prosa,
por extenso; em identificador de código, a sigla. Um nome de módulo e de imagem não é
nenhum dos dois — ele aparece em `deploy/`, no GHCR e no log do cluster, onde a sigla
não tem expansão à vista. O par por extenso no módulo e sigla no pacote é coerente com a
regra, e a fixa para um caso que ela não previa.

**`lab-auditory` não pode ser o nome, e o motivo é de idioma.** Em inglês `auditory` é
"auditivo", relativo à audição; "auditoria" é `audit`. Como todo identificador é escrito
em inglês pelo [ADR-0008](0008-os-dois-planos-em-processos-separados.md), o nome errado
ficaria em pacote, imagem e manifesto. As candidatas com o sentido pretendido são
`lab-audit`, `lab-journal`, `lab-ledger` e `lab-notebook` — as duas últimas alinhadas à
metáfora do caderno de laboratório que o repositório já usa.

**A contagem de serviços continua aberta**, e ela é o que resta de `E-2` e `E-15`.

### A quarta rodada, em 2026-08-06: uma contradição com ADR aceito

**Fechada em 2026-08-06.** `E-16` fixou o nome `lab-journal` e `E-17` tirou o caderno de
laboratório do Git — declarando **sem valor** a frase do `AGENTS.md` segundo a qual
`experiments/` e `docs/experiments/` entram no Git e "juntos, o histórico vira um caderno
de laboratório". As duas vivem em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-caderno-de-laboratório-sai-do-git).
`E-18` — um schema por serviço, sem acesso cruzado, contra a aresta `SELECT após a
quiescência` do ADR-0008 — vive em
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão).

### A quinta rodada, em 2026-08-06: o CDC, conferido

**Fechada em 2026-08-06.** `E-15` fechou em **quatro serviços no dia zero** e `E-19`
mandou as observações de passo atravessarem para o `lab-journal` ao vivo, evento por
evento; `E-20` nasceu aqui e fechou na rodada seguinte. A topologia vive em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#cinco-serviços-e-o-quatro-do-agentsmd-deixa-de-valer)
e a emissão ao vivo em
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão).

#### `E-19` — ao vivo, e a tensão com o ADR-0008

**Fechada em 2026-08-06.** As observações de passo atravessam para o `lab-journal`
**evento por evento**, e cada travessia entra na janela medida — o ADR-0008 já registrava
que a latência de rede entra na medida de todo experimento, e o E1 emite entre 900 e 1500
observações por execução. A decisão vive em
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão), e a
saída não escolhida — buffer local com remetente próprio — continua aberta em
[`E-36`](#e-36--a-emissão-ao-vivo-entra-na-janela-que-o-experimento-mede).

### A sexta rodada, em 2026-08-06: o CDC vira fonte do veredito

**Fechada em 2026-08-06.** `E-18` pôs o CDC como **fonte do veredito**, sem `SELECT`
cruzado, e `E-20` fechou **sem BFF** — o frontend manda comando ao `lab-plane` e lê
histórico e streaming do `lab-journal`. A primeira vive em
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão), a segunda em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#comando-no-lab-plane-leitura-no-lab-journal-sem-bff).

#### O que `E-18` preserva, e o que ela desmonta

**Fechada em 2026-08-06.** Ela preserva a regra de schema sem exceção — uma conexão de
replicação lógica consome o WAL e não faz `SELECT` em tabela alheia —, desmonta a
detecção cruzada e o rótulo `fontes divergentes`, e **tira o CDC da etapa 5 para o dia
zero**. O racional inteiro vive em
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#consequências).

### O esqueleto do grupo I, escrito em 2026-08-06

O primeiro código do repositório entrou no mesmo dia em que o grupo I fechou. Ele
compila, empacota, sobe contra PostgreSQL real e **não implementa nada**.

| Decisão | Como ela virou arquivo                                           |
|---------|------------------------------------------------------------------|
| `E-1`   | `pom.xml` reactor, Java 25, Spring Boot 4.1.0                    |
| `E-2`   | `shared`, `lab-plane`, `lab-journal`, `system-under-test`        |
| `E-4`   | `.github/workflows/build.yml`: verify, depois imagem no GHCR     |
| `E-5`   | `compose.yaml` e `local/postgres-init.sql`, um papel por serviço |
| `E-6`   | `frontend/`, React 19 com `Dockerfile` e nginx próprios          |
| `E-7`   | Flyway configurado nos três, com `create-schemas`                |
| `E-18`  | `ALTER ROLE lab_plane REPLICATION`, e nenhum `GRANT` cruzado     |
| `E-20`  | dois caminhos no `nginx.conf` e no proxy do Vite                 |

#### Cinco coisas que escrever o código decidiu, e que ninguém tinha perguntado

**A região `application` do ADR-0008 vira três folhas.** Aquele ADR nomeia
`dev.da0hn.lab.application` como a região de composição e ponto de entrada. Com três
executáveis, um pacote único ali ficaria dividido entre três artefatos — split package,
que compila e envenena qualquer análise por pacote. Cada bootstrap ganhou folha própria:
`application.labplane`, `application.journal` e `application.sut`, com
`scanBasePackages` declarado. **A emenda ao ADR-0008 precisa cobrir isto**, junto da
região `journal`, que também não existe lá.

**A direção proibida do ADR-0008 deixou de precisar de guarda.** O `system-under-test`
não declara dependência do `lab-plane`, então a chamada proibida é erro de compilação. O
ArchUnit foi **retirado** dos `pom.xml` por isso: uma dependência declarada sem uso é
exatamente o que a regra estrutural do repositório proíbe. Ele volta quando `D-ARQ-07`
decidir o que cada classe de regra verifica.

**O `public` foi revogado no banco local.** Um schema comum a todos os papéis é o
caminho por onde `E-18` vazaria sem ninguém notar: bastaria uma tabela criada sem
qualificar o schema. `REVOKE ALL ON SCHEMA public FROM PUBLIC` fecha isso.

**O SSE exige três diretivas no nginx.** Sem `proxy_buffering off`, o servidor acumula a
resposta e entrega o evento só quando o buffer enche — o que transforma "ao vivo" de
`E-19` em "em lote", sem erro nenhum aparecer. É a classe de defeito que o repositório
mais teme: o silencioso.

**O `lab-journal` já pode ter migração, e os outros dois não.** O
[ADR-0007](0007-o-log-de-observacoes-forma-ordem-e-onde-vive.md) já fixou a forma e a
ordem do log de observações, então a primeira migração do histórico não depende do grupo
II. As tabelas `resource` e `allocation` dependem, porque `E-8` a `E-13` continuam
abertas. Nenhuma migração entrou neste commit.

#### Cinco defeitos que o esqueleto teve, e o que cada um ensina

Nenhum deles apareceu como erro. Os cinco produziram **verde**, que é a forma de falha
que este repositório mais teme.

**A auto-configuração do Flyway saiu de `spring-boot-autoconfigure` no Spring Boot 4.**
Ela vive num módulo próprio, `spring-boot-flyway`. Sem ele, o `flyway-core` fica no
classpath, o contexto sobe, o health check responde `UP`, e **nenhuma migração roda**.

**O Flyway não cria schema quando não há migração a aplicar.** `create-schemas: true` é
condição, e não ordem: ele cria o schema antes de aplicar a primeira migração, e sem
nenhuma ele não faz nada. As três `V1` existem por isso, e criam apenas um
`COMMENT ON SCHEMA`.

**Os dois defeitos acima se somam num terceiro.** A fronteira de `E-18` ficava declarada
em `application.yml` e ausente no banco: os três serviços conectavam ao mesmo
`database`, nenhum schema existia, e nada os impedia de escrever no mesmo espaço de
nomes. A regra estava escrita e não estava valendo.

**O teste `contextLoads` não pega nada disso.** Ele prova que o Spring sobe, o que é
verdade mesmo com o Flyway inerte. Os testes passaram a consultar `pg_namespace` e
afirmar que o schema daquele processo existe — o que falha se qualquer um dos três
defeitos voltar.

**A tabela de controle do Flyway tem uma coluna `version`.** Uma guarda ingênua para a
proibição do ADR-0006 acusaria defeito na primeira execução. A verificação exclui
`flyway_schema_history`: a coluna pertence à ferramenta de migração, e não ao domínio
medido.

Um sexto, de ambiente e não de decisão: a imagem `postgres:18` mudou o ponto de
montagem para `/var/lib/postgresql`, porque os dados passaram a viver num subdiretório
por versão maior. Montar `/var/lib/postgresql/data` faz o contêiner recusar-se a subir —
este falhou ruidosamente, e por isso não está na lista acima.

#### O que o esqueleto prova, e o que ele não prova

Prova: os quatro artefatos constroem, os três serviços Java sobem contra PostgreSQL 18
real por Testcontainers, o Flyway cria o schema de cada um, e o `compose.yaml` levanta o
conjunto com `wal_level=logical`.

Não prova nada sobre consistência distribuída. Nenhum dos 42 fenômenos é reproduzível, o
oráculo não existe, e o CDC está provisionado mas não consumido.

### `E-21`: pular o build do módulo que não mudou, aberto em 2026-08-06

Metade deste assunto já fechou sem decisão, porque não havia alternativa a debater. O
[`Dockerfile`](../../Dockerfile) copiava os quatro `src/` numa camada só e construía o
reactor inteiro uma vez por imagem; como as três imagens Java partilham o arquivo, uma
mudança em qualquer módulo alterava o hash daquela camada nas três e invalidava o cache
de todas. O `cache-from: type=gha` do workflow existia e nunca era aproveitado entre
commits. Hoje `shared` é camada própria e cada imagem compila só o módulo pedido —
medido com Docker 29.5.3, tocar `lab-plane/src` deixa o build de `lab-journal` inteiro
em cache.

**O que sobra é decisão, e é isto: pular o job do módulo intocado.** Os quatro jobs da
matriz continuam rodando sempre. O do módulo que não mudou agora é barato, mas não é
grátis — ele resolve o cache, exporta um manifesto idêntico ao anterior e ocupa um
runner.

**O obstáculo não é o GitHub Actions, é a regra de tag.** A tag é o SHA do commit, e o
motivo está escrito no próprio workflow: uma tag móvel torna impossível dizer qual
imagem produziu um resultado de experimento, que é a propriedade que este repositório
existe para ter. Um job pulado deixa `ghcr.io/.../<módulo>:<sha>` sem existir, e todo
manifest que referencie o SHA do commit para os quatro serviços aponta para o vazio.

```mermaid
flowchart TD
    C["commit toca só lab-plane"]
    C --> B["build de lab-plane<br/>publica :sha-novo"]
    C --> P{"pular os outros três?"}
    P -->|" sim, sem mais nada "| X["lab-journal:sha-novo<br/>NÃO EXISTE"]
    P -->|" sim, com retag "| R["imagetools create<br/>copia o manifesto anterior"]
    P -->|" não, como hoje "| T["build cacheado<br/>publica :sha-novo"]
    X --> F["deploy/ aponta para o vazio"]
```

| Alternativa                        | A favor                                          | Contra                                            |
|------------------------------------|--------------------------------------------------|---------------------------------------------------|
| 1. matriz dinâmica com retag       | todo SHA continua tendo as quatro imagens        | achar o SHA anterior depende de retenção no GHCR  |
| 2. matriz dinâmica, tag por módulo | mais barato e mais honesto                       | transfere a complexidade inteira para `E-3`       |
| 3. não fazer nada                  | zero mecanismo novo; a regra de tag fica intacta | um job redundante por módulo intocado, por commit |

**A recomendação é a 3, e o motivo é que não há número.** Nenhum job de imagem completou
no GitHub até hoje, e o tempo de construção de uma imagem continua desconhecido.
Escolher entre 1 e 2 antes da primeira medição é optar pela complexidade no escuro. E a
alternativa 2 decide na prática a forma da tag, que é conteúdo de `E-3` — adiada por
escolha explícita na mesma data.

**Gatilho que reabre esta linha:** a primeira execução real do workflow produzir um
tempo de build, ou `E-3` fechar. O que vier primeiro.

**Por que ainda não há número, e o motivo não é deste repositório.** Em 2026-08-06 os
dois workflows passaram a executar — o `docs` fechou verde em 7s, e no `build` o job
`provas` obteve runner e `mvn verify` passou em 1m16s. Os quatro jobs `imagem`, que
rodam em paralelo depois dele, ficaram quinze minutos na fila e terminaram com
`The job was not acquired by Runner of type hosted even after multiple attempts`. Uma
reexecução passou mais de quarenta minutos sem sequer criar os jobs, e o cancelamento
foi recusado com `Cannot cancel a workflow re-run that has not yet queued` enquanto a
API do próprio run continuava a reportar `queued` — dois subsistemas do GitHub
discordando sobre o mesmo objeto. A causa é incidente de plataforma no GitHub Actions,
reportado em [`githubstatus.com`](https://www.githubstatus.com/) na mesma data. Nada
neste repositório o provoca e nada aqui o resolve; a medição espera o serviço
normalizar.

### O grupo II, reaberto em 2026-08-06: quatro achados antes de qualquer escolha

As seis linhas `E-8` a `E-13` foram enunciadas em 2026-08-03, e três decisões
posteriores mudaram o terreno delas sem que nenhuma fosse reescrita: `D-DAT-05` pôs um
discriminador de execução na chave primária das duas tabelas, `E-5` pôs um schema por
serviço, e `E-18` tirou o `SELECT` cruzado do oráculo e pôs o CDC no lugar. O que segue
é o efeito disso, registrado antes da rodada e **sem decidir nada**.

| Achado                                           | Linha atingida | Efeito                        |
|--------------------------------------------------|----------------|-------------------------------|
| a ordem das colunas da chave primária é ambígua  | linha nova     | `E-22`                        |
| Row Level Security deixou de alcançar o veredito | `E-12`         | uma das duas candidatas cai   |
| a chave estrangeira teria de ser composta        | `E-9`          | o argumento contra cresce     |
| o índice em debate não é sobre `(resource_id)`   | `E-10`         | enunciado corrigido, e barato |

#### `E-22` — a própria `D-DAT-05` diz duas coisas sobre a ordem da chave

A tabela da decisão diz que "a chave primária das duas tabelas passa a incluir a
execução". O diagrama da mesma seção rotula a tabela como "PK começa pelo
discriminador". As consequências dizem que "todo índice passa a começar pelo
discriminador" e, na frase seguinte, que "o discriminador é a **segunda** coluna da
chave". Começar e ser segundo não são compatíveis, e as três frases estão em
[`modelo-de-dados.md`](arquivo/proposta-2026-08-03/modelo-de-dados.md#d-dat-05--reset-entre-execuções).

A escolha não é cosmética, e o motivo é o mesmo pelo qual aquela decisão preferiu
UUIDv7 a UUIDv4. Com `(execution_id, id)`, o prefixo de instante do UUIDv7 é crescente
e toda inserção cai no fim da B-tree. Com `(id, execution_id)`, a coluna à esquerda é o
`bigint` derivado da semente — valores pequenos que **se repetem** a cada execução —, e
as inserções se espalham pelo índice inteiro. É exatamente a fragmentação dentro da
janela de medida que a decisão diz querer evitar.

```mermaid
flowchart TB
    subgraph A["(execution_id, id)"]
        A1["UUIDv7 à esquerda<br/>prefixo cresce no tempo"]
        A2["inserção no fim da B-tree"]
        A3["consulta por execução<br/>usa o prefixo"]
        A1 --> A2
        A1 --> A3
    end
    subgraph B["(id, execution_id)"]
        B1["bigint da semente à esquerda<br/>repete a cada execução"]
        B2["inserção espalhada<br/>fragmenta durante a medida"]
        B1 --> B2
    end
```

O acesso do `increment` conhece os dois valores e funciona em qualquer das duas ordens,
então nada quebra — o custo é só de desempenho, dentro da janela medida.

#### `E-9` — a chave estrangeira teria de ser composta

`D-DAT-02` pesou uma chave estrangeira simples, de `allocation.resource_id` para
`resource.id`. Com o discriminador na chave primária, `resource.id` sozinho deixa de ser
único, e a referência passa a ser `(resource_id, execution_id)` para `(id,
execution_id)` — o que exige a coluna do discriminador também em `allocation`, e ela já
está lá pela mesma decisão.

O argumento contra cresce em duas frentes. O lock `FOR KEY SHARE` que
[`D-DAT-02`](arquivo/proposta-2026-08-03/modelo-de-dados.md#d-dat-02--chave-estrangeira-de-allocationresource_id)
nomeia continua igual, e agora o vocabulário do Lab Plane — que `D-DAT-05` aceitou pôr
na chave do sistema medido — passa a aparecer também na restrição de integridade dele.

#### `E-10` — o índice em debate é `(execution_id, resource_id)`

[`D-DAT-03`](arquivo/proposta-2026-08-03/modelo-de-dados.md#d-dat-03--índice-sobre-allocationresource_id)
debate um índice sobre `allocation(resource_id)`. A consequência de `D-DAT-05` diz que
todo índice começa pelo discriminador, então o índice em debate é
`(execution_id, resource_id)`, e o enunciado de 2026-08-03 está vencido na letra.

**A decisão ficou mais barata do que era.** Sem o discriminador, o índice servia a uma
finalidade só, e discutível: aproximar o predicate lock do `SERIALIZABLE` do conflito
real. Com ele, o índice também é o que impede uma consulta por execução de varrer o
histórico inteiro — o crescimento monotônico que `P-DAT-11` aceitou sem particionamento
e sem retenção.

**O que não mudou:** a replicação lógica decodifica mudança de heap, e não de índice. O
índice não altera o que o oráculo de `E-18` enxerga. Ele altera o custo de escrita
dentro da janela medida, que é o argumento contra registrado em `D-DAT-03`.

Nenhum dos quatro é decisão. `E-22` é linha nova; os outros três levam `E-9`, `E-10` e
`E-12` à rodada com o enunciado corrigido.

### A primeira rodada do grupo II, em 2026-08-06

| ID     | Escolha                                                   | Seguiu a recomendação? |
|--------|-----------------------------------------------------------|------------------------|
| `E-8`  | `bigint` derivado da semente                              | sim                    |
| `E-9`  | sem chave estrangeira, com verificação de órfãs           | sim                    |
| `E-10` | índice `(execution_id, resource_id)`, com o plano efetivo | sim                    |
| `E-22` | chave primária `(execution_id, id)`, decidida duas vezes  | sim                    |

**`E-8` — `bigint`.** O único argumento contra era a colisão entre duas execuções da
mesma semente, e o discriminador de `D-DAT-05` o removeu. O custo já estava registrado
como consequência aceita no
[ADR-0002](0002-o-dominio-minimo-e-os-dois-oraculos.md): a geração de identidade sai do
banco, todo `INSERT` carrega a chave, e uma inserção manual em `psql` durante depuração
deixa de funcionar sem que alguém escolha um identificador.

#### `E-9` fecha a escolha e abre uma pendência que `E-18` criou

A escolha é **sem chave estrangeira**, e o motivo é o lock: um `INSERT` em `allocation`
com FK adquire `FOR KEY SHARE` na linha de `resource`, e ele conflita com o `FOR UPDATE`
da estratégia `PESSIMISTIC`. Um bloqueio vindo da restrição seria atribuído à estratégia,
e a comparação entre estratégias mediria o esquema em vez do fenômeno.

**A metade que não fecha é onde a verificação de órfãs vive.** A recomendação de
`D-DAT-02` a punha "no mesmo lugar em que o oráculo já lê o banco" — e esse lugar
**deixou de existir** em `E-18`. O Lab Plane não faz `SELECT` no schema do system under
test; ele consome o WAL. Verificar órfã a partir do stream exige reconstruir o conjunto
de `resource.id` existentes e cruzá-lo com os `INSERT` de `allocation`, que é derivar
estado a partir de eventos — o mesmo obstáculo que já deixou o oráculo de capacidade sem
fonte declarada nesta mesma fila.

```mermaid
flowchart TB
    E9["E-9: sem FK<br/>a integridade fica com o código"]
    V["quem verifica a órfã?"]
    A["SELECT do Lab Plane<br/>proibido por E-18"]
    B["reconstrução pelo stream<br/>é derivar estado de eventos"]
    C["semeadura correta por construção<br/>sem verificação nenhuma"]
    E9 --> V
    V -.-> A
    V -.-> B
    V -.-> C
```

A terceira saída é a única sem obstáculo declarado, e ela troca verificação por
confiança no código da semeadura. **Nenhuma das três foi escolhida.** A pendência fica
vizinha da fonte do oráculo de capacidade, e as duas provavelmente fecham juntas.

**`E-10` — o índice entra, e ele depende de `E-22`.** A obrigação que vem junto é a de
`D-DAT-03`: o plano de execução efetivo vai no relatório do braço `SERIALIZABLE`, sob
pena de o número não ser interpretável. O custo é escrita de índice a cada `INSERT` do
E5, dentro da janela medida. **Se `E-22` escolher `(execution_id, id)`**, a chave
primária de `allocation` já começa pelo discriminador e este índice é adicional; se
escolher `(id, execution_id)`, ele passa a ser o único caminho de acesso por execução.

#### `E-22` — as duas premissas que a rodada corrigiu

A pergunta que a linha recebeu foi se a ordem `(id, execution_id)` é o que permite uma
segunda execução, "já que o `id` é auto-incrementado". As duas metades são falsas, e a
segunda é a que importa.

**O `id` não é auto-incrementado, e não pode ser.** O
[ADR-0002](0002-o-dominio-minimo-e-os-dois-oraculos.md) determina que o identificador é
gerado no código do sistema medido a partir da semente, e que o esquema NÃO DEVE usar
`SERIAL`, `IDENTITY`, `nextval` nem valor padrão do banco. Duas execuções da mesma
semente produzem **os mesmos** identificadores, por exigência — e foi precisamente isso
que obrigou o discriminador a entrar na chave.

**A ordem das colunas não muda o que a chave permite.** `PRIMARY KEY (a, b)` e
`PRIMARY KEY (b, a)` impõem a mesma restrição: o **par** é único, e nenhuma das duas diz
nada sobre `a` ou `b` isoladamente. As duas ordens permitem a segunda execução
igualmente, e o que a permite é o discriminador **estar** na chave — decidido em
`D-DAT-05`, não nesta linha.

```mermaid
flowchart LR
    subgraph U["o que as duas ordens têm em comum"]
        U1["o par é único"]
        U2["a segunda execução cabe"]
    end
    subgraph D["o que a ordem decide"]
        D1["qual WHERE o índice serve"]
        D2["onde a inserção cai na B-tree"]
    end
```

`E-22` decide desempenho e caminho de acesso dentro da janela medida, e **não** decide
capacidade nenhuma do esquema.

#### `E-22` fecha em `(execution_id, id)`, e a linha foi decidida duas vezes

A primeira escolha foi `(id, execution_id)`, e ela caiu no mesmo dia. O percurso fica
registrado porque o que a inverteu foi uma correção de mérito, e não uma mudança de
gosto.

**O argumento que sustentava a primeira escolha estava inflado, e quem o inflou foi esta
fila.** Ele dizia que buscar "a mesma linha em **todas** as execuções" é operação central
do laboratório, porque comparar `NONE`, `PESSIMISTIC` e `OPTIMISTIC` é comparar a mesma
entidade lógica entre execuções. **Não é uma consulta.** O oráculo do
[ADR-0002](0002-o-dominio-minimo-e-os-dois-oraculos.md) calcula
`perdidas = commits − (value_final − value_inicial)` **dentro** de cada execução, e a
comparação entre estratégias acontece depois, sobre números já calculados, no relatório.
Nenhum caminho quente junta execuções numa consulta só; isso é inspeção manual em `psql`,
e ela pode pagar uma varredura.

| Consulta                            | Quem a faz                   | Frequência   |
|-------------------------------------|------------------------------|--------------|
| tudo de uma execução                | consumidor de CDC, histórico | todo momento |
| a linha 42000 de uma execução       | operação medida              | todo momento |
| a linha 42000 em todas as execuções | pessoa depurando em `psql`   | raro         |

A ordem escolhida põe as duas primeiras no prefixo do índice, e deixa a terceira pagar
varredura. A ordem descartada fazia o inverso — otimizava a rara e punha a frequente na
dependência de um índice secundário, sobre um histórico que nunca é apagado.

**O ganho de escrita vem junto.** O `execution_id` é um UUIDv7, cujo prefixo de instante
cresce, então toda inserção cai no fim da B-tree em vez de espalhada por ela. É a mesma
propriedade pela qual `D-DAT-05` preferiu UUIDv7 a UUIDv4, agora valendo também para a
chave primária. A pressão de `fillfactor` que a ordem descartada exigiria deixa de ser
questão, e `P-DAT-2` continua tratando só do autovacuum.

**O custo que passa a valer.** As linhas de uma mesma execução ficam fisicamente
adjacentes no índice, e workers concorrentes inserem na mesma página de folha. É
contenção de índice dentro da janela medida — ruído do instrumento, e não fenômeno
estudado. Ele não tem mitigação decidida, e é vizinho de `P-DAT-2` pelo mesmo motivo:
nenhuma política de página está declarada em documento nenhum.

**`E-10` permanece, e volta a ser aditivo.** Com o discriminador já no prefixo da chave
primária, o índice `(execution_id, resource_id)` deixa de ser o único caminho por
execução e volta ao papel que `D-DAT-03` lhe deu: aproximar o predicate lock do
`SERIALIZABLE` do conflito real. A obrigação de registrar o plano efetivo no relatório
continua.

**A contradição interna de `D-DAT-05` fica resolvida do outro lado.** A escolha ratifica
o diagrama — "PK começa pelo discriminador" — e a consequência de que "todo índice passa
a começar pelo discriminador". A frase vencida é "o discriminador é a segunda coluna da
chave", e ela fica registrada como tal aqui, sem editar o documento arquivado.

#### `E-23` — o nome da coluna do discriminador, aberto ao escrever o primeiro DDL

Com `E-8`, `E-9`, `E-10` e `E-22` fechadas, o `CREATE TABLE` das duas tabelas pode ser
escrito — e ele trava numa palavra. `D-DAT-05` decidiu que a coluna afirma "discriminador
de inquilino, com **nome genérico no sistema medido**", e deixou o nome concreto em
aberto de propósito: o sistema medido não sabe que o valor é uma execução de experimento,
e para ele aquilo é a partição lógica dos dados.

Chamá-la de `execution_id` nas tabelas do system under test contradiz a decisão na
palavra exata que ela escolheu evitar. **A ligação com o Lab Plane é justamente o que a
coluna não pode declarar**, porque declará-la põe vocabulário do instrumento dentro do
medido — o mesmo custo que `D-DAT-05` nomeou ao aceitar o discriminador na chave, e que
esta linha decide se paga inteiro ou pela metade.

```mermaid
flowchart LR
    LP["lab-plane<br/>sabe: é uma execução"]
    COL["a coluna nas duas tabelas<br/>do sistema medido"]
    SUT["system under test<br/>vê: uma partição de dados"]
    LP -->|" abre a execução com o valor "| COL
    COL --> SUT
    SUT -.->|" o nome não pode<br/>dizer 'execução' "| LP
```

As candidatas visíveis são `tenant_id`, `partition_id` e `run_id`. As duas primeiras
honram a decisão e custam um salto mental em toda consulta do Lab Plane; a terceira é
legível dos dois lados e é a que a decisão diz para não usar. **Nenhuma foi escolhida**,
e o `CREATE TABLE` não pode ser escrito antes disso.

#### `E-11` mudou de terreno: o instrumento já publica identidade no sistema medido

**Fechada em 2026-08-06.** A recomendação da proposta era o **domínio medido derivar o
identificador, ciente da semente**, e os três achados desta fila mostraram que ela perdeu
o apoio depois que `D-DAT-05` pôs o discriminador do Lab Plane na chave primária das
tabelas medidas. O racional vive em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#identidade-embutida-no-domínio-medido-ou-no-lab-plane).

### A segunda rodada do grupo II, em 2026-08-06

**Fechada em 2026-08-06 na parte da identidade.** `E-11` escolheu **onde a regra de
derivação mora** — um componente próprio, com contrato — e abriu `E-24` no mesmo ato; o
racional vive em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-componente-de-identidade).
`E-13` fechou por papel do valor, e as duas seções de `E-23` continuam abaixo por não
terem ADR que as carregue.

#### `E-11` fecha no componente próprio, e abre `E-24` no mesmo ato

**Fechada em 2026-08-06, contra a recomendação.** A escolha aceita o custo de **um
contexto inteiro por uma regra de uma linha**, em troca de a regra ficar isolada e com
contrato testável. O racional vive em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-componente-de-identidade).

#### `E-24` — a alternativa C isola a regra, e não decide quem a invoca

**Fechada em 2026-08-06.** `E-11` respondeu onde a regra mora, e não quem a chama; das
três formas, a de **serviço próprio é a única que dispensa escolher entre os dois
planos**, ao custo de uma chamada de rede. O racional vive em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-componente-de-identidade).

#### `E-13` fecha por papel do valor, e o `AGENTS.md` muda no mesmo commit

**Fechada em 2026-08-06, e ela não gerou ADR.** As regras de aleatoriedade e de relógio
alcançam todo valor que entra em veredito, em escalonamento ou em identidade derivada da
semente, indiferentemente do plano que o produz — e o discriminador de execução não entra
em nenhum dos três papeis. A regra e o porquê dela vivem no
[`AGENTS.md` da raiz](../../AGENTS.md#regras-estruturais-que-valem-sempre), alterado no
mesmo commit, que passa a ser o dono desta decisão.

#### `E-23` ganhou uma quarta candidata: nome diferente de cada lado

A pergunta é de 2026-08-06, e ela desfaz um pressuposto que as três candidatas anteriores
carregavam sem enunciar — o de que a coluna precisa ter **um** nome. Ela não precisa.
Pela decisão `E-18` cada serviço tem seu próprio schema e nenhum lê o do outro, então
nada obriga que a coluna do sistema medido e a das tabelas do Lab Plane se chamem igual.

```mermaid
flowchart LR
    LPT["tabelas do lab-plane<br/>execution_id"]
    SUT["tabelas medidas<br/>nome genérico"]
    CDC["o stream de CDC<br/>traz o nome do medido"]
    LPT -->|" abre a execução "| SUT
    SUT --> CDC
    CDC -->|" o consumidor traduz "| LPT
```

**O salto mental não desaparece; ele muda de lugar.** Nas suas próprias tabelas o Lab
Plane escreve `execution_id` e lê `execution_id`. Mas o oráculo lê o sistema medido por
CDC, e o stream carrega o nome que a coluna tem **lá** — a tradução passa a viver no
consumidor, num ponto só e nomeado, em vez de espalhada por toda consulta. Contra: um
mesmo valor com dois nomes exige que alguém saiba que são o mesmo, e essa ligação deixa
de ser visível no esquema.

#### `E-23` fecha em nomes assimétricos, um por lado da fronteira

A coluna se chama `partition_id` nas tabelas do sistema medido e `execution_id` nas
tabelas do Lab Plane. É a quarta candidata, e ela sai da pergunta de 2026-08-06. O
`CREATE TABLE` das duas tabelas medidas deixa de estar bloqueado.

`D-DAT-05` fica honrada na letra: o sistema medido não carrega a palavra "execução" em
lugar nenhum, e para ele aquilo é o que o nome diz — uma partição. O instrumento escreve
e lê `execution_id` nas suas próprias tabelas, sem salto mental.

**O custo é uma ligação que o esquema não declara.** Um mesmo valor com dois nomes exige
que alguém saiba que são o mesmo, e nenhuma constraint diz isso — não poderia dizer, já
que `E-18` proíbe o cruzamento de schemas. A tradução vive num ponto só, no consumidor do
stream de CDC, e é ali que ela precisa estar escrita e testada.

### Timestamps, propostos em 2026-08-06, e a fronteira os separa em duas linhas

A proposta é `created_at` e `updated_at` nas duas tabelas medidas, e `executed_at`,
`concluded_at`, `created_at` e `updated_at` do lado do Lab Plane. **Os dois lados têm
argumentos disjuntos**, e por isso viram duas linhas. `E-25` volta a bloquear o
`CREATE TABLE` que `E-23` acabara de desbloquear.

#### `E-25` — timestamps nas tabelas medidas

**A objeção mais forte não é técnica, é pedagógica.** `updated_at` é um token de versão
clássico — `UPDATE resource SET value = ? WHERE id = ? AND updated_at = ?` é optimistic
locking escrito sem a palavra. A regra do [`AGENTS.md`](../../AGENTS.md) manda introduzir
o problema antes da solução, e é exatamente por isso que `version` não está no esquema. A
coluna entrega de graça metade do que o E1 deve construir do zero.

```mermaid
flowchart LR
    U["updated_at no esquema mínimo"]
    V["version no esquema mínimo"]
    O["optimistic locking<br/>disponível sem construir nada"]
    U --> O
    V --> O
    V -.->|" recusado pelo ADR-0001 "| R["a regra pedagógica"]
    U -.->|" a mesma recusa<br/>vale aqui? "| R
```

**A segunda objeção é sobre como o valor nasce.** As três formas custam:

| Forma                     | O que custa                                  |
|---------------------------|----------------------------------------------|
| `DEFAULT now()`           | relógio do banco, fora de qualquer adaptador |
| trigger `BEFORE UPDATE`   | código dentro da transação medida            |
| preenchida pela aplicação | o medido passa a depender do adaptador       |

O `DEFAULT now()` tem um defeito a mais, e ele é específico do PostgreSQL: `now()`
retorna o instante de **início da transação**, e não o do statement — duas rows escritas
na mesma transação recebem o mesmo valor, o que apaga justamente a ordem que a coluna
deveria mostrar. O trigger é pior por outro motivo: ele acrescenta trabalho **dentro da
janela exata** onde o lost update acontece, e o laboratório mede o que ocorre ali. A
terceira respeita a regra do relógio, e cobra que o sistema medido dependa do adaptador
por uma coluna que nenhum oráculo lê.

**A regra do relógio injetável não as proíbe, e isso precisa ser dito.** Pelo alcance
fixado em `E-13` nesta mesma data, as regras valem sobre valor que entra em veredito, em
escalonamento ou em identidade derivada da semente. Um `created_at` de `resource` não
entra em nenhum dos três. **A objeção vem da pedagogia e do custo na janela medida, não
da regra** — e confundir as duas coisas seria usar a regra como argumento que ela não faz.

**A favor:** com o discriminador preservando execuções antigas, uma pessoa que inspecione
o banco depois quer ordená-las no tempo. **Contra isso:** a ordem já existe e é melhor —
o CDC entrega em ordem de LSN, que é a ordem real de commit. Um timestamp de wall clock é
pior que o LSN para ordenar, e é o LSN que o oráculo usa.

#### `E-26` — timestamps nas tabelas do Lab Plane

**Aqui não há objeção pedagógica.** O Lab Plane é o instrumento, e não o objeto de
estudo; `executed_at` e `concluded_at` são propriedade da execução, e a timeline do
[ADR-0001](0001-o-passo-como-unidade-de-execucao.md) e o relatório dependem de saber
quando cada coisa aconteceu. `created_at` e `updated_at` da definição de experimento são
metadados de CRUD, sem relação com medida.

**Mas `E-13` acabou de decidir algo que alcança esta linha, e não é óbvio.** O veredito em
formato **curva** do grupo D é uma fila crescendo ao longo do tempo. Se a curva for
construída sobre `executed_at` e `concluded_at`, esses valores **entram no papel
veredito** — e o relógio que os produz DEVE ser o adaptador injetável, nunca um
`DEFAULT now()` do banco. É a primeira consequência concreta da formulação por papel.

```mermaid
flowchart TB
    E["executed_at, concluded_at"]
    Q{"a curva do grupo D<br/>é construída sobre eles?"}
    S["entram no papel veredito<br/>relógio injetável obrigatório"]
    N["metadado operacional<br/>a regra não os alcança"]
    E --> Q
    Q -->|" sim "| S
    Q -->|" não "| N
```

**Uma segunda pergunta fica aberta, e ela é do laboratório, não do CRUD.** `executed_at` e
`concluded_at` marcam a fronteira da janela medida pelo relógio do Lab Plane, enquanto o
oráculo ordena eventos por LSN do WAL do sistema medido. **São duas fontes de tempo
distintas**, e correlacionar as duas é exatamente o problema que o grupo E estuda sob o
nome de clock skew. Nada nesta fila decide como elas se alinham.

**Nenhuma das duas linhas foi decidida.**

### A terceira rodada do grupo II, em 2026-08-06

**Fechada em 2026-08-06.** `E-12` pôs um broker entre o conector de CDC e o Lab Plane,
`E-24` escolheu o **serviço próprio** para o componente de identidade, e `E-25` e `E-26`
fixaram as colunas de tempo dos dois lados da fronteira. O broker vive em
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão), o serviço de identidade em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-componente-de-identidade), e as colunas de tempo nos Example Mapping de
[atualização perdida](../features/deteccao-de-atualizacao-perdida/example-mapping.md#perguntas-em-aberto)
e de [execução de experimento](../features/execucao-de-experimento/example-mapping.md#perguntas-em-aberto).

#### `E-12` fecha no broker, e o LSN é o que torna a escolha defensável

**Fechada em 2026-08-06, contra a recomendação.** O transporte entre o WAL e o oráculo —
conector, broker e filtro por execução, com `E-28` e `E-29` — vive em
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão), junto do argumento do LSN que
torna a escolha defensável e da **dispensa explicita** da regra de tecnologia.

#### `E-24` fecha no serviço próprio, e a latência sai da janela se a derivação for antes

**Fechada em 2026-08-06.** A objeção da latência **some se a derivação acontecer na fase
de seeding**, antes de a janela medida abrir, e nenhum dos quatro experimentos hoje
especificados pede identidade nova durante os passos — se um pedir, a linha reabre. O
racional vive em
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-componente-de-identidade).

### Quatro linhas novas, abertas pelas escolhas da terceira rodada

As outras duas, `E-28` e `E-29`, fecharam em 2026-08-06 e a parte permanente delas vive em
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão).

#### `E-27` — como o valor de `created_at` e `updated_at` nasce

`E-25` decidiu que as colunas existem. **Não decidiu quem as preenche**, e as três formas
já estão medidas acima: `DEFAULT now()` colapsa rows da mesma transação num só instante;
trigger `BEFORE UPDATE` acrescenta trabalho **dentro** da janela medida; e o preenchimento
pela aplicação faz o sistema medido depender do adaptador de relógio por uma coluna que
nenhum oráculo lê. A segunda é a única que altera o que se está medindo.

#### `E-30` — o slot do conector deixou de ser por execução, e vira permanente

Com o conector publicando continuamente, o replication slot dele é **um só e de vida
longa**, e não um por execução. A retenção de WAL sai do cenário "um slot órfão por
execução morta" e entra em "um slot que retém tudo se o conector ficar fora do ar" — no
banco compartilhado do homelab, com vizinhos. `max_slot_wal_keep_size` volta a ser a
mitigação, e continua sendo parâmetro de cluster que afeta terceiros.

### O que a quarta rodada apurou antes de perguntar, em 2026-08-06

#### `E-27` ganhou uma quarta forma, e ela separa dois defeitos que estavam juntos

As três formas registradas acima misturam dois defeitos distintos de `DEFAULT now()`: o
relógio ser o do servidor, e o valor ser o instante de **início da transação**. A segunda
metade tem saída própria — `clock_timestamp()` devolve o instante real da chamada, e duas
linhas gravadas na mesma transação recebem valores diferentes. O relógio continua sendo o
do servidor, e continua fora de qualquer adaptador.

| Forma                       | Relógio      | Instante            |
|-----------------------------|--------------|---------------------|
| `DEFAULT now()`             | do servidor  | início da transação |
| `DEFAULT clock_timestamp()` | do servidor  | da chamada          |
| trigger `BEFORE UPDATE`     | do servidor  | da chamada          |
| aplicação, pelo adaptador   | do adaptador | da chamada          |

**A tensão que ninguém viu ao fechar `E-25`.** O grupo E estuda clock skew, e o insumo
natural de um experimento assim é justamente uma coluna de tempo escrita pela aplicação,
com relógio que o experimento pode deslocar. Se `updated_at` vier do adaptador, ela deixa
de ser metadado inerte e vira matéria-prima possível — e a regra escrita em `E-25`, de que
nenhuma estratégia a lê, passa a conviver com um experimento que a lê por outro motivo. A
regra fala de estratégia de concorrência e não de oráculo, então não há contradição hoje.
**Há pressão sobre uma regra recém-escrita, e ela precisa ficar visível.**

#### `E-30` não entra nesta rodada, e a razão é que ela depende de `E-5`

A mitigação de retenção é `max_slot_wal_keep_size`, que é **parâmetro de cluster**. Decidir
o valor dele exige antes saber se o laboratório roda no PostgreSQL compartilhado do homelab
ou em uma instância própria — que é a linha `E-5`, aberta. Fixar um valor agora seria impor
um limite ao vizinho sem ter decidido que existe vizinho.

> **A premissa deste adiamento não vale mais, e ninguém percebeu na hora.** `E-5` já
> estava fechada quando este parágrafo foi escrito, no PostgreSQL **compartilhado** do
> homelab. O argumento se inverte: sabe-se que o vizinho existe, e não fixar o limite é
> que passa a impor risco a ele. `E-30` deixa de estar bloqueada e passa a estar
> **aberta e decidível**. O que ela decide continua sendo parâmetro de cluster, e por
> isso a decisão alcança o `homelab-infrastructure`, e não só este repositório.

### A quarta rodada do grupo II, em 2026-08-06

| Linha              | Escolha                               | Seguiu a recomendação? |
|--------------------|---------------------------------------|------------------------|
| `E-27`             | aplicação, pelo adaptador de relógio  | sim                    |
| `E-28`             | Debezium Server, processo separado    | não                    |
| `E-29` (topologia) | a mesma instância, e o custo é aceito | não                    |
| `E-29` (filtro)    | filtro no consumidor, com contagem    | sim                    |

#### `E-27` fecha na aplicação, e o DDL das duas tabelas medidas deixa de ter lacuna

As colunas nascem `timestamptz NOT NULL`, sem `DEFAULT` e sem trigger, e o valor vem do
adaptador de relógio no momento da escrita. Nada roda dentro da transação medida além do
`INSERT` ou do `UPDATE` que já rodaria.

**A ausência de `DEFAULT` é deliberada e tem custo.** Uma escrita que esqueça a coluna
falha por `NOT NULL` em vez de gravar um valor plausível e errado. É a troca certa aqui:
um erro barulhento na primeira execução vale mais que um instante silenciosamente vindo do
relógio errado, meses depois, num experimento de clock skew.

A tensão registrada acima permanece por escrito: se algum experimento do grupo E ler
`updated_at` como insumo, a coluna deixa de ser metadado inerte, e a regra de `E-25` passa
a conviver com essa leitura. A regra fala de estratégia de concorrência, e não de oráculo
— **não há contradição hoje, e há pressão amanhã**.

### Três linhas novas, abertas pela quarta rodada

#### `E-31` — onde vive a configuração do Debezium Server

Ele não é um módulo Maven, e não nasce do reactor. A configuração é declarativa e precisa
ser versionada, entregue e bumpada como os outros quatro artefatos. **Isso reabre a
pressão sobre `E-3`**, a forma do `deploy/`, que segue adiada.

#### `E-32` — o teste que prova que o LSN chega ao consumidor

**Fechada em 2026-08-06.** O LSN é o que ordena os eventos do WAL, e nada garante que ele
sobreviva à travessia `pgoutput` → Debezium Server → RabbitMQ → `lab-plane`: uma
transformação de mensagem no meio do caminho pode descartar o bloco `source` que o carrega.
A guarda decidida é um teste de aceitação sobre a cadeia inteira, descrito abaixo em
[`E-32` fecha na cadeia inteira](#e-32-fecha-na-cadeia-inteira-e-o-teste-ganha-uma-segunda-asserção)
e registrado em
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#negativas).

`E-33`, a terceira linha aberta por esta rodada, fechou na mesma data e sua lápide está em
[`E-33` fecha na distinção](#e-33-fecha-na-distinção-e-ela-transforma-uma-recomendação-de-e-3-em-requisito).

### O que a quinta rodada apurou antes de perguntar, em 2026-08-06

Dois achados sobre `E-31`, verificados na documentação do Debezium Server e na própria
árvore, e um deles abre `E-34`, uma linha que ninguém tinha visto.

#### `E-31` — a variável de ambiente sobrepõe tudo, e isso dissolve a tensão do Secret

O Debezium Server é uma aplicação Quarkus. A configuração vive em
`config/application.properties`, com os prefixos `debezium.source.*` para o conector e
`debezium.sink.*` para o destino — e **toda opção presente nesse arquivo pode ser
acrescentada ou sobreposta por variável de
ambiente**. A fonte é a
[documentação de operação do Debezium Server](https://debezium.io/documentation/reference/stable/operations/debezium-server.html),
conferida em 2026-08-06 — evidência externa, e não deste repositório.

Isso importa porque a credencial de `REPLICATION` sobre o banco do sistema medido é um
Secret, e o [`AGENTS.md`](../../AGENTS.md) proíbe Secret neste repositório. Sem o override
por ambiente, um arquivo versionado obrigaria a interpolação como único recurso; com ele,
a senha simplesmente nunca aparece em arquivo nenhum.

**Há precedente na árvore, e ele aponta para o ambiente.** O [`compose.yaml`](../../compose.yaml)
não monta arquivo de configuração para serviço nenhum: `LAB_PLANE_DB_URL`,
`SUT_DB_PASSWORD` e as demais vão todas por ambiente. A única exceção é
`local/postgres-init.sql`, que é script de inicialização do banco e não configuração de
aplicação.

| Forma                                 | Onde a senha vive | O que o `deploy/` carrega |
|---------------------------------------|-------------------|---------------------------|
| arquivo versionado, senha interpolada | ambiente          | ConfigMap com o arquivo   |
| só variável de ambiente               | ambiente          | as variáveis do manifesto |
| esperar `E-3`                         | —                 | nada, e o CDC não sobe    |

A terceira não é neutra. Enquanto ela durar, o Debezium Server roda no `compose.yaml` de
desenvolvimento e **não existe no homelab** — o que significa que o veredito não pode ser
produzido lá.

#### `E-34`, aberta pela apuração: o sink tem duas formas, e elas não são intercambiáveis

O Debezium Server oferece **dois** sinks de RabbitMQ: `rabbitmq`, sobre AMQP 0-9-1, com
`exchange` e `routingKey`; e `rabbitmqstream`, sobre o protocolo de stream, com semântica
de offset e retenção.

**A escolha entre eles amarra o objeto de estudo do grupo B.** O grupo estuda fila cheia e
consumidor lento — e uma *queue* AMQP que enche não é a mesma coisa que um *stream* com
retenção configurada, onde o produtor não é bloqueado pelo consumidor lento da mesma forma.
Escolher o sink pelo conforto do consumidor escolheria, sem dizer, qual fenômeno de
saturação o laboratório consegue reproduzir.

A linha não entra nesta rodada. Ela depende de o grupo B ter experimento especificado, e
hoje ele não tem.

### A quinta rodada do grupo II, em 2026-08-06

| Linha  | Escolha                                      | Seguiu a recomendação? |
|--------|----------------------------------------------|------------------------|
| `E-31` | não decidida; exigência nova registrada      | —                      |
| `E-32` | aceitação com os três contêineres            | sim                    |
| `E-33` | invalida só se o discriminador estiver ativo | sim                    |

#### `E-31` não fecha, e o que a impede é uma exigência que a fila não enunciava

Nenhuma das três formas foi escolhida, e a razão é ortogonal a todas elas: **rodar o
Debezium Server no cluster exige mudar o repositório
[`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure)**, e essa
exigência não estava escrita em lugar nenhum desta fila. Ela vale para qualquer das três
formas, porque nenhuma delas é alcançada por um `deploy/` que este repositório sozinho
produza.

O que ela acrescenta, pelo que o [`AGENTS.md`](../../AGENTS.md) já registra do contrato da
ADR 0017 daquele repositório:

- **A credencial de `REPLICATION` é um Secret**, e Secret não entra aqui. Ela é cifrada
  com SOPS/KSOPS no homelab e referenciada por nome — o que significa que a decisão de
  `E-31` sobre onde a configuração vive **não** decide onde a senha vive; ela já está
  decidida, e fora deste repositório.
- **O `Application` do ArgoCD aponta para um `deploy/` que não existe.** Já é o
  `ComparisonError` registrado em `E-3`. Um serviço a mais não o piora, mas também não
  chega ao cluster antes de `E-3` fechar.

**Pergunta em aberto: a ADR 0017 alcança uma imagem que este repositório não constrói?** O
`AGENTS.md` registra que ela descreve o laboratório como "monorepo de microsserviços JVM",
e o contrato dela fala em imagem publicada no GHCR com tag igual ao SHA do commit. O
`debezium/server` é imagem de terceiro, com tag de versão do Debezium, e nenhum commit
daqui a produz. Se isso é caso previsto ou lacuna, não foi conferido aqui.

#### `E-32` fecha na cadeia inteira, e o teste ganha uma segunda asserção

**Fechada em 2026-08-06.** O teste é de aceitação e sobe **três contêineres** — PostgreSQL
com `wal_level=logical` por comando explícito, Debezium Server e RabbitMQ —, escrevendo,
lendo do broker e comparando o LSN lido com o `pg_current_wal_lsn()` do momento da
escrita. A segunda asserção é o que o torna guarda em vez de conferência: ela falha se
alguém ligar o `ExtractNewRecordState` e o bloco `source` desaparecer. **O teste não
existe**, e até existir o veredito repousa sobre uma promessa de terceiro —
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#negativas).

#### `E-33` fecha na distinção, e ela transforma uma recomendação de `E-3` em requisito

**Fechada em 2026-08-06.** Um evento que chega ao `lab-plane` com discriminador de execução
**ativo** e não reconhecido invalida a execução; um com discriminador de execução encerrada
é descartado em silêncio, porque ele é resíduo de uma janela que já fechou. A distinção só
se sustenta se um `lab-plane` souber quais execuções estão ativas — e com duas réplicas,
uma delas não sabe. **A réplica única deixou de ser preferência e virou condição do
veredito confiável**, o que é insumo vivo para `E-3`, ainda aberta. A consequência está em
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#consequências),
e onde a lista de execuções ativas vive continua aberto em
[`E-35`](#e-35--onde-o-lab-plane-guarda-quais-execuções-estão-ativas).

### Duas linhas novas, abertas pela quinta rodada

#### `E-34` — qual dos dois sinks de RabbitMQ, e o que ele amarra

Aberta na apuração acima. `rabbitmq` sobre AMQP 0-9-1 contra `rabbitmqstream` sobre o
protocolo de stream. A escolha decide, sem dizer, qual fenômeno de saturação o grupo B
consegue reproduzir. **Não entra até o grupo B ter experimento especificado.**

#### `E-35` — onde o `lab-plane` guarda quais execuções estão ativas

`E-33` exige a resposta a "este discriminador pertence a execução ativa?", e não disse de
onde ela vem. Em memória, a resposta some num reinício e toda a execução seguinte passa a
descartar às cegas. Numa tabela do schema do `lab-plane`, ela sobrevive — e cria a primeira
tabela daquele schema, hoje vazio. A linha decide qual das duas, e como uma execução
abandonada deixa de ser ativa.

### Duas linhas abertas pelo ADR-0010, ao reconciliar os cards

O [ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md) nasceu `Aceito`
em 2026-08-06 deixando lacunas marcadas como `Pergunta em aberto`. Duas delas precisam de
linha aqui, porque **uma pergunta dentro de um ADR aceito não pode ser respondida editando
o ADR**. Uma terceira, a fonte do `value_inicial`, foi apurada como aberta **por engano** —
ela fechou em 2026-08-05, e o parágrafo de `E-36` registra onde.

#### `E-36` — a emissão ao vivo entra na janela que o experimento mede

`E-19` decidiu que as observações de passo atravessam para o `lab-journal` ao vivo, evento
por evento. O ADR-0008 já registra que a latência de rede entra na medida de todo
experimento, e o E1 emite entre 900 e 1500 observações por execução — a emissão evento a
evento acrescenta cada uma dessas travessias **dentro** da janela medida. **A saída existe
e nunca foi escolhida:** emissão não bloqueante, em que o passo enfileira num buffer local
e um remetente próprio esvazia. O custo dela é perder o buffer quando o `lab-plane` cai —
e a etapa 6 mata o processo de propósito. A linha decide qual das duas.

**Não confundir com o `value_inicial`, que já tem fonte.** Esta linha nasceu de uma
apuração que o tratava como aberto; ele não é. `O20` fechou em 2026-08-05 pelo estado
inicial ser **inserido** antes de cada execução, e capturado como qualquer outro evento —
o registro está em
[`decisoes-pendentes.md`](arquivo/proposta-2026-08-03/decisoes-pendentes.md#o20-fecha-o-estado-inicial-é-criado-dentro-da-janela-de-captura),
que também descarta o snapshot inicial do Debezium por nome, porque ele lê a tabela
inteira e devolve ao instrumento o acesso ao banco medido.

#### `E-37` — o que a proibição de derivar estado de stream alcança

O ADR-0002 proíbe o oráculo derivar o estado final de um log. O oráculo do predicado
precisa de `Σ amount`, e obtê-la do WAL é somar eventos de `INSERT` — reconstruir um total
a partir de um stream, que é o que a proibição descreve. O oráculo exato lê o **último**
evento, sem somar, e se a mesma proibição o alcança nunca foi decidido. A linha decide o
alcance e, em consequência, **se o E5 tem oráculo**. As regras `R3` e `R5` do card de
proteção inerte ficam sem mecanismo até ela fechar.

### `E-38` — o limite do Feature Card contra o card como fonte de verdade

Aberta em 2026-08-06, ao reconciliar os cards com o ADR-0010. **A decisão de que
`docs/features/` é fonte de verdade e o limite de 5500 caracteres do Feature Card não
convivem.** Um card que carrega tudo o que uma consulta precisa é maior que um card que
resume e aponta.

A medição depois da reconciliação, com o verificador de limites:

| Card                            | Antes | Depois | Limite |
|---------------------------------|-------|--------|--------|
| detecção de atualização perdida | 7470  | 9576   | 5500   |
| execução de experimento         | 7372  | 8278   | 5500   |
| observação passo a passo        | 6641  | 8512   | 5500   |
| detecção de proteção inerte     | 5312  | 7029   | 5500   |

**Três dos quatro já excediam antes**, e o quarto passou a exceder. A pendência de que o
card de atualização perdida violava o limite de palavras já estava registrada, e nunca foi
decidida — o que mudou é que agora ela alcança todos os quatro, e por um motivo novo: não é
prosa em excesso, é conteúdo que a decisão de fonte de verdade exige que esteja ali.

Três saídas, nenhuma escolhida. Dividir cada card em dois artefatos, e decidir o que fica
em qual. Subir o limite, e aceitar que um card longo deixa de ser lido de ponta a ponta.
Ou manter o limite e aceitar que o card volte a apontar para o ADR — o que **desfaz** a
decisão de 2026-08-06. **A terceira não é neutra**, e é por isso que a linha existe em vez
de o limite ser ajustado em silêncio.

#### `E-38` fecha por uma quarta saída, escolhida em 2026-08-06

**Diagrama, bloco de código e tabela deixaram de entrar na contagem**, em todo artefato
`.md` que tenha limite. A escolha é da pessoa, e resolve a linha sem tocar em nenhuma
das três saídas acima: o limite continua 5500, os cards continuam carregando tudo o que
uma consulta precisa, e nenhum volta a apontar para o ADR.

O que a linha media não era o que ela queria medir. Um card cresce em caracteres por
três motivos, e só um deles é prosa em excesso: uma regra nova acrescenta uma **linha de
tabela** com evidência e aprovador, um fluxo novo acrescenta um **diagrama** — e as
convenções deste repositório **exigem os dois**. O limite punia o cumprimento da regra.

| Card                            | Bruto | Prosa | Limite |
|---------------------------------|-------|-------|--------|
| detecção de atualização perdida | 9245  | 3637  | 5500   |
| detecção de proteção inerte     | 6721  | 4651  | 5500   |
| execução de experimento         | 8011  | 2922  | 5500   |
| observação passo a passo        | 8286  | 2604  | 5500   |

O verificador é
[`check_artifact_limits.py`](../../.claude/skills/feature-planning/scripts/check_artifact_limits.py),
e a regra está em [`../AGENTS.md`](../AGENTS.md#feature-card) e em
[`README.md`](README.md#convenções).

**O `behavior.feature` fica de fora da regra, e não por esquecimento.** Em Gherkin a
tabela `Exemplos:` **é** o cenário, e não ilustração dele; descontá-la esvaziaria o
limite em vez de corrigi-lo.

#### `E-39` — o Example Mapping tem limite, e as instruções dizem que não

Aberta em 2026-08-06, pela mesma medição. Duas coisas se contradizem, e nenhuma é nova:
[`check_artifact_limits.py`](../../.claude/skills/feature-planning/scripts/check_artifact_limits.py)
impõe 4500 caracteres a `example-mapping.md`, enquanto o texto de `docs/AGENTS.md`
dizia, até hoje, que o Example Mapping **não tem limite** — e mandava mover para lá o
diagrama que não coubesse no card.

Com a contagem por prosa, dois dos quatro continuam acima:

| Example Mapping                 | Bruto | Prosa | Limite |
|---------------------------------|-------|-------|--------|
| execução de experimento         | 10452 | 6443  | 4500   |
| observação passo a passo        | 8626  | 6260  | 4500   |
| detecção de proteção inerte     | 7355  | 4293  | 4500   |
| detecção de atualização perdida | 5486  | 3925  | 4500   |

Aqui é prosa mesmo, e não moldura — a regra nova não os salva. As saídas eram: subir o
limite dos dois, cortar prosa deles, ou aceitar que o Example Mapping é o artefato sem
teto e remover a entrada do verificador.

#### `E-39` fecha sem teto, no mesmo dia

**O `example-mapping.md` não tem limite.** Escolhido pela pessoa em 2026-08-06, pela
terceira saída. Um Example Mapping cresce por exemplo acrescentado, e acrescentar
exemplo **é o trabalho dele** — um teto ali transforma "achei mais um contraexemplo" em
"preciso apagar um dos antigos", que é o oposto do que o artefato existe para fazer.

Quem estava fora de sincronia era o verificador: `docs/AGENTS.md` já dizia que ele não
tem limite. O script ganhou uma isenção **por nome**, e não a simples remoção da entrada
— sem ela o arquivo cairia no teto genérico de 4000 para `.md`, mais apertado que o que
a decisão removeu.

O custo está nomeado: o Example Mapping passa a ser o único artefato de
[`../features/`](../features/README.md) sem freio nenhum.

**Sobra uma pendência da mesma família, e ela é anterior a tudo isto.** O
`behavior.feature` de detecção de atualização perdida tem 4295 caracteres contra um teto
de 3500 — e já tinha 4223 antes das edições de hoje. Ele **não** recebe o desconto de
tabela, por decisão: em Gherkin a tabela `Exemplos:` é o cenário, e não ilustração dele.
Subir o teto, dividir o arquivo ou cortar cenário é escolha, e ela não foi feita.

#### `E-40` — o componente de identidade contradiz um `DEVE` do ADR-0002

**Fechada em 2026-08-06: não há contradição.** O `DEVE` do ADR-0002 opõe **aplicação a
banco**, e não sistema medido a serviço externo — o que ele proibe é o banco atribuir
identidade por `SERIAL`, `IDENTITY` ou `nextval`. O ADR-0002 não é emendado nem
substituído, e o
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#justificativa) registra a leitura e o motivo dela, de propósito.

#### `E-41` — o que a decisão do broker desfaz fora do ADR

Aberta em 2026-08-06, na segunda revisão do ADR-0012. Duas consequências que não vivem
dentro de nenhum ADR e que ficariam sem dono.

**O `REPLICATION` do papel `lab_plane` perdeu o propósito.** `local/postgres-init.sql:18`
faz `ALTER ROLE lab_plane REPLICATION;`, e o comentário acima dele diz que o `lab-plane`
lê o WAL por replicação lógica. Com o conector em processo próprio, quem lê o WAL é o
Debezium Server — o `lab-plane` consome do broker e **não precisa mais do atributo**.
Mantê-lo deixa a credencial de leitura do WAL no mesmo processo que produz o veredito,
que é a razão pela qual o conector foi separado.

**Um papel novo, dedicado ao conector, recebe o `REPLICATION`.** Escolhido pela pessoa em
2026-08-06. A alternativa era o papel do sistema medido, e ela perde por ampliar o que
uma falha nele alcança: ler o próprio WAL não é necessário para o domínio, e o
laboratório mata processos do sistema medido de propósito na etapa 6.

Manter o `GRANT` no `lab_plane` **desfaria o motivo de o conector existir em processo
próprio** — a credencial de leitura do WAL voltaria ao processo que produz o veredito, um
nível abaixo da regra de fronteira. O `local/postgres-init.sql` muda no commit que traz o
ADR-0012.

**A matriz de integrações envelheceu no mesmo ato.**
[`integrations.md`](../architecture/integrations.md#matriz) registra o RabbitMQ como
**hipótese**, com a ressalva de que ele entra na etapa 5 e não antes. A decisão do broker
o põe no dia zero. A regra de `docs/AGENTS.md` obriga a matriz a separar fato de hipótese
e proíbe deixar uma linha envelhecer — a linha é reescrita no commit que traz o ADR.

**Ao reescrevê-la, apareceu uma segunda linha morta que ninguém tinha registrado.** A
matriz descrevia `Lab Plane (oráculo) → PostgreSQL`, por `SELECT` após a quiescência —
exatamente a regra que o
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão) revogou
ao mandar o oráculo ler o WAL. Ela foi substituída pelas três linhas do caminho decidido:
conector → PostgreSQL por replicação lógica, conector → RabbitMQ, RabbitMQ → `lab-plane`.
A linha do RabbitMQ do domínio continua **hipótese**, porque o que a decisão do broker
antecipou foi a existência do broker, e não o uso dele pelos grupos B e C.

**O que isso revela é maior que as duas linhas.** A matriz não tem quem a reconcilie
quando um ADR nasce; ela envelheceu porque a checagem não existe, e não porque alguém
esqueceu. Se cada ADR passa a listar o que desfaz fora de si — e se a checagem disso é
humana ou executável — **ninguém decidiu**: `Pergunta em aberto`.

## A dívida de ADR do Lote E, levantada em 2026-08-06

**Vinte e nove linhas fecharam desde 2026-08-06, e nenhum ADR nasceu.** O último é o
[ADR-0009](0009-a-classificacao-do-dual-write-e-a-regiao-de-pacote.md), de 2026-08-05,
vindo do Lote A. Todo o Lote E vive nesta fila, e em nenhum outro lugar.

Isso **não** foi decidido. A regra de 2026-08-04 diz que a escolha do artefato acontece
depois da decisão, e a escolha simplesmente não foi feita — nem a favor do ADR, nem a
favor de `docs/features/`. A fila virou o depósito de tudo, por omissão.

### Três defeitos que já são visíveis, e nenhum é hipótese

**Uma linha desta fila foi decidida duas vezes.** `E-22` fechou, e reabriu, e fechou de
novo — o registro está em
[`E-22` fecha em `(execution_id, id)`](#e-22-fecha-em-execution_id-id-e-a-linha-foi-decidida-duas-vezes).
Uma decisão que não é consultável como registro é uma decisão que se retoma sem perceber.

**`E-18` é citada como regra estabelecida, e não tem estatuto de regra.** O
[`AGENTS.md`](../../AGENTS.md) a invoca para explicar por que o oráculo lê o WAL; o
[`compose.yaml`](../../compose.yaml) a invoca em comentário; três rodadas desta fila a
usam como premissa. Ela vive numa linha de um arquivo de 2431 linhas, **sem estado, sem
rastro de alteração e sem mecanismo de substituição** — que é exatamente o que
[`README.md`](README.md#estados) dá a um ADR.

**A fila não tem teto, e o índice de ADR tem.** Esta página passou de 2009 para 2431
linhas em três rodadas de um único dia. O [`README.md`](README.md#esta-página-tem-um-teto-de-514-linhas-e-ele-não-é-escolha)
carrega um teto de 514 linhas justamente porque um documento que só cresce deixa de ser
lido. Nada equivalente protege esta fila.

### A triagem contra os quatro critérios

Aplicando [os quatro critérios](README.md#uma-decisão-merece-adr-quando) às vinte e nove
linhas fechadas, elas se agrupam em **seis temas**, e não em vinte e nove artefatos. Duas
linhas não atendem a critério nenhum, e três seguem abertas.

| Tema candidato                                       | Linhas fechadas                                | Estado                         |
|------------------------------------------------------|------------------------------------------------|--------------------------------|
| a fronteira de schema e o CDC como fonte do veredito | `E-18`, `E-19`                                 | **contradiz o ADR-0002**       |
| os quatro serviços e o caderno fora do Git           | `E-14` a `E-17`, `E-20`                        | **emenda o ADR-0008**          |
| o transporte do veredito até o oráculo               | `E-12`, `E-28`, `E-29`, `E-33`                 | maduro                         |
| o alcance das regras estruturais por papel do valor  | `E-13`                                         | maduro; já mudou o `AGENTS.md` |
| a identidade derivada da semente                     | `E-8`, `E-11`, `E-24`                          | maduro                         |
| a chave, o discriminador e as colunas de tempo       | `E-9`, `E-10`, `E-22`, `E-23`, `E-25` a `E-27` | maduro                         |
| a entrega: build, imagem, banco e configuração       | `E-1` a `E-7`, `E-21`, `E-31`                  | **incompleto**: `E-3` aberta   |

**Os dois primeiros não são opcionais.** A decisão `B-4`, de 2026-08-05, diz que
contradição com ADR aceito **é** decisão arquitetural nova e gera ADR. `E-18` contradiz o
oráculo do ADR-0002, que pressupunha ler o estado final do sistema medido; `E-14` a `E-17`
emendam o ADR-0008, que fala em dois planos onde hoje existem quatro serviços. Os dois
já estão registrados como pendência nesta fila, e nenhum foi escrito.

**Duas linhas não viram ADR, e é o critério que diz isso.** `E-16` escolheu o nome
`lab-journal` — nome não atende a nenhum dos quatro. `E-32` decidiu a forma de um teste,
e o artefato dela é o próprio teste, não um documento.

**O sétimo tema não está pronto.** A entrega tem `E-3` aberta, e agora `E-31` também. Um
ADR de entrega escrito hoje registraria metade de uma decisão.

### A saída, decidida em 2026-08-06

**Os seis são escritos em sequência, um por vez, com o contexto limpo entre eles.** O
roteiro de cada sequência e o conteúdo que cada ADR precisa carregar estão em
[`plano-de-escrita-do-lote-e.md`](plano-de-escrita-do-lote-e.md) — um documento com prazo
de validade, apagado quando os seis existirem.

**A linha da fila é removida quando o ADR nasce.** Decidido contra a recomendação de
deixar lápide, e a verificação que sustentou a escolha desmontou a objeção: nenhuma
citação externa aponta para as seções de rodada do Lote E. As âncoras citadas de fora
desta fila são todas de seções anteriores a ele.

**A premissa acima caiu, e a lápide passou a ser obrigatória.** Decidido em 2026-08-07,
pelo achado `A-11` de
[`2026-08-06-coerencia-e-limites-documentais.md`](../audits/2026-08-06-coerencia-e-limites-documentais.md#a-11--a-fila-ativa-contém-narrativa-integral-de-decisões-fechadas):
os ADRs 0010, 0011 e 0012 nasceram citando seções de rodada do Lote E, e o corpo de um ADR
aceito não pode ser editado para apontar para outro lugar. **Onde um documento imutável
cita o heading, o heading permanece byte a byte**, e sob ele ficam o estado `fechada`, o
ADR que a absorveu e o link com âncora. Onde ninguém cita, a narrativa é apagada sem
lápide. A poda de 2026-08-07 aplicou as duas regras.

**`docs/features/` é fonte de verdade, junto dos ADRs**, e por isso cada sequência entrega
ADR e card no mesmo commit. A regra nasceu de um achado: **três cards contradizem `E-18`
hoje**, cada um afirmando que o oráculo emite `SELECT` depois da quiescência. Enquanto
`E-18` era linha de fila, isso era incoerência; quando ela virar ADR aceito, passa a ser
violação da regra `B-4`.

## A imutabilidade do corpo de um ADR aceito, revogada em 2026-08-07

**Fechada em 2026-08-07, por decisão explícita da pessoa.** A linha nasce aqui já
fechada: a revogação foi aplicada na árvore antes de ter linha na fila, e a fila é onde
uma decisão desse alcance precisa estar registrada. Ela veio da auditoria de
[`2026-08-06-coerencia-e-limites-documentais.md`](../audits/2026-08-06-coerencia-e-limites-documentais.md#resultado-executivo),
e não inaugura lote novo — a organização da fila em lotes não foi reaberta.

**O problema.** O corpo de um ADR aceito nunca era editado, e a regra custava mais do que
protegia: um teto de linhas no [`README.md`](README.md#esta-página-tem-um-teto-de-514-linhas-e-ele-não-é-escolha)
que existia só para não deslocar citação, entradas de defeito declaradas insolúveis em
[`citations-baseline.txt`](../../scripts/citations-baseline.txt), errata em cabeçalho para
dizer que uma citação apontava para o lugar errado sem poder consertá-la, e um adendo
criado para incorporar o que uma citação quebrada sustentava.

**A alternativa era manter a regra**, aceitando esses custos, com a proteção que ela dava:
impedir que a decisão de ontem fosse reescrita para parecer a de hoje.

**A escolha: revogar, com o patch como quinta forma de alterar um ADR aceito**, ao lado de
substituição, subsunção, emenda e adendo. O patch é limitado a texto que não carrega
decisão, e cada um exige a linha correspondente em `## Patches aplicados`, no mesmo commit
— é assim que a proteção antiga sobrevive por outra via.

**O conteúdo é do [`README.md`](README.md#a-revogação-da-imutabilidade-decidida-em-2026-08-07)**,
e não desta fila: o que é patch e o que não é, as quatro regras do livro-razão, a isenção
da seção na contagem de prosa e a exclusão do campo `Alterado por` estão lá, e não são
reproduzidos aqui.

**A consequência que alcança esta fila não é a que se esperaria: as lápides continuam
obrigatórias.** A regra de
[`A saída, decidida em 2026-08-06`](#a-saída-decidida-em-2026-08-06) preserva o heading
citado porque `scripts/check_citations.py` precisa que a âncora exista — e isso independe
de o corpo do ADR ser editável. A premissa mudou; a conclusão não.

## O rito que reconcilia a matriz com a árvore

**Aberta, e nasce sem recomendação.** Ela veio da reestruturação do roteamento
documental, que deu a `docs/README.md` o papel de roteador único. Não inaugura lote novo.

**O problema.** O roteador declara dois donos para fatos vizinhos: a árvore versionada
prova **o que existe e executa**, e a
[matriz](../architecture/integrations.md#matriz) é dona do **estado de cada fronteira de
processo**. Os dois respondem a perguntas diferentes, e por isso a divisão é boa — mas
nada define o que fazer quando eles discordam. Uma fronteira marcada como decidida e
ausente cujo código já está na árvore, ou uma marcada como implementada cujo módulo foi
removido, são o mesmo defeito visto de dois lados, e hoje quem o encontra decide sozinho
qual dos dois corrigir.

**A tentação a evitar é a inferência automática:** tratar a árvore como sempre vencedora
transformaria toda remoção temporária em regressão de estado documentado, e tratar a
matriz como sempre vencedora reintroduz a hipótese promovida a fato que a própria matriz
existe para impedir.

**Três alternativas, e nenhuma escolhida.**

| Rito                       | O que ele faz                                                                       | O custo                                                    |
|----------------------------|-------------------------------------------------------------------------------------|------------------------------------------------------------|
| árvore vence, sempre       | quem vir a divergência corrige a matriz no mesmo turno, citando o caminho           | uma remoção temporária vira regressão registrada           |
| matriz vence até revisão   | a divergência abre linha aqui, e a matriz só muda por decisão                       | o documento fica errado enquanto a linha não fecha         |
| verificação determinística | um script confere as afirmações da matriz que têm caminho versionado, e falha no CI | só alcança o que for expresso como caminho, e não o estado |

```mermaid
flowchart TD
  D["a matriz e a árvore<br/>discordam"] --> Q{"qual rito?"}
  Q -->|" árvore vence "| A["corrigir a matriz<br/>no mesmo turno"]
  Q -->|" matriz vence "| B["abrir linha nesta fila<br/>e não editar a matriz"]
  Q -->|" verificação "| C["script confere o que tem<br/>caminho versionado"]
  A --> R["a divergência fecha"]
  B --> R
  C --> R
```

**A terceira não exclui as outras duas**, e é a única que impede a divergência de passar
despercebida — as outras duas só dizem o que fazer depois que alguém a nota. A linha
decide qual rito vale e, se for a terceira, o que exatamente o script consegue afirmar.

## O orçamento de prosa: quem é dono do teto, e o que ele alcança

**Aberta.** Ela é a segunda das quatro perguntas do plano de navegação documental, que
nasceu em `4d15bd6` e foi removido da árvore em `4f04246` — o texto original é recuperável
por `git show 4d15bd6:docs/audits/2026-08-07-navegacao-documental-para-agentes.md`. A
primeira daquelas perguntas fechou no [`AGENTS.md`](../../AGENTS.md#como-o-planejamento-funciona-aqui),
e a quarta é a linha [acima](#o-rito-que-reconcilia-a-matriz-com-a-árvore). Esta e a
[seguinte](#o-que-apura-a-âncora-citada-antes-de-uma-redução) ficaram sem dono quando o
arquivo saiu, e voltam aqui por isso. Não inaugura lote novo.

**O problema.** O teto genérico de prosa é 4.000 caracteres, e quem o aplica é
[`check_artifact_limits.py`](../../.claude/skills/feature-planning/scripts/check_artifact_limits.py).
O workflow [`docs`](../../.github/workflows/docs.yml) só o executa sobre
`docs/adr/[0-9]*.md`. Fora desse glob, ninguém mede — e medidos em 2026-08-08, seis
arquivos excedem o genérico sem que nada falhe:

| Arquivo                                  | Prosa medida | Teto aplicado hoje |
|------------------------------------------|--------------|--------------------|
| `docs/plano-do-laboratorio.md`           | 48.253       | genérico, 4.000    |
| `docs/CONTEXT.md`                        | 35.633       | genérico, 4.000    |
| `docs/adr/plano-de-escrita-do-lote-e.md` | 25.405       | genérico, 4.000    |
| `docs/specification-process.md`          | 18.493       | genérico, 4.000    |
| `docs/questions/README.md`               | 10.442       | genérico, 4.000    |
| `docs/features/README.md`                | 4.616        | genérico, 4.000    |

**Duas coisas distintas estão fundidas.** Um teto que descreve mal o artefato é defeito de
regra; um teto que ninguém executa é defeito de alcance. A isenção de `AGENTS.md` e
`docs/AGENTS.md`, declarada em `4f04246` dentro do próprio script, resolveu dois casos pelo
primeiro eixo e deixou o segundo intacto — os seis acima não estão isentos, estão fora do
alcance da medição.

**A tentação a evitar é declarar isenção nova a cada arquivo que exceda.** Cada isenção
carrega justificativa escrita, o que é bom; o que falta é o critério contra o qual a
próxima seria conferida, e sem ele a soma das justificativas **é** o critério, sem nunca
ter sido decidida.

**Três alternativas, e nenhuma escolhida.**

| Alternativa                  | O que ela faz                                                                                | O custo                                                               |
|------------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| isenção declarada, uma a uma | mantém o que `4f04246` fez, e o script segue sendo o dono do número e das exceções           | o critério fica implícito na soma das justificativas                  |
| teto por classe de artefato  | o processo declara classes — instrução, índice, plano, glossário, fila — e um teto para cada | classificar artefato novo vira decisão, e há artefato em duas classes |
| medir tudo sem falhar        | o CI mede todo Markdown e publica o número, falhando só nas classes com teto                 | o número deixa de ser guardrail e vira relatório que ninguém lê       |

```mermaid
flowchart TD
  A["um Markdown excede<br/>o teto genérico"] --> Q{"qual regime?"}
  Q -->|" isenção uma a uma "| I["justificativa no script,<br/>caso a caso"]
  Q -->|" teto por classe "| C["classificar o artefato,<br/>e aplicar o teto da classe"]
  Q -->|" medir sem falhar "| M["publicar a medição,<br/>falhar só onde há teto"]
  I --> D["o alcance da medição<br/>continua a decidir"]
  C --> D
  M --> D
```

**A linha decide três coisas, e não uma:** qual arquivo é dono do número — hoje ele vive
no script e o [processo](../specification-process.md#feature-card--o-padrão) o cita —,
quais caminhos a medição alcança no CI, e como uma isenção nasce. Decidir só a primeira
deixa os seis arquivos acima exatamente como estão.

## O que apura a âncora citada antes de uma redução

**Fechada em 2026-08-08, por decisão explícita da pessoa.** Terceira das quatro perguntas
do mesmo plano removido, e irmã da linha
[acima](#o-orçamento-de-prosa-quem-é-dono-do-teto-e-o-que-ele-alcança).

**A decisão.** [`check_citations.py`](../../scripts/check_citations.py) ganha um modo de
consulta que responde, sob demanda, quem cita cada heading de um arquivo. **Nada é gravado
na árvore**: a resposta é recalculada no momento da redução e descartada, e por isso não
existe derivado a envelhecer. A guarda que o verificador já executa no CI permanece como a
rede de segurança embaixo da consulta.

Duas alternativas foram descartadas com motivo. O **índice reverso versionado** grava a
mesma resposta num arquivo da árvore, e diverge da fonte no primeiro commit que ninguém
regenerar. O **inventário aprovado por pessoa** não carrega decisão humana nenhuma: a
lápide já é obrigatória para todo heading citado, de modo que o inventário apenas dataria
uma descoberta técnica — e datá-la é o defeito que ele tenta evitar, como a verificação de
2026-08-06 provou ao envelhecer em horas.

**A consulta alcança também a âncora interna, e por um defeito descoberto ao decidir
isto.** Verificado em 2026-08-08: o verificador reconhece a citação externa e **não**
reconhece a interna, porque o padrão exige o `.md` antes do `#`.

```text
reconhecida:      <arquivo>.md#<slug>
não reconhecida:  [texto](#<slug>)
```

Uma âncora interna apontando para título inexistente passa sem defeito nenhum. Esta fila
carrega 16 links dessa forma, e podá-la sem cobri-los quebraria até 16 deles em
silêncio; `CONTEXT.md` carrega
zero, e por isso [A-09](../audits/2026-08-06-coerencia-e-limites-documentais.md#a-09--contextmd-é-glossário-proposta-decisão-e-backlog-ao-mesmo-tempo)
não corre esse risco.

**Pergunta em aberto.** Se o verificador **também** passa a acusar âncora interna quebrada
no CI, e não apenas a responder por ela na consulta, continua sem decisão. Ampliar o que
ele acusa muda o que o corpus precisa satisfazer, e essa é decisão da pessoa.

**O que já está decidido, e não é objeto desta linha.** A lápide é obrigatória: a regra de
[`A saída, decidida em 2026-08-06`](#a-saída-decidida-em-2026-08-06) preserva o heading
citado, e a [revogação da imutabilidade](#a-imutabilidade-do-corpo-de-um-adr-aceito-revogada-em-2026-08-07)
mudou a premissa sem mudar a conclusão. A pergunta aqui é **como se descobre quais headings
são esses**, antes de encolher qualquer documento.

**O problema.** Fechar
[A-09](../audits/2026-08-06-coerencia-e-limites-documentais.md#a-09--contextmd-é-glossário-proposta-decisão-e-backlog-ao-mesmo-tempo)
e
[A-11](../audits/2026-08-06-coerencia-e-limites-documentais.md#a-11--a-fila-ativa-contém-narrativa-integral-de-decisões-fechadas)
exige remover texto de dois documentos citados de fora. **Nenhuma apuração existe**: quem
reduzir precisa varrer o corpus à mão atrás de quem cita o heading que vai apagar, e
[`check_citations.py`](../../scripts/check_citations.py) só acusa o defeito **depois** de
ele ser cometido, na próxima execução.

**A objeção que sustenta a urgência.** O
[plano de escrita do Lote E](plano-de-escrita-do-lote-e.md) registra que a verificação de
2026-08-06 concluiu que nenhuma citação externa apontava para as seções de rodada — e que a
conclusão deixou de valer no ato de escrever os ADRs 0010 a 0012, que passaram a citá-las.
Uma apuração manual foi feita, estava correta, e envelheceu em horas.

**Três alternativas, e nenhuma escolhida.**

| Alternativa                    | O que ela faz                                                                      | O custo                                                        |
|--------------------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------|
| inventário aprovado por pessoa | levanta-se a lista reversa uma vez, e a pessoa aprova quais headings ganham lápide | envelhece na primeira citação nova, como já envelheceu uma vez |
| índice reverso gerado          | um script deriva, de todas as citações, quem aponta para cada heading              | é derivado, e um arquivo derivado versionado diverge da fonte  |
| guarda no CI                   | `check_citations.py` já falha quando um heading citado desaparece do alvo          | não é preventiva: acusa depois da remoção, e não antes dela    |

```mermaid
flowchart TD
  R["quero reduzir<br/>um documento"] --> Q{"como sei quais<br/>headings são citados?"}
  Q -->|" inventário "| I["lista aprovada<br/>numa data"]
  Q -->|" índice gerado "| G["script deriva<br/>quem cita o quê"]
  Q -->|" guarda no CI "| C["a remoção falha<br/>o build"]
  I --> P["a redução acontece<br/>com lápide onde é preciso"]
  G --> P
  C --> P
```

**A terceira alternativa já está implementada, e descobrir isso reformula a pergunta.**
Verificado em 2026-08-08:
[`check_citations.py`](../../scripts/check_citations.py) compara cada âncora citada
contra os títulos do alvo, e emite `ancora nao corresponde a titulo nenhum do alvo`.
Ele **já falha** quando um heading citado desaparece, e a comparação corre contra a
árvore atual — não contra o estado anterior, que uma leitura anterior desta linha supunha
necessário. Reproduz-se com dois arquivos, um citando o outro por âncora, e o heading
apagado do alvo.

O que falta, portanto, não é detecção: é **antecedência**. O verificador responde "você
quebrou" na execução seguinte à remoção; esta linha pergunta o que responde "vai quebrar"
**antes** dela, para que a lápide entre no mesmo commit que reduz o texto. A escolha real
está entre as duas primeiras alternativas, e a terceira deixa de ser trabalho a fazer para
virar a rede de segurança que já existe embaixo delas.

**A segunda alternativa é mais barata do que a tabela sugere**, e isso também é
descoberta desta verificação: `inspect()` já resolve, para cada citação, o par (arquivo
alvo, slug). Um índice reverso não exige um analisador novo — exige inverter e agrupar o
que a função já computa.

E o custo que restava a ela **pressupõe uma premissa que não é obrigatória**: um derivado
só diverge da fonte se for **versionado**. Um modo de consulta que responda, sob demanda,
quem cita um heading não deixa arquivo nenhum na árvore para envelhecer — ele é lido no
momento da redução e descartado. A escolha, então, não é entre inventário e índice: é
entre **guardar a resposta** e **saber recalculá-la**, e é a mesma escolha que a regra
de não repetir estado que outro documento é dono de manter já fez em toda esta base.

**As duas primeiras são parentes da terceira alternativa da linha do rito**, e podem sair
de um mesmo script — mas são decisões separadas, e fundi-las escolheria a ferramenta
antes do problema. Enquanto esta linha não fechar, **nenhuma redução de `CONTEXT.md` ou da
fila deve começar**: é o que separa fechar A-09 e A-11 de quebrar citação de ADR aceito.

## O nível de isolamento não tem lugar nesta fila

O E5 exige a comparação do mesmo experimento sob `READ COMMITTED`, `REPEATABLE READ` e
`SERIALIZABLE`. Só o terceiro aborta uma das transações, com SQLSTATE `40001`. O plano
registra a exigência na seção 6, e nomeia o nível de isolamento como parâmetro do
experimento — escopo que os quatro experimentos anteriores não têm.

**Nenhuma linha desta fila nomeia esse parâmetro.**

A decisão de estratégias de concorrência é o destino aparente, e ela não serve sem
argumento. Uma estratégia é código da aplicação: `NONE`, `ATOMIC_UPDATE`, `OPTIMISTIC` e
`PESSIMISTIC` mudam o SQL que os passos emitem. Um nível de isolamento é propriedade da
transação, e ele muda o que o banco faz com o mesmo SQL. O E5 é o experimento que separa
os dois eixos: com `OPTIMISTIC` ativo sob `READ COMMITTED`, a invariante quebra sem
exceção nenhuma, porque inserir uma alocação não incrementa a versão de linha alguma.
Tratar o isolamento como mais um valor da mesma enumeração apagaria a distinção que o
experimento existe para mostrar.

Três destinos são possíveis, e a escolha não foi feita.

- **Estratégias de concorrência**, com o isolamento declarado como eixo separado dentro
da mesma decisão. O custo é uma decisão que passa a carregar dois eixos.
- **Experiment**, que define o que uma execução declara. O isolamento seria um campo da
definição, ao lado da semente. O custo é decidir a semântica do parâmetro num ADR cujo
assunto é o ciclo de vida da execução.
- **Linha própria nesta fila**, se a escolha tiver alternativas e trade-off que nenhuma
das duas comporte.

Uma pista contra o terceiro destino: o E5 não escolhe um nível, ele varre três. O que a
plataforma precisa é do eixo de variação, e não de um valor decidido uma vez.

Registrado em 2026-07-31, no levantamento do que falta para fechar o MVP.

## A anomalia por frequência: uma proposta que muda o estatuto da barreira

O laboratório foi planejado para **construir** a anomalia. O E2 declara a intercalação
`W1.READ → W2.READ → W1.WRITE → W2.WRITE`, o escalonador a impõe, e a atualização
perdida aparece em toda execução. A proposta inverte o mecanismo: a anomalia emerge da
**frequência** de execuções concorrentes, e o trabalho da plataforma passa a ser
**diagnosticar** se o erro esperado ocorreu.

A proposta não é uma preferência de implementação. Ela troca o que a plataforma promete:
de "esta execução produz a anomalia" para "esta configuração produz a anomalia com esta
taxa". As duas promessas exigem instrumentos diferentes.

#### O que a proposta contradiz

**A aresta `25 → 1` do plano**, seção 4. O texto lá diz: "o lost update precisa ser
demonstrado, não sorteado. Sem barreiras, o experimento produz *às vezes perde* — que é
a mesma frase que o engenheiro já dizia antes de abrir o laboratório." É o argumento
mais forte contra a proposta, e ele já estava escrito antes dela.

**O estatuto epistêmico do E2.** O plano separa E1 de E2 assim: "E1 prova que o
laboratório *detecta*. E2 prova que o laboratório *constrói*. São capacidades
diferentes, e a segunda é a que torna a primeira confiável." Sem barreira, a segunda
capacidade some, e a confiança na primeira perde o apoio que o plano lhe deu.

**A cláusula de honestidade do ADR-0001**, que está `Aceito`. Ela compara um braço com
barreiras contra um braço sem elas. Com um braço só, a cláusula fica sem sujeito. A
falha que ela existe para pegar — o runtime fabricando o fenômeno por agendamento —
deixa de ser possível pelo mesmo motivo, mas a fabricação por estado compartilhado
dentro do instrumento continua, e [`Q-0001-2`](../questions/Q-0001-2.md) registra que
ela não tem guarda.

**O ADR-0003 inteiro.** Ele define como uma barreira é declarada. A questão 4 daquele
documento está `aberto (crítico)` por causa desta proposta, e ele NÃO DEVE ser aceito
antes que este item seja decidido.

#### O que a proposta não contradiz, e o que ela reforça

**O oráculo do ADR-0002 já é uma contagem, e não um booleano.**
`perdidas = commits − (value_final − value_inicial)` mede magnitude. Uma taxa é a mesma
contagem dividida pelo número de tentativas, e nada no ADR-0002 precisa mudar para
produzi-la. O domínio mínimo foi escolhido de um jeito que serve às duas promessas.

**O E1 já é a proposta.** Cem incrementos, dez workers, nenhuma barreira, `value < 100`.
A mudança não introduz um experimento novo no MVP: ela promove a forma do E1 a norma e
rebaixa a do E2.

**O grupo de controle deixa de ser disciplina e vira pré-requisito lógico.** A regra
"se `NONE` não violar, a carga é insuficiente" já está no repositório. Sob a proposta,
ela passa a ser a única coisa que faz um resultado negativo significar alguma coisa.

**O passo sobrevive com duas das três motivações.** O ADR-0001 fixou o passo por três
exigências: barreira determinística, injeção de falha em ponto nomeado e timeline. A
proposta atinge a primeira e não toca nas outras duas. A etapa 6 continua precisando de
`AFTER_COMMIT` exato, e a timeline continua sendo um registro por passo.

#### O que a proposta cria, e ninguém decidiu ainda

**Um resultado negativo passa a ter quatro causas, e a plataforma não distingue nenhuma
delas hoje.** "Zero violações" PODE significar: a anomalia é impossível naquela
configuração; a anomalia é possível e a janela nunca foi atingida; a anomalia ocorreu e
o oráculo não a viu, porque ele lê o estado final quiescente (
[`Q-0002-3`](../questions/Q-0002-3.md) ); ou os workers nunca se sobrepuseram, porque o
pool de conexões os serializou. A primeira é o resultado que o experimento busca. As
outras três são defeitos do instrumento com a mesma aparência.

**A plataforma mede a consequência, e passaria a precisar medir a exposição.** Uma
atualização perdida exige que dois workers leiam o mesmo valor antes que qualquer um
escreva. Esse evento é contável a partir do log de observações que o ADR-0001 já obriga
o runtime a emitir. Contá-lo separa "a janela não abriu" de "a janela abriu e nada
aconteceu" — que é a distinção que converte um zero em conhecimento. Nenhum documento do
repositório nomeia essa métrica.

**Um resultado negativo precisa de regra de parada e de declaração de confiança.** Com N
tentativas e zero violações, o limite superior da taxa fica em torno de `3/N` com 95% de
confiança. Sem uma regra escrita, cada execução escolhe o próprio N, e dois relatórios
com o mesmo veredito afirmam coisas diferentes. Quem escolhe N, e o que o relatório
afirma quando o zero aparece, é decisão nova.

**O veredito ganha um terceiro formato.** A fila prevê booleano e curva. Taxa com
intervalo não é nenhum dos dois: ela tem um número e uma incerteza, e a incerteza
precisa aparecer no relatório. A decisão dos formatos de veredito muda de escopo por
causa disso.

**A falha intermitente entra no pipeline.** Um experimento probabilístico num workflow
que precisa ficar verde é um teste instável por construção. A tensão 2 do plano chama a
falha intermitente de "o pior resultado possível num instrumento de medida", e a
exigência de nascer entregando põe esse custo no primeiro commit, não depois.

#### Três desfechos, e nenhum é obviamente certo

**Remoção da barreira.** O agendamento sai, o ADR-0003 é descontinuado ainda `Proposto`,
e o E2 deixa de existir como experimento separado. Custo: a plataforma passa a afirmar
apenas o que observou, e perde o poder de mostrar a intercalação que causa o fenômeno —
que é a exigência pedagógica do cenário 25.

**Rebaixamento a instrumento de diagnóstico.** A frequência produz o resultado; a
barreira responde à pergunta que o resultado negativo deixa aberta. Se a execução por
frequência não produzir violação, a mesma configuração roda com a intercalação forçada:
violação ali significa carga insuficiente na primeira; ausência nas duas significa que a
anomalia é impossível naquela configuração. A barreira vira o **controle positivo** do
experimento, e o ADR-0003 continua válido com a seção `## Contexto` reescrita.

**Eixo coigual.** Frequência e barreira convivem como duas resoluções do experimento, do
mesmo jeito que o ADR-0001 fez com alta e baixa resolução da operação. Custo: todo
experimento passa a ter dois braços obrigatórios, e o laboratório carrega as duas
máquinas desde o MVP.

Registrado em 2026-07-31, no turno em que a proposta foi apresentada, antes de qualquer
resposta a ela.

O segundo desfecho foi o escolhido, e o
[ADR-0004](0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md) o fixou
junto dos instrumentos de diagnóstico. Ele foi aceito em 2026-08-01.

O [ADR-0003](0003-a-linguagem-do-agendamento.md) foi aceito no mesmo dia, com a seção
`## Contexto` reescrita para justificá-lo pela execução de controle. O parágrafo acima
que o proibia de ser aceito registra o bloqueio vigente em 2026-07-31, e deixou de valer
quando o ADR-0004 escolheu o desfecho.

O debate da aceitação mudou dois pontos do que está escrito acima. A exposição de
referência é contada no **controle negativo**, e não na execução medida: uma estratégia
que serializa fecha a janela, e ler esse zero como carga fraca condenaria a estratégia
mais protetora. E o veredito `sem exposição`, previsto aqui, não existe — o controle
negativo já detectava aquele caso, e o lugar foi ocupado por `janela mal declarada`.

## De onde esta fila veio

As duas origens continuam no repositório, e as duas viram lápide pela decisão `C-2`.

| Origem                                                                                                                 | O que ficou lá                                  |
|------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`README.md`](README.md), seção "Fila de decisões"                                                                     | uma lápide; o conteúdo veio inteiro para cá     |
| [`arquivo/proposta-2026-08-03/decisoes-pendentes.md`](arquivo/proposta-2026-08-03/decisoes-pendentes.md), Blocos 0 a 6 | o texto original, congelado; a fila viva é esta |

**A segunda não pôde ser esvaziada, e o motivo é técnico.** Nove citações por número de
linha apontam para `decisoes-pendentes.md` a partir dos ADRs 0008 e 0009, a maior em
`:1879`. O corpo de um ADR aceito NÃO PODE ser editado, então qualquer edição que
desloque uma linha até 1879 quebra citação que ninguém pode corrigir. Aquele arquivo é
append-only, e o texto dos blocos permanece lá como registro histórico congelado.
