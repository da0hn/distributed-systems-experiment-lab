# language: pt
#
# ARQUIVO INATIVO — este arquivo NÃO é especificação viva.
#
# Nenhuma regra que estes cenários cobrem tem `Aprovada por` preenchido, e uma regra
# pendente não sustenta Gherkin. Enquanto isso valer, nada aqui DEVE virar teste ou
# código. Os cenários ficam na árvore, e voltam ao conjunto ativo regra a regra,
# quando uma pessoa aprovar a regra que cada um sustenta.
# O estado das regras é do índice de capacidades: docs/features/README.md#índice.
#
# Fonte das regras: docs/adr/0002-o-dominio-minimo-e-os-dois-oraculos.md, Aceito,
# e docs/plano-do-laboratorio.md, seção 6, E5.

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
    Então nenhum SELECT é emitido contra o schema do system under test
    E nenhuma entrada do log de observações é usada para derivá-la

  @teste-ausente @protecao-inerte
  Cenário: a estratégia otimista não protege a invariante derivada
    Dado a estratégia OPTIMISTIC ativa
    E dois workers que leem a soma das alocações antes de qualquer inserção
    Quando cada um insere uma alocação de 6
    Então a soma das alocações é 12
    E nenhuma exceção de conflito de versão é lançada

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

  @teste-ausente @ortogonalidade
  Cenário: o eixo do isolamento é independente do eixo da estratégia
    Dado a estratégia OPTIMISTIC sob o nível "READ COMMITTED"
    E a estratégia NONE sob o nível "SERIALIZABLE"
    Quando os dois braços executam a mesma carga
    Então o primeiro braço viola a invariante
    E o segundo braço não viola a invariante
