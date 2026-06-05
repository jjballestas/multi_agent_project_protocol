#!/usr/bin/env python3
"""Runtime M0 orchestrator entry point.

M0 is intentionally read-only: --plan prints the deterministic next action and
does not invoke agents or mutate protocol state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .context import load_state
    from .router import select_next
except ImportError:  # pragma: no cover - direct script execution
    from context import load_state
    from router import select_next


def main() -> int:
    parser = argparse.ArgumentParser(description="Protocol runtime orchestrator.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--plan", action="store_true", help="Dry-run: print next action without mutating state")
    args = parser.parse_args()

    if not args.plan:
        parser.error("M0 only supports --plan dry-run")

    result = select_next(load_state(Path(args.root)))
    print(json.dumps({"dry_run": True, "next": result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
