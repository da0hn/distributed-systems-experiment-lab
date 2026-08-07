# Graph Report - D:\Code\Personal\distributed-consistency-lab  (2026-08-07)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 372 nodes · 396 edges · 81 communities (27 shown, 54 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a29f4c4d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Contratos de API
- package.json
- ADR-0012: Broker no caminho do veredito
- resource-service
- scan_transcripts.py
- compilerOptions
- ADR README
- ADR 0002 Minimal Domain and Oracles
- json-schema.json
- Unique Invariant
- check_citations.py
- SystemUnderTestApplicationTests
- LabJournalApplicationTests.java
- LabPlaneApplicationTests.java
- PostgreSQL Service
- Chaos Relay
- ADR-0004: Estatuto da Barreira e Diagnóstico da Não Ocorrência
- O terceiro formato de veredito precisa caber ao lado dos dois já previstos
- resource-service (ADR-0011)
- Q-0001-4 — O escalonador precisa de um protocolo de desistência
- main.tsx
- LabJournalApplication
- LabPlaneApplication
- SystemUnderTestApplication
- Skill Design de Código-fonte
- O N declarado antes não fecha com uma estratégia que retenta
- Lab Plane Application Configuration
- System Under Test Application Configuration
- Arquitetura Mínima e Guardas
- Entrega Contínua no Homelab
- Estratégias de Concorrência
- Topologia Lab Plane e system under test
- Shared Module (lab-messaging-contract)
- Idempotent Inbox
- Leitura Autoritativa (Grupo de Controle de Leitura)
- Série Arquivada de ADRs
- Skill Modelagem de Domínio
- Context Format Reference
- AsyncAPI Template
- Example Mapping Template
- Feature Card Template
- Implementation Plan Template
- Integrations Template
- OpenAPI Template
- Path
- ADR-0007 Observation Log Form, Order and Storage
- ADR-0008
- lab-journal
- system-under-test
- README da rodada de arquitetura arquivada
- Plano de escrita dos ADRs do Lote E
- ADR-0011: topologia de serviços
- Example Mapping: Execução de Experimento
- Feature Card — Execução de experimento e classificação do veredito
- Q-0001-1: Endereço de Fronteira vs Edição
- Q-0002-1: Regras de Comparação por Valor
- Q-0003-3: Critério de Igualdade entre Execuções
- Q-0001-3 — O critério de igualdade entre dois traços de SQL não está definido
- Q-0002-3 — Os dois oráculos descrevem apenas o estado final quiescente
- Q-0002-4 — O estado inicial não é estabelecido por ninguém
- Comparar janelas exige um instante comparável entre workers
- Q-0019
- Q-0020
- Q-0021
- Q-0022
- Q-0023
- Q-0024
- Q-0025
- Q-0026
- Q-0027
- Q-0028
- Frontend Index
- ADR-0017 do Homelab (Contrato de Entrega)
- dev.da0hn.lab:distributed-consistency-lab
- lab-journal
- lab-plane
- shared
- system-under-test

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 14 edges
2. `Contratos de API` - 13 edges
3. `ADR-0002 — O domínio mínimo e os dois oráculos` - 12 edges
4. `ADR-0012: Broker no caminho do veredito` - 10 edges
5. `scan()` - 7 edges
6. `inspect()` - 7 edges
7. `SystemUnderTestApplicationTests` - 7 edges
8. `ADR 0002 Minimal Domain and Oracles` - 7 edges
9. `ADR README` - 7 edges
10. `Fila de avaliação — decisões pendentes` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Documentation Workflow` --references--> `ADR README`  [EXTRACTED]
  .github/workflows/docs.yml → docs/adr/README.md
- `ADR Reviewer Agent` --references--> `ADR README`  [EXTRACTED]
  .claude/agents/adr-reviewer.md → docs/adr/README.md
- `ADR Writer Agent` --references--> `ADR README`  [EXTRACTED]
  .claude/agents/adr-writer.md → docs/adr/README.md
- `Citations Baseline` --references--> `ADR README`  [EXTRACTED]
  scripts/citations-baseline.txt → docs/adr/README.md
- `Fila de decisões` --references--> `ADR-0017 do homelab-infrastructure`  [EXTRACTED]
  docs/adr/fila-de-decisoes.md → homelab-infrastructure/docs/adr/0017-cicd-das-aplicacoes-no-github-actions.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **CDC transport path to verdict** — docs_adr_0012_o_broker_no_caminho_do_veredito_e_a_dispensa_que_ele_exigiu_wal, docs_adr_0012_o_broker_no_caminho_do_veredito_e_a_dispensa_que_ele_exigiu_debezium_server, docs_adr_0012_o_broker_no_caminho_do_veredito_e_a_dispensa_que_ele_exigiu_rabbitmq [EXTRACTED 1.00]
- **Services with separate schemas and process boundaries** — docs_adr_0011_a_topologia_de_servicos_e_o_caderno_de_laboratorio_fora_do_git_lab_journal, docs_adr_0011_a_topologia_de_servicos_e_o_caderno_de_laboratorio_fora_do_git_system_under_test [EXTRACTED 0.95]
- **LSN-based CDC transport integrity** — docs_adr_0012_o_broker_no_caminho_do_veredito_e_a_dispensa_que_ele_exigiu_lsn, docs_adr_0012_o_broker_no_caminho_do_veredito_e_a_dispensa_que_ele_exigiu_debezium_server, docs_adr_0012_o_broker_no_caminho_do_veredito_e_a_dispensa_que_ele_exigiu_rabbitmq [EXTRACTED 1.00]
- **Reconciliação das fontes de autoridade documental** — docs_audits_2026_08_06_coerencia_e_limites_documentais_document, docs_adr_fila_de_decisoes_document, docs_architecture_integrations_document, concept_authority_documental [EXTRACTED 0.95]
- **Local Laboratory Service Topology** — compose_postgres, compose_lab_plane, compose_lab_journal, compose_system_under_test, compose_frontend [EXTRACTED 1.00]
- **Specification and Decision Process** — docs_specification_process, docs_adr_readme, docs_context [EXTRACTED 0.95]
- **Fluxo de execução, observações e relatório pela API** — recurso_execucao, recurso_observacao, relatorio_execucao, sse_streaming [EXTRACTED 1.00]
- **Arquitetura de eventos para histórico e tempo real** — rabbitmq_eventos, servico_historico, sse_streaming, debezium_cdc [EXTRACTED 1.00]
- **Propostas de arquitetura de 2026-08-03** — docs_adr_arquivo_proposta_2026_08_03_entrega_continua, docs_adr_arquivo_proposta_2026_08_03_interface_web, docs_adr_arquivo_proposta_2026_08_03_mensageria, docs_adr_arquivo_proposta_2026_08_03_modelo_de_dados [EXTRACTED 1.00]
- **Lab Plane and system under test shared schema boundary** — lab_plane, shared_kernel_schema [EXTRACTED 0.95]
- **Experiment observation and diagnosis flow** — docs_features_execucao_de_experimento_feature_card_document, docs_features_observacao_passo_a_passo_feature_card_document, docs_features_deteccao_de_atualizacao_perdida_feature_card_document, docs_features_deteccao_de_protecao_inerte_feature_card_document [INFERRED 0.85]
- **Services with isolated database schemas** — lab_journal_lab_journal_schema, lab_plane_lab_plane_schema, system_under_test_sut_schema [EXTRACTED 1.00]
- **Lab Journal, Lab Plane, and System Under Test services** — lab_journal_service, lab_plane_service, system_under_test_service [INFERRED 0.85]
- **ADR-0004 Diagnostic Flow for Non-Occurrence** — docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_adr_0004, docs_adr_0003_a_linguagem_do_agendamento_adr_0003 [INFERRED 0.90]
- **Conjunto de questões que motivam o protocolo de término do worker (ADR-0005)** — docs_questions_q_0001_4_q-0001-4, docs_questions_q_0002_2_q-0002-2, docs_questions_q_0003_1_q-0003-1, docs_questions_q_0003_2_q-0003-2 [INFERRED 0.95]
- **Itens na fila 'A forma do escalonador'** — docs_questions_q_0001_4_q-0001-4, docs_questions_q_0002_2_q-0002-2, docs_questions_q_0003_1_q-0003-1, docs_questions_q_0003_2_q-0003-2 [EXTRACTED 1.00]
- **Distinct Writing Origins for a Single Invariant** — docs_adr_arquivo_0002_operator, docs_adr_arquivo_0002_agent, docs_adr_arquivo_0002_reconciler, docs_adr_arquivo_0002_lease_expiry [EXTRACTED 1.00]
- **Group 1 Mutual Exclusion Strategies** — docs_adr_arquivo_0003_optimistic, docs_adr_arquivo_0003_concurrencystrategy [EXTRACTED 0.90]
- **Core Domain Model Definition** — docs_adr_arquivo_0001_resource, docs_adr_arquivo_0001_capacitymodel, docs_adr_arquivo_0001_invariant [EXTRACTED 1.00]
- **Transição para Invariante Distribuída na Etapa 5** — docs_adr_arquivo_0011_resource_service, docs_adr_arquivo_0011_allocation_service, docs_adr_arquivo_0008_workflow_engine, docs_adr_arquivo_0008_placementsaga [EXTRACTED 1.00]
- **Plataforma Local e Contrato de Versão** — docs_adr_arquivo_0010_docker_compose, docs_adr_arquivo_0010_compose_profiles, docs_adr_arquivo_0010_versions_env, docs_adr_arquivo_0010_service_manifest [EXTRACTED 1.00]
- **Execução de Workflow Plugável** — docs_adr_arquivo_0009_step_executor, docs_adr_arquivo_0009_sync_in_process, docs_adr_arquivo_0009_async_message, docs_adr_arquivo_0009_stepoutcomesink [EXTRACTED 1.00]
- **Mecanismos de Injeção de Falha (ADR-0012)** — docs_adr_arquivo_0012_onde_o_chaos_service_intercepta_chaos_relay, docs_adr_arquivo_0012_onde_o_chaos_service_intercepta_toxiproxy, docs_adr_arquivo_0012_onde_o_chaos_service_intercepta_adaptador_de_relogio [EXTRACTED 1.00]
- **Componentes do Eixo de Leitura (ADR-0013)** — docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_observer, docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_leitura_autoritativa, docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_projecao_assincrona, docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_outbox_adr_0007 [EXTRACTED 1.00]

## Communities (81 total, 54 thin omitted)

### Community 0 - "Contratos de API"
Cohesion: 0.09
Nodes (34): ADR-0002 — O domínio mínimo e os dois oráculos, ADR-0005 — A forma do escalonador, ADR-0006 — A forma da estratégia de concorrência, API HTTP e SSE, Change Data Capture, Debezium e Change Data Capture, ADR-0009: A classificação do dual write e a região de pacote, ADR-0010 — Fronteira de schema e CDC como fonte do veredito (+26 more)

### Community 1 - "package.json"
Cohesion: 0.07
Nodes (26): dependencies, react, react-dom, description, devDependencies, @types/react, @types/react-dom, typescript (+18 more)

### Community 2 - "ADR-0012: Broker no caminho do veredito"
Cohesion: 0.11
Nodes (24): Feature Planning Skill, Workflow Retro Skill, Patch de Skill Template, Taxonomia de Atrito, Modelo de autoridade documental, Debezium Server, RabbitMQ e Lab Plane, Barreira como controle positivo para diagnóstico de frequência, ADR-0007: O log de observações (+16 more)

### Community 3 - "resource-service"
Cohesion: 0.09
Nodes (23): Tabela allocation (schema revisado), Coluna deadline_at, Invariante de Motor Verificável por SQL, EvictionSaga, Mecanismo de Idempotency Key, PlacementSaga, Tabela saga_instance, Tabela saga_step (+15 more)

### Community 4 - "scan_transcripts.py"
Cohesion: 0.18
Nodes (20): counts_prose_only(), default_limit(), is_table_row(), main(), parse_limit(), prose_only(), Devolve o limite do arquivo, ou None quando ele e' isento., Remove blocos cercados e linhas de tabela, que nao entram na contagem. (+12 more)

### Community 5 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noEmit, noFallthroughCasesInSwitch (+13 more)

### Community 6 - "ADR README"
Cohesion: 0.13
Nodes (16): ADR Reviewer Agent, ADR Writer Agent, ADR Skill, ADR Template, ADR Lifecycle, ADR-0007, Decision A2, ADR README (+8 more)

### Community 7 - "ADR 0002 Minimal Domain and Oracles"
Cohesion: 0.18
Nodes (16): ArgoCD, ADR 0002 Minimal Domain and Oracles, ADR 0005 Scheduler Form, ADR 0006 Concurrency Strategy, Decisões pendentes, Entrega contínua no homelab, Interface web, Mensageria: RabbitMQ, CloudEvents e CDC (+8 more)

### Community 8 - "json-schema.json"
Cohesion: 0.13
Nodes (14): additionalProperties, description, examples, $id, properties, required, $schema, title (+6 more)

### Community 9 - "Unique Invariant"
Cohesion: 0.15
Nodes (13): CapacityModel, Unique Invariant, Resource (Aggregate), Agent (Writing Origin), Lease Expiry (Writing Origin), Operator (Writing Origin), OVERCOMMITTED State, Reconciler (Writing Origin) (+5 more)

### Community 10 - "check_citations.py"
Cohesion: 0.32
Nodes (11): NamedTuple, Defect, gfm_slug(), headings_of(), inspect(), line_count(), main(), Path (+3 more)

### Community 11 - "SystemUnderTestApplicationTests"
Cohesion: 0.39
Nodes (6): DataSource, PostgreSQLContainer, SpringBootTest, Test, Testcontainers, SystemUnderTestApplicationTests

### Community 12 - "LabJournalApplicationTests.java"
Cohesion: 0.43
Nodes (6): DataSource, PostgreSQLContainer, SpringBootTest, Test, Testcontainers, LabJournalApplicationTests

### Community 13 - "LabPlaneApplicationTests.java"
Cohesion: 0.43
Nodes (6): DataSource, PostgreSQLContainer, SpringBootTest, Test, Testcontainers, LabPlaneApplicationTests

### Community 14 - "PostgreSQL Service"
Cohesion: 0.48
Nodes (7): Docker Compose Configuration, Frontend Service, Lab Journal Service, Lab Plane Service, PostgreSQL Service, System Under Test Service, Build Workflow

### Community 15 - "Chaos Relay"
Cohesion: 0.47
Nodes (6): experiment-service (ADR-0011), Adaptador de Relógio, Chaos Relay, chaos-service (ADR-0012), Toxiproxy, Observer (ADR-0013)

### Community 16 - "ADR-0004: Estatuto da Barreira e Diagnóstico da Não Ocorrência"
Cohesion: 0.40
Nodes (5): ADR-0001: Passo como Unidade de Execução, ADR-0003: Linguagem do Agendamento, NONE Strategy, ADR-0004: Estatuto da Barreira e Diagnóstico da Não Ocorrência, Q-0001-2: Compartilhamento por Colaborador Injetado sem Guarda

### Community 17 - "O terceiro formato de veredito precisa caber ao lado dos dois já previstos"
Cohesion: 0.67
Nodes (4): Os Dois Formatos de Veredito, Os dois oráculos descrevem apenas o estado final quiescente, O terceiro formato de veredito precisa caber ao lado dos dois já previstos, O limite 3/N pressupõe ensaios independentes

### Community 18 - "resource-service (ADR-0011)"
Cohesion: 0.50
Nodes (4): allocation-service (ADR-0011), resource-service (ADR-0011), Transactional Outbox (ADR-0007), Projeção Assíncrona (Modelo de Leitura)

### Community 19 - "Q-0001-4 — O escalonador precisa de um protocolo de desistência"
Cohesion: 0.50
Nodes (4): Q-0001-4 — O escalonador precisa de um protocolo de desistência, Q-0002-2 — Quem declara que a execução terminou, e o oráculo lê antes ou depois disso, Q-0003-1 — Um worker que nunca chega trava o agendamento, e a recusa por texto não o alcança, Q-0003-2 — Um agendamento sobre uma tentativa que talvez não ocorra

### Community 24 - "Skill Design de Código-fonte"
Cohesion: 0.67
Nodes (3): Skill Design de Código-fonte, Aprofundamento de Módulos, Projetando Duas Vezes

### Community 25 - "O N declarado antes não fecha com uma estratégia que retenta"
Cohesion: 0.67
Nodes (3): Experiment, O estado inicial não é estabelecido por ninguém, O N declarado antes não fecha com uma estratégia que retenta

### Community 26 - "Lab Plane Application Configuration"
Cohesion: 0.67
Nodes (3): Lab Plane Schema, Lab Plane Service, Lab Plane Application Configuration

### Community 27 - "System Under Test Application Configuration"
Cohesion: 0.67
Nodes (3): System Under Test Service, System Under Test Application Configuration, SUT Schema

## Ambiguous Edges - Review These
- `resource-service (ADR-0011)` → `Projeção Assíncrona (Modelo de Leitura)`  [AMBIGUOUS]
  docs/adr/arquivo/0013-eixo-de-leitura-defasagem-e-como-medi-la.md · relation: conceptually_related_to

## Knowledge Gaps
- **166 isolated node(s):** `CapacityModel`, `Operator (Writing Origin)`, `Lease Expiry (Writing Origin)`, `OVERCOMMITTED State`, `OPTIMISTIC Concurrency Strategy` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **54 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `resource-service (ADR-0011)` and `Projeção Assíncrona (Modelo de Leitura)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Contratos de API` connect `Contratos de API` to `ADR 0002 Minimal Domain and Oracles`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `ADR-0002 — O domínio mínimo e os dois oráculos` connect `Contratos de API` to `ADR-0012: Broker no caminho do veredito`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `Modelo de domínio, bounded contexts e context map` connect `Contratos de API` to `ADR-0012: Broker no caminho do veredito`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **What connects `CapacityModel`, `Operator (Writing Origin)`, `Lease Expiry (Writing Origin)` to the rest of the system?**
  _166 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Contratos de API` be split into smaller, more focused modules?**
  _Cohesion score 0.08912655971479501 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._