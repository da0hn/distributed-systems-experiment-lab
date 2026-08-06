package dev.da0hn.lab.application.labplane;

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
class LabPlaneApplicationTests {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres =
      new PostgreSQLContainer<>("postgres:18-alpine");

  @Autowired
  private DataSource dataSource;

  /**
   * A schema that does not exist is the failure this test exists to catch.
   *
   * <p>Booting the context is not enough: a missing Flyway auto-configuration
   * leaves the driver on the classpath, the health check green and the schema
   * absent — the whole boundary of decision E-18 declared in configuration and
   * missing from the database. That combination already happened here once.
   */
  @Test
  void flywayCreatesTheSchemaThisProcessOwns() {
    final var schema = new JdbcTemplate(this.dataSource).queryForObject(
        "SELECT nspname FROM pg_namespace WHERE nspname = ?",
        String.class,
        "lab_plane");

    assertThat(schema).isEqualTo("lab_plane");
  }

}
