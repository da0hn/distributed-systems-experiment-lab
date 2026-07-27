# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Não existe código neste repositório

Não há `pom.xml`, nenhuma classe Java, nenhum `docker-compose.yml`. **Não há comando de
build, de teste ou de execução.** Se você tentar `mvn test`, `docker compose up` ou
qualquer coisa parecida, vai falhar — e o motivo não é configuração faltando.

O repositório contém apenas ADRs e um esqueleto de diretórios vazios (`.gitkeep`). Isso
é deliberado: a decisão vem antes do código. Um ADR escrito depois da implementação não
é uma decisão, é uma justificativa.

Quando o código existir, a stack decidida no `README.md` é Java 21, Spring Boot 3.x,
Maven em reactor único, PostgreSQL, RabbitMQ. O pacote raiz Java ainda **não foi
escolhido** — essa decisão acompanha o parent POM, que por sua vez depende do ADR-0011
(número de módulos do reactor).

## O trabalho aqui é escrever e debater ADRs

Esta é a atividade principal do repositório, e ela tem um processo rígido.

### A regra dura

> **Nada que importa pode existir apenas na conversa.**

O contexto da conversa é limpo entre um ADR e outro. Toda objeção, alternativa
descartada ou pendência é escrita na seção `## Questões em aberto` do próprio arquivo do
ADR, **no mesmo turno em que é levantada** — antes de responder ou perguntar qualquer
coisa. Uma objeção que fica só no chat desaparece no próximo compact, em silêncio.

### Estados e aceitação

Nenhum ADR é aceito por omissão, e nenhum é aceito sem aprovação explícita do usuário.
Um ADR com questões em aberto está bloqueado por elas. Ao aceitar, remova a seção
`## Questões em aberto` e mova o que foi decidido para `## Decisão` ou `## Consequências`.

Um ADR **aceito** nunca é editado nem apagado. Para mudar a decisão, escreva um ADR novo
e marque o antigo como `Substituído por ADR-NNNN`. Enquanto estiver `Proposto`, editar é
permitido.

Mantenha a tabela **"Onde o debate parou"** em `docs/adr/README.md` sincronizada. Ela é o
estado do projeto.

### Convenções de ADR

- Numeração sequencial de quatro dígitos, nunca reutilizada. Arquivo:
  `NNNN-titulo-em-kebab-case.md`. Template em `docs/adr/0000-template.md`.
- Português do Brasil, com acentuação correta. Frases curtas. Voz ativa. Uma ideia por
  frase. Linhas quebradas manualmente em ~88 colunas.
- A seção `## Alternativas consideradas` costuma valer mais que a `## Decisão`. Cada
  alternativa leva um parágrafo começando com `**Descartada.**` e um motivo **técnico**.
  Não construa espantalhos: se a alternativa tem um argumento legítimo a favor,
  reconheça-o e mostre por que perde.
- `## Quando esta decisão deixa de valer` precisa de um sinal concreto e observável, não
  de uma intenção vaga.
- Sem emojis. Sem linguagem de marketing.

## Arquitetura conceitual

Ler só um ADR não basta; estas quatro ideias atravessam vários.

**Uma única invariante.** `Σ(alocações ativas) ≤ capacidade` e `capacidade disponível ≥ 0`.
Nenhuma outra regra de negócio existe. Toda complexidade do repositório é infraestrutura
de consistência, não domínio (ADR-0001).

**Dois modelos de verificação.** `MATERIALIZED` (contador na linha do recurso) produz
lost update; `DERIVED` (soma das alocações) produz write skew, que lock de linha não
alcança. A mesma invariante gera duas famílias de anomalia. O resultado mais valioso do
laboratório vive aqui: `DERIVED` + `OPTIMISTIC` é uma **proteção presente e inerte** —
a anotação está lá, nenhuma exceção é lançada, e a invariante quebra (ADR-0001, ADR-0003).

**Dois planos.** O Control Plane é o sistema sob teste; o Lab Plane é o instrumento que o
mede. Confundir os dois invalida qualquer conclusão — um bug no instrumento vira um falso
resultado de consistência. A regra 6 do ADR-0006 impõe isso com ArchUnit.

**O grupo de controle é obrigatório.** A estratégia `NONE` não é um estado provisório: se
`NONE` não violar a invariante, o experimento não tem carga suficiente e o resultado das
outras estratégias não significa nada. O mesmo padrão reaparece em outros ADRs
(`target: AUTHORITATIVE` no 0013, executor síncrono no 0009).

**O veredito tem dois eixos.** Safety (`safety.violations == 0`, nunca pode ser violado)
e liveness (`convergence.seconds < N`, é o objeto da medida). A distinção existe porque um
fato externo legítimo — a capacidade encolheu — viola a invariante sem nenhuma
concorrência. Rejeitar um comando é legítimo; rejeitar um fato observado não é (ADR-0002).

## Regras estruturais que valem sempre

- **`shared/` nunca contém domínio.** Só envelope de evento, correlação, tipos de erro de
  transporte e a fonte de aleatoriedade semeada. Entidade, invariante ou DTO de serviço lá
  transformaria o laboratório num monólito distribuído (ADR-0005).
- **`experiments/` guarda definições; `docs/experiments/` guarda resultados.** Os dois
  entram no Git — juntos, o histórico vira um caderno de laboratório (ADR-0004).
- **Nenhuma aleatoriedade não semeada.** `Math.random()`, `java.util.Random` e
  `ThreadLocalRandom` são proibidos fora do componente de aleatoriedade semeada. Uma
  chamada esquecida quebra a reprodutibilidade em silêncio, meses depois (ADR-0004,
  ADR-0006 regra 7).
- **O tempo é injetável.** `Instant.now()`, `LocalDateTime.now()` e
  `System.currentTimeMillis()` só em adaptador de relógio. O relógio é uma origem de
  escrita, e sem isso expiração de lease e clock skew ficam impossíveis de testar
  (ADR-0006 regra 8).
- **O domínio é Java puro.** Sem Spring, sem JPA, sem Jackson. A invariante é testável com
  um `new` e um `assert`, em milissegundos (ADR-0006).

## Estado atual do debate

13 ADRs, **todos `Proposto`, nenhum aceito.** Os ADRs 0001 e 0002 chegaram a ser aceitos e
foram reabertos quando objeções posteriores os atingiram.

Os ADRs 0008 a 0013 foram rascunhados de uma vez, em paralelo, e **nenhum foi debatido**.
Escritos sem se ver, produziram tensões entre si que estão listadas em
`docs/adr/README.md`, seção "Tensões entre os rascunhos".

**O ADR-0011 (decomposição em serviços) é o próximo a debater e destrava os demais.** A
colisão que ele resolve: o ADR-0001 verifica a invariante numa transação que toca
`resource` e `allocation`; o ADR-0005 proíbe um serviço de ler a tabela de outro. As duas
só coexistem se os dois agregados pertencerem ao mesmo serviço. Isso decide se as
estratégias da Etapa 1 (`ATOMIC_UPDATE`, `OPTIMISTIC`, `PESSIMISTIC` — todas mecanismos de
um banco só) são sequer aplicáveis.

**Os cinco serviços do esqueleto nunca foram decididos.** Os nomes em `services/` são uma
hipótese de trabalho. Não os trate como decisão.

## Ao trabalhar aqui

- Questione decisões quando fizer sentido, e explique trade-offs. O usuário pediu
  explicitamente mentoria arquitetural, não geração de código.
- Prefira registrar uma questão em aberto a inventar uma decisão para fechar uma lacuna.
  No processo deste repositório, a primeira vale mais que a segunda.
- Ao mexer em arquivos, faça `git add` apenas dos arquivos relacionados e gere um único
  commit em Conventional Commits (skill `commit`).
