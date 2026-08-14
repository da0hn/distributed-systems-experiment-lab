# ADR-0014: O broker na travessia da observação

- **Estado:** Aceito
- **Data:** 2026-08-10
- **Etapa do roadmap:** 1 — reaproveita o broker que o ADR-0012 já trouxe ao dia zero.
- **Relacionado:** emenda o
  [ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md) e o
  [ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md), que
  recebem `Última atualização` e `Alterado por` no mesmo commit. Depende do
  [ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md), dono do
  RabbitMQ que esta decisão passa a reutilizar.
- **Nome do arquivo:** mantém o sufixo `-e-o-cursor-monotonico-do-replay`, herdado de
  quando este ADR ainda decidia o cursor de replay. O título perdeu essa parte na divisão
  de 2026-08-11, que cedeu o cursor ao ADR-0016; a divisão de 2026-08-12, que cede a
  persistência e o buffer ao ADR-0017, não devolve a parte perdida — ela desfaz só o que
  havia entrado depois de `a5d5777`. Por que o arquivo não é renomeado junto é lacuna
  registrada na linha
  [`E-83`](../fila-de-decisoes.md#e-83--onde-mora-o-racional-de-não-renomear-o-arquivo-do-adr-0014)
  da fila.

- **Última atualização:** 2026-08-12
- **Alterado por:**
  [ADR-0016](0016-o-streaming-e-o-replay-do-log-de-observacoes.md) — **divisão**, a sexta
  forma, decidida em 2026-08-11
  ([`README.md`](README.md#a-divisão-de-um-adr-aceito-decidida-em-2026-08-11)). Cinco
  subseções de `## Decisão` saíram deste corpo e vivem no ADR-0016, vigentes: "No
  `lab-journal`, a ordem é serial: persiste, depois emite"; "O push ao vivo é o pub/sub
  interno do Spring, em `AFTER_COMMIT`"; "O replay por cursor é o único mecanismo, com ou
  sem histórico completo"; "O cursor é campo próprio, monotônico por execução"; e "Dois
  instantes, nenhum deles é ordem". Com elas saíram os trechos de `## Justificativa`,
  `## Trade-offs` e `## Alternativas consideradas` que as sustentavam, e o título perdeu
  a parte que as nomeava — o nome do arquivo, não.
- **Alterado por:**
  [ADR-0017](0017-a-persistencia-antecipada-do-log-de-observacoes-e-o-buffer-que-a-alimenta.md)
  — **divisão**, aplicada uma segunda vez, decidida em 2026-08-12
  ([`../fila-de-decisoes.md`](../fila-de-decisoes.md#e-64-fecha-em-desfazer-por-divisão-escolhida-em-2026-08-12)).
  Duas subseções de `## Decisão` haviam entrado neste corpo depois de `a5d5777`, sem forma
  do lifecycle que as autorizasse — "A persistência no `lab-journal` começa na etapa 1, e
  não mais na 6" e "O runtime publica por um buffer em memória, numa thread separada" —,
  mais um parágrafo normativo que havia entrado dentro de "O evento sai do passo pelo
  broker". As duas subseções e o parágrafo saíram deste corpo e vivem no ADR-0017,
  vigentes, junto do argumento de `## Justificativa`, `## Consequências`, `## Trade-offs`
  e `## Alternativas consideradas` que os sustentava. **Três outras mudanças no corpo
  aceito acompanham a divisão, e este campo as declara.** Em
  `## Alternativas consideradas`, uma **fusão** que também havia entrado depois de
  `a5d5777` foi desfeita — "Sem broker: ao vivo bloqueante, ou buffer local com remetente
  próprio" volta a ser as duas subseções que o commit de aceite tinha, byte a byte;
  restaurar o corpo aceito não pede forma do lifecycle, porque é o corpo aceito que as
  seis formas protegem. E `## Quando esta decisão deixa de valer` e
  `## O que este ADR desfaz fora de si` foram reduzidas ao que sobra depois das duas
  divisões. **Os dois ADRs continuam `Aceito`**: nada aqui saiu de vigor, e o que entrou
  sem forma agora tem uma.

## Contexto

O [ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão) exige
que as observações atravessem "ao vivo, evento por evento", sem fixar **como**; as
[negativas](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#negativas)
nomeiam "buffer local com remetente próprio" como saída nunca escolhida. O
[ADR-0007](0007-o-log-de-observacoes-forma-ordem-e-onde-vive.md#onde-o-log-vive) põe o log
em memória e adia a persistência durável para a etapa 6.

As [negativas do ADR-0008](0008-os-dois-planos-em-processos-separados.md#negativas) põem
a latência da rede na medida pelas consultas ao escalonador e ao injetor, nas 900 a 1500
fronteiras do E1; a emissão da observação só virou travessia de rede depois, pelo
[ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão). O
[ADR-0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#comando-no-lab-plane-leitura-no-lab-journal-sem-bff)
desenha a aresta da observação indo direto do `lab-plane` ao `lab-journal`. O
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão)
pôs o RabbitMQ no caminho do veredito, consumindo CDC **com LSN** — identidade que
mensagem de negócio comum não tem; as
[negativas dele](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#negativas)
registram que a dispensa exigida foi "dispensada, e não satisfeita", e que ela não é
precedente ([`AGENTS.md`](../../AGENTS.md#regras-estruturais-que-valem-sempre)).

## Problema

**Como a observação sai do passo e chega ao `lab-journal` sem entrar na janela medida, e
sem que uma queda proposital do `lab-plane` apague o que ocorreu?**

Forças em conflito:

- O ADR-0010 exige travessia ao vivo, evento por evento, sem fixar o transporte.
- A travessia síncrona entra na janela medida, uma por fronteira: 900 a 1500 no E1.
- A etapa 6 mata o `lab-plane`, e o que não saiu do processo morre com ele.
- Uma observação perdida sem sinal envenena o veredito.
- Reaproveitar o broker exige dispensa explícita: a do ADR-0012 não é precedente.

## Decisão

### O evento sai do passo pelo broker

O evento de observação DEVE sair do passo pelo **broker** — o RabbitMQ do
[ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão),
que hoje serve só ao caminho do veredito e passa a servir também ao da observação.
Nenhum transporte novo entra na árvore.

## Justificativa

**Por que o broker.** A travessia síncrona mantém as 900 a 1500 observações do E1 dentro
da janela medida. O buffer local sem broker falha na etapa que o laboratório existe para
estudar: a etapa 6 mata o `lab-plane` de propósito, e um buffer não esvaziado desaparece
com ele — o instrumento perdendo dado em silêncio, a confusão que a separação de planos
existe para impedir
([ADR-0008, Justificativa](0008-os-dois-planos-em-processos-separados.md#justificativa)).
O broker sobrevive à queda do `lab-plane` por construção, e é a única das três opções sem
esse modo de falha; por isso a dispensa já concedida ao ADR-0012 é concedida de novo aqui,
explicitamente.

**Por que emenda, e não substituição.** A regra alterada não dá título ao ADR de origem,
nem é a decisão principal dele: a do ADR-0010 continua exigindo travessia ao vivo — muda
só o transporte. O precedente é o dos ADRs 0009, 0010 e 0011, que emendaram regra dentro
de `## Decisão` pelo mesmo critério e seguem `Aceito`.

## Consequências

### Positivas

- A travessia de 900 a 1500 observações sai do caminho bloqueante, e nenhuma tecnologia
  nova entra na árvore: o RabbitMQ já existe pelo ADR-0012.

### Negativas

- O broker vira dependência também da observação: sem ele de pé, a tela para de
  atualizar.
- **Pergunta em aberto.** De onde a contagem de coincidências do
  [ADR-0004](0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#a-plataforma-conta-coincidências)
  lê os dados — deste log, ou de estrutura própria. Se ler o log e uma observação se
  perder em trânsito, a contagem cai a zero e a ordem 3 da
  [classificação do zero](0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-zero-é-classificado-e-a-classificação-tem-quatro-valores)
  produziria `protegido` sobre banco violado — falso negativo silencioso.
- **Pergunta em aberto.** A contrapressão entre broker e `lab-journal`, para o consumidor
  lento, não foi decidida.
- O broker PODE duplicar, reordenar ou perder mensagem, por diagrama do próprio
  [ADR-0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md#decisão).
  A observação não carrega LSN, e nenhuma deduplicação foi decidida.

### Neutras

- O `lab-journal` mantém schema próprio, sem acesso direto de outro serviço — a
  fronteira do
  [ADR-0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão)
  não muda.

## Trade-offs

- O benefício **a travessia de 900 a 1500 observações sai do caminho síncrono** foi
  aceito em troca do custo **uma segunda dispensa da regra de tecnologia, e o broker vira
  ponto único de falha também para a observação**.

## Alternativas consideradas

### Ao vivo bloqueante, como o ADR-0010 deixava implícito

**Descartada.** É o que já valia: a observação atravessa direto, sem transporte
declarado. Perde por manter as 900 a 1500 travessias do E1 dentro da janela medida
([ADR-0008, Negativas](0008-os-dois-planos-em-processos-separados.md#negativas)).

### Buffer local volátil, com um remetente por worker

**Descartada.** A favor: nenhum processo novo. Perde pelo argumento da Justificativa: o
buraco que a etapa 6 abre não é sinalizado — a saída que o
[ADR-0010, Negativas](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#negativas)
já registrava como não escolhida.

## Quando esta decisão deixa de valer

O gatilho original desta seção — mais de uma instância do `lab-journal`, e a
contrapressão do broker sob carga para o consumidor lento — foi cedido ao
[ADR-0016](0016-o-streaming-e-o-replay-do-log-de-observacoes.md#quando-esta-decisão-deixa-de-valer)
na divisão de 2026-08-11, junto das subseções que ele sustentava. Nenhum gatilho próprio
do transporte pelo broker, isolado da forma como o `lab-journal` o consome, foi
identificado até aqui.

## O que este ADR desfaz fora de si

Esta decisão desatualiza os arquivos abaixo, fora do próprio corpo.

| Documento                                                                                                                                                         | O que muda                                                                                                                                                                                                                                                                                |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [ADR-0010, Decisão](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão)                                                                         | a regra "ao vivo, evento por evento" ganha mecanismo — o broker; emenda registrada no cabeçalho                                                                                                                                                                                           |
| [ADR-0011, Comando no `lab-plane`...](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#comando-no-lab-plane-leitura-no-lab-journal-sem-bff) | a aresta direta `LP -->\|" observações "\| LJ` do diagrama passa pelo broker; emenda registrada no cabeçalho                                                                                                                                                                              |
| [`AGENTS.md`, Regras estruturais](../../AGENTS.md#regras-estruturais-que-valem-sempre)                                                                            | "A regra foi dispensada uma vez" fica falsa: esta decisão concede a segunda dispensa, para o mesmo broker no caminho da observação                                                                                                                                                        |
| [`integrations.md`, Matriz](../architecture/integrations.md#matriz)                                                                                               | a linha `lab-plane` → RabbitMQ descreve este caminho; as outras linhas que `a5d5777` também reivindicava para este ADR — `frontend` → `lab-journal` por SSE, e RabbitMQ → `lab-journal` — foram cedidas ao ADR-0016 na divisão de 2026-08-11, e o `desfaz` dele é quem as reivindica hoje |
| [feature-card.md, R12](../features/observacao-passo-a-passo/feature-card.md#regras-de-negócio)                                                                    | regra `pendente` de Feature Card, e não ADR aceito; nomeia o broker e carrega a evidência deste ADR ao lado da do ADR-0010                                                                                                                                                                |

## Patches aplicados

Nenhum patch aplicado.

O regime de patch está em [`README.md`](README.md#a-revogação-da-imutabilidade-decidida-em-2026-08-07).
Um patch conserta citação, caminho ou erro material; ele NÃO DEVE alterar a decisão nem o
argumento que a sustentava.
