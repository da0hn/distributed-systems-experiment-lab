---
name: domain-modeling
description: Constrói e afia o modelo de domínio de um projeto. Use quando o usuário quiser fixar terminologia de domínio ou uma linguagem ubíqua, registrar uma decisão arquitetural, ou quando outra skill precisar manter o modelo de domínio.
---

# Modelagem de domínio

Construa e afie ativamente o modelo de domínio do projeto enquanto o desenho acontece.
Esta é a disciplina *ativa* — desafiar termos, inventar cenários de fronteira, e escrever
o glossário e as decisões no instante em que se cristalizam. (Apenas *ler* `docs/CONTEXT.md`
em busca de vocabulário não é esta skill — isso é um hábito de uma linha que qualquer
skill pode ter. Esta skill é para quando você está mudando o modelo, não só consumindo
ele.)

## Estrutura de arquivos

Este repositório tem um único contexto hoje — um laboratório de fenômenos de sistemas
distribuídos, não múltiplos domínios de negócio:

```
docs/
├── CONTEXT.md
├── specification-process.md
├── adr/
│   ├── 0001-titulo-em-kebab-case.md
│   └── 0002-titulo-em-kebab-case.md
└── features/
```

Se um `docs/CONTEXT-MAP.md` passar a existir, o repositório terá múltiplos contextos. O
mapa aponta para onde cada um vive — veja o formato em
[references/context-format.md](references/context-format.md). Nada neste repositório
justifica isso hoje: um único laboratório, um único glossário.

**`docs/CONTEXT.md` já existe.** Não o crie, não o recrie e não trate a ausência dele
como estado possível. O trabalho é acrescentar e afiar entrada, nunca inaugurar o
arquivo.

## O que entra no glossário, e o que não entra

Uma entrada tem quatro partes, e só essas quatro: **termo**, **definição breve**,
**status ou sinônimos recusados**, e **link de origem**. O formato exato está em
[references/context-format.md](references/context-format.md).

**Quatro coisas NÃO DEVEM entrar**, porque cada uma já tem dono:

| O que aparece na conversa                        | Onde ele vive                                   |
|--------------------------------------------------|-------------------------------------------------|
| alternativa de nome, com o argumento de cada uma | linha da `../../../docs/fila-de-decisoes.md`         |
| decisão de vocabulário, proposta ou tomada       | a mesma linha da fila; ADR quando ela o merecer |
| ata de como o termo foi debatido                 | a linha da fila, e nunca o glossário            |
| pergunta em aberto e backlog de termos           | `docs/questions/`, ou o `example-mapping.md`    |

O glossário registra o vocabulário **vigente**. Um termo em disputa não ganha entrada:
ele ganha linha na fila, e entra aqui quando a pessoa escolher. Escrever a disputa aqui
cria um segundo repositório de decisões, e os dois divergem no primeiro turno.

## Durante a sessão

### Desafie contra o glossário

Quando o usuário usar um termo que conflite com a linguagem já registrada em
`docs/CONTEXT.md`, aponte isso na hora. "Seu glossário define 'tentativa' como X, mas
você parece estar dizendo Y — qual dos dois é?"

### Afie linguagem imprecisa

Quando o usuário usar um termo vago ou sobrecarregado, proponha um termo canônico
preciso. "Você diz 'operação' — quer dizer a definição da operação ou uma execução dela?
São coisas diferentes."

### Discuta cenários concretos

Quando relações de domínio estiverem em discussão, teste-as sob estresse com cenários
específicos. Invente cenários que sondem casos de fronteira e forcem precisão sobre os
limites entre conceitos.

### Cruze com o código

Quando o usuário afirmar como algo funciona, verifique se o código concorda. Se encontrar
uma contradição, mostre-a: "O código conta `perdidas` a partir de `commits`, mas você
acabou de dizer que a contagem vem de `sucessos` — qual dos dois está certo?"

### Atualize docs/CONTEXT.md na hora

Quando um termo for resolvido, atualize `docs/CONTEXT.md` ali mesmo. Não acumule para
depois — capture no instante em que acontece. Use o formato em
[references/context-format.md](references/context-format.md).

`docs/CONTEXT.md` fica totalmente livre de detalhe de implementação. Não o trate como
especificação, rascunho, ata ou repositório de decisão. É um glossário, e nada mais —
a tabela de "O que entra no glossário" diz para onde vai o resto.

### Ofereça ADR com parcimônia

Quando uma decisão de domínio for difícil de reverter, surpreendente sem contexto e
resultado de um trade-off real, ela deixa de ser vocabulário e vira decisão
arquitetural — os quatro critérios de `docs/adr/README.md`. Não escreva o ADR você
mesmo: acione a skill adr, que contém o template e o ciclo de vida.

Nunca traga um template de ADR próprio para esta skill. O repositório tem um único
processo de ADR, e ele vive na skill adr.
