#!/usr/bin/env python3
"""Deterministic fake backend for llm_turn_wrapper golden cases."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture")
    parser.add_argument("--exit-code", type=int, default=0)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--stderr", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _prompt = sys.stdin.read()
    if args.sleep_seconds:
        time.sleep(args.sleep_seconds)
    if args.stderr:
        print(args.stderr, file=sys.stderr)
    if args.fixture:
        sys.stdout.write(Path(args.fixture).read_text(encoding="utf-8"))
    return int(args.exit_code)


if __name__ == "__main__":
    raise SystemExit(main())
