#!/usr/bin/env python3
"""Execute the exportable delivery-watchdog discrimination proof."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path


MARKER = "coord-session-proof-7f6d"
MODEL_TRAILER = "Co-Authored-By: Claude (Opus) <shared-model@example.invalid>"
CONTRACT_RE = re.compile(r"^[ ]*WATCHDOG_COMMIT_TRAILER = ([A-Za-z0-9-]+)[ ]*$", re.MULTILINE)
MESSAGE_RE = re.compile(r"^MSG-[^-]+-(?P<sender>[^-]+)-to-(?P<recipient>[^-]+)-.+\.md$")
OBSOLETE_GUIDE_TOKENS = ("<SELF_COMMIT_FILTER>",)


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


def load_trailer_key(guide: Path) -> str:
    try:
        text = guide.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"cannot read exportable watchdog guide: {exc}") from exc
    matches = CONTRACT_RE.findall(text)
    if len(matches) != 1:
        raise ValueError("guide must expose exactly one WATCHDOG_COMMIT_TRAILER contract")
    obsolete = [token for token in OBSOLETE_GUIDE_TOKENS if token in text]
    if obsolete:
        raise ValueError(
            "guide still prescribes an identity-based self-filter: " + ", ".join(obsolete)
        )
    return matches[0]


def classify(guide: Path, marker: str, records: list[str]) -> dict[str, list[str]]:
    trailer_key = load_trailer_key(guide)
    trailer = re.compile(
        rf"^{re.escape(trailer_key)}:[ \t]*{re.escape(marker)}[ \t]*$", re.MULTILINE
    )

    def has_exact_trailer(record: str) -> bool:
        fields = record.split("\x1f", 2)
        return len(fields) == 3 and trailer.search(fields[2]) is not None

    return {
        "filtered": [record for record in records if has_exact_trailer(record)],
        "visible": [record for record in records if not has_exact_trailer(record)],
    }


def mailbox_additions(mailbox_dir: Path, previous: set[str], pattern: str) -> list[dict[str, str]]:
    current = {
        path.name
        for path in mailbox_dir.iterdir()
        if path.is_file() and fnmatch.fnmatchcase(path.name, pattern)
    } if mailbox_dir.is_dir() else set()
    alerts = []
    for name in sorted(current - previous):
        match = MESSAGE_RE.fullmatch(name)
        if match:
            alerts.append({"name": name, **match.groupdict()})
        else:
            alerts.append({"name": name, "unparsed": "true"})
    return alerts


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


def invoke_shipped_filter(script: Path, guide: Path, records: list[str]) -> dict[str, list[str]]:
    result = subprocess.run(
        [sys.executable, str(script), "--classify", "--guide", str(guide), "--marker", MARKER],
        input=json.dumps(records), text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr.strip() or "shipped filter failed")
    return json.loads(result.stdout)


def proof(scratch: Path, guide: Path) -> int:
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
        mailbox_dir = repo / "Area_comun" / "mailbox" / "open"
        before = set()
        commit(repo, "coordinator one", coordinator=True)
        commit(repo, "worker one", coordinator=False)
        commit(repo, "coordinator two", coordinator=True)
        commit(repo, "worker two", coordinator=False, mailbox=True)

        records = [
            record for record in run(repo, "log", "--reverse", "--format=%H%x1f%an%x1f%B%x1e").split("\x1e")
            if record.strip()
        ]
        result = invoke_shipped_filter(Path(__file__).resolve(), guide, records)
        false_positive_records = [
            f"subject\x1fShared Actor\x1fmentions Protocol-Monitor-Origin: {MARKER} in prose",
            f"subject Protocol-Monitor-Origin: {MARKER}\x1fShared Actor\x1fclean body",
            f"hash\x1fProtocol-Monitor-Origin: {MARKER}\x1fclean body",
        ]
        false_positive_result = classify(guide, MARKER, false_positive_records)
        old_own = [record for record in records if "Co-Authored-By: Claude (Opus)" in record]
        same_identity = all("\x1fShared Actor\x1f" in record and MODEL_TRAILER in record for record in records)
        alerts = mailbox_additions(mailbox_dir, before, "*-to-Coordinator-*")
        mailbox_alert = alerts == [{
            "name": "MSG-20990101-Worker-to-Coordinator-HANDOFF.md",
            "sender": "Worker", "recipient": "Coordinator",
        }]
        malformed_name = "MSG-2099-01-01-Worker-Coordinator-HANDOFF.md"
        (mailbox_dir / malformed_name).write_text("delivery\n", encoding="ascii")
        noisy_unparsed = mailbox_additions(
            mailbox_dir,
            {"MSG-20990101-Worker-to-Coordinator-HANDOFF.md"},
            "MSG-*",
        ) == [{"name": malformed_name, "unparsed": "true"}]
        parsed_control = mailbox_additions(
            mailbox_dir,
            {malformed_name},
            "MSG-*",
        ) == [{
            "name": "MSG-20990101-Worker-to-Coordinator-HANDOFF.md",
            "sender": "Worker", "recipient": "Coordinator",
        }]
        if not (len(records) == 4 and len(result["filtered"]) == 2 and len(result["visible"]) == 2):
            raise AssertionError("shipped marker filter did not produce the required 2/2 split")
        if len(old_own) != 4:
            raise AssertionError("historical provider/model filter did not reproduce the 4/4 silent watchdog")
        if false_positive_result != {"filtered": [], "visible": false_positive_records}:
            raise AssertionError("marker text outside an exact trailer was incorrectly filtered")
        if not same_identity:
            raise AssertionError("fixture commits do not share Git and provider/model identity")
        if not mailbox_alert:
            raise AssertionError("mailbox directory-listing delta did not emit the worker delivery alert")
        if not noisy_unparsed:
            raise AssertionError("unparseable matching mailbox filename was silently discarded")
        if not parsed_control:
            raise AssertionError("parseable mailbox filename did not emit exactly one normal alert")
        print("OK: old filter silenced 4/4; shipped filter split 2/2; mailbox listing alerted; malformed name alerted")
        return 0
    finally:
        if repo.exists():
            remove_tree(repo)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch-root", type=Path)
    parser.add_argument("--classify", action="store_true")
    parser.add_argument("--guide", type=Path)
    parser.add_argument("--marker")
    args = parser.parse_args()
    if args.classify:
        if not args.guide or not args.marker:
            parser.error("--classify requires --guide and --marker")
        records = json.load(sys.stdin)
        print(json.dumps(classify(args.guide, args.marker, records), sort_keys=True))
        return 0
    if not args.scratch_root:
        parser.error("--scratch-root is required for the proof")
    guide = args.guide or Path(__file__).resolve().parents[2] / "skills" / "session-watchdogs.skill.md"
    return proof(args.scratch_root.resolve(), guide.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
