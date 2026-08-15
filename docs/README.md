# Documentação

**Este arquivo é o índice de `docs/`, e só isso.** Ele diz o que cada pasta guarda, para
que quem procura um documento saiba onde olhar. Ele não carrega regra, estado, inventário
nem contagem — cada uma dessas coisas tem dono próprio, e uma segunda cópia envelhece em
silêncio.

Para saber o que o sistema **faz**, leia o código. A árvore versionada, os testes e a
configuração são a fonte da verdade.

## A estrutura

```
docs/
  README.md               este índice
  roadmap.md              o plano geral, em alto nível
  data-dictionary.md      o de/para do vocabulário do laboratório
  backlog.md              o que está sendo feito; instável
  architecture/           a arquitetura, os serviços e as restrições
    constraints/          uma restrição arquitetural por arquivo
    schemas/              a forma dos schemas, e as propostas de modelo
  adr/                    as decisões arquiteturais; congelado
  features/               o comportamento de cada funcionalidade
  contracts/              o contrato formal entre processos
  diagrams/               o que o Mermaid não expressa
```

## O que cada caminho guarda

| Caminho                                    | O que vive ali                                         |
|--------------------------------------------|--------------------------------------------------------|
| [`roadmap.md`](roadmap.md)                 | o plano geral do laboratório, em alto nível            |
| [`data-dictionary.md`](data-dictionary.md) | o de/para do vocabulário, português e inglês           |
| `backlog.md`                               | o que está sendo feito; instável, e nunca referenciado |
| [`architecture/`](architecture/README.md)  | os serviços, a topologia e as restrições arquiteturais |
| [`adr/`](adr/README.md)                    | as decisões arquiteturais já tomadas; congelado        |
| [`features/`](features/README.md)          | o comportamento pretendido de cada funcionalidade      |
| [`contracts/`](contracts/README.md)        | o contrato formal entre processos, quando existir      |
| [`diagrams/`](diagrams/)                   | o que o Mermaid não expressa, em `.excalidraw.svg`     |

## Três coisas que valem antes de abrir qualquer arquivo

**`adr/` está congelado.** Ele registra o que já foi decidido. Nenhum ADR novo nasce ali,
e nenhum ADR existente é editado. Decisão arquitetural nova acontece na conversa, e vai
para o código.

**`backlog.md` NÃO DEVE ser referenciado.** Ele é a memória de trabalho entre sessões: uma
linha dele nasce e some conforme o trabalho anda, então um link para ele aponta para texto
que não estará lá. É o único arquivo desta pasta que aparece acima sem link, e isso é
deliberado.

**Um documento daqui não é contrato.** Onde ele contradisser a árvore, a árvore está
certa — e a contradição é defeito a corrigir, e não estado aceito. O que obriga a
atualizar cada caminho desta pasta está em [`AGENTS.md`](AGENTS.md), ao lado deste
índice.

As regras de trabalho do repositório estão no [`AGENTS.md`](../AGENTS.md) da raiz.
