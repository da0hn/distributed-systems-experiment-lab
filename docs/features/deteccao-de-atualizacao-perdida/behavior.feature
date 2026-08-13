# language: pt
#
# Este arquivo cobre somente regra aprovada por pessoa, na forma em que ela foi
# aprovada. Nenhum cenário aqui sustenta regra `pendente` — regra pendente NÃO DEVE
# virar cenário Gherkin. O estado de cada regra é do índice de capacidades, e não é
# repetido aqui: docs/features/README.md#índice.
#
# Fonte das regras: feature-card.md, tabela "Regras de negócio" — dona da coluna
# `Evidência` de cada regra.

Funcionalidade: Detecção da atualização perdida
  Para que "às vezes perde" seja substituído por uma contagem
  Como quem estuda concorrência
  Quero saber quantos incrementos se perderam e sob qual proteção

  Contexto:
    Dado um recurso com value igual a 0
    E que cada worker tem sua própria conexão

  @teste-ausente @oraculo
  Cenário: o oráculo conta os incrementos perdidos
    Dado uma execução com 10 workers e 100 incrementos sem proteção
    Quando ela termina com 100 commits e o recurso com value igual a 63
    Então o oráculo reporta 37 incrementos perdidos

  @teste-ausente @oraculo @borda
  Cenário: uma tentativa que commitou e reportou falha entra no denominador
    Dado uma tentativa que alcançou a fronteira AFTER_COMMIT
    E uma falha injetada nessa fronteira
    Quando a operação reporta erro ao Lab Plane
    Então a tentativa é contada em commits
    E a tentativa não é contada em sucessos

  @teste-ausente @oraculo @borda
  Cenário: uma tentativa que esgotou as tentativas não entra no denominador
    Dado uma operação que esgotou as tentativas sem alcançar AFTER_COMMIT
    Quando o oráculo calcula o denominador
    Então a operação não é contada em commits

  @teste-ausente @oraculo @repeticao
  Cenário: uma operação que commita duas vezes é contada duas vezes
    Dado uma operação que commitou, falhou depois do commit e tentou de novo
    E que as duas tentativas alcançaram AFTER_COMMIT
    Quando o oráculo calcula o denominador
    Então a operação contribui com 2 commits

  @teste-ausente @dual-write
  Cenário: a diferença entre commits e sucessos mede o dual write
    Dado uma execução que termina com 100 commits e 94 sucessos
    Quando o relatório é montado
    Então o relatório exibe 6 como medida de dual write
    E esse número não é reportado como incremento perdido

  @teste-ausente @oraculo @isolamento-de-planos
  Cenário: o oráculo lê o WAL do sistema medido e não o log de observações
    Dado uma execução terminada
    Quando o oráculo determina o valor final do recurso
    Então o valor final vem do último value do recurso visto no stream de replicação
    E a comparação só ocorre depois de o stream alcançar o LSN do commit final
    E o valor inicial vem do INSERT que criou o estado inicial no mesmo stream
    E nenhuma entrada do log de observações é usada para derivá-lo
    E nenhum SELECT é emitido contra o schema do system under test

  @teste-ausente @grupo-de-controle
  Cenário: o grupo de controle precisa falhar
    Dado uma execução com 10 workers e 100 incrementos sem proteção
    Quando ela termina com o recurso em value igual a 100
    Então a plataforma declara a carga insuficiente
    E nenhum resultado comparativo sobre a mesma carga é reportado

  @teste-ausente @semente
  Cenário: duas execuções da mesma semente produzem os mesmos identificadores
    Dado uma execução com a semente 42
    E outra execução com a semente 42
    Quando as duas geram o identificador do recurso
    Então os dois identificadores coincidem

  @teste-ausente @conexao @borda
  Esquema do Cenário: um pool que não é maior que o número de workers invalida a execução
    Dado uma execução declarando 10 workers
    E um pool de conexões com capacidade <capacidade>
    Quando a execução é submetida
    Então a plataforma recusa a execução
    E a recusa informa que o pool serializaria os workers

    Exemplos:
      | capacidade |
      | 10         |
      | 5          |

  @teste-ausente @comparacao
  Esquema do Cenário: a mesma carga sob três estratégias
    Dado a carga de 10 workers e 100 incrementos
    Quando ela executa sob a estratégia "<estrategia>"
    Então o valor final do recurso é <resultado>

    Exemplos:
      | estrategia    | resultado    |
      | NONE          | menor que 100|
      | ATOMIC_UPDATE | 100          |
      | PESSIMISTIC   | 100          |
