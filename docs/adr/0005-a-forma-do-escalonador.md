# ADR-0005: A forma do escalonador — estado, decisão e protocolo de desistência

- **Estado:** Aceito
- **Data:** 2026-08-01
- **Etapa do roadmap:** 1
- **Relacionado:** depende do ADR-0001 (escalonador pressuposto), do ADR-0002 (oráculo)
  e do ADR-0003 (chegada, travessia, agendamento). **Subsume** a tabela de classificação
  do ADR-0004, sem substituí-lo, pela convenção emendada em 2026-07-31 ([
  `README.md`](README.md#substituição-e-subsunção-são-coisas-diferentes)).
- **Questões que este ADR resolve:** [`Q-0001-4`](../questions/Q-0001-4.md),
  [`Q-0002-2`](../questions/Q-0002-2.md), [`Q-0003-1`](../questions/Q-0003-1.md),
  [`Q-0003-2`](../questions/Q-0003-2.md).

- **Última atualização:** 2026-08-05
- **Errata:** a citação `README.md:598-609`, na seção `## Contexto`, quebrou em
  2026-08-03, quando o índice encolheu de 908 para 517 linhas. A seção citada era
  `### Q-0002-2`, extraída para
  [`../questions/Q-0002-2.md`](../questions/Q-0002-2.md). O corpo não foi editado.
  Decisão `C-6`, em `../architecture/decisoes-pendentes.md`.

## Vocabulário

Este documento pressupõe **passo**, **fronteira** e **tentativa** do ADR-0001;
**chegada**, **travessia**, **papel**, **carga**, **agendamento** e **encontro** do
ADR-0003; **execução medida**, **execução de controle** e **janela de exposição** do
ADR-0004. Ele define dois termos.

- **término** — o instante em que um worker para de tentar uma execução de operação. Por
  commit final, por resposta negativa da estratégia a "há outra tentativa?", ou por
  falha não recuperada por ela.
- **desistência** — o efeito do término de um worker sobre uma restrição pendente cujo
  antecedente é uma chegada dele que não vai mais ocorrer.

## Contexto

O ADR-0001 fixou que o runtime consulta o escalonador em cada fronteira e registrou a
ausência: "a decisão não fixa como o escalonador decide, que estado ele guarda, nem como
um worker que morreu o notifica" (`0001-o-passo-como-unidade-de-execucao.md:327-330`). O
ADR-0003 definiu a linguagem do agendamento sem definir quem a executa. O ADR-0004
definiu que o oráculo lê o banco depois do último término, sem dizer quem observa esse
instante (`README.md:598-609`).

Duas responsabilidades caem no mesmo componente. Toda execução precisa de um sinal de
"todos os workers terminaram" antes que o oráculo leia. Só a execução de controle
positivo, com agendamento do ADR-0003, resolve restrições de precedência.

Um worker que termina — por falha injetada ou por sucesso — antes de produzir a chegada
que uma restrição espera trava os workers que aguardam essa chegada. O sintoma é
idêntico ao de um bug do runtime.

## Problema

**Que estado o escalonador guarda, como ele sabe que um worker terminou, e o que
acontece com uma restrição cujo antecedente não vai mais ocorrer?**

Forças em conflito:

- Determinismo. O término precisa ser observado no instante em que ocorre, como o
  ADR-0001 exige para todo evento.
- Terminação. Uma restrição sem antecedente não pode travar a execução para sempre.
- Reuso. O mesmo mecanismo precisa servir a execuções sem agendamento.
- Nomeação. Uma execução que desiste não é o mesmo caso que os cinco já classificados
  pelo ADR-0004.

## Decisão

O escalonador mantém, por execução, um contador de workers ativos e um conjunto de
restrições de precedência pendentes. O conjunto é vazio fora da execução de controle.

O runtime relata dois eventos ao escalonador: a **chegada** de um worker numa fronteira,
como o ADR-0001 já exige, e o **término** de um worker, evento novo desta decisão.

```mermaid
sequenceDiagram
    participant W as worker
    participant R as runtime
    participant Esc as escalonador
    W ->> R: tentativa termina
    R ->> R: commit, ou estratégia diz "não há outra"?
    R ->> Esc: término do worker
    Esc ->> Esc: decrementa ativos, resolve restrições pendentes
```

### O contador de ativos sinaliza o fim da execução

Quando o contador chega a zero, o escalonador sinaliza "execução terminada". É este
sinal que o oráculo do ADR-0002 aguarda antes de ler o banco.
[`Q-0002-2`](../questions/Q-0002-2.md) fecha aqui: o escalonador declara, o oráculo
espera.

### O término resolve a desistência

Ao receber o término de um worker, o escalonador verifica toda restrição pendente cujo
antecedente cite aquele worker numa fronteira que ele não alcançou. Se existir, a
restrição não pode mais ser satisfeita — **desistência** — e quem espera por ela é
liberado.

A desistência cobre os dois casos das questões encaminhadas. Um worker morto por falha
injetada nunca chega — [`Q-0001-4`](../questions/Q-0001-4.md). Um worker que comete na
tentativa 1 nunca produz a chegada agendada para a tentativa 2 —
[`Q-0003-2`](../questions/Q-0003-2.md). Os dois terminam pelo mesmo evento.

### O veredito nomeia a desistência

Uma execução de controle com desistência produz o sexto valor da tabela de classificação
do ADR-0004
(`0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md:211-217`), nomeado
`agendamento não cumprido`. Os cinco valores daquele ADR continuam válidos sem alteração
para o caso que eles cobrem — uma execução de controle que termina sem desistência.
`agendamento não cumprido` cobre o caso que aquele ADR não previu: a execução de
controle que não termina o próprio agendamento.

`agendamento não cumprido` NÃO DEVE ser lido como `exposição insuficiente`. O primeiro
diz que o controle não terminou. O segundo diz que ele terminou sem violar.

### O escalonador usa `ReentrantLock` para excluir acesso ao próprio estado

O contador de ativos e o mapa de restrições pendentes vivem atrás de um único
`ReentrantLock` por execução. `chegada()` e `término()` adquirem o mesmo lock antes de
ler ou alterar qualquer um dos dois, e o liberam em bloco `finally`.

## Justificativa

**Por que dois eventos, e não um.** Chegada diz que o worker está numa fronteira agora;
término diz que ele não vai chegar a mais nenhuma. Fundir os dois exigiria que toda
chegada soubesse se é a última — resposta que só a estratégia dá.

**Por que o contador de ativos serve toda execução.**
[`Q-0002-2`](../questions/Q-0002-2.md) não depende de agendamento. Reaproveitar o evento
de término evita um segundo mecanismo para a mesma pergunta.

**Por que a desistência é imediata, e não por timeout.** Timeout mede tempo de parede,
proibido fora de um adaptador de relógio. O término já é um evento do próprio runtime.

**Por que a desistência é veredito novo, e não `inválido`.** `inválido` é a carga que
não expôs nada. `agendamento não cumprido` é a carga que expôs, mas cujo controle não
terminou o próprio agendamento. Confundir os dois esconderia a causa do relatório.

**Por que `ReentrantLock`, e não `synchronized`.** A regra estrutural deste repositório
proíbe `synchronized`, `ReentrantLock` e `AtomicInteger` no sistema sob teste, sem
exceção declarada por trecho de código. Um guard textual que procure a palavra-chave
`synchronized` em qualquer classe do sistema sob teste
([`Q-0002-1`](../questions/Q-0002-1.md), [`Q-0004-2`](../questions/Q-0004-2.md)) precisa
de uma exceção para o escalonador, se o escalonador também usar a palavra-chave. Usar
`ReentrantLock` no Lab Plane mantém a proibição sem exceção: a palavra-chave
`synchronized` nunca aparece em código nenhum do repositório, e o guard não precisa
distinguir os dois planos para decidir o que rejeitar.

## Consequências

### Positivas

- O oráculo ganha um instante único para ler o banco, derivado do mesmo evento que
  resolve desistência.
- Um worker morto por falha injetada não trava mais a execução de controle.
- [`Q-0003-2`](../questions/Q-0003-2.md) deixa de ser hipotético: `OPTIMISTIC` no E3 e
  no E4 usa o mesmo mecanismo.
- A tabela de veredito do ADR-0004 ganha o caso que faltava, sem reabrir os cinco
  aceitos.
- A proibição de `synchronized` no sistema sob teste continua sem exceção — o Lab Plane
  também não usa a palavra-chave, e um guard textual não precisa distinguir os dois
  planos.

### Negativas

- **O runtime ganha um segundo evento a emitir, além da chegada.**
- **A desistência não distingue worker morto de worker rápido.** Os dois produzem o
  mesmo veredito, e só a timeline separa os dois casos.
- **`agendamento não cumprido` é um sexto caso que ninguém debateu antes de hoje.**
- **`ReentrantLock` exige liberar o lock manualmente em bloco `finally`.**
  `synchronized` faria isso pela própria sintaxe, sem chance de esquecimento.

### Neutras

- O escalonador passa a ser componente com estado por execução, e não apenas função pura
  consultada em cada fronteira.

## Trade-offs

- O benefício **desistência determinística, sem relógio** foi aceito em troca do custo
  **um segundo evento em toda tentativa**.
- O benefício **um mecanismo só serve agendamento e término** foi aceito em troca do
  custo **o escalonador guardar estado, e não ser mais uma função pura**.
- O benefício **a tabela do ADR-0004 ganha o caso que faltava** foi aceito em troca do
  custo **um sexto veredito que ninguém debateu quando o quinto foi aceito**.
- O benefício **a proibição de `synchronized` no sistema sob teste continua sem
  exceção**
  foi aceito em troca do custo **liberar o `ReentrantLock` exige bloco `finally`
  explícito, que `synchronized` dispensaria**.

## Alternativas consideradas

### Alternativa B — máquina de estados formal por execução

Cada execução de controle tem uma FSM com estados nomeados por restrição, verificável
isoladamente.

**Descartada.** Dá mais rigor de prova. Perde por custo: o MVP só exercita controle
positivo com dois workers e uma restrição por vez. Uma FSM por restrição é código que
ninguém precisa provar antes de o E5 crescer além disso.

### Alternativa C — escalonador passivo, worker consulta por sondagem

O worker pergunta periodicamente "posso atravessar?", em vez de o escalonador empurrar a
decisão.

**Descartada.** É mais simples, sem canal de notificação. Perde porque contradiz a
exigência do ADR-0001 de observar cada evento no instante em que ocorre — a sondagem
introduz um atraso não determinístico entre o evento e a reação a ele.

### Alternativa D — bloqueio grosso com `synchronized`

`chegada()` e `término()` marcados `synchronized`, cobrindo o contador de ativos e o
mapa de restrições na mesma seção crítica.

**Descartada.** É a forma mais direta de Java para uma seção crítica composta, e não
introduz dependência nova. Perde porque a palavra-chave `synchronized` deixaria de ser
exclusiva do que este repositório proíbe: um guard textual precisaria de uma exceção
para o escalonador, e uma exceção documentada é uma exceção que alguém PODE copiar para
o lugar errado.

### Alternativa E — escalonador como ator single-thread

O runtime empurra chegada e término para uma fila, e uma única thread consome, em vez de
as threads de worker acessarem o estado diretamente.

**Descartada.** Dá ordenação determinística de brinde. Perde por custo: o worker
chamador ainda espera o processamento terminar antes de prosseguir — o mesmo bloqueio de
antes, com um componente de execução novo no meio. É o mesmo tipo de custo que a
Alternativa C já perdeu para: complexidade que o problema não pede.

## Quando esta decisão deixa de valer

Reveja esta decisão quando um controle precisar de várias restrições pendentes ao mesmo
tempo, em escala que o mapa simples não navegue sem uma FSM — o E5 com mais de dois
papéis, por exemplo.
