# Architecture Decision Records

Decisões de arquitetura do Distributed Systems Experiment Lab.

## O que é um ADR

Um ADR registra uma decisão de arquitetura e o motivo dela. Um ADR não é documentação de código. O código mostra *o que* o sistema faz. O ADR mostra
*por que* o sistema é assim, e **o que foi descartado e por quê**.

Escreva o ADR **antes** de implementar. Um ADR escrito depois vira justificativa.

## Uma decisão merece ADR quando

- possui alternativas plausíveis;
- tem impacto arquitetural duradouro;
- cria restrições futuras;
- representa um trade-off importante.

Decisão trivial não vira ADR. Escolher o nome de uma variável, a versão de patch de uma biblioteca ou o formato de um log não atende a nenhum dos
quatro critérios.

## Convenções

- Numeração sequencial de quatro dígitos. Nunca reutilize um número **dentro da série corrente**.
- Nome do arquivo: `NNNN-titulo-em-kebab-case.md`. Template em
  [`0000-template.md`](0000-template.md).
- Idioma: português do Brasil, com acentuação correta. Frases curtas. Voz ativa. Uma ideia por frase. Linhas quebradas manualmente em ~88 colunas.
- A seção `## Alternativas consideradas` costuma valer mais que a `## Decisão`. Cada alternativa leva um parágrafo começando com `**Descartada.**` e
  um motivo **técnico**. Não construa espantalhos: se a alternativa tem argumento legítimo a favor, reconheça-o e mostre por que perde.
- `## Quando esta decisão deixa de valer` precisa de um sinal concreto e observável, não de uma intenção vaga.
- Sem emojis. Sem linguagem de marketing.

## Duas séries, e como citá-las

A numeração foi reiniciada em 2026-07-28. Existem duas séries no repositório, e um mesmo número aparece nas duas com significados diferentes.

| Forma de citar | Onde vive                       | O que é                   |
|----------------|---------------------------------|---------------------------|
| `ADR-0001`     | `docs/adr/`                     | **série corrente**        |
| `arquivo/0001` | [`docs/adr/arquivo/`](arquivo/) | primeira série, arquivada |

Use sempre o prefixo `arquivo/` ao citar a série antiga. Sem ele, a referência é ambígua.

O motivo do arquivamento e o que sobreviveu estão em
[`arquivo/README.md`](arquivo/README.md) e em
[`../plano-do-laboratorio.md`](../plano-do-laboratorio.md), seção 10.

## Estados

| Estado          | Significado                                           |
|-----------------|-------------------------------------------------------|
| `Proposto`      | A decisão está em discussão.                          |
| `Aceito`        | A decisão está em vigor.                              |
| `Substituído`   | Um ADR mais recente substitui esta decisão.           |
| `Descontinuado` | A decisão não se aplica mais. Nenhum ADR a substitui. |

## Índice

**Nenhum ADR foi escrito na série corrente.**

O planejamento está em [`../plano-do-laboratorio.md`](../plano-do-laboratorio.md). Ele **não decide nada** — é a análise que define quais decisões
precisam ser tomadas e em que ordem.

## Processo de debate

Os ADRs são debatidos **um por um**. Nenhum é aceito por omissão, e nenhum é aceito sem aprovação explícita.

O contexto da conversa é limpo a cada ADR refinado. Por isso vale uma regra dura:

> **Nada que importa pode existir apenas na conversa.**

Toda objeção levantada durante o debate é escrita na seção `## Questões em aberto` do próprio ADR, **no mesmo turno em que é levantada**, antes de
responder ou perguntar qualquer outra coisa. Uma objeção que fica só no chat desaparece no próximo compact, em silêncio.

Um ADR sem questões em aberto está pronto para ser aceito. Um ADR com questões em aberto está bloqueado por elas. Ao aceitar, a seção
`## Questões em aberto` é removida e o que foi decidido passa para `## Decisão` ou `## Consequências`.

Um ADR **aceito** nunca é editado nem apagado. Para mudar a decisão, escreva um ADR novo e marque o antigo como `Substituído por ADR-NNNN`. Enquanto
estiver `Proposto`, editar é permitido.

### A lição que a primeira série deixou

Os documentos `arquivo/0008` a `arquivo/0013` foram rascunhados **de uma vez, em paralelo**. Escritos sem se ver, produziram três contradições entre
si: duas reescritas concorrentes da mesma tabela de regras, dois nomes para o mesmo deslocamento de relógio, e uma métrica com dois significados.

Nenhum dos seis chegou a ser debatido. O custo de escrever seis ADRs em lote foi inteiramente perdido.

**Um ADR por vez. Nenhum rascunho antecipado.**

## Fila de decisões

Ordem em que as decisões precisam ser tomadas, derivada de
[`../plano-do-laboratorio.md`](../plano-do-laboratorio.md).

Os números **não** estão atribuídos. Um número é atribuído quando o ADR é escrito — atribuir antes cria buracos na sequência quando a ordem muda.

| Ordem | Decisão                                                                       | Por que precisa vir aqui                                                |
|-------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| 1     | **O passo como unidade de execução, observação e injeção de falha**           | toda outra decisão herda a forma que esta escolher (plano, seção 2)     |
| 2     | **O domínio mínimo: contador com oráculo exato mais predicado de capacidade** | define o que é medido; o oráculo exato é o que torna o MVP verificável  |
| 3     | **Estratégias de concorrência como dado, não como branch**                    | sem isso o experimento de comparação não existe                         |
| 4     | **O log de observações: forma, ordem e onde vive**                            | é o substrato da timeline agora e do replay depois                      |
| 5     | **Experiment: definição, semente, hipótese e asserções**                      | precisa resolver a tensão entre Designer na UI e definição versionada   |
| 6     | **Os dois formatos de veredito: booleano e curva**                            | se ficar para depois, o grupo D não cabe na arquitetura                 |
| 7     | **Arquitetura mínima, stack e guardas executáveis**                           | um módulo, dois planos na mesma JVM, separação imposta por teste        |
| 8     | **Entrega contínua no homelab desde o dia zero**                              | o serviço precisa nascer entregando; ratifica ou emenda a ADR 0017 lá   |

As decisões 1 e 2 destravam o MVP inteiro. As demais podem ser debatidas em paralelo ao avanço do MVP, **uma por vez**.

### A ordem das decisões 7 e 8 está sob tensão

O laboratório é entregue no cluster do
[`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure), e a exigência é que um serviço **nasça já entregando** — pipeline e CI/CD
no mesmo commit que cria o módulo, não retrofitados depois.

Isso não move a decisão 1: o formato do passo não afeta o que o pipeline empacota. Mas move as decisões 7 e 8 para **junto do primeiro módulo
compilável**, e as decisões 2 a 6 deixam de ser pré-requisito de escrever código de esqueleto. O `Dockerfile` e o `deploy/kustomization.yaml` fixam o
número de módulos e a forma do artefato — que é o conteúdo da decisão 7.

A decisão 8 tem uma particularidade que nenhuma outra tem: **parte dela já foi tomada fora deste repositório.** A ADR 0017 do homelab, aceita em
2026-07-26, escolheu Gradle, Toxiproxy e "microsserviços JVM" para este laboratório, dois dias antes do replanejamento que descartou a arquitetura de
serviços. Ratificar ou emendar é decisão consciente e explícita. O inventário completo do que sobrevive e do que colide está em
[`../plano-do-laboratorio.md`](../plano-do-laboratorio.md), seção 12.
