#!/usr/bin/env python3
"""Read-only aggregator of REAL token usage per agent/task from cron run logs.

Each governed agent runs through a mailbox cron (`.protocol-tmp/<id>_mailbox_cron/runs/*.err.log`)
whose CLI prints a "tokens used" line followed by the count (dot/comma thousands separators). This
script attributes those tokens to the agent (derived from the cron directory name) and the task
(parsed from the run filename), with NO side effects: it never writes the ledger or protocol state.
It only reads run logs, so it is safe to call from the read-only panel bridge.

Note: an agent that runs as an interactive session (not a mailbox cron) leaves no run log here, so it
shows zero tokens by construction. Agent identities are derived from the cron directory at runtime;
no identity is hard-coded (keeps the script domain/identity neutral).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TASK_RE = re.compile(r"(TASK-\d{1,8})", re.IGNORECASE)
TOKENS_LINE_RE = re.compile(r"tokens?\s+used", re.IGNORECASE)
DIGITS_RE = re.compile(r"\d[\d.,]*")


def agent_for_cron(cron_dir_name: str) -> str:
    base = cron_dir_name.replace("_mailbox_cron", "").replace("_cron", "").strip("_")
    return base[:1].upper() + base[1:] if base else "none"


def parse_token_count(lines: list[str], start: int) -> int:
    for offset in range(0, 4):
        idx = start + offset
        if idx >= len(lines):
            break
        match = DIGITS_RE.search(lines[idx])
        if match:
            digits = re.sub(r"[^\d]", "", match.group(0))
            if digits:
                return int(digits)
    return 0


def tokens_from_log(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    lines = text.splitlines()
    total = 0
    for i, line in enumerate(lines):
        if TOKENS_LINE_RE.search(line):
            tail = line[line.lower().find("used") + 4:] if "used" in line.lower() else ""
            same = DIGITS_RE.search(tail)
            if same and re.sub(r"[^\d]", "", same.group(0)):
                total += int(re.sub(r"[^\d]", "", same.group(0)))
            else:
                total += parse_token_count(lines, i + 1)
    return total


def collect(root: Path) -> dict:
    tmp = root / ".protocol-tmp"
    rows: list[dict] = []
    if tmp.exists():
        for runs_dir in sorted(tmp.glob("*/runs")):
            agent = agent_for_cron(runs_dir.parent.name)
            for log in sorted(runs_dir.glob("*.err.log")):
                tokens = tokens_from_log(log)
                if tokens <= 0:
                    continue
                task_match = TASK_RE.search(log.name)
                task_id = task_match.group(1).upper() if task_match else "none"
                rows.append({"agent": agent, "task_id": task_id, "tokens": tokens, "run": log.name})

    por_agente: dict[str, dict] = {}
    por_tarea: dict[str, dict] = {}
    total = 0
    for row in rows:
        total += row["tokens"]
        agent_bucket = por_agente.setdefault(row["agent"], {"tokens": 0, "runs": 0})
        agent_bucket["tokens"] += row["tokens"]
        agent_bucket["runs"] += 1
        task_bucket = por_tarea.setdefault(row["task_id"], {})
        task_bucket[row["agent"]] = task_bucket.get(row["agent"], 0) + row["tokens"]

    return {
        "fuente": "cron run logs (.protocol-tmp/*/runs/*.err.log; CLI 'tokens used')",
        "total_tokens": total,
        "runs": len(rows),
        "por_agente": dict(sorted(por_agente.items())),
        "por_tarea": dict(sorted(por_tarea.items())),
        "nota": "Un agente que corre como sesion interactiva (sin cron) no se loguea aqui; muestra 0 por construccion.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate read-only per-agent token usage from cron run logs.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    print(json.dumps(collect(Path(args.root).resolve()), indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
