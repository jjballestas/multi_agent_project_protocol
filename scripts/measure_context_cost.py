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
DEFAULT_SLIM_COLDSTART_GLOBS = [
    "AGENTS.md",
    "Area_comun/README.md",
    "Area_comun/protocol/TASK_PROTOCOL.md",
    "Area_comun/state/PROJECT_STATE.slim.json",
    "Area_comun/state/TASK_INDEX.slim.json",
    "Area_comun/state/CLAIMS.slim.json",
]
SLIM_VIEW_FILES = {
    "Area_comun/state/PROJECT_STATE.slim.json",
    "Area_comun/state/TASK_INDEX.slim.json",
    "Area_comun/state/CLAIMS.slim.json",
}


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


def virtual_file_entry(path: str, text: str, divisor: int) -> dict[str, Any]:
    chars = len(text)
    return {
        "path": path,
        "chars": chars,
        "tokens": token_count(chars, divisor),
        "virtual": True,
    }


def generated_slim_entries(root: Path, config: dict[str, Any], divisor: int) -> list[dict[str, Any]]:
    try:
        sys.path.insert(0, str(root))
        from runtime.protocol_replay import build_genesis_snapshot, build_slim_views, canonical_json_text
    except Exception:
        return []
    slim_views = build_slim_views(build_genesis_snapshot(root), config)
    return [
        virtual_file_entry(path, canonical_json_text(slim_views[path]), divisor)
        for path in sorted(slim_views)
    ]


def measure_patterns(root: Path, patterns: list[str], divisor: int, *, config: dict[str, Any] | None = None) -> dict[str, Any]:
    patterns = [str(pattern) for pattern in patterns]
    mailbox_pattern = "Area_comun/mailbox/open/*.md"
    if mailbox_pattern not in patterns:
        patterns.append(mailbox_pattern)
    files = [file_entry(root, path, divisor) for path in unique_files(root, patterns)]
    missing_slim = SLIM_VIEW_FILES.intersection(patterns) - {item["path"] for item in files}
    if missing_slim and config is not None:
        generated = {
            item["path"]: item
            for item in generated_slim_entries(root, config, divisor)
            if item["path"] in missing_slim
        }
        files.extend(generated[path] for path in sorted(generated))
        files = sorted(files, key=lambda item: item["path"])
    return {
        "files": files,
        "total_chars": sum(item["chars"] for item in files),
        "total_tokens": sum(item["tokens"] for item in files),
    }


def measure_cold_start(root: Path, config: dict[str, Any], divisor: int) -> dict[str, Any]:
    token_config = config.get("token_cost") or {}
    patterns = token_config.get("coldstart_globs") or DEFAULT_COLDSTART_GLOBS
    return measure_patterns(root, patterns, divisor, config=config)


def measure_cold_start_modes(root: Path, config: dict[str, Any], divisor: int) -> dict[str, Any]:
    full = measure_patterns(root, DEFAULT_COLDSTART_GLOBS, divisor, config=config)
    slim = measure_patterns(root, DEFAULT_SLIM_COLDSTART_GLOBS, divisor, config=config)
    target_tokens = 10000
    return {
        "full": full,
        "slim": slim,
        "delta_tokens": full["total_tokens"] - slim["total_tokens"],
        "delta_chars": full["total_chars"] - slim["total_chars"],
        "target_tokens": target_tokens,
        "slim_within_target": slim["total_tokens"] < target_tokens,
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


def runtime_context_policy(config: dict[str, Any]) -> dict[str, Any]:
    runtime = config.get("runtime") if isinstance(config.get("runtime"), dict) else {}
    raw = runtime.get("context_policy") if isinstance(runtime.get("context_policy"), dict) else {}
    return {
        "compaction_enabled": bool(raw.get("compaction_enabled") is True),
        "recent_turn_summaries": int(raw.get("recent_turn_summaries") or 3),
        "task_close_summary_max_tokens": int(raw.get("task_close_summary_max_tokens") or 2000),
        "subagents_enabled": bool(raw.get("subagents_enabled") is True),
        "subagent_summary_max_tokens": int(raw.get("subagent_summary_max_tokens") or 2000),
        "assembled_context_warn_tokens": raw.get("assembled_context_warn_tokens"),
        "consolidation_tool_call_count": int(raw.get("consolidation_tool_call_count") or 10),
        "consolidation_overhead_budget_pct": int(raw.get("consolidation_overhead_budget_pct") or 5),
    }


def task_spec_paths(root: Path, task: dict[str, Any]) -> list[str]:
    value = str(task.get("spec_id") or "").strip()
    if not value or value.lower() == "none":
        return []
    if value.endswith(".md") or "/" in value or "\\" in value:
        return [value.replace("\\", "/")]
    spec_dir = root / "Area_comun/specs"
    return [path.relative_to(root).as_posix() for path in sorted(spec_dir.glob(f"{value}*.md"))]


def task_context_file_tokens(root: Path, paths: list[str], divisor: int) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for relative in sorted(dict.fromkeys(paths)):
        path = root / relative
        if not path.exists() or not path.is_file():
            continue
        files.append(file_entry(root, path, divisor))
    return {
        "files": files,
        "total_chars": sum(item["chars"] for item in files),
        "total_tokens": sum(item["tokens"] for item in files),
    }


def measure_turn_context(root: Path, config: dict[str, Any], divisor: int) -> dict[str, Any]:
    tasks = [
        task
        for task in load_json(root / "Area_comun/state/TASK_INDEX.json").get("tasks") or []
        if str(task.get("status") or "").lower() in {"ready", "claimed", "in_progress", "in_review", "blocked"}
    ]
    compact_sources = list((config.get("token_cost") or {}).get("coldstart_globs") or DEFAULT_SLIM_COLDSTART_GLOBS)
    legacy_sources = list(DEFAULT_COLDSTART_GLOBS)
    entries: list[dict[str, Any]] = []
    for task in tasks:
        specs = task_spec_paths(root, task)
        compact = task_context_file_tokens(root, [*compact_sources, *specs], divisor)
        legacy = task_context_file_tokens(root, [*legacy_sources, *specs], divisor)
        entries.append(
            {
                "task_id": task.get("id"),
                "status": task.get("status"),
                "with_compaction": compact,
                "without_compaction": legacy,
                "delta_tokens": legacy["total_tokens"] - compact["total_tokens"],
                "delta_chars": legacy["total_chars"] - compact["total_chars"],
            }
        )
    return {
        "context_policy": runtime_context_policy(config),
        "tasks": entries,
        "total_with_compaction_tokens": sum(item["with_compaction"]["total_tokens"] for item in entries),
        "total_without_compaction_tokens": sum(item["without_compaction"]["total_tokens"] for item in entries),
        "total_delta_tokens": sum(item["delta_tokens"] for item in entries),
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
        "cold_start_modes": measure_cold_start_modes(root, config, divisor),
        "dead_weight": measure_dead_weight(root),
        "mailbox_overhead": measure_mailbox_overhead(root, divisor),
        "turn_context": measure_turn_context(root, config, divisor),
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
    modes = result.get("cold_start_modes") or {}
    if modes:
        print("Cold-start modes")
        print(f"  full_tokens: {modes['full']['total_tokens']}")
        print(f"  slim_tokens: {modes['slim']['total_tokens']}")
        print(f"  delta_tokens: {modes['delta_tokens']}")
        print(f"  slim_within_target: {modes['slim_within_target']}")
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
    turn_context = result.get("turn_context") or {}
    if turn_context:
        print("")
        print("Turn context")
        print(f"  with_compaction_tokens: {turn_context['total_with_compaction_tokens']}")
        print(f"  without_compaction_tokens: {turn_context['total_without_compaction_tokens']}")
        print(f"  delta_tokens: {turn_context['total_delta_tokens']}")
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
    parser.add_argument("--baseline", action="store_true", help="Emit parseable baseline JSON (alias for --json with baseline metadata).")
    parser.add_argument("--budget", action="store_true", help="Evaluate token_cost.budget as warning.")
    parser.add_argument("--output", help="Write JSON output to this path.")
    args = parser.parse_args()

    result = measure(Path(args.root).resolve())
    if args.baseline:
        result["baseline"] = {"schema_version": "context_baseline.v1", "measured_with": "measure_context_cost"}
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    elif args.json_output or args.baseline:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result, args.budget)
    return 0


if __name__ == "__main__":
    sys.exit(main())
