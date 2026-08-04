# Architecture Decision Records

Decisões de arquitetura do Distributed Systems Experiment Lab.

## O que é um ADR

Um ADR registra uma decisão de arquitetura e o motivo dela. Um ADR não é documentação de
código. O código mostra *o que* o sistema faz. O ADR mostra *por que* o sistema é assim,
e **o que foi descartado e por quê**.

Escreva o ADR **antes** de implementar. Um ADR escrito depois vira justificativa.

## Uma decisão merece ADR quando

- possui alternativas plausíveis;
- tem impacto arquitetural duradouro;
- cria restrições futuras;
- representa um trade-off importante.

Decisão trivial não vira ADR. Escolher o nome de uma variável, a versão de patch de uma
biblioteca ou o formato de um log não atende a nenhum dos quatro critérios.

## Convenções

- Numeração sequencial de quatro dígitos. Nunca reutilize um número **dentro da série
  corrente**.
- Nome do arquivo: `NNNN-titulo-em-kebab-case.md`. O template oficial está em
  [`.claude/skills/adr/references/adr.md`](../../.claude/skills/adr/references/adr.md).
- Idioma: português do Brasil, com acentuação correta. Frases de 10 a 20 palavras. Voz
  ativa. Uma ideia por frase. Linhas quebradas manualmente em ~88 colunas.
- Um conceito tem **um** nome. Escolhido "passo", nunca alterne para "etapa", "estágio"
  ou "fase" no parágrafo seguinte.
- `## Decisão` carrega só o **quê**. O porquê vive em `## Justificativa`, e a comparação
  vive em `## Alternativas consideradas`. Quem lê anos depois precisa distinguir o que
  está em vigor do argumento que o sustentava na época.
- `## Trade-offs` é obrigatório, no formato "o benefício **X** foi aceito em troca do
  custo **Y**". Positivas e Negativas dizem o que aconteceu; o par diz o que foi trocado
  pelo quê.
- Requisito normativo usa RFC 2119 traduzida, em caixa alta: `DEVE`, `NÃO DEVE`,
  `DEVERIA`, `NÃO DEVERIA`, `PODE`. Nunca como ênfase. Um requisito escrito assim pode
  virar teste; escrito como prosa descritiva, não pode. `DEVE` marca o que a plataforma
  rejeita ou impede; `DEVERIA` marca a recomendação que alguém PODE contrariar com
  motivo.
- Palavras proibidas sem número ou fato que as sustente: `talvez`, `provavelmente`,
  `geralmente`, `normalmente`, `aproximadamente`, `adequado`, `corretamente`,
  `rapidamente`, `eficiente`, `simples`, `robusto`. Explique o motivo em vez de
  qualificar com advérbio.
- Substitua pronome ambíguo ("ele", "ela", "isso") pelo substantivo, sempre que houver
  risco de dúvida.
- A seção `## Alternativas consideradas` costuma valer mais que a `## Decisão`. Cada
  alternativa leva um parágrafo começando com `**Descartada.**` e um motivo **técnico**.
  Não construa espantalhos: se a alternativa tem argumento legítimo a favor, reconheça-o
  e mostre por que perde.
- Todo fluxo apresentado no ADR vai **também** como diagrama Mermaid, num bloco
  `mermaid` junto do parágrafo que o descreve. Use `sequenceDiagram` para troca de
  chamadas e ordem no tempo, e `flowchart` para topologia e hierarquia. A prosa e o
  diagrama descrevem o mesmo fluxo, e quem lê escolhe por onde entrar. Excalidraw serve
  ao desenho que o Mermaid não expressa; exporte para `.excalidraw.svg` ao lado do ADR,
  porque o SVG renderiza no GitHub e continua editável. Diagrama que não acrescenta nada
  à prosa fica de fora.
- `## Quando esta decisão deixa de valer` precisa de um sinal concreto e observável, não
  de uma intenção vaga.
- Sem emojis. Sem linguagem de marketing. Nada de "a melhor solução", "a solução ideal"
  ou "a abordagem moderna" — troque opinião por fato observável.

Antes de apresentar um ADR, verifique: existe **uma** decisão só? O problema está claro?
A justificativa está separada da decisão? As alternativas têm motivo de rejeição? Os
trade-offs estão explícitos? As consequências trazem custos **e** benefícios? Sobrou
palavra vaga ou linguagem opinativa? O texto continua compreensível sem conhecimento
prévio?

## Duas séries, e como citá-las

A numeração foi reiniciada em 2026-07-28. Existem duas séries no repositório, e um mesmo
número aparece nas duas com significados diferentes.

| Forma de citar | Onde vive                       | O que é                   |
|----------------|---------------------------------|---------------------------|
| `ADR-0001`     | `docs/adr/`                     | **série corrente**        |
| `arquivo/0001` | [`docs/adr/arquivo/`](arquivo/) | primeira série, arquivada |

Use sempre o prefixo `arquivo/` ao citar a série antiga. Sem ele, a referência é
ambígua.

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

| ADR                                                                      | Título                                                                 | Estado     |
|--------------------------------------------------------------------------|------------------------------------------------------------------------|------------|
| [0001](0001-o-passo-como-unidade-de-execucao.md)                         | O passo como unidade de execução, observação e injeção de falha        | `Aceito`   |
| [0002](0002-o-dominio-minimo-e-os-dois-oraculos.md)                      | O domínio mínimo: contador com oráculo exato e predicado de capacidade | `Aceito`   |
| [0003](0003-a-linguagem-do-agendamento.md)                               | A linguagem do agendamento: como uma barreira é declarada              | `Aceito`   |
| [0004](0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md) | O estatuto da barreira e o diagnóstico da não ocorrência               | `Aceito`   |
| [0005](0005-a-forma-do-escalonador.md)                                   | A forma do escalonador: estado, decisão e protocolo de desistência     | `Aceito`   |
| [0006](0006-a-forma-da-estrategia-de-concorrencia.md)                    | A forma da estratégia de concorrência: contrato plugável e calibração  | `Aceito`   |

O planejamento está em [`../plano-do-laboratorio.md`](../plano-do-laboratorio.md). Ele
**não decide nada** — é a análise que define quais decisões precisam ser tomadas e em
que ordem.

## Processo de debate

Os ADRs são debatidos **um por um**. Nenhum é aceito por omissão, e nenhum é aceito sem
aprovação explícita.

O contexto da conversa é limpo a cada ADR refinado. Por isso vale uma regra dura:

> **Nada que importa pode existir apenas na conversa.**

Toda objeção levantada durante o debate é escrita na seção `## Questões em aberto` do
próprio ADR, **no mesmo turno em que é levantada**, antes de responder ou perguntar
qualquer outra coisa. Uma objeção que fica só no chat desaparece no próximo compact, em
silêncio.

Um ADR está pronto para ser aceito quando nenhuma questão dele tem status `aberto` ou
`aberto (crítico)`. Questão com status `encaminhado` não bloqueia a aceitação — ela
pertence a outro ADR já identificado na fila. Questão com status `resolvida` também não
bloqueia: ela foi fechada durante o debate, e a subseção dela diz onde.

Ao aceitar, a seção `## Questões em aberto` é removida. O que foi decidido passa para
`## Decisão` ou `## Consequências`. Cada questão com status `encaminhado` é transportada
para um arquivo em [`docs/questions/`](../questions/README.md), **inteira e no mesmo
commit da aceitação**. Um ADR NÃO DEVE ser aceito enquanto suas questões encaminhadas não
estiverem transportadas: o enunciado se perde, e a linha da fila que o citava fica
pendurada.

Um ADR **aceito** nunca é editado nem apagado. Para mudar a decisão, escreva um ADR novo
e marque o antigo como `Substituído por ADR-NNNN`. Enquanto estiver `Proposto`, editar é
permitido.

### Substituição e subsunção são coisas diferentes

Um ADR novo que **contradiga** a decisão de um aceito o substitui. O antigo recebe
`Substituído por ADR-NNNN`, e o que ele decidiu sai de vigor.

Um ADR novo PODE, em vez disso, **subsumir** uma regra de um aceito. A subsunção
acontece quando a regra antiga continua correta no caso que ela enxergava, e o ADR novo
separa casos que ela tratava como um só. O ADR antigo permanece `Aceito`, e a regra
continua valendo com o alcance que o ADR novo lhe der.

Três exigências separam a subsunção da edição disfarçada:

- o ADR que subsume DEVE citar a regra subsumida pelo texto e pela seção de origem;
- ele DEVE dizer em que caso a regra antiga continua valendo sem mudança;
- ele NÃO DEVE contradizer a regra antiga em caso nenhum. Se contradisser, é
  substituição, e a substituição é o caminho.

O texto do ADR antigo NÃO DEVE ser tocado. Quem o lê isolado lê o que se decidiu na
época, e o índice diz quais ADRs vieram depois dele.

O custo desta emenda é que a leitura de um ADR aceito deixa de bastar por si. Uma regra
dele PODE ter alcance recortado por um documento posterior que ele não cita, porque não
existia quando ele foi escrito.

Registrado em 2026-07-31, para resolver a questão 1 do ADR-0004.

### A lição que a primeira série deixou

Os documentos `arquivo/0008` a `arquivo/0013` foram rascunhados **de uma vez, em
paralelo**. Escritos sem se ver, produziram três contradições entre si: duas reescritas
concorrentes da mesma tabela de regras, dois nomes para o mesmo deslocamento de relógio,
e uma métrica com dois significados.

Nenhum dos seis chegou a ser debatido. O custo de escrever seis ADRs em lote foi
inteiramente perdido.

**Um ADR por vez. Nenhum rascunho antecipado.**

## Fila de decisões

Ordem em que as decisões precisam ser tomadas, derivada de
[`../plano-do-laboratorio.md`](../plano-do-laboratorio.md).

Os números **não** estão atribuídos. Um número é atribuído quando o ADR é escrito —
atribuir antes cria buracos na sequência quando a ordem muda.

A coluna `Ordem` é posição na fila, e a posição muda quando uma decisão entra no meio.
**Cite uma decisão pelo nome, nunca pela posição.** Uma citação por posição continua
válida depois da inserção, e passa a apontar para outra decisão.

| Ordem | Decisão                                                                                                                          | Por que precisa vir aqui                                                                                                                                                                                                                                                    |
|-------|----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1     | **O passo como unidade de execução, observação e injeção de falha** — ADR-0001, `Aceito`                                         | toda outra decisão herda a forma que esta escolheu (plano, seção 2)                                                                                                                                                                                                         |
| 2     | **O domínio mínimo: contador com oráculo exato mais predicado de capacidade** — ADR-0002, `Aceito`                               | define o que é medido; fechou [`Q-0001-3`](../questions/Q-0001-3.md) e encaminhou quatro questões novas                                                                                                                                                                     |
| 3     | **O estatuto da barreira e o diagnóstico da não ocorrência** — ADR-0004, `Aceito`                                                | rebaixou a barreira a controle positivo, fixou a taxa como veredito e encaminhou cinco questões                                                                                                                                                                             |
| 4     | **A linguagem do agendamento: como uma barreira é declarada** — ADR-0003, `Aceito`                                               | o ADR-0001 fixa o endereço da fronteira e para aí; sem a linguagem, a execução de controle do ADR-0004 não é declarável; encaminhou quatro questões                                                                                                                         |
| 5     | **A forma do escalonador: estado, decisão e protocolo de desistência** — [ADR-0005](0005-a-forma-do-escalonador.md), `Aceito`    | consumiu o agendamento e executou a barreira; resolveu [`Q-0001-4`](../questions/Q-0001-4.md), [`Q-0002-2`](../questions/Q-0002-2.md), [`Q-0003-1`](../questions/Q-0003-1.md) e [`Q-0003-2`](../questions/Q-0003-2.md), e encaminhou [`Q-0005-1`](../questions/Q-0005-1.md) |
| 6     | **Estratégias de concorrência como dado, não como branch** — [ADR-0006](0006-a-forma-da-estrategia-de-concorrencia.md), `Aceito` | sem isso o experimento de comparação não existe; [`Q-0001-2`](../questions/Q-0001-2.md) pede o controle positivo aqui; acrescenta a coluna `version` e nomeia a estratégia de calibração do ADR-0002                                                                        |
| 7     | **O log de observações: forma, ordem e onde vive**                                                                               | é o substrato da timeline agora e do replay depois; [`Q-0001-1`](../questions/Q-0001-1.md) pede aqui a identidade da operação gravada no registro do resultado, e [`Q-0003-3`](../questions/Q-0003-3.md) o critério de igualdade entre duas execuções                       |
| 8     | **Experiment: definição, semente, hipótese e asserções**                                                                         | precisa resolver a tensão entre Designer na UI e definição versionada; [`Q-0002-4`](../questions/Q-0002-4.md) pede aqui o ciclo de vida de uma execução, e [`Q-0003-8`](../questions/Q-0003-8.md) o que `N` conta                                                           |
| 9     | **Os dois formatos de veredito: booleano e curva**                                                                               | se ficar para depois, o grupo D não cabe na arquitetura; [`Q-0002-3`](../questions/Q-0002-3.md) acrescenta o eixo pontual contra contínuo no tempo                                                                                                                          |
| 10    | **Arquitetura mínima, stack e guardas executáveis**                                                                              | um módulo, dois planos na mesma JVM, separação imposta por teste; [`Q-0002-1`](../questions/Q-0002-1.md) pede a guarda que torna as três regras executáveis                                                                                                                 |
| 11    | **Entrega contínua no homelab desde o dia zero**                                                                                 | o serviço precisa nascer entregando; ratifica ou emenda a ADR 0017 lá                                                                                                                                                                                                       |

O passo e o domínio mínimo destravam o MVP inteiro. O agendamento e o escalonador
destravam o E2 — o experimento que prova que a plataforma **constrói** a anomalia, e não
apenas a detecta. As demais podem ser debatidas em paralelo ao avanço do MVP, **uma por
vez**.

O estatuto da barreira entrou na fila em 2026-07-31, à frente do agendamento, e foi
aceito em 2026-08-01 como ADR-0004. O parágrafo acima vale com uma emenda: o agendamento
e o escalonador destravam a **execução de controle**, e não o experimento reportado. O
E2 deixou de ser experimento do MVP. Enunciado da proposta em
[a anomalia por frequência](#a-anomalia-por-frequência-uma-proposta-que-muda-o-estatuto-da-barreira).

O agendamento e o escalonador entraram na fila em 2026-07-29. O ADR-0001 encaminhava as
duas para "ADR próprio" sem que nenhuma delas estivesse aqui. Um encaminhamento sem
destino é vazamento, não delegação. O agendamento foi aceito em 2026-08-01 como
ADR-0003, e encaminhou [`Q-0003-1`](../questions/Q-0003-1.md),
[`Q-0003-2`](../questions/Q-0003-2.md), [`Q-0003-3`](../questions/Q-0003-3.md) e
[`Q-0003-8`](../questions/Q-0003-8.md). A forma do escalonador foi aceita no mesmo dia
como ADR-0005: resolveu [`Q-0001-4`](../questions/Q-0001-4.md),
[`Q-0002-2`](../questions/Q-0002-2.md), [`Q-0003-1`](../questions/Q-0003-1.md) e
[`Q-0003-2`](../questions/Q-0003-2.md), e encaminhou
[`Q-0005-1`](../questions/Q-0005-1.md).

### A ordem da arquitetura mínima e da entrega contínua está sob tensão

O laboratório é entregue no cluster do
[`homelab-infrastructure`](https://github.com/da0hn/homelab-infrastructure), e a
exigência é que um serviço **nasça já entregando** — pipeline e CI/CD no mesmo commit
que cria o módulo, não retrofitados depois.

Isso não move o passo: o formato dele não afeta o que o pipeline empacota. Mas move a
arquitetura mínima e a entrega contínua para **junto do primeiro módulo compilável**, e
as decisões entre o domínio mínimo e os vereditos deixam de ser pré-requisito de
escrever código de esqueleto. O `Dockerfile` e o `deploy/kustomization.yaml` fixam o
número de módulos e a forma do artefato — que é o conteúdo da arquitetura mínima.

A entrega contínua tem uma particularidade que nenhuma outra tem: **parte dela já foi
tomada fora deste repositório.** A ADR 0017 do homelab, aceita em 2026-07-26, escolheu
Gradle, Toxiproxy e "microsserviços JVM" para este laboratório, dois dias antes do
replanejamento que descartou a arquitetura de serviços. Ratificar ou emendar é decisão
consciente e explícita. O inventário completo do que sobrevive e do que colide está em
[`../plano-do-laboratorio.md`](../plano-do-laboratorio.md), seção 12.

### O nível de isolamento não tem lugar nesta fila

O E5 exige a comparação do mesmo experimento sob `READ COMMITTED`, `REPEATABLE READ` e
`SERIALIZABLE`. Só o terceiro aborta uma das transações, com SQLSTATE `40001`. O plano
registra a exigência na seção 6, e nomeia o nível de isolamento como parâmetro do
experimento — escopo que os quatro experimentos anteriores não têm.

**Nenhuma linha desta fila nomeia esse parâmetro.**

A decisão de estratégias de concorrência é o destino aparente, e ela não serve sem
argumento. Uma estratégia é código da aplicação: `NONE`, `ATOMIC_UPDATE`, `OPTIMISTIC` e
`PESSIMISTIC` mudam o SQL que os passos emitem. Um nível de isolamento é propriedade da
transação, e ele muda o que o banco faz com o mesmo SQL. O E5 é o experimento que separa
os dois eixos: com `OPTIMISTIC` ativo sob `READ COMMITTED`, a invariante quebra sem
exceção nenhuma, porque inserir uma alocação não incrementa a versão de linha alguma.
Tratar o isolamento como mais um valor da mesma enumeração apagaria a distinção que o
experimento existe para mostrar.

Três destinos são possíveis, e a escolha não foi feita.

- **Estratégias de concorrência**, com o isolamento declarado como eixo separado dentro
  da mesma decisão. O custo é uma decisão que passa a carregar dois eixos.
- **Experiment**, que define o que uma execução declara. O isolamento seria um campo da
  definição, ao lado da semente. O custo é decidir a semântica do parâmetro num ADR cujo
  assunto é o ciclo de vida da execução.
- **Linha própria nesta fila**, se a escolha tiver alternativas e trade-off que nenhuma
  das duas comporte.

Uma pista contra o terceiro destino: o E5 não escolhe um nível, ele varre três. O que a
plataforma precisa é do eixo de variação, e não de um valor decidido uma vez.

Registrado em 2026-07-31, no levantamento do que falta para fechar o MVP.

### A anomalia por frequência: uma proposta que muda o estatuto da barreira

O laboratório foi planejado para **construir** a anomalia. O E2 declara a intercalação
`W1.READ → W2.READ → W1.WRITE → W2.WRITE`, o escalonador a impõe, e a atualização
perdida aparece em toda execução. A proposta inverte o mecanismo: a anomalia emerge da
**frequência** de execuções concorrentes, e o trabalho da plataforma passa a ser
**diagnosticar** se o erro esperado ocorreu.

A proposta não é uma preferência de implementação. Ela troca o que a plataforma promete:
de "esta execução produz a anomalia" para "esta configuração produz a anomalia com esta
taxa". As duas promessas exigem instrumentos diferentes.

#### O que a proposta contradiz

**A aresta `25 → 1` do plano**, seção 4. O texto lá diz: "o lost update precisa ser
demonstrado, não sorteado. Sem barreiras, o experimento produz *às vezes perde* — que é
a mesma frase que o engenheiro já dizia antes de abrir o laboratório." É o argumento
mais forte contra a proposta, e ele já estava escrito antes dela.

**O estatuto epistêmico do E2.** O plano separa E1 de E2 assim: "E1 prova que o
laboratório *detecta*. E2 prova que o laboratório *constrói*. São capacidades
diferentes, e a segunda é a que torna a primeira confiável." Sem barreira, a segunda
capacidade some, e a confiança na primeira perde o apoio que o plano lhe deu.

**A cláusula de honestidade do ADR-0001**, que está `Aceito`. Ela compara um braço com
barreiras contra um braço sem elas. Com um braço só, a cláusula fica sem sujeito. A
falha que ela existe para pegar — o runtime fabricando o fenômeno por agendamento —
deixa de ser possível pelo mesmo motivo, mas a fabricação por estado compartilhado
dentro do instrumento continua, e [`Q-0001-2`](../questions/Q-0001-2.md) registra que
ela não tem guarda.

**O ADR-0003 inteiro.** Ele define como uma barreira é declarada. A questão 4 daquele
documento está `aberto (crítico)` por causa desta proposta, e ele NÃO DEVE ser aceito
antes que este item seja decidido.

#### O que a proposta não contradiz, e o que ela reforça

**O oráculo do ADR-0002 já é uma contagem, e não um booleano.**
`perdidas = commits − (value_final − value_inicial)` mede magnitude. Uma taxa é a mesma
contagem dividida pelo número de tentativas, e nada no ADR-0002 precisa mudar para
produzi-la. O domínio mínimo foi escolhido de um jeito que serve às duas promessas.

**O E1 já é a proposta.** Cem incrementos, dez workers, nenhuma barreira, `value < 100`.
A mudança não introduz um experimento novo no MVP: ela promove a forma do E1 a norma e
rebaixa a do E2.

**O grupo de controle deixa de ser disciplina e vira pré-requisito lógico.** A regra
"se `NONE` não violar, a carga é insuficiente" já está no repositório. Sob a proposta,
ela passa a ser a única coisa que faz um resultado negativo significar alguma coisa.

**O passo sobrevive com duas das três motivações.** O ADR-0001 fixou o passo por três
exigências: barreira determinística, injeção de falha em ponto nomeado e timeline. A
proposta atinge a primeira e não toca nas outras duas. A etapa 6 continua precisando de
`AFTER_COMMIT` exato, e a timeline continua sendo um registro por passo.

#### O que a proposta cria, e ninguém decidiu ainda

**Um resultado negativo passa a ter quatro causas, e a plataforma não distingue nenhuma
delas hoje.** "Zero violações" PODE significar: a anomalia é impossível naquela
configuração; a anomalia é possível e a janela nunca foi atingida; a anomalia ocorreu e
o oráculo não a viu, porque ele lê o estado final quiescente
([`Q-0002-3`](../questions/Q-0002-3.md)); ou os workers nunca se sobrepuseram, porque o
pool de conexões os serializou. A primeira é o resultado que o experimento busca. As
outras três são defeitos do instrumento com a mesma aparência.

**A plataforma mede a consequência, e passaria a precisar medir a exposição.** Uma
atualização perdida exige que dois workers leiam o mesmo valor antes que qualquer um
escreva. Esse evento é contável a partir do log de observações que o ADR-0001 já obriga
o runtime a emitir. Contá-lo separa "a janela não abriu" de "a janela abriu e nada
aconteceu" — que é a distinção que converte um zero em conhecimento. Nenhum documento do
repositório nomeia essa métrica.

**Um resultado negativo precisa de regra de parada e de declaração de confiança.** Com N
tentativas e zero violações, o limite superior da taxa fica em torno de `3/N` com 95% de
confiança. Sem uma regra escrita, cada execução escolhe o próprio N, e dois relatórios
com o mesmo veredito afirmam coisas diferentes. Quem escolhe N, e o que o relatório
afirma quando o zero aparece, é decisão nova.

**O veredito ganha um terceiro formato.** A fila prevê booleano e curva. Taxa com
intervalo não é nenhum dos dois: ela tem um número e uma incerteza, e a incerteza
precisa aparecer no relatório. A decisão dos formatos de veredito muda de escopo por
causa disso.

**A falha intermitente entra no pipeline.** Um experimento probabilístico num workflow
que precisa ficar verde é um teste instável por construção. A tensão 2 do plano chama a
falha intermitente de "o pior resultado possível num instrumento de medida", e a
exigência de nascer entregando põe esse custo no primeiro commit, não depois.

#### Três desfechos, e nenhum é obviamente certo

**Remoção da barreira.** O agendamento sai, o ADR-0003 é descontinuado ainda `Proposto`,
e o E2 deixa de existir como experimento separado. Custo: a plataforma passa a afirmar
apenas o que observou, e perde o poder de mostrar a intercalação que causa o fenômeno —
que é a exigência pedagógica do cenário 25.

**Rebaixamento a instrumento de diagnóstico.** A frequência produz o resultado; a
barreira responde à pergunta que o resultado negativo deixa aberta. Se a execução por
frequência não produzir violação, a mesma configuração roda com a intercalação forçada:
violação ali significa carga insuficiente na primeira; ausência nas duas significa que a
anomalia é impossível naquela configuração. A barreira vira o **controle positivo** do
experimento, e o ADR-0003 continua válido com a seção `## Contexto` reescrita.

**Eixo coigual.** Frequência e barreira convivem como duas resoluções do experimento, do
mesmo jeito que o ADR-0001 fez com alta e baixa resolução da operação. Custo: todo
experimento passa a ter dois braços obrigatórios, e o laboratório carrega as duas
máquinas desde o MVP.

Registrado em 2026-07-31, no turno em que a proposta foi apresentada, antes de qualquer
resposta a ela.

O segundo desfecho foi o escolhido, e o
[ADR-0004](0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md) o fixou
junto dos instrumentos de diagnóstico. Ele foi aceito em 2026-08-01.

O [ADR-0003](0003-a-linguagem-do-agendamento.md) foi aceito no mesmo dia, com a seção
`## Contexto` reescrita para justificá-lo pela execução de controle. O parágrafo acima
que o proibia de ser aceito registra o bloqueio vigente em 2026-07-31, e deixou de valer
quando o ADR-0004 escolheu o desfecho.

O debate da aceitação mudou dois pontos do que está escrito acima. A exposição de
referência é contada no **controle negativo**, e não na execução medida: uma estratégia
que serializa fecha a janela, e ler esse zero como carga fraca condenaria a estratégia
mais protetora. E o veredito `sem exposição`, previsto aqui, não existe — o controle
negativo já detectava aquele caso, e o lugar foi ocupado por `janela mal declarada`.

## Questões encaminhadas

Uma questão com status `encaminhado` pertence a outro ADR já identificado na fila. Ao
aceitar o ADR de origem, o enunciado dela é transportado — **inteiro, não resumido, no
mesmo commit da aceitação** — para um arquivo próprio em
[`docs/questions/`](../questions/README.md). Um ADR NÃO DEVE ser aceito enquanto suas
questões encaminhadas não estiverem transportadas: o enunciado se perde, e a linha da
fila que o citava fica pendurada.

O formato do identificador `Q-NNNN-K`, o ciclo de vida `pendente` → `resolvida por
ADR-NNNN` e o índice completo — enunciado, origem, destino na fila e status de cada
questão — vivem em [`docs/questions/README.md`](../questions/README.md).
