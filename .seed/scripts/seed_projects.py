#!/usr/bin/env python3
"""CLI entrypoint for SPEC-013 project seeding (R13-07).

Delegates to ``spiderfeet_v2.workflow.seed_projects``.

Usage:
  poetry run python .seed/scripts/seed_projects.py
  poetry run python .seed/scripts/seed_projects.py --dry-run
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spiderfeet_v2.workflow.seed_projects import main

if __name__ == "__main__":
    raise SystemExit(main())
