-- Um papel por servico, com um schema por papel. E a decisao E-18 de
-- 2026-08-06: um servico jamais acessa o schema de outro.
--
-- No homelab estes papeis sao criados por quem opera a Camada 6, e as senhas
-- vem cifradas com SOPS. Aqui elas sao literais de proposito: este arquivo
-- so e lido pelo contêiner local, e nenhum Secret entra neste repositorio.

CREATE ROLE lab_plane   LOGIN PASSWORD 'lab_plane';
CREATE ROLE lab_journal LOGIN PASSWORD 'lab_journal';
CREATE ROLE sut         LOGIN PASSWORD 'sut';

-- Cada papel cria e possui o proprio schema. O Flyway de cada aplicacao o
-- cria na primeira migracao, por `create-schemas: true`.
GRANT CREATE ON DATABASE lab TO lab_plane, lab_journal, sut;

-- O `lab-plane` le o WAL por replicacao logica, e nao por SELECT no schema
-- alheio. Sem este atributo o oraculo escolhido em E-18 nao tem fonte.
ALTER ROLE lab_plane REPLICATION;

-- Nenhum papel enxerga o `public`, que ficaria como espaco de nomes comum
-- por onde a regra de E-18 vazaria sem ninguem notar.
REVOKE ALL ON SCHEMA public FROM PUBLIC;
