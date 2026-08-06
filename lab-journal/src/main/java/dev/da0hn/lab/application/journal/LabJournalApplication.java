package dev.da0hn.lab.application.journal;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point of the Lab Journal, which keeps the history and serves it.
 *
 * <p>The region {@code dev.da0hn.lab.journal} is not in ADR-0008: it was
 * created by decision E-16 on 2026-08-06, and the amendment that records it
 * in the ADR has not been written yet.
 */
@SpringBootApplication(scanBasePackages = {
    "dev.da0hn.lab.journal",
    "dev.da0hn.lab.application.journal"
})
public class LabJournalApplication {

  public static void main(final String[] args) {
    SpringApplication.run(LabJournalApplication.class, args);
  }

}
