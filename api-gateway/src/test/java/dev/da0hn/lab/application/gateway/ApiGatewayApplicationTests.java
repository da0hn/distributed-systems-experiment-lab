package dev.da0hn.lab.application.gateway;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.gateway.route.Route;
import org.springframework.cloud.gateway.route.RouteLocator;

@SpringBootTest
class ApiGatewayApplicationTests {

  @Autowired
  private RouteLocator routeLocator;

  /**
   * A gateway with no routes is the failure this test exists to catch.
   *
   * <p>Booting the context proves nothing here. The property that declares
   * routes moved namespace between Spring Cloud Gateway versions, and a
   * misspelled prefix is not an error: unknown configuration is ignored, the
   * context starts, the health check is green, and every request falls through
   * to a 404. Nothing points at the configuration.
   */
  @Test
  void routesAreLoadedFromConfiguration() {
    final List<String> ids = this.routeLocator.getRoutes()
        .map(Route::getId)
        .collectList()
        .block();

    assertThat(ids).containsExactlyInAnyOrder("lab-plane", "lab-journal");
  }

  /**
   * No route may match a path outside {@code /api}.
   *
   * <p>The edge proxy serves the interface and forwards only {@code /api} here,
   * so a catch-all would be dead configuration in production and a trap in
   * diagnostics: a request to this process's own port would answer 200 with
   * whatever the catch-all points at, instead of the 404 that says the API
   * route does not exist. The assertion is on the predicate because a route
   * added later carries its own, and nothing else would notice.
   */
  @Test
  void everyRouteIsScopedToTheApiPrefix() {
    final List<String> predicates = this.routeLocator.getRoutes()
        .map(route -> route.getPredicate().toString())
        .collectList()
        .block();

    assertThat(predicates).allMatch(predicate -> predicate.contains("/api/"));
  }

  /**
   * The measured system must not be reachable through the gateway.
   *
   * <p>A request made by hand during a measured window counts in the exact
   * oracle as a real commit, and nothing tells it apart from the experiment's
   * own load — the verdict comes out wrong with no error anywhere. Adding a
   * route for it would be a one-line change, so the absence is asserted.
   */
  @Test
  void theMeasuredSystemHasNoRoute() {
    final List<String> targets = this.routeLocator.getRoutes()
        .map(route -> route.getUri().toString())
        .collectList()
        .block();

    assertThat(targets).noneMatch(uri -> uri.contains("system-under-test"));
  }

}
