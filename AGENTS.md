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
2. **NÃO DEVE escrever documentação por iniciativa própria.** Nem ADR, nem Feature Card,
   nem Example Mapping, nem seção nova em documento existente. A decisão de documentar é
   da pessoa, sempre, e ela precisa ser dita nesta sessão — em palavras, não inferida de
   uma regra deste arquivo nem do gatilho de uma skill.
3. **Pendência de definição vai para o [`BACKLOG.md`](BACKLOG.md) da raiz, e para lugar
   nenhum além dele.** Um tópico de alto nível, uma linha ou um parágrafo curto. Sem
   data, sem identificador, sem alternativa enumerada, sem trade-off escrito — o git já
   guarda quando e por quê.
4. **Bloqueio de implementação vira pergunta, e não documento.** Quando faltar uma
   definição para escrever código, use `AskUserQuestion`. Se a pessoa não responder
   agora, registre o tópico no `BACKLOG.md` e implemente o resto.

**Documentar vale a pena num caso raro, e ele tem uma marca: o conhecimento não cabe no
código.** Um contrato com sistema externo, um motivo que só existe fora da árvore, uma
escolha que o código executa mas não explica. Comportamento, estrutura e fluxo **não** são
esse caso — o código já os diz, e um `.md` que os repete nasce divergente. Na dúvida, não
escreva: pergunte.

**O que está em `docs/` é histórico, e não contrato.** Não o leia para descobrir o que
fazer, não o cite como evidência, não o mantenha sincronizado com o código, e não o
apague — a triagem daquele diretório é da pessoa, arquivo por arquivo. Se um documento de
lá contradisser o código, o código está certo.

**Estas regras não são estado de projeto, e por isso não expiram.** Elas continuam
valendo em toda sessão futura até que a pessoa as revogue neste arquivo, por escrito.

| Comando                           | O que ele faz                                         |
|-----------------------------------|-------------------------------------------------------|
| `mvn verify`                      | compila e sobe cada serviço contra PostgreSQL efêmero |
| `docker compose up --build`       | sobe o banco e os serviços do `compose.yaml`          |
| `npm --prefix frontend run build` | constrói a interface                                  |

A stack, as versões e os serviços que sobem estão declarados em `pom.xml`,
`compose.yaml` e `frontend/package.json`. Leia-os de lá.

## Convenções gerais de escrita

**Esta seção é um portão, e não um convite.** Ela só entra em cena depois que a pessoa
pediu um documento em palavras, e nunca é motivo para escrever um. Ela não alcança
mensagem de commit, resposta de chat, comentário de código nem `.md` que já existe — não
reformate o que está lá para obedecê-la.

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
guarda é tópico do `BACKLOG.md`.

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
- **Questione decisões quando fizer sentido, e explique trade-offs** — na conversa. A
  pessoa pediu mentoria arquitetural, e mentoria acontece falando, não versionando.
- **Prefira uma linha no `BACKLOG.md` a inventar uma decisão para fechar uma lacuna.**
- **Não invente integração, contrato ou regra.** O que não puder ser confirmado no código
  ou na configuração é pergunta, nunca fato. A regra antiga de citação por âncora nomeada
  vale apenas dentro de `docs/`, e você não escreve lá sem pedido.
- Ao mexer em arquivos, faça `git add` apenas dos arquivos relacionados e gere um único
  commit em Conventional Commits (skill `commit`).
