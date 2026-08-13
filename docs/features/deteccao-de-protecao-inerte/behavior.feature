# language: pt
#
# Este arquivo cobre somente regra aprovada por pessoa, na forma em que ela foi
# aprovada. Nenhum cenário aqui sustenta regra `pendente` — regra pendente NÃO DEVE
# virar cenário Gherkin. O estado de cada regra é do índice de capacidades, e não é
# repetido aqui: docs/features/README.md#índice.
#
# Fonte das regras: feature-card.md, tabela "Regras de negócio" — dona da coluna
# `Evidência` de cada regra.

Funcionalidade: Detecção de proteção presente e inerte
  Para que "ter uma estratégia" deixe de ser confundido com "estar protegido"
  Como quem ativou uma estratégia de concorrência
  Quero ver a invariante quebrar sem que exceção nenhuma seja lançada

  Contexto:
    Dado um recurso com capacity igual a 10 e nenhuma alocação
    E que a verdade é a soma das alocações, não uma coluna do recurso

  @teste-ausente @predicado
  Esquema do Cenário: o predicado de capacidade decide se a alocação cabe
    Dado alocações somando <soma>
    Quando um worker executa allocate com amount igual a <amount>
    Então a alocação é <resultado>

    Exemplos:
      | soma | amount | resultado |
      | 0    | 6      | inserida  |
      | 6    | 4      | inserida  |
      | 6    | 6      | recusada  |

  @teste-ausente @anomalia
  Cenário: duas alocações válidas violam a invariante sem exceção
    Dado dois workers que leem a soma das alocações antes de qualquer inserção
    E que os dois leem 0
    Quando cada um insere uma alocação de 6
    Então a soma das alocações é 12
    E nenhuma exceção é lançada
    E nenhuma linha foi sobrescrita

  @teste-ausente @oraculo
  Cenário: a violação reportada carrega os dois números
    Dado uma execução que terminou com soma 12 sobre capacity 10
    Quando o oráculo avalia o predicado
    Então o veredito é violação
    E a violação informa a soma 12 e a capacidade 10

  @teste-ausente @oraculo @isolamento-de-planos
  Cenário: o oráculo não alcança o schema do sistema medido
    Dado uma execução terminada
    Quando o oráculo determina a soma das alocações
    Então a soma vem dos eventos de INSERT no WAL do sistema medido
    E nenhum SELECT é emitido contra o schema do system under test
    E nenhuma entrada do log de observações é usada para derivá-la

  @teste-ausente @isolamento
  Esquema do Cenário: o mesmo experimento sob três níveis de isolamento
    Dado o nível de isolamento "<nivel>"
    Quando dois workers alocam 6 cada um sobre capacity 10
    Então a soma final das alocações é <soma_final>
    E o número de transações abortadas com SQLSTATE 40001 é <abortos>

    Exemplos:
      | nivel           | soma_final | abortos |
      | READ COMMITTED  | 12         | 0       |
      | REPEATABLE READ | 12         | 0       |
      | SERIALIZABLE    | 6          | 1       |
