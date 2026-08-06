package dev.da0hn.lab.application.journal;

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
class LabJournalApplicationTests {

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
        "lab_journal");

    assertThat(schema).isEqualTo("lab_journal");
  }

}
