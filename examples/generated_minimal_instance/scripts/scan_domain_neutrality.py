#!/usr/bin/env python3
"""Scan configured protocol surfaces for domain-specific terms.

Example trees are exempt by design because they are illustrative, may contain domain fixtures,
and are not canonical policy surfaces. Generated policy examples remain traceably covered by
scanning their canonical templates and regenerating the examples from those scanned templates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LEGACY_IDENTITY_LITERAL_FILES = {
    "runtime/apply.py",
    "runtime/budget.py",
    "runtime/context.py",
    "runtime/eventlog.py",
    "runtime/ledger_ops.py",
    "runtime/metrics.py",
    "runtime/router.py",
    "scripts/prune_state.py",
}
GENERIC_IDENTITY_TOKENS = {"agent", "human", "humano", "owner"}


def identity_scan_path(relative_path: str) -> bool:
    return (
        (relative_path.startswith("runtime/") and relative_path.endswith(".py"))
        or (relative_path.startswith("scripts/") and relative_path.endswith((".py", ".ps1")))
    )


def glob_to_regex(pattern: str) -> re.Pattern[str]:
    normalized = pattern.replace("\\", "/").strip("/")
    parts: list[str] = ["^"]
    i = 0
    while i < len(normalized):
        char = normalized[i]
        if char == "*":
            if i + 1 < len(normalized) and normalized[i + 1] == "*":
                parts.append(".*")
                i += 2
            else:
                parts.append("[^/]*")
                i += 1
        elif char == "?":
            parts.append("[^/]")
            i += 1
        else:
            parts.append(re.escape(char))
            i += 1
    parts.append("$")
    return re.compile("".join(parts))


def matches_any(relative_path: str, patterns: list[str]) -> bool:
    return any(glob_to_regex(pattern).match(relative_path) for pattern in patterns)


def iter_scanned_files(root: Path, scan_globs: list[str], exempt_globs: list[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root).as_posix()
        if matches_any(relative_path, scan_globs) and not matches_any(relative_path, exempt_globs):
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def load_config(root: Path) -> dict:
    config_path = root / "protocol.config.json"
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def configured_identity_terms(config: dict) -> list[str]:
    terms: set[str] = set()
    registry = config.get("agent_registry") if isinstance(config.get("agent_registry"), dict) else {}
    for agent in registry.get("agents") or []:
        if isinstance(agent, dict):
            value = str(agent.get("id") or "").strip()
            # Exempt generic identity words (agent/human/owner/...) as agent ids too,
            # consistent with the agent_roles handling below -- an agent legitimately named
            # "Human"/"Owner"/"Agent" must not false-flag where those words appear in neutral code.
            if len(value) >= 3 and value.casefold() not in GENERIC_IDENTITY_TOKENS:
                terms.add(value)
    roles = config.get("agent_roles") if isinstance(config.get("agent_roles"), dict) else {}
    for value in roles.values():
        text = str(value or "").strip()
        if len(text) >= 3 and text.casefold() not in GENERIC_IDENTITY_TOKENS:
            terms.add(text)
        for token in re.split(r"\s+", text):
            clean = token.strip()
            if len(clean) >= 4 and clean.casefold() not in GENERIC_IDENTITY_TOKENS:
                terms.add(clean)
    return sorted(terms, key=str.casefold)


def compile_terms(terms: list[str], kind: str) -> list[tuple[str, re.Pattern[str], str]]:
    compiled: list[tuple[str, re.Pattern[str], str]] = []
    for term in terms:
        clean_term = str(term).strip()
        if not clean_term:
            continue
        pattern = re.compile(rf"(?<!\w){re.escape(clean_term)}(?!\w)", re.IGNORECASE)
        compiled.append((clean_term, pattern, kind))
    return compiled


def scan_file(root: Path, path: Path, terms: list[tuple[str, re.Pattern[str], str]]) -> list[str]:
    findings: list[str] = []
    relative_path = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for term, pattern, kind in terms:
            if kind == "identity":
                if not identity_scan_path(relative_path) or relative_path in LEGACY_IDENTITY_LITERAL_FILES:
                    continue
            if pattern.search(line):
                findings.append(f"{relative_path}:{line_number}: {term}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan protocol files for domain-specific terms.")
    parser.add_argument("--root", default=".", help="Repository or instance root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config = load_config(root)
    neutrality = config.get("domain_neutrality")
    if not neutrality or neutrality.get("enabled") is False:
        return 0

    denylist = neutrality.get("denylist") or []
    scan_globs = neutrality.get("scan_globs") or []
    exempt_globs = neutrality.get("exempt_globs") or []
    if (root / "connectors").exists() and "connectors/**" not in scan_globs:
        scan_globs = [*scan_globs, "connectors/**"]
    if (root / "skills").exists() and "skills/**" not in scan_globs:
        scan_globs = [*scan_globs, "skills/**"]
    terms = [
        *compile_terms(denylist, "domain"),
        *compile_terms(configured_identity_terms(config), "identity"),
    ]

    if not terms or not scan_globs:
        return 0

    findings: list[str] = []
    for path in iter_scanned_files(root, scan_globs, exempt_globs):
        findings.extend(scan_file(root, path, terms))

    for finding in findings:
        print(finding)

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
