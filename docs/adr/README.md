# Architecture Decision Records

Este diretório contém as decisões de arquitetura do Distributed Consistency Lab.

## O que é um ADR

Um ADR registra uma decisão de arquitetura e o motivo dela. Um ADR não é documentação de código. O código mostra *o que* o sistema faz. O ADR mostra
*por que* o sistema é assim, e *quais alternativas foram descartadas*.

Escreva o ADR **antes** de implementar. Um ADR escrito depois vira justificativa.

## Convenções

- Numeração sequencial de quatro dígitos. Nunca reutilize um número.
- Nome do arquivo: `NNNN-titulo-em-kebab-case.md`.
- Idioma: português. Frases curtas. Voz ativa. Uma ideia por frase.
- Um ADR nunca é apagado ou editado depois de aceito. Para mudar uma decisão, escreva um ADR novo e marque o antigo como `Substituído por ADR-NNNN`.

## Estados

| Estado          | Significado                                           |
|-----------------|-------------------------------------------------------|
| `Proposto`      | A decisão está em discussão.                          |
| `Aceito`        | A decisão está em vigor.                              |
| `Substituído`   | Um ADR mais recente substitui esta decisão.           |
| `Descontinuado` | A decisão não se aplica mais. Nenhum ADR a substitui. |

## Índice

> **Nenhum ADR foi aceito ainda.** Todos estão em debate, um a um. Um ADR só muda para
> `Aceito` depois de revisado e aprovado explicitamente.

| #                                                           | Título                                                      | Estado      | Etapa |
|-------------------------------------------------------------|-------------------------------------------------------------|-------------|-------|
| [0001](0001-dominio-generico-com-invariante-unica.md)       | Domínio genérico de recursos com invariante única           | Aceito      | 0     |
| [0002](0002-quatro-origens-de-escrita.md)                   | Quatro origens de escrita com semânticas distintas          | Aceito      | 0     |
| [0003](0003-estrategias-de-concorrencia-plugaveis.md)       | Estratégias de concorrência plugáveis                       | Proposto    | 1     |
| [0004](0004-experiment-como-entidade-de-primeira-classe.md) | Experiment como entidade de primeira classe                 | Proposto    | 4     |
| [0005](0005-monorepo-com-reactor-unico.md)                  | Monorepo com reactor Maven único e `shared/` apenas técnico | Proposto    | 0     |
| [0006](0006-hexagonal-com-archunit.md)                      | Arquitetura hexagonal com ArchUnit como guarda executável   | Proposto    | 1     |
| [0007](0007-outbox-e-inbox.md)                              | Transactional Outbox e Inbox como base de integração        | Proposto    | 2     |
| 0008                                                        | Motor de workflow próprio com profundidade máxima 2         | Não escrito | 5     |
| 0009                                                        | Dois executores plugáveis para o motor de workflow          | Não escrito | 5     |
| 0010                                                        | Plataforma local com profiles do Docker Compose             | Não escrito | 0     |

## Processo de debate

Os ADRs são debatidos **um por um**. Nenhum é aceito por omissão.

O contexto da conversa é limpo a cada ADR refinado. Por isso vale uma regra dura:

> **Nada que importa pode existir apenas na conversa.**

Toda objeção levantada durante o debate é escrita na seção **`## Questões em aberto`**
do próprio ADR, no mesmo momento em que é levantada. Um ADR sem questões em aberto
está pronto para ser aceito. Um ADR com questões em aberto está bloqueado por elas.

Quando o ADR é aceito, a seção `## Questões em aberto` é removida e o que foi decidido
passa para `## Decisão` ou `## Consequências`.

### Onde o debate parou

| ADR  | Situação                                                                       |
|------|--------------------------------------------------------------------------------|
| 0001 | Aceito. Uma consequência foi superada pelo ADR-0002; há nota no arquivo.        |
| 0002 | Aceito.                                                                        |
| 0003 | **Próximo a debater.** Duas questões em aberto registradas no arquivo.          |
| 0004 | Aguardando. Uma questão em aberto: o veredito binário foi superado pelo 0002.   |
| 0005 | Aguardando. Duas questões em aberto, levantadas ao criar o esqueleto.           |
| 0006 | Aguardando. Duas questões em aberto, dependentes do padrão de pacote.           |
| 0007 | Aguardando.                                                                    |

**Dívida declarada:** a origem Lease Expiry (ADR-0002) exige `expires_at` em
`allocation`, campo que o ADR-0001 não tem. Um ADR novo o adiciona na Etapa 5,
substituindo o ADR-0001.

Os ADRs 0008 a 0010 só serão escritos depois que os anteriores forem aceitos.

## Template

Use [`0000-template.md`](0000-template.md).
