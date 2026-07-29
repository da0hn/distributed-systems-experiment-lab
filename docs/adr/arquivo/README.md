# Arquivo — primeira série de ADRs

Estes treze documentos são a **primeira série de ADRs** do repositório, arquivada em
2026-07-28. Nenhum deles foi aceito.

## Convenção de citação

A numeração foi reiniciada. Um número existe duas vezes no repositório, em séries
diferentes, e as duas séries **não se referem à mesma decisão**.

| Forma de citar | Onde vive           | O que é                                     |
|----------------|---------------------|---------------------------------------------|
| `arquivo/0001` | `docs/adr/arquivo/` | primeira série, arquivada, nenhuma em vigor |
| `ADR-0001`     | `docs/adr/`         | série corrente                              |

Um documento desta pasta que cite "ADR-0002" está citando `arquivo/0002`. As referências
cruzadas internas foram preservadas como estavam escritas.

## Por que foram arquivados

Eles não estão errados. Eles respondem a uma pergunta que mudou.

A primeira série foi construída sobre esta pergunta:

> Quanto custa proteger uma invariante de capacidade sob concorrência, e o que muda
> quando ela é distribuída entre serviços?

O replanejamento de 2026-07-28 trocou a pergunta central por outra:

> Como construir um instrumento que reproduza, observe e compare os fenômenos
> conhecidos de sistemas distribuídos?

As duas se sobrepõem, mas não coincidem. Três divergências tornaram a primeira série
insustentável como está:

1. **A invariante deixou de ser o centro.** Oito dos quarenta e dois fenômenos do escopo
   novo dependem de uma invariante de domínio. Os outros trinta e quatro acontecem igual
   em qualquer domínio.
2. **A decomposição em cinco serviços deixou de ser premissa.** O `arquivo/0011`
   agenda a separação de fronteira; o escopo novo exige que ela seja provocada por um
   experimento que falha sem ela.
3. **O determinismo subiu de prioridade.** O `arquivo/0004` afirma que a semente não
   torna o sistema determinístico. O escopo novo exige barreiras artificiais que tornem
   uma race condition reproduzível por construção.

O inventário do que sobreviveu e do que colidiu está em
[`docs/plano-do-laboratorio.md`](../../plano-do-laboratorio.md), seção 10.

## Por que continuam no repositório

Pela seção `## Alternativas consideradas`.

O raciocínio que descarta uma alternativa é a parte cara de um ADR, e ela não caduca
junto com a decisão. Três exemplos que a série corrente vai precisar reaproveitar:

- `arquivo/0001` demonstra por que verificar uma invariante por contador materializado e
  por soma derivada produz **duas famílias de anomalia diferentes**, e por que
  optimistic locking é inerte no segundo caso.
- `arquivo/0011` enumera o custo exato de mover uma tabela de fronteira depois que o
  sistema já existe, e argumenta contra dividir no dia zero.
- `arquivo/0012` mapeia os três lugares onde um injetor de falha pode interceptar, e o
  que cada um contamina.

Um documento arquivado que preserva um argumento vale mais que um documento apagado.

## Índice

| #                                                                   | Título                                             | Estado ao arquivar       |
|---------------------------------------------------------------------|----------------------------------------------------|--------------------------|
| [0001](0001-dominio-generico-com-invariante-unica.md)               | Domínio genérico de recursos com invariante única  | Proposto                 |
| [0002](0002-quatro-origens-de-escrita.md)                           | Quatro origens de escrita com semânticas distintas | Proposto                 |
| [0003](0003-estrategias-de-concorrencia-plugaveis.md)               | Estratégias de concorrência plugáveis              | Proposto                 |
| [0004](0004-experiment-como-entidade-de-primeira-classe.md)         | Experiment como entidade de primeira classe        | Proposto                 |
| [0005](0005-monorepo-com-reactor-unico.md)                          | Monorepo com reactor Maven único                   | Proposto                 |
| [0006](0006-hexagonal-com-archunit.md)                              | Arquitetura hexagonal com ArchUnit                 | Proposto                 |
| [0007](0007-outbox-e-inbox.md)                                      | Transactional Outbox e Inbox                       | Proposto                 |
| [0008](0008-motor-de-workflow-proprio-com-profundidade-maxima-2.md) | Motor de workflow próprio                          | Rascunho, nunca debatido |
| [0009](0009-dois-executores-plugaveis-para-o-motor-de-workflow.md)  | Dois executores plugáveis                          | Rascunho, nunca debatido |
| [0010](0010-plataforma-local-com-profiles-do-docker-compose.md)     | Plataforma local com profiles do Compose           | Rascunho, nunca debatido |
| [0011](0011-decomposicao-em-servicos-e-fronteiras-transacionais.md) | Decomposição em serviços                           | Rascunho, nunca debatido |
| [0012](0012-onde-o-chaos-service-intercepta.md)                     | Onde o Chaos Service intercepta                    | Rascunho, nunca debatido |
| [0013](0013-eixo-de-leitura-defasagem-e-como-medi-la.md)            | O eixo de leitura e como medi-la                   | Rascunho, nunca debatido |

## Regra

**Nenhum documento desta pasta é editado.** Ele registra o que se pensava em 2026-07-28
e continua registrando isso. Uma correção feita aqui apagaria a única coisa que o
arquivo tem a oferecer.
