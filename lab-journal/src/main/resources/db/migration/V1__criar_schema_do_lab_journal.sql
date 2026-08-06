-- Ver a nota em `lab-plane/.../V1__criar_schema_do_lab_plane.sql`: sem uma
-- migracao, o Flyway nao cria o schema.
--
-- Nenhuma tabela entra aqui. O ADR-0007 ja fixou a forma e a ordem do log de
-- observacoes, entao a primeira tabela do historico pode ser escrita sem
-- esperar o grupo II — ela nao entrou neste commit, que e so o esqueleto.

COMMENT ON SCHEMA lab_journal IS
  'O caderno de laboratorio. Unico guardiao do historico desde a decisao '
  'E-17, de 2026-08-06: docs/experiments/ nao existe.';
