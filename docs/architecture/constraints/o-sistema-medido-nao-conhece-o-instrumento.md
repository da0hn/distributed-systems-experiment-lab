# O sistema medido não conhece o instrumento

**O `system-under-test` não sabe que está sendo medido.** Ele não depende de nenhum
outro módulo da aplicação, não chama nenhum outro serviço e não é alcançável de fora.

O que a árvore mostra:

- `system-under-test/pom.xml` declara `shared` e os starters do Spring, e nenhum dos
  outros executáveis;
- `api-gateway/src/main/resources/application.yml` não tem rota para ele, enquanto tem
  uma para o `lab-plane` e outra para o `lab-journal`;
- `system-under-test/src/main/resources/application.yml` não define
  `server.servlet.context-path`, ao contrário dos outros dois serviços de aplicação;
- a porta publicada no `compose.yaml` existe só para diagnóstico na máquina local.

**A ausência de rota é o ponto, e não um esquecimento.** Uma requisição feita à mão
durante a janela medida entra no oráculo como commit real, e nada a distingue da carga
do experimento. O veredito sai errado, e nenhum erro aparece: nem no log, nem no health
check, nem no relatório da execução.

A separação continua no sentido do dado. O instrumento não lê o schema do sistema
medido — ele lê o WAL, por replicação lógica
([a fronteira de schema](cada-servico-tem-o-proprio-schema.md)) —, e a credencial que
permite essa leitura não pertence ao processo que julga
([o privilégio de replicação](quem-le-o-wal-nao-produz-o-veredito.md)).

**O que esta restrição protege é a leitura do resultado.** Um defeito do instrumento
tem de aparecer como defeito do instrumento. Se o instrumento puder tocar o sistema
medido por um caminho que a fronteira não cobre, um bug dele passa a produzir um
veredito de inconsistência — e quem lê o relatório conclui sobre o sistema medido uma
coisa que só era verdade sobre a régua.
