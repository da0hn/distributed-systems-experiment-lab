/**
 * Contracts visible to both planes, as fixed by ADR-0008.
 *
 * <p>Nothing here may depend on {@code dev.da0hn.lab.labplane},
 * {@code dev.da0hn.lab.journal} or {@code dev.da0hn.lab.sut}. The Maven
 * reactor already enforces it: this module declares no dependency on the
 * executable ones, so the forbidden direction is a compilation error rather
 * than a convention someone has to remember.
 *
 * <p>The package is empty on purpose. A contract is written when the
 * interface it describes exists, never before.
 */
package dev.da0hn.lab.shared;
