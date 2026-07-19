#!/usr/bin/env python3
"""Real-commit regression checks for the index-materializing pre-commit hook."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def require(result: subprocess.CompletedProcess[str], expected: int, label: str) -> None:
    if result.returncode != expected:
        raise AssertionError(
            f"{label}: expected exit {expected}, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def require_rejected(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode == 0:
        raise AssertionError(
            f"{label}: expected a non-zero exit\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def commit(root: Path, message: str) -> subprocess.CompletedProcess[str]:
    return run(["git", "commit", "-qm", message], root)


def main() -> int:
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="protocol-precommit-") as tmp:
        root = Path(tmp) / "repo"
        (root / ".githooks").mkdir(parents=True)
        (root / "scripts").mkdir()
        (root / "runtime").mkdir()
        (root / "Area_comun" / "state").mkdir(parents=True)
        shutil.copy2(source / ".githooks" / "pre-commit", root / ".githooks" / "pre-commit")
        (root / "scripts" / "prune_state.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        (root / "scripts" / "validate_collaboration_state.py").write_text(
            "import json, pathlib\n"
            "state=json.loads((pathlib.Path('Area_comun/state/TASK_INDEX.json')).read_text())\n"
            "raise SystemExit(1 if state.get('broken') else 0)\n",
            encoding="utf-8",
        )
        (root / "scripts" / "generate_human_guide.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        (root / "runtime" / "protocol_replay.py").write_text("# judgment dependency\n", encoding="utf-8")
        state = root / "Area_comun" / "state" / "TASK_INDEX.json"
        state.write_text("{}\n", encoding="utf-8")
        require(run(["git", "init", "-q"], root), 0, "git init")
        require(run(["git", "config", "user.email", "hook@example.invalid"], root), 0, "git email")
        require(run(["git", "config", "user.name", "Hook Test"], root), 0, "git name")
        require(run(["git", "config", "core.hooksPath", ".githooks"], root), 0, "hook path")
        require(run(["git", "add", "."], root), 0, "initial add")
        require(run(["git", "commit", "--no-verify", "-qm", "fixture"], root), 0, "fixture commit")

        state.write_text('{"broken": true}\n', encoding="utf-8")
        require(run(["git", "add", str(state.relative_to(root))], root), 0, "stage governed state")
        negative = commit(root, "negative staged state")
        if negative.returncode == 0 or "collaboration state in staged snapshot is invalid" not in negative.stderr:
            raise AssertionError(
                "invalid staged collaboration state was not rejected\n"
                f"stdout:\n{negative.stdout}\nstderr:\n{negative.stderr}"
            )

        require(run(["git", "restore", "--staged", str(state.relative_to(root))], root), 0, "unstage state")
        require(run(["git", "restore", str(state.relative_to(root))], root), 0, "restore state")

        validator = root / "scripts" / "validate_collaboration_state.py"
        validator.write_text("raise SystemExit(1)\n", encoding="utf-8")
        marker = root / "AGENTS.md"
        marker.write_text("staged clean change\n", encoding="utf-8")
        require(run(["git", "add", "AGENTS.md"], root), 0, "stage own governed change")
        require(commit(root, "unstaged validator isolation"), 0, "unstaged validator does not alter verdict")
        require(run(["git", "restore", "scripts/validate_collaboration_state.py"], root), 0, "restore validator")

        state.write_text('{"peer_unstaged": true}\n', encoding="utf-8")
        marker.write_text("second staged clean change\n", encoding="utf-8")
        require(run(["git", "add", "AGENTS.md"], root), 0, "stage concurrent own change")
        require(commit(root, "concurrent peer work"), 0, "unstaged peer governed work does not block")
        require(run(["git", "restore", str(state.relative_to(root))], root), 0, "restore peer work")

        require(
            run(["git", "mv", "scripts/validate_collaboration_state.py", "scripts/validator_renamed.py"], root),
            0,
            "stage R100 validator rename",
        )
        require_rejected(commit(root, "negative R100 judgment rename"), "staged R100 judgment rename")
        require(run(["git", "restore", "--staged", "scripts/validate_collaboration_state.py", "scripts/validator_renamed.py"], root), 0, "unstage rename")
        require(run(["git", "restore", "scripts/validate_collaboration_state.py"], root), 0, "restore renamed validator")
        if (root / "scripts" / "validator_renamed.py").exists():
            (root / "scripts" / "validator_renamed.py").unlink()

        before = set((root / ".git" / "worktrees").iterdir()) if (root / ".git" / "worktrees").exists() else set()
        state.write_text('{"broken": true}\n', encoding="utf-8")
        require(run(["git", "add", str(state.relative_to(root))], root), 0, "stage cleanup failure")
        require_rejected(commit(root, "negative cleanup"), "invalid snapshot cleanup")
        after = set((root / ".git" / "worktrees").iterdir()) if (root / ".git" / "worktrees").exists() else set()
        if before != after:
            raise AssertionError("temporary materialization left .git/worktrees residue")
    print("OK: real-commit index snapshot, concurrency, R100, rejection, and cleanup regressions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
