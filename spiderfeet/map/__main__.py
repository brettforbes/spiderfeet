"""CLI: python -m spiderfeet.map [--config PATH]"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from spiderfeet.map.bootstrap import bootstrap_map
from spiderfeet.map.config import TypeDBConfigError, load_connection_config
from spiderfeet.map.connection import ping

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap spiderfeet-map in TypeDB")
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to typedb.connection.json (default: .config/typedb.connection.json)",
    )
    parser.add_argument(
        "--ping-only",
        action="store_true",
        help="Only test server connectivity",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate the map database before bootstrap",
    )
    args = parser.parse_args(argv)

    try:
        from pathlib import Path

        cfg = load_connection_config(Path(args.config) if args.config else None)
    except TypeDBConfigError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.ping_only:
        ok = ping(cfg)
        print("ok" if ok else "unreachable")
        return 0 if ok else 1

    report = bootstrap_map(cfg, reset=args.reset)
    print(json.dumps(report.__dict__, indent=2))
    if not report.ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
