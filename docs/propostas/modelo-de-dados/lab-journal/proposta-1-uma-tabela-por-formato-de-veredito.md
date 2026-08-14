# Proposta 1 — Uma tabela por formato de veredito

A aposta central é que o `lab-journal` conhece a forma de cada veredito, e cada formato
ganha tabela própria com coluna tipada. Ela otimiza a comparação entre execuções.

## O problema que este modelo resolve

O E3 compara estratégias sobre a mesma carga, e a comparação é de magnitude. O relatório
exibe três contagens, a taxa de aborto e o limite superior do zero, pelo
[ADR-0004](../../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#o-veredito-de-uma-execução-medida-é-uma-taxa).
Um caderno que guarde o relatório inteiro como texto não sustenta essa
tabela. Cada célula exigiria abrir e reinterpretar o documento. Aqui cada número é coluna, e a tabela
comparativa vira uma consulta.

O mesmo caderno guarda o log de observações evento a evento, persistido desde a etapa 1
pelo
[ADR-0017](../../../adr/0017-a-persistencia-antecipada-do-log-de-observacoes-e-o-buffer-que-a-alimenta.md#a-persistência-no-lab-journal-começa-na-etapa-1-e-não-mais-na-6).
O stream o lê por cursor, e não por instante, pelo
[ADR-0016](../../../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md#o-replay-por-cursor-é-o-único-mecanismo-com-ou-sem-histórico-completo).

## O modelo

```mermaid
erDiagram
    definicao_de_experimento ||--o{ execucao : "declara"
    execucao ||--|| contagem_de_execucao : "produz"
    execucao ||--o| veredito_do_contador : "produz"
    execucao ||--o| veredito_do_predicado : "produz"
    execucao ||--o| veredito_de_taxa : "produz"
    execucao ||--o{ observacao : "registra"
    definicao_de_experimento {
        uuid id PK "atribuido pela aplicacao; sem DEFAULT"
        text nome "declarado pela pessoa, no frontend"
        bigint semente "entrada declarada da execucao"
        bigint n_declarado "o N, escrito antes de executar"
        int workers "parte da carga declarada"
        text operacao "parte da carga declarada"
        text janela_abre "endereco de fronteira F_abre"
        text janela_fecha "endereco de fronteira F_fecha"
        timestamptz created_at "relogio do banco; metadado de CRUD"
        timestamptz updated_at "relogio do banco; metadado de CRUD"
    }
    execucao {
        uuid id PK "o execution_id, nome do lado do instrumento"
        uuid definicao_id FK "FK dentro do proprio schema"
        text papel "calibracao, controle negativo, medida, controle positivo"
        text estrategia "NONE, ATOMIC_UPDATE, OPTIMISTIC, PESSIMISTIC"
        text nivel_de_isolamento "fora da carga declarada, de proposito"
        timestamptz executed_at "adaptador de relogio; sem DEFAULT"
        timestamptz concluded_at "adaptador de relogio; sem DEFAULT"
    }
    contagem_de_execucao {
        uuid execucao_id PK "uma linha por execucao, sempre"
        bigint tentativas_lancadas "o N que o experimento declarou"
        bigint commits "passagens pela fronteira AFTER_COMMIT"
        bigint violacoes "saida do oraculo daquele experimento"
        bigint coincidencias "pares de janelas de exposicao sobrepostas"
    }
    veredito_do_contador {
        uuid execucao_id PK "presente so onde o oraculo exato roda"
        bigint perdidas "commits menos a diferenca de value"
        bigint value_inicial "lido do WAL, nunca por SELECT cruzado"
        bigint value_final "lido do WAL, nunca por SELECT cruzado"
    }
    veredito_do_predicado {
        uuid execucao_id PK "presente so onde o predicado roda"
        boolean satisfeito "a soma cabe na capacidade"
        bigint soma_obtida "somatorio de amount, vindo do WAL"
        bigint capacidade_declarada "o limite contra o qual se compara"
    }
    veredito_de_taxa {
        uuid execucao_id PK "presente so quando violacoes vale zero"
        text classificacao "invalido, janela mal declarada, exposicao insuficiente, protegido"
        int ordem_que_casou "1 a 5, da tabela normativa do ADR-0004"
    }
    observacao {
        uuid execucao_id PK "1a coluna da chave composta"
        bigint cursor PK "2a coluna; monotonico por execucao"
        bigint tentativa "campo da forma de um evento"
        text worker "campo da forma de um evento"
        text endereco_de_fronteira "endereco completo, do ADR-0001"
        text tipo "RESULTADO_DE_PASSO, BLOQUEIO, LIBERACAO, FALHA_INJETADA"
        boolean restrito "so em BLOQUEIO e LIBERACAO; nulo no resto"
        jsonb fatos "payload opaco; so em RESULTADO_DE_PASSO"
        timestamptz ocorrido_em "atribuido no lab-plane"
        timestamptz persistido_em "atribuido no lab-journal"
    }
```

A `execucao` carrega o discriminador, e o instrumento o chama de `execution_id`, pelo
[ADR-0015](../../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#o-nome-assimétrico-do-discriminador-e-a-tradução-num-ponto-único).
Nenhuma linha do desenho atravessa schema, e essa ausência é a decisão, pela regra de
[`schemas/`](../../../architecture/schemas/README.md#a-ausência-de-linha-entre-os-dois-diagramas-é-a-decisão).

## O que o diagrama não expressa

| Ausência ou detalhe                         | O que ela decide                                                                                                                                                                                                                 |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ordem da chave de `observacao`              | `(execucao_id, cursor)`, discriminador primeiro; a ordem inversa espalha o replay de uma execução por toda a B-tree                                                                                                              |
| índice                                      | nenhum índice aditivo; a chave composta já serve ao `cursor > C` do replay ([ADR-0016](../../../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md#o-replay-por-cursor-é-o-único-mecanismo-com-ou-sem-histórico-completo)) |
| `DEFAULT` em `executed_at` e `concluded_at` | ausente; as duas vêm do adaptador de relógio, pelo [ADR-0015](../../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#as-colunas-de-tempo-e-a-fonte-do-relógio-por-papel-do-valor)                        |
| `DEFAULT` na definição de experimento       | presente; `created_at` e `updated_at` da definição vêm do banco, pela mesma tabela do ADR-0015 — é a única coluna deste schema em que `now()` não contraria a regra de relógio injetável                                         |
| trigger                                     | nenhum, em tabela nenhuma; a escrita que esquecer a coluna falha alto                                                                                                                                                            |
| chave estrangeira                           | todas dentro de `lab_journal`; nenhuma alcança `sut` nem `lab_plane`, pelo [ADR-0010](../../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão)                                                         |
| taxa de violação, taxa de aborto e o limite | não são colunas; as três derivam de `contagem_de_execucao`, e guardá-las criaria um segundo lugar onde o mesmo número vive                                                                                                       |
| tabela para o formato curva do E4           | ausente, de propósito; ele não tem forma decidida ([`features/README.md`](../../../features/README.md#capacidade-conhecida-e-não-especificada))                                                                                  |
| tabela de veredito no caderno               | ela guarda o veredito, e não o produz; o caderno NÃO DEVE derivar veredito do log ([ADR-0002](../../../adr/0002-o-dominio-minimo-e-os-dois-oraculos.md#o-oráculo-lê-o-banco-e-não-deve-ler-o-log-de-observações))                |

## Trade-offs

| O que fica fácil                                                                          | O que fica caro ou impossível                                                                                              |
|-------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| a tabela comparativa do E3 vira uma consulta, com as três contagens lado a lado           | cada formato de veredito novo é uma migração, e o E4 fica sem casa até a decisão de formato                                |
| `NOT NULL` recusa a linha incompleta antes de a tela mostrar um relatório sem denominador | um relatório que o `lab-plane` emitir com campo novo é descartado em silêncio, até alguém migrar                           |
| a calibração é verificável em SQL: `commits` contra `value_final − value_inicial`         | o caderno passa a conhecer o vocabulário dos oráculos, e uma emenda de ADR sobre veredito alcança o schema dele            |
| o replay por cursor lê uma chave composta, sem índice aditivo nem ordenação por tempo     | `classificacao` e `ordem_que_casou` copiam a tabela normativa do ADR-0004 para dentro do schema, livres para divergir dela |

## O que esta proposta NÃO decide

| Assunto                                       | Estado                                                                                                                                                           |
|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| a composição global dos formatos de veredito  | continua aberta; este desenho apenas dá tabela ao formato já decidido, e cala sobre como eles convivem num relatório                                             |
| onde vive a definição de experimento          | não existe decisão sobre em qual banco ela vive ([`schemas/lab-plane.md`](../../../architecture/schemas/lab-plane.md#o-que-o-diagrama-do-lab_plane-não-desenha)) |
| a fonte do `persistido_em`                    | o ADR-0016 exige o instante, e não nomeia o relógio dele                                                                                                         |
| o formato JSON de cada evento no stream       | segue aberto no próprio [ADR-0016](../../../adr/0016-o-streaming-e-o-replay-do-log-de-observacoes.md#negativas)                                                  |
| o que acontece com o `Last-Event-ID` inválido | comportamento não decidido, pelo mesmo ADR                                                                                                                       |
| a limpeza entre duas execuções                | nada aqui apaga linha, e nada aqui decide quem apaga                                                                                                             |

## Perguntas que ela levanta

| Pergunta em aberto                                                                                                                                                                                                                                         |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Dois regimes de relógio conviveriam no mesmo schema — banco na definição, adaptador na execução. A pessoa aceita essa assimetria dentro de um arquivo de migração só?                                                                                      |
| O controle positivo NÃO DEVE ser reportado como resultado ([ADR-0004](../../../adr/0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md#a-barreira-é-o-controle-positivo)). Nada neste desenho o impede. Uma coluna `papel` basta como guarda? |
| Nada impede duas linhas de veredito para a mesma execução, em tabelas diferentes. Isso é composição implícita, e ela não foi decidida?                                                                                                                     |
| `cursor` é palavra reconhecida pelo PostgreSQL em contexto de comando. O nome da coluna precisa mudar, ou a citação entre aspas basta?                                                                                                                     |
| A `classificacao` guarda o veredito, e `ordem_que_casou` guarda como se chegou nele. Guardar as duas é redundância útil, ou é a mesma informação duas vezes?                                                                                               |

## Por que ela não é a Proposta 2 nem a 3

Ela aposta que o caderno **conhece** a forma de um veredito. A Proposta 2 aposta o
contrário, e guarda o relatório como documento opaco. A Proposta 3 não aposta
na forma do veredito: ela aposta na estrutura do ciclo de execuções, e faz o schema recusar a
comparação que o ADR-0004 proíbe.
