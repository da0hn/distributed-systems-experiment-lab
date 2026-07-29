# ADR-0010: Plataforma local com profiles do Docker Compose

- **Estado:** Proposto
- **Data:** 2026-07-26
- **Etapa do roadmap:** 0
- **Relacionado:** ADR-0001, ADR-0004, ADR-0006, ADR-0007, ADR-0011

## Contexto

O laboratório roda numa máquina só. Um homelab, com Docker e Docker Compose.

A stack completa tem PostgreSQL, RabbitMQ, Prometheus, Grafana, Loki, Tempo,
OpenTelemetry Collector, os contêineres de aplicação e o frontend. São doze ou mais
processos, e quase todos consomem memória em repouso.

O roadmap consome essa stack em camadas. A Etapa 1 mede estratégias de concorrência
contra um banco: ela precisa de PostgreSQL e nada mais. A Etapa 2 introduz o Outbox e o
relay (ADR-0007): entra o RabbitMQ. A Etapa 4 torna o experimento uma entidade com
asserções sobre métricas (ADR-0004): entra a observabilidade. A Etapa 7 traz o frontend.

Duas restrições vêm de outros ADRs e limitam o que esta decisão pode fazer.

O ADR-0004 exige reprodutibilidade. Um experimento é reexecutado meses depois com a
mesma semente e precisa produzir o mesmo veredito. A plataforma faz parte do sujeito do
experimento, não do cenário.

O ADR-0006, regra 8, torna o relógio injetável para permitir cenários de clock skew.
Contêineres Docker no mesmo host **compartilham o relógio do kernel**. A plataforma não
tem como dar tempos diferentes a dois contêineres.

## Problema

Subir tudo para rodar um teste de domínio de 3 ms é desperdício, e o desperdício diário
vira atrito. Atrito faz o laboratório ser usado menos.

Subir de menos é pior. Um experimento executado sem o Collector produz um relatório sem
as métricas que a asserção do ADR-0004 consulta. O experimento não falha: ele responde a
pergunta errada.

As forças em conflito:

- O ciclo de desenvolvimento diário precisa de segundos, não de minutos.
- Um experimento precisa do ambiente **completo e idêntico** ao da execução anterior.
- A memória do homelab é finita e compartilhada com o resto do que roda nele.
- Um ambiente montado à mão diverge sem avisar. A divergência só aparece no veredito.

A pergunta é: como subir só o necessário sem que "o necessário" vire uma escolha tomada
de memória a cada execução?

## Decisão

A plataforma local vive em `platform/compose/`, num único arquivo `docker-compose.yml`
com **profiles**. Cada camada da stack é um profile. A etapa do roadmap determina o
conjunto de profiles, e o conjunto é declarado em preset, nunca digitado de memória.

### Mecanismo

Um serviço sem a chave `profiles` sobe sempre. Um serviço com `profiles` só sobe quando
o profile é ativado.

```yaml
services:
  postgres:                       # sem profiles — é a base, sobe sempre
    image: ${POSTGRES_IMAGE}
    healthcheck: { test: ["CMD-SHELL", "pg_isready -U postgres"], interval: 2s }

  rabbitmq:
    profiles: ["messaging"]
    image: ${RABBITMQ_IMAGE}
```

### Os seis profiles

| Profile         | Contém                                              | Existe para                    |
|-----------------|-----------------------------------------------------|--------------------------------|
| *(base)*        | `postgres`, `postgres-init` (one-shot)              | tudo que toque estado          |
| `messaging`     | `rabbitmq`, `rabbitmq-init` (one-shot)              | Outbox, Inbox, DLQ (ADR-0007)  |
| `control`       | os N contêineres do Control Plane (ADR-0011)        | o sistema sob teste            |
| `lab`           | `experiment-service`, `chaos-service`               | o instrumento que mede         |
| `observability` | `otel-collector`, `prometheus`, `grafana`, `loki`, `tempo` | asserções do ADR-0004   |
| `replicas`      | réplicas dos serviços do Control Plane              | concorrência entre processos   |
| `frontend`      | `frontend`                                          | árvore causal (Etapa 7)        |

`control` e `lab` são profiles separados porque os dois planos são separados (ADR-0006,
regra 6). Subir o Control Plane sem o Lab Plane é a configuração normal da Etapa 2: o
relay é observado por log e por consulta SQL, não por instrumento.

`replicas` não é um profile de "mais capacidade". Ele existe para produzir a
concorrência que uma única JVM não produz: duas réplicas do relay disputando a mesma
linha de `outbox` sob `FOR UPDATE SKIP LOCKED`, duas réplicas do mesmo caso de uso
disputando o mesmo `resource`.

### A tabela que é o coração deste ADR

| Etapa | Tema                          | Profiles ativos                            | Contêineres |
|-------|-------------------------------|--------------------------------------------|-------------|
| 0     | Domínio, origens, monorepo    | nenhum — o domínio é `new` + `assert`      | 0           |
| 1     | Concorrência, ArchUnit        | *(base)*                                   | 1 + init    |
| 2     | Outbox e relay                | *(base)* + `messaging` + `control`         | 2 + N       |
| 3     | Inbox, dedupe, ordem, DLQ     | Etapa 2 + `lab`                            | 2 + N + 2   |
| 4     | Experimentos com semente      | Etapa 3 + `observability`                  | Etapa 3 + 5 |
| 5     | Workflow, saga, lease         | Etapa 4 + `replicas`                       | Etapa 4 + K |
| 7     | Frontend da árvore causal     | Etapa 5 + `frontend`                       | Etapa 5 + 1 |
| 10    | Homelab                       | fora da competência deste ADR              | —           |

`N` é o número de contêineres do Control Plane. Ele é **parâmetro**, não premissa: o
ADR-0011 o define. Nenhum profile acima muda de nome ou de significado conforme o valor
de `N`. `K` depende de quantos serviços do Control Plane têm réplica, o que também é
consequência do ADR-0011.

A Etapa 1 sobe **um contêiner**. Esse é o ponto inteiro desta decisão.

### Os presets são obrigatórios

O Compose ativa profiles por `--profile` ou por `COMPOSE_PROFILES`. O laboratório usa a
segunda forma, num alvo de `make` por etapa:

```makefile
etapa-2: ; COMPOSE_PROFILES=messaging,control docker compose \
             --env-file ../versions.env up -d
```

Isso não é açúcar. O Compose trata `depends_on` sobre um serviço de profile inativo de
forma que já variou entre versões — em algumas ele ativa o profile da dependência, em
outras ele falha. **O laboratório não depende desse comportamento.** Cada combinação
válida é declarada por extenso num preset, e um profile nunca ativa outro
implicitamente.

Um experimento do ADR-0004 registra no relatório o conjunto de profiles ativo. Um
relatório sem esse campo não é reproduzível, porque não diz o que estava de pé.

### O contrato de versões

Toda imagem é fixada em **versão exata mais digest**. Nunca `latest`. Nunca tag
flutuante de minor (`postgres:16` é proibido tanto quanto `postgres:latest` — ele flutua
no patch).

```
# platform/versions.env — fonte única de verdade
POSTGRES_IMAGE=postgres:16.4@sha256:0f3b...
RABBITMQ_IMAGE=rabbitmq:3.13.7-management@sha256:9a12...
```

Isto não é higiene genérica de Docker. É exigência direta do ADR-0004, e a cadeia é
concreta:

1. O ADR-0001 decidiu o modelo `DERIVED`, cuja única saída correta é `SERIALIZABLE`
   com retry no `40001`.
2. `SERIALIZABLE` no PostgreSQL é SSI. O SSI decide abortar com base em locks de
   predicado, cuja granularidade depende de parâmetros do servidor e do plano escolhido
   pelo planejador.
3. Locks de predicado escalam de linha para página e de página para relação quando a
   memória de `max_pred_locks_per_transaction` acaba. A escalada aumenta o falso
   positivo, ou seja, aborta transações que não conflitavam.
4. Planejador, defaults e o próprio SSI mudam entre versões maiores do PostgreSQL.

Consequência: a taxa de `40001` de um experimento é uma propriedade **da versão do
PostgreSQL**, não só do código. Trocar `16.4` por `17.2` sem trocar uma linha de Java
muda o número que o relatório publica. Com `latest`, a troca acontece sozinha, em
silêncio, num `docker compose pull` qualquer, e o relatório antigo passa a descrever um
sistema que não existe mais.

O digest existe porque a tag, em tese, é mutável: o publicador pode reescrever
`16.4`. O digest não pode. A tag legível fica ao lado do digest para que o arquivo
continue lido por humanos.

Atualizar uma versão é um commit próprio, com um experimento reexecutado antes e depois.
A diferença entre os dois relatórios é o resultado da atualização.

### Isolamento de dados entre serviços

**Um banco. Um schema por serviço. Um `ROLE` por serviço. `GRANT` só no próprio
schema.**

```sql
CREATE ROLE resource_svc LOGIN PASSWORD :'resource_pwd';
CREATE SCHEMA IF NOT EXISTS resource AUTHORIZATION resource_svc;
ALTER ROLE resource_svc SET search_path = resource;
-- nenhum GRANT em outro schema: o default do PostgreSQL já nega
```

A alternativa era um banco por serviço. Ela foi descartada por três motivos, e nenhum
deles é custo de memória:

- **Não protege mais.** O que se quer impedir é um `JOIN` entre o schema de um serviço e
  o de outro. A ausência de `GRANT` já o impede, com o mesmo rigor: a consulta falha com
  `42501`, no servidor, antes de qualquer lógica de aplicação. Bancos separados dão a
  mesma negação por um caminho diferente.
- **Custa uma capacidade que o laboratório usa.** O `experiment-service` precisa fechar
  o experimento com consultas de veredito sobre o estado final de todos os serviços
  (ADR-0004). Com um banco, isso é um `ROLE` `experiment_reader` com
  `SELECT` em todos os schemas e uma conexão. Com bancos separados, são N conexões e
  nenhuma consulta que cruze os dois — a asserção de safety teria que ser montada na
  aplicação, dentro do próprio instrumento.
- **Não custa nada em fidelidade transacional.** O PostgreSQL não tem transação entre
  bancos. Ele também não tem transação entre schemas de serviços diferentes, porque o
  `GRANT` a proíbe. As duas montagens produzem exatamente a mesma fronteira
  transacional, que é o que o ADR-0011 vai decidir.

O `experiment_reader` é a única leitura que cruza schemas. Ela é legítima e não fere a
regra 6 do ADR-0006: o Lab Plane observa o Control Plane, e observação não é
dependência. A seta é de leitura, e ela nasce do plano certo.

**A decisão é verificável.** Para cada par ordenado de serviços `(A, B)`, um teste de
integração conecta como o `ROLE` de `A`, faz `SELECT 1 FROM <schema_de_B>.<tabela>` e
exige `SQLSTATE 42501`. Os N × (N − 1) casos são gerados a partir do manifesto descrito
abaixo, então o teste cresce sozinho quando um serviço nasce. Um `GRANT`
largo demais quebra a build no mesmo commit em que foi escrito.

### Como um serviço nasce

Um serviço novo exige um schema, um `ROLE`, um `GRANT`, um bloco no compose, uma
exchange, uma fila e uma DLQ. Sete passos. À mão, um deles é esquecido, e o sintoma
aparece meses depois como um erro de permissão sem contexto, ou como um evento que some
sem DLQ.

A decisão: **nada disso é escrito à mão.** Existe um manifesto declarativo, e o resto é
gerado.

```yaml
# platform/services.yaml — o único arquivo editado por uma pessoa
services:
  - name: resource
    plane: control
    schema: resource
    role: resource_svc
    messaging: { exchange: resource.events, dlq: true }
```

`tools/new-service` lê o manifesto e gera três artefatos, todos com um cabeçalho
`# GERADO — não edite; edite platform/services.yaml`:

| Gerado                                     | A partir de           |
|--------------------------------------------|-----------------------|
| `platform/postgres/init/NN-<name>.sql`      | `schema`, `role`      |
| fragmento de serviço do `docker-compose.yml`| `name`, `plane`       |
| `platform/rabbitmq/definitions.json`        | `messaging`           |

A verificação fecha o ciclo: a build regenera tudo e falha se `git diff` não estiver
vazio. Um passo esquecido deixa de ser um erro de permissão confuso e vira uma build
vermelha no commit que o causou.

Dois detalhes de implementação que já foram decididos porque são armadilhas conhecidas:

- **O init do PostgreSQL não roda via `docker-entrypoint-initdb.d`.** Aquele diretório
  só é executado quando o volume está vazio. Um serviço adicionado depois nunca teria
  seu schema criado num ambiente já existente, e o sintoma seria exatamente o erro de
  permissão que esta seção quer eliminar. O init roda num contêiner one-shot
  `postgres-init`, com `depends_on: service_healthy`, em **todo**
  `up`. Todo script é idempotente (`CREATE SCHEMA IF NOT EXISTS`, criação de `ROLE`
  guardada por `DO $$ ... $$`).
- **O RabbitMQ carrega `definitions.json` na inicialização**, via `load_definitions`.
  Uma fila nova exige reiniciar o contêiner. Isso é aceito: é explícito, é barato, e a
  alternativa — declarar fila em código de aplicação — esconderia a topologia dentro do
  serviço que o ADR-0007 quer manter observável.

### Clock skew não é competência da plataforma

Contêineres no mesmo host compartilham o relógio do kernel. Não existe profile capaz de
adiantar o relógio de um contêiner em 300 ms.

A plataforma faz a única parte que lhe cabe: injeta um deslocamento por contêiner, como
variável de ambiente (`LAB_CLOCK_OFFSET_MS`), e o adaptador de relógio do ADR-0006 o
aplica. O skew é simulado no processo, não no sistema operacional. A especificação desse
adaptador é a questão 2 do ADR-0006 e continua lá.

### Testcontainers e Compose coexistem

| Uso                                 | Ferramenta     | Por quê                             |
|-------------------------------------|----------------|-------------------------------------|
| Teste automatizado (`mvn test`, CI) | Testcontainers | isolamento; sem estado residual     |
| Experimento do ADR-0004             | Compose        | carga sustentada; observabilidade   |
| Desenvolvimento diário, frontend    | Compose        | ambiente de pé entre execuções      |
| Grafana, Loki, Tempo, Prometheus    | Compose apenas | não cabem no tempo de vida do teste |

A fronteira: **Testcontainers responde "o código está correto"; o Compose responde
"sob quais condições ele para de funcionar"**. É a mesma divisão que o ADR-0004 já faz
entre teste e experimento, agora aplicada ao ambiente.

Se as versões divergirem entre os dois, o teste e o experimento medem sistemas
diferentes, e o pior caso é o silencioso: o teste passa contra o PostgreSQL 17 e o
experimento aborta transações a mais contra o 16. Por isso **as duas ferramentas leem o
mesmo arquivo**.

`platform/versions.env` é a fonte única. O Compose o consome com `--env-file`. A build
Maven o converte em `platform-versions.properties`, empacotado como recurso de teste, e
os testes constroem contêineres a partir dele:

```java
new PostgreSQLContainer<>(DockerImageName.parse(PlatformImages.postgres()))
```

Duas guardas tornam isso verificável: a conversão falha se uma chave usada no compose
não existir no `versions.env`, e uma regra ArchUnit (ADR-0006) proíbe literal de string
em `DockerImageName.parse`. Não é possível fixar uma versão só no teste.

### O que este ADR não decide

Este ADR decide o **ambiente local de uma máquina**. A Etapa 10 é outro assunto e recebe
ADR próprio. Ficam explicitamente fora desta decisão: chart Helm, ArgoCD,
`Ingress`, `StorageClass`, gestão de segredo, topologia de nó, `HorizontalPodAutoscaler`
e política de rede.

**O Compose não é descartado quando o Kubernetes chegar.** Os dois convivem, porque
respondem perguntas diferentes. O Compose é o loop interno e o ambiente onde um
experimento roda de forma reproduzível numa máquina. O Kubernetes acrescenta o que uma
máquina só não oferece: partição de rede entre nós de verdade, `rolling update` durante
carga, e o efeito de um pod morto no meio de um relay. Descartar o Compose trocaria um
ciclo de segundos por um de minutos sem responder pergunta nenhuma.

O que atravessa a fronteira é o contrato de versões: o `versions.env` precisa continuar
sendo a fonte única quando existir `values.yaml`. Como, é competência da Etapa 10.

## Questões em aberto

### 1. O número de contêineres de aplicação depende do ADR-0011

Esta é uma dependência direta, e ela é maior que uma contagem.

Se o ADR-0011 mantiver `resource` e `allocation` no mesmo serviço, o profile `control`
tem menos contêineres, a invariante do ADR-0001 é verificada numa transação local, e a
Etapa 1 mede concorrência com um único contêiner de aplicação — ou nenhum, se a Etapa 1
rodar tudo por Testcontainers. Nesse mundo, `messaging` só é necessário na Etapa 2,
exatamente como a tabela acima diz.

Se o ADR-0011 separar os dois, a invariante vira distribuída. A verificação passa a
exigir mensagem entre serviços já na Etapa 1, e `messaging` sobe uma etapa na tabela. O
profile mínimo da Etapa 1 deixa de ser um contêiner e vira quatro.

A tabela etapa × profile está escrita com `N` como parâmetro justamente para sobreviver
às duas saídas. O que **não** sobrevive é a linha da Etapa 1: ela precisa ser reescrita
se o ADR-0011 separar os agregados. Este ADR não pode ser aceito antes do 0011.

### 2. A observabilidade é opcional ou obrigatória a partir da Etapa 4?

A favor de obrigatória: as asserções do ADR-0004 consultam métricas. Um experimento sem
Prometheus e sem Collector avalia asserções sobre séries vazias, e o resultado é um
veredito falso, não um erro. Nesse caso o perfil barato desaparece da Etapa 4 em diante,
e o custo diário volta.

A favor de opcional: o `experiment-service` poderia ler os endpoints de métrica dos
serviços diretamente e dispensar a pilha inteira para a maioria dos experimentos,
deixando Grafana, Loki e Tempo para quando alguém for de fato olhar um gráfico. O custo
é que o instrumento passa a ter um segundo caminho de coleta, e os dois podem
discordar — o que é a pior falha possível num instrumento de medida.

Não decidido. A decisão depende de as asserções do ADR-0004 serem escritas primeiro.

### 3. Digest ou tag exata

A favor do digest: é imutável de verdade. Uma tag pode ser reescrita pelo publicador, e
nesse caso a reprodutibilidade é perdida sem nenhum sinal.

Contra: o digest torna o arquivo ilegível, e a atualização de uma versão passa a exigir
uma consulta ao registry. Pior, um digest fixado numa arquitetura pode não resolver em
outra se o manifesto multi-arquitetura não for usado — o que transformaria o
`versions.env` num arquivo dependente da máquina, o oposto do que ele existe para ser.

A decisão escrita acima (tag **e** digest) assume manifesto multi-arquitetura em todas
as imagens usadas. Isso não foi verificado imagem por imagem.

### 4. O volume sobrevive entre experimentos?

A favor de descartar: o ADR-0004 exige que duas execuções com a mesma semente partam do
mesmo estado. Uma tabela `inbox` com `eventId` da execução anterior faz a segunda
execução descartar eventos que a primeira processou. A reprodutibilidade morre
exatamente no mecanismo que o ADR-0007 quer estudar.

A favor de preservar: o ADR-0007 já registra que o expurgo agressivo apaga a evidência
que um experimento precisaria. Destruir o volume ao fim de cada execução destrói
`outbox`, `inbox` e as tabelas de estado — justamente onde se investiga um veredito
inesperado.

A saída provável é dumpar antes de destruir, mas isso exige decidir o que entra no dump,
onde ele fica e por quanto tempo. Nada disso está decidido.

### 5. Onde o `versions.env` é lido pelos testes

A conversão para `platform-versions.properties` precisa acontecer em algum módulo Maven,
e o arquivo de origem está **fora** de qualquer módulo. Um caminho relativo à raiz do
repositório funciona no IDE e quebra quando o teste roda a partir de um jar, ou com o
diretório de trabalho diferente.

A alternativa é colocar o helper em `shared/`, mas o ADR-0005 restringe `shared/` a
conteúdo técnico de contrato de mensagem. Uma leitura de versão de imagem cabe ali?
Provavelmente sim, por ser técnica; mas abrir a porta para "utilitário de build" em
`shared/` é o começo do monólito distribuído que o ADR-0005 rejeita.

## Consequências

### Positivas

- O ciclo da Etapa 1 sobe um contêiner. Um teste de domínio continua rodando sem nenhum,
  porque o domínio é Java puro (ADR-0006).
- O ambiente de um experimento passa a ser um dado registrado no relatório. A pergunta
  "o que estava de pé?" tem resposta em texto, e não depende de memória.
- O `versions.env` faz teste e experimento medirem o mesmo sistema, por construção. Uma
  divergência de versão vira erro de build, não vira diferença inexplicada entre dois
  números.
- O isolamento entre serviços é imposto pelo servidor de banco, com `SQLSTATE`
  próprio, e é testado. Convenção documentada não sobrevive à terceira semana; um
  `GRANT` ausente sobrevive.
- Um serviço novo custa uma entrada de manifesto. Os sete passos manuais viram um.

### Negativas

- Profiles multiplicam as combinações possíveis, e a maioria delas é inválida. Os
  presets contêm o dano, mas alguém que rode `docker compose up` com um `--profile`
  solto encontra um serviço de aplicação sem broker e um erro de conexão obscuro.
- O gerador é código que ninguém pediu. Ele precisa ser mantido, e ele quebra em
  cenários que o manifesto não previu — um serviço com duas exchanges, por exemplo.
- Fixar digest torna a atualização de versão um pequeno ritual. Isso é intencional, mas
  é atrito real, e atrito costuma virar imagem desatualizada.
- O `postgres-init` a cada `up` acrescenta segundos ao ciclo e exige que todo script
  seja idempotente para sempre. Um script novo escrito sem `IF NOT EXISTS` quebra o
  segundo `up`, não o primeiro — o pior momento para descobrir.
- Um único arquivo `docker-compose.yml` cresce. Com observabilidade e réplicas, ele
  passa de trezentas linhas, e é preciso ler `profiles` linha a linha para saber o que
  sobe quando.

### Neutras

- Compose e Kubernetes vão coexistir a partir da Etapa 10. Isso significa duas
  descrições do mesmo sistema, com o risco de divergirem. O `versions.env` cobre a
  versão de imagem; não cobre variável de ambiente, limite de recurso nem topologia.
- O laboratório fica preso ao Docker Compose v2 com suporte a `profiles` e a
  `COMPOSE_PROFILES`. Podman Compose e Colima resolvem parcialmente; nenhum é suportado
  explicitamente.

## Alternativas consideradas

### Alternativa A — um único compose sem profiles

Um arquivo, um `docker compose up`, tudo de pé sempre.

**Descartada.** É a opção mais simples de ler e a mais cara de usar. Doze contêineres
para rodar um teste que toca uma tabela transformam o ciclo diário num intervalo de
espera, e o custo é pago em toda execução, não só na primeira. A variante "vários
arquivos combinados com `-f`" tem o mesmo efeito prático dos profiles, mas espalha a
definição de um serviço por arquivos diferentes e torna impossível ler num lugar só o
que sobe em cada etapa — que é exatamente a pergunta que a tabela etapa × profile existe
para responder.

### Alternativa B — Kubernetes local (kind, k3d, minikube) desde a Etapa 0

Usar na Etapa 0 o mesmo orquestrador da Etapa 10, eliminando a segunda descrição do
sistema.

**Descartada.** O argumento a favor é bom — paridade com o destino — e por isso a
alternativa foi considerada a sério. Mas ela cobra o custo do Kubernetes nas etapas em
que o laboratório ainda não tem pergunta de Kubernetes para fazer. Na Etapa 1, um
`kubectl apply` mais um build de imagem mais um `imagePullPolicy` correto substituem
`docker compose up` para subir um PostgreSQL, e o tempo entre alterar um caso de uso e
observar o efeito cresce de segundos para dezenas de segundos. Pior, o modo de falha
muda de qualidade: um `CrashLoopBackOff` na Etapa 1 é tempo gasto aprendendo Kubernetes,
não consistência. O laboratório existe para estudar consistência.

### Alternativa C — Testcontainers para tudo, sem Compose

O Testcontainers já sobe PostgreSQL e RabbitMQ, e sabe montar módulos compostos. Um
experimento poderia ser um processo Java que sobe a stack que precisa.

**Descartada.** O tempo de vida está errado. Testcontainers existe para nascer e morrer
com um teste, e o laboratório precisa de um ambiente que sobreviva entre execuções: para
abrir o Grafana, para desenvolver o frontend, para inspecionar uma tabela `outbox`
depois de um veredito estranho. Além disso, a stack de observabilidade não é uma
dependência de teste — Prometheus com dez segundos de série temporal não responde nada.
E, se toda a plataforma virasse código Java, a definição do ambiente passaria a viver
dentro do processo que ele deve observar, o que aproxima o instrumento do sistema sob
teste na direção que o ADR-0006 proíbe.

### Alternativa D — Tilt ou Skaffold

Ferramentas de loop interno com rebuild automático, live update e orquestração por
perfil.

**Descartada.** Elas resolvem um problema que este laboratório não tem: o loop de
edição-build-deploy de muitos serviços num cluster, com muitas pessoas. Aqui é uma
pessoa, uma máquina e um reactor Maven único (ADR-0005), onde o rebuild já é
`mvn install`. O custo é uma dependência a mais entre a intenção e o que sobe, com
`Tiltfile` próprio para manter — e o benefício, live update, só apareceria na Etapa 10,
quando o alvo for Kubernetes. Reavaliar quando o alvo for o cluster, não antes.

## Quando esta decisão deixa de valer

O sinal concreto de que a estratificação virou custo morto: **trinta dias em que todo
`make` executado foi o preset da etapa mais alta**. Se ninguém sobe mais o perfil
mínimo, os profiles deixaram de economizar alguma coisa e só restou a complexidade de
mantê-los. Nesse caso, volte à Alternativa A.

O sinal concreto de que a estratificação virou fonte de erro: **duas execuções do mesmo
experimento, com a mesma semente, produzem vereditos diferentes, e a diferença é
explicada por um contêiner presente numa execução e ausente na outra**. Isso significa
que o conjunto de profiles virou uma variável não controlada do experimento — a
plataforma passou a interferir na medida. Nesse caso, o preset da etapa vira campo
obrigatório e validado da definição do experimento (ADR-0004), não apenas um campo do
relatório.
