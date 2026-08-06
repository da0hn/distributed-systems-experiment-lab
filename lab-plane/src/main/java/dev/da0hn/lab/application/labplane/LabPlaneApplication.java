package dev.da0hn.lab.application.labplane;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point of the Lab Plane, the instrument that measures.
 *
 * <p>ADR-0008 names {@code dev.da0hn.lab.application} as the composition
 * region. With three executables, a single package there would be split
 * across three artifacts, so each one gets its own leaf. Component scanning
 * is therefore declared explicitly: the region this process owns lives under
 * {@code dev.da0hn.lab.labplane}, one level above this class.
 */
@SpringBootApplication(scanBasePackages = {
    "dev.da0hn.lab.labplane",
    "dev.da0hn.lab.application.labplane"
})
public class LabPlaneApplication {

  public static void main(final String[] args) {
    SpringApplication.run(LabPlaneApplication.class, args);
  }

}
