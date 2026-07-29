# ADR-0004: Experiment como entidade de primeira classe

- **Estado:** Proposto
- **Data:** 2026-07-26
- **Etapa do roadmap:** 4
- **Relacionado:** ADR-0001, ADR-0002, ADR-0003, ADR-0009

## Contexto

O laboratório existe para produzir conclusões sobre consistência distribuída. Uma
conclusão sem procedimento reproduzível não é uma conclusão. É uma anedota.

Sistemas distribuídos são não determinísticos por natureza. A ordem de execução depende
de escalonamento de threads, latência de rede e carga da máquina. Duas execuções
idênticas produzem resultados diferentes.

## Problema

Se o resultado muda a cada execução, três coisas ficam impossíveis:

- **Confirmar um bug.** Um `lost update` que apareceu uma vez em mil execuções não pode
  ser investigado. Ele não volta quando você adiciona um log.
- **Provar uma correção.** Depois de aplicar uma estratégia, a ausência do bug pode ser
  sorte.
- **Comparar estratégias.** Se a estratégia A e a estratégia B rodaram sob condições
  diferentes, a diferença de resultado não prova nada.

A pergunta é: como tornar um sistema não determinístico reproduzível o suficiente para
servir de instrumento de medida?

## Decisão

O laboratório trata `Experiment` como uma **entidade de primeira classe**, não como um
script de teste.

Um experimento é declarado em JSON, versionado no repositório, executado pelo
`experiment-service` e produz um relatório em `docs/experiments/`.

```json
{
  "name": "reorder-quebra-optimistic-lock",
  "hypothesis": "Optimistic lock NÃO protege contra heartbeat de agente fora de ordem, mas SEQUENCE_GUARD protege",
  "seed": 42,
  "resource": { "capacity": 100, "strategy": "OPTIMISTIC" },
  "load": { "operators": 10, "agents": 3, "durationSeconds": 60, "rps": 200 },
  "chaos": { "reorderProbability": 0.3, "duplicateProbability": 0.1, "delayMs": [50, 800] },
  "assertions": ["invariant.violations == 0"]
}
```

### Os quatro campos obrigatórios

**`hypothesis`.** Uma frase que pode estar errada. Este campo é obrigatório e é
verificado por revisão humana, não por código. Um experimento sem hipótese é uma
observação — ele produz números, não conhecimento. A hipótese é escrita **antes** da
execução, o que impede racionalizar o resultado depois.

**`seed`.** Uma semente que alimenta todo gerador pseudoaleatório do laboratório: o
Chaos Service, a geração de carga, os atrasos artificiais. Nenhum componente do
laboratório usa `Math.random()`, `Random` sem semente, ou `UUID.randomUUID()` em caminho
que afete a ordem de execução.

O `seed` **não** torna o sistema determinístico. Escalonamento de thread e latência de
rede real continuam livres. O `seed` torna a **injeção de falha** determinística. Isso
reduz o espaço de variação o suficiente para que um bug reapareça em algumas tentativas,
em vez de nunca.

**`assertions`.** O veredito é executável. O experimento passa ou falha sem julgamento
humano. As asserções são consultas sobre o estado final e sobre as métricas coletadas.

**`chaos`.** As probabilidades de falha são declaradas, não implícitas. Um experimento
que não declara caos declara `{}` — e isso é uma informação registrada, não uma omissão.

### O resultado é um artefato versionado

Cada execução escreve um relatório em `docs/experiments/AAAA-MM-DD-nome-seed.md`, com a
definição completa, o resultado das asserções, as métricas e o veredito sobre a
hipótese. O relatório entra no Git.

Isso transforma o histórico do repositório num caderno de laboratório.

## Questões em aberto

### 1. O veredito binário está desatualizado — o ADR-0002 o alterou

O exemplo acima declara `"assertions": ["invariant.violations == 0"]`. O ADR-0002
decidiu que a invariante do ADR-0001 tem **dois eixos de leitura**, porque o relato de
capacidade do Agent pode violá-la sem nenhuma concorrência.

| Eixo | Pergunta | Asserção | Pode ser violado? |
|---|---|---|---|
| **Safety** | O sistema **aceitou** uma escrita que quebrou a invariante? | `safety.violations == 0` | nunca |
| **Liveness** | Depois de quebrada por fato externo, o sistema **converge**? | `convergence.seconds < N` | é o objeto da medida |

Este ADR precisa ser corrigido antes de ser aceito. Três pontos exigem decisão:

- **O `Experiment` declara qual eixo verifica?** Um experimento de Operator só tem
  safety. Um de Agent tem os dois. Isso deve ser explícito no JSON ou inferido das
  origens de carga?
- **Como o limiar `N` de convergência é escolhido?** Um limiar mal calibrado produz
  falha intermitente, que é o pior resultado possível num instrumento de medida. O
  ADR-0007 já registra que o polling do relay adiciona latência mediana de 100 ms — o
  limiar precisa ser folgado o suficiente para não medir o próprio instrumento.
- **O que significa uma asserção de liveness que falha?** Pode ser bug de convergência,
  ou pode ser limiar apertado demais. As duas causas produzem o mesmo sintoma, e o
  relatório precisa conseguir distingui-las.

### 2. O instrumento não consegue medir leitura desatualizada

As asserções deste ADR são consultas sobre o **estado final** e sobre métricas
agregadas. Uma leitura desatualizada não existe no estado final: por definição, ela é um
valor que era falso no instante em que foi lido e virou verdadeiro depois. Quando o
experimento termina, não sobrou evidência dela em lugar nenhum.

O ADR-0001 lista "CQRS e defasagem de leitura" entre os seis temas que dependem do
domínio — ou seja, entre os que este laboratório existe para estudar. Mas os ADRs 0001,
0002, 0003 e 0007 tratam apenas do eixo de **escrita**: quem escreve, com que semântica,
protegido por qual mecanismo. Nenhum decide o que é uma leitura no laboratório, nem como
uma leitura errada vira um veredito.

Três coisas ficam sem definição:

- **Quem lê.** As quatro origens do ADR-0002 são origens de escrita. Não existe um ator
  leitor com contrato próprio, e sem ele não há de quem observar a defasagem.
- **Como uma leitura desatualizada é capturada.** Ela precisa ser registrada no instante
  em que acontece, com o valor lido e o valor verdadeiro na mesma marca de tempo. Isso é
  um mecanismo de amostragem, não uma consulta ao estado final — e nenhum existe.
- **Qual é a asserção.** `safety.violations == 0` não serve: nenhuma invariante foi
  violada. O sistema respondeu um valor obsoleto e correto no passado. A pergunta certa
  é sobre a distribuição da defasagem (`staleness.p99 < N`), o que exige o mecanismo de
  amostragem acima.

**Consequência prática:** enquanto isso não for decidido, todo experimento que envolva
CQRS, réplica de leitura ou projeção assíncrona produzirá um relatório que só mede
escrita. O laboratório concluiria "nenhuma violação" num cenário em que o usuário viu
dados errados o tempo todo — o pior tipo de falso negativo num instrumento de medida.

Isso pede um ADR próprio, ainda não numerado, sobre o eixo de leitura. Ele não bloqueia
a Etapa 1, mas bloqueia qualquer experimento de CQRS.

## Consequências

### Positivas

- Um bug encontrado pode ser reencontrado. Basta reexecutar com o mesmo `seed`.
- A comparação entre estratégias é honesta: mesma carga, mesmo caos, mesma semente.
- O campo `hypothesis` obriga a pensar antes de rodar. Isso é a diferença entre
  experimentar e observar.
- O `experiment-service` vira um consumidor exigente da observabilidade. Se uma métrica
  não existir, a asserção não pode ser escrita. Isso força instrumentação útil, em vez
  de instrumentação decorativa.

### Negativas

- Toda fonte de aleatoriedade do laboratório precisa aceitar a semente injetada. Isso é
  uma restrição transversal, fácil de violar por acidente. Uma chamada a
  `Math.random()` esquecida num adaptador quebra a reprodutibilidade em silêncio.
  **Mitigação:** uma regra ArchUnit proíbe `java.util.Random`, `Math.random` e
  `ThreadLocalRandom` fora do componente de aleatoriedade semeada (ver ADR-0006).
- O `experiment-service` é infraestrutura de laboratório. Ele não ensina nada sobre
  sistemas distribuídos por si só. É custo puro, justificado pelo que ele viabiliza.
- A reprodutibilidade é parcial e isso precisa ser dito com honestidade nos relatórios.
  Um experimento pode falhar em reproduzir. O relatório deve registrar quantas
  tentativas foram necessárias.

### Neutras

- O `experiment-service` pertence ao **Lab Plane**, não ao sistema sob teste. Ele é o
  instrumento. Um bug nele contamina a medida, mas não é um bug de consistência. A
  separação Lab Plane / Control Plane é protegida por ArchUnit.

## Alternativas consideradas

### Alternativa A — testes JUnit com Testcontainers

Cada cenário vira um método de teste. O resultado é o do JUnit.

**Descartada como mecanismo principal, mantida como complemento.** O JUnit é ótimo para
verificar correção sob concorrência moderada, e o laboratório usa Testcontainers
extensivamente na Etapa 1. Mas o JUnit não serve para experimento porque: a carga
sustentada de 60 segundos com 200 rps não cabe num teste unitário; o resultado é
booleano, sem métricas; e o histórico do JUnit não é versionado com contexto.

O laboratório usa os dois. Testes garantem que o código funciona. Experimentos descobrem
sob quais condições ele para de funcionar.

### Alternativa B — ferramenta de carga externa (k6, Gatling, JMeter)

Delegar a geração de carga a uma ferramenta madura.

**Descartada.** A ferramenta externa gera carga, mas não controla a semente do caos
injetado dentro dos serviços. O `seed` precisa atravessar a fronteira entre o gerador de
carga e o Chaos Service. Com ferramenta externa, seriam duas fontes de aleatoriedade
independentes, e a reprodutibilidade se perderia.

Além disso, escrever o gerador de carga é barato para o perfil de carga do laboratório,
e o custo de aprender a ferramenta não retorna em conhecimento sobre consistência.

### Alternativa C — execução manual, resultado anotado à mão

Rodar cenários pelo frontend e anotar o que aconteceu.

**Descartada.** Não escala além de meia dúzia de cenários, e o viés de confirmação é
alto: quem roda o cenário já sabe o que espera ver.

## Quando esta decisão deixa de valer

Reveja esta decisão se os relatórios pararem de ser lidos. Um caderno de laboratório que
ninguém consulta é custo sem retorno. O sinal concreto: um experimento executado cujo
relatório não foi aberto por ninguém em trinta dias.
