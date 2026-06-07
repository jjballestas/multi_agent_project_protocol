#!/usr/bin/env python3
"""Measure protocol context cost with a deterministic chars/token proxy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_COLDSTART_GLOBS = [
    "AGENTS.md",
    "Area_comun/README.md",
    "Area_comun/protocol/TASK_PROTOCOL.md",
    "Area_comun/state/PROJECT_STATE.json",
    "Area_comun/state/TASK_INDEX.json",
    "Area_comun/state/CLAIMS.json",
]


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        return handle.read()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def token_count(char_count: int, divisor: int) -> int:
    if divisor <= 0:
        divisor = 4
    return char_count // divisor


def unique_files(root: Path, patterns: list[str]) -> list[Path]:
    files: dict[str, Path] = {}
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                files[relative] = path
    return [files[key] for key in sorted(files)]


def file_entry(root: Path, path: Path, divisor: int) -> dict[str, Any]:
    text = read_text(path)
    chars = len(text)
    return {
        "path": path.relative_to(root).as_posix(),
        "chars": chars,
        "tokens": token_count(chars, divisor),
    }


def measure_cold_start(root: Path, config: dict[str, Any], divisor: int) -> dict[str, Any]:
    token_config = config.get("token_cost") or {}
    patterns = token_config.get("coldstart_globs") or DEFAULT_COLDSTART_GLOBS
    patterns = [str(pattern) for pattern in patterns]
    mailbox_pattern = "Area_comun/mailbox/open/*.md"
    if mailbox_pattern not in patterns:
        patterns.append(mailbox_pattern)
    files = [file_entry(root, path, divisor) for path in unique_files(root, patterns)]
    return {
        "files": files,
        "total_chars": sum(item["chars"] for item in files),
        "total_tokens": sum(item["tokens"] for item in files),
    }


def percent(part: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def measure_dead_weight(root: Path) -> dict[str, Any]:
    claims = load_json(root / "Area_comun/state/CLAIMS.json").get("claims") or []
    tasks = load_json(root / "Area_comun/state/TASK_INDEX.json").get("tasks") or []
    released_claims = [claim for claim in claims if str(claim.get("status", "")).lower() == "released"]
    done_tasks = [task for task in tasks if str(task.get("status", "")).lower() == "done"]
    return {
        "claims": {
            "total": len(claims),
            "released": len(released_claims),
            "released_percent": percent(len(released_claims), len(claims)),
        },
        "tasks": {
            "total": len(tasks),
            "done": len(done_tasks),
            "done_percent": percent(len(done_tasks), len(tasks)),
        },
    }


def split_frontmatter(text: str) -> tuple[str, str] | None:
    match = re.match(r"(?s)^---\r?\n(?P<frontmatter>.*?)\r?\n---\r?\n?(?P<body>.*)$", text)
    if not match:
        return None
    return match.group("frontmatter"), match.group("body")


def measure_mailbox_overhead(root: Path, divisor: int) -> dict[str, Any]:
    files = unique_files(root, ["Area_comun/mailbox/**/*.md"])
    entries: list[dict[str, Any]] = []
    frontmatter_chars = 0
    body_chars = 0
    for path in files:
        split = split_frontmatter(read_text(path))
        if split is None:
            continue
        frontmatter, body = split
        fm_chars = len(frontmatter)
        b_chars = len(body)
        frontmatter_chars += fm_chars
        body_chars += b_chars
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "frontmatter_chars": fm_chars,
                "body_chars": b_chars,
            }
        )
    total_chars = frontmatter_chars + body_chars
    ratio = round(frontmatter_chars / body_chars, 4) if body_chars else 0.0
    return {
        "files": entries,
        "message_count": len(entries),
        "frontmatter_chars": frontmatter_chars,
        "body_chars": body_chars,
        "frontmatter_tokens": token_count(frontmatter_chars, divisor),
        "body_tokens": token_count(body_chars, divisor),
        "frontmatter_to_body_ratio": ratio,
        "frontmatter_percent": percent(frontmatter_chars, total_chars),
    }


def measure(root: Path) -> dict[str, Any]:
    config = load_json(root / "protocol.config.json")
    token_config = config.get("token_cost") or {}
    divisor = int(token_config.get("chars_per_token") or 4)
    budget = token_config.get("budget")
    result = {
        "root": str(root),
        "chars_per_token": divisor,
        "cold_start": measure_cold_start(root, config, divisor),
        "dead_weight": measure_dead_weight(root),
        "mailbox_overhead": measure_mailbox_overhead(root, divisor),
        "budget": {
            "cold_start_tokens": budget,
            "exceeded": bool(budget is not None and measure_cold_start(root, config, divisor)["total_tokens"] > int(budget)),
        },
    }
    return result


def print_human(result: dict[str, Any], show_budget: bool) -> None:
    cold = result["cold_start"]
    dead = result["dead_weight"]
    mailbox = result["mailbox_overhead"]
    print("Context cost report")
    print(f"Root: {result['root']}")
    print(f"Chars per token: {result['chars_per_token']}")
    print("")
    print("Cold-start")
    print(f"  total_chars: {cold['total_chars']}")
    print(f"  total_tokens: {cold['total_tokens']}")
    for item in cold["files"]:
        print(f"  - {item['path']}: {item['tokens']} tok ({item['chars']} chars)")
    print("")
    print("Dead weight")
    print(
        f"  claims released: {dead['claims']['released']}/{dead['claims']['total']} "
        f"({dead['claims']['released_percent']}%)"
    )
    print(
        f"  tasks done: {dead['tasks']['done']}/{dead['tasks']['total']} "
        f"({dead['tasks']['done_percent']}%)"
    )
    print("")
    print("Mailbox frontmatter")
    print(f"  messages: {mailbox['message_count']}")
    print(f"  frontmatter/body ratio: {mailbox['frontmatter_to_body_ratio']}")
    print(f"  frontmatter_percent: {mailbox['frontmatter_percent']}%")
    if show_budget and result["budget"]["cold_start_tokens"] is not None:
        budget = result["budget"]["cold_start_tokens"]
        if result["budget"]["exceeded"]:
            print(f"WARNING: cold-start tokens {cold['total_tokens']} exceed budget {budget}")
        else:
            print(f"OK: cold-start tokens {cold['total_tokens']} within budget {budget}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure deterministic context cost.")
    parser.add_argument("--root", default=".", help="Repository or instance root.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit parseable JSON.")
    parser.add_argument("--budget", action="store_true", help="Evaluate token_cost.budget as warning.")
    args = parser.parse_args()

    result = measure(Path(args.root).resolve())
    if args.json_output:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result, args.budget)
    return 0


if __name__ == "__main__":
    sys.exit(main())
