#!/usr/bin/env python3
"""Golden cases for mailbox status/folder consistency."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_collaboration_state.py"
VALIDATOR_PS1 = ROOT / "scripts" / "validate_collaboration_state.ps1"
PRUNE = ROOT / "scripts" / "prune_state.py"
MINIMAL = ROOT / "examples" / "minimal_instance"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def message(status: str) -> str:
    return (
        "---\n"
        "type: FYI\n"
        f"status: {status}\n"
        "requires_response: false\n"
        "---\n\n"
        "Mailbox fixture.\n"
    )


def copy_minimal(root: Path) -> None:
    shutil.copytree(MINIMAL, root, dirs_exist_ok=True)
    for state in ("open", "answered", "archived"):
        folder = root / "Area_comun" / "mailbox" / state
        folder.mkdir(parents=True, exist_ok=True)
        for stale in folder.glob("MSG-*.md"):
            stale.unlink()
        write(folder / ".gitkeep", "\n")


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(VALIDATOR), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def run_validator_ps1(root: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    command = [shell, "-NoProfile", "-File", str(VALIDATOR_PS1), "-Root", str(root)]
    return subprocess.run(command, text=True, capture_output=True, check=False)


def assert_validator(name: str, files: dict[str, str], expected: int) -> None:
    with tempfile.TemporaryDirectory(prefix=f"mailbox-{name}-") as temp:
        fixture = Path(temp)
        copy_minimal(fixture)
        for relative, status in files.items():
            write(fixture / relative, message(status))
        result = run_validator(fixture)
        if result.returncode != expected:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError(f"{name}: expected exit {expected}, got {result.returncode}")
        ps1 = run_validator_ps1(fixture)
        if ps1 is not None and ps1.returncode != expected:
            print(ps1.stdout)
            print(ps1.stderr)
            raise AssertionError(f"{name} ps1: expected exit {expected}, got {ps1.returncode}")


def build_prune_fixture(root: Path) -> None:
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
                "done_ratio_hard": 99,
                "released_ratio_hard": 99,
                "recent_done_tasks": 1,
                "recent_released_claims": 1,
                "mailbox_keep_recent": 1,
            },
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active", "active_tasks": []})
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    write(root / "Area_comun/mailbox/open/.gitkeep", "\n")
    write(root / "Area_comun/mailbox/answered/MSG-001-old.md", message("answered"))
    write(root / "Area_comun/mailbox/answered/MSG-002-new.md", message("answered"))
    write(root / "Area_comun/mailbox/archived/.gitkeep", "\n")


def case_prune_normalizes_archived_status() -> None:
    with tempfile.TemporaryDirectory(prefix="mailbox-prune-") as temp:
        fixture = Path(temp)
        build_prune_fixture(fixture)
        result = subprocess.run(
            ["python", str(PRUNE), "--root", str(fixture), "--apply"],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        archived = fixture / "Area_comun/mailbox/archived/MSG-001-old.md"
        assert archived.exists()
        assert "status: archived" in archived.read_text(encoding="utf-8")
        validation = run_validator(fixture)
        assert validation.returncode == 0, validation.stdout + validation.stderr


def main() -> int:
    assert_validator(
        "clean",
        {
            "Area_comun/mailbox/open/MSG-open.md": "open",
            "Area_comun/mailbox/answered/MSG-answered.md": "answered",
            "Area_comun/mailbox/archived/MSG-archived.md": "archived",
        },
        0,
    )
    assert_validator("answered_with_open_status", {"Area_comun/mailbox/answered/MSG-bad.md": "open"}, 1)
    assert_validator("archived_with_answered_status", {"Area_comun/mailbox/archived/MSG-bad.md": "answered"}, 1)
    assert_validator("open_with_answered_status", {"Area_comun/mailbox/open/MSG-bad.md": "answered"}, 1)
    case_prune_normalizes_archived_status()
    print("OK: mailbox status cases passed (5).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
