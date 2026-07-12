#!/usr/bin/env python3
"""Thin wrapper to compose _Current_Ontology.md (SPEC-006 Epic O)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_CORPUS_DIR = Path(__file__).resolve().parent
if str(_CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(_CORPUS_DIR))

from core.structure_doc_engine import write_ontology_doc  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose _Current_Ontology.md from structure packs")
    parser.add_argument("--dry-run", action="store_true", help="Report target path without writing")
    args = parser.parse_args()
    path = write_ontology_doc(dry_run=args.dry_run)
    if args.dry_run:
        print(f"dry-run: would write {path}")
    else:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
