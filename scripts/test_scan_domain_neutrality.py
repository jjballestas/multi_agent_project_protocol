#!/usr/bin/env python3
"""Regression coverage for mandatory domain-neutrality scan surfaces."""

from __future__ import annotations

import importlib.util
import hashlib
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
        "negative": "The PowerShell gate must reject the same leak and must not restore a whole-file exemption.",
        "mutation": ".replace(powershell_narrow_rule, powershell_whole_file_rule)",
        "boundaries": (
            "self.assertEqual(python_findings, powershell_findings)",
            'self.assertIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", powershell.stdout)',
            'self.assertNotIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", mutant.stdout)',
            'self.assertIn(f"scripts/unlisted_probe.py:1: {coordinator_identity}", mutant.stdout)',
        ),
        "exercised_by": "test_powershell_whole_file_exemption_mutation_is_killed",
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

    def run_python_scanner(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCANNER_PATH), "--root", str(self.root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_powershell_scanner(
        self, scanner_path: Path = POWERSHELL_SCANNER_PATH
    ) -> subprocess.CompletedProcess[str]:
        executable = shutil.which("pwsh") or shutil.which("powershell")
        if not executable:
            self.skipTest("PowerShell is not installed")
        return subprocess.run(
            [executable, "-NoProfile", "-File", str(scanner_path), "-Root", str(self.root)],
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

    def test_powershell_whole_file_exemption_mutation_is_killed(self) -> None:
        """PERMANENT_NEGATIVE: NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY"""
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

        python = self.run_python_scanner()
        powershell = self.run_powershell_scanner()
        self.assertEqual(python.returncode, 1, python.stdout + python.stderr)
        self.assertEqual(powershell.returncode, 1, powershell.stdout + powershell.stderr)
        python_findings = set(python.stdout.splitlines())
        powershell_findings = set(powershell.stdout.splitlines())
        self.assertEqual(python_findings, powershell_findings)
        self.assertIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", powershell.stdout)

        source = POWERSHELL_SCANNER_PATH.read_text(encoding="utf-8-sig")
        powershell_narrow_rule = (
            "if (Test-IdentityLiteralExempt -RelativePath $file.RelativePath "
            "-LineNumber ($lineIndex + 1) -Term $scanTerm.Term) {"
        )
        powershell_whole_file_rule = (
            "if ($IdentityLiteralExemptions.ContainsKey($file.RelativePath)) {"
        )
        mutated_source = source.replace(powershell_narrow_rule, powershell_whole_file_rule)
        self.assertNotEqual(source, mutated_source)
        mutant_path = self.scratch_root / "scan_domain_neutrality_whole_file_mutant.ps1"
        mutant_path.write_text(mutated_source, encoding="utf-8")
        mutant = self.run_powershell_scanner(mutant_path)
        self.assertNotIn(f"scripts/harness/peer_mailbox_cron.ps1:10: {coordinator_identity}", mutant.stdout)
        self.assertIn(f"scripts/unlisted_probe.py:1: {coordinator_identity}", mutant.stdout)

    def test_identity_exemption_inventories_are_one_to_one_and_in_parity(self) -> None:
        scanner = load_scanner()
        powershell_source = POWERSHELL_SCANNER_PATH.read_text(encoding="utf-8-sig")
        inventory_block = powershell_source.split("$IdentityLiteralExemptions = @{", 1)[1].split(
            "$GenericIdentityTokens", 1
        )[0]
        powershell_inventory: dict[str, dict[int, tuple[str, ...]]] = {}
        current_path: str | None = None
        for line in inventory_block.splitlines():
            path_match = re.match(r'^    "([^"]+)" = @\{$', line)
            if path_match:
                current_path = path_match.group(1)
                powershell_inventory[current_path] = {}
                continue
            line_match = re.match(r'^            (\d+) = @\((.*)\)$', line)
            if line_match and current_path:
                hashes = tuple(re.findall(r'"([0-9a-f]{64})"', line_match.group(2)))
                powershell_inventory[current_path][int(line_match.group(1))] = hashes

        python_inventory = {
            path: {int(line): tuple(hashes) for line, hashes in declaration["lines"].items()}
            for path, declaration in scanner.IDENTITY_LITERAL_EXEMPTIONS.items()
        }
        self.assertEqual(powershell_inventory, python_inventory)

        configured_terms = scanner.configured_identity_terms(scanner.load_config(REPO_ROOT))
        terms_by_digest = {
            hashlib.sha256(term.casefold().encode("utf-8")).hexdigest(): term
            for term in configured_terms
        }
        declared_exemption_count = 0
        for relative_path, lines in python_inventory.items():
            source_lines = (REPO_ROOT / relative_path).read_text(encoding="utf-8-sig").splitlines()
            for line_number, hashes in lines.items():
                self.assertLessEqual(line_number, len(source_lines), relative_path)
                source_line = source_lines[line_number - 1]
                for digest in hashes:
                    term = terms_by_digest[digest]
                    matches = re.findall(rf"(?i)(?<!\w){re.escape(term)}(?!\w)", source_line)
                    self.assertGreaterEqual(len(matches), 1, f"{relative_path}:{line_number}:{term}")
                    declared_exemption_count += 1
        self.assertEqual(declared_exemption_count, 91)

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
