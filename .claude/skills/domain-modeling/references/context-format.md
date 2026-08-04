# Formato de docs/CONTEXT.md

## Estrutura

```md
# {Nome do contexto}

{Uma ou duas frases descrevendo o que este contexto é e por que existe.}

## Linguagem

**Passo**:
{Uma ou duas frases descrevendo o termo}
_Evite_: etapa, estágio, fase

**Tentativa**:
Uma passagem completa pela sequência de passos de uma operação.
_Evite_: execução, rodada

**Operação**:
A definição versionada de uma sequência de passos, distinta de cada execução dela.
_Evite_: fluxo, workflow
```

## Regras

- **Seja opinativo.** Quando várias palavras existirem para o mesmo conceito, escolha a
  melhor e liste as outras em `_Evite_`.
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
- Se nenhum dos dois existir, crie `docs/CONTEXT.md` de forma preguiçosa quando o
  primeiro termo for resolvido.

Este repositório está, hoje, no terceiro caso: nem `docs/CONTEXT.md` nem
`docs/CONTEXT-MAP.md` existem ainda. O primeiro termo resolvido cria o arquivo.
