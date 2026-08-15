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

O broker, o Debezium Server e os manifests de entrega ainda não existem na árvore.

**A árvore é a única fonte do que existe.** Rode `git ls-files` e leia `pom.xml`,
`compose.yaml` e `frontend/package.json`. O que falta definir está no
[BACKLOG.md](BACKLOG.md).

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

## Documentação

**Três arquivos governam o repositório, e são só estes três:**

| Arquivo                  | O que ele é                                          |
|--------------------------|------------------------------------------------------|
| [AGENTS.md](AGENTS.md)   | as regras de trabalho, para pessoas e para agentes   |
| [BACKLOG.md](BACKLOG.md) | as pendências de definição, em tópicos de alto nível |
| este `README.md`         | o que o projeto é e como rodá-lo                     |

O [CLAUDE.md](CLAUDE.md) apenas importa o `AGENTS.md`, para que o repositório permaneça
agnóstico de agente.

**`docs/` é histórico congelado.** Aquele diretório foi escrito sob um processo de
especificação que não vale mais, e boa parte dele descreve comportamento que nunca foi
implementado. Não o trate como contrato, não o mantenha sincronizado com o código e não o
cite como evidência. Quando ele contradisser a árvore, a árvore está certa.

**O código é a documentação.** Documento novo só nasce quando uma pessoa pedir por um.
