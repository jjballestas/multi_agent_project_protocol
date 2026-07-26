#!/usr/bin/env python3
"""Behavioral cases for the read-only scratch-discipline detector."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / "scripts" / "scan_scratch_discipline.py"
MONITOR = ROOT / "scripts" / "run_scratch_discipline_monitor.py"
INSTALLER = ROOT / "scripts" / "install_scratch_discipline_monitor.ps1"


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


def _assert_windows_installer_round_trip(scan_root: Path, scratch_root: Path) -> None:
    if sys.platform != "win32":
        return
    import ctypes

    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        raise AssertionError("Windows installer round-trip requires PowerShell")
    scan_arg = str(scan_root) + os.sep
    scratch_arg = str(scratch_root) + os.sep
    allow_arg = str(scan_root / "canonical-home") + os.sep
    def installer_arguments(scan_value: str) -> list[str]:
        result = subprocess.run(
            [
                shell, "-NoProfile", "-File", str(INSTALLER),
                "-Python", sys.executable,
                "-ScanRoot", scan_value,
                "-ScratchRoot", scratch_arg,
                "-KnownRepo", "https://example.invalid/owner/known-repository.git",
                "-AllowHome", allow_arg,
                "-MaxDepth", "2",
                "-WhatIf",
            ],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(f"installer preview failed: {result.stdout}{result.stderr}")
        prefix = "Scheduled task arguments: "
        line = next((item[len(prefix):] for item in result.stdout.splitlines() if item.startswith(prefix)), None)
        if line is None:
            raise AssertionError("installer -WhatIf did not print the composed argument line")
        argc = ctypes.c_int()
        command_line_to_argv = ctypes.windll.shell32.CommandLineToArgvW
        command_line_to_argv.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
        command_line_to_argv.restype = ctypes.POINTER(ctypes.c_wchar_p)
        parsed_pointer = command_line_to_argv(line, ctypes.byref(argc))
        if not parsed_pointer:
            raise AssertionError("CommandLineToArgvW rejected the installer argument line")
        try:
            return [parsed_pointer[index] for index in range(argc.value)]
        finally:
            ctypes.windll.kernel32.LocalFree(parsed_pointer)

    parsed = installer_arguments(scan_arg)
    intended = [
        str(MONITOR), "--",
        "--scan-root", scan_arg,
        "--scratch-root", scratch_arg,
        "--max-depth", "2",
        "--known-repo", "https://example.invalid/owner/known-repository.git",
        "--allow-home", allow_arg,
    ]
    if parsed != intended:
        raise AssertionError(f"installer argv round-trip mismatch: {parsed!r} != {intended!r}")

    volume_root = Path(ROOT.anchor).as_posix()
    for root_variant in (volume_root, ROOT.anchor, ROOT.drive):
        variant_parsed = installer_arguments(root_variant)
        variant_index = variant_parsed.index("--scan-root") + 1
        if variant_parsed[variant_index] != root_variant:
            raise AssertionError(
                f"installer changed volume-root vector: {variant_parsed[variant_index]!r} != {root_variant!r}"
            )
    volume_parsed = installer_arguments(volume_root)
    scan_index = volume_parsed.index("--scan-root") + 1
    if volume_parsed[scan_index] != volume_root or volume_parsed[scan_index].endswith(":"):
        raise AssertionError(f"installer collapsed volume root: {volume_parsed[scan_index]!r}")
    direct = subprocess.run(
        [sys.executable, *intended[:3], volume_root, *intended[4:]],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    composed = subprocess.run(
        [sys.executable, *volume_parsed], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if (composed.returncode, composed.stdout, composed.stderr) != (
        direct.returncode, direct.stdout, direct.stderr
    ):
        raise AssertionError("volume-root installer invocation differs from direct monitor invocation")


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

        _assert_windows_installer_round_trip(scan_root, allowed)

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
        monitor_result = subprocess.run(
            [
                sys.executable, str(MONITOR),
                "--scan-root", str(scan_root),
                "--scratch-root", str(allowed),
                "--known-repo", known_remote,
                "--allow-home", str(scan_root / "canonical-home"),
                "--check", "--json",
            ],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=False,
        )
        if monitor_result.returncode != 1:
            raise AssertionError(
                "monitor invocation without separator must preserve scanner exit 1: "
                f"{monitor_result.stdout}{monitor_result.stderr}"
            )
        monitor_names = {
            Path(item["path"]).name
            for item in json.loads(monitor_result.stdout)["findings"]
        }
        if monitor_names != names:
            raise AssertionError(f"monitor lost scanner arguments: {sorted(monitor_names)}")
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
