#!/usr/bin/env python3
"""Golden cases for Codex-loop cutover to submit_intent --intents."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.eventlog import read_jsonl_torn_safe  # noqa: E402
from runtime.ledger_ops import auto_claim_envelope, handoff_release_envelope, submit_envelope  # noqa: E402
from runtime.protocol_replay import protocol_state_drift, write_genesis_reference  # noqa: E402


TASK_ID = "TASK-9500"
NEXT_TASK_ID = "TASK-9501"
CLAIM_ID = f"CLAIM-{TASK_ID}-codex"
TIMESTAMP = "2026-06-08T00:00:00Z"
DATE = "2026-06-08"
COMMIT = "cutoverfixture123"
EXPIRES_AT = "2026-06-09"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n", encoding="ascii", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def protocol_config() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "runtime": {"enabled": True, "entrypoint": "runtime/orchestrator.py"},
        "agent_registry": {
            "enabled": True,
            "agents": [
                {
                    "id": "Codex",
                    "enabled": True,
                    "capabilities": ["implementer", "orchestrator", "reviewer", "test_engineer"],
                }
            ],
        },
        "event_auth": {"enabled": False},
        "event_state": {"enabled": True, "materialize": True, "enforce": False, "authoritative": False},
        "domain_neutrality": {"enabled": True, "denylist": [], "scan_globs": [], "exempt_globs": []},
        "state_invariants": [{"path": "status", "equals": "active"}],
    }


def task(task_id: str = TASK_ID, status: str = "ready") -> dict[str, Any]:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": status,
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "title": f"Cutover loop fixture {task_id}",
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "relates_to": [],
        "relevant_files": [],
        "deliverables": [],
        "blocked_by_questions": [],
        "updated_at": DATE,
    }


def active_task(task_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": task_payload["id"],
        "owner": task_payload["owner"],
        "status": task_payload["status"],
        "title": task_payload["title"],
    }


def claim_scope() -> list[str]:
    return [
        f"Area_comun/tasks/{TASK_ID}.md",
        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
        f"Area_comun/state/TASK_INDEX.json#{NEXT_TASK_ID}",
        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{NEXT_TASK_ID}",
        "Area_comun/state/CLAIMS.json",
    ]


def next_task() -> dict[str, Any]:
    return task(NEXT_TASK_ID, "ready")


def write_hot_state(root: Path, status: str = "ready") -> None:
    task_payload = task(TASK_ID, status)
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [task_payload]})
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "decisions": ["DECISION-0001"], "active_tasks": [active_task(task_payload)]},
    )
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write(root / "Area_comun/tasks" / f"{TASK_ID}.md", f"---\nid: {TASK_ID}\nstatus: {status}\n---\n\n# Fixture\n")
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "\n")


def build_fixture(root: Path) -> None:
    write_json(root / "protocol.config.json", protocol_config())
    write_hot_state(root)
    write_genesis_reference(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)


def event_count(root: Path) -> int:
    return len(read_jsonl_torn_safe(root / "runtime/state/events.jsonl"))


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def task_status(root: Path, task_id: str) -> str:
    tasks = {item["id"]: item for item in read_json(root / "Area_comun/state/TASK_INDEX.json")["tasks"]}
    return str(tasks[task_id]["status"])


def project_task_status(root: Path, task_id: str) -> str:
    tasks = {item["id"]: item for item in read_json(root / "Area_comun/state/PROJECT_STATE.json")["active_tasks"]}
    return str(tasks[task_id]["status"])


def claim_status(root: Path, claim_id: str) -> str:
    claims = {item["claim_id"]: item for item in read_json(root / "Area_comun/state/CLAIMS.json")["claims"]}
    return str(claims[claim_id]["status"])


def task_file_status(root: Path, task_id: str) -> str:
    text = (root / "Area_comun/tasks" / f"{task_id}.md").read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"task file has no status: {task_id}")


def assert_shadow_flags(root: Path) -> None:
    event_state = read_json(root / "protocol.config.json")["event_state"]
    assert event_state["enforce"] is False
    assert event_state["authoritative"] is False


def auto_claim() -> dict[str, Any]:
    return auto_claim_envelope(
        actor_id="Codex",
        timestamp=TIMESTAMP,
        commit=COMMIT,
        task_id=TASK_ID,
        claim_id=CLAIM_ID,
        scope=claim_scope(),
        expires_at=EXPIRES_AT,
        started_at=DATE,
        updated_at=DATE,
        notes="cutover loop fixture claim",
    )


def handoff_release() -> dict[str, Any]:
    return handoff_release_envelope(
        actor_id="Codex",
        timestamp=TIMESTAMP,
        commit=COMMIT,
        task_id=TASK_ID,
        claim_id=CLAIM_ID,
        task_upserts=[next_task()],
    )


def case_auto_claim_and_handoff_release_are_transactional_and_idempotent() -> None:
    with tempfile.TemporaryDirectory(prefix="cutover-loop-") as temp:
        root = Path(temp)
        build_fixture(root)
        assert protocol_state_drift(root)["has_drift"] is False
        before = event_count(root)

        acquired = submit_envelope(root, auto_claim())
        assert acquired["transaction"]["intent_count"] == 2
        assert event_count(root) == before + 2
        assert task_status(root, TASK_ID) == "in_progress"
        assert project_task_status(root, TASK_ID) == "in_progress"
        assert task_file_status(root, TASK_ID) == "in_progress"
        assert claim_status(root, CLAIM_ID) == "active"
        assert protocol_state_drift(root)["has_drift"] is False
        assert_shadow_flags(root)

        repeated_acquire = submit_envelope(root, auto_claim())
        assert repeated_acquire["deduped"] is True
        assert event_count(root) == before + 2
        assert task_status(root, TASK_ID) == "in_progress"

        released = submit_envelope(root, handoff_release())
        assert released["transaction"]["intent_count"] == 3
        assert event_count(root) == before + 5
        assert task_status(root, TASK_ID) == "in_review"
        assert project_task_status(root, TASK_ID) == "in_review"
        assert task_file_status(root, TASK_ID) == "in_review"
        assert task_status(root, NEXT_TASK_ID) == "ready"
        assert project_task_status(root, NEXT_TASK_ID) == "ready"
        assert claim_status(root, CLAIM_ID) == "released"
        assert protocol_state_drift(root)["has_drift"] is False
        assert_shadow_flags(root)

        repeated_release = submit_envelope(root, handoff_release())
        assert repeated_release["deduped"] is True
        assert event_count(root) == before + 5


def case_python_cli_builds_same_auto_claim_envelope() -> None:
    expected = auto_claim()
    result = run(
        [
            sys.executable,
            str(ROOT / "runtime/ledger_ops.py"),
            "--operation",
            "auto-claim",
            "--actor-id",
            "Codex",
            "--timestamp",
            TIMESTAMP,
            "--commit",
            COMMIT,
            "--task-id",
            TASK_ID,
            "--claim-id",
            CLAIM_ID,
            "--expires-at",
            EXPIRES_AT,
            "--started-at",
            DATE,
            "--updated-at",
            DATE,
            "--notes",
            "cutover loop fixture claim",
            *[arg for item in claim_scope() for arg in ("--scope", item)],
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == expected


def case_cli_submit_delegates_to_submit_intents() -> None:
    with tempfile.TemporaryDirectory(prefix="cutover-loop-cli-") as temp:
        root = Path(temp)
        build_fixture(root)
        result = run(
            [
                sys.executable,
                str(ROOT / "runtime/ledger_ops.py"),
                "--root",
                str(root),
                "--operation",
                "auto-claim",
                "--actor-id",
                "Codex",
                "--timestamp",
                TIMESTAMP,
                "--commit",
                COMMIT,
                "--task-id",
                TASK_ID,
                "--claim-id",
                CLAIM_ID,
                "--expires-at",
                EXPIRES_AT,
                "--started-at",
                DATE,
                "--updated-at",
                DATE,
                *[arg for item in claim_scope() for arg in ("--scope", item)],
                "--submit",
            ]
        )
        assert result.returncode == 0, result.stdout + result.stderr
        payload = json.loads(result.stdout)
        assert payload["transaction"]["intent_count"] == 2
        assert task_status(root, TASK_ID) == "in_progress"
        assert claim_status(root, CLAIM_ID) == "active"
        assert protocol_state_drift(root)["has_drift"] is False
        assert_shadow_flags(root)


def case_powershell_wrapper_parity_if_available() -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return
    result = run(
        [
            shell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "runtime/ledger_ops.ps1"),
            "-Operation",
            "auto-claim",
            "-ActorId",
            "Codex",
            "-Timestamp",
            TIMESTAMP,
            "-Commit",
            COMMIT,
            "-TaskId",
            TASK_ID,
            "-ClaimId",
            CLAIM_ID,
            "-Scope",
            ",".join(claim_scope()),
            "-ExpiresAt",
            EXPIRES_AT,
            "-StartedAt",
            DATE,
            "-UpdatedAt",
            DATE,
            "-Notes",
            "cutover loop fixture claim",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == auto_claim()


def main() -> int:
    cases = [
        case_auto_claim_and_handoff_release_are_transactional_and_idempotent,
        case_python_cli_builds_same_auto_claim_envelope,
        case_cli_submit_delegates_to_submit_intents,
        case_powershell_wrapper_parity_if_available,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} cutover loop golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
