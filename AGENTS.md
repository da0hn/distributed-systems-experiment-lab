# AGENTS.md

Guia para agentes de código ao trabalhar neste repositório.

## O modo de trabalho é implementação primeiro

**Esta seção revoga o processo documental que este arquivo descrevia antes, e ela
prevalece sobre qualquer outra seção deste arquivo, sobre `docs/` inteiro, sobre as
skills de `.claude/skills/` e sobre os agentes de `.claude/agents/`.** Onde houver
conflito, vale o que está aqui.

O que muda, em quatro regras:

1. **O código é a documentação.** A árvore, os testes e a configuração versionada são a
   fonte da verdade. Um `.md` que descreve comportamento não implementado é hipótese, e
   hipótese envelhece sozinha.
2. **NÃO DEVE inventar documento.** Nem ADR, nem artefato de processo, nem página nova
   sobre assunto que ninguém pediu, nem seção nova para registrar raciocínio próprio.
   Escrever porque pareceu útil é o que esta regra proíbe. **Manter em dia o que já
   existe é outra coisa, é obrigatório, e a seção "A documentação que restou acompanha o
   código" diz exatamente quando.**
3. **Pendência de definição vai para o `docs/backlog.md`, e para lugar nenhum além
   dele.** Um tópico de alto nível, uma linha ou um parágrafo curto. Sem data, sem
   identificador, sem alternativa enumerada, sem trade-off escrito — o git já guarda
   quando e por quê.
4. **Bloqueio de implementação vira pergunta, e não documento.** Quando faltar uma
   definição para escrever código, use `AskUserQuestion`. Se a pessoa não responder
   agora, registre o tópico no `docs/backlog.md` e implemente o resto.

**O `docs/backlog.md` é instável, e NÃO DEVE ser referenciado por documento nenhum.** Ele
existe para uma coisa só: guardar o que está sendo feito, para que a próxima sessão
continue de onde a anterior parou. Uma linha dele nasce e some conforme o trabalho anda,
então um link para ele aponta para texto que não estará lá — cite-o pelo caminho, em
texto puro, nunca como link, e nunca como evidência de nada.

**Documentar por conta própria vale a pena num caso raro, e ele tem uma marca: o
conhecimento não cabe no código.** Um contrato com sistema externo, um motivo que só
existe fora da árvore, uma escolha que o código executa mas não explica. Na dúvida, não
escreva: pergunte.

## O que existe na raiz, e onde aprofundar

Esta tabela é ponto de partida de busca, e não descrição de comportamento. Quando
precisar do detalhe, abra o arquivo indicado — ele é a autoridade, e esta tabela não.

| Caminho              | O que é                                                                                  | Onde aprofundar                                           |
|----------------------|------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `pom.xml`            | reactor Maven, e a declaração da stack: cinco módulos, Java e Spring Boot                | o próprio arquivo                                         |
| `shared/`            | módulo de código comum aos serviços                                                      | `shared/src/main/java`                                    |
| `api-gateway/`       | entrada única de HTTP, em Spring Cloud Gateway; roteia por prefixo de caminho            | `api-gateway/src/main/resources/application.yml`          |
| `lab-plane/`         | o plano de controle do laboratório                                                       | `lab-plane/src/main/resources/`, e `db/migration/` nele   |
| `lab-journal/`       | o caderno de laboratório: definição de experimento e resultado, fora do Git              | `lab-journal/src/main/resources/`, e `db/migration/` nele |
| `system-under-test/` | o sistema medido, e ele não conhece o instrumento                                        | `system-under-test/src/main/resources/`                   |
| `frontend/`          | a interface, em Vite; servida por nginx na imagem                                        | `frontend/package.json`, `vite.config.ts`, `nginx.conf`   |
| `compose.yaml`       | a topologia local: PostgreSQL com WAL lógico, os serviços, a interface e o Traefik       | o próprio arquivo                                         |
| `Dockerfile`         | a imagem dos serviços Java                                                               | o próprio arquivo                                         |
| `local/`             | insumos que o compose monta: `postgres-init.sql` e a configuração do Traefik             | `local/traefik/`                                          |
| `scripts/`           | os verificadores de documentação que o CI roda, e as baselines deles                     | `scripts/verify_docs.py`                                  |
| `.github/workflows/` | `build.yml` compila, prova e publica a imagem; `docs.yml` verifica `docs/`               | os próprios arquivos                                      |
| `.claude/`           | skills e agentes; boa parte descreve o processo revogado, e não vale contra este arquivo | —                                                         |
| `graphify-out/`      | saída de ferramenta externa; não é fonte de nada e não é mantida                         | —                                                         |
| `docs/`              | a documentação, em estrutura fechada                                                     | `docs/README.md`                                          |

**O `system-under-test` sobe no compose e não tem rota no gateway, e a ausência é
deliberada.** Uma requisição feita à mão durante a janela medida entra no oráculo exato
como commit real, e nada a distingue da carga do experimento.

| Comando                           | O que ele faz                                         |
|-----------------------------------|-------------------------------------------------------|
| `mvn verify`                      | compila e sobe cada serviço contra PostgreSQL efêmero |
| `docker compose up --build`       | sobe o banco e os serviços do `compose.yaml`          |
| `npm --prefix frontend run build` | constrói a interface                                  |

## `docs/` tem uma estrutura fechada

**Cinco pastas e quatro arquivos, e nada além disso.** Um documento que não couber em um
deles não é escrito, e nenhum caminho novo é inventado.

```
docs/
  README.md              índice: o que cada pasta guarda; só navegação
  roadmap.md             o plano geral, em alto nível, sem data
  data-dictionary.md     o de/para do vocabulário do laboratório
  backlog.md             instável; nunca referenciado
  architecture/          arquitetura, serviços e restrições arquiteturais
  adr/                   decisões arquiteturais, congeladas no tempo
  features/              uma feature do sistema por diretório
  contracts/             contrato formal entre processos, quando existir
  diagrams/              o que o Mermaid não expressa, em `.excalidraw.svg`
```

**`docs/adr/` está congelado.** Ele serve para consultar o que já foi decidido, e nada
novo é escrito ali — nem ADR, nem edição de ADR existente. Nenhum gatilho da seção
seguinte alcança esta pasta.

**Um documento daqui não é contrato.** Se ele contradisser o código, o código está certo —
e a contradição é defeito a corrigir, e não estado aceito.

**Estas regras não são estado de projeto, e por isso não expiram.** Elas continuam
valendo em toda sessão futura até que a pessoa as revogue neste arquivo, por escrito.

## A documentação que restou acompanha o código

A pasta encolheu para o que vale a pena manter, e o que sobrou é mantido. **Quando uma
mudança de código dispara uma linha desta tabela, atualizar o destino é obrigatório, e
não conta como iniciativa própria** — o gatilho é código concreto que entrou na árvore, e
não a impressão de que a página ficaria melhor.

| A mudança no código                                                                                      | O destino                        | O que escrever ali                                                     |
|----------------------------------------------------------------------------------------------------------|----------------------------------|------------------------------------------------------------------------|
| uma feature do sistema nasce e ganha comportamento executável                                            | `docs/features/<nome>/`          | o que a feature faz, e as regras que os testes provam                  |
| uma feature que já tem página muda de comportamento                                                      | a página dela                    | só a parte que mudou                                                   |
| um módulo do reactor, um serviço do `compose.yaml` ou uma rota do gateway nasce, muda de papel ou some   | `docs/architecture/README.md`    | o papel do serviço e a posição dele na topologia                       |
| uma restrição arquitetural nova passa a valer                                                            | `docs/architecture/constraints/` | um arquivo por restrição, dizendo o que ela proíbe e o que ela protege |
| um contrato entre processos é fixado: forma de evento, payload de fila, endpoint que outro serviço chama | `docs/contracts/`                | a forma do contrato, e quem está de cada lado                          |
| um termo do vocabulário do laboratório entra no código, ou muda de nome                                  | `docs/data-dictionary.md`        | a linha de/para, em português e em inglês                              |
| o plano geral muda de rumo                                                                               | `docs/roadmap.md`                | em alto nível, sem data e sem link                                     |

**A atualização vai no MESMO commit da mudança de código que a disparou.** Um commit
depois ela é esquecida, e uma página que descreve a árvore de ontem é pior que página
nenhuma: ela é lida como se descrevesse a de hoje.

**O que NÃO dispara nada:**

- refatoração que não muda comportamento observável;
- correção de defeito que restaura o comportamento já descrito;
- mudança de dependência, de versão ou de configuração de build;
- teste novo sobre comportamento que a página já descreve;
- qualquer coisa em `docs/adr/`, que está congelado.

**Se a atualização exigir uma definição que você não tem, não invente.** Use
`AskUserQuestion`. Se a resposta não vier agora, registre o tópico no `docs/backlog.md`,
implemente o código e diga na conversa qual página ficou para trás.

## Convenções gerais de escrita

**Esta seção é um portão, e não um convite.** Ela vale para o documento que a pessoa
pediu e para a atualização que a seção anterior obriga, e nunca é motivo para escrever um
documento novo. Ela não alcança mensagem de commit, resposta de chat nem comentário de
código — e não reformate `.md` existente só para obedecê-la.

- Linhas quebradas em aproximadamente 88 colunas. Um link Markdown longo PODE ultrapassar.
- Diagrama só quando ele explicar algo que o texto não explica. Mermaid inline;
  `sequenceDiagram` para ordem no tempo, `flowchart` para topologia, `erDiagram` para
  schema. **Deixou de ser obrigatório** acompanhar todo fluxo descrito com um diagrama.
- Sem emojis. Sem linguagem de marketing.

## Regras estruturais que valem sempre

Estas são regras de código, e a violação de qualquer uma produz falso resultado
silencioso.

- **Nenhuma aleatoriedade não semeada.** `Math.random()`, `java.util.Random` e
  `ThreadLocalRandom` são proibidos fora do componente de aleatoriedade semeada.
- **O tempo é injetável.** `Instant.now()`, `LocalDateTime.now()` e
  `System.currentTimeMillis()` só em adaptador de relógio. Sem isso, expiração de lease e
  clock skew ficam impossíveis de testar.
- **Nenhuma sincronização de JVM no sistema sob teste.** `synchronized`, `ReentrantLock` e
  `AtomicInteger` mascaram exatamente os fenômenos que o laboratório estuda. A exceção é a
  estratégia `JVM_LOCK`, que existe como experimento para provar que ela falha com duas
  instâncias.
- **Cada worker tem sua própria conexão.** Se o pool serializar dois workers, o
  experimento produz um falso negativo silencioso.
- **Nenhuma tecnologia entra por estar disponível.** Cada uma entra quando um experimento
  não puder ser executado sem ela.
- **O caderno de laboratório não vive no Git.** A definição de experimento e o resultado
  vivem no banco do `lab-journal`. Nem `experiments/` nem `docs/experiments/` são criados.

As três primeiras alcançam pelo papel do valor, e não pelo plano que o produz: valem sobre
todo valor que entra em veredito, em escalonamento ou em identidade derivada da semente,
no sistema medido ou no Lab Plane. Elas são hoje **texto, não guarda executável** — a
guarda é tópico do `docs/backlog.md`.

## Este repositório é entregue no homelab

O laboratório é entregue como carga de trabalho do repositório
[`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure). Três
guardrails operacionais:

- **A tag da imagem é `X.Y.Z-<run_number>`, nunca `latest`.** `X.Y.Z` vem do `pom.xml` do
  reactor e do `frontend/package.json`; o SHA do commit vive no label OCI
  `org.opencontainers.image.revision`.
- **Nenhum Secret vive neste repositório.** Eles ficam cifrados no homelab e são
  referenciados por nome.
- **`deploy/` não existe, e nunca vai existir aqui.** Os manifests vivem no
  `homelab-infrastructure`, em `kubernetes/applications/distributed-consistency-lab/`.

**Kubernetes é destino de entrega, não objeto de estudo.** Nenhum fenômeno é reproduzido
por um recurso do cluster.

## Ao trabalhar aqui

- **Implemente.** Quando o pedido couber em código, escreva o código. Não abra um ciclo de
  especificação, não proponha um artefato, não peça aprovação de regra escrita.
- **Feche a passada.** Código que dispara uma linha da tabela de gatilhos só está pronto
  com o destino atualizado, no mesmo commit.
- **Questione decisões quando fizer sentido, e explique trade-offs** — na conversa. A
  pessoa pediu mentoria arquitetural, e mentoria acontece falando, não versionando.
- **Prefira uma linha no `docs/backlog.md` a inventar uma decisão para fechar uma lacuna.**
- **Não invente integração, contrato ou regra.** O que não puder ser confirmado no código
  ou na configuração é pergunta, nunca fato.
- Ao mexer em arquivos, faça `git add` apenas dos arquivos relacionados e gere um único
  commit em Conventional Commits (skill `commit`).
