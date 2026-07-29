# ADR-0001: O passo como unidade de execução, observação e injeção de falha

- **Estado:** Proposto
- **Data:** 2026-07-28
- **Etapa do roadmap:** 1
- **Relacionado:** nenhum ADR aceito. Substitui em intenção o impasse do
  `arquivo/0012`. Referencia a regra 6 do `arquivo/0006`. Deixa uma ponta para a
  decisão 3 da fila (estratégias) e para o ADR do escalonador.

## Contexto

O repositório não tem código. O plano do laboratório
([`../plano-do-laboratorio.md`](../plano-do-laboratorio.md), seção 2) identifica esta
como a primeira decisão da fila, e toda outra herda a forma que ela escolher: o
formato da timeline, os pontos de injeção de falha, o mecanismo de barreira e a
viabilidade do replay determinístico.

Três exigências do briefing incidem sobre o mesmo lugar.

**Barreiras determinísticas (cenário 25).** O experimento E2 do MVP precisa produzir a
intercalação `W1.READ → W2.READ → W1.WRITE → W2.WRITE` em **toda** execução. Para
pausar o W1 entre a leitura e a escrita, alguém precisa deter o controle entre as
duas.

**Injeção de falha em ponto nomeado.** O briefing lista doze pontos: `BEFORE_READ`,
`AFTER_READ`, `BEFORE_WRITE`, `AFTER_WRITE`, `BEFORE_COMMIT`, `AFTER_COMMIT`,
`BEFORE_PUBLISH`, `AFTER_PUBLISH`, `BEFORE_CONSUME`, `AFTER_CONSUME`, `BEFORE_ACK`,
`AFTER_ACK`. Eles precisam ser referenciáveis pela definição de um experimento antes
de qualquer execução.

**A timeline.** O briefing quer ver `12:01:00.100 Worker-1 READ resource=42 version=1`.
Isso é um registro por passo, com o instante em que o passo terminou.

Duas restrições já existentes limitam as respostas possíveis. A regra 6 do
`arquivo/0006` proíbe o Control Plane de importar o Lab Plane. E o MVP inteiro roda
numa JVM só, o que torna essa separação verificável apenas por regra executável — não
há fronteira física que a imponha.

## Problema

Um método Java executa do começo ao fim sem devolver o controle. Entre a linha que lê
e a linha que grava não existe nada — nenhum lugar onde pausar, falhar ou registrar.

A pergunta é: **qual é a forma de uma operação, tal que exista uma fronteira
observável e controlável entre dois passos consecutivos, sem que o sistema sob teste
passe a conter o instrumento que o mede?**

As forças em conflito:

- Fidelidade. Quanto mais a operação se parecer com o código que um engenheiro
  escreveria, mais o resultado significa alguma coisa.
- Controle. Quanto mais fronteiras o runtime dominar, mais determinística é a
  reprodução.
- Separação. Um bug do instrumento não pode virar um resultado de consistência.
- Inspecionabilidade. A UI e a definição versionada do experimento precisam nomear um
  ponto de barreira **antes** de executar a operação uma primeira vez.

## Decisão

### A forma

Uma operação é uma **sequência ordenada e finita de passos nomeados**, construída a
cada execução e executada pelo runtime do laboratório. O runtime chama o passo. O
passo nunca chama o runtime.

O esboço abaixo é ilustrativo — fixa a forma, não a API:

```
operação increment(resourceId):
  escopo transacional {
    READ     rótulo "select-resource"  → SELECT value, version FROM resource WHERE id = ?
    COMPUTE  rótulo "increment"        → value + 1
    WRITE    rótulo "update-resource"  → UPDATE resource SET value = ?, version = version + 1 ...
  }
```

Cada passo carrega três coisas:

- um **rótulo**, único dentro da operação;
- um **tipo**, de um conjunto fechado que o runtime entende: `READ`, `COMPUTE`,
  `WRITE`, e adiante `PUBLISH`, `CONSUME`, `ACK`;
- um **corpo opaco**, que o runtime executa sem inspecionar.

O corpo é código Java comum, executando SQL real numa transação real num PostgreSQL
real. O runtime não gera, não interpreta e não analisa SQL.

### A tentativa é a unidade de sequência

A sequência de passos é a **tentativa**, não a operação. Uma execução de operação
produz uma ou mais tentativas. Ao fim de uma tentativa malsucedida, o runtime pergunta
se há outra; quem responde é a estratégia de concorrência, que é a decisão 3 da fila.
O runtime só precisa de "sim" ou "não".

O motivo é o `OPTIMISTIC`, que está no E3 e portanto no MVP: ele lê, calcula, grava e
**repete** ao conflitar. Uma sequência ordenada e finita não tem laço. Colocar o laço
dentro do runtime daria ao runtime estrutura de controle, e o argumento que derruba a
alternativa D deste ADR — o interpretador vira uma linguagem de programação pior —
passaria a valer contra a própria decisão.

O ganho não é apenas evitar o laço. O número de tentativas passa a ser um dado
observável do log, e é exatamente a métrica que o E3 e o E4 precisam: retries por
operação crescendo mais rápido que linearmente sob contenção.

A hierarquia completa:

```
execução de operação
└── tentativa                 1..N, decidida pela estratégia
    └── escopo transacional
        └── passo
            └── fronteira     entrada, saída
```

### A fronteira

Cada passo é cercado por duas fronteiras endereçáveis: a de entrada e a de saída. O
endereço canônico de uma fronteira é a tripla **(rótulo do passo, entrada|saída,
seletor de tentativa)**.

Os doze pontos do briefing são a convenção de nomenclatura da parte (rótulo,
entrada|saída) quando o tipo é único na operação: `BEFORE_READ` é a fronteira de
entrada do único passo de tipo `READ`. Quando o tipo aparece mais de uma vez, a
plataforma **rejeita** o nome abreviado em vez de escolher um dos passos.

O seletor de tentativa **não tem valor padrão**. Uma definição que diga apenas
`AFTER_READ` é rejeitada em qualquer operação que possa tentar mais de uma vez. O
motivo é que as duas leituras plausíveis medem coisas diferentes: uma barreira que
dispare em toda tentativa transforma um laço de retry em impasse, com um agendamento
escrito para uma passagem só; e uma falha injetada apenas na primeira tentativa testa
recuperação, enquanto uma falha injetada em todas testa esgotamento. Escolher em
silêncio produziria experimentos que medem outra coisa sem avisar ninguém.

Em cada fronteira o runtime faz duas coisas, **nesta ordem**:

1. consulta o escalonador, e bloqueia a thread do worker se houver barreira;
2. consulta o injetor de falha, e falha se houver falha declarada ali.

A ordem não é arbitrária. Se a injeção viesse antes do bloqueio, o worker morreria sem
nunca chegar à barreira, e o escalonador esperaria para sempre por um worker que já
não existe. Injetar depois de liberar mantém a falha dentro da ordem declarada.

### A observação

A observação não é o terceiro ato da fronteira. Ela é emitida **no instante em que
cada evento ocorre**:

- o resultado de um passo é observado quando o passo termina, antes da fronteira de
  saída ser consultada;
- o bloqueio e a liberação numa barreira são observados quando acontecem;
- a falha injetada é observada quando é lançada.

O motivo é a timeline. Se a observação do `READ` só fosse emitida depois da barreira
liberar, a timeline mostraria o `READ` do W1 acontecendo depois do `READ` do W2 — o
instrumento mentiria sobre a própria ordem que ele impôs.

O que o passo reporta é um conjunto de fatos (`version=1`, `rowsAffected=0`). O
runtime registra sem interpretar. Toda observação carrega o número da tentativa.

### A transação é demarcada através do Spring, não no lugar dele

O runtime abre o escopo transacional com `TransactionTemplate`, e os passos daquele
escopo rodam dentro do callback. Um escopo envolve uma sub-sequência contígua de
passos de uma tentativa.

O que isso preserva: o `PlatformTransactionManager`, a propagação, o nível de
isolamento configurado, os recursos ligados à thread e as regras de rollback. Nada
disso é reimplementado pelo laboratório, e o `SQLSTATE 40001` continua chegando pelo
caminho normal.

Consequência sobre os pontos nomeados: **`COMMIT` não é um passo que o runtime
executa.** Ele é o retorno do callback. `BEFORE_COMMIT` é a última fronteira dentro do
escopo; `AFTER_COMMIT` é a primeira fronteira depois dele. Isso é mais fiel que um
passo `COMMIT` explícito, e dá sentido exato à etapa 6: o commit aconteceu, o callback
retornou, e a falha injetada logo em seguida produz o dual write sem publicação.

### A resolução é um eixo do experimento

`@Transactional` continua possível, e não como concessão.

Para o runtime, uma operação com demarcação declarativa é uma sequência de **um passo
só**: corpo opaco, nenhuma fronteira interna, nenhuma barreira interna. O modelo não
precisa de uma segunda classe de operação — ele degenera. E a operação declarativa não
importa nada do Lab Plane: o runtime a chama como caixa-preta, e a regra 6 continua
verde.

Isso dá dois modos de resolução, e a escolha é do experimento, não da plataforma:

| Resolução | Forma                                             | Fronteiras internas | Serve para                                              |
|-----------|---------------------------------------------------|---------------------|---------------------------------------------------------|
| alta      | sequência de passos, escopo por `TransactionTemplate` | todas           | E2, E5, injeção em ponto nomeado, timeline fina         |
| baixa     | método `@Transactional`                           | nenhuma             | E1, carga alta, o lado sem barreiras da cláusula abaixo |

### A cláusula de honestidade

Toda anomalia reproduzida com barreiras precisa aparecer **também** sem barreiras, sob
carga alta. Se aparecer só com barreiras, o runtime está fabricando o fenômeno, e o
experimento não vale.

Com o eixo de resolução, esta cláusula fica mais forte do que era. "A mesma anomalia
sem barreiras" deixa de significar apenas "a mesma sequência de passos com o
escalonador desligado" e passa a poder significar **"o mesmo fenômeno no código que um
engenheiro escreveria"**. É uma resposta melhor à objeção de fidelidade do que
qualquer argumento textual deste documento.

A cláusula é obrigatória para todo experimento do laboratório. O E1 e o E2 do MVP a
exercitam primeiro.

### O que este ADR não decide

**A linguagem do agendamento.** A decisão fixa que existe uma fronteira consultável e
como ela é endereçada. Não fixa como uma barreira é declarada — se
`W1.READ → W2.READ → W1.WRITE → W2.WRITE` é uma lista ordenada de endereços, uma
máquina de estados, ou outra coisa. É ADR próprio, e ele depende deste.

**Quando há outra tentativa.** O runtime pergunta; a estratégia responde. A política é
a decisão 3 da fila.

Fica registrado para que a ausência não seja lida como omissão.

## Questões em aberto

### 1. O endereço da fronteira precisa sobreviver à edição da operação

Definições de experimento são versionadas e referenciam fronteiras. O rótulo sobrevive
à inserção de um passo no meio da operação — o índice não sobreviveria, e é por isso
que o rótulo foi escolhido. Mas o rótulo não sobrevive a uma renomeação, e nada impede
que o corpo de um passo mude mantendo o rótulo.

A etapa 12 quer reexecutar um experimento antigo e obter o mesmo resultado. Se o corpo
do passo mudou, o replay é de outro experimento com o mesmo nome. Nenhum mecanismo de
versionamento de operação foi proposto.

### 2. Uma operação construída por engano como singleton fabrica a anomalia

A decisão diz "construída a cada execução". O motivo é grave: se os passos fecharem
sobre estado compartilhado — um campo de bean, um `static`, um objeto de estado
reaproveitado — dez workers passam a escrever no mesmo `value` intermediário, e o
laboratório produz atualizações perdidas **dentro do próprio instrumento**.

O resultado é indistinguível de um lost update real. Nenhum teste falha. O relatório
fica plausível.

A regra 7 do `arquivo/0006` protege contra aleatoriedade não semeada com um teste
ArchUnit, porque `Math.random()` é um nome verificável. Aqui não há nome: "este lambda
captura estado compartilhado" não é uma consulta de ArchUnit. Que guarda executável
detecta isso?

### 3. As duas resoluções da mesma operação podem divergir em silêncio

A cláusula de honestidade compara uma anomalia produzida em alta resolução com a mesma
anomalia em baixa resolução. Isso só prova alguma coisa se as duas formas fizerem a
mesma coisa. E elas são código separado: uma sequência de passos e um método
`@Transactional`.

Nada impede que divirjam — um `WHERE` a mais, uma coluna a menos, um cálculo diferente.
Se divergirem, a cláusula deixa de comparar duas execuções do mesmo experimento e passa
a comparar dois experimentos, sem que ninguém perceba. É a mesma família de falha
silenciosa da questão 2.

Gerar uma forma a partir da outra resolveria, e reintroduziria a alternativa D pela
porta dos fundos: para gerar o método declarativo a partir dos passos, o runtime
precisaria entender o SQL que ele decidiu não entender.

### 4. O escalonador precisa de um protocolo de desistência

A ordem escolhida na fronteira (bloquear, depois falhar) evita que um worker morra
antes de chegar à barreira. Não evita o inverso: um worker que falha na fronteira de
saída do passo N nunca chegará à fronteira de entrada do passo N+1, e um escalonador
que espere por ele trava a execução inteira.

O runtime precisa notificar o escalonador de que um worker terminou — por falha
injetada, por exceção do banco ou por conclusão. A forma dessa notificação não foi
decidida, e ela pertence ao ADR do escalonador, não a este.

## Consequências

### Positivas

- As três exigências do briefing passam a ser a mesma exigência atendida uma vez. A
  barreira, o ponto de falha e a linha da timeline são o mesmo lugar do código.
- O impasse do `arquivo/0012` deixa de existir. Ele escolhia entre interceptar dentro
  do processo (fiel, mas contamina), no broker (isolado, mas entra na medida de
  latência) ou na rede (puro, mas não produz duplicata semântica). Com o runtime
  dirigindo, a direção da dependência se inverte: a injeção fica dentro do processo,
  que é o modo fiel, e a regra 6 continua verde.
- `AFTER_COMMIT` fica exato. Como o commit é o retorno do callback do
  `TransactionTemplate`, existe um instante inequívoco em que a transação já terminou e
  nada mais aconteceu. É a fronteira de que a etapa 6 depende.
- A operação é inspecionável antes de executar. A UI consegue listar os pontos de
  barreira de um experimento sem rodá-lo, e a definição versionada consegue
  referenciá-los.
- A timeline não precisa de instrumentação adicional. Ela é a projeção direta do log de
  observações, que já existe porque a fronteira existe.
- Os doze pontos nomeados do briefing saem de graça. Não há doze ganchos para manter;
  há um mecanismo e uma convenção de nomes.
- O número de tentativas vira dado de primeira classe do log, sem nada a mais: a
  métrica central do E3 e do E4 é subproduto de a tentativa ser a unidade.

### Negativas

- **Duas formas da mesma operação para manter.** O eixo de resolução compra a resposta
  de fidelidade ao preço de escrever o experimento duas vezes, e a cláusula de
  honestidade depende de as duas não divergirem. Ver questão 3.
- **O estado intermediário sai das variáveis locais.** `value + 1` calculado no
  `COMPUTE` precisa chegar ao `WRITE` por um escopo de execução explícito. Isso é mais
  verboso e mais fácil de errar que uma variável local — e o erro tem a forma da
  questão 2.
- **A operação em alta resolução não é o código que um engenheiro escreveria.** A regra
  pedagógica do repositório quer mostrar o problema no código real. A sequência de
  passos é uma tradução, e o leitor precisa fazer o mapeamento de volta. A forma de
  baixa resolução mitiga isso, mas não elimina.
- O endereço da fronteira ganhou um terceiro componente obrigatório. Definições de
  experimento ficam mais verbosas, e a exigência de declarar a tentativa vai incomodar
  em operações que nunca tentam duas vezes.
- Duas fronteiras por passo em vez de uma. É mais explícito, mas dobra o número de
  endereços que um experimento pode referenciar, e alguns deles são inúteis.
- O runtime vira código crítico do laboratório. Um bug nele contamina todos os
  experimentos ao mesmo tempo, e a cláusula de honestidade é a única defesa
  automatizada contra isso.

### Neutras

- O número de threads passa a ser função do número de workers, e o pool de conexões
  precisa ser maior que ele. Isso já era exigência do plano (seção 8); a decisão apenas
  a torna estrutural.
- Todos os passos de uma tentativa rodam na mesma thread, dedicada ao worker. A
  transação e a conexão ficam ligadas a essa thread do início ao fim do escopo, e a
  barreira bloqueia essa thread com os locks de linha segurados. Isso é desejado: é
  assim que contenção pessimista e deadlock são produzidos.
- Se essas threads são de plataforma ou virtuais é decisão da arquitetura mínima
  (decisão 7 da fila), não desta.

## Alternativas consideradas

### Alternativa A — método Java linear, sem passos

A operação é um método `@Transactional` comum. As anomalias aparecem por concorrência
real, sob carga alta.

**Descartada como forma única.** É a alternativa mais fiel que existe: o código é
literalmente o código de produção, não há interpretador para depurar e nenhuma dúvida
sobre o que está sendo medido. O argumento a favor é legítimo, e o eixo de resolução
desta decisão o incorpora — esta alternativa sobrevive como o modo de baixa resolução.

Ela perde como forma única porque não existe fronteira. Sem fronteira não há barreira,
não há ponto de falha nomeado e não há timeline por passo. O laboratório voltaria a
depender da sorte do escalonador, e o E2 — o experimento que prova que a plataforma
*constrói* a anomalia, e não apenas a *detecta* — seria impossível. O cenário 25,
marcado como "particularmente importante" no briefing, é exatamente a proibição desta
alternativa como forma única.

### Alternativa B — barreiras e ganchos inline no código do sistema sob teste

A operação continua um método linear, e o autor insere `barreira.espera("AFTER_READ")`
entre a leitura e a escrita.

**Descartada.** É a solução mais simples que funciona, e ela tem duas vantagens reais
sobre a decisão escolhida: as variáveis locais continuam funcionando, e a transação
continua demarcada onde um engenheiro a demarcaria.

Há ainda um contra-argumento honesto contra a objeção óbvia: se `barreira` fosse uma
porta declarada no Control Plane e implementada no Lab Plane, a regra 6 não seria
violada na forma. Isso é verdade — e insuficiente. A regra 6 existe para que o sistema
sob teste não saiba que está sendo medido; declarar a porta é o sistema sob teste
falando a linguagem do instrumento.

O motivo decisivo é outro, e é prático. Um método linear com ganchos só revela seus
pontos de pausa **executando**. O runtime não tem a lista de passos antes de rodar a
operação uma primeira vez. O Experiment Designer da UI não consegue oferecer os pontos
de barreira, e a definição versionada do experimento não consegue referenciá-los sem
que alguém os transcreva à mão do código — uma lista manual que apodrece, exatamente
como a questão 1 do `arquivo/0006` já previa em outro contexto.

### Alternativa C — instrumentação por aspecto ou bytecode

Um aspecto envolve os métodos do sistema sob teste e insere as fronteiras sem tocar no
código.

**Descartada.** Ela entrega o que B não entrega — contaminação visual zero — e mantém
`@Transactional` funcionando.

A granularidade é o problema. Um aspecto intercepta chamadas de método, e
`READ → COMPUTE → WRITE` dentro de um método não tem chamada nenhuma. Fragmentar em
métodos privados não resolve: a auto-invocação não passa pelo proxy do Spring.
Fragmentar em beans separados resolve, e nesse ponto a decomposição por passo já
aconteceu — só que implícita, sem nome estável e sem ordem declarada. Seria a decisão
escolhida, com todos os custos dela e nenhum dos benefícios de inspecionabilidade.

### Alternativa D — passos como dado puro, em DSL ou JSON

A operação inteira é declarada num arquivo, com o SQL de cada passo escrito ali. O
runtime interpreta.

**Descartada.** O ganho é grande e vale nomear: inspecionabilidade máxima, replay
trivial, o experimento inteiro cabe num arquivo versionado, e a UI monta operações sem
compilar nada.

Ela perde por dois motivos. O primeiro é técnico: qualquer passo com lógica — o
predicado do E5, a política de retry do `OPTIMISTIC` — exige estender a DSL, e uma DSL
estendida sob pressão vira uma linguagem de programação pior que Java. O segundo é
pedagógico e mais grave: a regra do repositório é mostrar o problema no código que um
engenheiro escreveria. Um JSON não é esse código, e o leitor perderia a única coisa que
o laboratório tem para ensinar.

### Alternativa E — continuações, com o passo cedendo o controle

O corpo da operação continua linear e cede o controle ao runtime em pontos marcados.

**Descartada.** Preservaria o código linear e a demarcação de transação, e é a única
alternativa que atacaria as questões 2 e 3 de frente.

A API de continuação delimitada da JVM é interna (`jdk.internal.vm.Continuation`) e
exige `--add-exports` para ser usada. Um laboratório cuja fundação depende de API
interna troca um problema conhecido por um imprevisível. E o ponto de cessão ainda
precisaria ser marcado no código do sistema sob teste — ou seja, a contaminação da
alternativa B permanece, com um mecanismo de bloqueio mais caro. Com uma thread por
worker, bloquear é trivial; a continuação não compra nada que a thread já não dê.

### Alternativa F — o runtime abre e fecha a transação por conta própria

O runtime pega a conexão do pool, chama `setAutoCommit(false)`, executa os passos e
chama `commit()`, sem passar pelo Spring.

**Descartada.** É o caminho mais direto para ter `BEGIN` e `COMMIT` como passos
explícitos e endereçáveis, e elimina qualquer dúvida sobre quem controla a transação.

Ela perde porque reimplementa o que já existe. Propagação, nível de isolamento,
recursos ligados à thread, tradução de exceção e regras de rollback passariam a ser
código do laboratório — código que precisaria estar correto para que qualquer resultado
significasse alguma coisa, e que ninguém pediu para estudar. Pior: a operação declarada
deixaria de rodar sob a mesma infraestrutura transacional da operação `@Transactional`,
e o eixo de resolução perderia o sentido. As duas resoluções precisam commitar do mesmo
jeito para que a comparação entre elas prove alguma coisa.

## Quando esta decisão deixa de valer

Reveja esta decisão quando o corpo de um passo precisar chamar o runtime para
funcionar. O sinal concreto: um passo que não consiga executar sem consultar o
escalonador, o injetor ou o log de observações no meio do próprio corpo. Isso
significaria que a fronteira entre passos não é fina o bastante para o fenômeno em
estudo, e que a unidade de execução precisa ser menor que o passo.

Reveja também se a asserção de honestidade falhar em qualquer experimento — se uma
anomalia aparecer em alta resolução e nunca em baixa, sob carga alta. Isso não é um
experimento ruim; é o runtime fabricando o fenômeno, e a forma da operação passa a ser
a suspeita principal.
