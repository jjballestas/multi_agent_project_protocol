#!/usr/bin/env python3
"""Real-commit regression checks for the index-materializing pre-commit hook."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import time
import os
from pathlib import Path


def run(
    args: list[str], cwd: Path, *, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=cwd, text=True, capture_output=True, check=False, env=env
    )


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


def commit(
    root: Path, message: str, *, full: bool = False
) -> subprocess.CompletedProcess[str]:
    env = None
    if full:
        env = os.environ.copy()
        env["HOOK_FULL"] = "1"
    return run(["git", "commit", "-qm", message], root, env=env)


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
            "import json, pathlib, sys\n"
            "sys.path.insert(0, str(pathlib.Path.cwd()))\n"
            "import runtime.protocol_replay\n"
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
        started = time.perf_counter()
        bounded = commit(root, "bounded default")
        elapsed = time.perf_counter() - started
        require(bounded, 0, "bounded default accepts without full validator")
        if elapsed >= 2.0:
            raise AssertionError(f"bounded default took {elapsed:.3f}s, expected <2s")
        require(run(["git", "reset", "--hard", "HEAD^"], root), 0, "reset bounded fixture")

        state.write_text('{"broken": true}\n', encoding="utf-8")
        require(run(["git", "add", str(state.relative_to(root))], root), 0, "restage governed state")
        negative = commit(root, "negative staged state", full=True)
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
        require(commit(root, "unstaged validator isolation", full=True), 0, "unstaged validator does not alter verdict")
        require(run(["git", "restore", "scripts/validate_collaboration_state.py"], root), 0, "restore validator")

        # Prune is judgment code too: an unstaged mutation must not affect a
        # clean staged commit because prune runs from the index materialization.
        prune = root / "scripts" / "prune_state.py"
        prune.write_text("raise SystemExit(23)\n", encoding="utf-8")
        marker.write_text("prune isolation\n", encoding="utf-8")
        require(run(["git", "add", "AGENTS.md"], root), 0, "stage prune-isolation change")
        require(
            commit(root, "unstaged prune isolation", full=True),
            0,
            "full mode isolates unstaged prune from staged judgment",
        )
        require(run(["git", "restore", "scripts/prune_state.py"], root), 0, "restore prune")

        state.write_text('{"peer_unstaged": true}\n', encoding="utf-8")
        marker.write_text("second staged clean change\n", encoding="utf-8")
        require(run(["git", "add", "AGENTS.md"], root), 0, "stage concurrent own change")
        require(commit(root, "concurrent peer work"), 0, "unstaged peer governed work does not block")
        require(run(["git", "restore", str(state.relative_to(root))], root), 0, "restore peer work")

        rename_cases = [
            ("scripts/validate_collaboration_state.py", "scripts/validator_renamed.py", "internal validator"),
            ("scripts/validate_collaboration_state.py", "docs/validator_renamed.py", "outbound validator"),
            ("runtime/protocol_replay.py", "docs/protocol_replay.py", "outbound runtime dependency"),
            ("Area_comun/state/TASK_INDEX.json", "docs/TASK_INDEX.json", "outbound governed state"),
            (".githooks/pre-commit", "docs/pre-commit", "outbound hook"),
        ]
        for source_path, destination_path, label in rename_cases:
            (root / destination_path).parent.mkdir(parents=True, exist_ok=True)
            require(run(["git", "mv", source_path, destination_path], root), 0, f"stage {label} R100 rename")
            # Preserve the worktree hook for the self-rename case; the index still
            # contains the R100 source->destination pair under judgment.
            if source_path == ".githooks/pre-commit":
                hook_at_head = run(["git", "show", f"HEAD:{source_path}"], root)
                require(hook_at_head, 0, "read executing hook from HEAD")
                (root / source_path).write_text(hook_at_head.stdout, encoding="utf-8", newline="\n")
            require_rejected(commit(root, f"negative R100 {label}", full=True), f"staged R100 {label} rename")
            require(run(["git", "restore", "--staged", source_path, destination_path], root), 0, f"unstage {label} rename")
            require(run(["git", "restore", source_path], root), 0, f"restore {label} source")
            destination = root / destination_path
            if destination.exists():
                destination.unlink()

        before = set((root / ".git" / "worktrees").iterdir()) if (root / ".git" / "worktrees").exists() else set()
        state.write_text('{"broken": true}\n', encoding="utf-8")
        require(run(["git", "add", str(state.relative_to(root))], root), 0, "stage cleanup failure")
        require_rejected(commit(root, "negative cleanup", full=True), "invalid snapshot cleanup")
        after = set((root / ".git" / "worktrees").iterdir()) if (root / ".git" / "worktrees").exists() else set()
        if before != after:
            raise AssertionError("temporary materialization left .git/worktrees residue")
    print(
        "OK: bounded default <2s; explicit full-mode snapshot, concurrency, "
        "R100, rejection, and cleanup regressions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
