#!/usr/bin/env python3
"""Git helpers for runtime turn commits."""

from __future__ import annotations

import subprocess
from pathlib import Path


POLICY_PATHS = (
    "AGENTS.md",
    "protocol.config.json",
    "protocol.config.template.json",
    "Area_comun/decisions/",
)


class VcsError(RuntimeError):
    pass


def normalize_repo_path(path: str) -> str:
    clean = path.replace("\\", "/").strip()
    clean = clean.split("#", 1)[0]
    return clean.strip("/")


def run_git(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if check and completed.returncode != 0:
        raise VcsError((completed.stdout + completed.stderr).strip())
    return completed


def is_policy_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if normalized.startswith(".git/") or normalized == ".git":
        return True
    return any(normalized == policy.rstrip("/") or normalized.startswith(policy) for policy in POLICY_PATHS)


def commit_turn(root: Path, message: str, paths: list[str], allow_policy: bool = False, verify: bool = True) -> str:
    """Commit a runtime turn with repository hooks enabled by default.

    ``verify=False`` is an explicit recovery-only bypass for repairing the gate itself or
    rolling back a broken gate; normal runtime turns must retain the default.
    """
    root = root.resolve()
    if not message.strip():
        raise VcsError("Commit message is required")
    repo_paths = sorted({normalize_repo_path(path) for path in paths if normalize_repo_path(path)})
    if not repo_paths:
        raise VcsError("No paths provided for turn commit")
    if not allow_policy:
        blocked = [path for path in repo_paths if is_policy_path(path)]
        if blocked:
            raise VcsError(f"Policy paths require allow_policy=True: {', '.join(blocked)}")
    run_git(root, ["add", "--", *repo_paths])
    commit_args = ["commit", "-m", message]
    if not verify:
        commit_args.append("--no-verify")
    run_git(root, commit_args)
    return run_git(root, ["rev-parse", "--short", "HEAD"]).stdout.strip()


def revert_last(root: Path) -> None:
    run_git(root.resolve(), ["revert", "--no-edit", "HEAD"])


def discard_worktree_changes(root: Path) -> None:
    root = root.resolve()
    run_git(root, ["restore", "--staged", "."])
    run_git(root, ["restore", "."])
