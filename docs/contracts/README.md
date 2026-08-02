# Contratos

O que atravessa uma fronteira de processo, formalizado como esquema.

## Estado: nenhum contrato existe

Não há `openapi/` nem `asyncapi/` neste diretório, e a ausência é deliberada.

Um contrato é criado **quando a interface existir**, e nenhuma existe:

| Contrato                         | Por que não existe                                                                                                  | Gatilho que o cria                |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| OpenAPI                          | nenhuma API HTTP foi exposta; a forma da fronteira entre a interface web e o Lab Plane não foi decidida (`Q-INT-1`) | a primeira rota HTTP escrita      |
| AsyncAPI                         | não há mensageria; o RabbitMQ entra na etapa 5, e exchanges, filas e roteamento não foram decididos                 | o primeiro experimento assíncrono |
| JSON Schema do relatório         | o relatório atravessa para a interface web e para `docs/experiments/`, e nenhum documento fixa a forma dele         | o primeiro relatório emitido      |
| DDL de `resource` e `allocation` | as colunas existem como prosa no ADR-0002; não há migração nem esquema executável (`Q-INT-5`)                       | a primeira migração escrita       |

**Um diretório vazio não é criado antecipadamente.** Uma pasta `openapi/` sem conteúdo
afirma que existem APIs a documentar, e a afirmação seria falsa. O repositório já pagou
por esse erro uma vez: o esqueleto de `services/` com cinco pastas de nome de dono foi
apagado justamente porque afirmava uma propriedade que não existia ([
`../plano-do-laboratorio.md`](../plano-do-laboratorio.md):723-726).

## Quando um contrato for criado

**A estrutura.** `contracts/openapi/<nome>.yaml` e `contracts/asyncapi/<nome>.yaml`, um
arquivo por interface.

**O que o contrato carrega, e o Markdown não repete.** Operações, autenticação e
autorização, payloads, respostas, erros, paginação, filtros, idempotência e política de
compatibilidade. O Feature Card faz link; ele não descreve de novo.

**Para eventos, o contrato distingue comando de evento de domínio**, e declara produtor,
consumidores conhecidos, tópico ou fila, chave de particionamento, versão, correlação,
idempotência, ordenação, retry, DLQ e garantia de entrega — **cada um apenas quando
houver evidência ou decisão explícita**. Um campo preenchido por analogia com outro
projeto é invenção.

**Evolução backward-compatible.** Um contrato publicado não muda de forma incompatível
sem que os consumidores sejam identificados e o impacto declarado.

**Exemplos realistas e esquemas validados.** Um contrato que não valida não é contrato.

## O que existe hoje no lugar de contrato

| Fronteira                            | Onde está descrita                                                                                                                                           | Forma                                                  |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| esquema de `resource` e `allocation` | [`../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md`](../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md):87-99                                             | prosa                                                  |
| conteúdo do relatório de execução    | [`../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md`](../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md):104-122 | prosa e tabela                                         |
| endereço de fronteira                | [`../adr/0001-o-passo-como-unidade-de-execucao.md`](../adr/0001-o-passo-como-unidade-de-execucao.md):176-187                                                 | prosa                                                  |
| manifests de entrega                 | ADR 0017 do `homelab-infrastructure`                                                                                                                         | Kustomize, **e o diretório `deploy/` não existe aqui** |

Ver [`../architecture/integrations.md`](../architecture/integrations.md) para a matriz
completa e a separação entre fato e hipótese.
