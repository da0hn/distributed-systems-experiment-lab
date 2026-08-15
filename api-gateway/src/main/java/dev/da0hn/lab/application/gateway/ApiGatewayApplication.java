package dev.da0hn.lab.application.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point of the API gateway, the single HTTP entry point of the lab.
 *
 * <p>Every executable gets its own leaf under
 * {@code dev.da0hn.lab.application}; a single package there would be split
 * across distinct artifacts. This one owns no region of its own: routing is
 * declared in configuration, so there is no business package to scan.
 *
 * <p>This process belongs to neither plane. It does not measure and it is not
 * measured — it forwards. Anything that composes a response out of two
 * services would make it a BFF, and the frontend deliberately talks to the
 * services it needs instead of to an aggregator.
 */
@SpringBootApplication
public class ApiGatewayApplication {

  public static void main(final String[] args) {
    SpringApplication.run(ApiGatewayApplication.class, args);
  }

}
