# Cada serviço tem o próprio schema, e ninguém lê o do vizinho

Três serviços dividem o banco `lab`, e não dividem nada além dele. Cada um tem papel
próprio, schema próprio e Flyway próprio.

| Papel no banco  | Schema        | Quem o usa            |
|-----------------|---------------|-----------------------|
| `lab_plane`     | `lab_plane`   | o `lab-plane`         |
| `lab_journal`   | `lab_journal` | o `lab-journal`       |
| `sut`           | `sut`         | o `system-under-test` |
| `cdc_connector` | nenhum        | ninguém, hoje         |

`local/postgres-init.sql` cria os papéis e concede `CREATE` no banco a cada serviço. O
`application.yml` de cada um fixa `spring.flyway.schemas`, `default-schema` e
`create-schemas: true`, e a migração `V1` existe justamente para forçar o Flyway a
rodar: sem nenhuma migração ele não roda, e sem rodar não cria schema nenhum — a
fronteira ficaria declarada em configuração e ausente no banco, com o health check
passando assim mesmo.

A última linha do arquivo de init faz `REVOKE ALL ON SCHEMA public FROM PUBLIC`. Sem
ela, o `public` seria o espaço de nomes comum por onde a fronteira vazaria sem ninguém
notar.

**O instrumento não é exceção.** A leitura do estado medido vem do WAL do PostgreSQL, e
nunca de um `SELECT` no schema do sistema medido. É por isso que o `compose.yaml` sobe o
banco com `wal_level=logical`, e por isso que o papel `lab_plane` não tem `REPLICATION`.

**O `SELECT` cruzado falharia em silêncio, e é isso que torna a regra cara.** Ele
funcionaria: a consulta devolveria linhas, o teste passaria, o veredito sairia. O que
mudaria é a origem do número — um estado lido depois do fato, pelo mesmo processo que
julga o fato, no lugar do registro que o banco produziu no instante do commit. Duas
execuções com o mesmo veredito passariam a afirmar coisas diferentes.

O schema de um serviço é privado por construção, e por isso ele **não é contrato**
([o que é contrato](o-que-e-contrato.md)).

A forma decidida de cada schema vive em [`../schemas/`](../schemas/README.md). Nenhuma
migração cria aquelas tabelas hoje: as três `V1` criam apenas o schema.
