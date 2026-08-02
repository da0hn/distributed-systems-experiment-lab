# language: pt
#
# Especificação viva. Nenhum destes cenários tem teste — não existe código no
# repositório. A tag @teste-ausente marca o cenário cujo teste precisa ser escrito;
# quando ele existir, a tag é trocada pelo identificador do teste.
#
# Fonte das regras: docs/adr/0001-o-passo-como-unidade-de-execucao.md, Aceito.
# Regras em debate não aparecem aqui — elas vivem em example-mapping.md.

Funcionalidade: Observação passo a passo de uma operação
  Para que a intercalação e a falha sejam endereçáveis por nome
  Como quem monta um experimento
  Quero que o runtime pare, falhe e observe entre dois passos consecutivos

  Contexto:
    Dado que a operação "increment" declara os passos "select-resource",
      "increment" e "update-resource", nesta ordem

  @teste-ausente @recusa
  Cenário: um endereço de fronteira que não resolve é recusado antes de executar
    Dado um experimento que endereça a fronteira de saída de "select-resurce"
    Quando o experimento é submetido
    Então a plataforma recusa o experimento sem executar passo nenhum
    E a recusa nomeia o endereço culpado

  @teste-ausente @recusa @borda
  Cenário: o nome abreviado é recusado quando o tipo aparece mais de uma vez
    Dado que a operação "increment" declara um segundo passo de tipo READ
    E um experimento que endereça "AFTER_READ"
    Quando o experimento é submetido
    Então a plataforma recusa o experimento
    E a recusa informa que o tipo READ aparece em mais de um passo

  @teste-ausente @recusa
  Cenário: o seletor de tentativa não tem valor padrão
    Dado uma operação que pode tentar mais de uma vez
    E um experimento que endereça "AFTER_READ" sem seletor de tentativa
    Quando o experimento é submetido
    Então a plataforma recusa o experimento

  @teste-ausente @ordem
  Cenário: o escalonador é consultado antes do injetor de falha
    Dado uma barreira declarada na fronteira de saída de "select-resource"
    E uma falha declarada na mesma fronteira
    Quando um worker alcança essa fronteira
    Então o worker é bloqueado antes de a falha ser lançada
    E o log de observações registra o bloqueio, a liberação e a falha, nesta ordem

  @teste-ausente @concorrencia
  Cenário: o escopo de execução rejeita acesso vindo de outro worker
    Dado que o worker 1 iniciou a tentativa 1 de "increment"
    Quando o worker 2 tenta ler o escopo de execução do worker 1
    Então o runtime rejeita o acesso
    E a rejeição nomeia o passo em que o acesso ocorreu

  @teste-ausente @guarda-estatica
  Cenário: uma definição de operação com estado mutável é rejeitada
    Dado uma definição de operação que declara um campo não final
    Quando a análise estática executa
    Então a definição é rejeitada
    E a rejeição nomeia o campo

  @teste-ausente @equivalencia
  Cenário: as duas resoluções da mesma operação emitem o mesmo traço de SQL
    Dado a operação "increment" em alta resolução
    E a mesma operação em baixa resolução, como método transacional
    Quando as duas executam sem concorrência sobre o mesmo estado inicial
    Então os dois traços têm o mesmo comprimento
    E em cada posição o texto normalizado e os valores ligados coincidem

  @teste-ausente @equivalencia @falha
  Cenário: a divergência entre traços falha nomeando a operação e a posição
    Dado a operação "increment" cujos dois braços divergem na posição 2
    Quando a prova de equivalência executa
    Então a prova falha
    E a falha nomeia a operação "increment" e a posição 2

  @teste-ausente @equivalencia @borda
  Cenário: dois traços com os mesmos statements em ordem diferente são diferentes
    Dado dois traços com os mesmos statements e os mesmos valores ligados
    Mas em ordem diferente
    Quando a prova de equivalência os compara
    Então a prova falha

  @teste-ausente @equivalencia @cobertura
  Esquema do Cenário: a prova de "allocate" cobre os três ramos do predicado
    Dado um recurso com capacidade 10 e alocações somando <soma_inicial>
    Quando "allocate" é provada com o argumento <amount>
    Então o ramo exercitado é "<ramo>"

    Exemplos:
      | soma_inicial | amount | ramo                    |
      | 0            | 6      | a alocação cabe         |
      | 4            | 6      | atinge a capacidade     |
      | 6            | 6      | a alocação excede       |
