#!/usr/bin/env python3
"""Golden cases for mailbox-safe state pruning."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRUNE = ROOT / "scripts" / "prune_state.py"
PRUNE_PS1 = ROOT / "scripts" / "prune_state.ps1"
VALIDATOR = ROOT / "scripts" / "validate_collaboration_state.py"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def message(status: str, *, requires_response: bool = False) -> str:
    response = "true" if requires_response else "false"
    return (
        "---\n"
        "type: TASK_ASSIGNMENT\n"
        f"status: {status}\n"
        f"requires_response: {response}\n"
        "response_owner: Codex\n"
        "requested_action: Run the fixture.\n"
        "question: none\n"
        "context_refs:\n"
        "  - Area_comun/tasks/TASK-9000.md\n"
        "---\n\n"
        "# Fixture message\n"
    )


def task(task_id: str, status: str) -> dict:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": status,
        "file": f"Area_comun/tasks/{task_id}.md",
        "deliverables": [],
    }


def claim(claim_id: str, status: str, task_id: str = "TASK-9000") -> dict:
    return {
        "claim_id": claim_id,
        "task_id": task_id,
        "owner": "Codex",
        "status": status,
        "scope": ["Area_comun/state/CLAIMS.json"],
    }


def build_fixture(root: Path) -> None:
    tasks = [task(f"TASK-900{i}", "done") for i in range(5)] + [task("TASK-9999", "in_progress")]
    claims = [claim(f"CLAIM-{i:04d}", "released") for i in range(6)] + [
        claim("CLAIM-active", "active", "TASK-9999")
    ]
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
                "enabled": True,
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
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    write(root / "Area_comun/mailbox/open/.gitkeep", "\n")
    write(root / "Area_comun/mailbox/open/MSG-001-open-requires-response.md", message("open", requires_response=True))
    write(root / "Area_comun/mailbox/answered/MSG-002-old-resolved.md", message("answered", requires_response=True))
    write(root / "Area_comun/mailbox/answered/MSG-003-new-resolved.md", message("answered", requires_response=True))
    write(root / "Area_comun/mailbox/answered/MSG-004-unresolved-in-wrong-folder.md", message("open", requires_response=True))
    write(root / "Area_comun/mailbox/archived/.gitkeep", "\n")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def run_prune(root: Path) -> subprocess.CompletedProcess[str]:
    return run(["python", str(PRUNE), "--root", str(root), "--apply"])


def run_prune_ps1(root: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run([shell, "-NoProfile", "-File", str(PRUNE_PS1), "-Root", str(root), "-Apply"])


def validate(root: Path) -> None:
    result = run(["python", str(VALIDATOR), "--root", str(root)])
    assert result.returncode == 0, result.stdout + result.stderr


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def assert_pruned_fixture(root: Path) -> None:
    validate(root)
    assert (root / "Area_comun/mailbox/open/MSG-001-open-requires-response.md").exists()
    assert (root / "Area_comun/mailbox/open/MSG-004-unresolved-in-wrong-folder.md").exists()
    archived = root / "Area_comun/mailbox/archived/MSG-002-old-resolved.md"
    assert archived.exists()
    assert "status: archived" in archived.read_text(encoding="utf-8")
    assert (root / "Area_comun/mailbox/answered/MSG-003-new-resolved.md").exists()
    assert len(load_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json")["tasks"]) == 4
    assert len(load_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json")["claims"]) == 4


def case_python_prune_mailbox_safety() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-prune-py-") as temp:
        root = Path(temp)
        build_fixture(root)
        result = run_prune(root)
        assert result.returncode == 0, result.stdout + result.stderr
        assert_pruned_fixture(root)
        second = run_prune(root)
        assert second.returncode == 0, second.stdout + second.stderr
        assert_pruned_fixture(root)


def case_powershell_wrapper_parity_if_available() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-prune-ps-") as temp:
        root = Path(temp)
        build_fixture(root)
        result = run_prune_ps1(root)
        if result is None:
            return
        assert result.returncode == 0, result.stdout + result.stderr
        assert_pruned_fixture(root)


SENTINEL = "[HISTORICO PODADO]"


def build_next_actions_fixture(root: Path, next_actions: list, recent_next_actions: int) -> None:
    """Fixture minimo para ejercitar la condensacion de next_actions via prune --apply."""
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "token_cost": {
                "chars_per_token": 4,
                "coldstart_globs": ["Area_comun/state/PROJECT_STATE.json"],
                "budget": 30000,
            },
            "maintenance": {
                "enabled": True,
                "cold_start_tokens_hard": 999999,
                "done_ratio_hard": 99,
                "released_ratio_hard": 99,
                "recent_done_tasks": 5,
                "recent_released_claims": 5,
                "mailbox_keep_recent": 5,
                "recent_next_actions": recent_next_actions,
            },
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "active_tasks": [], "next_actions": next_actions},
    )
    write(root / "Area_comun/mailbox/open/.gitkeep", "\n")
    write(root / "Area_comun/mailbox/answered/.gitkeep", "\n")
    write(root / "Area_comun/mailbox/archived/.gitkeep", "\n")


def load_next_actions(root: Path) -> list:
    return load_json(root / "Area_comun/state/PROJECT_STATE.json")["next_actions"]


def case_next_actions_condensed_above_threshold() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-prune-na-") as temp:
        root = Path(temp)
        actions = [f"accion historica {i}" for i in range(10)]
        build_next_actions_fixture(root, actions, recent_next_actions=3)
        result = run_prune(root)
        assert result.returncode == 0, result.stdout + result.stderr
        na = load_next_actions(root)
        # 1 centinela + 3 recientes
        assert len(na) == 4, na
        assert na[0].startswith(SENTINEL), na[0]
        assert "7 next_actions" in na[0], na[0]  # 10 - 3 condensadas
        assert na[1:] == actions[-3:], na
        # idempotente: segunda corrida no re-condensa ni duplica centinela
        assert run_prune(root).returncode == 0
        na2 = load_next_actions(root)
        assert na2 == na, na2


def case_next_actions_below_threshold_unchanged() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-prune-na2-") as temp:
        root = Path(temp)
        actions = ["accion 1", "accion 2"]
        build_next_actions_fixture(root, actions, recent_next_actions=3)
        assert run_prune(root).returncode == 0
        assert load_next_actions(root) == actions


def case_next_actions_disabled_when_absent_or_zero() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-prune-na3-") as temp:
        root = Path(temp)
        actions = [f"accion {i}" for i in range(10)]
        build_next_actions_fixture(root, actions, recent_next_actions=0)
        assert run_prune(root).returncode == 0
        assert load_next_actions(root) == actions


def case_next_actions_merges_prior_sentinel() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-prune-na4-") as temp:
        root = Path(temp)
        prior = f"{SENTINEL} 37 next_actions antiguas removidas (DECISION-0014)."
        actions = [prior] + [f"accion {i}" for i in range(6)]
        build_next_actions_fixture(root, actions, recent_next_actions=2)
        assert run_prune(root).returncode == 0
        na = load_next_actions(root)
        assert len(na) == 3, na  # centinela + 2 recientes
        assert na[0].startswith(SENTINEL), na[0]
        assert "41 next_actions" in na[0], na[0]  # 37 previos + (6 - 2) = 41
        assert na[1:] == [f"accion {i}" for i in range(4, 6)], na


def main() -> int:
    cases = [
        case_python_prune_mailbox_safety,
        case_powershell_wrapper_parity_if_available,
        case_next_actions_condensed_above_threshold,
        case_next_actions_below_threshold_unchanged,
        case_next_actions_disabled_when_absent_or_zero,
        case_next_actions_merges_prior_sentinel,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print("OK: runtime prune cases passed (mailbox safety + next_actions condensation + ps1 parity when available).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
