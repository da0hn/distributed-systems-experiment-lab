# Graph Report - D:\Code\Personal\distributed-consistency-lab  (2026-08-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 178 nodes · 203 edges · 26 communities (19 shown, 7 thin omitted)
- Extraction: 83% EXTRACTED · 12% INFERRED · 5% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f275569c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Architecture Decision Records Index
- Scheduling Language Concepts
- Core Execution Primitives
- Workflow Engine Internals
- Resource Concurrency Model
- Experiment Design Questions
- Pedagogical Experiment Roadmap
- Platform Service Decomposition
- Concurrency Phenomena Taxonomy
- Artifact Limit Checker
- Chaos Engineering Adapters
- Control Plane Entities
- Lab Runtime Architecture
- Specification Artifacts
- Allocation Service Projections
- ADR Process Conventions
- Messaging Contract Guards
- Reliable Messaging Patterns
- Infrastructure Planning Archive
- Authoritative Read Control
- Homelab Infrastructure ADR
- Experiment Definition Designer
- Specification First Principle
- Barrier Concept
- Increment Operation
- Declaration Rule R4

## God Nodes (most connected - your core abstractions)
1. `ADR-0004: O Estatuto da Barreira e o Diagnóstico da Não Ocorrência` - 15 edges
2. `ADR-0003: A linguagem do agendamento` - 11 edges
3. `Capacidades do Laboratório` - 10 edges
4. `ADR-0002: O Domínio Mínimo e os Dois Oráculos` - 9 edges
5. `Experiment` - 8 edges
6. `Índice de ADRs` - 7 edges
7. `Feature Card: Detecção da Atualização Perdida (E1 e E3)` - 7 edges
8. `ADR-0001: O Passo como Unidade de Execução` - 6 edges
9. `resource-service` - 6 edges
10. `Taxonomia dos 42 Fenômenos` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Regra Pedagógica: Problema → Causa → Solução → Trade-off` --conceptually_related_to--> `Roadmap de 12 Etapas`  [INFERRED]
  CLAUDE.md → docs/plano-do-laboratorio.md
- `Q-0003-1 Worker Unreachability` --conceptually_related_to--> `Experiment`  [AMBIGUOUS]
  docs/adr/README.md → docs/adr/arquivo/0004-experiment-como-entidade-de-primeira-classe.md
- `Q-0003-2 Scheduling on Missing Attempt` --conceptually_related_to--> `Experiment`  [AMBIGUOUS]
  docs/adr/README.md → docs/adr/arquivo/0004-experiment-como-entidade-de-primeira-classe.md
- `Q-0004-4 Stop Rule vs. Continuous Delivery` --conceptually_related_to--> `Experiment`  [AMBIGUOUS]
  docs/adr/README.md → docs/adr/arquivo/0004-experiment-como-entidade-de-primeira-classe.md
- `Q-0004-8 Confidence Limit Independence Assumption` --conceptually_related_to--> `Experiment`  [AMBIGUOUS]
  docs/adr/README.md → docs/adr/arquivo/0004-experiment-como-entidade-de-primeira-classe.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Arquitetura de Separação dos Planos** — docs_plano_do_laboratorio_runtime, docs_plano_do_laboratorio_control_plane, docs_plano_do_laboratorio_lab_plane, docs_plano_do_laboratorio_fault_injection [EXTRACTED 1.00]
- **Taxonomia dos 42 Fenômenos por Causa** — docs_plano_do_laboratorio_taxonomia, docs_plano_do_laboratorio_grupo_a, docs_plano_do_laboratorio_grupo_b, docs_plano_do_laboratorio_grupo_c, docs_plano_do_laboratorio_grupo_d, docs_plano_do_laboratorio_grupo_e [EXTRACTED 1.00]
- **MVP com Quatro Experimentos Fundacionais** — docs_plano_do_laboratorio_mvp, docs_plano_do_laboratorio_experimento_e1, docs_plano_do_laboratorio_experimento_e3, docs_plano_do_laboratorio_experimento_e5, docs_plano_do_laboratorio_oraculo_exato, docs_plano_do_laboratorio_oraculo_predicado [EXTRACTED 1.00]
- **Conceitos fundamentais do modelo de execução do ADR-0001** — docs_adr_0001_o_passo_como_unidade_de_execucao_step, docs_adr_0001_o_passo_como_unidade_de_execucao_boundary, docs_adr_0001_o_passo_como_unidade_de_execucao_attempt, docs_adr_0001_o_passo_como_unidade_de_execucao_operation, docs_adr_0001_o_passo_como_unidade_de_execucao_transaction_scope [EXTRACTED 1.00]
- **Componentes do plano de controle do runtime** — docs_adr_0001_o_passo_como_unidade_de_execucao_scheduler, docs_adr_0001_o_passo_como_unidade_de_execucao_barrier, docs_adr_0001_o_passo_como_unidade_de_execucao_fault_injector, docs_adr_0001_o_passo_como_unidade_de_execucao_boundary [EXTRACTED 1.00]
- **Modelo de domínio mínimo do ADR-0002** — docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos_resource, docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos_allocation, docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos_exact_oracle, docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos_predicate_oracle [EXTRACTED 1.00]
- **Vocabulário da linguagem de agendamento** — docs_adr_0003_a_linguagem_do_agendamento_evento, docs_adr_0003_a_linguagem_do_agendamento_papel, docs_adr_0003_a_linguagem_do_agendamento_carga, docs_adr_0003_a_linguagem_do_agendamento_encontro, docs_adr_0003_a_linguagem_do_agendamento_restricao_de_precedencia [EXTRACTED 0.95]
- **Fluxo de classificação do resultado zero** — docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_controle_negativo, docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_controle_positivo, docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_coincidencia, docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_janela_de_exposicao, docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia_classificacao_do_zero [EXTRACTED 0.95]
- **Série corrente de ADRs do laboratório** — docs_adr_0001_o_passo_como_unidade_de_execucao, docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos, docs_adr_0003_a_linguagem_do_agendamento, docs_adr_0004_o_estatuto_da_barreira_e_o_diagnostico_da_nao_ocorrencia [EXTRACTED 1.00]
- **Distinct Writing Origins for a Single Invariant** — docs_adr_arquivo_0002_operator, docs_adr_arquivo_0002_agent, docs_adr_arquivo_0002_reconciler, docs_adr_arquivo_0002_lease_expiry [EXTRACTED 1.00]
- **Group 1 Mutual Exclusion Strategies** — docs_adr_arquivo_0003_optimistic, docs_adr_arquivo_0003_concurrencystrategy [EXTRACTED 0.90]
- **Core Domain Model Definition** — docs_adr_arquivo_0001_resource, docs_adr_arquivo_0001_capacitymodel, docs_adr_arquivo_0001_invariant [EXTRACTED 1.00]
- **Transição para Invariante Distribuída na Etapa 5** — docs_adr_arquivo_0011_resource_service, docs_adr_arquivo_0011_allocation_service, docs_adr_arquivo_0008_workflow_engine, docs_adr_arquivo_0008_placementsaga [EXTRACTED 1.00]
- **Plataforma Local e Contrato de Versão** — docs_adr_arquivo_0010_docker_compose, docs_adr_arquivo_0010_compose_profiles, docs_adr_arquivo_0010_versions_env, docs_adr_arquivo_0010_service_manifest [EXTRACTED 1.00]
- **Execução de Workflow Plugável** — docs_adr_arquivo_0009_step_executor, docs_adr_arquivo_0009_sync_in_process, docs_adr_arquivo_0009_async_message, docs_adr_arquivo_0009_stepoutcomesink [EXTRACTED 1.00]
- **Mecanismos de Injeção de Falha (ADR-0012)** — docs_adr_arquivo_0012_onde_o_chaos_service_intercepta_chaos_relay, docs_adr_arquivo_0012_onde_o_chaos_service_intercepta_toxiproxy, docs_adr_arquivo_0012_onde_o_chaos_service_intercepta_adaptador_de_relogio [EXTRACTED 1.00]
- **Componentes do Eixo de Leitura (ADR-0013)** — docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_observer, docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_leitura_autoritativa, docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_projecao_assincrona, docs_adr_arquivo_0013_eixo_de_leitura_defasagem_e_como_medi_la_outbox_adr_0007 [EXTRACTED 1.00]
- **MVP Oracles and Experiments** — docs_features_deteccao_de_atualizacao_perdida_feature_card, docs_features_deteccao_de_protecao_inerte_feature_card, docs_features_execucao_de_experimento_feature_card, concept_oracle_lost_update, concept_oracle_protection_inertness [INFERRED 0.85]
- **ADR-0002 as Normative Source for Feature Rules** — docs_adr_0002_o_dominio_minimo_e_os_dois_oraculos, docs_features_deteccao_de_atualizacao_perdida_feature_card, docs_features_deteccao_de_protecao_inerte_feature_card, docs_plano_do_laboratorio [INFERRED 0.90]
- **Ciclo de execução de experimento** — docs_features_execucao_de_experimento_feature_card_execucao_de_um_experimento, docs_features_execucao_de_experimento_feature_card_r3, docs_features_execucao_de_experimento_feature_card_r4, docs_features_execucao_de_experimento_feature_card_r8, docs_features_execucao_de_experimento_feature_card_r9, docs_features_execucao_de_experimento_feature_card_r14 [EXTRACTED 1.00]
- **Reuso do oráculo do predicado no experimento E5** — docs_features_deteccao_de_protecao_inerte_feature_card_oraculo_do_predicado, docs_features_deteccao_de_protecao_inerte_feature_card_experimento_e5, docs_features_deteccao_de_protecao_inerte_feature_card_allocate [EXTRACTED 0.95]

## Communities (26 total, 7 thin omitted)

### Community 0 - "Architecture Decision Records Index"
Cohesion: 0.11
Nodes (27): Skill: /feature-planning, Lab Plane, Oracle for Lost Update Detection, Oracle for Inert Protection Detection, ADR-0001: O Passo como Unidade de Execução, ADR-0001: Passo como Unidade de Execução, Observação e Injeção de Falha, ADR-0002: O Domínio Mínimo e os Dois Oráculos, Índice de ADRs (+19 more)

### Community 1 - "Scheduling Language Concepts"
Cohesion: 0.18
Nodes (20): ADR-0003: A linguagem do agendamento, Carga (declaração de papéis de uma execução), Encontro (forma curta de agendamento), Evento (chegada e travessia numa fronteira), Papel (nome com cardinalidade), Restrição de precedência (A antes de B), ADR-0004: O Estatuto da Barreira e o Diagnóstico da Não Ocorrência, Chave de contenção (+12 more)

### Community 2 - "Core Execution Primitives"
Cohesion: 0.13
Nodes (16): Tentativa (Attempt), Fronteira (Boundary), Injetor de Falha (Fault Injector), Cláusula de Honestidade (Honesty Clause), Operação (Operation), Escalonador (Scheduler), Passo (Step), Corpo do Passo (Step Body) (+8 more)

### Community 3 - "Workflow Engine Internals"
Cohesion: 0.15
Nodes (14): Tabela allocation (schema revisado), Coluna deadline_at, Invariante de Motor Verificável por SQL, EvictionSaga, Mecanismo de Idempotency Key, PlacementSaga, Tabela saga_instance, Tabela saga_step (+6 more)

### Community 4 - "Resource Concurrency Model"
Cohesion: 0.17
Nodes (12): CapacityModel, Unique Invariant, Resource (Aggregate), Agent (Writing Origin), Lease Expiry (Writing Origin), Operator (Writing Origin), OVERCOMMITTED State, Reconciler (Writing Origin) (+4 more)

### Community 5 - "Experiment Design Questions"
Cohesion: 0.18
Nodes (11): Experiment, Experiment Report, Q-0002-3 Final Quiescent State, Q-0002-4 Initial State Management, Q-0003-1 Worker Unreachability, Q-0003-2 Scheduling on Missing Attempt, Q-0003-3 Experiment Equality Criteria, Q-0003-8 N Definition vs. Retry (+3 more)

### Community 6 - "Pedagogical Experiment Roadmap"
Cohesion: 0.25
Nodes (9): Regra Pedagógica: Problema → Causa → Solução → Trade-off, ADR-0002: Domínio Mínimo e Oráculo Exato, Experimento E1: Lost Update (Grupo de Controle), Experimento E3: Comparação de Estratégias, Experimento E5: Write Skew com Proteção Inerte, MVP do Laboratório, Oráculo Exato (Contagem de Perdas), Oráculo de Predicado sobre Conjunto (+1 more)

### Community 7 - "Platform Service Decomposition"
Cohesion: 0.22
Nodes (9): Docker Compose Profiles, docker-compose.yml, Manifesto de Serviços (platform/services.yaml), platform/versions.env, chaos-service, experiment-service, registry-service, resource-service (+1 more)

### Community 8 - "Concurrency Phenomena Taxonomy"
Cohesion: 0.29
Nodes (7): ADR-0004: Estatuto da Barreira e Diagnóstico da Não-Ocorrência, Grupo A: Intercalação, Grupo B: Entrega, Grupo C: Escrita Parcial, Grupo D: Saturação, Grupo E: Posse no Tempo, Taxonomia dos 42 Fenômenos

### Community 9 - "Artifact Limit Checker"
Cohesion: 0.67
Nodes (5): default_limit(), main(), parse_limit(), resolve_inside(), Path

### Community 10 - "Chaos Engineering Adapters"
Cohesion: 0.47
Nodes (6): experiment-service (ADR-0011), Adaptador de Relógio, Chaos Relay, chaos-service (ADR-0012), Toxiproxy, Observer (ADR-0013)

### Community 11 - "Control Plane Entities"
Cohesion: 0.40
Nodes (5): Allocate Operation, Allocation Entity, Control Plane, Increment Operation, Resource Entity

### Community 12 - "Lab Runtime Architecture"
Cohesion: 0.40
Nodes (5): Control Plane (Sistema sob Teste), Injeção de Falha em Pontos Nomeados, Lab Plane (Instrumento de Medida), Observação Passo a Passo, Runtime do Laboratório

### Community 13 - "Specification Artifacts"
Cohesion: 0.40
Nodes (5): ADR, BDD (behavior.feature), Contrato (Contract), Example Mapping, Feature Card

### Community 14 - "Allocation Service Projections"
Cohesion: 0.50
Nodes (4): allocation-service (ADR-0011), resource-service (ADR-0011), Transactional Outbox (ADR-0007), Projeção Assíncrona (Modelo de Leitura)

### Community 15 - "ADR Process Conventions"
Cohesion: 0.67
Nodes (3): Processo de ADR, Template de ADR, Convenções de ADR

### Community 16 - "Messaging Contract Guards"
Cohesion: 0.67
Nodes (3): Shared Module (lab-messaging-contract), ArchUnit Guard, Q-0004-2 Contention Key Guard

### Community 17 - "Reliable Messaging Patterns"
Cohesion: 0.67
Nodes (3): Idempotent Inbox, Transactional Outbox, Q-0004-3 Comparable Timestamps

### Community 18 - "Infrastructure Planning Archive"
Cohesion: 0.67
Nodes (3): Série Arquivada de ADRs, ArgoCD (homelab-infrastructure), Replanejamento de 2026-07-28

## Ambiguous Edges - Review These
- `Experiment` → `Q-0003-1 Worker Unreachability`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Experiment` → `Q-0003-2 Scheduling on Missing Attempt`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Experiment` → `Q-0004-4 Stop Rule vs. Continuous Delivery`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Experiment` → `Q-0004-8 Confidence Limit Independence Assumption`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Operator (Writing Origin)` → `Q-0002-2 Oracle Termination Observer`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Experiment Report` → `Q-0002-3 Final Quiescent State`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Experiment Report` → `Q-0003-3 Experiment Equality Criteria`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Experiment Report` → `Q-0004-5 Third Verdict Format`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `ArchUnit Guard` → `Q-0004-2 Contention Key Guard`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `Transactional Outbox` → `Q-0004-3 Comparable Timestamps`  [AMBIGUOUS]
  docs/adr/README.md · relation: conceptually_related_to
- `resource-service (ADR-0011)` → `Projeção Assíncrona (Modelo de Leitura)`  [AMBIGUOUS]
  docs/adr/arquivo/0013-eixo-de-leitura-defasagem-e-como-medi-la.md · relation: conceptually_related_to

## Knowledge Gaps
- **62 isolated node(s):** `ADR-0001: Passo como Unidade de Execução, Observação e Injeção de Falha`, `Lab Plane (Instrumento de Medida)`, `Injeção de Falha em Pontos Nomeados`, `Observação Passo a Passo`, `Convenções de ADR` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Experiment` and `Q-0003-1 Worker Unreachability`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Experiment` and `Q-0003-2 Scheduling on Missing Attempt`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Experiment` and `Q-0004-4 Stop Rule vs. Continuous Delivery`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Experiment` and `Q-0004-8 Confidence Limit Independence Assumption`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Operator (Writing Origin)` and `Q-0002-2 Oracle Termination Observer`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Experiment Report` and `Q-0002-3 Final Quiescent State`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Experiment Report` and `Q-0003-3 Experiment Equality Criteria`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._