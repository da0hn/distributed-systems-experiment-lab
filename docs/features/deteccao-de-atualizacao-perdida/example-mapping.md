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
2026-08-06. O
[`ADR-0015`](../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#as-colunas-de-tempo-e-a-fonte-do-relógio-por-papel-do-valor)
passou a ser o dono normativo destas duas colunas, no lado medido; esta seção é
ilustração dela, não fonte.

`created_at` e `updated_at` existem em `resource` e `allocation`, quem as preenche é a
aplicação pelo adaptador de relógio, e **a escrita que esquecer uma delas falha alto** em
vez de gravar um instante plausível e errado. A **forma** das duas colunas não é descrita
aqui — ela vive em
[`esquemas.md`](../../architecture/esquemas.md#o-que-o-diagrama-do-sut-não-desenha).

A objeção que a decisão não dissolveu é pedagógica, e vira regra escrita porque não é
executável:

> **Nenhuma estratégia de concorrência lê `updated_at`.** A coluna é metadado de
> auditoria. `UPDATE resource SET value = ? WHERE id = ? AND updated_at = ?` é optimistic
> locking escrito sem a palavra, e o E1 encontraria pronta metade da solução que ele deve
> construir do zero. A estratégia `OPTIMISTIC` introduz a sua própria coluna de versão,
> no ADR que a definir, depois de o experimento ter mostrado o problema.

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
