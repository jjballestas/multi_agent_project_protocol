#!/usr/bin/env python3
"""Execute the exportable delivery-watchdog discrimination proof."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
from pathlib import Path


MARKER = "coord-session-proof-7f6d"
MODEL_TRAILER = "Co-Authored-By: Shared Model <shared-model@example.invalid>"


def run(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def remove_tree(path: Path) -> None:
    def make_writable(function, target, _error) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(path, onerror=make_writable)


def commit(repo: Path, subject: str, coordinator: bool, mailbox: bool = False) -> None:
    serial = int(run(repo, "rev-list", "--all", "--count") or "0") + 1
    (repo / f"artifact-{serial}.txt").write_text(subject + "\n", encoding="ascii")
    if mailbox:
        mailbox_dir = repo / "Area_comun" / "mailbox" / "open"
        mailbox_dir.mkdir(parents=True, exist_ok=True)
        (mailbox_dir / "MSG-20990101-Worker-to-Coordinator-HANDOFF.md").write_text(
            "delivery\n", encoding="ascii"
        )
    run(repo, "add", ".")
    body = MODEL_TRAILER
    if coordinator:
        body += f"\n\nProtocol-Monitor-Origin: {MARKER}"
    run(repo, "commit", "-m", subject, "-m", body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch-root", required=True, type=Path)
    args = parser.parse_args()
    scratch = args.scratch_root.resolve()
    if scratch.parent == scratch or len(scratch.parts) < 4:
        raise SystemExit("scratch root must be a specific, non-root directory")
    repo = scratch / "repo"
    if repo.exists():
        remove_tree(repo)
    repo.mkdir(parents=True)
    try:
        run(repo, "init", "-q")
        run(repo, "config", "user.name", "Shared Actor")
        run(repo, "config", "user.email", "shared@example.invalid")
        commit(repo, "coordinator one", coordinator=True)
        commit(repo, "worker one", coordinator=False, mailbox=True)
        commit(repo, "coordinator two", coordinator=True)
        commit(repo, "worker two", coordinator=False)

        records = run(repo, "log", "--reverse", "--format=%H%x1f%an%x1f%B%x1e")
        commits = [record for record in records.split("\x1e") if record.strip()]
        own = [record for record in commits if f"Protocol-Monitor-Origin: {MARKER}" in record]
        visible = [record for record in commits if f"Protocol-Monitor-Origin: {MARKER}" not in record]
        same_identity = all(
            "\x1fShared Actor\x1f" in record and MODEL_TRAILER in record
            for record in commits
        )
        changed = run(repo, "show", "--name-only", "--format=", "HEAD~2")
        mailbox_alert = "MSG-20990101-Worker-to-Coordinator-HANDOFF.md" in changed
        if not (len(commits) == 4 and len(own) == 2 and len(visible) == 2):
            raise AssertionError("marker did not split two coordinator and two worker commits")
        if not same_identity:
            raise AssertionError("fixture commits do not share Git and provider/model identity")
        if not mailbox_alert:
            raise AssertionError("worker mailbox delivery was not detected")
        print("OK: 2 coordinator filtered, 2 worker retained, mailbox delivery alerted")
        return 0
    finally:
        if repo.exists():
            remove_tree(repo)


if __name__ == "__main__":
    raise SystemExit(main())
