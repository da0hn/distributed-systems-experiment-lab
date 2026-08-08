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
# Fonte das regras: docs/adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md
# e docs/adr/0002-o-dominio-minimo-e-os-dois-oraculos.md, os dois Aceito.
# O ADR-0003 está Aceito, e não gerou cenário aqui — ver example-mapping.md.

Funcionalidade: Execução de um experimento e classificação do veredito
  Para que um resultado zero signifique proteção e não defeito do instrumento
  Como quem lê o relatório de um experimento
  Quero que a plataforma classifique o zero e recuse reportar o que não mediu

  Contexto:
    Dado que a execução medida roda sem agendamento
    E que o experimento declara a janela de exposição que vai da saída de
      "select-resource" à entrada de "update-resource"

  @teste-ausente @calibracao
  Cenário: a calibração aprova o denominador quando os dois números coincidem
    Dado uma execução de calibração com uma estratégia que não perde incremento
    Quando ela termina com 100 commits e o valor do recurso sobe de 0 para 100
    Então a plataforma libera a execução medida

  @teste-ausente @calibracao @falha
  Cenário: a calibração recusa o relatório quando os dois números divergem
    Dado uma execução de calibração com uma estratégia que não perde incremento
    Quando ela termina com 100 commits e o valor do recurso sobe de 0 para 97
    Então a plataforma recusa o relatório
    E nenhum resultado daquela execução é reportado

  @teste-ausente @parada
  Cenário: a execução não para na primeira violação
    Dado uma execução medida com N igual a 1000
    Quando a primeira violação aparece na tentativa 12
    Então a execução prossegue até a tentativa 1000

  @teste-ausente @relatorio
  Cenário: o relatório traz as três contagens e as duas taxas
    Dado uma execução medida com N igual a 1000
    Quando ela termina com 980 commits e 37 violações
    Então o relatório exibe tentativas lançadas, commits e violações
    E o relatório exibe a taxa de violação de 37 sobre 980
    E o relatório exibe a taxa de aborto de 20 sobre 1000

  @teste-ausente @relatorio @borda
  Cenário: com zero violações o relatório declara o limite superior sobre os commits
    Dado uma execução medida com N igual a 1000
    Quando ela termina com 900 commits e nenhuma violação
    Então o relatório declara o limite superior da taxa a 95% de confiança
    E o limite é calculado sobre 900 commits, não sobre 1000 tentativas

  @teste-ausente @coincidencia @borda
  Cenário: janelas sobrepostas com chaves de contenção diferentes não formam coincidência
    Dado duas tentativas cujas janelas de exposição se sobrepõem no tempo
    Mas que reportam chaves de contenção diferentes
    Quando o runtime conta as coincidências
    Então o par não é contado

  @teste-ausente @coincidencia @recusa
  Cenário: cargas declaradas diferentes não são comparáveis
    Dado um controle negativo com N igual a 1000
    E uma execução medida com N igual a 100
    Quando a plataforma tenta comparar as duas contagens de coincidência
    Então a plataforma recusa a comparação

  @teste-ausente @classificacao
  Esquema do Cenário: o zero é classificado pela primeira condição que casar
    Dado uma execução medida que terminou com zero violações
    E um controle negativo que <controle_negativo>
    E coincidências do controle negativo iguais a <coincidencias_cn>
    E coincidências da execução medida iguais a <coincidencias_em>
    E um controle positivo que <controle_positivo>
    Quando a plataforma classifica o resultado
    Então o veredito é "<veredito>"

    Exemplos:
      | controle_negativo | coincidencias_cn | coincidencias_em | controle_positivo | veredito                 |
      | não viola         | 0                | 0                | não executa       | inválido                 |
      | viola             | 0                | 4                | não executa       | janela mal declarada     |
      | viola             | 12               | 0                | não executa       | protegido                |
      | viola             | 12               | 5                | viola             | exposição insuficiente   |
      | viola             | 12               | 5                | não viola         | protegido                |

  @teste-ausente @classificacao @ordem
  Cenário: a ordem da tabela vence quando duas condições casam ao mesmo tempo
    Dado uma execução medida que terminou com zero violações
    E um controle negativo que não viola
    E coincidências da execução medida iguais a zero
    Quando a plataforma classifica o resultado
    Então o veredito é "inválido"
    E o veredito não é "protegido"

  @teste-ausente @classificacao @recusa
  Esquema do Cenário: um veredito que não é proteção não sustenta comparação
    Dado um relatório com veredito "<veredito>"
    Quando ele é usado como evidência de proteção
    Então a plataforma recusa

    Exemplos:
      | veredito               |
      | inválido               |
      | janela mal declarada   |
      | exposição insuficiente |

  @teste-ausente @controle-positivo
  Cenário: o controle positivo responde sobre o resultado e não entra na contagem
    Dado uma execução medida com zero violações e coincidências próprias maiores que zero
    Quando o controle positivo executa e produz uma violação
    Então o relatório do experimento continua exibindo zero violações
    E o veredito é "exposição insuficiente"

  @teste-ausente @controle-positivo
  Cenário: o controle positivo é dispensado quando a estratégia fechou a janela
    Dado uma execução medida com zero violações e zero coincidências próprias
    Quando a plataforma classifica o resultado
    Então o controle positivo não é executado
    E o veredito é "protegido"

  @teste-ausente @resolucao @recusa
  Cenário: um experimento que pode reportar zero é recusado em baixa resolução
    Dado uma operação declarada como sequência de um passo, sem fronteiras internas
    Quando um experimento cujo veredito pode ser zero a submete
    Então a plataforma recusa o experimento
    E a recusa informa que a janela de exposição não tem onde ser ancorada
