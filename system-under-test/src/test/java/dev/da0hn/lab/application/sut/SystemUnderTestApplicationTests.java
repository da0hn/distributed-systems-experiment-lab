package dev.da0hn.lab.application.sut;

import static org.assertj.core.api.Assertions.assertThat;

import javax.sql.DataSource;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.jdbc.core.JdbcTemplate;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest
@Testcontainers
class SystemUnderTestApplicationTests {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres =
      new PostgreSQLContainer<>("postgres:18-alpine");

  @Autowired
  private DataSource dataSource;

  @Test
  void flywayCreatesTheSchemaThisProcessOwns() {
    final var schema = new JdbcTemplate(this.dataSource).queryForObject(
        "SELECT nspname FROM pg_namespace WHERE nspname = ?",
        String.class,
        "sut");

    assertThat(schema).isEqualTo("sut");
  }

  /**
   * The column {@code version} is forbidden until the commit that introduces
   * the OPTIMISTIC strategy, by ADR-0006. It is the pedagogical rule applied
   * to the schema: the problem is built before the solution exists.
   *
   * <p>Flyway's own bookkeeping table carries a {@code version} column and is
   * excluded here — it belongs to the migration tool, not to the measured
   * domain.
   */
  @Test
  void theVersionColumnIsNotInTheMeasuredDomainYet() {
    final var columns = new JdbcTemplate(this.dataSource).queryForObject(
        "SELECT count(*) FROM information_schema.columns "
            + "WHERE table_schema = 'sut' AND column_name = 'version' "
            + "AND table_name <> 'flyway_schema_history'",
        Integer.class);

    assertThat(columns).isZero();
  }

}
