# Graph Report - D:\Code\Personal\distributed-consistency-lab  (2026-08-05)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 211 nodes · 247 edges · 33 communities (14 shown, 19 thin omitted)
- Extraction: 91% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e33ade7d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Architecture Decision Records
- Plano do Laboratório
- resource-service
- scan_transcripts.py
- json-schema.json
- Modelo de Dados
- Unique Invariant
- ADR-0005: Forma do Escalonador
- Chaos Relay
- O terceiro formato de veredito precisa caber ao lado dos dois já previstos
- resource-service (ADR-0011)
- Q-0001-4 — O escalonador precisa de um protocolo de desistência
- Skill Design de Código-fonte
- O N declarado antes não fecha com uma estratégia que retenta
- Arquitetura Mínima e Guardas
- Entrega Contínua no Homelab
- Estratégias de Concorrência
- Shared Module (lab-messaging-contract)
- Idempotent Inbox
- Leitura Autoritativa (Grupo de Controle de Leitura)
- Série Arquivada de ADRs
- Skill Modelagem de Domínio
- AsyncAPI Template
- Example Mapping Template
- Feature Card Template
- Implementation Plan Template
- Integrations Template
- OpenAPI Template
- Q-0001-3 — O critério de igualdade entre dois traços de SQL não está definido
- Q-0002-3 — Os dois oráculos descrevem apenas o estado final quiescente
- Q-0002-4 — O estado inicial não é estabelecido por ninguém
- Comparar janelas exige um instante comparável entre workers
- ADR-0017 do Homelab (Contrato de Entrega)

## God Nodes (most connected - your core abstractions)
1. `Plano do Laboratório` - 10 edges
2. `Architecture Decision Records` - 8 edges
3. `Messaging: RabbitMQ, CloudEvents and CDC` - 8 edges
4. `scan()` - 7 edges
5. `ADR-0008: Os dois planos em processos separados` - 7 edges
6. `resource-service` - 6 edges
7. `Processo de especificação` - 6 edges
8. `Lab Plane` - 6 edges
9. `Pending Architecture Decisions` - 6 edges
10. `Data Model and PostgreSQL Schema` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Homelab CI/CD Delivery` --conceptually_related_to--> `Plano do Laboratório`  [EXTRACTED]
  AGENTS.md → docs/plano-do-laboratorio.md
- `Step as Execution Unit` --conceptually_related_to--> `Two Planes (SUT vs Lab Plane)`  [INFERRED]
  docs/plano-do-laboratorio.md → README.md
- `Projeção Assíncrona (Modelo de Leitura)` --conceptually_related_to--> `resource-service (ADR-0011)`  [AMBIGUOUS]
  docs/adr/arquivo/0013-eixo-de-leitura-defasagem-e-como-medi-la.md → docs/adr/arquivo/0011-decomposicao-em-servicos-e-fronteiras-transacionais.md
- `Q-0001-2: Compartilhamento por Colaborador Injetado sem Guarda` --semantically_similar_to--> `Retry Contract`  [INFERRED] [semantically similar]
  docs/questions/Q-0001-2.md → docs/adr/0006-a-forma-da-estrategia-de-concorrencia.md
- `E4: optimistic-under-contention` --conceptually_related_to--> `Three Verdict Formats`  [EXTRACTED]
  docs/plano-do-laboratorio.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **ADR Writer-Reviewer Loop** — claude, claude_agents_adr_writer, claude_agents_adr_reviewer, claude_skills_adr [EXTRACTED 0.95]
- **MVP Experiments (E1-E5)** — concept_experiment_e1, concept_experiment_e3, concept_experiment_e4, concept_experiment_e5, concept_exact_oracle, concept_predicate_oracle [EXTRACTED 0.95]
- **Core Architectural Concepts** — concept_step_as_execution_unit, concept_two_planes, concept_five_groups, concept_three_verdict_formats, concept_control_group_mandatory [EXTRACTED 0.90]
- **Fluxo de especificação de capacidade** — feature_card, example_mapping, behavior_feature, architecture_decision_record, context_glossary [EXTRACTED 1.00]
- **Arquitetura com planos separados** — lab_plane, system_under_test, postgresql [EXTRACTED 1.00]
- **Fluxo de decisão e documentação** — decision_queue, architecture_decision_record, feature_card [EXTRACTED 1.00]
- **System Under Test, Lab Plane and PostgreSQL Measurement Boundary** — system_under_test, lab_plane, postgresql [EXTRACTED 0.95]
- **Messaging Flow Through Runtime, RabbitMQ and CloudEvents** — system_under_test, rabbitmq, cloudevents [EXTRACTED 0.95]
- **Architecture Proposals Constrained by Accepted ADRs** — docs_architecture_entrega_continua, docs_architecture_interface_web, docs_architecture_mensageria, docs_architecture_modelo_de_dados [EXTRACTED 0.92]
- **Architecture Documents Cluster** — docs_architecture_modelo-de-dados_modelo-de-dados, docs_architecture_modelo-de-dominio_modelo-de-dominio, docs_architecture_modulos-e-fronteiras_modulos-e-fronteiras [INFERRED 0.80]
- **Lost Update Feature Cluster** — docs_features_deteccao-de-atualizacao-perdida_feature-card, docs_features_deteccao-de-atualizacao-perdida_example-mapping, docs_features_execucao-de-experimento_feature-card [INFERRED 0.75]
- **Open Questions Referenced Across Architecture** — docs_questions_Q-0001-1, docs_questions_Q-0002-1, docs_questions_Q-0003-3 [INFERRED 0.75]
- **ADR-0004 Diagnostic Flow for Non-Occurrence** — docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_adr_0004, docs_adr_0003_a_linguagem_do_agendamento_adr_0003, docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos_adr_0002 [INFERRED 0.90]
- **ADR-0006 Strategy Contract Definition** — docs_adr_0006_a_forma_da_estrategia_de_concorrencia_adr_0006, docs_adr_0005_a_forma_do_escalonador_adr_0005, docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos_adr_0002, docs_adr_0006_retry_contract [INFERRED 0.90]
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

## Communities (33 total, 19 thin omitted)

### Community 0 - "Architecture Decision Records"
Cohesion: 0.10
Nodes (34): Architecture Decision Record, ArgoCD, BDD behavior.feature, CloudEvents, Glossário de domínio CONTEXT.md, Debezium CDC, Fila de decisões, ADR-0007: O log de observações (+26 more)

### Community 1 - "Plano do Laboratório"
Cohesion: 0.09
Nodes (26): ADR Reviewer Agent, ADR Writer Agent, ADR Skill, ADR Template, ADR Lifecycle, Context Format Reference, Feature Planning Skill, Workflow Retro Skill (+18 more)

### Community 2 - "resource-service"
Cohesion: 0.09
Nodes (23): Tabela allocation (schema revisado), Coluna deadline_at, Invariante de Motor Verificável por SQL, EvictionSaga, Mecanismo de Idempotency Key, PlacementSaga, Tabela saga_instance, Tabela saga_step (+15 more)

### Community 3 - "scan_transcripts.py"
Cohesion: 0.24
Nodes (15): default_limit(), main(), parse_limit(), resolve_inside(), blocks_of(), emit(), find_transcripts_dir(), iter_records() (+7 more)

### Community 4 - "json-schema.json"
Cohesion: 0.13
Nodes (14): additionalProperties, description, examples, $id, properties, required, $schema, title (+6 more)

### Community 5 - "Modelo de Dados"
Cohesion: 0.21
Nodes (14): Modelo de Dados, Modelo de Domínio, Módulos e Fronteiras, Example Mapping: Detecção de Atualização Perdida, Feature Card: Detecção de Atualização Perdida, Example Mapping: Detecção de Proteção Inerte, Feature Card: Detecção de Proteção Inerte, Example Mapping: Execução de Experimento (+6 more)

### Community 6 - "Unique Invariant"
Cohesion: 0.15
Nodes (13): CapacityModel, Unique Invariant, Resource (Aggregate), Agent (Writing Origin), Lease Expiry (Writing Origin), Operator (Writing Origin), OVERCOMMITTED State, Reconciler (Writing Origin) (+5 more)

### Community 7 - "ADR-0005: Forma do Escalonador"
Cohesion: 0.24
Nodes (12): ADR-0001: Passo como Unidade de Execução, ADR-0002: Domínio Mínimo e Dois Oráculos, ADR-0003: Linguagem do Agendamento, NONE Strategy, ADR-0004: Estatuto da Barreira e Diagnóstico da Não Ocorrência, ADR-0005: Forma do Escalonador, Termination Concept, ADR-0006: Forma da Estratégia de Concorrência (+4 more)

### Community 8 - "Chaos Relay"
Cohesion: 0.47
Nodes (6): experiment-service (ADR-0011), Adaptador de Relógio, Chaos Relay, chaos-service (ADR-0012), Toxiproxy, Observer (ADR-0013)

### Community 9 - "O terceiro formato de veredito precisa caber ao lado dos dois já previstos"
Cohesion: 0.67
Nodes (4): Os Dois Formatos de Veredito, Os dois oráculos descrevem apenas o estado final quiescente, O terceiro formato de veredito precisa caber ao lado dos dois já previstos, O limite 3/N pressupõe ensaios independentes

### Community 10 - "resource-service (ADR-0011)"
Cohesion: 0.50
Nodes (4): allocation-service (ADR-0011), resource-service (ADR-0011), Transactional Outbox (ADR-0007), Projeção Assíncrona (Modelo de Leitura)

### Community 11 - "Q-0001-4 — O escalonador precisa de um protocolo de desistência"
Cohesion: 0.50
Nodes (4): Q-0001-4 — O escalonador precisa de um protocolo de desistência, Q-0002-2 — Quem declara que a execução terminou, e o oráculo lê antes ou depois disso, Q-0003-1 — Um worker que nunca chega trava o agendamento, e a recusa por texto não o alcança, Q-0003-2 — Um agendamento sobre uma tentativa que talvez não ocorra

### Community 12 - "Skill Design de Código-fonte"
Cohesion: 0.67
Nodes (3): Skill Design de Código-fonte, Aprofundamento de Módulos, Projetando Duas Vezes

### Community 13 - "O N declarado antes não fecha com uma estratégia que retenta"
Cohesion: 0.67
Nodes (3): Experiment, O estado inicial não é estabelecido por ninguém, O N declarado antes não fecha com uma estratégia que retenta

## Ambiguous Edges - Review These
- `resource-service (ADR-0011)` → `Projeção Assíncrona (Modelo de Leitura)`  [AMBIGUOUS]
  docs/adr/arquivo/0013-eixo-de-leitura-defasagem-e-como-medi-la.md · relation: conceptually_related_to

## Knowledge Gaps
- **92 isolated node(s):** `CapacityModel`, `Operator (Writing Origin)`, `Lease Expiry (Writing Origin)`, `OVERCOMMITTED State`, `OPTIMISTIC Concurrency Strategy` (+87 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `resource-service (ADR-0011)` and `Projeção Assíncrona (Modelo de Leitura)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What connects `CapacityModel`, `Operator (Writing Origin)`, `Lease Expiry (Writing Origin)` to the rest of the system?**
  _92 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Architecture Decision Records` be split into smaller, more focused modules?**
  _Cohesion score 0.10160427807486631 - nodes in this community are weakly interconnected._
- **Should `Plano do Laboratório` be split into smaller, more focused modules?**
  _Cohesion score 0.08712121212121213 - nodes in this community are weakly interconnected._
- **Should `resource-service` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `json-schema.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._