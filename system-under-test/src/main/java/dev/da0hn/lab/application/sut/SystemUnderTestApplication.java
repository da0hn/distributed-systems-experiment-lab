package dev.da0hn.lab.application.sut;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point of the system under test, the measured system.
 *
 * <p>Three rules of this repository apply to everything under
 * {@code dev.da0hn.lab.sut} and to nothing else: no JVM synchronization, no
 * unseeded randomness, and no direct clock reading. They are text today, not
 * an executable guard — see Q-0002-1 and decisions D-ARQ-07 to D-ARQ-09.
 */
@SpringBootApplication(scanBasePackages = {
    "dev.da0hn.lab.sut",
    "dev.da0hn.lab.application.sut"
})
public class SystemUnderTestApplication {

  public static void main(final String[] args) {
    SpringApplication.run(SystemUnderTestApplication.class, args);
  }

}
