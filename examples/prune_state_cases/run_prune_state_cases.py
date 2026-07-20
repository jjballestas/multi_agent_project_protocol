#!/usr/bin/env python3
"""Golden cases for scripts/prune_state.py."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "prune_state.py"
sys.path.insert(0, str(ROOT))
from scripts.prune_state import verify_archived_entries
from runtime.protocol_replay import protocol_state_drift
from runtime.regenesis import regenesis


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def task(task_id: str, status: str) -> dict:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": status,
        "file": f"Area_comun/tasks/{task_id}.md",
        "deliverables": [],
    }


def claim(claim_id: str, task_id: str, status: str) -> dict:
    return {
        "claim_id": claim_id,
        "task_id": task_id,
        "owner": "Codex",
        "status": status,
        "scope": ["Area_comun/state/CLAIMS.json"],
    }


def build_fixture(root: Path, *, done_count: int = 5, released_count: int = 8, disabled: bool = False) -> None:
    tasks = [task(f"TASK-90{i:02d}", "done") for i in range(done_count)] + [task("TASK-9999", "in_progress")]
    claims = [claim(f"CLAIM-{i:04d}", f"TASK-90{i:02d}", "released") for i in range(released_count)]
    claims.append(claim("CLAIM-active", "TASK-9999", "active"))
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "token_cost": {
                "chars_per_token": 4,
                "coldstart_globs": [
                    "Area_comun/state/PROJECT_STATE.json",
                    "Area_comun/state/TASK_INDEX.json",
                    "Area_comun/state/CLAIMS.json",
                ],
                "budget": 30000,
            },
            "maintenance": {
                "enabled": not disabled,
                "cold_start_tokens_hard": 999999,
                "done_ratio_hard": 70,
                "released_ratio_hard": 70,
                "recent_done_tasks": 1,
                "recent_released_claims": 2,
                "mailbox_keep_recent": 1,
            },
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": tasks})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": claims})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "active_tasks": [{"id": item["id"], "status": item["status"]} for item in tasks]},
    )
    for item in tasks:
        write(root / item["file"], f"---\nid: {item['id']}\nstatus: {item['status']}\n---\n")
    write(root / "Area_comun/mailbox/open/.gitkeep", "\n")
    write(root / "Area_comun/mailbox/answered/MSG-001-old.md", "---\nstatus: answered\n---\n")
    write(root / "Area_comun/mailbox/answered/MSG-002-new.md", "---\nstatus: answered\n---\n")
    write(root / "Area_comun/mailbox/archived/.gitkeep", "\n")


def run(root: Path, mode: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python", str(SCRIPT), "--root", str(root), mode], text=True, capture_output=True, check=False)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def case_due_and_apply() -> None:
    with tempfile.TemporaryDirectory(prefix="prune-due-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        assert run(fixture, "--check").returncode == 1
        first = run(fixture, "--apply")
        assert first.returncode == 0, first.stdout + first.stderr
        task_hot = load(fixture / "Area_comun/state/TASK_INDEX.json")["tasks"]
        task_archive = load(fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json")["tasks"]
        assert [item["id"] for item in task_hot] == ["TASK-9004", "TASK-9999"]
        assert len(task_archive) == 4
        assert len(load(fixture / "Area_comun/state/CLAIMS_ARCHIVE.json")["claims"]) == 6
        assert (fixture / "Area_comun/mailbox/archived/MSG-001-old.md").exists()
        second = run(fixture, "--apply")
        assert second.returncode == 0
        assert len(load(fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json")["tasks"]) == 4


def case_not_due_when_disabled() -> None:
    with tempfile.TemporaryDirectory(prefix="prune-disabled-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, disabled=True)
        check_started = time.perf_counter()
        assert run(fixture, "--check").returncode == 0
        check_elapsed = time.perf_counter() - check_started
        before = load(fixture / "Area_comun/state/TASK_INDEX.json")
        apply_started = time.perf_counter()
        applied = run(fixture, "--apply")
        apply_elapsed = time.perf_counter() - apply_started
        assert applied.returncode == 0, applied.stdout + applied.stderr
        assert json.loads(applied.stdout)["no_op"] is True
        assert load(fixture / "Area_comun/state/TASK_INDEX.json") == before
        assert apply_elapsed < max(check_elapsed * 3, 1.0), (check_elapsed, apply_elapsed)


def case_ps1_parity_if_available() -> None:
    if not shutil.which("pwsh"):
        return
    with tempfile.TemporaryDirectory(prefix="prune-ps1-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-File", str(ROOT / "scripts/prune_state.ps1"), "-Root", str(fixture), "-Check"],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 1, result.stdout + result.stderr


def case_missing_archive_row_fails_loudly() -> None:
    with tempfile.TemporaryDirectory(prefix="prune-archive-negative-") as temp:
        archive = Path(temp) / "TASK_INDEX_ARCHIVE.json"
        write_json(archive, {"tasks": []})
        try:
            verify_archived_entries(archive, [task("TASK-9000", "done")], ["TASK-9000"], "tasks", "id")
        except RuntimeError as exc:
            assert "TASK-9000" in str(exc)
        else:
            raise AssertionError("missing archived row did not fail")


def case_enforced_apply_prestages_archive_rows() -> None:
    """The real --apply path must pass its own post-submit archive drift gate."""
    with tempfile.TemporaryDirectory(prefix="prune-enforced-apply-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        config_path = fixture / "protocol.config.json"
        config = load(config_path)
        config.update(
            {
                "adoption_tier": "runtime",
                "event_auth": {"enabled": False},
                "event_state": {
                    "enabled": True,
                    "materialize": True,
                    "enforce": True,
                    "authoritative": True,
                },
                "agent_registry": {
                    "enabled": True,
                    "agents": [
                        {
                            "id": "Codex",
                            "enabled": True,
                            "capabilities": ["implementer", "orchestrator"],
                        }
                    ],
                },
            }
        )
        write_json(config_path, config)
        regenesis(
            fixture,
            actor_id="Codex",
            timestamp="2026-07-20T16:50:00Z",
            commit="fixture",
        )
        applied = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(fixture),
                "--apply",
                "--actor-id",
                "Codex",
                "--timestamp",
                "2026-07-20T16:51:00Z",
                "--commit",
                "fixture",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        assert applied.returncode == 0, applied.stdout + applied.stderr
        assert protocol_state_drift(fixture)["has_drift"] is False
        assert run(fixture, "--check").returncode == 0


def main() -> int:
    cases = [
        case_due_and_apply,
        case_not_due_when_disabled,
        case_ps1_parity_if_available,
        case_missing_archive_row_fails_loudly,
        case_enforced_apply_prestages_archive_rows,
    ]
    for case in cases:
        case()
    print("OK: prune_state cases passed (5, including enforced real-apply regression).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
