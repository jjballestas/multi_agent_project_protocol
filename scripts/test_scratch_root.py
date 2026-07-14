#!/usr/bin/env python3
"""Regression tests for the scratch-root policy check (DECISION-0098).

Covers: absent field = no-op (pinned legacy configs keep validating), relative path fails,
inside-tree path fails, outside-tree absolute path passes. Runs the Python validator directly
and the PowerShell validator via subprocess for parity (pattern of test_intake_gate).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from scripts.validate_collaboration_state import validate


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def minimal_instance(root: Path, scratch_root: str | None) -> None:
    config: dict = {
        "schema_version": "1.0",
        "protocol_version": "1.14.0",
        "project_name": "scratch_root_case",
        "adoption_tier": "coordination",
    }
    if scratch_root is not None:
        config["scratch_root"] = scratch_root
    write(root / "protocol.config.json", json.dumps(config, indent=2) + "\n")
    write(root / "Area_comun/state/PROJECT_STATE.json", '{"status":"active","active_tasks":[],"decisions":[]}\n')
    write(root / "Area_comun/state/TASK_INDEX.json", '{"schema_version":"1.0","tasks":[]}\n')
    write(root / "Area_comun/state/CLAIMS.json", '{"schema_version":"1.0","claims":[]}\n')


def run_ps1(root: Path) -> tuple[int, str]:
    pwsh = shutil.which("pwsh") or shutil.which("powershell")
    if not pwsh:
        return (-1, "no powershell available")
    proc = subprocess.run(
        [
            pwsh,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "scripts" / "validate_collaboration_state.ps1"),
            "-Root",
            str(root),
        ],
        capture_output=True,
        text=True,
    )
    return (proc.returncode, proc.stdout + proc.stderr)


class ScratchRootTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.mkdtemp(prefix="scratch-root-test-")
        self.root = Path(self._temp)

    def tearDown(self) -> None:
        shutil.rmtree(self._temp, ignore_errors=True)

    def _scratch_errors(self, validation) -> list[str]:
        return [e for e in validation.errors if "scratch_root" in e]

    def test_absent_field_is_noop(self) -> None:
        minimal_instance(self.root, scratch_root=None)
        validation = validate(self.root)
        self.assertEqual(self._scratch_errors(validation), [])

    def test_empty_field_is_noop(self) -> None:
        minimal_instance(self.root, scratch_root="")
        validation = validate(self.root)
        self.assertEqual(self._scratch_errors(validation), [])

    def test_relative_path_fails(self) -> None:
        minimal_instance(self.root, scratch_root="some/relative/dir")
        validation = validate(self.root)
        self.assertTrue(self._scratch_errors(validation))

    def test_inside_tree_fails(self) -> None:
        inside = str((self.root / "scratch").resolve()).replace("\\", "/")
        minimal_instance(self.root, scratch_root=inside)
        validation = validate(self.root)
        self.assertTrue(self._scratch_errors(validation))

    def test_outside_tree_passes(self) -> None:
        outside = str(Path(tempfile.gettempdir()).resolve() / "Aegis_Scratch" / "case").replace("\\", "/")
        minimal_instance(self.root, scratch_root=outside)
        validation = validate(self.root)
        self.assertEqual(self._scratch_errors(validation), [])

    def test_root_itself_fails(self) -> None:
        minimal_instance(self.root, scratch_root=str(self.root.resolve()).replace("\\", "/"))
        validation = validate(self.root)
        self.assertTrue(self._scratch_errors(validation))

    def test_sibling_with_common_prefix_passes(self) -> None:
        sibling = str(self.root.resolve()).replace("\\", "/") + "2"
        minimal_instance(self.root, scratch_root=sibling)
        validation = validate(self.root)
        self.assertEqual(self._scratch_errors(validation), [])

    def test_foreign_platform_absolute_passes(self) -> None:
        # A config born on the other platform must still validate here (CI cross-platform).
        foreign = "/home/ci/Aegis_Scratch/case" if os.name == "nt" else "D:/Aegis_Scratch/case"
        minimal_instance(self.root, scratch_root=foreign)
        validation = validate(self.root)
        self.assertEqual(self._scratch_errors(validation), [])

    def test_drive_relative_fails(self) -> None:
        minimal_instance(self.root, scratch_root="C:foo/scratch")
        validation = validate(self.root)
        self.assertTrue(self._scratch_errors(validation))

    def test_home_anchored_passes(self) -> None:
        minimal_instance(self.root, scratch_root="~/Aegis_Scratch/case")
        validation = validate(self.root)
        self.assertEqual(self._scratch_errors(validation), [])

    def test_ps1_parity_drive_relative_fails(self) -> None:
        minimal_instance(self.root, scratch_root="C:foo/scratch")
        code, output = run_ps1(self.root)
        if code == -1:
            self.skipTest("powershell not available")
        self.assertNotEqual(code, 0, output)
        self.assertIn("scratch_root", output)

    def test_ps1_parity_inside_tree_fails(self) -> None:
        inside = str((self.root / "scratch").resolve()).replace("\\", "/")
        minimal_instance(self.root, scratch_root=inside)
        code, output = run_ps1(self.root)
        if code == -1:
            self.skipTest("powershell not available")
        self.assertNotEqual(code, 0, output)
        self.assertIn("scratch_root", output)

    def test_ps1_parity_outside_tree_passes_check(self) -> None:
        outside = str(Path(tempfile.gettempdir()).resolve() / "Aegis_Scratch" / "case").replace("\\", "/")
        minimal_instance(self.root, scratch_root=outside)
        code, output = run_ps1(self.root)
        if code == -1:
            self.skipTest("powershell not available")
        self.assertNotIn("scratch_root must", output)


if __name__ == "__main__":
    unittest.main()
