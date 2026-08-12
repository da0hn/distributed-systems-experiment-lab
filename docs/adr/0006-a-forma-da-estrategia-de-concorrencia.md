# ADR-0006: A forma da estratégia de concorrência — contrato plugável e calibração

- **Estado:** Aceito
- **Data:** 2026-08-01
- **Etapa:** 2
- **Relacionado:** depende do ADR-0002 (R3, calibração) e do ADR-0005 (término). Não
  substitui nem subsume nenhum ADR aceito.
- **Fecha:** [`Q-0001-2`](../questions/Q-0001-2.md), [`Q-0005-1`](../questions/Q-0005-1.md).

- **Última atualização:** 2026-08-11
- **Errata:** a citação `README.md`, linhas 515-539, na seção `## Contexto`, quebrou em
  2026-08-03, quando o índice encolheu de 908 para 517 linhas. A seção citada era
  `### Q-0001-2`, extraída para
  [`../questions/Q-0001-2.md`](../questions/Q-0001-2.md). Decisão `C-6`, em
  `arquivo/proposta-2026-08-03/decisoes-pendentes.md`. **A citação foi consertada em
  2026-08-07**, pelo patch registrado no fim deste arquivo; esta errata permanece como
  registro do período em que o defeito não tinha conserto.

## Contexto

O ADR-0002 fixou o domínio e parou antes da estratégia: "quem a acrescenta é o ADR de
estratégias de concorrência"
([ADR-0002, `## Decisão`](0002-o-dominio-minimo-e-os-dois-oraculos.md#decisão)),
atribuindo a esta decisão três pontos: colunas, calibração e retry (linhas 283-297).

O ADR-0005 definiu **término** como o instante em que um worker para de tentar, "por
commit final, por resposta negativa da estratégia a 'há outra tentativa?', ou por falha
não recuperada por ela" (`0005-a-forma-do-escalonador.md:19-21`);
[`Q-0005-1`](../questions/Q-0005-1.md) diz que o critério de "falha não recuperada"
pertence a esta decisão. [`Q-0001-2`](../questions/Q-0001-2.md) pede o espelho do
controle negativo: uma estratégia cujas coincidências DEVEM ser exatamente zero. O
enunciado dela foi extraído do índice para aquele arquivo em 2026-08-03.

O plano nomeia quatro estratégias para o E3 — `NONE`, `ATOMIC_UPDATE`, `OPTIMISTIC`,
`PESSIMISTIC` (`plano-do-laboratorio.md:428-429`) — e registra que `PESSIMISTIC` "zera
as próprias coincidências e recebe `protegido` sem execução de controle"
(`plano-do-laboratorio.md:437-438`), pois o lock torna a intercalação inalcançável, sem
dizer o que isso exige do Lab Plane, nem qual estratégia calibra.

**Duas coisas têm o mesmo nome.** No Control Plane, a estratégia é a composição de
passos de `increment`, SQL diferente por estratégia (o ADR-0001 já tornou o corpo do
passo opaco). No Lab Plane, é um rótulo na declaração do experimento; escalonador,
oráculo e classificação do zero já foram decididos sem saber de estratégia nenhuma.
`plano-do-laboratorio.md:434`: "que a estratégia é um dado, não uma branch" — o segundo
sentido; o primeiro já está decidido em outro lugar.

## Problema

**O que muda no Lab Plane quando a estratégia muda, o que cada estratégia contrata com o
esquema e com o retry, e qual delas calibra?**

Forças em conflito:

- Neutralidade: Lab Plane que ramifique esconde o bug de uma estratégia.
- Reuso: escalonador, oráculo e classificação do zero não mudam por estratégia.
- Honestidade: calibração "sem perda" exige argumento técnico.
- Extensibilidade: estratégia nova se encaixa sem alterar o Lab Plane.

## Decisão

O Lab Plane trata a estratégia como **rótulo opaco de configuração do experimento**: ele
seleciona qual implementação de `increment` roda no Control Plane, e nada mais. Nenhum
componente do Lab Plane — escalonador, oráculo, contador de coincidências, classificador
do zero — DEVE inspecionar esse rótulo ou ramificar por ele.

Cada estratégia contrata três coisas: **composição de passos**, já decidida pelo
ADR-0001; **colunas adicionais** (`OPTIMISTIC` exige `version` em `Resource`; a migração
nasce no mesmo commit que introduz a estratégia, quando a arquitetura mínima existir —
fila, posição 10; `Q-INT-5`); e **critério de retry** — responde "há outra tentativa?" a
partir da exceção recebida do banco, no vocabulário de término do ADR-0005. O runtime
consulta a resposta; não a calcula.

Uma exceção que a estratégia não reconhecer como recuperável DEVE receber resposta
**não**: falha fechada, não tenta de novo por omissão. Fecha
[`Q-0005-1`](../questions/Q-0005-1.md) no nível do contrato; qual exceção cada uma
reconhece é comportamento observável, no Feature Card
[`deteccao-de-atualizacao-perdida`](../features/deteccao-de-atualizacao-perdida/feature-card.md).
**O contrato NÃO DEVE usar timeout de parede** — uma falha sistêmica (ex.: conexão
recusada) já não é reconhecida por nenhuma estratégia, e recebe **não** de imediato.

### `PESSIMISTIC` é a estratégia de controle positivo

Coincidências DEVEM ser zero em toda execução, pois o lock impede a janela de existir.
Uma violação aponta para o banco ou fabricação no instrumento, nunca para a estratégia.
Fecha [`Q-0001-2`](../questions/Q-0001-2.md).

### `ATOMIC_UPDATE` é a estratégia de calibração

Um único `UPDATE ... SET value = value + 1` satisfaz o ADR-0002 R3 sem coordenação de
aplicação: o PostgreSQL serializa toda escrita concorrente na linha. Não há janela entre
ler e escrever, pois não há leitura.

## Justificativa

**Rótulo opaco** — a separação Control Plane / Lab Plane existe para que um bug do
instrumento não vire resultado de consistência
([ADR-0002, `## Justificativa`](0002-o-dominio-minimo-e-os-dois-oraculos.md#justificativa));
um Lab Plane que ramifique por estratégia vira quatro instrumentos com o mesmo nome.
**Coluna só quando o código existir** — migração sem tabela para alterar não tem efeito
verificável, o mesmo adiamento que o ADR-0002 aceitou para o domínio inteiro.
**Retry é da estratégia** — o ADR-0005 já delega "há outra tentativa?" a ela; centralizar
a lista de exceções no runtime obrigaria toda estratégia nova a editar o Lab Plane.

**`PESSIMISTIC` controle positivo** — só ele impede a *janela*, não só o *resultado*
errado; as outras três podem ter janela aberta e resultado certo, o que a execução de
controle do ADR-0004/0005 verifica.

**Por que `ATOMIC_UPDATE`, e não `PESSIMISTIC`, calibra.** O `UPDATE` avalia `value + 1`
contra o valor corrente da linha dentro do próprio statement, sob o lock que ele mesmo
adquire — não há leitura separada da escrita, logo nenhuma janela para uma segunda
tentativa "roubar" um valor obsoleto. `PESSIMISTIC` também é zero-perda, mas via `SELECT
... FOR UPDATE` seguido de `UPDATE`: dois statements e um lock que o código da operação
adquire e libera. Uma calibração que falhasse com `PESSIMISTIC` teria causa ambígua — o
contador do Lab Plane, ou um bug no manejo do lock. Com `ATOMIC_UPDATE` a atomicidade
vem do PostgreSQL, não de código escrito aqui: uma falha só pode apontar o instrumento.

**Por que sem timeout de parede.** O ADR-0005 já fixou o princípio vizinho: "a
desistência é imediata, e não por timeout — timeout mede tempo de parede, proibido fora
de um adaptador de relógio" (`0005-a-forma-do-escalonador.md:121-123`). A falha fechada
por padrão é mais forte que um timeout: falha no primeiro sintoma, sem esperar `T`
segundos. Quantas vezes `OPTIMISTIC` tenta de novo sob exceção que **reconhece** já tem
dono — [`Q-0003-8`](../questions/Q-0003-8.md), encaminhada para `Experiment` — e esta
decisão não o duplica.

## Consequências

### Positivas

- Lab Plane reutilizável entre as quatro estratégias;
  [`Q-0001-2`](../questions/Q-0001-2.md) e [`Q-0005-1`](../questions/Q-0005-1.md) fecham
  sem esperar a arquitetura mínima; a calibração do ADR-0002 R3 ganha procedimento.

### Negativas

- Toda estratégia nova implementa o contrato de retry, mesmo trivial; a resposta padrão
  "não" PODE mascarar um bug de classificação em vez de falhar ruidosamente.

### Neutras

- `JVM_LOCK` não é avaliado aqui, ver `## Quando esta decisão deixa de valer`.

## Trade-offs

- O benefício **Lab Plane neutro a estratégia** foi aceito em troca do custo **toda
  estratégia nova implementa o mesmo contrato de retry, mesmo trivial**.
- O benefício **calibração isolada do mecanismo de qualquer estratégia** foi aceito em
  troca do custo **`PESSIMISTIC`, também zero-perda, não pode calibrar**.

## Alternativas consideradas

### Alternativa A — branch por estratégia no escalonador ou no oráculo

O Lab Plane inspeciona o rótulo e ajusta comportamento — pula a execução de controle
quando o rótulo for `PESSIMISTIC`. **Descartada** — acopla o Lab Plane à identidade de
cada estratégia, e um bug do runtime nesse `if` vira resultado de consistência.

### Alternativa B — lista global de exceções retryable no runtime

Tabela mapeia `SQLSTATE` para "tenta de novo". **Descartada** — a mesma exceção
significa coisas diferentes por estratégia: unicidade é esperada sob `OPTIMISTIC` e bug
sob `ATOMIC_UPDATE`.

### Alternativa C — `PESSIMISTIC` como estratégia de calibração

**Descartada** — mistura o mecanismo sob teste com o de verificação; argumento completo
em `## Justificativa`.

### Alternativa D — operação única, SQL condicional por estratégia

Template emitindo `FOR UPDATE` ou `version` conforme a estratégia. **Descartada** —
contradiz o ADR-0001: o runtime NÃO DEVE gerar SQL.

## Quando esta decisão deixa de valer

Reveja quando `JVM_LOCK` exigir mecanismo que o contrato de três pontos não descreva —
garantia que dependa do número de instâncias, não do SQL. Sinal: a etapa 4 ganha gatilho
(`plano-do-laboratorio.md:362-364`).

## Patches aplicados

O regime de patch está em [`README.md`](README.md#a-revogação-da-imutabilidade-decidida-em-2026-08-07).
Um patch conserta citação, caminho ou erro material; ele NÃO DEVE alterar a decisão nem o
argumento que a sustentava.

| Data       | Seção do corpo     | O que mudou                                                                             | Por quê                                                                                                                                                                                                                                                                                                                                     |
|------------|--------------------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-08-07 | `## Contexto`      | a citação `README.md`, linhas 515-539, passou a apontar para `../questions/Q-0001-2.md` | a seção `### Q-0001-2` foi extraída do índice em 2026-08-03 e a citação apontava além do fim do arquivo; a errata do cabeçalho a nomeava sem poder consertá-la                                                                                                                                                                              |
| 2026-08-11 | `## Contexto`      | `0002-o-dominio-minimo-e-os-dois-oraculos.md:94-95` virou âncora `#decisão`             | a frase citada entre aspas — "quem a acrescenta é o ADR de estratégias de concorrência" — vive em `## Decisão` do ADR-0002. O intervalo caía nas forças em conflito de `## Problema`, e caía lá **antes** do deslocamento de dez linhas que o commit do ADR-0015 somou: a deriva é cumulativa, e o número nunca voltaria a alcançar a frase |
| 2026-08-11 | `## Justificativa` | `ADR-0002:344-349` virou âncora `#justificativa`                                        | o argumento citado — a separação existe para que um bug do instrumento não vire resultado de consistência — vive em `## Justificativa` do ADR-0002, hoje em `:375`. O intervalo caía no parágrafo do `sucessos` no denominador, que é outro argumento                                                                                       |

A entrada correspondente saiu de
[`citations-baseline.txt`](../../scripts/citations-baseline.txt) no mesmo commit.
