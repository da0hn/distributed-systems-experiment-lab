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
