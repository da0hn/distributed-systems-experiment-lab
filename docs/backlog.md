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
  substitui. Quando isso for feito, atenção ao `redirect_uri`: o Traefik local roda em
  HTTP por escolha, então o único cenário que a stack local **não** reproduz é o de TLS
  terminado antes do gateway — que é justamente onde um `redirect_uri` com esquema errado
  se manifesta.
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
- **O término de uma execução, agora que o instrumento é dois serviços.** Um executa os
  passos e escala; o outro admite, consome o stream e produz o veredito, em instância
  única. O término é notificado aos dois, e cada um age no que lhe cabe. Quem julga não
  pode somar quando a notificação chega — os eventos ainda estão em voo entre o WAL e a
  fila —, e por isso ele espera a marca de fim do stream; a notificação serve para armar
  o prazo que separa `fonte atrasada` de execução ainda rodando. Falta decidir quem
  emite a parada antecipada, como a marca é escrita, e que nome os dois serviços recebem.

- **Os conjuntos de valores que as colunas de `CHECK` do plano não fecham.** Os lados de
  fronteira, os níveis de isolamento aceitos, o destino da carga, a forma do identificador
  de execução e quem atribui as chaves primárias. Sem eles a migração das tabelas do plano
  não pode ser escrita, e o que depende dela fica parado.
- **As colunas de tempo do schema.** Falta decidir se as tabelas do sistema medido ganham
  criação e atualização, e se o início e o fim de uma execução entram no veredito por
  curva — o segundo obriga relógio injetado em vez do relógio do banco.
- **A rota `/api/runs` não leva a lugar nenhum.** O caminho existe no roteamento e não tem
  implementação atrás dele.
- **O contrato de iniciar uma execução.** Falta decidir se a requisição cria uma execução
  ou uma sequência delas, e se a chave de idempotência é exigida do cliente.
- **A vida de uma execução ativa.** Falta o limite, se a execução encerrada por limite
  ainda produz veredito, e se cancelamento e abandono se distinguem no registro.
- **O limite de espera do oráculo.** Falta o número a partir do qual a sentinela desiste e
  a leitura é rotulada como fonte atrasada.
- **Quem confere a alocação órfã.** Não há foreign key entre os dois schemas, e o
  instrumento não pode consultar o schema do sistema medido para verificar integridade.
- **O que a contagem base conta, e o que o relatório afirma sobre um zero.** A taxa de
  aborto pode contar tentativas ou execuções de operação, e os dois números diferem;
  falta também decidir quem escolhe o número de tentativas de uma execução medida.
- **A forma do veredito por curva.** O segundo formato não tem forma concreta, e falta
  decidir se a taxa com intervalo de confiança é um terceiro formato ou uma variação.
- **O modelo de thread do worker.** Threads de plataforma ou threads virtuais, decidido
  antes de escrever o runtime de execução.
- **Onde o runtime fixa o nível de isolamento** de cada tentativa, já que ele é parâmetro
  do experimento e não configuração global do serviço.
- **O tipo de evento para o bloqueio de buffer.** Falta decidir se o conjunto fechado de
  tipos do log de observações ganha mais um valor, ou se esse bloqueio é registrado fora
  do log.
- **Onde vive a configuração do Debezium Server**, e por onde a senha do banco chega até
  ela.
- **A transação que atravessa duas chamadas de passo.** A direção provisória é uma sessão
  guardada pelo sistema medido, indexada por um identificador que carrega a instância que
  a criou. A confiança registrada é baixa, e ela colide com a forma decidida do escopo
  transacional.
- **O serviço que ajusta o número de instâncias do sistema medido antes da janela
  medida.** Falta decidir onde ele vive, qual credencial de cluster ele carrega — ela não
  pode ficar no processo que produz o veredito — e se escalar dentro da janela é
  permitido.
- **A stack do frontend e o teto de eventos no navegador.** Framework de componentes,
  forma de renderização, e paginação contra o servidor quando o stream cresce demais para
  a tela.

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
- **O prefixo `/api/lab-plane` nomeia um serviço que virou dois.** Falta decidir se ele se
  divide em dois prefixos ou se os dois processos seguem publicando sob um só.
- **A sessão do Access expira no meio de um stream de longa duração.** É modo de falha
  real, e ninguém testou o caminho inteiro.
