#!/usr/bin/env python3
"""Regression coverage for mandatory domain-neutrality scan surfaces."""

from __future__ import annotations

import importlib.util
import json
import re
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
    {
        "id": "NEG-NEUTRALITY-IDENTITY-EXEMPTION-SCOPE",
        "negative": "A whole-file identity exemption must not hide a new identity outside its declared lines.",
        "mutation": ".replace(narrow_rule, whole_file_rule)",
        "boundaries": (
            'self.assertNotIn(f"scripts/harness/peer_mailbox_cron.ps1:9: {provider_identity}", baseline.stdout)',
            'self.assertIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", baseline.stdout)',
            'self.assertIn(f"scripts/unlisted_probe.py:1: {coordinator_identity}", baseline.stdout)',
            'self.assertNotIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", mutant.stdout)',
            'self.assertIn(f"scripts/unlisted_probe.py:1: {coordinator_identity}", mutant.stdout)',
        ),
        "exercised_by": "test_whole_file_identity_exemption_mutation_is_killed",
    },
    {
        "id": "NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY",
        "negative": "Real-tree identity probes must produce identical findings through both gates, including an unseen route.",
        "mutation": "indented_source = source.replace(",
        "boundaries": (
            "self.assertEqual(expected_findings, python_findings)",
            "self.assertEqual(expected_findings, powershell_findings)",
            "self.assertNotEqual(python_findings, indented_findings)",
            "self.assertNotEqual(python_findings, outside_findings)",
            "self.assertNotEqual(expected_findings, symmetric_python_findings)",
        ),
        "exercised_by": "test_real_tree_identity_parity_rejects_single_scanner_exemptions",
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
        provider_identity = "Code" + "x"
        coordinator_identity = "Arqui" + "tecto"
        config = {
            "agent_registry": {
                "agents": [
                    {"id": "SampleAgent"},
                    {"id": provider_identity},
                    {"id": coordinator_identity},
                ]
            },
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

    def run_python_scanner(
        self, scanner_path: Path = SCANNER_PATH, root: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(scanner_path), "--root", str(root or self.root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_powershell_scanner(
        self, scanner_path: Path = POWERSHELL_SCANNER_PATH, root: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        executable = shutil.which("pwsh") or shutil.which("powershell")
        if not executable:
            self.skipTest("PowerShell is not installed")
        return subprocess.run(
            [executable, "-NoProfile", "-File", str(scanner_path), "-Root", str(root or self.root)],
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

    def test_whole_file_identity_exemption_mutation_is_killed(self) -> None:
        """PERMANENT_NEGATIVE: NEG-NEUTRALITY-IDENTITY-EXEMPTION-SCOPE"""
        provider_identity = "Code" + "x"
        coordinator_identity = "Arqui" + "tecto"
        harness = self.root / "scripts" / "harness" / "peer_mailbox_cron.ps1"
        harness.parent.mkdir(parents=True)
        harness.write_text(
            "\n" * 8
            + f'[ValidateSet("Auto", "Anthropic", "{provider_identity}")][string]$AgentProvider = "Auto",\n'
            + f'$DefaultCoordinator = "{coordinator_identity}"\n',
            encoding="utf-8",
        )
        (self.root / "scripts" / "unlisted_probe.py").write_text(
            f'DEFAULT_COORDINATOR = "{coordinator_identity}"\n', encoding="utf-8"
        )

        baseline = self.run_python_scanner()
        self.assertEqual(baseline.returncode, 1, baseline.stdout + baseline.stderr)
        self.assertNotIn(f"scripts/harness/peer_mailbox_cron.ps1:9: {provider_identity}", baseline.stdout)
        self.assertIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", baseline.stdout)
        self.assertIn(f"scripts/unlisted_probe.py:1: {coordinator_identity}", baseline.stdout)

        source = SCANNER_PATH.read_text(encoding="utf-8")
        narrow_rule = "if is_identity_literal_exempt(relative_path, line_number, term):"
        whole_file_rule = "if relative_path in IDENTITY_LITERAL_EXEMPTIONS:"
        mutated_source = source.replace(narrow_rule, whole_file_rule)
        self.assertNotEqual(source, mutated_source)
        mutant_path = self.scratch_root / "scan_domain_neutrality_whole_file_mutant.py"
        mutant_path.write_text(mutated_source, encoding="utf-8")
        mutant = subprocess.run(
            [sys.executable, str(mutant_path), "--root", str(self.root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", mutant.stdout)
        self.assertIn(f"scripts/unlisted_probe.py:1: {coordinator_identity}", mutant.stdout)

    def test_real_tree_identity_parity_rejects_single_scanner_exemptions(self) -> None:
        """PERMANENT_NEGATIVE: NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY"""
        scanner = load_scanner()
        probe_root = self.scratch_root / "real-tree-probe"
        probe_root.mkdir()
        shutil.copy2(REPO_ROOT / "protocol.config.json", probe_root / "protocol.config.json")
        config = scanner.load_config(REPO_ROOT)["domain_neutrality"]
        scan_globs = scanner.append_required_patterns(
            config["scan_globs"], scanner.REQUIRED_SCAN_GLOBS
        )
        exempt_globs = scanner.append_required_patterns(
            config["exempt_globs"], scanner.REQUIRED_EXEMPT_GLOBS
        )
        configured_identities = scanner.configured_identity_terms(scanner.load_config(REPO_ROOT))
        probe_identity = "Code" + "x"
        expected_findings: set[str] = set()
        for source_path in scanner.iter_scanned_files(REPO_ROOT, scan_globs, exempt_globs):
            relative_path = source_path.relative_to(REPO_ROOT).as_posix()
            if not scanner.identity_scan_path(relative_path):
                continue
            target_path = probe_root / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            lines = source_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
            first_probe_line = len(lines) + 1
            lines.extend(f'# real-tree parity probe: {term}' for term in configured_identities)
            target_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            for offset, probe_term in enumerate(configured_identities):
                for matched_term in configured_identities:
                    if re.search(
                        rf"(?i)(?<!\w){re.escape(matched_term)}(?!\w)", probe_term
                    ):
                        expected_findings.add(
                            f"{relative_path}:{first_probe_line + offset}: {matched_term}"
                        )

        unseen_relative_path = "scripts/remediation_slip1_probe.py"
        unseen_path = probe_root / unseen_relative_path
        unseen_lines = [probe_identity, *[term for term in configured_identities if term != probe_identity]]
        unseen_path.write_text(
            "".join(f'OWNER = "{term}"\n' for term in unseen_lines), encoding="utf-8"
        )
        for line_number, probe_term in enumerate(unseen_lines, start=1):
            for matched_term in configured_identities:
                if re.search(rf"(?i)(?<!\w){re.escape(matched_term)}(?!\w)", probe_term):
                    expected_findings.add(
                        f"{unseen_relative_path}:{line_number}: {matched_term}"
                    )

        python = subprocess.run(
            [sys.executable, str(SCANNER_PATH), "--root", str(probe_root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        powershell = self.run_powershell_scanner(root=probe_root)
        self.assertEqual(python.returncode, 1, python.stdout + python.stderr)
        self.assertEqual(powershell.returncode, 1, powershell.stdout + powershell.stderr)
        python_findings = set(python.stdout.splitlines())
        powershell_findings = set(powershell.stdout.splitlines())
        self.assertEqual(expected_findings, python_findings)
        self.assertEqual(expected_findings, powershell_findings)

        source = POWERSHELL_SCANNER_PATH.read_text(encoding="utf-8-sig")
        digest = "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93"
        exemption = (
            f'  "{unseen_relative_path}" = @{{\n'
            '        Reason = "SLIP-1 indentation mutant."\n'
            f'        Lines = @{{ 1 = @("{digest}") }}\n'
            '    }\n'
        )
        indented_source = source.replace(
            "$IdentityLiteralExemptions = @{\n",
            "$IdentityLiteralExemptions = @{\n" + exemption,
            1,
        )
        self.assertNotEqual(source, indented_source)
        indented_path = self.scratch_root / "scan_domain_neutrality_indented_mutant.ps1"
        indented_path.write_text(indented_source, encoding="utf-8")
        indented = self.run_powershell_scanner(indented_path, probe_root)
        indented_findings = set(indented.stdout.splitlines())
        self.assertNotEqual(python_findings, indented_findings)
        self.assertNotIn(f"{unseen_relative_path}:1: {probe_identity}", indented_findings)

        outside_assignment = (
            f'$IdentityLiteralExemptions["{unseen_relative_path}"] = @{{\n'
            '    Reason = "SLIP-1 outside-block mutant."\n'
            f'    Lines = @{{ 1 = @("{digest}") }}\n'
            '}\n'
        )
        outside_source = source.replace(
            "$GenericIdentityTokens = @(", outside_assignment + "$GenericIdentityTokens = @(", 1
        )
        self.assertNotEqual(source, outside_source)
        outside_path = self.scratch_root / "scan_domain_neutrality_outside_mutant.ps1"
        outside_path.write_text(outside_source, encoding="utf-8")
        outside = self.run_powershell_scanner(outside_path, probe_root)
        outside_findings = set(outside.stdout.splitlines())
        self.assertNotEqual(python_findings, outside_findings)
        self.assertNotIn(f"{unseen_relative_path}:1: {probe_identity}", outside_findings)

        python_source = SCANNER_PATH.read_text(encoding="utf-8")
        scan_loop_rule = "    for line_number, line in enumerate(text.splitlines(), start=1):\n"
        symmetric_python_source = python_source.replace(
            scan_loop_rule,
            f'    if relative_path == "{unseen_relative_path}":\n'
            + "        return []\n"
            + scan_loop_rule,
            1,
        )
        self.assertNotEqual(python_source, symmetric_python_source)
        symmetric_python_path = self.scratch_root / "scan_domain_neutrality_symmetric_mutant.py"
        symmetric_python_path.write_text(symmetric_python_source, encoding="utf-8")
        symmetric_powershell_source = source.replace(
            "foreach ($file in $files) {\n",
            "foreach ($file in $files) {\n"
            + f'    if ($file.RelativePath -eq "{unseen_relative_path}") {{ continue }}\n',
            1,
        )
        self.assertNotEqual(source, symmetric_powershell_source)
        symmetric_powershell_path = (
            self.scratch_root / "scan_domain_neutrality_symmetric_mutant.ps1"
        )
        symmetric_powershell_path.write_text(symmetric_powershell_source, encoding="utf-8")
        symmetric_python = self.run_python_scanner(symmetric_python_path, probe_root)
        symmetric_powershell = self.run_powershell_scanner(symmetric_powershell_path, probe_root)
        symmetric_python_findings = set(symmetric_python.stdout.splitlines())
        symmetric_powershell_findings = set(symmetric_powershell.stdout.splitlines())
        self.assertEqual(symmetric_python_findings, symmetric_powershell_findings)
        self.assertNotEqual(expected_findings, symmetric_python_findings)
        self.assertNotIn(
            f"{unseen_relative_path}:1: {probe_identity}", symmetric_python_findings
        )

    def test_powershell_scanner_matches_required_coverage_when_available(self) -> None:
        result = self.run_powershell_scanner()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("scripts/memory/nested_probe.py:1", result.stdout)
        self.assertIn("scripts/root_identity_probe.py:1", result.stdout)
        self.assertIn("scripts/memory/identity_probe.py:1", result.stdout)
        self.assertIn("Area_comun/protocol/MEMORY_INDEX_POLICY.json:2", result.stdout)
        self.assertNotIn("runtime/memory/generated-pack.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
