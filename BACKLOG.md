# BACKLOG

Arquivo único das pendências de definição deste projeto. Tópicos de alto nível, uma linha
ou um parágrafo curto cada.

**Como usar este arquivo:**

- **Não tem data.** O git guarda quando a linha entrou e quando saiu.
- **Não tem identificador.** Nada aqui é citado de fora; se precisar apontar para um
  tópico, use o título dele.
- **Não tem alternativa enumerada nem trade-off escrito.** Isso se discute na conversa, e
  o resultado vai para o código.
- **Uma pendência resolvida some daqui**, no mesmo commit que a resolve.
- **Um agente pode acrescentar um tópico**, e nunca resolver um sozinho.

---

## Implementação

Nada de fenômeno ou capacidade está implementado. O que existe é esqueleto executável:
compila, empacota e sobe contra PostgreSQL.

- **Qual é o primeiro experimento a rodar de ponta a ponta.** Escolher um fenômeno e levá-lo
  até o veredito, em vez de construir infraestrutura genérica antes.
- **Guarda executável para aleatoriedade semeada, relógio injetável e ausência de
  sincronização de JVM.** Hoje as três regras são texto no `AGENTS.md`; uma violação passa
  em silêncio e quebra a reprodutibilidade meses depois. Falta decidir a forma da guarda —
  ArchUnit, inspeção de bytecode, regra de compilação.
- **Onde o experimento que mata o processo de propósito encontra o orquestrador que o
  reinicia.** Um `Deployment` com `selfHeal: true` desfaz a falha injetada. É a confusão
  entre sistema medido e instrumento um nível abaixo, e não tem solução escolhida.
- **Autenticação e regras próprias no `api-gateway`.** O gateway entrou como módulo Spring
  justamente para ser o ponto único disso, e hoje ele só encaminha por prefixo. Falta
  escolher o mecanismo, e decidir se ele convive com o Cloudflare Access na frente ou o
  substitui.
- **O SSE atrás do Cloudflare.** O gateway é reativo e não bufferiza o corpo, mas o
  Cloudflare pode: um stream bufferizado vira lote sem produzir erro nenhum. Falta o
  `Cache-Control: no-transform` no servidor, e ninguém testou o caminho inteiro.
- **Como o instrumento alcança uma instância específica do sistema medido.** O `Service` do
  Kubernetes escolhe uma instância por conexão, e o experimento que sobe o sistema medido
  com duas instâncias precisa que a segunda chamada de um passo caia na mesma que abriu a
  transação. Se cair na outra, a transação não existe lá, e a falha é indistinguível de um
  fenômeno de consistência real. Falta escolher entre `Service` headless com DNS por pod,
  endereço da instância carregado no identificador da sessão, ou um discovery com
  metadados de instância. Isso não passa pelo `api-gateway`, que só serve o navegador.

## Instruções do repositório

- **Onde vivem as regras estruturais de código.** Aleatoriedade semeada, relógio
  injetável, ausência de sincronização de JVM e conexão por worker estão hoje no
  `AGENTS.md`, e não é o lugar delas. Falta escolher o destino e reescrevê-las.
- **A definição do oráculo exato e da calibração não vive mais em lugar estável.** A
  fórmula `lost_operations = commits − (final_value − initial_value)` e a exigência de
  calibrar com `ATOMIC_UPDATE` saíram do `AGENTS.md` junto com a arquitetura conceitual.
  Elas viram código quando o primeiro experimento for implementado, ou se perdem.

## Documentação existente

- **Triagem de `docs/`.** São 149 arquivos Markdown versionados, ~43 mil linhas, escritos
  sob um processo que não vale mais. A revisão é arquivo por arquivo, e a decisão de
  apagar, encolher ou manter é da pessoa. Nada foi apagado.
- **Os verificadores documentais.** O workflow `docs` roda `verify_docs.py`,
  `check_queue_ids.py` e `check_schema_sync.py`, e um hook `PostToolUse` em
  `.claude/settings.json` roda o primeiro a cada edição de `.md` — citação por âncora,
  teto de tamanho, padding de tabela, fim de linha, unicidade de identificador de fila e
  sincronia entre `erDiagram` e migração Flyway. Eles sustentam o processo revogado, e o
  de citações **reprova quem apagar um heading citado**, o que torna a triagem de `docs/`
  mais cara do que precisa. Falta decidir quais sobrevivem.
- **As skills e os agentes de especificação.** `feature-planning`, `adr`, e os agentes
  `feature-writer`, `feature-reviewer`, `spec-coordinator` e `artifact-verifier`
  continuam no disco, agora sem gatilho automático. Falta decidir se ficam.

## Entrega

- **O `Application` do ArgoCD segue em `ComparisonError`.** Os manifests vivem no
  `homelab-infrastructure`, e a implementação do lado de lá não foi feita. O pipeline não
  está completo.
