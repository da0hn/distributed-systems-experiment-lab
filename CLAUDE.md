# CLAUDE.md

Guia para o Claude Code (claude.ai/code) ao trabalhar neste repositório.

## Não existe código neste repositório

Não há `pom.xml`, nenhuma classe Java, nenhum `docker-compose.yml`. **Não há comando de
build, de teste ou de execução.** Se você tentar `mvn test`, `docker compose up` ou
qualquer coisa parecida, vai falhar — e o motivo não é configuração faltando.

O repositório contém documentos de planejamento, ADRs e um esqueleto de diretórios
vazios. Isso é deliberado: a decisão vem antes do código. Um ADR escrito depois da
implementação não é uma decisão, é uma justificativa.

Quando o código existir, a stack é Java 25, Spring Boot 4.x, PostgreSQL, Docker. O
RabbitMQ entra na etapa 5. O pacote raiz Java, o build e o número de módulos ainda
**não foram escolhidos** — é a decisão 8 da fila em `docs/adr/README.md`.

## O que este projeto é

Uma plataforma experimental para reproduzir, observar e comparar problemas conhecidos
de sistemas distribuídos. Não é uma aplicação de negócio: não existe pedido, pagamento,
cliente ou estoque. O escopo cobre 42 fenômenos, de lost update a cascading failure.

O documento que define tudo é [`docs/plano-do-laboratorio.md`](docs/plano-do-laboratorio.md).
Leia-o antes de propor qualquer coisa.

## O trabalho aqui é escrever e debater ADRs

Esta é a atividade principal do repositório, e ela tem um processo rígido.

### A regra dura

> **Nada que importa pode existir apenas na conversa.**

O contexto da conversa é limpo entre um ADR e outro. Toda objeção, alternativa
descartada ou pendência é escrita na seção `## Questões em aberto` do próprio arquivo do
ADR, **no mesmo turno em que é levantada** — antes de responder ou perguntar qualquer
coisa. Uma objeção que fica só no chat desaparece no próximo compact, em silêncio.

### Um ADR por vez, nunca em lote

A primeira série do repositório rascunhou seis ADRs de uma vez, em paralelo. Escritos
sem se ver, produziram três contradições entre si e nenhum chegou a ser debatido. O
custo foi inteiramente perdido.

**Não rascunhe ADRs antecipadamente.** A fila de decisões em `docs/adr/README.md` lista
o que precisa ser decidido e em que ordem, **sem números atribuídos** — o número é
atribuído quando o ADR é escrito.

### Estados e aceitação

Nenhum ADR é aceito por omissão, e nenhum é aceito sem aprovação explícita do usuário.
Um ADR com questões em aberto está bloqueado por elas. Ao aceitar, remova a seção
`## Questões em aberto` e mova o que foi decidido para `## Decisão` ou `## Consequências`.

Um ADR **aceito** nunca é editado nem apagado. Para mudar a decisão, escreva um ADR novo
e marque o antigo como `Substituído por ADR-NNNN`. Enquanto estiver `Proposto`, editar é
permitido.

### Duas séries de ADR

A numeração foi reiniciada em 2026-07-28. Um mesmo número existe em duas séries.

| Forma de citar | Onde vive | O que é |
|---|---|---|
| `ADR-0001` | `docs/adr/` | série corrente |
| `arquivo/0001` | `docs/adr/arquivo/` | primeira série, arquivada, nenhum aceito |

**Sempre use o prefixo `arquivo/` ao citar a série antiga.** Sem ele a referência é
ambígua. Os documentos do arquivo **nunca são editados** — eles registram o que se
pensava naquela data.

### Convenções de ADR

- Numeração sequencial de quatro dígitos, nunca reutilizada dentro da série corrente.
  Arquivo: `NNNN-titulo-em-kebab-case.md`. Template em `docs/adr/0000-template.md`.
- Português do Brasil, com acentuação correta. Frases curtas. Voz ativa. Uma ideia por
  frase. Linhas quebradas manualmente em ~88 colunas.
- A seção `## Alternativas consideradas` costuma valer mais que a `## Decisão`. Cada
  alternativa leva um parágrafo começando com `**Descartada.**` e um motivo **técnico**.
  Não construa espantalhos: se a alternativa tem um argumento legítimo a favor,
  reconheça-o e mostre por que perde.
- `## Quando esta decisão deixa de valer` precisa de um sinal concreto e observável, não
  de uma intenção vaga.
- Sem emojis. Sem linguagem de marketing.
- Nem toda decisão merece ADR. Só as que têm alternativas plausíveis, impacto
  arquitetural duradouro, criam restrição futura ou representam um trade-off.

## Arquitetura conceitual

Ler só um ADR não basta; estas cinco ideias atravessam todo o projeto.

**Uma operação é uma sequência de passos.** Barreiras determinísticas, fault injection
em pontos nomeados e a timeline são a mesma exigência: existe uma fronteira observável
e controlável entre passos consecutivos. O runtime executa os passos e, em cada
fronteira, consulta o escalonador, consulta o injetor de falha e emite uma observação.
O que é sintético é apenas o agendamento — o SQL, a transação e o isolamento são reais.
Esta é a decisão 1 da fila, e todo o resto herda a forma que ela escolher.

**Dois planos.** O Control Plane é o sistema sob teste; o Lab Plane é o instrumento que
o mede. Confundir os dois invalida qualquer conclusão — um bug no instrumento vira um
falso resultado de consistência. Nas primeiras etapas os dois vivem na **mesma JVM**, o
que torna a separação por teste executável mais necessária, não menos. O runtime chama a
operação; a operação nunca chama o runtime.

**Cinco grupos, classificados pela causa.** Intercalação, Entrega, Escrita parcial,
Saturação, Posse no tempo. A classificação é pela fonte de não determinismo, não pela
tecnologia, porque é a causa que determina o que a plataforma precisa saber controlar.

**O veredito tem dois formatos.** Booleano (a invariante foi violada?) para os grupos A,
B, C e E. **Curva** para o grupo D — backpressure não tem estado errado, tem uma fila
crescendo e um limiar que alguém precisa declarar. Se a plataforma for construída só
para o primeiro formato, o grupo D não cabe, e isso só aparece tarde.

**O grupo de controle é obrigatório.** A estratégia `NONE` não é um estado provisório:
se `NONE` não violar a invariante, o experimento não tem carga suficiente e o resultado
das outras estratégias não significa nada. O mesmo padrão reaparece na exigência de que
uma anomalia produzida com barreiras apareça **também** sem elas, sob carga alta — sem
isso o runtime está fabricando o fenômeno, não reproduzindo.

## Regra pedagógica

> Nunca introduza primeiro a solução. Introduza primeiro o problema.

Para estudar Outbox, não comece implementando Outbox. Construa o experimento em que o
commit e a publicação são operações independentes, provoque a falha entre elas, observe
a inconsistência — e só então introduza o Outbox e rode o mesmo experimento.

```
PROBLEMA → CAUSA → SOLUÇÃO → TRADE-OFF
```

Vale para os 42 fenômenos, sem exceção.

## Regras estruturais que valem sempre

- **Nenhuma tecnologia entra por estar disponível.** Cada uma entra quando um
  experimento não puder ser executado sem ela. Antes de propor Valkey, RabbitMQ ou
  OpenTelemetry, diga qual limitação concreta da stack atual ela resolve.
- **Nenhuma aleatoriedade não semeada.** `Math.random()`, `java.util.Random` e
  `ThreadLocalRandom` são proibidos fora do componente de aleatoriedade semeada. Uma
  chamada esquecida quebra a reprodutibilidade em silêncio, meses depois.
- **O tempo é injetável.** `Instant.now()`, `LocalDateTime.now()` e
  `System.currentTimeMillis()` só em adaptador de relógio. Sem isso, expiração de lease
  e clock skew ficam impossíveis de testar.
- **Nenhuma sincronização de JVM no sistema sob teste.** `synchronized`,
  `ReentrantLock` e `AtomicInteger` mascaram exatamente os fenômenos do grupo A. A
  exceção é a estratégia `JVM_LOCK`, que existe **como experimento** para provar que
  ela falha com duas instâncias.
- **Cada worker tem sua própria conexão.** Se o pool serializar dois workers, o
  experimento produz um falso negativo silencioso.
- **`experiments/` guarda definições; `docs/experiments/` guarda resultados.** Os dois
  entram no Git — juntos, o histórico vira um caderno de laboratório. (A fonte de
  verdade entre arquivo versionado e Experiment Designer na UI ainda é uma tensão
  aberta: plano, seção 11.)

## Estado atual

**Nenhum ADR na série corrente.** O planejamento está escrito, a fila de decisões está
definida, e nada foi decidido.

O próximo passo é a **decisão 1 da fila: o passo como unidade de execução, observação e
injeção de falha**. Enquanto ela não existir, nenhuma linha de código é escrita.

A árvore de diretórios atual (`services/` com cinco pastas, `deploy/`,
`platform/observability/`) deriva das decisões **arquivadas** e não corresponde ao
plano — o MVP é uma aplicação e um banco. A limpeza acompanha a decisão 7 da fila.

## Ao trabalhar aqui

- Questione decisões quando fizer sentido, e explique trade-offs. O usuário pediu
  explicitamente mentoria arquitetural, não geração de código.
- Ao surgir uma decisão relevante: apresente o problema, apresente as alternativas,
  explique os trade-offs, recomende uma — e espere que a decisão seja consciente. Não
  decida em silêncio, e não projete a solução final antecipadamente.
- Prefira registrar uma questão em aberto a inventar uma decisão para fechar uma lacuna.
  No processo deste repositório, a primeira vale mais que a segunda.
- Ao mexer em arquivos, faça `git add` apenas dos arquivos relacionados e gere um único
  commit em Conventional Commits (skill `commit`).
