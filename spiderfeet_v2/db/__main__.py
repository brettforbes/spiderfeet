"""Allow `python -m spiderfeet_v2.db` (delegates to bootstrap)."""

from spiderfeet_v2.db.bootstrap import main

if __name__ == "__main__":
    raise SystemExit(main())
