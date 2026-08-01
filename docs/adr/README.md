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

| ADR                                                          | Título                                                          | Estado     |
|--------------------------------------------------------------|-----------------------------------------------------------------    |------------|
| [0001](0001-o-passo-como-unidade-de-execucao.md)             | O passo como unidade de execução, observação e injeção de falha    | `Aceito`   |
| [0002](0002-o-dominio-minimo-e-os-dois-oraculos.md)          | O domínio mínimo: contador com oráculo exato e predicado de capacidade | `Aceito`   |
| [0003](0003-a-linguagem-do-agendamento.md)                   | A linguagem do agendamento: como uma barreira é declarada       | `Proposto` |

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

| Ordem | Decisão                                                                                              | Por que precisa vir aqui                                                                                                                                                                                            |
|-------|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1     | **O passo como unidade de execução, observação e injeção de falha** — ADR-0001, `Aceito`             | toda outra decisão herda a forma que esta escolheu (plano, seção 2)                                                                                                                                                 |
| 2     | **O domínio mínimo: contador com oráculo exato mais predicado de capacidade** — ADR-0002, `Aceito`   | define o que é medido; fechou [`Q-0001-3`](#q-0001-3--o-critério-de-igualdade-entre-dois-traços-de-sql-não-está-definido) e encaminhou quatro questões novas                                                        |
| 3     | **A linguagem do agendamento: como uma barreira é declarada** — ADR-0003, `Proposto`                 | o ADR-0001 fixa o endereço da fronteira e para aí; sem a linguagem o E2 não é declarável                                                                                                                            |
| 4     | **A forma do escalonador: estado, decisão e protocolo de desistência**                               | consome o agendamento e executa a barreira; [`Q-0001-4`](#q-0001-4--o-escalonador-precisa-de-um-protocolo-de-desistência) e [`Q-0002-2`](#q-0002-2--quem-declara-que-a-execução-terminou-e-o-oráculo-lê-antes-ou-depois-disso) pedem a mesma máquina |
| 5     | **Estratégias de concorrência como dado, não como branch**                                           | sem isso o experimento de comparação não existe; [`Q-0001-2`](#q-0001-2--o-compartilhamento-por-colaborador-injetado-continua-sem-guarda) pede o controle positivo aqui; acrescenta a coluna `version` e nomeia a estratégia de calibração do ADR-0002 |
| 6     | **O log de observações: forma, ordem e onde vive**                                                   | é o substrato da timeline agora e do replay depois; [`Q-0001-1`](#q-0001-1--o-endereço-da-fronteira-precisa-sobreviver-à-edição-da-operação) pede aqui a identidade da operação gravada no registro do resultado    |
| 7     | **Experiment: definição, semente, hipótese e asserções**                                             | precisa resolver a tensão entre Designer na UI e definição versionada; [`Q-0002-4`](#q-0002-4--o-estado-inicial-não-é-estabelecido-por-ninguém) pede aqui o ciclo de vida de uma execução                            |
| 8     | **Os dois formatos de veredito: booleano e curva**                                                   | se ficar para depois, o grupo D não cabe na arquitetura; [`Q-0002-3`](#q-0002-3--os-dois-oráculos-descrevem-apenas-o-estado-final-quiescente) acrescenta o eixo pontual contra contínuo no tempo                     |
| 9     | **Arquitetura mínima, stack e guardas executáveis**                                                  | um módulo, dois planos na mesma JVM, separação imposta por teste; [`Q-0002-1`](#q-0002-1--a-comparação-por-valor-depende-de-regras-que-nenhum-teste-verifica) pede a guarda que torna as três regras executáveis     |
| 10    | **Entrega contínua no homelab desde o dia zero**                                                     | o serviço precisa nascer entregando; ratifica ou emenda a ADR 0017 lá                                                                                                                                               |

O passo e o domínio mínimo destravam o MVP inteiro. O agendamento e o escalonador
destravam o E2 — o experimento que prova que a plataforma **constrói** a anomalia, e não
apenas a detecta. As demais podem ser debatidas em paralelo ao avanço do MVP, **uma por
vez**.

O agendamento e o escalonador entraram na fila em 2026-07-29. O ADR-0001 encaminhava as
duas para "ADR próprio" sem que nenhuma delas estivesse aqui. Um encaminhamento sem
destino é vazamento, não delegação.

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
