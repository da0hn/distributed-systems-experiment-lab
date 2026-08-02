# language: pt

@teste-ausente
Funcionalidade: [Nome da capacidade]
  Como [ator]
  Quero [objetivo]
  Para [resultado]

  Contexto:
    Dado [pré-condição observável]

  Cenário: [Fluxo principal]
    Quando [ação]
    Então [resultado observável]

  Cenário: [Falha relevante]
    Dado [pré-condição de falha]
    Quando [ação]
    Então [erro ou recusa observável]

  Cenário: [Caso de borda]
    Dado [limite que muda o resultado]
    Quando [ação]
    Então [resultado observável]
