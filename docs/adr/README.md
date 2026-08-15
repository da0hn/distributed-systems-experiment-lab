# Architecture Decision Records

**Esta pasta é histórico, e está congelada.** Nenhum ADR novo nasce aqui, e nenhum ADR
existente é editado, emendado, patcheado, adendado, dividido ou substituído. Ela existe
para consultar o que já foi decidido, e para nada além disso.

**Decisão arquitetural nova acontece na conversa, e vai para o código.** Ela não vira
documento neste diretório.

**Se um ADR contradisser a árvore, a árvore está certa.** O código é a fonte da verdade,
e nenhum arquivo daqui é mantido em sincronia com ele.

## Índice

| ADR                                                                                       | Título                                                                     | Do que trata                                                                         |
|-------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [0001](0001-o-passo-como-unidade-de-execucao.md)                                          | O passo como unidade de execução, observação e injeção de falha            | Uma operação é uma sequência ordenada e finita de passos nomeados.                   |
| [0002](0002-o-dominio-minimo-e-os-dois-oraculos.md)                                       | O domínio mínimo: contador com oráculo exato e predicado de capacidade     | O domínio tem duas entidades, `Resource` e `Allocation`, e nenhum nome de negócio.   |
| [0003](0003-a-linguagem-do-agendamento.md)                                                | A linguagem do agendamento — como uma barreira é declarada                 | O agendamento é um conjunto de restrições de precedência entre eventos.              |
| [0004](0004-o-estatuto-da-barreira-e-o-diagnostico-da-nao-ocorrencia.md)                  | O estatuto da barreira e o diagnóstico da não ocorrência                   | A execução medida roda sem agendamento, e o veredito dela é uma taxa.                |
| [0005](0005-a-forma-do-escalonador.md)                                                    | A forma do escalonador — estado, decisão e protocolo de desistência        | O escalonador guarda os workers ativos e as restrições pendentes de cada execução.   |
| [0006](0006-a-forma-da-estrategia-de-concorrencia.md)                                     | A forma da estratégia de concorrência — contrato plugável e calibração     | A estratégia é rótulo opaco, e nenhum componente do Lab Plane ramifica por ela.      |
| [0007](0007-o-log-de-observacoes-forma-ordem-e-onde-vive.md)                              | O log de observações — forma, ordem e onde vive                            | Um evento do log é registro imutável com tentativa, worker, fronteira e tipo.        |
| [0008](0008-os-dois-planos-em-processos-separados.md)                                     | Os dois planos em processos separados, desde o dia zero                    | A chamada de passo atravessa a rede, e o Control Plane não chama o Lab Plane.        |
| [0009](0009-a-classificacao-do-dual-write-e-a-regiao-de-pacote.md)                        | A classificação do dual write e a região de pacote do sistema sob teste    | O dual write é escrita parcial, e o sistema sob teste vive em `dev.da0hn.lab.sut`.   |
| [0010](0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md)                      | A fronteira de schema e o CDC como fonte do veredito                       | Nenhum serviço lê o schema de outro, e o oráculo lê o WAL por replicação lógica.     |
| [0011](0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md)            | A topologia de serviços e o caderno de laboratório fora do Git             | Cinco serviços compõem o laboratório, e o caderno de laboratório fica fora do Git.   |
| [0012](0012-o-broker-no-caminho-do-veredito-e-a-dispensa-que-ele-exigiu.md)               | O broker no caminho do veredito, e a dispensa que ele exigiu               | O Debezium Server lê o WAL por `pgoutput` e publica no RabbitMQ, em instância única. |
| [0013](0013-a-proveniencia-da-fonte-como-criterio-da-proibicao-do-oraculo.md)             | A proveniência da fonte como critério da proibição do oráculo              | A proibição alcança a fonte produzida pelo instrumento, e nada além dela.            |
| [0014](0014-o-broker-na-travessia-da-observacao-e-o-cursor-monotonico-do-replay.md)       | O broker na travessia da observação                                        | O evento de observação sai do passo pelo broker, sem transporte novo na árvore.      |
| [0015](0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md)                 | A chave, o discriminador de execução e as colunas de tempo                 | Quais colunas restringem a medição, quem pode lê-las e como a janela se delimita.    |
| [0016](0016-o-streaming-e-o-replay-do-log-de-observacoes.md)                              | O streaming e o replay do log de observações                               | O `lab-journal` persiste o evento antes de emiti-lo, e emite em `AFTER_COMMIT`.      |
| [0017](0017-a-persistencia-antecipada-do-log-de-observacoes-e-o-buffer-que-a-alimenta.md) | A persistência antecipada do log de observações, e o buffer que a alimenta | A persistência no `lab-journal` começa na etapa 1, por um buffer em memória.         |
| [0018](0018-cada-controle-roda-sob-o-seu-proprio-nivel.md)                                | Cada controle roda sob o seu próprio nível                                 | O controle negativo roda sob o nível mais fraco, e o positivo sob o nível medido.    |
| [0019](0019-a-entrega-sai-do-deploy-e-a-imagem-ganha-tag-semantica.md)                    | A entrega sai do `deploy/`, e a imagem ganha tag semântica                 | Os manifests vivem no `homelab-infrastructure`, e `deploy/` não nasce aqui.          |
| [0020](0020-o-aviso-de-conclusao-e-a-subsuncao-do-adr-0008.md)                            | O aviso de conclusão, e a subsunção da proibição do ADR-0008               | O sistema medido pode avisar a conclusão por callback HTTP, e só isso.               |
