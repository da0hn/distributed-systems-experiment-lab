# AGENTS.md — trabalhando dentro de `docs/`

Este arquivo faz duas coisas: diz **o que cada caminho de `docs/` guarda**, para que a
busca comece no lugar certo, e diz **que forma cada documento tem** — o teto de um Feature
Card, os blocos de um Example Mapping, o que entra num arquivo de restrição.

**Ele não diz quando escrever.** Isso é da tabela de gatilhos do
[`AGENTS.md` da raiz](../AGENTS.md), que prevalece sobre tudo o que está aqui e não é
reproduzido aqui — regra que vale no repositório inteiro mora lá, e uma segunda cópia
envelhece em silêncio.

O [`README.md`](README.md) desta pasta é o índice de navegação, para quem **procura** um
documento. Este arquivo é para quem vai **escrever** um.

## O que cada caminho guarda, e onde aprofundar

Quando o destino for pasta, o `README.md` dela é a autoridade — abra-o antes de escrever
qualquer coisa dentro dela. A tabela abaixo é ponto de partida de busca, e não descrição
de conteúdo.

| Caminho                     | O que guarda                                                                            | Onde aprofundar                                                    |
|-----------------------------|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| `README.md`                 | o índice de navegação da pasta; ele não carrega regra, estado nem inventário            | o próprio arquivo                                                  |
| `roadmap.md`                | o plano geral em alto nível: a abstração, os cinco grupos de fenômenos e as doze etapas | o próprio arquivo                                                  |
| `data-dictionary.md`        | o de/para do vocabulário do laboratório: termo em inglês, explicação em português       | o próprio arquivo                                                  |
| `backlog.md`                | o que está sendo feito, para a próxima sessão continuar; instável                       | o próprio arquivo                                                  |
| `architecture/`             | os processos que o repositório sobe, o papel de cada um, os schemas e as restrições     | [`architecture/README.md`](architecture/README.md)                 |
| `architecture/constraints/` | uma restrição arquitetural por arquivo, dizendo o que ela proíbe e o que ela protege    | os arquivos da pasta                                               |
| `architecture/schemas/`     | a forma do schema de cada serviço, e as propostas de modelo de dados                    | [`architecture/schemas/README.md`](architecture/schemas/README.md) |
| `adr/`                      | as decisões arquiteturais já tomadas, congeladas no tempo                               | [`adr/README.md`](adr/README.md)                                   |
| `features/`                 | uma funcionalidade do sistema por diretório, e o que cada uma faz                       | [`features/README.md`](features/README.md)                         |
| `contracts/`                | o contrato formal entre processos, quando existir                                       | [`contracts/README.md`](contracts/README.md)                       |
| `diagrams/`                 | o que o Mermaid não expressa, exportado em `.excalidraw.svg`; hoje está vazia           | —                                                                  |

**`backlog.md` aparece acima sem link, e isso é deliberado** — a raiz proíbe referenciá-lo,
e a proibição alcança esta tabela.

**Se o que você quer escrever não couber em nenhuma linha, ele não vira documento.**
Nenhum caminho novo é inventado nesta pasta — o assunto vai para a conversa, e a pendência
para o `backlog.md`. Uma funcionalidade se divide em três arquivos, e qual deles recebe o
quê está em [Feature Card](#feature-card), [Example Mapping](#example-mapping) e
[BDD](#bdd).

## O que nunca é editado

`adr/`. Nenhum arquivo dela é criado, editado, emendado, dividido, patcheado ou
substituído — nem por um gatilho da raiz, nem por iniciativa própria.

Quando um ADR contradisser a árvore, a divergência **não** se conserta ali: ela se
conserta no destino que a tabela de gatilhos da raiz indicar.

## Quando escrever aqui

**Quem decide isso é o `AGENTS.md` da raiz**, na tabela de
[gatilhos](../AGENTS.md#a-documentação-que-restou-acompanha-o-código): ela diz qual
mudança de código obriga a atualizar qual caminho desta pasta, e que a atualização vai no
mesmo commit da mudança que a disparou. Ela não é reproduzida aqui — o gatilho nasce no
código, e quem mexe em código lê aquele arquivo, não este.

Este arquivo responde a outra pergunta: **uma vez que o gatilho disparou, que forma o
destino tem.**

## Que forma cada destino tem

Uma funcionalidade do sistema ocupa um diretório em `features/`, nomeado em kebab-case, com três
arquivos: `feature-card.md`, `example-mapping.md` e `behavior.feature`.

### Feature Card

Caminho: `features/<slug>/feature-card.md`.

- **Um card cobre uma funcionalidade**, nunca um endpoint, uma classe ou uma tarefa técnica.
  É o oráculo que delimita a funcionalidade, e por isso E1 e E3 partilham um card.
- Seções, nesta ordem: problema e resultado esperado; atores e gatilho; escopo; fora de
  escopo; regras de negócio; integrações e contratos afetados; riscos e decisões
  pendentes; critérios de pronto; links.
- **Máximo 5.500 caracteres de prosa.** Diagrama, bloco de código e tabela não entram na
  contagem. **Quem conta é o script, e nenhuma medição montada à mão vale** — nem `wc`, nem
  contagem de palavras, nem tamanho bruto do arquivo:

  ```bash
  python .claude/skills/feature-planning/scripts/check_artifact_limits.py \
    --root . --file docs/features/<slug>/feature-card.md
  ```

- **Toda regra leva evidência com caminho e âncora GFM**, numa coluna própria; número de
  linha só quando o alvo não tiver título que o alcance, dentro de um bloco Mermaid por
  exemplo. A coluna ao lado diz quem aprovou a regra.
- Ao criar uma funcionalidade, acrescente a linha dela em
  [`features/README.md`](features/README.md), que é o índice dono da lista — e **não** em
  [`README.md`](README.md), que é roteador e não carrega inventário.

### Example Mapping

Caminho: `features/<slug>/example-mapping.md`. **Ele não tem teto** — cresce por exemplo
acrescentado, e acrescentar exemplo é o trabalho dele.

Quatro blocos: história, regras, exemplos concretos e perguntas em aberto. O exemplo
existe para revelar o que a regra não disse — fronteira, erro, repetição, concorrência,
idempotência —, e um que apenas a reafirma em outras palavras não acrescenta nada. Use
contraexemplo para registrar o que a regra deixa passar.

### BDD

Caminho: `features/<slug>/behavior.feature`. Cabeçalho `# language: pt`.

- **Comportamento externo e observável.** Nome de classe, de tabela e de coluna não
  aparecem num cenário; o veredito, a contagem e a recusa aparecem.
- Poucos cenários por regra: o fluxo principal, uma falha relevante, e um caso de borda
  quando ele mudar o resultado.
- Todo cenário leva a tag `@teste-ausente` enquanto não houver teste que o verifique.
  Quando o teste existir, troque a tag pelo identificador dele.
- **Nenhuma dependência de BDD entra no projeto por causa disso.**

### `architecture/`

O `README.md` da pasta é o dono da topologia: os processos, o papel de cada um e a posição
na rede. Cada afirmação dele foi conferida na árvore — `pom.xml`, `compose.yaml`,
`Dockerfile`, os `application.yml`, as migrações Flyway e `local/`. Mantenha essa
propriedade: o que não puder ser confirmado ali não entra.

Uma **restrição** ganha arquivo próprio em `constraints/`, e ela diz o que proíbe e o que
protege. Uma restrição sem consequência observável não é restrição.

Os **schemas** têm verificador próprio, que compara a forma desenhada com as migrações
Flyway. Ele roda no CI, e a divergência aceita vive numa baseline:

```bash
python scripts/check_schema_sync.py --root . --baseline scripts/schema-sync-baseline.txt
```

### `contracts/`

**Um contrato é criado quando a interface existir**, nunca antes. Caminhos:
`contracts/openapi/` e `contracts/asyncapi/`.

- **Não crie diretório vazio.** Uma pasta `openapi/` sem conteúdo afirma que existem APIs a
  documentar, e o repositório já pagou por esse erro uma vez.
- O que estiver formalizado num contrato **NÃO DEVE** ser repetido em Markdown.
- Ao criar o primeiro, atualize [`contracts/README.md`](contracts/README.md), que é o dono
  do inventário e dos gatilhos.

### `data-dictionary.md`

Uma linha por termo, com o par português/inglês e uma frase dizendo o que ele é. **Os
termos são em inglês, e as explicações em português**, porque todo identificador de código
é escrito em inglês.

Um termo que nasceu em inglês e não tem par vai para a segunda tabela do arquivo, e não
para a primeira.

### `roadmap.md`

Alto nível, sem data e sem link. Ele diz para onde o projeto vai; ele não inventaria o que
já existe na árvore, e não decide nada. Uma etapa que mudou de pergunta ou de dificuldade
muda aqui; uma etapa que apenas atrasou não muda nada, porque não há prazo declarado.

## Convenções de escrita

As convenções gerais estão no [`AGENTS.md` da raiz](../AGENTS.md) e valem aqui sem
alteração: linhas em aproximadamente 88 colunas, sem emojis, sem linguagem de marketing.

Sobre diagrama: **ele entra quando explicar algo que o texto não explica**. Mermaid inline
— `sequenceDiagram` para ordem no tempo, `flowchart` para topologia, `erDiagram` para a
forma de um schema. Excalidraw só para o que o Mermaid não expressa, exportado como
`.excalidraw.svg` em `diagrams/`. Um diagrama que repete a prosa fica de fora.

## Antes de encerrar uma edição

- Os links relativos resolvem. Um link entre níveis de diretório erra com facilidade —
  `architecture/README.md` apontando para `../README.md` resolve para `docs/README.md`, e
  não para a raiz.
- O que não pôde ser confirmado no código está escrito como pergunta em aberto, e não como
  fato.
- Os verificadores que o CI roda passam, com a invocação exata dele:

  ```bash
  python scripts/verify_docs.py --root . --baseline scripts/verify-docs-baseline.txt
  python scripts/check_schema_sync.py --root . --baseline scripts/schema-sync-baseline.txt
  ```

  O `--baseline` **não tem valor padrão**: omiti-lo faz o verificador reportar como defeito
  toda divergência que já era aceita.

- Antes de apagar um heading, descubra quem o cita — a resposta é recalculada a cada
  execução, e nada é gravado na árvore:

  ```bash
  python scripts/check_citations.py --root . --quem-cita docs/<arquivo>.md
  ```
