#!/usr/bin/env python3
"""Behavioral cases for the read-only scratch-discipline detector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / "scripts" / "scan_scratch_discipline.py"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scratch-root",
        required=True,
        type=Path,
        help="Existing designated scratch root beneath which the simulated root is created.",
    )
    return parser


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _attested_tree(path: Path) -> None:
    (path / "Area_comun").mkdir(parents=True)
    (path / "runtime").mkdir()
    _write(path / "protocol.config.json", "{}\n")


def _git_tree(path: Path, remote: str) -> None:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(
        ["git", "-C", str(path), "remote", "add", "origin", remote], check=True
    )
    _write(path / "payload.txt", "unchanged\n")


def _fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda value: value.as_posix()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"D" if path.is_dir() else b"F")
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def main() -> int:
    args = _parser().parse_args()
    designated = args.scratch_root.resolve()
    designated.mkdir(parents=True, exist_ok=True)
    simulated = designated / f"scratch-discipline-{uuid.uuid4().hex}"
    scan_root = simulated / "simulated-volume"
    allowed = scan_root / "designated-scratch"
    known_remote = "https://example.invalid/owner/known-repository.git"
    try:
        allowed.mkdir(parents=True)
        _attested_tree(allowed / "compliant")
        _git_tree(scan_root / "stray-clone", known_remote)
        _attested_tree(scan_root / "stray-markers")
        _attested_tree(scan_root / "canonical-home")
        _attested_tree(scan_root / "container" / "nested-stray")
        corrupt = scan_root / "corrupt-git"
        corrupt.mkdir()
        _write(corrupt / ".git", "gitdir: missing-directory\n")
        _write(scan_root / "unrelated" / "notes.txt", "personal data\n")
        before = _fingerprint(simulated)

        result = _run(
            "--scan-root",
            str(scan_root),
            "--scratch-root",
            str(allowed),
            "--known-repo",
            known_remote,
            "--allow-home",
            str(scan_root / "canonical-home"),
            "--check",
            "--json",
        )
        if result.returncode != 1:
            raise AssertionError(
                f"stray fixture must exit 1, got {result.returncode}: {result.stderr}"
            )
        payload = json.loads(result.stdout)
        names = {Path(item["path"]).name for item in payload["findings"]}
        if names != {"stray-clone", "stray-markers"}:
            raise AssertionError(f"unexpected findings: {sorted(names)}")
        if any("DECISION-0018" not in item["rule"] for item in payload["findings"]):
            raise AssertionError("each finding must carry the actionable rule")
        after = _fingerprint(simulated)
        if before != after:
            raise AssertionError("scanner modified the fixture tree")

        deep_result = _run(
            "--scan-root", str(scan_root),
            "--scratch-root", str(allowed),
            "--known-repo", known_remote,
            "--allow-home", str(scan_root / "canonical-home"),
            "--max-depth", "2", "--check", "--json",
        )
        deep_names = {
            Path(item["path"]).name
            for item in json.loads(deep_result.stdout)["findings"]
        }
        if "nested-stray" not in deep_names or "canonical-home" in deep_names:
            raise AssertionError(f"depth/allowlist failure: {sorted(deep_names)}")
        if "WARNING: cannot resolve git candidate" not in deep_result.stderr:
            raise AssertionError("corrupt git candidate must produce a visible warning")

        clean_root = designated / f"scratch-discipline-clean-{uuid.uuid4().hex}"
        clean_allowed = clean_root / "designated-scratch"
        try:
            _attested_tree(clean_allowed / "compliant")
            _write(clean_root / "unrelated" / "notes.txt", "personal data\n")
            clean_result = _run(
                "--scan-root",
                str(clean_root),
                "--scratch-root",
                str(clean_allowed),
                "--known-repo",
                known_remote,
                "--check",
            )
            if clean_result.returncode != 0:
                raise AssertionError(
                    f"clean fixture must exit 0: {clean_result.stdout}{clean_result.stderr}"
                )
        finally:
            shutil.rmtree(clean_root, ignore_errors=True)
    finally:
        shutil.rmtree(simulated, ignore_errors=True)
    print("OK: scratch-discipline detector cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
