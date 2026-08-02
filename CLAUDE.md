# CLAUDE.md

Guia para o Claude Code (claude.ai/code) ao trabalhar neste repositório.

## Não existe código neste repositório

Não há `pom.xml`, nenhuma classe Java, nenhum `docker-compose.yml`. **Não há comando de
build, de teste ou de execução.** Se você tentar `mvn test`, `docker compose up` ou
qualquer coisa parecida, vai falhar — e o motivo não é configuração faltando.

A árvore versionada tem 28 arquivos, todos documentação ou configuração de editor. Isso é
deliberado: a especificação vem antes do código.

Quando o código existir, a stack é Java 25, Spring Boot 4.x, PostgreSQL, Docker. O
RabbitMQ entra na etapa 5. O pacote raiz Java, o build e o número de módulos ainda **não
foram escolhidos** — é a decisão de arquitetura mínima na fila de `docs/adr/README.md`.

## O que este projeto é

Uma plataforma experimental para reproduzir, observar e comparar problemas conhecidos de
sistemas distribuídos. Não é uma aplicação de negócio: não existe pedido, pagamento,
cliente ou estoque. O escopo cobre 42 fenômenos, de lost update a cascading failure.

O documento que define tudo é
[`docs/plano-do-laboratorio.md`](docs/plano-do-laboratorio.md). Leia-o antes de propor
qualquer coisa.

## Como o planejamento funciona aqui

**Use automaticamente a skill `/feature-planning` antes de planejar, refinar, estimar
ou propor a implementação de uma funcionalidade ou atualização.** A skill cria e valida
os artefatos de especificação deste repositório.

**Desde 2026-08-01 o ADR deixou de ser a forma principal de documentação.** O padrão é
**Feature Card mais Example Mapping**, com Gherkin para o comportamento estabilizado e
contratos para o que atravessa fronteira de processo.

A divisão que organiza tudo:

> **O ADR guarda o porquê da escolha. O Feature Card guarda o quê do comportamento.**

O motivo da mudança está medido: o repositório acumulou 3.874 linhas de documentação para
zero linha de código, e os ADRs passaram a carregar três naturezas no mesmo arquivo —
decisão arquitetural, regra de negócio e tabela de decisão. Só a primeira é decisão.

| Artefato        | Onde vive                                 | O que responde                                                            |
|-----------------|-------------------------------------------|---------------------------------------------------------------------------|
| Feature Card    | `docs/features/<slug>/feature-card.md`    | o quê da capacidade, em no máximo 700 palavras                            |
| Example Mapping | `docs/features/<slug>/example-mapping.md` | regras, exemplos concretos, perguntas em aberto, itens adiados            |
| BDD             | `docs/features/<slug>/behavior.feature`   | comportamento externo observável, em Gherkin português                    |
| Contrato        | `docs/contracts/openapi/`, `asyncapi/`    | o que atravessa fronteira de processo — **só quando a interface existir** |
| Integrações     | `docs/architecture/integrations.md`       | a matriz, separando fato de hipótese                                      |
| ADR             | `docs/adr/`                               | o porquê de uma decisão arquitetural durável, e o que foi descartado      |

O processo completo está em
[`docs/specification-process.md`](docs/specification-process.md). O índice das capacidades
está em [`docs/features/README.md`](docs/features/README.md). **Leia os dois antes de
escrever qualquer artefato novo.**

### O teste que separa ADR de Feature Card

| Pergunta                                                | Sim → ADR | Sim → Feature Card |
|---------------------------------------------------------|-----------|--------------------|
| Existe alternativa que alguém defenderia com argumento? | sim       | —                  |
| A escolha restringe o que se pode construir depois?     | sim       | —                  |
| A frase descreve o que o sistema faz, e é verificável?  | —         | sim                |
| Um teste poderia falhar por causa dela?                 | —         | sim                |

Uma regra que caiba nas duas colunas indica um ADR carregando comportamento. Escreva o ADR
com o porquê e o card com o quê, e faça o card citar o ADR por arquivo e linha.

### Convenções dos artefatos de especificação

- **Um Feature Card cobre uma capacidade**, nunca um endpoint, uma classe ou uma tarefa
  técnica. Um card acima de 700 palavras está cobrindo mais de uma — divida.
- **Um card por oráculo, não por experimento.** É o oráculo que define o comportamento
  observável. E1 e E3 compartilham o mesmo oráculo e vivem num card só.
- **Toda regra do card leva a evidência**, com arquivo e linha. O que não puder ser
  confirmado entra como `Pergunta em aberto`, nunca como fato.
- **Não converta exemplo em Gherkin antes de as perguntas estarem explícitas.** Um cenário
  escrito sobre regra em debate congela a versão errada dela. Regra debatida vira exemplo;
  só exemplo estabilizado vira cenário.
- **Gherkin em português** (`# language: pt`), descrevendo comportamento externo. Nome de
  classe, de tabela e de coluna não aparecem num cenário.
- **Nenhuma dependência de BDD entra no projeto por causa disso.** Enquanto não houver
  código, os `.feature` são a especificação viva, e cada cenário está marcado
  `@teste-ausente`.
- **Um contrato é criado quando a interface existir**, nunca antes. Não crie diretório
  vazio: uma pasta `openapi/` sem conteúdo afirma que existem APIs a documentar.
- **O que estiver formalizado num contrato NÃO DEVE ser repetido em Markdown.**

### A regra dura vale para todo artefato

> **Nada que importa pode existir apenas na conversa.**

O contexto da conversa é limpo entre uma sessão e outra. Toda objeção, alternativa
descartada ou pendência é escrita no arquivo — na seção `## Questões em aberto` do ADR, ou
na seção de perguntas em aberto do Example Mapping — **no mesmo turno em que é levantada**,
antes de responder ou perguntar qualquer coisa. Uma objeção que fica só no chat desaparece
no próximo compact, em silêncio.

## O processo de ADR, quando um ADR for escrito

O processo continua valendo sem alteração. O que mudou é a frequência com que ele é
acionado.

### Um ADR por vez, nunca em lote

A primeira série do repositório rascunhou seis ADRs de uma vez, em paralelo. Escritos sem
se ver, produziram três contradições entre si e nenhum chegou a ser debatido. O custo foi
inteiramente perdido.

**Não rascunhe ADRs antecipadamente.** A fila de decisões em `docs/adr/README.md` lista o
que precisa ser decidido e em que ordem, **sem números atribuídos** — o número é atribuído
quando o ADR é escrito.

### Estados e aceitação

Nenhum ADR é aceito por omissão, e nenhum é aceito sem aprovação explícita do usuário.

Cada questão da seção `## Questões em aberto` tem um status, e só dois deles bloqueiam:
`aberto` e `aberto (crítico)`. `encaminhado` marca a questão que pertence a outro ADR já
na fila; `resolvida` marca a questão fechada durante o debate por algo que não é decisão
daquele ADR.

Ao aceitar, remova a seção `## Questões em aberto` e mova o que foi decidido para
`## Decisão` ou `## Consequências`. Antes de remover, **transporte cada questão
`encaminhado`** — inteira, no mesmo commit — para a seção `## Questões encaminhadas` de
`docs/adr/README.md`, onde ela recebe o identificador `Q-NNNN-K`. Sem o transporte, o
enunciado é apagado e a linha da fila que o citava fica pendurada.

Um ADR **aceito** nunca é editado nem apagado. Para mudar a decisão, escreva um ADR novo e
marque o antigo como `Substituído por ADR-NNNN`. Enquanto estiver `Proposto`, editar é
permitido.

**Substituição e subsunção são diferentes.** Um ADR que contradiga um aceito o substitui.
Um ADR que apenas recorte o alcance de uma regra antiga a **subsume**: o antigo permanece
`Aceito` e o texto dele não é tocado. As três exigências da subsunção estão em
`docs/adr/README.md`.

### Duas séries de ADR

A numeração foi reiniciada em 2026-07-28. Um mesmo número existe em duas séries.

| Forma de citar | Onde vive           | O que é                                  |
|----------------|---------------------|------------------------------------------|
| `ADR-0001`     | `docs/adr/`         | série corrente                           |
| `arquivo/0001` | `docs/adr/arquivo/` | primeira série, arquivada, nenhum aceito |

**Sempre use o prefixo `arquivo/` ao citar a série antiga.** Sem ele a referência é
ambígua. Os documentos do arquivo **nunca são editados** — eles registram o que se pensava
naquela data.

### Convenções de ADR

A lista completa está em `docs/adr/README.md`, seção `## Convenções`, e o esqueleto em
`docs/adr/0000-template.md`. **Leia os dois antes de escrever um ADR.** O que mais pega:

- Numeração sequencial de quatro dígitos, nunca reutilizada dentro da série corrente.
  Arquivo: `NNNN-titulo-em-kebab-case.md`.
- **`## Decisão` carrega só o quê.** O porquê vive em `## Justificativa`.
- **`## Trade-offs` é obrigatório**, no formato "o benefício X foi aceito em troca do custo
  Y". Um ADR sem trade-off explícito é propaganda.
- A seção `## Alternativas consideradas` costuma valer mais que a `## Decisão`. Cada
  alternativa leva um parágrafo começando com `**Descartada.**` e um motivo **técnico**.
  Não construa espantalhos: se a alternativa tem argumento legítimo, reconheça-o.
- `## Quando esta decisão deixa de valer` precisa de sinal concreto e observável.
- `## Questões em aberto` é a última seção, e abre com uma tabela-resumo de status.

A skill global `create-adr` **não** governa a estrutura aqui — o template deste repositório
governa. O que vale dela é o guia de escrita
(`~/.claude/skills/create-adr/references/style-guide.md`), com uma exceção deliberada: a
RFC 2119 é escrita em português, não em inglês.

## Convenções de escrita, válidas em todo documento

- Português do Brasil, com acentuação correta. Frases de 10 a 20 palavras. Voz ativa. Uma
  ideia por frase. Linhas quebradas em ~88 colunas.
- Um conceito tem **um** nome. Escolhido "passo", nunca alterne para "etapa" ou "fase".
- Requisito normativo usa RFC 2119 traduzida, em caixa alta: `DEVE`, `NÃO DEVE`,
  `DEVERIA`, `NÃO DEVERIA`, `PODE`. Nunca como ênfase.
- Lista de palavras proibidas (`simples`, `robusto`, `eficiente`, `geralmente`,
  `provavelmente`…) em `docs/adr/README.md`. Explique o motivo em vez de qualificar com
  advérbio.
- Todo fluxo apresentado vai **também** como diagrama Mermaid, junto do parágrafo que o
  descreve. `sequenceDiagram` para ordem no tempo, `flowchart` para topologia e hierarquia.
  Excalidraw só para o que o Mermaid não expressa, exportado como `.excalidraw.svg`.
- Sem emojis. Sem linguagem de marketing.
- Um link Markdown longo PODE ultrapassar 88 colunas — quebrá-lo no meio o inutiliza.

## Arquitetura conceitual

Ler só um documento não basta; estas cinco ideias atravessam todo o projeto.

**Uma operação é uma sequência de passos.** Barreiras determinísticas, fault injection em
pontos nomeados e a timeline são a mesma exigência: existe uma fronteira observável e
controlável entre passos consecutivos. O runtime executa os passos e, em cada fronteira,
consulta o escalonador, consulta o injetor de falha e emite uma observação. O que é
sintético é apenas o agendamento — o SQL, a transação e o isolamento são reais. É a decisão
do **ADR-0001**, `Aceito`, especificada em
[`docs/features/observacao-passo-a-passo/`](docs/features/observacao-passo-a-passo/feature-card.md).

**Dois planos.** O Control Plane é o sistema sob teste; o Lab Plane é o instrumento que o
mede. Confundir os dois invalida qualquer conclusão — um bug no instrumento vira um falso
resultado de consistência. Nas primeiras etapas os dois vivem na **mesma JVM**, o que torna
a separação por teste executável mais necessária, não menos. O runtime chama a operação; a
operação nunca chama o runtime.

**Cinco grupos, classificados pela causa.** Intercalação, Entrega, Escrita parcial,
Saturação, Posse no tempo. A classificação é pela fonte de não determinismo, não pela
tecnologia, porque é a causa que determina o que a plataforma precisa saber controlar.

**O veredito tem três formatos.** Booleano (a invariante foi violada?) para os grupos A, B,
C e E. **Curva** para o grupo D — backpressure não tem estado errado, tem uma fila crescendo
e um limiar que alguém precisa declarar. E **taxa com limite de confiança**, acrescentada
pelo ADR-0004: um número mais uma incerteza, que não é caso particular de nenhum dos outros
dois. Como os três convivem é decisão em aberto na fila.

**O grupo de controle é obrigatório.** A estratégia `NONE` não é um estado provisório: se
`NONE` não violar a invariante, o experimento não tem carga suficiente e o resultado das
outras estratégias não significa nada. O ADR-0004 tornou isso a primeira linha da
classificação do veredito zero.

## Regra pedagógica

> Nunca introduza primeiro a solução. Introduza primeiro o problema.

Para estudar Outbox, não comece implementando Outbox. Construa o experimento em que o
commit e a publicação são operações independentes, provoque a falha entre elas, observe a
inconsistência — e só então introduza o Outbox e rode o mesmo experimento.

```
PROBLEMA → CAUSA → SOLUÇÃO → TRADE-OFF
```

Vale para os 42 fenômenos, sem exceção. É por isso que `version` não está no esquema.

## Regras estruturais que valem sempre

- **Nenhuma tecnologia entra por estar disponível.** Cada uma entra quando um experimento
  não puder ser executado sem ela. Antes de propor Valkey, RabbitMQ ou OpenTelemetry, diga
  qual limitação concreta da stack atual ela resolve.
- **Nenhuma aleatoriedade não semeada.** `Math.random()`, `java.util.Random` e
  `ThreadLocalRandom` são proibidos fora do componente de aleatoriedade semeada. Uma chamada
  esquecida quebra a reprodutibilidade em silêncio, meses depois.
- **O tempo é injetável.** `Instant.now()`, `LocalDateTime.now()` e
  `System.currentTimeMillis()` só em adaptador de relógio. Sem isso, expiração de lease e
  clock skew ficam impossíveis de testar.
- **Nenhuma sincronização de JVM no sistema sob teste.** `synchronized`, `ReentrantLock` e
  `AtomicInteger` mascaram exatamente os fenômenos do grupo A. A exceção é a estratégia
  `JVM_LOCK`, que existe **como experimento** para provar que ela falha com duas instâncias.
- **Cada worker tem sua própria conexão.** Se o pool serializar dois workers, o experimento
  produz um falso negativo silencioso.
- **`experiments/` guarda definições; `docs/experiments/` guarda resultados.** Os dois
  entram no Git — juntos, o histórico vira um caderno de laboratório. (A fonte de verdade
  entre arquivo versionado e Experiment Designer na UI é tensão aberta: plano, seção 11.)

As três primeiras são hoje **texto, não regra executável**. `Q-0002-1` registra isso, e a
guarda pertence à decisão de arquitetura mínima.

## Estado atual

### Especificação

Quatro capacidades estão especificadas e **nenhuma implementada**. O índice está em
[`docs/features/README.md`](docs/features/README.md):

| Capacidade                        | Cobre                                                          |
|-----------------------------------|----------------------------------------------------------------|
| `observacao-passo-a-passo`        | o runtime de passos, fronteiras, log e prova de equivalência   |
| `execucao-de-experimento`         | o ciclo de quatro execuções e a classificação do veredito zero |
| `deteccao-de-atualizacao-perdida` | E1 e E3, o oráculo exato do contador                           |
| `deteccao-de-protecao-inerte`     | E5, o oráculo do predicado de capacidade                       |

**O E4 não tem card, de propósito.** O veredito em formato curva não tem forma decidida, e
um card agora seria majoritariamente pergunta em aberto. O motivo está registrado no índice.

**Nenhum contrato existe.** Nenhuma interface existe para contratar — `docs/contracts/README.md`
lista os quatro gatilhos que criam cada um.

### Decisões

**Os quatro ADRs da série corrente estão `Aceito`: 0001 e 0002 de 2026-07-29, 0004 e 0003
de 2026-08-01.** Nenhum pode ser editado. Nenhum ADR está `Proposto` hoje.

| ADR  | O que fixou                                                                             |
|------|-----------------------------------------------------------------------------------------|
| 0001 | o passo como unidade de execução, observação e injeção de falha                         |
| 0002 | o domínio mínimo, o oráculo exato e o oráculo do predicado                              |
| 0003 | a linguagem do agendamento: precedência entre eventos, encontro, sete recusas           |
| 0004 | a barreira rebaixada a controle positivo; a taxa como veredito; a classificação do zero |

Três consequências mudam o que se pode propor daqui em diante:

- **O oráculo exato é `perdidas = commits − (value_final − value_inicial)`**, onde `commits`
  conta passagens pela fronteira `AFTER_COMMIT`, por tentativa. Não é `sucessos` — contar
  retornos de operação cancela perda real contra falha injetada depois do commit.
- **Toda execução medida exige calibração antes**, com uma estratégia sem perda, em que
  `commits` DEVE igualar `value_final − value_inicial`. Qual é essa estratégia ainda não foi
  decidido.
- **`version` não existe no esquema.** Quem a acrescenta é o ADR de estratégias de
  concorrência, junto da política que a lê. O esboço ilustrativo do ADR-0001 lê uma coluna
  que o esquema não tem — o esboço não é normativo.

As questões encaminhadas são `Q-0001-1` a `Q-0001-4`, `Q-0002-1` a `Q-0002-4` e `Q-0004-2`
a `Q-0004-8`, e vivem em `docs/adr/README.md`, seção `## Questões encaminhadas`. **Cite-as
por esse identificador**, nunca por "a questão K do ADR-NNNN". Cada uma tem destino nomeado
na fila. A `Q-0001-3` está `resolvida por ADR-0002`, e o enunciado permanece lá de propósito.

As perguntas levantadas durante o Example Mapping vivem nos próprios `example-mapping.md`, e
**não** foram transportadas para a fila de ADRs.

### Pendências de processo

- **O papel futuro da fila de decisões de `docs/adr/README.md` não foi decidido.** Das onze
  linhas, quatro são ADR legítimo; o restante é comportamento enfileirado como arquitetura.
  Podá-la exige decisão explícita do usuário.
- **Não está escrito se um Feature Card pode contradizer um ADR aceito**, nem quem aprova um
  card. As duas lacunas estão registradas em `docs/specification-process.md`.

### Árvore

A árvore só tem `docs/`. O esqueleto herdado das decisões arquivadas foi apagado nos commits
`83fcfc9` e `e1c88ae` — inclusive o `deploy/`, para onde o ArgoCD do homelab aponta. O
`Application` de lá está em `ComparisonError` hoje. O conserto acompanha as decisões de
arquitetura mínima e de entrega contínua.

## Este repositório é entregue no homelab

O laboratório é a primeira carga de trabalho da Camada 8 do repositório
[`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure), e a exigência é
que um serviço **nasça já entregando**: pipeline e CI/CD no mesmo commit que cria o módulo,
nunca retrofitados. O contrato está na **ADR 0017 daquele repositório**, que está
**Aceita** — leia-a antes de propor qualquer coisa sobre build, empacotamento ou deploy.

O essencial dela: GitHub Actions exclusivamente, em runner hospedado; imagem no GHCR com
`GITHUB_TOKEN` efêmero e tag = SHA do commit, nunca `latest`; manifests Kustomize em
`deploy/` **deste** repositório, bumpados pelo workflow da `master`; ArgoCD por polling
(~3 min); nenhum Secret aqui — eles ficam cifrados com SOPS/KSOPS no homelab e são
referenciados por nome.

A matriz completa de integrações, separando fato de hipótese, está em
[`docs/architecture/integrations.md`](docs/architecture/integrations.md). Três cuidados que
valem sempre:

- **A ADR 0017 é de 2026-07-26 e o replanejamento daqui é de 2026-07-28.** Ela descreve o
  laboratório como "monorepo de microsserviços JVM" — a arquitetura **arquivada**. Ela também
  escolhe **Gradle** e **Toxiproxy**, que nunca foram debatidos aqui. Não absorva nada disso
  em silêncio: o inventário está em `docs/plano-do-laboratorio.md`, seção 12.
- **Kubernetes é destino de entrega, não objeto de estudo.** Nenhum dos 42 fenômenos é
  reproduzido por um recurso do cluster.
- **O orquestrador reage ao que o experimento faz.** Um experimento que mata o processo de
  propósito (etapa 6) roda sob um `Deployment` que o reinicia, com `selfHeal: true`. Isso é
  a confusão Control Plane / Lab Plane um nível abaixo, e não tem solução decidida.

## Ao trabalhar aqui

- Questione decisões quando fizer sentido, e explique trade-offs. O usuário pediu
  explicitamente mentoria arquitetural, não geração de código.
- Ao surgir uma decisão relevante: apresente o problema, apresente as alternativas, explique
  os trade-offs, recomende uma — e espere que a decisão seja consciente. Não decida em
  silêncio, e não projete a solução final antecipadamente.
- **Prefira registrar uma questão em aberto a inventar uma decisão para fechar uma lacuna.**
  No processo deste repositório, a primeira vale mais que a segunda.
- **Não invente integração, contrato ou regra.** Toda afirmação relevante leva evidência com
  caminho de arquivo e linha. O que não puder ser confirmado é `Pergunta em aberto`, nunca
  fato.
- A LLM gera perguntas, contraexemplos e lacunas. **Regra de negócio e decisão são aprovadas
  por pessoa, explicitamente.**
- Ao mexer em arquivos, faça `git add` apenas dos arquivos relacionados e gere um único
  commit em Conventional Commits (skill `commit`).
