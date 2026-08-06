-- Ver a nota em `lab-plane/.../V1__criar_schema_do_lab_plane.sql`: sem uma
-- migracao, o Flyway nao cria o schema.
--
-- As tabelas `resource` e `allocation` dependem das decisoes E-8 a E-13. A
-- coluna `version` continua proibida no esquema ate o commit que introduzir
-- a estrategia OPTIMISTIC, por exigencia do ADR-0006 — ela e o exemplo da
-- regra pedagogica: primeiro o problema, depois a solucao.

COMMENT ON SCHEMA sut IS
  'O sistema medido. Nao sabe que esta sendo medido, e nao conhece nenhum '
  'outro servico deste repositorio.';
