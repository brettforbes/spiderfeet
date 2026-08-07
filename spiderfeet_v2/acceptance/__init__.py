"""SPEC-010 Epic AP — backend acceptance harness (R10-29 / R10-30).

AP2 lands ``run_four_targets.py`` with dry-run support. AP1 (G3) owns the
live 4-target evidence sign-off — this package does not claim AP1 complete.
"""

from spiderfeet_v2.acceptance.targets import DEFAULT_TARGETS, DOCUMENTED_TARGETS

__all__ = ["DEFAULT_TARGETS", "DOCUMENTED_TARGETS"]
