# Distributed Systems Experiment Lab

Plataforma experimental para reproduzir, observar e comparar problemas de sistemas
distribuídos. Não é uma aplicação de negócio: o laboratório cria condições controladas,
mede o sistema sob teste e explica o resultado de cada execução.

A regra pedagógica é simples:

> PROBLEMA → CAUSA → SOLUÇÃO → TRADE-OFF

A solução nunca entra antes de o problema ser observável e reproduzível.

## Estado atual

O repositório já possui um esqueleto executável, mas ainda não reproduz nenhum fenômeno.
Ele compila, empacota e sobe localmente com PostgreSQL; não há regras de negócio,
tabelas de domínio ou consumidor de CDC implementados.

O broker, o Debezium Server e o diretório `deploy/` são decisões ou pendências de
arquitetura que ainda não existem na árvore.

Na entrega, o GitHub Actions publica as imagens no GHCR com tag igual ao SHA do
commit, e nenhum Secret vive neste repositório. Os manifests Kustomize de `deploy/`,
que o ArgoCD do homelab espera, ainda não existem: o pipeline está parcialmente
implementado e bloqueado por essa decisão. A fonte para saber o que está implementado,
decidido ou aberto é a
[matriz de integrações](docs/architecture/integrations.md#matriz).

## Módulos e serviços presentes

Os módulos do reactor Maven, declarados em `pom.xml`:

| Módulo              | Papel                                                   |
|---------------------|---------------------------------------------------------|
| `shared`            | biblioteca compartilhada; não gera imagem               |
| `lab-plane`         | instrumento que coordena a execução e produz o veredito |
| `lab-journal`       | caderno de laboratório e leitura de observações         |
| `system-under-test` | sistema medido pelos experimentos                       |

Fora do reactor, o Compose ainda sobe:

| Componente  | Papel                                      |
|-------------|--------------------------------------------|
| `frontend/` | interface React, em contêiner próprio      |
| PostgreSQL  | banco local do Compose; não é módulo Maven |

A separação entre o sistema medido e o instrumento é uma decisão arquitetural; a
topologia decidida e suas lacunas estão nos
[ADRs da série corrente](docs/adr/README.md#índice).

## Executar localmente

Pré-requisitos: Java 25, Maven, Docker e Node.js para o frontend.

```bash
mvn verify
docker compose up --build
npm --prefix frontend run build
```

Esses comandos verificam o esqueleto; eles não executam experimentos de consistência
ainda.

## Como navegar pela documentação

| Para entender                                 | Leia                                                                                                                     |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| Mapa e ordem de leitura                       | [Documentação](docs/README.md#em-que-ordem-ler)                                                                          |
| Taxonomia, dependências pedagógicas e roadmap | [Plano do laboratório](docs/plano-do-laboratorio.md#1-o-que-mudou-e-por-que-o-planejamento-anterior-não-serve-como-está) |
| Decisões arquiteturais aceitas e pendentes    | [Índice de ADRs](docs/adr/README.md#índice) e [fila de decisões](docs/adr/fila-de-decisoes.md#o-que-esta-fila-enfileira) |
| Capacidades já especificadas                  | [Feature Cards](docs/features/README.md#índice)                                                                          |
| Fronteiras entre processos e seu estado       | [Matriz de integrações](docs/architecture/integrations.md#matriz)                                                        |
| Processo, aprovações e artefatos              | [Processo de especificação](docs/specification-process.md#a-decisão-vem-antes-do-artefato)                               |
| Perguntas encaminhadas                        | [Índice de questões](docs/questions/README.md#índice)                                                                    |
| Contratos formais e seus gatilhos             | [Contratos](docs/contracts/README.md#estado-nenhum-contrato-existe)                                                      |
| Vocabulário vigente                           | [Glossário](docs/CONTEXT.md#linguagem)                                                                                   |

O plano organiza o estudo, os ADRs registram decisões duráveis e os Feature Cards
descrevem comportamento. Quando houver divergência, a decisão aceita e a configuração
versionada prevalecem sobre resumos de onboarding.

## Para agentes e contribuidores

As regras operacionais do repositório estão em [AGENTS.md](AGENTS.md). O
[CLAUDE.md](CLAUDE.md) apenas roteia para essa mesma fonte, para que o repositório
permaneça agnóstico de agente.

Antes de propor uma mudança de comportamento, siga o
[processo de especificação](docs/specification-process.md#a-decisão-vem-antes-do-artefato).
Antes de alterar arquitetura, consulte os ADRs e a fila; não crie uma decisão para
fechar uma lacuna sem aprovação humana.
