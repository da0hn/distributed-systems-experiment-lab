# ADR-0005: Monorepo com reactor Maven único e `shared/` apenas técnico

- **Estado:** Proposto
- **Data:** 2026-07-26
- **Etapa do roadmap:** 0
- **Relacionado:** ADR-0006

## Contexto

O laboratório terá cinco serviços Java, um módulo compartilhado, um frontend e
diretórios de plataforma, infraestrutura e deployment.

Todos os serviços evoluem juntos, mantidos por uma pessoa. Nenhum serviço tem
consumidor externo. Nenhum serviço tem ciclo de release independente.

## Problema

Duas perguntas precisam de resposta.

**Primeira: um repositório ou vários?** Vários repositórios são a organização típica
de microsserviços em empresas. Um repositório é típico de times pequenos.

**Segunda: o que pode ser compartilhado entre serviços?** Compartilhar código reduz
duplicação. Compartilhar código de domínio destrói a autonomia dos serviços — o
principal motivo de existirem microsserviços.

## Decisão

### Um monorepo com reactor Maven único

Todos os módulos Java ficam num único reactor. Um `pom.xml` raiz define versões de
dependência em `dependencyManagement`. Os módulos herdam.

```
distributed-consistency-lab/
├── pom.xml                     ← parent, packaging=pom, dependencyManagement
├── services/
│   ├── resource-service/
│   ├── allocation-service/
│   ├── registry-service/
│   ├── chaos-service/
│   └── experiment-service/
└── shared/
    └── lab-messaging-contract/
```

Um `mvn test` na raiz compila e testa tudo. Uma mudança em `shared/` quebra a build
de quem depende dela **imediatamente**, não no próximo release.

### `shared/` contém apenas infraestrutura técnica

O módulo compartilhado contém:

- o envelope de evento (`eventId`, `aggregateId`, `aggregateVersion`,
  `correlationId`, `causationId`, `traceId`, `timestamp`, `producer`, `payload`)
- utilitários de correlação e propagação de contexto
- tipos de erro de transporte
- a fonte de aleatoriedade semeada (ver ADR-0004)

O módulo compartilhado **nunca** contém:

- entidades de domínio
- regras de negócio
- a invariante do ADR-0001
- DTOs de API de um serviço específico
- repositórios ou acesso a dados

### Nenhum serviço compartilha banco

Cada serviço tem seu próprio schema. Nenhum serviço lê a tabela de outro. A
comunicação é por API ou por evento.

Esta regra vale mesmo quando os serviços rodam na mesma instância PostgreSQL durante
o desenvolvimento local. Um schema por serviço, com usuário próprio e permissão
negada nos schemas alheios — a restrição é imposta pelo banco, não pela disciplina.

## Questões em aberto

Estas questões surgiram ao criar o esqueleto de diretórios do monorepo.

### 1. O plano fica visível na estrutura de diretórios?

A árvore acima mostra `services/` plano — cinco serviços, mesmo nível. Mas eles não
são equivalentes. Três pertencem ao **Control Plane** (`resource-service`,
`allocation-service`, `registry-service`) e dois ao **Lab Plane** (`chaos-service`,
`experiment-service`). A regra 6 do ADR-0006 proíbe o Control Plane de importar o Lab
Plane.

Uma regra que a estrutura não mostra é uma regra que só existe no teste. As opções
são:

- manter `services/` plano e deixar a separação só nos pacotes Java e no ArchUnit
- agrupar: `services/control-plane/...` e `services/lab-plane/...`
- separar na raiz: `services/` para o Control Plane e `lab/` para o Lab Plane

A terceira opção é a mais forte semanticamente — ela deixa claro que o Lab Plane não é
"mais um serviço". O custo é que o reactor passa a ter duas árvores de módulos.

**Estado:** o esqueleto foi criado com `services/` plano, seguindo esta decisão como
escrita. A mudança é barata enquanto não houver código.

### 2. Qual é o pacote raiz Java?

Nenhum `pom.xml` existe ainda, e o `groupId` não foi escolhido. Isso não é detalhe de
nomenclatura: as regras 4, 5 e 7 do ADR-0006 são expressas em **padrões de pacote**
(`..resource..`, `shared..`, `shared..random..`). O padrão de pacote precisa tornar
essas regras exprimíveis sem ambiguidade.

Decisão adiada para o ADR do parent POM.

### 3. Nenhum ADR decide a decomposição em serviços

A árvore acima lista cinco serviços. **Esse número nunca foi decidido.** Ele aparece
aqui como um dado, e este ADR não é o lugar de decidi-lo — o assunto desta decisão é
build e repositório, não fronteira de serviço.

Nenhum ADR responde:

- por que cinco, e não um módulo único, ou três, ou sete
- qual serviço é dono de qual tabela
- qual expõe qual contrato REST, e qual publica qual evento
- em que etapa cada um passa a existir

O ADR-0001 define dois agregados (`resource`, `allocation`) e o ADR-0002 define quatro
origens de escrita. A passagem de "dois agregados e quatro origens" para "cinco
serviços" não está escrita em lugar nenhum.

#### A colisão com o ADR-0001

Esta é a parte grave. O ADR-0001 verifica a invariante com uma leitura em `allocation`,
uma comparação com `resource.capacity` e uma escrita — **em uma transação**. A seção
*Nenhum serviço compartilha banco*, acima, proíbe exatamente isso quando `resource` e
`allocation` pertencem a serviços diferentes.

As duas decisões não podem estar certas ao mesmo tempo. As leituras possíveis são:

- **A — um dono para os dois agregados.** `resource-service` possui `resource` **e**
  `allocation`, num schema só. A invariante permanece verificável por ACID. Nesse caso
  `allocation-service` é dono do *workflow* de alocação, não do dado, e o nome atual
  engana.
- **B — dois donos desde o início.** A invariante vira distribuída na Etapa 1. Isso
  torna inaplicáveis as quatro estratégias da Etapa 1 do ADR-0003 (`NONE`,
  `ATOMIC_UPDATE`, `OPTIMISTIC`, `PESSIMISTIC`) — todas são mecanismos de um banco só.
  A Etapa 1 passaria a exigir saga, que é a Etapa 5.
- **C — separação gradual.** Um dono nas etapas 1 a 3, com a invariante local; a
  divisão em dois serviços chega junto com o Outbox (ADR-0007) e a saga (Etapa 5). O
  laboratório mede então a diferença entre os dois arranjos, com o mesmo experimento.

A opção C preserva o valor experimental: não é possível medir o custo de distribuir
sem ter o resultado não distribuído para comparar. Esse é o mesmo argumento do grupo de
controle usado no motor de workflow.

**Estado:** o esqueleto criou os cinco diretórios, vazios. Nenhum contém código, e a
mudança continua barata. A decisão pertence a um ADR próprio, sobre decomposição em
serviços, que precisa vir **antes** do parent POM — o número de módulos do reactor
depende dela.

## Consequências

### Positivas

- Refatoração atômica. Mudar o envelope de evento e todos os consumidores num só
  commit é possível.
- Nenhum versionamento de artefato interno. Não existe "qual versão de
  `lab-messaging-contract` o `resource-service` usa" — existe uma só, a do commit.
- A build da raiz é a verificação de integração mais barata que existe.
- Um só lugar para configurar dependências, plugins, versão do Java e regras de
  qualidade.

### Negativas

- O reactor único **esconde acoplamento**. Como tudo compila junto, é fácil um
  serviço importar a classe de outro sem perceber. Em repositórios separados, isso
  seria impossível por construção.

  **Mitigação obrigatória:** as regras ArchUnit do ADR-0006 substituem a barreira
  física perdida. Sem elas, esta decisão é ruim.

- A build fica mais lenta conforme o laboratório cresce. Aceito: cinco serviços não
  chegam perto do ponto em que isso importa.
- A estrutura não representa como empresas grandes organizam microsserviços com times
  independentes. O laboratório perde a experiência de versionamento de contrato entre
  repositórios.

### Neutras

- O frontend fica no mesmo repositório mas fora do reactor Maven. Ele tem seu próprio
  gerenciador de pacotes. Não há integração de build entre os dois.

## Alternativas consideradas

### Alternativa A — um repositório por serviço

O modelo de microsserviços em empresas grandes: cada serviço com seu repositório,
pipeline e ciclo de release.

**Descartada.** O custo é alto e o retorno em conhecimento sobre *consistência* é
zero. Cada mudança no envelope de evento exigiria: publicar uma versão nova do
contrato, abrir cinco pull requests, e coordenar a ordem de merge. Isso ensina sobre
gestão de dependências, não sobre sistemas distribuídos.

Se o objetivo do laboratório fosse estudar evolução de contrato entre times, esta
alternativa seria a correta.

### Alternativa B — monorepo sem reactor (builds independentes)

Um repositório, mas cada serviço com `pom.xml` isolado, sem parent comum.

**Descartada.** Perde a verificação de integração barata sem ganhar autonomia real
— os módulos continuam no mesmo repositório, então a barreira física não existe de
qualquer forma. É o pior dos dois modelos.

### Alternativa C — `shared/` com o domínio comum

Colocar `Resource` e a invariante em `shared/`, já que vários serviços a mencionam.

**Descartada com firmeza.** Esta é a decisão que transforma microsserviços num
monólito distribuído. Se dois serviços compartilham o modelo de domínio, eles
compartilham o ciclo de mudança. Uma alteração na invariante exige deploy coordenado
de ambos. O sistema fica com o custo operacional de microsserviços e o acoplamento de
um monólito.

Quando dois serviços precisam falar sobre o mesmo conceito, cada um mantém sua
própria representação. A tradução entre elas é um **Anti-Corruption Layer** explícito,
e a duplicação é intencional.

## Quando esta decisão deixa de valer

Reveja esta decisão se o laboratório passar a ter mais de uma pessoa mantendo
serviços diferentes com cadências diferentes. O sinal concreto: dois commits no mesmo
dia que tocam serviços distintos e conflitam.
