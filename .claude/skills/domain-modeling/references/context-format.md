# Formato de docs/CONTEXT.md

## O idioma

**O nome do termo é em inglês; a explicação, em português.** Regra adotada em 2026-08-04
junto da decisão `D-ARQ-06`: todo identificador de código deste laboratório é escrito em
inglês, e o glossário nomeia o que vira código.

A linha `_Evite_` lista as palavras **inglesas** recusadas para o mesmo conceito. Quando
o termo já existir em português no corpus, o par entra na tabela de de/para — e **só
lá**, para que os dois lugares não possam divergir.

Os rótulos de estado — `estabelecido`, `proposto`, `aposentado` — continuam em
português. Eles descrevem o processo do repositório e nunca viram identificador.

## Uma entrada tem quatro partes, e só quatro

Termo, definição breve, status ou sinônimos recusados, e link de origem. O link aponta
para onde o termo foi decidido — o ADR, a linha da fila ou o Feature Card —, e é ele que
mantém o glossário fora do negócio de guardar argumento.

```md
# {Nome do contexto}

{Uma ou duas frases descrevendo o que este contexto é e por que existe.}

## De/para — português para inglês

| Português   | Inglês    |
|-------------|-----------|
| `passo`     | `step`    |
| `tentativa` | `attempt` |

## Linguagem

**step** — `estabelecido`
{Uma ou duas frases descrevendo o termo}
_Evite_: stage, phase, action
_Origem_: [ADR-0001](adr/0001-o-passo-como-unidade-de-execucao.md#decisão)

**attempt** — `estabelecido`
Uma passagem completa pela sequência de passos de uma operação.
_Evite_: round, iteration, retry
_Origem_: [ADR-0001](adr/0001-o-passo-como-unidade-de-execucao.md#decisão)
```

## O que NÃO DEVE entrar

Cada um destes já tem dono, e escrevê-lo aqui cria um segundo repositório de decisões:

| O que aparece na conversa                        | Onde ele vive                                   |
|--------------------------------------------------|-------------------------------------------------|
| alternativa de nome, com o argumento de cada uma | linha da `../../../../docs/fila-de-decisoes.md`         |
| decisão de vocabulário, proposta ou tomada       | a mesma linha da fila; ADR quando ela o merecer |
| ata de como o termo foi debatido                 | a linha da fila, e nunca o glossário            |
| pergunta em aberto e backlog de termos           | `docs/questions/`, ou o `example-mapping.md`    |

Um termo em disputa **não ganha entrada**. Ele ganha linha na fila, e entra aqui quando
a pessoa escolher. Uma entrada com `proposto` no status descreve um termo que já foi
escrito no corpus e ainda não foi ratificado — ela não é o lugar de propor um nome novo.

## Regras

- **Seja opinativo.** Quando várias palavras existirem para o mesmo conceito, escolha a
  melhor e liste as outras em `_Evite_`.
- **Verifique se a palavra inglesa já está numa linha `_Evite_`.** Um termo português
  costuma recusar justamente o anglicismo que a conversão promove a nome. Ao converter,
  a linha se inverte — e quando a recusa deve permanecer, isso é escolha, não tradução:
  registre-a como pergunta em aberto.
- **Mantenha definições enxutas.** Uma ou duas frases no máximo. Defina o que o termo
  **é**, não o que ele faz.
- **Inclua só termos específicos do contexto deste projeto.** Conceito geral de
  programação (timeout, tipo de erro, padrão utilitário) não entra, mesmo que o projeto
  use bastante. Antes de acrescentar um termo, pergunte: isto é um conceito único deste
  contexto, ou um conceito geral de programação? Só o primeiro pertence aqui.
- **Agrupe termos sob subtítulos** quando surgirem agrupamentos naturais. Se todos os
  termos pertencem a uma área coesa só, uma lista simples basta.

## Contexto único contra múltiplos contextos

**Contexto único (este repositório, hoje):** um `docs/CONTEXT.md` na raiz de `docs/`.

**Múltiplos contextos, se algum dia existirem:** um `docs/CONTEXT-MAP.md` na raiz de
`docs/` lista os contextos, onde cada um vive e como eles se relacionam:

```md
# Mapa de contextos

## Contextos

- [Laboratório](./CONTEXT.md) — o vocabulário do experimento e do runtime

## Relações

- (nenhuma — contexto único)
```

A skill infere qual estrutura se aplica:

- Se `docs/CONTEXT-MAP.md` existir, leia-o para encontrar os contextos.
- Se só existir `docs/CONTEXT.md` na raiz, é contexto único.

**Este repositório está no segundo caso.** `docs/CONTEXT.md` existe e
`docs/CONTEXT-MAP.md` não. Nenhum dos dois é criado por esta skill: o glossário já está
lá, e o mapa só nasce quando houver um segundo contexto para mapear.
