# Plano de implementação

Rastreador de alto nível do trabalho de implementação. **Este arquivo não decide nada.**
Ele existe porque o contexto de uma sessão é limpo, e uma pendência que fica só na
conversa desaparece no próximo compact.

## O corte de 2026-08-15

A pessoa pausou a etapa de planejamento documental e seguiu para implementação, com a
documentação acompanhando **depois de cada etapa**, e não antes.

A primeira etapa é **a definição de experimento** — os parâmetros que a pessoa declara
antes de rodar. Não é o runtime de passos, não é o oráculo, não é a observação.

**`E-57` fechou em `lab_plane`**, escolhido pela pessoa. O `lab_journal` é sistema de
auditoria e recebe o resultado; o `lab-plane` gerencia os parâmetros, controla execução e
término, e apresenta o veredito. A definição é insumo da medição, e não registro dela.

**O modelo escolhido é o P2 do `lab-plane`** — plano durável, filtro de execução ativa e
diagnóstico de admissão. O desenho vigente está em
`architecture/schemas/propostas/modelo-de-dados/lab-plane/proposta-escolhida/diagramas/`, e nenhuma
observação, calibração ou veredito vive nesse schema.

## As tarefas

| ID  | Tarefa                                                                  | Estado     |
|-----|-------------------------------------------------------------------------|------------|
| `1` | decidir os conjuntos de valores que oito colunas de `CHECK` não têm     | aberta     |
| `2` | a migração das tabelas do plano no `lab-plane`                          | bloqueada  |
| `3` | o modelo de escrita e a atribuição de identidade sem sequence           | bloqueada  |
| `4` | a admissão: expandir encontro em precedências, e recusar o inadmissível | bloqueada  |
| `5` | os endpoints sob `/api/runs`, que hoje roteiam para lugar nenhum        | bloqueada  |
| `6` | a documentação que a escolha de `E-57` desatualizou                     | aberta     |
| `7` | a entrada única de HTTP, e o roteamento por prefixo no Traefik          | feita aqui |

A tarefa `2` depende da `1`; a `3` e a `4` dependem da `2`; a `5` depende da `3`. A `6`
roda depois da implementação, e alcança a fila de decisões, o dono da forma do schema, o
ADR-0015, o Example Mapping de `execucao-de-experimento`, a matriz de integrações e o
roteador de consulta.

**A tarefa `7` não depende de nenhuma outra.** O gateway é o Traefik, e o service
discovery é o `Service` mais o CoreDNS. Nada de Kong, de APISIX ou de Consul entra aqui.

As quatro escolhas da pessoa, de 2026-08-15, e o custo nomeado de cada uma:

| Escolha          | O que ficou decidido, e o que ela custa                                                                                                                                                                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| a origem         | uma só, e é a do frontend: tudo entra por `lab.ghonda.dev`, e a API vive sob `/api/`. Não há CORS, não há preflight, e o SSE dispensa `withCredentials`. Nada de DNS ou de certificado muda — um wildcard cobre um label só, e este hostname cai no `*` existente                    |
| o prefixo        | nomeia o serviço, e não o recurso: `/api/lab-plane` e `/api/lab-journal`. A URL passa a dizer de qual plano veio a resposta; mover um recurso de serviço muda a URL do cliente, aceito porque o frontend já conhece os dois                                                          |
| o `StripPrefix`  | não é usado. Cada serviço declara `server.servlet.context-path` com o prefixo inteiro, `/api` incluído, e o caminho público iguala o interno. Custo descoberto na implementação: o Actuator cairia dentro do prefixo publicado, com `show-details: always`, e foi para porta própria |
| o sistema medido | não é exposto, e fica alcançável só de dentro do cluster. Um `curl` à mão durante a janela medida entra no oráculo exato como commit real, e nada o distingue da carga do experimento                                                                                                |

O lado do homelab está nas issues `#7`, o `IngressRoute`, e `#8`, a Access Application —
esta nasceu de um achado: o Access é declarado por hostname literal, e não por wildcard,
então um hostname novo nasce público. Deste lado está feito e verificado — um Traefik no
`compose.yaml` é a entrada única, o mapa vive em `local/traefik/dynamic.yml`, o Actuator
saiu para porta própria, e o `nginx.conf` deixou de rotear e passou a recusar `/api` com
404, porque o catch-all devolvia o `index.html` com 200.

**A tarefa `1` é escolha da pessoa, e não trabalho de código.** O próprio desenho declara
que nenhum documento do repositório decidiu esses conjuntos — os lados de fronteira, os
níveis de isolamento aceitos, o destino da carga, a forma de `execution_id` e quem
atribui as chaves primárias.

## Fora desta etapa

O runtime de passos, o escalonador, os dois oráculos, o caminho da observação até a tela,
o schema do `lab_journal` e o serviço de identidade. Registrados para não parecerem
esquecimento.

## Decisões de 2026-08-15 sobre topologia, todas fora da etapa atual

Vieram de uma pergunta sobre o sistema medido suportar múltiplas instâncias. Nenhuma é
da definição de experimento, e nenhuma bloqueia as tarefas acima.

| Assunto                                | Estado                  | O que ficou registrado                                                                                                                                                                                                                                                                                                                                                     |
|----------------------------------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| duas execuções medidas ao mesmo tempo  | decidida                | PODEM coexistir, **exceto onde a medida é a saturação** — ali a exclusividade é obrigatória. O discriminador separa os dados, e não a contenção do banco. Custo nomeado: um buraco no stream passa a invalidar todas as execuções ativas do intervalo, e não uma                                                                                                           |
| número de instâncias do sistema medido | decidida                | ajustado por um **serviço de provisionamento próprio**, antes de a janela medida abrir. Aberto: onde ele vive, qual credencial de cluster carrega — ela não pode ficar no processo que produz o veredito —, se a escala dentro da janela é permitida, e se a dispensa da regra de tecnologia foi escrita. Alternativas em `E-95`                                           |
| dividir o `lab-plane` em dois          | **decidida**            | **sim.** Um serviço executa — runtime, escalonador, injetor, workers — e PODE ter várias instâncias. O outro julga: consome o stream, mantém a lista de execuções ativas, admite e produz o veredito, em **instância única**. A réplica única é exigida por conhecer as execuções ativas, e não por executar passos, e a divisão solta a metade que não tem essa exigência |
| quem recebe `/api/runs` e a admissão   | consequência da divisão | **quem julga.** Admitir é escrever na lista de execuções ativas, e essa lista é o que prende a instância única. Pôr a admissão num terceiro serviço abriria corrida: um discriminador ainda não propagado ao consumidor faz o evento legítimo ser lido como corrupção, e a execução é invalidada                                                                           |
| o schema `lab_plane` depois da divisão | consequência da divisão | fica **inteiro** com quem julga e admite — plano do experimento, lista de execuções ativas e diagnóstico de admissão são todos dele. Quem executa nasce **sem schema**, porque não grava estado durável. **A etapa atual não muda:** as tarefas `1` a `5` seguem como estão                                                                                                |
| o nome dos dois serviços               | aberta                  | não decidido. O módulo `lab-plane` existe no reactor, no `compose.yaml` e no papel do banco; se ele mantém o nome ao ficar com o schema, e como o serviço que executa se chama, é escolha da pessoa                                                                                                                                                                        |
| o artefato que registra a divisão      | aberta                  | topologia de serviço é decisão arquitetural durável, e o precedente é o ADR-0011, que dividiu o instrumento a primeira vez ao tirar o log para o `lab-journal`. Pelo corte de 2026-08-15 o documento vem **depois** da implementação, e o runtime de passos está fora da etapa atual                                                                                       |
| transação entre chamadas de passo      | direção provisória      | a tentativa vira uma sessão guardada pelo sistema medido, indexada por um identificador que carrega a instância que o criou. A pessoa registrou baixa confiança; confirma-se ou desfaz-se quando a chamada de passo for implementada                                                                                                                                       |
| ADR-0001 contra ADR-0008               | achado, sem tratamento  | `TransactionTemplate` exige todos os passos num mesmo bloco de código, e o ADR-0008 pôs o runtime noutro processo. Qualquer mecanismo para a transação entre chamadas alcança o corpo do ADR-0001, e o regime de patch não cobre isso — é emenda ou substituição                                                                                                           |

## Pendências levantadas e não resolvidas

- O `Application` do ArgoCD aponta para `deploy/` neste repositório, e este repositório
  decidiu que `deploy/` nunca vai existir. A contradição é anterior à tarefa `7` e não é
  criada por ela, mas a issue `#7` depende da `#2`, que é onde ela cai.
- O SSE atravessa o Traefik sem buffer, e o Cloudflare na frente pode bufferizar — um
  stream bufferizado vira lote sem produzir erro. O servidor precisa de
  `Cache-Control: no-transform`, e ninguém escreveu isso ainda.
- O Access com sessão de 24 horas expirando no meio de um stream de longa duração é modo
  de falha real, e não foi testado. Está anotado na issue `#8`.
- A divisão do `lab-plane` em dois alcança o prefixo `/api/lab-plane`: ele nomeia um
  serviço que passa a ser dois, e não se decidiu se vira dois prefixos ou segue um.
- Este arquivo não tem linha no roteador de `docs/README.md`, e isso é parte da tarefa `6`.
- Os dois arquivos de diagrama da proposta escolhida seguem não versionados, por escolha
  da pessoa.
