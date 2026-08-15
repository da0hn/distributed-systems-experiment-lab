# Roadmap

O laboratório é um instrumento. Ele reproduz um fenômeno conhecido de sistemas
distribuídos, observa o que aconteceu passo a passo, e compara o custo das estratégias
que tentam evitá-lo. O objeto de estudo é o fenômeno, e nunca a tecnologia que o
hospeda.

Este documento diz para onde o projeto vai, em alto nível. Ele não inventaria o que já
existe na árvore, e não decide nada.

## A abstração que sustenta tudo

Uma operação do sistema medido é uma sequência de passos nomeados. O runtime executa
essa sequência e, na fronteira entre dois passos, faz três coisas na ordem: pergunta ao
escalonador se aquele worker prossegue, pergunta ao injetor de falha se algo falha ali,
e emite uma observação.

Três exigências convergem para essa forma, e nenhuma delas é atendível se uma operação
for um método comum. Parar um worker entre a leitura e a escrita exige o controle entre
as duas. Injetar falha em ponto nomeado sem espalhar ganchos pelo sistema medido exige
que o gancho fique na fronteira, e não dentro. E uma timeline com um registro por passo
exige que o passo exista como unidade.

O que é sintético é o agendamento, e só ele. O SQL é real, a transação é real, o nível
de isolamento é o do PostgreSQL, e o erro de serialização vem do PostgreSQL. O
laboratório decide quando cada transação dá o próximo passo, e nada além disso.

Isso cobra um preço, e ele é pago uma vez: toda anomalia reproduzida com agendamento
precisa aparecer também sem ele, sob carga. Se ela aparecer só com agendamento, o
instrumento fabricou o fenômeno em vez de reproduzi-lo.

## Os cinco grupos de fenômenos

Os fenômenos são agrupados pela fonte de não determinismo que produz a anomalia, e não
pela tecnologia envolvida. O agrupamento importa porque ele diz o que o instrumento
precisa saber controlar para reproduzir cada família.

| Grupo           | A fonte da anomalia                                                | O que o instrumento precisa controlar                   | Veredito                |
|-----------------|--------------------------------------------------------------------|---------------------------------------------------------|-------------------------|
| Intercalação    | dois fluxos tocam o mesmo estado no mesmo banco                    | a ordem entre passos; o nível de isolamento             | booleano                |
| Entrega         | o canal não garante uma vez, em ordem, no prazo                    | a interceptação do canal, com semente                   | booleano                |
| Escrita parcial | uma mudança lógica atravessa dois sistemas que não commitam juntos | a falha em ponto nomeado; a amostragem no tempo         | booleano e convergência |
| Saturação       | nada está incorreto, e o sistema não dá conta                      | a taxa de produção, a latência e a profundidade de fila | curva                   |
| Posse no tempo  | quem tem o direito de escrever, e até quando                       | o relógio injetado; mais de um processo                 | booleano                |

**Intercalação.** Race condition, lost update, conflito otimista, contenção pessimista,
deadlock, write skew, non-repeatable read e phantom read. Substrato: um processo, N
workers, um PostgreSQL, nenhum broker. É o grupo mais barato de montar, e o que mais
depende do passo como unidade.

**Entrega.** Duplicata de mensagem e de comando, reordenação, atraso, perda, poison
message, DLQ, crash de consumidor e competing consumers. Substrato: acrescenta o broker
ao domínio medido.

**Escrita parcial.** Dual write, falha de produtor, falha de consumidor, Outbox, Inbox,
idempotência, consistência eventual, stale read e falha de projeção. Este grupo exige um
mecanismo que nenhum outro exige: a amostragem no tempo. Uma leitura defasada não
sobrevive até o estado final, porque ela era falsa no instante em que foi lida e virou
verdadeira depois. Nenhuma consulta ao estado final a encontra.

**Saturação.** Retry, retry storm, backpressure, slow consumer, thundering herd, hot
resource, ordenação contra throughput, partial failure, cascading failure e timeout.
Este grupo quebra o modelo de veredito do resto do laboratório: não existe estado
errado. Existe uma fila crescendo, e alguém precisa declarar o limiar a partir do qual
isso é falha.

**Posse no tempo.** Single writer, lock distribuído, expiração de lease e fencing token.
É o único grupo em que mais de um processo é obrigatório. Um lock distribuído com um
processo só é um lock local com passos a mais.

**Transversal.** Latência artificial de rede, event replay e replay determinístico não
são grupos. São capacidades do instrumento, e cada uma é construída junto com o grupo
que a exigir.

## A progressão de dificuldade

Doze etapas. Cada uma responde uma pergunta concreta e introduz exatamente uma
dificuldade nova. Nenhuma etapa tem infraestrutura como entregável.

| #  | A pergunta que a etapa responde                                | O que entra no instrumento                                              | Grupo                |
|----|----------------------------------------------------------------|-------------------------------------------------------------------------|----------------------|
| 1  | Como demonstrar um lost update, e provar que ele aconteceu?    | o passo como unidade; o log de observações; a timeline; o oráculo exato | intercalação         |
| 2  | Qual estratégia corrige, e a que custo?                        | a comparação entre execuções; throughput e retry                        | intercalação         |
| 3  | Por que a proteção pode estar presente e inerte?               | a verdade derivada; o nível de isolamento como parâmetro                | intercalação         |
| 4  | O que quebra quando o worker deixa de ser uma thread?          | a segunda instância do sistema medido                                   | intercalação e posse |
| 5  | O que muda quando a operação vira uma mensagem?                | o broker no domínio medido; competing consumers; duplicata              | entrega              |
| 6  | O que acontece se o processo morre entre o commit e o publish? | a injeção de falha em ponto nomeado; o Outbox                           | escrita parcial      |
| 7  | Como garantir que o efeito lógico aconteça uma vez só?         | o Inbox; a chave de idempotência; a deduplicação                        | escrita parcial      |
| 8  | Para onde vai a mensagem que nunca dá certo?                   | a política de retry; poison message; DLQ; replay                        | entrega e saturação  |
| 9  | Como medir o que o usuário viu, e não o que ficou gravado?     | a amostragem no tempo; a projeção; o tempo de convergência              | escrita parcial      |
| 10 | Quando um sistema correto deixa de servir?                     | o veredito por curva; o controle de taxa; a profundidade de fila        | saturação            |
| 11 | Quem tem o direito de escrever, e até quando?                  | o relógio injetado; o lease; o fencing token                            | posse no tempo       |
| 12 | Como transformar um bug de concorrência num teste repetível?   | o replay determinístico completo                                        | transversal          |

A quarta etapa não tem prazo. Ela acontece quando o experimento do lock de JVM ficar
vermelho com duas instâncias. Se esse experimento nunca for escrito, a etapa nunca
chega, e isso é informação, e não atraso.

A nona etapa destrava a décima e a décima primeira. A amostragem no tempo é
pré-requisito de tudo que envolve convergência, e adiá-la faz o laboratório concluir
"nenhuma violação" em cenários onde o usuário viu dado errado o tempo inteiro.

## O primeiro conjunto de experimentos

As três primeiras etapas formam o conjunto mínimo, e ele fica inteiro no grupo da
intercalação. Nenhum deles exige broker nem um segundo processo do lado medido.

- **O lost update sem proteção.** Cem incrementos, dez workers, o mesmo recurso, nenhuma
  estratégia. Este experimento precisa falhar: se o valor final bater com o esperado, a
  carga é fraca demais e nenhum resultado posterior significa coisa alguma.
- **A comparação de estratégias.** A mesma carga quatro vezes, trocando apenas a
  estratégia. Ela prova que a estratégia é um dado de configuração, e não um desvio no
  código, e mostra o custo de cada uma lado a lado.
- **O otimista sob contenção.** Estratégia fixa, workers de dois a cinquenta sobre o
  mesmo recurso. É o primeiro experimento cujo resultado é uma curva, e não um veredito
  booleano, e ele obriga o instrumento a suportar os dois formatos antes que a
  arquitetura enrijeça.
- **A proteção presente e inerte.** Dois workers leem a soma das alocações, concluem que
  cabe mais uma, e inserem. A soma excede a capacidade e nenhuma exceção é lançada:
  inserir uma alocação não versiona linha nenhuma, porque não existe linha compartilhada
  para versionar.

O último é o resultado que mais justifica o laboratório existir. Nenhum teste de unidade
o detecta, e ele mostra que ter uma estratégia de concorrência e estar protegido são
coisas diferentes.

## As regras que a progressão respeita

- **O problema vem antes da solução.** O Outbox só entra depois que o dual write falhar
  na tela. Entregar a solução de um problema que ninguém viu não ensina nada.
- **O grupo de controle é obrigatório.** A execução sem proteção precisa violar. É a
  regra que separa um laboratório de uma demonstração.
- **A separação em processos é provocada, e nunca agendada.** A arquitetura evolui
  quando um experimento fica vermelho sem a evolução. O gatilho é o lock de JVM: ele
  resolve o lost update com uma instância e falha com duas, e o resultado verdadeiro
  ensina a lição falsa enquanto ninguém rodar a segunda.
- **Nenhuma tecnologia entra por estar disponível.** Cada uma entra quando um
  experimento não puder ser executado sem ela.
- **Um zero não é uma observação.** Ele é a ausência de uma, e por isso o zero é
  classificado antes de ser reportado: a carga pode não quebrar nada, a janela pode
  estar mal declarada, a exposição pode ser insuficiente, ou a estratégia pode estar
  protegendo de fato.
- **A suspeita fica no lado do sistema medido.** Enquanto o oráculo for exato, um
  resultado estranho aponta para o sistema, e nunca para a medida.

## Onde o laboratório roda

Ele é entregue como carga de trabalho do homelab, e o Kubernetes é destino de entrega, e
não objeto de estudo. Nenhum fenômeno é reproduzido por um recurso do cluster.

O caderno de laboratório não vive no Git. A definição de cada experimento e o resultado
de cada execução ficam em banco, escritos pelo instrumento.
