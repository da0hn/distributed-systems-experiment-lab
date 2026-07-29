# ADR-0013: O eixo de leitura — defasagem, CQRS e como medi-la

- **Estado:** Proposto
- **Data:** 2026-07-26
- **Etapa do roadmap:** a definir
- **Relacionado:** ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0006, ADR-0007, ADR-0011

## Contexto

O ADR-0001 lista "CQRS e defasagem de leitura" entre os seis temas que dependem do
domínio — ou seja, entre os que este laboratório existe para estudar.

Nenhum ADR decidiu como esse tema é medido. Os ADRs 0001, 0002, 0003 e 0007 tratam
do eixo de **escrita**: quem escreve, com que semântica, protegido por qual mecanismo.

O ADR-0002 define quatro origens, e as quatro são de escrita. Não existe ator leitor
com contrato próprio.

O ADR-0004 define o veredito executável. As asserções dele são consultas sobre o
**estado final** e sobre métricas agregadas. Toda origem do ADR-0002 deixa rastro no
estado final: uma alocação a mais, um contador errado, um `Resource` em
`OVERCOMMITTED`.

A questão 2 do ADR-0004 registra que uma leitura desatualizada não deixa rastro
nenhum.

## Problema

Uma leitura desatualizada é, por definição, um valor que era falso no instante em que
foi lido e virou verdadeiro depois. Quando o experimento termina, ela não existe em
lugar nenhum: nem no banco, nem no log de eventos, nem na invariante.

O resultado é um **falso negativo estrutural do instrumento**. O laboratório concluiria
"nenhuma violação" num cenário em que o usuário viu dado errado o tempo inteiro.

Cinco forças estão em conflito.

**Força 1 — a verdade não pode ser consultada no instante da leitura.** Consultar a
verdade tem latência própria, e a verdade muda enquanto a consulta acontece. Uma
segunda leitura, feita depois da primeira, sempre parece mais fresca — o erro de medida
tem sinal conhecido e é somado à defasagem que se quer medir.

**Força 2 — o relógio não é confiável entre processos.** Se o leitor e o escritor
vivem em processos diferentes, o clock skew entre eles entra na medida. O ADR-0002 já
declara que não existe um "agora" global.

**Força 3 — amostrar toda leitura muda o sistema medido.** Registrar cada leitura
custa latência no caminho crítico e produz um volume que domina o relatório.

**Força 4 — nem toda medida tolera amostragem.** Defasagem é uma distribuição, e
distribuição sobrevive a uma amostra. Uma violação de read-your-writes é um evento
raro e binário: perdê-la na amostra é o mesmo falso negativo que este ADR existe para
eliminar.

**Força 5 — hoje não há de onde a defasagem vir.** Não existe réplica de leitura nem
projeção CQRS decidida. Sem um estado derivado, não há nada para ficar atrasado.

A pergunta é: quem lê, como a defasagem é capturada no instante em que acontece, e
qual asserção a transforma em veredito.

## Decisão

O laboratório ganha um **eixo de leitura**, com três peças: um ator observador, um
mecanismo de amostragem que reconstrói a verdade depois, e um vocabulário de asserções
separado do vocabulário de escrita.

### 1. Quem lê — o Observer é uma categoria, não uma quinta origem

O laboratório tem um ator leitor chamado **Observer**. Ele **não** é uma quinta origem
do ADR-0002.

O eixo de classificação daquele ADR é *como cada origem quebra a invariante ao
escrever*. O Observer não escreve nada e não quebra invariante nenhuma. Colocá-lo
naquela tabela exigiria uma coluna "falha característica" vazia, e sugeriria que as
nove estratégias do ADR-0003 o protegem — nenhuma delas reduz defasagem em um
milissegundo.

| | Origens de escrita (ADR-0002) | Observer (este ADR) |
|---|---|---|
| Escreve estado | sim | nunca |
| Pode violar a invariante | sim | não |
| Protegido pelo ADR-0003 | sim | não se aplica |
| Sujeito da asserção | o estado autoritativo | a sessão do leitor |
| Sobrevive ao estado final | sim | não — daí este ADR |

**O Observer vive no Lab Plane.** Ele é um papel do gerador de carga do
`experiment-service`, que já representa o Operator. Ele chama a mesma API pública de
leitura que qualquer cliente chamaria. A regra 6 do ADR-0006 continua valendo: o
Control Plane expõe a leitura e não sabe que está sendo observado.

**O Observer nunca consulta a verdade.** Ele registra apenas o que a resposta lhe
entregou. A verdade é **reconstruída depois do experimento**, a partir do histórico de
versões (ver item 2). Isso elimina a Força 1 por construção: não existe segunda
leitura, então não existe latência de segunda leitura na medida.

**Toda resposta de leitura carrega um envelope.** Simétrico ao envelope de evento do
ADR-0007, e como ele, técnico e genérico — cabe em `shared/` sem violar a proibição do
ADR-0005 contra domínio compartilhado.

| Campo | Uso |
|---|---|
| `value` | o que foi lido |
| `asOfVersion` | a `aggregateVersion` até a qual a resposta foi construída |
| `source` | `AUTHORITATIVE` ou `PROJECTION` |
| `servedBy` | identidade da réplica que respondeu |
| `servedAt` | instante de atendimento, do adaptador de relógio |
| `clockId` | identidade do relógio que produziu `servedAt` |

`asOfVersion` é o campo que faz o mecanismo inteiro funcionar. O modelo de leitura já
precisa persistir a versão aplicada para se defender de reordenação (`SEQUENCE_GUARD`,
ADR-0003). Expor uma coluna que já existe custa zero.

### 2. Como a defasagem é capturada — amostra no instante, verdade reconstruída depois

O Observer grava uma **amostra de leitura** num destino do Lab Plane, fora do caminho
crítico e fora do banco do Control Plane.

| Campo | Origem | Para que serve |
|---|---|---|
| `sampleId` | Observer | identidade |
| `sessionId` | Observer | agrupa leituras e escritas do mesmo leitor |
| `aggregateId` | Observer | qual `Resource` |
| `readVersion` | envelope (`asOfVersion`) | o que o leitor viu |
| `readValue` | envelope | o valor lido |
| `source`, `servedBy`, `servedAt`, `clockId` | envelope | procedência e relógio |
| `lastWriteVersion` | Observer | marca d'água de escrita da própria sessão |
| `previousReadVersion` | Observer | leitura anterior da mesma sessão |

**A verdade é reconstruída, não consultada.** A tabela `outbox` do ADR-0007 já é um log
append-only de versões: toda mudança de estado gravou, na mesma transação, um evento
com `aggregateVersion` e `occurredAt`. Depois que o experimento termina, o histórico de
versões de cada agregado sai de uma consulta a essa tabela. A verdade no instante `t` é
a maior versão cujo commit precede `t`.

#### Versão é a medida primária; tempo é derivada e condicional

```
staleness.versionLag  = versãoVerdadeiraEm(servedAt) − readVersion
staleness.millis      = servedAt − commitDe(readVersion + 1)
```

A primeira é exata, inteira e **independente de relógio**. A segunda responde "há
quanto tempo o valor que o leitor viu deixou de ser verdadeiro" e depende de dois
relógios: o do processo que atendeu a leitura e o do processo que fez o commit.

**A regra 8 do ADR-0006 ajuda, e é o que torna a segunda medida utilizável.** Sem ela,
o skew entre processos é ruído incontrolável. Com ela, o relógio é um adaptador
injetável: o experimento declara o desvio de cada nó, o adaptador reporta `clockId`
junto com o instante, e o desvio declarado é subtraído da medida. Skew deixa de ser
ruído e vira **parâmetro do experimento** — que é exatamente o cenário de clock skew
que a regra 8 foi escrita para viabilizar.

Resta o skew não declarado. Regra dura: **`staleness.millis` só é reportado quando
todos os `clockId` da amostra pertencem ao mesmo domínio de relógio.** No Docker
Compose local, todos os contêineres derivam do relógio do host e o domínio é único. Em
Kubernetes com múltiplos nós, não é — e nesse caso o relatório emite apenas
`versionLag` e registra a omissão. Uma medida temporal com skew desconhecido é pior que
nenhuma: ela parece precisa.

Vale a versão carregada no modelo de leitura? Sim. Ela é a única medida exata, custa uma
coluna que o modelo de leitura já precisa ter, e é o que permite ao laboratório rodar em
Kubernetes sem perder o eixo inteiro.

#### Duas taxas de amostragem, por motivos diferentes

| Regime | O que amostra | Taxa | Por quê |
|---|---|---|---|
| **Probabilística semeada** | leituras de sessões que nunca escreveram | `readSampleRate`, declarada no experimento | mede uma distribuição; uma amostra basta |
| **Dirigida** | toda leitura de sessão que já escreveu | 100% | mede eventos raros e binários; perder um é falso negativo |

A probabilidade vem da fonte de aleatoriedade semeada de `shared/random`, protegida
pela regra 7 do ADR-0006. Mesma semente, mesmas leituras amostradas.

A amostragem dirigida é cara por leitura e barata no total, porque o Observer controla
quantas sessões escrevem. `writeThenReadRatio` declara essa fração no experimento.

**As duas garantias mais graves não precisam nem da verdade nem do relógio.**
Read-your-writes e monotonic reads são comparações **dentro da própria sessão**:
`readVersion` contra `lastWriteVersion`, e `readVersion` contra `previousReadVersion`.
Nenhuma reconstrução, nenhum timestamp, nenhum skew. A máquina cara — o log de versões,
o domínio de relógio — só é necessária para a métrica **menos** grave, que é a
distribuição de defasagem.

### 3. Qual é a asserção — safety e liveness, aplicados à sessão

`safety.violations == 0` não serve, e não por descuido: nenhuma invariante foi violada.
O sistema respondeu um valor obsoleto e correto no passado.

**O eixo de leitura não é um terceiro eixo.** Ele reusa safety e liveness, aplicados a
um sujeito diferente. O ADR-0002 mede propriedades do **estado autoritativo**. Este ADR
mede propriedades da **sessão de um leitor**.

| Sujeito | Safety | Liveness |
|---|---|---|
| Estado autoritativo (ADR-0002) | `safety.violations == 0` | `convergence.seconds < N` |
| Sessão do leitor (este ADR) | `guarantee.readYourWrites.violations == 0`<br/>`guarantee.monotonicReads.violations == 0` | `staleness.versionLag.p99 <= N`<br/>`guarantee.eventualConvergence.seconds < N` |

O vocabulário é unificado na **forma** e separado no **sujeito**. Nada é duplicado.

#### As métricas

| Métrica | Tipo | Precisa da verdade? | Precisa de relógio? |
|---|---|---|---|
| `staleness.versionLag.p50/p99/max` | distribuição, em versões | sim | não |
| `staleness.millis.p50/p99/max` | distribuição, em tempo | sim | sim — condicional |
| `staleness.samples` | contagem — obrigatória no relatório | — | — |
| `guarantee.readYourWrites.violations` | contagem de eventos | não | não |
| `guarantee.monotonicReads.violations` | contagem de eventos | não | não |
| `guarantee.eventualConvergence.seconds` | tempo até `versionLag == 0` | sim | sim |

`staleness.samples` é obrigatório porque um `p99` calculado sobre 1200 amostras é
estimado por 12 pontos. O relatório precisa dizer isso. Um experimento que precise de
`p99.9` aumenta a taxa; ele não confia na amostra.

#### As garantias, e o cenário mínimo que viola cada uma

| Garantia | Violação | Cenário mínimo |
|---|---|---|
| **read-your-writes** | `readVersion < sessão.lastWriteVersion` | 1 escrita confirmada + 1 leitura na mesma sessão, num caminho de leitura assíncrono |
| **monotonic reads** | `readVersion(t2) < readVersion(t1)`, mesma sessão, `t2 > t1` | 2 réplicas do modelo de leitura com defasagens diferentes, sem afinidade de sessão |
| **eventual convergence** | existe leitura com `versionLag > 0` após `quiesceSeconds` sem nenhuma escrita | relay travado por mensagem envenenada, ou projeção que perdeu um evento e não tem recuperação |

**Monotonic reads é vacuamente satisfeito com uma réplica só.** Com um único
consumidor, a versão aplicada nunca retrocede. A asserção fica verde sem provar nada.
Ela só tem conteúdo quando o modelo de leitura tem duas réplicas — o que depende da
Etapa 5. Ver a questão 3.

#### Read-your-writes não é defasagem alta

São coisas diferentes, e a primeira é a mais grave.

| | Defasagem alta | Violação de read-your-writes |
|---|---|---|
| Referência da comparação | a verdade global | a marca d'água da própria sessão |
| Natureza | distribuição | evento binário |
| Eixo | liveness | **safety** |
| Aceitável? | pode ser — um painel 2 s atrás é útil | nunca |
| Sensível à magnitude | sim, é a própria medida | não — 5 ms de defasagem já viola |
| Causalidade com o leitor | nenhuma | direta: o leitor causou o fato que não vê |

Uma sessão pode observar 5 segundos de defasagem sem nenhuma violação, se ela nunca
escreveu. Outra pode observar 5 milissegundos e violar, se escreveu nesses 5
milissegundos. A gravidade não está na magnitude. Está no **elo causal**: o leitor
executou uma ação, recebeu confirmação, e o sistema lhe mostrou um mundo em que a ação
não aconteceu.

Por isso read-your-writes é uma asserção de safety, sem limiar, sem calibração e sem
risco de falha intermitente — ao contrário de todo limiar temporal do ADR-0004.

```mermaid
sequenceDiagram
    participant O as Observer (Lab Plane)<br/>sessão S
    participant W as Caminho de escrita<br/>autoritativo
    participant DB as PostgreSQL
    participant R as Outbox Relay
    participant P as Projeção<br/>(modelo de leitura)

    O->>W: POST /allocations — sessão S
    W->>DB: BEGIN; INSERT allocation; INSERT outbox; COMMIT
    Note over DB: resource v7 → v8
    W-->>O: 201 Created, asOfVersion = 8
    Note over O: S.lastWriteVersion = 8

    O->>P: GET /resources/{id} — sessão S
    P-->>O: 200 OK, asOfVersion = 7, source = PROJECTION
    Note over O: readVersion 7 < lastWriteVersion 8<br/>readYourWrites.violations += 1

    R->>DB: SELECT ... FOR UPDATE SKIP LOCKED
    R->>P: evento v8
    Note over P: tarde demais — a violação já<br/>aconteceu e não sobrevive ao<br/>estado final
```

Sem a amostra do Observer, o experimento acima termina com `safety.violations == 0`,
`convergence.seconds` dentro do limiar e um relatório verde.

### 4. De onde a defasagem vem — o relay não basta

Hoje o laboratório não tem réplica de leitura nem projeção CQRS. A fonte natural de
atraso é o relay do Outbox: 100 ms de latência mediana adicionada pelo ciclo de polling
(ADR-0007).

**Isso não é suficiente, e o motivo é estrutural.** O relay atrasa a *propagação de um
evento*. Defasagem de leitura é a distância entre um estado derivado e o autoritativo.
Sem estado derivado, o atraso do relay não é defasagem — é apenas latência de evento,
que o ADR-0007 já mede.

Se o Operator escreve e lê o mesmo estado autoritativo, `versionLag` é zero por
construção, em qualquer carga, com qualquer caos. Não há o que medir.

**O laboratório precisa de uma projeção assíncrona de verdade.** A menor que produz
cenário interessante é a que responde à pergunta que um usuário realmente faz:

```
resource_view {
  resource_id
  capacity
  allocated          -- Σ alocações ativas
  available
  state              -- HEALTHY | OVERCOMMITTED  (ADR-0002)
  as_of_version      -- alimenta 'asOfVersion' do envelope de leitura
  updated_at
}
```

Ela é alimentada por eventos, pelo Inbox, sem nenhum acesso às tabelas do lado de
escrita. Ela é a mesma resposta que o caminho autoritativo dá — o que a torna
comparável, e o que torna a divergência entre as duas a medida inteira.

**Em que etapa ela entra.** A projeção precisa do Outbox (Etapa 2) e do Inbox (Etapa 3).
O Observer e a amostragem entram junto com ela. O vocabulário de asserções só vira
veredito com o `experiment-service` (Etapa 4). A segunda réplica do modelo de leitura,
que dá conteúdo a `monotonicReads`, depende da Etapa 5.

**Por que a etapa deste ADR fica `a definir`.** Ele não bloqueia a Etapa 1: naquele
momento toda leitura é autoritativa e `versionLag` é zero por construção — não existe
falso negativo a eliminar. Ele bloqueia qualquer experimento de CQRS. E o número exato
depende de onde a projeção vive, que é competência do ADR-0011. Fixar uma etapa aqui
seria fixar uma decisão de outro ADR pela porta dos fundos.

### 5. O experimento declara o eixo de leitura

O JSON do ADR-0004 ganha um bloco `read` e asserções no novo vocabulário.

```json
{
  "name": "projecao-quebra-read-your-writes",
  "hypothesis": "Ler da projeção viola read-your-writes sob carga; ler do autoritativo não",
  "seed": 42,
  "read": {
    "observers": 5,
    "rps": 50,
    "target": "PROJECTION",
    "sessionAffinity": "STICKY",
    "readSampleRate": 0.1,
    "writeThenReadRatio": 0.2,
    "quiesceSeconds": 5
  },
  "assertions": [
    "safety.violations == 0",
    "guarantee.readYourWrites.violations == 0",
    "staleness.versionLag.p99 <= 1"
  ]
}
```

**`target: AUTHORITATIVE` é o grupo de controle do eixo de leitura**, com o mesmo papel
que `NONE` tem no ADR-0003. Ele precisa registrar `versionLag == 0` em toda amostra. Se
não registrar, o instrumento está errado, e nenhum resultado com `PROJECTION` significa
coisa alguma.

## Questões em aberto

### 1. Quem é dono da projeção — e se o dono for o mesmo, a projeção é real?

Este ADR decide **o que** é projetado e **que** a projeção é assíncrona e alimentada por
evento. Ele não decide quem a hospeda: isso é competência exclusiva do ADR-0011.

A escolha não é neutra, e os dois lados têm argumento:

- **Mesmo serviço do dado autoritativo.** Barato e imediato. Mas a projeção passa a ser
  um artefato do laboratório, não uma consequência da arquitetura: o serviço tem a
  verdade a uma consulta de distância e escolhe não usá-la. Um crítico diria que a
  defasagem foi fabricada.
- **Serviço separado.** É a situação real de CQRS, e a defasagem é consequência genuína
  da fronteira. Mas exige que a decomposição já esteja decidida, e o ADR-0011 ainda não
  existe.

Argumento contra o crítico, registrado sem fechar a questão: uma réplica de leitura do
PostgreSQL fica atrás do primário pelo mesmo motivo — o dado está a uma consulta de
distância e o sistema escolhe não fazê-la. O laboratório mediria o mesmo fenômeno.

### 2. O limiar de `staleness` sofre do mesmo mal que o limiar de convergência

A questão 1 do ADR-0004 já registra o problema: o relay adiciona 100 ms medianos, e um
limiar apertado mede o próprio instrumento. `staleness.millis.p99 < 150` mediria o
intervalo de polling, não a arquitetura.

- **Limiar relativo** (`p99 < 3 × intervaloDePolling`) se autocalibra e nunca mede o
  instrumento. Em troca, esconde regressões: se o relay ficar duas vezes mais lento, a
  asserção continua verde.
- **Limiar absoluto** é honesto e comparável entre execuções. Em troca, quebra toda vez
  que o intervalo de polling muda, e a falha não distingue "a arquitetura piorou" de "o
  instrumento mudou".

`versionLag` não sofre disso — `p99 <= 1` é absoluto e independe do relógio. Isso é
argumento para o limiar temporal ser secundário, mas não fecha a questão: `versionLag`
não responde "quanto tempo o usuário viu dado errado", que é a pergunta do tema.

### 3. `monotonicReads` entra agora ou na Etapa 5?

Com uma réplica só, a asserção é vacuamente verdadeira.

- **Incluir agora.** O vocabulário fica completo e os relatórios antigos permanecem
  comparáveis. Em troca, uma asserção verde que não prova nada é o pior tipo de teste —
  ela produz confiança sem evidência.
- **Adiar para a Etapa 5.** Honesto. Em troca, a asserção precisa ser adicionada depois,
  e todo relatório anterior fica sem o campo, quebrando a comparação entre execuções.

Uma terceira saída não avaliada: incluir a asserção e marcá-la explicitamente como
`VACUOUS` no relatório enquanto houver uma réplica só. Isso resolve os dois lados, mas
adiciona um estado de asserção que o ADR-0004 não tem.

### 4. Retenção do log de versões contra o expurgo do Outbox

A reconstrução da verdade depende de a `outbox` conter o histórico completo de versões
do período do experimento. O ADR-0007 já registra que um expurgo agressivo apaga
evidência.

- **Reusar a `outbox`.** Custo zero: a tabela existe e já é gravada na transação da
  escrita. Em troca, a política de expurgo passa a ter dois donos com objetivos opostos
  — operação quer apagar, medida quer guardar — e a evidência some sem aviso.
- **Log de versões dedicado, append-only.** Explícito e imune ao expurgo. Em troca, é
  uma segunda escrita na transação crítica, que é exatamente o caminho cuja latência e
  contenção o laboratório está medindo. O instrumento entraria na medida.

### 5. `convergence.seconds` e `eventualConvergence` colidem no nome

Os dois fenômenos são distintos, e o argumento está na seção de decisão: sujeitos
diferentes, componentes que falham diferentes, observabilidade diferente. Mas os nomes
se parecem o bastante para confundir a leitura de um relatório.

Qualificar o nome do ADR-0002 (`convergence.state.seconds`) resolveria. Mas editar o
ADR-0002 não é competência deste ADR. Fica registrado que, quando os dois forem aceitos, um dos
nomes precisa de qualificador.

### 6. O que define uma sessão de leitura

`sessionId` é a chave de read-your-writes e de monotonic reads. Este ADR assume que o
Observer o escolhe e o envia num cabeçalho.

- **Cabeçalho escolhido pelo Observer.** Simples e determinístico. Em troca, a sessão de
  um cliente real é um cookie ou uma conexão, e a afinidade a uma réplica é propriedade
  do balanceador — o laboratório não estaria modelando nada disso.
- **Derivar da conexão.** Fiel. Em troca, não é controlável por um experimento semeado,
  e o cenário de monotonic reads deixa de ser reproduzível.

`sessionAffinity: STICKY | ROUND_ROBIN` aparece no JSON acima como se fosse decidido.
Não é: quem implementa a afinidade — o Observer, um balanceador ou o próprio serviço —
depende do arranjo de réplicas, que é da Etapa 5.

## Consequências

### Positivas

- O falso negativo estrutural desaparece. Um experimento de CQRS passa a poder falhar
  pelo motivo certo.
- As duas asserções mais graves — read-your-writes e monotonic reads — são exatas,
  binárias e independentes de relógio e de reconstrução. Elas não têm limiar, logo não
  têm falha intermitente. Isso é raro no laboratório e é o oposto do que a questão 1 do
  ADR-0004 teme.
- A verdade reconstruída a partir da `outbox` reaproveita uma tabela que já existe pelo
  ADR-0007. O eixo de leitura não adiciona nenhuma escrita ao caminho crítico.
- O envelope de leitura torna a procedência de toda resposta explícita. `source` e
  `servedBy` respondem "de onde veio este número" sem inferência.
- `target: AUTHORITATIVE` dá ao eixo de leitura um grupo de controle com a mesma função
  que `NONE` tem no ADR-0003: se o controle não for zero, nada mais significa nada.
- A regra 8 do ADR-0006 deixa de ser incômodo e vira pré-requisito. O clock skew passa a
  ser parâmetro declarado do experimento, não ruído.

### Negativas

- **O laboratório precisa de uma projeção assíncrona que ele hoje não tem.** É um
  consumidor novo, uma tabela nova e um caminho de leitura novo — custo real, e ele só
  existe para que o tema seja mensurável.
- O modelo de leitura passa a expor `asOfVersion` na API pública. É um detalhe interno
  vazando para fora, e um sistema de produção pensaria duas vezes. Aqui é aceito porque
  é a única medida exata; ainda assim é vazamento.
- `staleness.millis` é condicional. Ele desaparece do relatório em ambiente com mais de
  um domínio de relógio, e desaparecer é confuso para quem lê. A alternativa — reportar
  um número com skew desconhecido — é pior, mas o custo de legibilidade é real.
- A amostragem probabilística torna `p99` uma estimativa. O relatório precisa carregar
  o tamanho da amostra e quem o lê precisa entender o que isso significa.
- A amostragem dirigida a 100% muda o perfil de carga: sessões que escrevem passam a ter
  toda leitura registrada. O custo é do Lab Plane, mas o Observer é o mesmo processo que
  gera a carga, e um Observer sobrecarregado gera carga irregular.
- Mais um bloco no JSON de experimento, mais seis métricas no relatório. O ADR-0004 fica
  maior sem ficar mais simples.

### Neutras

- O Observer pertence ao Lab Plane. Ele é instrumento, não sistema sob teste. Um bug
  nele produz falso positivo de defasagem, não bug de consistência.
- Este ADR não altera nenhuma decisão de escrita. As quatro origens, as nove estratégias
  e os dois `capacityModel` continuam como estão. O eixo de leitura é ortogonal a todos.
- A projeção é `DERIVED` no sentido do ADR-0001 — ela mantém `allocated` como soma — mas
  isso não a coloca na matriz daquele ADR. Ela não é fonte de verdade e não decide
  escrita nenhuma.

## Alternativas consideradas

### Alternativa A — leitura dupla: consultar a projeção e a verdade no mesmo instante

O Observer lê a projeção e, em seguida, lê o estado autoritativo, e compara os dois
valores na hora.

**Descartada.** A segunda leitura tem latência própria e acontece **depois** da
primeira. O erro de medida tem sinal conhecido: a verdade lida sempre parece mais
fresca, então a defasagem medida é sistematicamente maior que a real, pelo tempo de
ida e volta da segunda chamada. Uma violação de poucos milissegundos ficaria
indistinguível do erro do instrumento.

Além disso, ela dobra a carga de leitura sobre o sistema sob teste, e a carga extra cai
justamente sobre o caminho autoritativo — o mesmo cuja contenção o ADR-0003 mede.

### Alternativa B — amostrar toda leitura

Registrar cada leitura, sem probabilidade, sem regime dirigido.

**Descartada.** O registro entra no caminho da leitura, e latência de leitura é uma das
coisas medidas. A 200 rps por 60 segundos, o volume de amostras domina o relatório e o
custo de escrevê-las compete com a carga.

A amostragem semeada preserva a forma da distribuição a um custo conhecido, e o único
caso que amostra nenhuma tolera — os eventos raros e binários — está coberto pelo
regime dirigido a 100%. A decisão não é "amostrar ou não": é amostrar **o que tolera**
e não amostrar **o que não tolera**.

### Alternativa C — medir a defasagem apenas em tempo, sem versão

Registrar somente `servedAt` e o instante em que o valor deixou de ser verdadeiro.

**Descartada.** O ADR-0002 já declara que não existe "agora" global. Uma defasagem
medida só em tempo não distingue "o leitor viu um valor velho" de "o relógio do leitor
está 200 ms atrás". As duas hipóteses produzem exatamente o mesmo número, e o
laboratório não teria como escolher entre elas.

`versionLag` é exato, inteiro e imune a relógio. O tempo permanece como medida derivada,
válida sob a condição de domínio de relógio único.

### Alternativa D — declarar o leitor como quinta origem no ADR-0002

Acrescentar uma linha "Reader" à tabela das quatro origens.

**Descartada.** Aquela tabela classifica origens por *como cada uma quebra a invariante
ao escrever*, e a coluna "falha característica" é o que dá sentido a ela. Um leitor não
escreve e não quebra invariante nenhuma: a coluna ficaria vazia.

Pior, a inclusão sugeriria que as estratégias do ADR-0003 se aplicam ao leitor. Nenhuma
se aplica: lock, chave de idempotência e guarda de sequência protegem o momento da
escrita e não reduzem defasagem em um milissegundo. O eixo de leitura é ortogonal ao
ADR-0003, e a tabela do ADR-0002 esconderia isso.

### Alternativa E — verificador de linearizabilidade sobre o histórico (Jepsen, Knossos)

Registrar o histórico completo de invocações e respostas, com limites de tempo real, e
rodar um verificador que decide se a história é linearizável.

**Descartada para o uso geral, adiada como experimento pontual.** É a abordagem
rigorosa: não exige projeção, não exige versão no modelo de leitura e não exige
confiança em relógio além dos limites de cada operação.

Dois problemas a inviabilizam como mecanismo principal. O custo do verificador cresce
mal com o tamanho do histórico, e 60 segundos a 200 rps produzem uma história muito além
do que esses verificadores processam. E o veredito é do tipo errado para este
laboratório: "não linearizável" não diz **qual** garantia falhou, e o laboratório existe
para ensinar a diferença entre read-your-writes, monotonic reads e convergência.

Fica registrada como boa candidata a um experimento curto e dedicado, com dezenas de
operações em vez de milhares.

### Alternativa F — mostrar a defasagem no frontend da Etapa 7, sem asserção

A árvore causal já desenha propagação. Bastaria colorir o atraso.

**Descartada.** Visualização não é veredito. Ela não falha uma execução, não entra no
relatório versionado e depende de alguém estar olhando no momento certo. É exatamente o
problema que o ADR-0004 resolveu para o eixo de escrita, e repeti-lo no eixo de leitura
seria andar para trás.

A visualização continua desejável — sobre os dados que este ADR passa a produzir.

## Quando esta decisão deixa de valer

Reveja esta decisão se o grupo de controle deixar de ser zero. O sinal concreto: um
experimento com `read.target: AUTHORITATIVE` que registre qualquer amostra com
`versionLag > 0`. Isso significa que o instrumento está medindo a si mesmo, e nenhum
resultado com `PROJECTION` tem valor enquanto isso não for explicado.

Reveja a projeção assíncrona se ela nunca ficar atrás. O sinal concreto: três
experimentos seguidos em que `staleness.versionLag.max == 0` sob a carga máxima
declarada. Uma projeção que não se atrasa não ensina nada sobre CQRS, e o custo do
Observer não retorna.
