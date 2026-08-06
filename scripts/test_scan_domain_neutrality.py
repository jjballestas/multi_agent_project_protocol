#!/usr/bin/env python3
"""Regression coverage for mandatory domain-neutrality scan surfaces."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = REPO_ROOT / "scripts" / "scan_domain_neutrality.py"
POWERSHELL_SCANNER_PATH = REPO_ROOT / "scripts" / "scan_domain_neutrality.ps1"

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-NEUTRALITY-NESTED-IDENTITY",
        "negative": "A configured identity in a nested script remains visible to the neutrality gate.",
        "mutation": ".replace(identity_rule, restricted_rule)",
        "boundaries": (
            'self.assertIn("scripts/memory/identity_probe.py:1", baseline.stdout)',
            'self.assertNotIn("scripts/memory/identity_probe.py:1", mutant.stdout)',
        ),
        "exercised_by": "test_nested_identity_depth_restriction_is_killed",
    },
)


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_domain_neutrality_under_test", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load domain-neutrality scanner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DomainNeutralityCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory(prefix="domain-neutrality-")
        self.scratch_root = Path(self._tempdir.name).resolve()
        self.root = (self.scratch_root / "fixture").resolve()
        if self.scratch_root not in self.root.parents:
            raise RuntimeError("fixture path escaped the designated scratch root")
        (self.root / "scripts" / "memory").mkdir(parents=True)
        (self.root / "Area_comun" / "protocol").mkdir(parents=True)
        (self.root / "runtime" / "memory").mkdir(parents=True)

        self.term = "trad" + "ing"
        config = {
            "agent_registry": {"agents": [{"id": "SampleAgent"}]},
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
        (self.root / "scripts" / "root_identity_probe.py").write_text(
            'IDENTITY = "SampleAgent"\n', encoding="utf-8"
        )
        (self.root / "scripts" / "memory" / "identity_probe.py").write_text(
            'IDENTITY = "SampleAgent"\n', encoding="utf-8"
        )
        (self.root / "Area_comun" / "protocol" / "MEMORY_INDEX_POLICY.json").write_text(
            json.dumps({"probe": self.term}, indent=2) + "\n", encoding="utf-8"
        )
        (self.root / "runtime" / "memory" / "generated-pack.md").write_text(
            f"generated corpus: {self.term}\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        resolved = self.root.resolve()
        if self.scratch_root not in resolved.parents:
            raise RuntimeError("refusing to clean outside the designated scratch root")
        self._tempdir.cleanup()

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
        self.assertIn("scripts/root_identity_probe.py:1", result.stdout)
        self.assertIn("scripts/memory/identity_probe.py:1", result.stdout)
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
        self.assertIn("scripts/memory/identity_probe.py", scanned)
        self.assertIn("Area_comun/protocol/MEMORY_INDEX_POLICY.json", scanned)
        self.assertNotIn("runtime/memory/generated-pack.md", scanned)

        (self.root / "scripts" / "memory" / "nested_probe.py").write_text(
            'PROBE = "neutral"\n', encoding="utf-8"
        )
        (self.root / "Area_comun" / "protocol" / "MEMORY_INDEX_POLICY.json").write_text(
            json.dumps({"probe": "neutral"}, indent=2) + "\n", encoding="utf-8"
        )
        clean = self.run_python_scanner()
        self.assertEqual(clean.returncode, 1, clean.stdout + clean.stderr)
        self.assertIn("scripts/root_identity_probe.py:1", clean.stdout)
        self.assertIn("scripts/memory/identity_probe.py:1", clean.stdout)

    def test_nested_identity_depth_restriction_is_killed(self) -> None:
        """PERMANENT_NEGATIVE: NEG-NEUTRALITY-NESTED-IDENTITY"""
        baseline = self.run_python_scanner()
        self.assertIn("scripts/memory/identity_probe.py:1", baseline.stdout)

        source = SCANNER_PATH.read_text(encoding="utf-8")
        identity_rule = 'relative_path.startswith("scripts/")\n            and relative_path.endswith'
        restricted_rule = (
            'relative_path.startswith("scripts/")\n'
            '            and relative_path.count("/") == 1\n'
            '            and relative_path.endswith'
        )
        mutated_source = source.replace(identity_rule, restricted_rule)
        self.assertNotEqual(source, mutated_source)
        mutant_path = self.scratch_root / "scan_domain_neutrality_mutant.py"
        mutant_path.write_text(mutated_source, encoding="utf-8")
        mutant = subprocess.run(
            [sys.executable, str(mutant_path), "--root", str(self.root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertIn("scripts/root_identity_probe.py:1", mutant.stdout)
        self.assertNotIn("scripts/memory/identity_probe.py:1", mutant.stdout)

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
        self.assertIn("scripts/root_identity_probe.py:1", result.stdout)
        self.assertIn("scripts/memory/identity_probe.py:1", result.stdout)
        self.assertIn("Area_comun/protocol/MEMORY_INDEX_POLICY.json:2", result.stdout)
        self.assertNotIn("runtime/memory/generated-pack.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
