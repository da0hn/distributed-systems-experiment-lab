# Dicionário de dados

O de/para do vocabulário deste laboratório.

**Os termos são em inglês, e as explicações em português.** Todo identificador de
código é escrito em inglês, e este dicionário nomeia o que vira código. O corpus escrito
do repositório é português, e a tabela abaixo é a ponte entre os dois.

## Português para inglês

| Português                    | Inglês                  | O que é                                                                                                         |
|------------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------|
| `sistema sob teste`          | `system under test`     | O plano medido: as operações, as estratégias e o acesso ao banco.                                               |
| `operação`                   | `operation`             | Uma sequência ordenada e finita de passos nomeados, executada pelo runtime.                                     |
| `definição de operação`      | `operation definition`  | A fábrica sem estado que monta a sequência de passos, chamada uma vez por tentativa.                            |
| `passo`                      | `step`                  | Uma unidade nomeada de trabalho do sistema medido, cujo corpo o runtime não inspeciona.                         |
| `rótulo`                     | `label`                 | O nome de um passo, único dentro da operação.                                                                   |
| `tipo de passo`              | `step type`             | Um valor de conjunto fechado que o runtime entende, como `READ`, `COMPUTE` e `WRITE`.                           |
| `corpo opaco`                | `opaque body`           | O código de um passo, que emite SQL real e que o runtime não gera nem interpreta.                               |
| `fronteira`                  | `boundary`              | O instante em que o controle está com o runtime, e não com o corpo do passo.                                    |
| `endereço de fronteira`      | `boundary address`      | A tripla rótulo, entrada ou saída, e seletor de tentativa, que identifica uma fronteira.                        |
| `seletor de tentativa`       | `attempt selector`      | A parte do endereço que diz em qual tentativa aquela fronteira vale.                                            |
| `tentativa`                  | `attempt`               | Uma passagem completa pela sequência de passos.                                                                 |
| `execução de operação`       | `operation execution`   | A invocação de uma operação por um worker, do começo até o término. Contém as tentativas.                       |
| `escopo de execução`         | `execution scope`       | Onde vive o estado intermediário entre dois passos de uma tentativa.                                            |
| `escopo transacional`        | `transactional scope`   | A sub-sequência contígua de passos que roda dentro de uma transação.                                            |
| `resolução alta`             | `high resolution`       | A operação escrita como sequência de passos, com todas as fronteiras internas.                                  |
| `resolução baixa`            | `low resolution`        | A mesma operação escrita como um passo só, sem nenhuma fronteira interna.                                       |
| `escalonador`                | `scheduler`             | Decide, em cada fronteira, se o worker que chegou ali prossegue ou espera.                                      |
| `evento`                     | `event`                 | Um instante endereçável da execução sobre o qual o agendamento fala.                                            |
| `chegada`                    | `arrival`               | O instante em que o worker alcança a fronteira e devolve o controle ao runtime.                                 |
| `travessia`                  | `crossing`              | O instante em que o escalonador libera aquele worker daquela fronteira.                                         |
| `papel`                      | `role`                  | Um nome com uma cardinalidade. O agendamento cita papéis, e nunca índices de worker.                            |
| `carga`                      | `load`                  | A declaração de papéis de uma execução. A soma das cardinalidades é o número de workers.                        |
| `agendamento`                | `schedule`              | O conjunto de restrições de precedência de uma execução. O conjunto vazio não agenda nada.                      |
| `restrição de precedência`   | `precedence constraint` | A unidade do agendamento, na forma `A antes de B`, entre dois eventos.                                          |
| `encontro`                   | `meeting`               | A forma curta em que os workers de um ou mais papéis esperam uns pelos outros numa fronteira.                   |
| `término`                    | `termination`           | O instante em que um worker para de tentar uma execução de operação.                                            |
| `desistência`                | `withdrawal`            | O efeito do término sobre uma restrição cuja chegada antecedente não vai mais ocorrer.                          |
| `barreira`                   | `barrier`               | A instrução `pare nesta fronteira`. O que existe hoje é a restrição de precedência, e a parada é o efeito dela. |
| `injetor de falha`           | `fault injector`        | Decide se uma falha declarada dispara naquela fronteira. O runtime o consulta depois do escalonador.            |
| `ponto nomeado`              | `named point`           | A convenção de nomes das fronteiras, de `BEFORE_READ` a `AFTER_ACK`.                                            |
| `verdade materializada`      | `materialized truth`    | O número que responde à pergunta do experimento e ocupa uma coluna.                                             |
| `verdade derivada`           | `derived truth`         | O número que responde à pergunta do experimento e não ocupa coluna nenhuma.                                     |
| `estratégia de concorrência` | `concurrency strategy`  | A composição de passos que muda o SQL: `NONE`, `ATOMIC_UPDATE`, `OPTIMISTIC`, `PESSIMISTIC`, `JVM_LOCK`.        |
| `rótulo de estratégia`       | `strategy label`        | O dado opaco de configuração que seleciona qual estratégia roda. Nada no instrumento ramifica por ele.          |
| `chave de contenção`         | `contention key`        | O fato opaco que diz qual alvo aquela tentativa disputa.                                                        |
| `semente`                    | `seed`                  | A entrada declarada que fixa toda aleatoriedade e a identidade das entidades.                                   |
| `oráculo`                    | `oracle`                | Compara o estado final do sistema medido com o resultado que o experimento declarou esperar.                    |
| `oráculo exato`              | `exact oracle`          | O oráculo do contador: `lost_operations = commits − (final_value − initial_value)`.                             |
| `oráculo do predicado`       | `predicate oracle`      | O oráculo da capacidade, que avalia `Σ amount ≤ capacity` depois do fim da execução.                            |
| `sucessos`                   | `successes`             | O número de execuções de operação que reportaram sucesso ao instrumento.                                        |
| `perdidas`                   | `lost_operations`       | A contagem de operações perdidas que o oráculo exato produz.                                                    |
| `value_inicial`              | `initial_value`         | O valor do contador antes da execução.                                                                          |
| `value_final`                | `final_value`           | O valor do contador depois da execução.                                                                         |
| `violações`                  | `violations`            | A saída do oráculo numa execução: a contagem de perdas, ou o booleano do predicado.                             |
| `tentativa lançada`          | `launched attempt`      | Uma tentativa que o runtime iniciou. Ela termina em commit ou em aborto.                                        |
| `taxa de violação`           | `violation rate`        | `violations / commits`. O relatório exibe as contagens, e não apenas a razão.                                   |
| `taxa de aborto`             | `abort rate`            | `(N − commits) / N`. É onde aparece o custo de uma estratégia que protege descartando trabalho.                 |
| `limite superior a 95%`      | `95% upper bound`       | O número que o relatório declara quando `violations = 0`. Sai de `commits`, e nunca de `N`.                     |
| `janela de exposição`        | `exposure window`       | O intervalo, dentro de uma tentativa, em que a anomalia é possível.                                             |
| `coincidência`               | `coincidence`           | Duas tentativas cujas janelas de exposição se sobrepõem sobre a mesma chave de contenção.                       |
| `exposição oferecida`        | `offered exposure`      | As coincidências do controle negativo: o que a carga oferece quando nada interfere.                             |
| `exposição sobrevivente`     | `surviving exposure`    | As coincidências da execução medida: o que sobra depois que a estratégia agiu.                                  |
| `calibração`                 | `calibration`           | A execução que precede a medida, com uma estratégia sem perda, e que confere o instrumento.                     |
| `execução medida`            | `measured run`          | A execução cujo resultado o experimento reporta. Ela roda sem agendamento.                                      |
| `execução de controle`       | `control run`           | Uma execução que não é reportada, e que existe para interpretar uma execução medida.                            |
| `controle negativo`          | `negative control`      | A execução de controle sem estratégia, que viola por definição.                                                 |
| `controle positivo`          | `positive control`      | A execução de controle com agendamento, que prova se a anomalia é alcançável ali.                               |
| `veredito`                   | `verdict`               | O que uma execução afirma.                                                                                      |
| `classificação do zero`      | `zero classification`   | O rótulo que uma execução medida com `violations = 0` recebe.                                                   |
| `protegido`                  | `protected`             | O rótulo do zero que sustenta a comparação entre estratégias.                                                   |
| `inválido`                   | `invalid`               | O rótulo do zero cujo controle negativo não viola: a carga não quebra nada.                                     |
| `janela mal declarada`       | `misdeclared window`    | O rótulo do zero cujo controle negativo viola e conta zero coincidências.                                       |
| `exposição insuficiente`     | `insufficient exposure` | O rótulo do zero em que a anomalia é alcançável e a carga não a alcançou.                                       |
| `agendamento não cumprido`   | `unfulfilled schedule`  | O rótulo da execução de controle que não termina o próprio agendamento, por desistência.                        |
| `observação`                 | `observation`           | Um fato que o runtime emite no instante em que o evento ocorre.                                                 |
| `log de observações`         | `observation log`       | A sequência apensável de eventos de uma execução, populada pelo runtime. Não é fonte para o oráculo.            |
| `fatos brutos`               | `raw facts`             | O payload opaco que um passo devolve ao runtime, registrado sem interpretação.                                  |
| `restrito`                   | `constrained`           | O booleano de um evento de bloqueio ou liberação, verdadeiro quando havia restrição pendente ali.               |
| `instante de parede`         | `wall-clock instant`    | O metadado de exibição de um evento. Fora dos pares restritos, ele não prova precedência.                       |
| `traço de SQL`               | `SQL trace`             | Os statements que uma tentativa enviou ao banco, cada um com os valores ligados a ele.                          |
| `prova de equivalência`      | `equivalence proof`     | O teste que compara os traços de SQL das duas resoluções da mesma operação.                                     |
| `cláusula de honestidade`    | `honesty clause`        | A regra de que toda anomalia reproduzida com agendamento aparece também sem ele.                                |
| `experimento`                | `experiment`            | A unidade que declara carga, `N`, semente, janela, operação, estratégia e nível de isolamento.                  |
| `fenômeno`                   | `phenomenon`            | Um comportamento conhecido de sistemas distribuídos que o laboratório reproduz e compara.                       |
| `grupo A a E`                | `group A to E`          | A classificação dos fenômenos pela fonte de não determinismo que produz a anomalia.                             |
| `etapa`                      | `stage`                 | Uma posição do roadmap, com uma pergunta e uma dificuldade nova. Não é sinônimo de `step`.                      |
| `domínio medido`             | `measured domain`       | As entidades e as operações sobre as quais o experimento age.                                                   |
| `runtime de execução`        | `execution runtime`     | O componente que executa a sequência de passos e devolve o controle em cada fronteira.                          |
| `escalonamento`              | `scheduling`            | A atividade de decidir, fronteira a fronteira, quem prossegue e quem espera.                                    |
| `registro de observações`    | `observation record`    | Uma entrada do log de observações.                                                                              |
| `diagnóstico`                | `diagnosis`             | O que o instrumento afirma sobre a própria medida, ao lado do veredito sobre o sistema medido.                  |
| `definição de experimento`   | `experiment definition` | Os parâmetros que a pessoa declara antes de rodar. É insumo da medição, e não registro dela.                    |
| `invariante observada`       | `observed invariant`    | Uma regra que o laboratório verifica e que o sistema medido não impõe.                                          |

## Os termos que nasceram em inglês

Estes não têm par português, e por isso não aparecem na tabela acima.

| Termo        | O que é                                                                                         |
|--------------|-------------------------------------------------------------------------------------------------|
| `Lab Plane`  | O instrumento que mede: runtime, escalonador, injetor de falha, log de observações e oráculo.   |
| `worker`     | O executor de execuções de operação, com conexão própria ao banco. Não é um processo.           |
| `runtime`    | O componente que executa os passos e para em cada fronteira para consultar e observar.          |
| `Resource`   | A entidade do domínio medido que carrega `value` e `capacity`, e nenhum nome de negócio.        |
| `Allocation` | A entidade do domínio medido que carrega o `amount` alocado a um recurso. Nunca é liberada.     |
| `increment`  | A operação que lê o recurso, calcula o valor mais um, e grava.                                  |
| `allocate`   | A operação que lê a soma das alocações, compara com a capacidade, e insere quando couber.       |
| `commits`    | O número de passagens pela fronteira `AFTER_COMMIT`. Não é o número de operações bem-sucedidas. |
| `timeline`   | A projeção direta do log de observações.                                                        |
| `N`          | O número de tentativas lançadas que a execução medida declara antes de começar.                 |
