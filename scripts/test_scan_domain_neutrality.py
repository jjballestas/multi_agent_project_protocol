#!/usr/bin/env python3
"""Regression coverage for mandatory domain-neutrality scan surfaces."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = REPO_ROOT / "scripts" / "scan_domain_neutrality.py"
POWERSHELL_SCANNER_PATH = REPO_ROOT / "scripts" / "scan_domain_neutrality.ps1"
SCRATCH_ROOT = Path("D:/Aegis_Scratch/multi_agent_project_protocol/test_scan_domain_neutrality")


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_domain_neutrality_under_test", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load domain-neutrality scanner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DomainNeutralityCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = (SCRATCH_ROOT / uuid.uuid4().hex).resolve()
        if SCRATCH_ROOT.resolve() not in self.root.parents:
            raise RuntimeError("fixture path escaped the designated scratch root")
        (self.root / "scripts" / "memory").mkdir(parents=True)
        (self.root / "Area_comun" / "protocol").mkdir(parents=True)
        (self.root / "runtime" / "memory").mkdir(parents=True)

        self.term = "trad" + "ing"
        config = {
            "domain_neutrality": {
                "enabled": True,
                "denylist": [self.term],
                "scan_globs": [
                    "Area_comun/protocol/*.md",
                    "runtime/**",
                    "scripts/*.py",
                    "scripts/*.ps1",
                ],
                "exempt_globs": ["runtime/state/**"],
            }
        }
        (self.root / "protocol.config.json").write_text(
            json.dumps(config, indent=2) + "\n", encoding="utf-8"
        )
        (self.root / "scripts" / "memory" / "nested_probe.py").write_text(
            f'PROBE = "{self.term}"\n', encoding="utf-8"
        )
        (self.root / "Area_comun" / "protocol" / "MEMORY_INDEX_POLICY.json").write_text(
            json.dumps({"probe": self.term}, indent=2) + "\n", encoding="utf-8"
        )
        (self.root / "runtime" / "memory" / "generated-pack.md").write_text(
            f"generated corpus: {self.term}\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        resolved = self.root.resolve()
        if SCRATCH_ROOT.resolve() not in resolved.parents:
            raise RuntimeError("refusing to clean outside the designated scratch root")
        shutil.rmtree(resolved, ignore_errors=True)

    def run_python_scanner(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCANNER_PATH), "--root", str(self.root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_nested_scripts_and_policy_are_scanned_but_generated_pack_is_exempt(self) -> None:
        result = self.run_python_scanner()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("scripts/memory/nested_probe.py:1", result.stdout)
        self.assertIn("Area_comun/protocol/MEMORY_INDEX_POLICY.json:2", result.stdout)
        self.assertNotIn("runtime/memory/generated-pack.md", result.stdout)

        scanner = load_scanner()
        config = scanner.load_config(self.root)["domain_neutrality"]
        scan_globs = scanner.append_required_patterns(
            config["scan_globs"], scanner.REQUIRED_SCAN_GLOBS
        )
        exempt_globs = scanner.append_required_patterns(
            config["exempt_globs"], scanner.REQUIRED_EXEMPT_GLOBS
        )
        scanned = {
            path.relative_to(self.root).as_posix()
            for path in scanner.iter_scanned_files(self.root, scan_globs, exempt_globs)
        }
        self.assertIn("scripts/memory/nested_probe.py", scanned)
        self.assertIn("Area_comun/protocol/MEMORY_INDEX_POLICY.json", scanned)
        self.assertNotIn("runtime/memory/generated-pack.md", scanned)

        (self.root / "scripts" / "memory" / "nested_probe.py").write_text(
            'PROBE = "neutral"\n', encoding="utf-8"
        )
        (self.root / "Area_comun" / "protocol" / "MEMORY_INDEX_POLICY.json").write_text(
            json.dumps({"probe": "neutral"}, indent=2) + "\n", encoding="utf-8"
        )
        clean = self.run_python_scanner()
        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

    def test_powershell_scanner_matches_required_coverage_when_available(self) -> None:
        executable = shutil.which("pwsh") or shutil.which("powershell")
        if not executable:
            self.skipTest("PowerShell is not installed")
        result = subprocess.run(
            [
                executable,
                "-NoProfile",
                "-File",
                str(POWERSHELL_SCANNER_PATH),
                "-Root",
                str(self.root),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("scripts/memory/nested_probe.py:1", result.stdout)
        self.assertIn("Area_comun/protocol/MEMORY_INDEX_POLICY.json:2", result.stdout)
        self.assertNotIn("runtime/memory/generated-pack.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
