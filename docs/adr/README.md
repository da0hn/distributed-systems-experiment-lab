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

> **Nenhum ADR foi aceito.** Todos estão em debate, um a um. Um ADR só muda para
> `Aceito` depois de revisado e aprovado explicitamente.
>
> Os ADRs 0001 e 0002 chegaram a ser marcados como `Aceito` e **voltaram a `Proposto`**.
> Objeções posteriores atingiram os dois: o ADR-0001 colide com o ADR-0005 na questão de
> quem é dono de qual tabela, e o eixo de leitura que o ADR-0001 declara como tema de
> estudo não tem instrumento que o meça (questão 2 do ADR-0004). Aceitar por antiguidade
> seria aceitar por omissão.

| #                                                                   | Título                                                      | Estado   | Etapa |
|---------------------------------------------------------------------|-------------------------------------------------------------|----------|-------|
| [0001](0001-dominio-generico-com-invariante-unica.md)               | Domínio genérico de recursos com invariante única           | Proposto | 0     |
| [0002](0002-quatro-origens-de-escrita.md)                           | Quatro origens de escrita com semânticas distintas          | Proposto | 0     |
| [0003](0003-estrategias-de-concorrencia-plugaveis.md)               | Estratégias de concorrência plugáveis                       | Proposto | 1     |
| [0004](0004-experiment-como-entidade-de-primeira-classe.md)         | Experiment como entidade de primeira classe                 | Proposto | 4     |
| [0005](0005-monorepo-com-reactor-unico.md)                          | Monorepo com reactor Maven único e `shared/` apenas técnico | Proposto | 0     |
| [0006](0006-hexagonal-com-archunit.md)                              | Arquitetura hexagonal com ArchUnit como guarda executável   | Proposto | 1     |
| [0007](0007-outbox-e-inbox.md)                                      | Transactional Outbox e Inbox como base de integração        | Proposto | 2     |
| [0008](0008-motor-de-workflow-proprio-com-profundidade-maxima-2.md) | Motor de workflow próprio com profundidade máxima 2         | Proposto | 5     |
| [0009](0009-dois-executores-plugaveis-para-o-motor-de-workflow.md)  | Dois executores plugáveis para o motor de workflow          | Proposto | 5     |
| [0010](0010-plataforma-local-com-profiles-do-docker-compose.md)     | Plataforma local com profiles do Docker Compose             | Proposto | 0     |
| [0011](0011-decomposicao-em-servicos-e-fronteiras-transacionais.md) | Decomposição em serviços e fronteiras transacionais         | Proposto | 0     |
| [0012](0012-onde-o-chaos-service-intercepta.md)                     | Onde o Chaos Service intercepta sem contaminar              | Proposto | 3     |
| [0013](0013-eixo-de-leitura-defasagem-e-como-medi-la.md)            | O eixo de leitura: defasagem, CQRS e como medi-la           | Proposto | —     |

## Processo de debate

Os ADRs são debatidos **um por um**. Nenhum é aceito por omissão.

O contexto da conversa é limpo a cada ADR refinado. Por isso vale uma regra dura:

> **Nada que importa pode existir apenas na conversa.**

Toda objeção levantada durante o debate é escrita na seção **`## Questões em aberto`**
do próprio ADR, no mesmo momento em que é levantada. Um ADR sem questões em aberto está pronto para ser aceito. Um ADR com questões em aberto está
bloqueado por elas.

Quando o ADR é aceito, a seção `## Questões em aberto` é removida e o que foi decidido passa para `## Decisão` ou `## Consequências`.

### Onde o debate parou

Os ADRs 0008 a 0013 foram **rascunhados de uma vez**, em paralelo, e nenhum foi debatido. Eles entram na fila como qualquer outro. Um rascunho não é
uma decisão.

| ADR  | Situação                                                                         |
|------|----------------------------------------------------------------------------------|
| 0001 | Reaberto. Colide com o ADR-0005 sobre quem é dono de `resource` e `allocation`.  |
| 0002 | Reaberto. Depende do ADR-0011 para saber onde cada origem escreve.               |
| 0003 | Três questões em aberto; a terceira depende do ADR-0011.                         |
| 0004 | Aguardando. Duas questões: o veredito de dois eixos e o eixo de leitura ausente. |
| 0005 | Aguardando. Três questões em aberto; a terceira colide com o ADR-0001.           |
| 0006 | Aguardando. Três questões próprias; além disso, 0011 e 0012 mexem nas regras.    |
| 0007 | Aguardando.                                                                      |
| 0008 | Rascunho. Quatro questões. Reivindica `expires_at` e substituir o 0001.          |
| 0009 | Rascunho. Cinco questões; a primeira bloqueia a Etapa 5.                         |
| 0010 | Rascunho. Cinco questões. Não pode ser aceito antes do 0011.                     |
| 0011 | **Próximo a debater.** Rascunho, quatro questões. Desbloqueia 0003, 0005 e 0010. |
| 0012 | Rascunho. Seis questões. Colide com o 0010 na nomenclatura do relógio.           |
| 0013 | Rascunho. Seis questões. Nenhuma bloqueia a Etapa 1.                             |

### Tensões entre os rascunhos

Os seis foram escritos sem se ver. Três pontos de atrito já são visíveis e precisam de resolução no debate, não no código:

1. **A tabela de regras do ADR-0006 é reescrita por dois ADRs diferentes.** O 0011 divide a regra 4 em 4a e 4b; o 0012 divide a regra 6 em 6a, 6b e
   6c. As duas reescritas não se contradizem, mas nenhuma das duas viu a outra, e a tabela final precisa ser consolidada em um lugar só.
2. **O 0010 e o 0012 divergem no nome do deslocamento de relógio.** O 0010 injeta
   `LAB_CLOCK_OFFSET_MS`; o 0012 escolheu `clock.offset-millis` **de propósito**, porque sua regra 6c proíbe o Control Plane de ler propriedade sob o
   prefixo `lab.`. No binding relaxado do Spring, `LAB_CLOCK_OFFSET_MS` resolve para `lab.clock.offset-ms`
   — exatamente o que a 6c proíbe. A colisão é silenciosa: nada falha, e a regra 6c nasce violada pela plataforma.
3. **`convergence.seconds` fica ambíguo.** O 0002 usa o nome para convergência do estado; o 0013 registra que o mesmo nome serviria para convergência
   de leitura. São fenômenos distintos com sujeitos distintos e não podem dividir a métrica.

**Dívida declarada:** a origem Lease Expiry (ADR-0002) exige `expires_at` em
`allocation`, campo que o ADR-0001 não tem. O rascunho do ADR-0008 reivindica ser o ADR que o adiciona, e com isso reivindica **substituir o
ADR-0001**. Isso só vale se o 0008 for aceito; enquanto isso, a dívida continua aberta.

**Colisão declarada:** o ADR-0001 verifica a invariante numa transação que toca
`resource` e `allocation`. O ADR-0005 proíbe um serviço de ler a tabela de outro. As duas decisões só coexistem se os dois agregados pertencerem ao
mesmo serviço — e nenhum ADR decidiu isso. O ADR-0011 resolve a colisão. Ele precisa vir **antes** do parent POM e antes de qualquer código da Etapa
1. Ver a questão 3 do ADR-0005 e a questão 3 do ADR-0003.

**Lacuna declarada — o Chaos Service não tem lugar.** O ADR-0004 exige duplicata, reordenação e atraso semeados. A regra 6 do ADR-0006 proíbe o
Control Plane de importar o Lab Plane. Interceptar dentro do processo é o modo fiel e contaminante; interceptar no broker é isolado e adiciona
latência à própria medida; interceptar na rede é puro e não produz duplicata semântica. O rascunho do ADR-0012 propõe uma resposta. Ver a questão 3 do
ADR-0006.

**Lacuna declarada — o laboratório só mede escrita.** As quatro origens do ADR-0002 são origens de escrita, e as asserções do ADR-0004 são consultas
sobre o estado final. Uma leitura desatualizada não sobrevive até o estado final: ela é um valor que era falso no instante em que foi lido. Hoje um
experimento de CQRS concluiria "nenhuma violação" num cenário em que o usuário viu dado errado o tempo inteiro. O rascunho do ADR-0013 propõe uma
resposta. Ver a questão 2 do ADR-0004.

**Ordem sugerida de debate.** O ADR-0011 vem primeiro: ele é o único cuja resposta muda o conteúdo dos outros. Os rascunhos 0008, 0009 e 0010 declaram
dependência explícita dele, e o 0010 diz que não pode ser aceito antes. Debater qualquer um deles antes do 0011 é retrabalho garantido.

## Template

Use [`0000-template.md`](0000-template.md).
