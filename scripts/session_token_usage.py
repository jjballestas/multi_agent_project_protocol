#!/usr/bin/env python3
"""Read-only aggregator of REAL token usage for an INTERACTIVE agent session.

Cron-driven agents leave a CLI run log (see agent_token_usage.py). An agent that runs as an interactive
assistant session does NOT; its real usage lives in the session transcripts the assistant harness writes
to disk (one JSONL per session, each assistant message carrying a `usage` object with
input/output/cache token counts). This script sums those into a single agent's token cost, with NO side
effects: it only reads transcript files.

Identity-neutral: the agent id and the transcripts directory are passed in (no identity or host path is
hard-coded). "tokens" reports input+output (the billable, peer-comparable figure); cache reads are
reported separately because they dominate the raw count but are not a comparable cost.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def collect(transcripts_dir: Path, agent: str) -> dict:
    input_tokens = output_tokens = cache_tokens = messages = sessions = 0
    if transcripts_dir.exists():
        for path in sorted(transcripts_dir.glob("*.jsonl")):
            sessions += 1
            try:
                handle = path.open("r", encoding="utf-8", errors="replace")
            except OSError:
                continue
            with handle:
                for line in handle:
                    if '"usage"' not in line:
                        continue
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    message = event.get("message") if isinstance(event.get("message"), dict) else None
                    usage = (message or {}).get("usage") if message else event.get("usage")
                    if not isinstance(usage, dict):
                        continue
                    input_tokens += int(usage.get("input_tokens", 0) or 0)
                    output_tokens += int(usage.get("output_tokens", 0) or 0)
                    cache_tokens += int(usage.get("cache_creation_input_tokens", 0) or 0)
                    cache_tokens += int(usage.get("cache_read_input_tokens", 0) or 0)
                    messages += 1

    tokens = input_tokens + output_tokens
    return {
        "fuente": "session transcripts (assistant harness; message.usage input+output)",
        "agente": agent,
        "tokens": tokens,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_tokens": cache_tokens,
        "sessions": sessions,
        "messages": messages,
        "por_agente": {agent: {"tokens": tokens, "runs": sessions}} if tokens > 0 else {},
        "nota": "tokens = input+output (billable); cache_tokens (lecturas de cache) se reporta aparte por no ser comparable.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate read-only interactive-session token usage.")
    parser.add_argument("--transcripts", required=True, help="Directory of session transcript *.jsonl files.")
    parser.add_argument("--agent", required=True, help="Agent id these interactive sessions belong to.")
    args = parser.parse_args()
    print(json.dumps(collect(Path(args.transcripts).expanduser(), str(args.agent)), indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
