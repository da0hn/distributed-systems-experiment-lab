# Quem lê o WAL não é quem produz o veredito

`local/postgres-init.sql` cria um quarto papel, `cdc_connector`, com `LOGIN` e
`REPLICATION`. Ele não recebe `CREATE` no banco, não possui schema e nenhum serviço da
aplicação o usa. Nenhum processo do `compose.yaml` o consome hoje.

**O atributo `REPLICATION` não pertence ao `lab-plane`.** Dá-lo ao processo que produz o
veredito seria quebrar a fronteira de schema um nível abaixo dela: o mesmo processo que
julga passaria a carregar a credencial que alcança o banco inteiro, incluindo o schema
do sistema medido. A regra continuaria escrita, e a única coisa a impedir a consulta
direta seria a disciplina de quem escreve o código.

Separar o papel torna a proibição uma propriedade do banco, e não uma convenção. O
`lab-plane` consome mensagem, e não toca o WAL.

**O papel existe e o processo que o usaria, não.** É provisionamento sem consumo, e está
assim de propósito: a credencial e a configuração de replicação são a parte cara de
mudar depois, e o consumidor é a parte que se escreve quando houver o que consumir.
