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
- Nome do arquivo: `NNNN-titulo-em-kebab-case.md`. Template em
  [`0000-template.md`](0000-template.md).
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
para [`## Questões encaminhadas`](#questões-encaminhadas), **inteira e no mesmo commit
da aceitação**. Um ADR NÃO DEVE ser aceito enquanto suas questões encaminhadas não
estiverem transportadas: o enunciado se perde, e a linha da fila que o citava fica
pendurada.

Um ADR **aceito** nunca é editado nem apagado. Para mudar a decisão, escreva um ADR novo
e marque o antigo como `Substituído por ADR-NNNN`. Enquanto estiver `Proposto`, editar é
permitido.

### Substituição e subsunção são coisas diferentes

Um ADR novo que **contradiga** a decisão de um aceito o substitui. O antigo recebe
`Substituído por ADR-NNNN`, e o que ele decidiu sai de vigor.

Um ADR novo PODE, em vez disso, **subsumir** uma regra de um aceito. A subsunção acontece
quando a regra antiga continua correta no caso que ela enxergava, e o ADR novo separa
casos que ela tratava como um só. O ADR antigo permanece `Aceito`, e a regra continua
valendo com o alcance que o ADR novo lhe der.

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

| Ordem | Decisão                                                                                            | Por que precisa vir aqui                                                                                                                                                                                                                                                          |
|-------|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1     | **O passo como unidade de execução, observação e injeção de falha** — ADR-0001, `Aceito`           | toda outra decisão herda a forma que esta escolheu (plano, seção 2)                                                                                                                                                                                                               |
| 2     | **O domínio mínimo: contador com oráculo exato mais predicado de capacidade** — ADR-0002, `Aceito` | define o que é medido; fechou [`Q-0001-3`](#q-0001-3--o-critério-de-igualdade-entre-dois-traços-de-sql-não-está-definido) e encaminhou quatro questões novas                                                                                                                      |
| 3     | **O estatuto da barreira e o diagnóstico da não ocorrência** — ADR-0004, `Aceito`                  | rebaixou a barreira a controle positivo, fixou a taxa como veredito e encaminhou cinco questões                                                                                                                                                                                   |
| 4     | **A linguagem do agendamento: como uma barreira é declarada** — ADR-0003, `Aceito`                 | o ADR-0001 fixa o endereço da fronteira e para aí; sem a linguagem, a execução de controle do ADR-0004 não é declarável; encaminhou quatro questões                                                                                                                               |
| 5     | **A forma do escalonador: estado, decisão e protocolo de desistência**                             | consome o agendamento e executa a barreira; [`Q-0001-4`](#q-0001-4--o-escalonador-precisa-de-um-protocolo-de-desistência) e [`Q-0002-2`](#q-0002-2--quem-declara-que-a-execução-terminou-e-o-oráculo-lê-antes-ou-depois-disso) pedem a mesma máquina, com `Q-0003-1` e `Q-0003-2` |
| 6     | **Estratégias de concorrência como dado, não como branch**                                         | sem isso o experimento de comparação não existe; [`Q-0001-2`](#q-0001-2--o-compartilhamento-por-colaborador-injetado-continua-sem-guarda) pede o controle positivo aqui; acrescenta a coluna `version` e nomeia a estratégia de calibração do ADR-0002                            |
| 7     | **O log de observações: forma, ordem e onde vive**                                                 | é o substrato da timeline agora e do replay depois; [`Q-0001-1`](#q-0001-1--o-endereço-da-fronteira-precisa-sobreviver-à-edição-da-operação) pede aqui a identidade da operação gravada no registro do resultado, e `Q-0003-3` o critério de igualdade entre duas execuções       |
| 8     | **Experiment: definição, semente, hipótese e asserções**                                           | precisa resolver a tensão entre Designer na UI e definição versionada; [`Q-0002-4`](#q-0002-4--o-estado-inicial-não-é-estabelecido-por-ninguém) pede aqui o ciclo de vida de uma execução, e `Q-0003-8` o que `N` conta                                                           |
| 9     | **Os dois formatos de veredito: booleano e curva**                                                 | se ficar para depois, o grupo D não cabe na arquitetura; [`Q-0002-3`](#q-0002-3--os-dois-oráculos-descrevem-apenas-o-estado-final-quiescente) acrescenta o eixo pontual contra contínuo no tempo                                                                                  |
| 10    | **Arquitetura mínima, stack e guardas executáveis**                                                | um módulo, dois planos na mesma JVM, separação imposta por teste; [`Q-0002-1`](#q-0002-1--a-comparação-por-valor-depende-de-regras-que-nenhum-teste-verifica) pede a guarda que torna as três regras executáveis                                                                  |
| 11    | **Entrega contínua no homelab desde o dia zero**                                                   | o serviço precisa nascer entregando; ratifica ou emenda a ADR 0017 lá                                                                                                                                                                                                             |

O passo e o domínio mínimo destravam o MVP inteiro. O agendamento e o escalonador
destravam o E2 — o experimento que prova que a plataforma **constrói** a anomalia, e não
apenas a detecta. As demais podem ser debatidas em paralelo ao avanço do MVP, **uma por
vez**.

O estatuto da barreira entrou na fila em 2026-07-31, à frente do agendamento, e foi
aceito em 2026-08-01 como ADR-0004. O parágrafo acima vale com uma emenda: o agendamento
e o escalonador destravam a **execução de controle**, e não o experimento reportado. O E2
deixou de ser experimento do MVP. Enunciado da proposta em
[a anomalia por frequência](#a-anomalia-por-frequência-uma-proposta-que-muda-o-estatuto-da-barreira).

O agendamento e o escalonador entraram na fila em 2026-07-29. O ADR-0001 encaminhava as
duas para "ADR próprio" sem que nenhuma delas estivesse aqui. Um encaminhamento sem
destino é vazamento, não delegação. O agendamento foi aceito em 2026-08-01 como ADR-0003,
e encaminhou `Q-0003-1`, `Q-0003-2`, `Q-0003-3` e `Q-0003-8`. **A forma do escalonador é
a primeira decisão não tomada da fila**, e quatro questões apontam para ela.

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
dentro do instrumento continua, e `Q-0001-2` registra que ela não tem guarda.

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
o oráculo não a viu, porque ele lê o estado final quiescente (`Q-0002-3`); ou os workers
nunca se sobrepuseram, porque o pool de conexões os serializou. A primeira é o resultado
que o experimento busca. As outras três são defeitos do instrumento com a mesma
aparência.

**A plataforma mede a consequência, e passaria a precisar medir a exposição.** Uma
atualização perdida exige que dois workers leiam o mesmo valor antes que qualquer um
escreva. Esse evento é contável a partir do log de observações que o ADR-0001 já obriga
o runtime a emitir. Contá-lo separa "a janela não abriu" de "a janela abriu e nada
aconteceu" — que é a distinção que converte um zero em conhecimento. Nenhum documento do
repositório nomeia essa métrica.

**Um resultado negativo precisa de regra de parada e de declaração de confiança.** Com
N tentativas e zero violações, o limite superior da taxa fica em torno de `3/N` com 95%
de confiança. Sem uma regra escrita, cada execução escolhe o próprio N, e dois
relatórios com o mesmo veredito afirmam coisas diferentes. Quem escolhe N, e o que o
relatório afirma quando o zero aparece, é decisão nova.

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
aceitar o ADR de origem, o enunciado da questão é transportado para cá — **inteiro, não
resumido**. O ADR de destino precisa nascer com o problema que motivou a entrada dele na
fila. Um resumo é a mesma perda, mais devagar.

Cada questão transportada recebe um identificador `Q-NNNN-K`: `NNNN` é o ADR de origem,
`K` é o número que a questão tinha na seção `## Questões em aberto` dele. Os dois são
congelados no ato da aceitação, e o identificador nunca é reutilizado. **Cite uma
questão por esse identificador**, nunca por "a questão K do ADR-NNNN" — aquela seção
deixa de existir quando o ADR é aceito, e a citação passa a apontar para nada.

Uma questão transportada nasce com status `pendente`. Ela **não** é removida desta seção
quando alguém a resolve: o status passa a `resolvida por ADR-NNNN`, e a subseção dela
abre nomeando onde a decisão está. O enunciado permanece porque ele registra o que
estava em jogo antes da decisão — e é isso que um leitor futuro não consegue reconstruir
a partir do ADR de destino.

O custo dessa escolha é que a seção cresce e passa a conter questão viva ao lado de
questão morta. A coluna `Status` é a única marca que as separa, e ela é obrigatória por
isso.

O enunciado transportado é reescrito num ponto só: as referências internas ao ADR de
origem. "Este ADR", "aqui" e "a questão 3" não significam nada fora do documento em que
foram escritas, e passam a nomear o ADR e o identificador.

| ID         | Questão                                                                    | Destino na fila              | Status                  |
|------------|----------------------------------------------------------------------------|------------------------------|-------------------------|
| `Q-0001-1` | O endereço da fronteira precisa sobreviver à edição da operação            | o log de observações         | pendente                |
| `Q-0001-2` | O compartilhamento por colaborador injetado continua sem guarda            | estratégias de concorrência  | pendente                |
| `Q-0001-3` | O critério de igualdade entre dois traços de SQL não está definido         | o domínio mínimo             | resolvida por ADR-0002  |
| `Q-0001-4` | O escalonador precisa de um protocolo de desistência                       | a forma do escalonador       | pendente                |
| `Q-0002-1` | A comparação por valor depende de regras que nenhum teste verifica         | arquitetura mínima e guardas | pendente                |
| `Q-0002-2` | Quem declara que a execução terminou, e o oráculo lê antes ou depois disso | a forma do escalonador       | pendente                |
| `Q-0002-3` | Os dois oráculos descrevem apenas o estado final quiescente                | os dois formatos de veredito | pendente                |
| `Q-0002-4` | O estado inicial não é estabelecido por ninguém                            | Experiment                   | pendente                |
| `Q-0003-1` | Um worker que nunca chega trava o agendamento                              | a forma do escalonador       | pendente                |
| `Q-0003-2` | Um agendamento sobre uma tentativa que talvez não ocorra                   | a forma do escalonador       | pendente                |
| `Q-0003-3` | Duas execuções do mesmo experimento não têm critério de igualdade          | o log de observações         | pendente                |
| `Q-0003-8` | O `N` declarado antes não fecha com uma estratégia que retenta             | Experiment                   | pendente                |
| `Q-0004-2` | Nada obriga o passo a reportar a chave de contenção                        | arquitetura mínima e guardas | pendente                |
| `Q-0004-3` | Comparar janelas exige um instante comparável entre workers                | o log de observações         | pendente                |
| `Q-0004-4` | A regra de parada colide com a exigência de nascer entregando              | entrega contínua no homelab  | pendente                |
| `Q-0004-5` | O terceiro formato de veredito precisa caber ao lado dos dois já previstos | os dois formatos de veredito | pendente                |
| `Q-0004-8` | O limite `3/N` pressupõe ensaios independentes                             | os dois formatos de veredito | pendente                |

### Q-0001-1 — O endereço da fronteira precisa sobreviver à edição da operação

Origem: ADR-0001, questão 1. Destino: **o log de observações**, descrito na fila como o
substrato do replay. A identidade gravada acompanha o registro do resultado, e não a
definição da operação.

Definições de experimento são versionadas e referenciam fronteiras. O rótulo sobrevive à
inserção de um passo no meio da operação — o índice não sobreviveria, e é por isso que o
rótulo foi escolhido. Mas o rótulo não sobrevive a uma renomeação, e nada impede que o
corpo de um passo mude mantendo o rótulo.

A etapa 12 quer reexecutar um experimento antigo e obter o mesmo resultado. Se o corpo
do passo mudou, o replay é de outro experimento com o mesmo nome. Nenhum mecanismo de
versionamento de operação foi proposto.

Uma pista aparece dentro do próprio ADR-0001. A prova de equivalência já produz um traço
de SQL normalizado por operação. Esse traço deriva do corpo dos passos, e não do rótulo
deles: renomear um passo não altera o traço, e trocar o statement altera. Registrar o
traço junto do resultado daria ao replay um critério de identidade que ninguém precisa
lembrar de incrementar à mão. A pista tem dois limites. Ela depende de `Q-0001-3` — sem
critério de normalização o traço não é comparável — e ela é cega para o passo `COMPUTE`,
que não emite SQL nenhum.

A questão tem duas metades, e só uma é grave. A renomeação do rótulo quebra a resolução
do endereço, e a plataforma DEVE recusar endereço que não resolve — a falha é ruidosa, e
o experimento antigo não roda. A mudança de corpo com o rótulo intacto não quebra nada:
o replay executa, entrega um resultado, e ninguém sabe que mediu outra operação. É esta
metade que precisa de mecanismo.

Sobra um subcaso da primeira metade. O rótulo é um nome reciclável. Uma edição que
renomeie `select-resource` e atribua esse mesmo rótulo a outro passo faz o endereço
resolver para o passo errado, sem erro nenhum. É a classe de falha que a proibição de
reutilizar número de ADR já evita em outro lugar deste repositório.

Quatro candidatas apareceram no debate de 2026-07-29. Nenhuma foi escolhida.

**Versão declarada à mão na definição da operação.** O resultado grava a versão, e o
replay recusa quando divergir. Custa uma anotação, e a mudança aparece no diff. Ela
apodrece em silêncio, porque ninguém incrementa. É a "lista manual que apodrece" com que
o ADR-0001 descartou a alternativa B, e usá-la aqui contradiz o próprio argumento.

**Digest do traço de SQL normalizado.** Reusa a máquina da prova de equivalência, e
deriva do corpo em vez de declaração humana. Depende de `Q-0001-3`, e é cega para o
passo
`COMPUTE`: trocar `value + 1` por `value + 2` não altera o texto de statement nenhum
quando o parâmetro entra como marcador. Num laboratório de contadores, o `COMPUTE` é a
lógica.

**Digest do bytecode dos corpos.** Enxerga qualquer mudança de corpo, inclusive a do
`COMPUTE`. Enxerga também o que não é mudança: outra versão do compilador, o nome de uma
variável local, o índice de um lambda sintético. É a borda estrita de `Q-0001-3` no grau
máximo, e o laboratório aprenderia a ignorar a recusa.

**O SHA do commit no registro do resultado.** O resultado em `docs/experiments/` grava o
commit em que rodou, e o replay compara. O dado é automático, já existe, e identifica o
sistema inteiro — inclusive a versão do driver JDBC e do Spring, que a seção
`## Consequências` do ADR-0001 reconhece como fonte de divergência de traço. Ela não diz
**o que** mudou, apenas que algo mudou, e o `git diff` entre os dois commits responde o
resto. A ADR 0017 do homelab já usa o SHA como tag de imagem, e o artefato executável
daquele commit existe no GHCR.

A quarta candidata é a proposta na mesa, por ser a única cujo dado nenhum humano precisa
manter e cuja cobertura não para na borda do SQL. O debate de 2026-07-29 não a
confirmou.

### Q-0001-2 — O compartilhamento por colaborador injetado continua sem guarda

Origem: ADR-0001, questão 2. Destino: **estratégias de concorrência**. Esta é a primeira
entrada daquela decisão.

As três camadas decididas pelo ADR-0001 protegem um caminho: o escopo de execução entre
passos. Elas não protegem outro. Um repositório injetado que guarde um `Map` como cache
é uma definição de operação limpa, uma análise estática verde e um escopo íntegro — e os
workers compartilham por ele assim mesmo. O laboratório volta a produzir atualizações
perdidas dentro do próprio instrumento, e o resultado continua indistinguível de um lost
update real.

A cláusula de honestidade não fecha essa lacuna. Ela compara alta resolução com baixa, e
a operação em baixa resolução também usa o colaborador injetado. As duas resoluções
violam a invariante, e a cláusula passa.

O **controle positivo** cobre a rota sem precisar enxergá-la. O repositório já exige
controle negativo: se a estratégia `NONE` não violar a invariante, o experimento não tem
carga suficiente. Falta o espelho — uma estratégia cuja contagem de violações DEVE ser
exatamente zero. Se `PESSIMISTIC` violar, ou o banco está errado ou o instrumento está
fabricando, e a fabricação atravessa qualquer lock do PostgreSQL porque acontece antes
dele.

O controle positivo custa uma execução, não aponta a origem, e pressupõe que exista uma
estratégia declarada. Por isso ele pertence ao ADR de estratégias de concorrência.

### Q-0001-3 — O critério de igualdade entre dois traços de SQL não está definido

**Resolvida pelo ADR-0002**, na subseção `### O critério de igualdade entre dois traços
de SQL`. Dois traços são iguais quando têm o mesmo comprimento e, em cada posição, o
texto normalizado e a lista de valores ligados coincidem. A normalização colapsa espaço
em branco e não faz mais nada, porque qualquer regra além disso exigiria um analisador
de SQL — proibido pelo ADR-0001. Os valores ligados são comparados como valores, e a
ordem entre statements é comparada como sequência.

Origem: ADR-0001, questão 3. Destino: **o domínio mínimo**, porque o oráculo exato do
contador é o que dá base para escolher.

A prova de equivalência do ADR-0001 exige que as duas resoluções emitam o mesmo traço.
"O mesmo" precisa de definição, e a definição tem duas bordas ruins. Uma normalização
frouxa deixa passar a diferença que importa. Uma normalização estrita reprova um par
correto, e o laboratório aprende a ignorar o teste.

Três pontos estão sem critério. O parâmetro ligado aparece como valor ou como marcador —
comparar valores torna o teste dependente do dado de entrada. A ordem entre leituras
independentes muda sem que a operação tenha mudado, e comparar sequência reprova o que
comparar conjunto aceitaria. E o conjunto de entradas amostradas define o que a prova
cobre; fora dele a divergência continua invisível.

O que o ADR-0001 decidiu: a prova existe, ela compara traço de SQL de execução sem
concorrência, e a cláusula de honestidade não vale para uma operação enquanto a prova
dela não existir.

### Q-0001-4 — O escalonador precisa de um protocolo de desistência

Origem: ADR-0001, questão 4. Destino: **a forma do escalonador**. Esta é a primeira
entrada daquela decisão.

A ordem escolhida pelo ADR-0001 na fronteira — bloquear, depois falhar — evita que um
worker morra antes de chegar à barreira. Ela não evita o inverso. Um worker que falha na
fronteira de saída do passo N nunca chegará à fronteira de entrada do passo N+1, e um
escalonador que espere por ele trava a execução inteira.

O runtime precisa notificar o escalonador de que um worker terminou — por falha
injetada, por exceção do banco ou por conclusão. A forma dessa notificação não foi
decidida pelo ADR-0001.

### Q-0002-1 — A comparação por valor depende de regras que nenhum teste verifica

Origem: ADR-0002, questão 1. Destino: **arquitetura mínima e guardas executáveis**, que
já carrega a análise estática exigida pela camada 2 do ADR-0001. A guarda é da mesma
família: rejeitar chamadas proibidas nas classes do sistema sob teste.

A justificativa do ADR-0002 apoia-se em três regras: o relógio é injetável, a
aleatoriedade é semeada, e a identidade é atribuída pela aplicação. As três são texto em
`CLAUDE.md` e em ADRs arquivados. Nenhuma delas é hoje uma regra executável.

Uma chamada esquecida a `Instant.now()` dentro de um corpo de passo faz a prova de
equivalência reprovar um par correto, de forma intermitente — o pior resultado possível
num instrumento de medida, porque a reprovação some quando alguém reexecuta. O
diagnóstico apontaria para o critério de igualdade, e a causa estaria no corpo do passo.

### Q-0002-2 — Quem declara que a execução terminou, e o oráculo lê antes ou depois disso

Origem: ADR-0002, questão 2. Destino: **a forma do escalonador**, junto de `Q-0001-4`,
porque a resposta é a mesma máquina.

Os dois oráculos do ADR-0002 leem o banco "depois que o último worker terminar". Nada
naquele ADR nem no ADR-0001 define quem observa esse instante.

`Q-0001-4` registra o problema vizinho: um worker que falha na fronteira de saída do
passo N nunca chega à fronteira de entrada do passo N+1, e um escalonador que espere por
ele trava a execução. O runtime precisa de uma notificação de que um worker terminou —
por falha, por exceção ou por conclusão.

O oráculo é o consumidor dessa mesma notificação, um nível acima: ele precisa saber que
**todos** terminaram. Se ele ler cedo, mede um estado intermediário e reporta uma perda
que ainda seria escrita.

### Q-0002-3 — Os dois oráculos descrevem apenas o estado final quiescente

Origem: ADR-0002, questão 3. Destino: **os dois formatos de veredito**, que já está na
fila para impedir que a arquitetura endureça em torno do formato booleano.

`perdidas` e `Σ amount ≤ capacity` são avaliados uma vez, sobre um banco parado. Isso
serve aos cinco experimentos do MVP, porque as duas anomalias deixam rastro permanente:
um incremento perdido não volta, e uma alocação excedente não sai da tabela.

Não serve ao grupo E, posse no tempo. Uma expiração de lease produz um intervalo em que
dois donos existem ao mesmo tempo, e o estado final tem um dono só. Não serve ao grupo
D, cujo veredito é uma curva. E não serve a nenhum fenômeno cuja violação seja
transitória por natureza.

Esta questão acrescenta um terceiro eixo àquela decisão: além de booleano contra curva,
existe pontual contra contínuo no tempo. A tensão 3 do plano — a amostragem no tempo não
tem forma, e é a lacuna mais antiga do repositório — é a mesma questão vista de outro
lado.

### Q-0002-4 — O estado inicial não é estabelecido por ninguém

Origem: ADR-0002, questão 4. Destino: **Experiment**, porque a escolha depende do ciclo
de vida de uma execução, que aquele ADR define.

O oráculo do ADR-0002 lê `value_inicial` antes do primeiro worker. Aquele ADR não diz
quem escreve esse valor, nem como o banco volta ao ponto de partida entre duas execuções
do mesmo experimento. Ele fixa uma restrição sobre a resposta, e encaminha o resto.

As candidatas visíveis têm custos diferentes e nenhuma é obviamente certa. Um `TRUNCATE`
entre execuções é barato e apaga o histórico de uma execução anterior que alguém talvez
quisesse inspecionar. Um schema por execução isola e multiplica objetos no banco. Um
recurso novo por execução, com identificador derivado da semente, não apaga nada e faz a
tabela crescer sem limite.

A escolha afeta o critério de igualdade de traço do ADR-0002: se o identificador do
recurso mudar a cada execução, ele é um valor ligado que difere entre duas execuções da
mesma entrada, e a comparação por valor reprova o par.

As três candidatas não são equivalentes diante da exigência de replay. O identificador
derivado da semente faz duas execuções da mesma semente produzirem o mesmo
identificador, que é o que a etapa 12 exige — e é também o que faz a segunda execução
colidir com as linhas deixadas pela primeira. A candidata do recurso novo por execução
só evita a colisão se o identificador variar entre execuções, e aí ela contradiz a
comparação por valor. Sobram a limpeza entre execuções e o isolamento por schema.

A parte decidida pelo ADR-0002: o identificador do recurso DEVE ser função da semente do
experimento, e NÃO DEVE ser função do instante da execução. O que resta é quem executa a
limpeza, em que momento, e se o histórico de uma execução anterior sobrevive.

### Q-0003-1 — Um worker que nunca chega trava o agendamento, e a recusa por texto não o alcança

Origem: ADR-0003, questão 1. Destino: **a forma do escalonador**, junto de `Q-0001-4`,
porque a resposta é a mesma máquina.

A seção `## Decisão` do ADR-0003 recusa antes de executar o que o texto do agendamento
revela: ciclo, papel inexistente, endereço que não resolve. Sobra o que o texto não
revela.

Um worker morto por falha injetada na fronteira anterior nunca produz a chegada que os
outros esperam. O encontro fica incompleto, e a execução para. O sintoma é idêntico ao de
um bug do runtime e ao de um ciclo que a detecção tivesse deixado passar.

`Q-0001-4` registra o mesmo problema do lado do worker: o runtime precisa notificar o
escalonador de que um worker terminou, por falha, por exceção ou por conclusão. O
agendamento é o consumidor dessa notificação — ele precisa saber que a chegada esperada
não virá, para decidir entre liberar os demais e declarar o experimento inválido. A
escolha entre esses dois não é a mesma pergunta que `Q-0001-4` faz, e ela depende da
resposta daquela.

O ADR-0004 aumentou a superfície desta questão. A execução de controle roda sobre a carga
da execução medida, e o E1 usa dez workers. Uma chegada que não vem deixa de ser o caso
raro de uma falha injetada e passa a incluir o worker que terminou seu quinhão de trabalho
antes dos outros. A subseção `### A execução de controle declara a própria carga, com uma
passagem por worker` do ADR-0003 trata do eixo que produz esse desalinhamento.

### Q-0003-2 — Um agendamento sobre uma tentativa que talvez não ocorra

Origem: ADR-0003, questão 2. Destino: **a forma do escalonador**, pelo mesmo motivo de
`Q-0003-1`.

O ADR-0001 exige seletor de tentativa em todo endereço de fronteira, sem valor padrão. O
E2 usa uma estratégia sem retry e cita `tentativa 1` sem ambiguidade.

O E4 roda `OPTIMISTIC` com 2 a 50 workers, e o número de tentativas de cada worker é
resultado do experimento, não entrada dele. Um encontro declarado para a `tentativa 2` de
dois workers espera por um worker que PODE ter concluído na primeira e nunca chegará.

É o caso geral de `Q-0003-1`, e a diferença importa: aqui a espera impossível não vem de
falha, e sim de sucesso. Nenhuma análise do texto do agendamento a detecta, porque o
texto está correto.

O ADR-0004 tirou esta questão do hipotético. O texto acima dizia que a pergunta valeria
para "o primeiro experimento que combine os dois". Esse experimento é o E3: ele tem
`OPTIMISTIC` entre as quatro estratégias, e o controle positivo do braço otimista roda
sobre a configuração dele. Um zero com exposição sobrevivente no braço `OPTIMISTIC` é
exatamente o caso que o ADR-0004 manda desempatar com a barreira, e é o caso em que o
número de tentativas não é conhecido antes.

### Q-0003-3 — Duas execuções do mesmo experimento não têm critério de igualdade

Origem: ADR-0003, questão 3. Destino: **o log de observações**, que a fila descreve como
o substrato do replay, e que já recebeu `Q-0001-1` pelo lado da identidade da operação.

A seção `## Decisão` do ADR-0003 fixa que o determinismo garantido é o do veredito, e que
a timeline PODE variar nos trechos que nenhuma restrição ordena. A etapa 12 quer
reexecutar um experimento antigo e obter o mesmo resultado, e "o mesmo resultado" passa a
ter duas leituras possíveis.

Comparar apenas o veredito aceita duas execuções cujas timelines divergem em tudo que o
agendamento não ordena — que é o comportamento desejado, e também o que esconde uma
mudança real de comportamento sob uma coincidência de veredito. Comparar a timeline
inteira reprova execuções corretas, pelo mesmo motivo que derrubou a alternativa A
daquele ADR.

O critério provável é intermediário: duas execuções são iguais quando o veredito coincide
e quando a ordem dos eventos **restringidos** coincide. Esse critério não foi verificado
contra nenhum experimento, e ele exige que o log distinga o evento que uma restrição
ordenou do evento que ocorreu livre. Nada hoje exige esse registro.

O ADR-0004 partiu a questão em duas metades com dificuldades diferentes. Numa execução de
controle, o critério intermediário acima ainda tem chance: existem eventos restringidos
para comparar. Numa execução medida não existe restrição nenhuma, e o veredito é uma taxa
que a concorrência real produz. Duas execuções medidas com a mesma semente PODEM devolver
taxas diferentes sem que nada tenha mudado, e a etapa 12 quer reexecutar um experimento
antigo e obter o mesmo resultado. O que "o mesmo resultado" significa para uma taxa não
foi decidido em documento nenhum.

### Q-0003-8 — O `N` declarado antes não fecha com uma estratégia que retenta

Origem: ADR-0003, questão 8. Destino: **Experiment**, que define o que uma execução
declara, junto de `Q-0002-4`. A pergunta é o que `N` conta, e `N` é entrada declarada de
uma execução.

O ADR-0004 exige que uma execução medida declare `N` antes de começar, e chama `N` de
número de **tentativas lançadas**. Tentativa é termo do ADR-0001: uma passagem completa
pela sequência de passos, e uma execução de operação produz uma ou mais.

As duas leituras de `N` quebram em pontos diferentes.

Se `N` conta tentativas no sentido do ADR-0001, ele inclui os retries. Sob `OPTIMISTIC`,
o número de retries é resultado da execução, e não entrada dela: o ADR-0001 registra que
"o número de tentativas vira um dado observável do log", e um dado observável não é
declarável antes. O E3 e o E4 rodam `OPTIMISTIC`, e os dois estão no MVP.

Se `N` conta execuções de operação, ele é declarável, e a taxa de aborto `(N − commits)/N`
deixa de enxergar o retry. Uma execução de operação que falhe duas vezes e cometa na
terceira entra como um lançamento e um commit, e a taxa de aborto dela é zero. A
`## Justificativa` do ADR-0004 diz que essa taxa existe para mostrar "a estratégia que
evita a anomalia descartando trabalho" — e sob esta leitura ela não mostra o trabalho
descartado.

O ADR-0004 está `Aceito` e não pode ser editado. A questão não é do agendamento: ela
apareceu no ADR-0003 porque o seletor de tentativa do ADR-0001 é o mesmo eixo, e a
decisão da questão 6 daquele documento obrigou a olhar para ele. A resolução PODE exigir
um ADR que substitua a contagem do ADR-0004, e não apenas a decisão de destino.

### Q-0004-2 — Nada obriga o passo a reportar a chave de contenção

Origem: ADR-0004, questão 2. Destino: **arquitetura mínima e guardas executáveis**, que
já carrega `Q-0002-1` e a análise estática exigida pela camada 2 do ADR-0001. A guarda é
da mesma família: verificar uma propriedade das classes do sistema sob teste que nenhum
teste verifica hoje.

A seção `## Decisão` do ADR-0004 resolveu a metade que era decisão dele. Duas janelas
sobrepostas no tempo formam coincidência apenas quando as chaves de contenção coincidem,
e a chave chega ao Lab Plane como um fato reportado pelo passo — o caminho que o ADR-0001
já abriu para `version` e `rowsAffected`.

O que sobra é a obrigação. Um passo que não reporte a chave produz uma contagem de
coincidências que o runtime aceita sem saber que está errada, e o zero é classificado a
partir dela. O resultado é um veredito `protegido` num experimento cuja janela abriu, ou
um `janela mal declarada` num experimento cuja declaração está correta, sem que teste
nenhum falhe.

Sem a chave, a contagem seria pior fora do MVP. Os experimentos do MVP operam sobre um
`Resource` único, e toda sobreposição temporal é sobreposição sobre a mesma linha. Um
experimento com cem recursos e dez workers produz sobreposição o tempo todo, e quase
nenhuma delas é oportunidade de anomalia. A chave existe para essa configuração; a guarda
existe para o dia em que alguém a escrever e esquecer de reportá-la.

A forma da guarda tem uma dificuldade que a decisão de destino precisa enfrentar. A
exigência não vale para todo passo: ela vale para os passos que delimitam uma janela de
exposição declarada por algum experimento. Uma regra que exija a chave de todo passo
reprova código correto; uma regra que a exija de nenhum não pega o esquecimento. O
ligamento entre a declaração da janela e o corpo do passo é onde a guarda precisa olhar,
e esse ligamento vive no experimento, não na classe.

### Q-0004-3 — Comparar janelas exige um instante comparável entre workers

Origem: ADR-0004, questão 3. Destino: **o log de observações**, que a fila descreve como
o substrato da timeline e do replay.

A contagem de coincidências compara intervalos produzidos por threads diferentes. A
comparação exige que os instantes registrados por dois workers sejam ordenáveis entre si,
e não apenas dentro de cada worker.

O repositório exige que o tempo seja injetável, e `Q-0002-1` registra que essa exigência
ainda não é regra executável. Nenhum documento diz qual relógio o log usa, nem se ele é
monotônico, nem qual é a resolução dele. Duas janelas que se sobreponham por menos que a
resolução do relógio contam como disjuntas, e a contagem de coincidências subestima.

A questão pertence ao log de observações porque a resposta é uma propriedade do registro,
e não do ADR-0004. Aquela decisão consome o instante; ela não escolhe de onde ele vem.

### Q-0004-4 — A regra de parada colide com a exigência de nascer entregando

Origem: ADR-0004, questão 4. Destino: **entrega contínua no homelab desde o dia zero**.

`N` declarado antes resolve o viés da taxa e cria um custo de tempo. Um `N` alto ocupa o
runner do GitHub Actions; um `N` baixo produz um experimento que passa numa execução e
falha na seguinte, sem que nada tenha mudado.

O laboratório é entregue por um pipeline que precisa ficar verde, e a ADR 0017 do homelab
fixa runner hospedado. Nenhum dos dois repositórios decidiu se um experimento roda no
pipeline, se ele roda sob demanda, ou se o pipeline executa uma versão reduzida com `N`
menor — que seria uma terceira execução, com um terceiro significado.

A tensão 2 do plano é a mesma vista de outro lado: um limiar mal calibrado produz falha
intermitente, "o pior resultado possível num instrumento de medida". Aqui o limiar é `N`.

### Q-0004-5 — O terceiro formato de veredito precisa caber ao lado dos dois já previstos

Origem: ADR-0004, questão 5. Destino: **os dois formatos de veredito**, já na fila, que
passa a tratar três.

A fila prevê booleano para os grupos A, B, C e E, e curva para o grupo D. O ADR-0004
acrescenta taxa com limite de confiança, e o acréscimo não é um caso particular de nenhum
dos dois. Uma taxa tem um número e uma incerteza; um booleano não tem nenhum dos dois, e
uma curva tem uma série.

`Q-0002-3` já acrescentava um eixo àquela decisão — pontual contra contínuo no tempo. Com
`Q-0004-5` e `Q-0004-8`, aquele ADR passa a resolver três eixos ao mesmo tempo, e PODE
precisar ser dividido.

A comparação entre execuções depende disso. A tabela do E3 põe quatro estratégias lado a
lado, e sob o ADR-0004 três delas trazem taxa zero com limites de confiança diferentes.
Como essa tabela é lida, e o que ela permite concluir, não é decisão do ADR-0004.

### Q-0004-8 — O limite `3/N` pressupõe ensaios independentes

Origem: ADR-0004, questão 8. Destino: **os dois formatos de veredito**, junto de
`Q-0004-5`. As duas tratam do mesmo objeto: `Q-0004-5` pergunta como o formato
taxa-com-incerteza cabe ao lado do booleano e da curva, e `Q-0004-8` pergunta o que a
incerteza publicada afirma. Decidir a apresentação sem decidir a validade produziria um
relatório com um número que ninguém sabe ler.

O ADR-0004 recortou o alcance desta questão ao resolver o denominador: o limite passou a
ser calculado sobre `commits`, e não sobre `N`. A troca corrige o denominador e não toca
no pressuposto de independência, que é o que `Q-0004-8` registra.

A regra dos três estima o limite superior de uma proporção quando zero eventos ocorrem em
`N` ensaios independentes. As tentativas de uma execução medida não são independentes:
elas competem pelo mesmo recurso, pelo mesmo pool de conexões e pelo mesmo escalonador do
sistema operacional. Uma tentativa lenta atrasa as vizinhas, e os resultados ficam
correlacionados.

O efeito da correlação sobre o intervalo não tem sinal conhecido sem um modelo, e o
ADR-0004 publica o número como afirmação de força no relatório. A seção `## Problema`
daquele ADR nomeia o risco: "um número que pareça uma medida sem ser uma medida é pior
que a ausência do número".

A questão é menor que as duas que o ADR-0004 resolveu no mesmo debate em um ponto, e
maior em outro. Menor porque o limite ordena corretamente dois relatórios com número de
commits diferente, que é o uso principal que a `## Justificativa` daquele ADR lhe dá.
Maior porque o número publicado carrega uma precisão que o pressuposto não sustenta, e
quem o ler não saberá disso.
