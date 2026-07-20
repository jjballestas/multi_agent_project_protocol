#!/usr/bin/env python3
"""Read the append-only event-log head as an exact seq/hash pair."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def event_log_head(root: Path) -> tuple[int, str]:
    path = root / "runtime/state/events.jsonl"
    if not path.exists():
        return (0, hashlib.sha256(b"").hexdigest())
    last = b""
    with path.open("rb") as handle:
        for raw_line in handle:
            if raw_line.strip():
                last = raw_line.rstrip(b"\r\n")
    if not last:
        return (0, hashlib.sha256(b"").hexdigest())
    event = json.loads(last.decode("utf-8-sig"))
    return (int(event["seq"]), hashlib.sha256(last).hexdigest())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    seq, digest = event_log_head(Path(args.root).resolve())
    print(json.dumps({"seq": seq, "hash": digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
