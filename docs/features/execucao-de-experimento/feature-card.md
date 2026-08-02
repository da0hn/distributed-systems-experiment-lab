# Feature Card — Execução de um experimento e classificação do veredito

Estado: `especificado, não implementado` · Origem: [`ADR-0004`](../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md), `Aceito`

## Problema e resultado esperado

Zero violações não diz nada por si. O zero tem quatro causas com a mesma aparência: a
anomalia é impossível ali; a janela nunca abriu; a carga não gerou concorrência; ou a
janela foi declarada errada. A primeira é conhecimento, as outras três são defeito do
instrumento.

Resultado esperado: todo veredito é **classificado**, e a plataforma recusa reportar como
proteção o zero que não é proteção.

## Atores e gatilho

Quem monta o experimento declara carga, `N`, janela e estratégia. O runtime conta commits,
violações e coincidências. O oráculo lê o banco depois da quiescência.

## Escopo

O ciclo de quatro execuções. O `N` declarado antes. As taxas de violação e de aborto. O
limite superior do zero. A janela de exposição e a contagem de coincidências. A
classificação do zero. A barreira como controle positivo.

## Fora de escopo

O veredito em **formato curva** (E4) não tem forma decidida — ver
[`README.md`](../README.md). Estratégias, nível de isolamento e estado inicial entre
execuções estão na fila.

## Regras de negócio

| # | Regra | Evidência |
|---|---|---|
| R1 | A execução medida roda **sem agendamento**. O agendamento **NÃO DEVE** produzir o resultado reportado. | ADR-0004:100-102 |
| R2 | Um experimento tem quatro execuções: calibração, controle negativo, medida e controle positivo. Só a última tem agendamento. | ADR-0003:150-152 |
| R3 | Na calibração, `commits` **DEVE** igualar `value_final − value_inicial`. Divergindo, a plataforma **DEVE** recusar o relatório. | ADR-0002:177-182 |
| R4 | `N` **DEVE** ser declarado antes. A execução **NÃO DEVE** parar na primeira violação nem prosseguir além de `N`. | ADR-0004:126-128 |
| R5 | O veredito é `violações / commits`. O relatório **DEVE** exibir as três contagens, e **NÃO DEVE** exibir apenas a razão. | ADR-0004:112-113 |
| R6 | O relatório **DEVE** exibir a taxa de aborto, `(N − commits) / N`. | ADR-0004:115-117 |
| R7 | Com zero violações, o relatório **DEVE** declarar o limite superior a 95%, em torno de `3 / commits`. **NÃO DEVE** ser calculado sobre `N`. | ADR-0004:119-122 |
| R8 | Um experimento cujo veredito **PODE** ser zero **DEVE** declarar a janela `(F_abre, F_fecha)`. | ADR-0004:132-135 |
| R9 | O runtime **DEVE** contar coincidências em **toda** execução, derivadas do log. O sistema sob teste **NÃO DEVE** participar. | ADR-0004:159-169 |
| R10 | Janelas sobrepostas com chaves de contenção diferentes **NÃO DEVEM** contar como coincidência. | ADR-0004:191-199 |
| R11 | A plataforma **NÃO DEVE** comparar contagens de execuções cuja carga declarada diferir. | ADR-0004:187-189 |
| R12 | Com zero violações, a plataforma **DEVE** classificar pela tabela de cinco condições, **na ordem**. `inválido`, `janela mal declarada` e `exposição insuficiente` **NÃO DEVEM** ser reportados como proteção. | ADR-0004:204-221 |
| R13 | O controle positivo roda com zero violações **e** coincidências próprias maiores que zero. Ele **NÃO DEVE** ser reportado como resultado. | ADR-0004:246-258 |
| R14 | Um experimento cujo veredito **PODE** ser zero **DEVE** rodar em alta resolução. | ADR-0004:278-282 |

O ciclo em diagrama está no [Example Mapping](example-mapping.md).

## Integrações e contratos afetados

O relatório atravessa para a interface web e para `docs/experiments/`. **Nenhum contrato o
formaliza** — `Q-INT-1` em [`integrations.md`](../../architecture/integrations.md).

## Riscos e decisões pendentes

| Questão | O que está em jogo |
|---|---|
| `Q-0004-8` | o limite `3/commits` pressupõe independência que as tentativas não têm |
| `Q-0004-4` | `N` alto ocupa o runner; `N` baixo produz falha intermitente no pipeline |
| `Q-0004-5` | a taxa com incerteza é um terceiro formato de veredito |
| `Q-0002-2` | quem declara o fim da execução, e se o oráculo lê antes ou depois |
| `Q-0004-2` | nada obriga o passo a reportar a chave de contenção que R10 consome |

O [`ADR-0003`](../../adr/0003-a-linguagem-do-agendamento.md) está `Proposto`, questão 4 em
`aberto (crítico)`. Referência aqui, não regra estabilizada.

## Critérios de pronto

R3 a R14 verificadas por teste. Um veredito `inválido`, `janela mal declarada` ou
`exposição insuficiente` é recusado como evidência de proteção. A ordem de avaliação é
testada com um caso em que duas condições casam ao mesmo tempo.

## Links

[Example Mapping](example-mapping.md) · [BDD](behavior.feature) ·
[`ADR-0004`](../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md)
