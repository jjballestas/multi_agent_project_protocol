#!/usr/bin/env python3
"""Golden cases for TASK-0105 slim views."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.protocol_replay import (  # noqa: E402
    build_genesis_snapshot,
    build_slim_views,
    canonical_json_text,
    current_protocol_snapshot,
    materialize_to_disk,
    protocol_state_drift,
    slim_view_drift,
    write_genesis_reference,
)
from scripts.measure_context_cost import measure  # noqa: E402


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_text(payload), encoding="ascii", newline="\n")


def base_config(*, slim: bool, coldstart_slim: bool = False) -> dict[str, Any]:
    coldstart = [
        "AGENTS.md",
        "Area_comun/README.md",
        "Area_comun/protocol/TASK_PROTOCOL.md",
        "Area_comun/state/PROJECT_STATE.json",
        "Area_comun/state/TASK_INDEX.json",
        "Area_comun/state/CLAIMS.json",
    ]
    if coldstart_slim:
        coldstart = [
            "AGENTS.md",
            "Area_comun/README.md",
            "Area_comun/protocol/TASK_PROTOCOL.md",
            "Area_comun/state/PROJECT_STATE.slim.json",
            "Area_comun/state/TASK_INDEX.slim.json",
            "Area_comun/state/CLAIMS.slim.json",
        ]
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_registry": {
            "enabled": True,
            "agents": [
                {"id": "golden", "enabled": True, "capabilities": ["implementer", "orchestrator"]},
            ],
        },
        "token_cost": {"chars_per_token": 4, "coldstart_globs": coldstart, "budget": 30000},
        "maintenance": {"recent_next_actions": 2},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "slim_views_enabled": slim,
        },
    }


def state_docs() -> dict[str, dict[str, Any]]:
    return {
        "task_index": {
            "schema_version": "1.0",
            "tasks": [
                {
                    "id": "TASK-0001",
                    "status": "ready",
                    "owner": "Codex",
                    "phase": "P2",
                    "priority": "high",
                    "title": "Hot task",
                    "deliverables": ["not-in-slim"],
                },
                {
                    "id": "TASK-0002",
                    "status": "blocked",
                    "owner": "Claude",
                    "phase": "P2",
                    "priority": "normal",
                    "title": "Blocked task",
                    "blocked_by_questions": ["Question?"],
                },
                {
                    "id": "TASK-0003",
                    "status": "done",
                    "owner": "Codex",
                    "phase": "P2",
                    "priority": "low",
                    "title": "Done task",
                },
                {
                    "id": "TASK-0004",
                    "status": "cancelled",
                    "owner": "Claude",
                    "phase": "P2",
                    "priority": "low",
                    "title": "Cancelled task",
                },
            ],
        },
        "project_state": {
            "status": "active",
            "decisions": ["DECISION-0001"],
            "active_tasks": [
                {"id": "TASK-0001", "status": "ready", "owner": "Codex", "title": "Hot task"},
                {"id": "TASK-0003", "status": "done", "owner": "Codex", "title": "Done task"},
            ],
            "next_actions": ["old", "middle", "new"],
            "risks": ["risk-old", "risk-new"],
            "open_questions": ["open-old", "open-new"],
        },
        "claims": {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": "CLAIM-1",
                    "task_id": "TASK-0001",
                    "owner": "Codex",
                    "status": "active",
                    "scope": ["runtime/protocol_replay.py"],
                },
                {
                    "claim_id": "CLAIM-2",
                    "task_id": "TASK-0003",
                    "owner": "Claude",
                    "status": "released",
                    "scope": ["Area_comun/state/CLAIMS.json"],
                },
            ],
        },
    }


def make_repo(slim: bool = True, *, coldstart_slim: bool = False) -> Path:
    tmp_parent = ROOT / ".tmp"
    tmp_parent.mkdir(exist_ok=True)
    root = tmp_parent / f"slim-view-case-{uuid.uuid4().hex}"
    root.mkdir()
    for relative, text in {
        "AGENTS.md": "agents\n",
        "Area_comun/README.md": "readme\n",
        "Area_comun/protocol/TASK_PROTOCOL.md": "task protocol\n",
    }.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="ascii", newline="\n")
    docs = state_docs()
    write_json(root / "protocol.config.json", base_config(slim=slim, coldstart_slim=coldstart_slim))
    write_json(root / "Area_comun/state/TASK_INDEX.json", docs["task_index"])
    write_json(root / "Area_comun/state/PROJECT_STATE.json", docs["project_state"])
    write_json(root / "Area_comun/state/CLAIMS.json", docs["claims"])
    write_genesis_reference(
        root,
        actor_id="golden",
        timestamp="2026-06-13T00:00:00Z",
        idempotency_key="golden:genesis",
    )
    return root


def cleanup(root: Path) -> None:
    shutil.rmtree(root, ignore_errors=True)


def gc_1_derivation_happy_path() -> None:
    root = make_repo()
    try:
        slim = build_slim_views(build_genesis_snapshot(root), base_config(slim=True))
        tasks = slim["Area_comun/state/TASK_INDEX.slim.json"]["tasks"]
        assert [task["id"] for task in tasks] == ["TASK-0001", "TASK-0002"]
        assert "deliverables" not in tasks[0]
        assert tasks[1]["blocked_by_questions"] == ["Question?"]
        project = slim["Area_comun/state/PROJECT_STATE.slim.json"]
        assert [task["id"] for task in project["active_tasks"]] == ["TASK-0001"]
        assert project["next_actions"] == ["middle", "new"]
        claims = slim["Area_comun/state/CLAIMS.slim.json"]["claims"]
        assert [claim["claim_id"] for claim in claims] == ["CLAIM-1"]
    finally:
        cleanup(root)


def gc_2_terminal_filter() -> None:
    root = make_repo()
    try:
        slim = build_slim_views(build_genesis_snapshot(root), base_config(slim=True))
        ids = {task["id"] for task in slim["Area_comun/state/TASK_INDEX.slim.json"]["tasks"]}
        assert "TASK-0003" not in ids
        assert "TASK-0004" not in ids
        claim_ids = {claim["claim_id"] for claim in slim["Area_comun/state/CLAIMS.slim.json"]["claims"]}
        assert "CLAIM-2" not in claim_ids
    finally:
        cleanup(root)


def gc_3_anti_drift() -> None:
    root = make_repo()
    try:
        materialize_to_disk(root, current_protocol_snapshot(root))
        assert not slim_view_drift(root)["has_drift"]
        write_json(root / "Area_comun/state/TASK_INDEX.slim.json", {"view": "task_index.slim", "tasks": []})
        assert slim_view_drift(root)["has_drift"]
        assert protocol_state_drift(root)["has_drift"]
        intent = {
            "idempotency_key": "golden:drift-abort",
            "claim": {
                "op": "acquire",
                "task_id": "TASK-0001",
                "owner": "golden",
                "claim": {
                    "claim_id": "CLAIM-GOLDEN",
                    "task_id": "TASK-0001",
                    "owner": "golden",
                    "status": "active",
                    "scope": ["Area_comun/state/CLAIMS.json"],
                    "started_at": "2026-06-13T00:01:00Z",
                    "updated_at": "2026-06-13T00:01:00Z",
                    "expires_at": "2026-06-14",
                    "notes": "golden drift gate",
                },
            },
        }
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "runtime" / "submit_intent.py"),
                "--root",
                str(root),
                "--actor-id",
                "golden",
                "--timestamp",
                "2026-06-13T00:01:00Z",
                "--intent-json",
                json.dumps(intent, sort_keys=True),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        output = completed.stderr + completed.stdout
        assert completed.returncode != 0, output
        assert "drift" in output.lower(), output
    finally:
        cleanup(root)


def gc_4_atomic_rollback() -> None:
    root = make_repo()
    try:
        materialize_to_disk(root, current_protocol_snapshot(root))
        before = {
            path: (root / path).read_text(encoding="ascii")
            for path in [
                "Area_comun/state/CLAIMS.json",
                "Area_comun/state/CLAIMS.slim.json",
                "Area_comun/state/PROJECT_STATE.json",
                "Area_comun/state/PROJECT_STATE.slim.json",
                "Area_comun/state/TASK_INDEX.json",
                "Area_comun/state/TASK_INDEX.slim.json",
            ]
        }
        snapshot = current_protocol_snapshot(root)
        snapshot["state"]["task_index"]["tasks"][0]["title"] = "Changed"
        try:
            materialize_to_disk(root, snapshot, fail_after_writes=2)
        except Exception as exc:
            assert "simulated materialization failure" in str(exc)
        after = {path: (root / path).read_text(encoding="ascii") for path in before}
        assert before == after
    finally:
        cleanup(root)


def gc_5_flag_off() -> None:
    root = make_repo(slim=False)
    try:
        materialize_to_disk(root, current_protocol_snapshot(root))
        assert not (root / "Area_comun/state/TASK_INDEX.slim.json").exists()
        assert not slim_view_drift(root)["has_drift"]
        assert not protocol_state_drift(root)["has_drift"]
    finally:
        cleanup(root)


def gc_6_measurement() -> None:
    root = make_repo(slim=True)
    try:
        result = measure(root)
        modes = result["cold_start_modes"]
        assert modes["full"]["total_tokens"] > modes["slim"]["total_tokens"]
        assert modes["delta_tokens"] > 0
    finally:
        cleanup(root)


def gc_7_log_out_of_coldstart() -> None:
    root = make_repo(slim=True, coldstart_slim=True)
    try:
        config = json.loads((root / "protocol.config.json").read_text(encoding="utf-8"))
        globs = set(config["token_cost"]["coldstart_globs"])
        assert "runtime/state/events.jsonl" not in globs
        assert "Area_comun/state/TASK_INDEX.json" not in globs
        assert "Area_comun/state/TASK_INDEX.slim.json" in globs
    finally:
        cleanup(root)


CASES: dict[str, Callable[[], None]] = {
    "GC-1": gc_1_derivation_happy_path,
    "GC-2": gc_2_terminal_filter,
    "GC-3": gc_3_anti_drift,
    "GC-4": gc_4_atomic_rollback,
    "GC-5": gc_5_flag_off,
    "GC-6": gc_6_measurement,
    "GC-7": gc_7_log_out_of_coldstart,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run slim-view golden cases.")
    parser.add_argument("--golden-case", choices=sorted(CASES))
    args = parser.parse_args()
    selected = [args.golden_case] if args.golden_case else sorted(CASES)
    results = []
    for name in selected:
        try:
            CASES[name]()
            results.append({"case": name, "ok": True})
        except Exception as exc:
            results.append({"case": name, "ok": False, "error": str(exc)})
    print(json.dumps({"passed": sum(1 for item in results if item["ok"]), "total": len(results), "results": results}, indent=2, sort_keys=True))
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
