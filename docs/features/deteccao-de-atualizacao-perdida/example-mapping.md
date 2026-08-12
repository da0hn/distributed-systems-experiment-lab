# Example Mapping — Detecção da atualização perdida

Companheiro de [`feature-card.md`](feature-card.md). Regras do
[`ADR-0002`](../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md) e do
[`ADR-0006`](../../adr/0006-a-forma-da-estrategia-de-concorrencia.md), ambos `Aceito`, e
da seção 6 do [`plano-do-laboratorio.md`](../../plano-do-laboratorio.md).

## História

> Como quem estuda concorrência, preciso saber **quantos** incrementos se perderam e sob
> qual proteção, para "às vezes perde" deixar de ser a única frase disponível.

## Regras e exemplos

### R2 a R4 — Esquema sem `version`, identidade da semente

- O E1 roda sem coluna de versão — o ponto pedagógico. O esboço do ADR-0001 lê `version`
  numa coluna inexistente; fixa forma, não é normativo.
- A semente `42` produz sempre o mesmo identificador (replay da etapa 12), e por isso
  também colide com as linhas da execução anterior
  ([`Q-0002-4`](../../questions/Q-0002-4.md)). Um `SERIAL` quebraria essa igualdade,
  tornando o identificador função da ordem de inserção.

### R5 a R9 — O oráculo e o denominador

- 100 incrementos, 10 workers: `commits = 100`, `value_final = 63`, `perdidas = 37`.
- Uma operação que commita, falha e tenta de novo incrementa **duas** vezes; contar por
  operação esconderia o segundo incremento.
- Uma tentativa que alcança `AFTER_COMMIT` e falha depois **entra** em `commits` e
  **não** em `sucessos`; uma que esgota tentativas sem alcançar a fronteira não entra em
  nenhum dos dois.
- Com `sucessos` no denominador, uma perda real seria cancelada por falha injetada depois
  do commit (`commits = 100`, `sucessos = 94`: os 6 são dual write, não perda), e o
  relatório ficaria verde sobre um banco inconsistente (**contraexemplo**).
- Derivar `value_final` do **log de observações** mediria o instrumento com o instrumento
  (**contraexemplo**). O
  [`ADR-0010`](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md)
  retomou o mecanismo por outro caminho, e o contraexemplo continua de pé: o WAL é escrito
  pelo **sistema medido**, e o log de observações pelo instrumento. O `SELECT` cruzado,
  que era a alternativa aqui, deixou de existir.

### R10 e R11 — O grupo de controle, e uma conexão por worker

- `value` final igual a 100 sob 100 incrementos: carga insuficiente, nenhum resultado do
  E3 sobre a mesma carga significa algo (**erro**).
- Um pool de 5 conexões com 10 workers serializa metade; a anomalia não aparece, e o
  relatório diz "protegido" errado (**falso negativo silencioso**).

**As duas regras trocaram de evidência em 2026-08-12, e uma delas encolheu.** As duas
citavam o [plano](../../plano-do-laboratorio.md#3-taxonomia-refinada), e o plano
[não decide nada](../../../AGENTS.md#o-que-este-projeto-é) — a citação afirmava decisão
onde só havia análise. `R10` passou a citar o
[ADR-0004](../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-zero-é-classificado-e-a-classificação-tem-quatro-valores),
que é o dono dela: a ordem 1 da tabela de quatro valores diz que o controle negativo que
não viola produz veredito `inválido`, e é exatamente isso que `R10` enuncia em prosa.
`R11` passou a citar o
[guardrail da raiz](../../../AGENTS.md#regras-estruturais-que-valem-sempre), e **perdeu a
oração "e isso DEVE ser verificado, não presumido"**: nenhum documento diz quem verifica
nem quando, e uma regra aprovada não pode carregar exigência sem dono. A oração vive
agora só como `P5`, abaixo. Nem `R10` nem `R11` mudaram de conteúdo — mudou de onde
elas vêm.

### E3 — A estratégia é um dado, não uma branch

- **Exemplo E3.1** — A mesma carga roda quatro vezes: `NONE` perde; `ATOMIC_UPDATE`,
  `OPTIMISTIC`, `PESSIMISTIC` chegam a 100, `OPTIMISTIC` pagando em taxa de aborto e
  `PESSIMISTIC` em espera de lock — a tabela precisa das duas colunas.

### R12 a R16 — O contrato de estratégia (ADR-0006)

- **E3.4, calibração** — `ATOMIC_UPDATE` calibra: `commits` iguala `value_final −
  value_inicial`, pois o `UPDATE` é a única operação sobre a linha, sem leitura antes.
- **E3.5/E3.6, controle positivo** — `PESSIMISTIC` roda sem execução de controle:
  coincidências sempre zero, pois o lock torna a janela inalcançável; uma violação
  aponta para o banco ou fabricação no instrumento, nunca para a estratégia.
- **E3.7/E3.8, retry** — Cada estratégia responde "há outra tentativa?" a partir da
  exceção recebida; `OPTIMISTIC` reconhece `version` divergente como recuperável, e uma
  exceção não reconhecida recebe **não** — falha fechada.

### R19 — `updated_at` não entra em nenhuma decisão de estratégia

- **Exemplo** — `OPTIMISTIC` decide "há outra tentativa?" (R13) só a partir da exceção
  que o banco devolve, sem consultar `updated_at`; a mesma semente, replayada em
  instantes de parede diferentes, produz o mesmo padrão de retry.
- **Contraexemplo, o optimistic locking sem o nome** — uma estratégia gravasse
  `UPDATE resource SET value = ? WHERE id = ? AND updated_at = ?`, comparando o
  `updated_at` lido antes do cálculo com o valor da linha no momento do `UPDATE`: a
  atualização perdida deixaria de ocorrer, mas por um mecanismo de versionamento que o
  card ainda não decidiu construir — a seção dedicada abaixo,
  ["`updated_at` existe no esquema, e nenhuma estratégia pode
  lê-la"](#updated_at-existe-no-esquema-e-nenhuma-estratégia-pode-lê-la), detalha por
  que R19 proíbe exatamente isso.

## Perguntas em aberto

| #   | Pergunta                                                          | Origem                                    |
|-----|-------------------------------------------------------------------|-------------------------------------------|
| P2  | Quem estabelece o estado inicial entre execuções?                 | [`Q-0002-4`](../../questions/Q-0002-4.md) |
| P4  | O oráculo lê o estado quiescente. E violação transitória?         | [`Q-0002-3`](../../questions/Q-0002-3.md) |
| P5  | R11 exige pool maior que workers — quem verifica, e quando?       | nova                                      |
| P6  | `capacity` existe, `increment` não a lê — intencional?            | nova                                      |
| P7  | Três estratégias podem empatar em taxa zero — o que isso conclui? | [`Q-0004-5`](../../questions/Q-0004-5.md) |
| P8  | A proibição de derivar de stream alcança `value_final`?           | nova, com o `ADR-0010`                    |
| P9  | A emissão ao vivo entra na janela medida — usar buffer local?     | nova, com o `ADR-0010`                    |
| P10 | Um experimento de clock skew pode ler `updated_at` como insumo?   | nova, com as decisões de 2026-08-06       |

P1 e P3 foram respondidas por R14/R15 do ADR-0006, `Aceito`.

### `updated_at` existe no esquema, e nenhuma estratégia pode lê-la

**Esta seção entrou aqui em 2026-08-07**, a partir de duas decisões fechadas em
2026-08-06, e foi **corrigida em 2026-08-12** pelo fecho de
[`E-76`](../../adr/fila-de-decisoes.md#e-76-fecha-em-a-regra-desce-para-o-feature-card-escolhida-em-2026-08-12).
O dono normativo de `created_at`/`updated_at` como colunas do esquema continua o
[`ADR-0015`](../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#as-colunas-de-tempo-e-a-fonte-do-relógio-por-papel-do-valor).
Mas a proibição de uma estratégia ler `updated_at` — R19 — nunca foi decidida por aquele
ADR: ele mesmo cita a regra como sendo de
[`E-25`](../../adr/fila-de-decisoes.md#e-25--timestamps-nas-tabelas-medidas), "não do
fecho de `E-27`". O fecho de `E-76` desceu a regra e o argumento pedagógico de `E-25`
para este card, que **passa a hospedar a redação de referência dos dois** — a poda do
corpo de `E-25` na fila deixa de estar travada com este commit, e é trabalho de um
commit separado da sessão principal.

`created_at` e `updated_at` existem em `resource` e `allocation`, quem as preenche é a
aplicação pelo adaptador de relógio, e **a escrita que esquecer uma delas falha alto** em
vez de gravar um instante plausível e errado. A **forma** das duas colunas não é descrita
aqui — ela vive em
[`schemas/sut.md`](../../architecture/schemas/sut.md#o-que-o-diagrama-do-sut-não-desenha).

**A transcrição abaixo é fiel ao corpo de `E-25`**, e não uma paráfrase — é o texto que
sustenta R19, aprovado por pessoa em 2026-08-06:

> A objeção mais forte não é técnica, é pedagógica. `updated_at` é um token de versão
> clássico — `UPDATE resource SET value = ? WHERE id = ? AND updated_at = ?` é optimistic
> locking escrito sem a palavra. A regra do AGENTS.md manda introduzir o problema antes da
> solução, e é exatamente por isso que `version` não está no esquema. A coluna entrega de
> graça metade do que o E1 deve construir do zero.
>
> — [`E-25`, timestamps nas tabelas medidas](../../adr/fila-de-decisoes.md#e-25--timestamps-nas-tabelas-medidas)

A estratégia `OPTIMISTIC` introduz a sua própria coluna de versão, no ADR que a definir,
depois de o experimento ter mostrado o problema — e não lendo `updated_at` emprestada.

Ela é da mesma natureza das três regras que [`Q-0002-1`](../../questions/Q-0002-1.md)
registra como texto sem guarda, e é **mais fácil de violar sem perceber**: a coluna estará
lá, preenchida, e o código que a lê parecerá inocente.

**A pressão de P10 é real e não é contradição hoje.** O grupo E estuda clock skew, e o
insumo natural de um experimento assim é uma coluna de tempo escrita pela aplicação, com
relógio que o experimento desloca. Se `updated_at` for esse insumo, ela deixa de ser
metadado inerte. A regra acima fala de **estratégia de concorrência**, e não de oráculo
nem de experimento — não há contradição hoje, e há pressão amanhã.

## Adiado de propósito

| Item                                             | Gatilho                                    |
|--------------------------------------------------|--------------------------------------------|
| Migração da coluna `version`                     | a decisão de arquitetura mínima            |
| Nível de isolamento como parâmetro               | o E5, que varre três níveis                |
| SQL exato de cada estratégia; mapa exceção→retry | código existir; `ADR-0006` fixa o contrato |

## O que não virou cenário, e por quê

R1 é estrutural e vira `Contexto`. R12 (rótulo opaco) descreve o Lab Plane por dentro,
não comportamento externo. R13 a R15 ainda não entraram em `behavior.feature` — esse
arquivo já excede o próprio limite (débito anterior), e fica para uma passada dedicada.

R19, embora deixe de ser `pendente` nesta rodada, também não ganha cenário aqui. Quem a
aprovou foi a **pessoa**, em 2026-08-06, no fecho de
[`E-25`](../../adr/fila-de-decisoes.md#e-25--timestamps-nas-tabelas-medidas)
— e não o ciclo de redação, que só a transportou para cá. O escopo desse transporte
fechou em card e Example Mapping, e não tocou `behavior.feature`: R19 é candidata à
próxima passada dedicada, junto de R13 a R15.
