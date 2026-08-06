-- O schema em si e criado pelo Flyway, por `create-schemas: true`, antes de
-- aplicar esta migracao. Ela existe porque sem NENHUMA migracao o Flyway nao
-- roda, e sem rodar ele nao cria schema nenhum — a fronteira de `E-18`
-- ficaria declarada em configuracao e ausente no banco, com o health check
-- passando assim mesmo.
--
-- Nenhuma tabela entra aqui. As do Lab Plane dependem das decisoes E-8 a
-- E-13, do grupo II do Lote E.

COMMENT ON SCHEMA lab_plane IS
  'O instrumento. Le o WAL do system under test por replicacao logica, e '
  'nunca as tabelas dele por SELECT (decisao E-18, 2026-08-06).';
