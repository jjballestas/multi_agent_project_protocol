#!/usr/bin/env python3
"""Scan configured protocol surfaces for domain-specific terms.

Example trees are exempt by design because they are illustrative, may contain domain fixtures,
and are not canonical policy surfaces. Generated policy examples remain traceably covered by
scanning their canonical templates and regenerating the examples from those scanned templates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# Identity exceptions are term-and-line scoped.  The reasons below audit every file in
# the former whole-file allowlist; adding a new identity anywhere in one of these files
# therefore remains a finding.  Line movement intentionally fails closed and requires
# the exception to be reviewed alongside the moved code.  Term digests are SHA-256 of
# the case-folded identity, so the scanner does not flag its own exception declaration.
_EXEMPT_TERM_1 = "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93"
_EXEMPT_TERM_2 = "1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e"
_EXEMPT_TERM_3 = "fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7"
_EXEMPT_TERM_4 = "e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb"
_EXEMPT_TERM_5 = "9775f123593b08a132c7cf8f54927592c171e05134bae46a8c0ed7b40579b178"
_EXEMPT_TERM_6 = "c857d09db23e6822e3600bc06ad8d58f92ed62bc8efd81c753f77048662cb97d"

IDENTITY_LITERAL_EXEMPTIONS: dict[str, dict[str, object]] = {
    "runtime/apply.py": {
        "reason": "Compatibility fixture output preserves the historical implementer owner.",
        "lines": {440: (_EXEMPT_TERM_1,)},
    },
    "runtime/budget.py": {
        "reason": "Historical hardening annotations identify the independent review pass.",
        "lines": {68: (_EXEMPT_TERM_2,), 104: (_EXEMPT_TERM_2,)},
    },
    "runtime/context.py": {
        "reason": "Legacy fallback roles preserve the pre-registry compatibility contract.",
        "lines": {16: (_EXEMPT_TERM_1,), 17: (_EXEMPT_TERM_4, _EXEMPT_TERM_5)},
    },
    "runtime/eventlog.py": {
        "reason": "Legacy key fallbacks and historical review annotations are compatibility evidence.",
        "lines": {
            320: (_EXEMPT_TERM_2, _EXEMPT_TERM_3, _EXEMPT_TERM_1),
            472: (_EXEMPT_TERM_2,),
            1331: (_EXEMPT_TERM_2,),
        },
    },
    "runtime/ledger_ops.py": {
        "reason": "The legacy command description names the compatibility loop it builds for.",
        "lines": {319: (_EXEMPT_TERM_1,)},
    },
    "runtime/metrics.py": {
        "reason": "A historical hardening annotation identifies the independent review pass.",
        "lines": {196: (_EXEMPT_TERM_2,)},
    },
    "runtime/router.py": {
        "reason": "Legacy fallback envelopes preserve the pre-registry human-owner contract.",
        "lines": {
            120: (_EXEMPT_TERM_4, _EXEMPT_TERM_5),
            130: (_EXEMPT_TERM_4, _EXEMPT_TERM_5),
        },
    },
    "scripts/harness/peer_mailbox_cron.ps1": {
        "reason": "These occurrences identify the third-party provider CLI, executable, or install path.",
        "lines": {
            9: (_EXEMPT_TERM_1,),
            555: (_EXEMPT_TERM_1, _EXEMPT_TERM_6),
            562: (_EXEMPT_TERM_1,),
            572: (_EXEMPT_TERM_1,),
            581: (_EXEMPT_TERM_1,),
            582: (_EXEMPT_TERM_1,),
            589: (_EXEMPT_TERM_1,),
            605: (_EXEMPT_TERM_1,),
            1591: (_EXEMPT_TERM_1,),
        },
    },
    "scripts/memory/test_memory_db.py": {
        "reason": "Exact fixture lines exercise multi-agent indexing and per-agent memory isolation.",
        "lines": {
            205: (_EXEMPT_TERM_2, _EXEMPT_TERM_3, _EXEMPT_TERM_1),
            238: (_EXEMPT_TERM_1,),
            239: (_EXEMPT_TERM_1,),
            306: (_EXEMPT_TERM_3, _EXEMPT_TERM_1),
            337: (_EXEMPT_TERM_1,),
            346: (_EXEMPT_TERM_1,),
            351: (_EXEMPT_TERM_1,),
            374: (_EXEMPT_TERM_1,),
            388: (_EXEMPT_TERM_4,),
            393: (_EXEMPT_TERM_4,),
            415: (_EXEMPT_TERM_1,),
            473: (_EXEMPT_TERM_1,),
            477: (_EXEMPT_TERM_1,),
            482: (_EXEMPT_TERM_1,),
            488: (_EXEMPT_TERM_1,),
            494: (_EXEMPT_TERM_1,),
            501: (_EXEMPT_TERM_1,),
            528: (_EXEMPT_TERM_1,),
            553: (_EXEMPT_TERM_1,),
            558: (_EXEMPT_TERM_1,),
            596: (_EXEMPT_TERM_1,),
            912: (_EXEMPT_TERM_1,),
            997: (_EXEMPT_TERM_1,),
            1053: (_EXEMPT_TERM_1,),
            1095: (_EXEMPT_TERM_1,),
            1110: (_EXEMPT_TERM_1,),
            1161: (_EXEMPT_TERM_1,),
            1215: (_EXEMPT_TERM_1,),
            1219: (_EXEMPT_TERM_1,),
            1446: (_EXEMPT_TERM_1,),
            1759: (_EXEMPT_TERM_1,),
            1820: (_EXEMPT_TERM_1,),
            1897: (_EXEMPT_TERM_1,),
            1915: (_EXEMPT_TERM_1,),
            1944: (_EXEMPT_TERM_1,),
            1953: (_EXEMPT_TERM_1,),
            1976: (_EXEMPT_TERM_1,),
            1991: (_EXEMPT_TERM_1,),
            2014: (_EXEMPT_TERM_1,),
            2024: (_EXEMPT_TERM_1,),
            2041: (_EXEMPT_TERM_1,),
            2058: (_EXEMPT_TERM_1,),
            2063: (_EXEMPT_TERM_1,),
            2073: (_EXEMPT_TERM_1,),
            2079: (_EXEMPT_TERM_1,),
            2097: (_EXEMPT_TERM_1,),
            2116: (_EXEMPT_TERM_3, _EXEMPT_TERM_1),
            2123: (_EXEMPT_TERM_1,),
            2157: (_EXEMPT_TERM_1,),
            2158: (_EXEMPT_TERM_1,),
            2173: (_EXEMPT_TERM_1,),
            2195: (_EXEMPT_TERM_1,),
            2209: (_EXEMPT_TERM_1,),
            2218: (_EXEMPT_TERM_1,),
            2226: (_EXEMPT_TERM_1,),
            2235: (_EXEMPT_TERM_1,),
        },
    },
    "scripts/prune_state.py": {
        "reason": "Legacy state fixtures preserve the historical writer marker.",
        "lines": {
            272: (_EXEMPT_TERM_1,),
            409: (_EXEMPT_TERM_1,),
            410: (_EXEMPT_TERM_1,),
            411: (_EXEMPT_TERM_1,),
            412: (_EXEMPT_TERM_1,),
        },
    },
}
GENERIC_IDENTITY_TOKENS = {"agent", "human", "humano", "owner"}
REQUIRED_SCAN_GLOBS = (
    "scripts/**/*.py",
    "scripts/**/*.ps1",
    "Area_comun/protocol/*.json",
)
REQUIRED_EXEMPT_GLOBS = ("runtime/memory/**",)


def append_required_patterns(configured: list[str], required: tuple[str, ...]) -> list[str]:
    return [*configured, *(pattern for pattern in required if pattern not in configured)]


def identity_scan_path(relative_path: str) -> bool:
    return (
        (relative_path.startswith("runtime/") and relative_path.endswith(".py"))
        or (
            relative_path.startswith("scripts/")
            and relative_path.endswith((".py", ".ps1"))
        )
    )


def is_identity_literal_exempt(relative_path: str, line_number: int, term: str) -> bool:
    declaration = IDENTITY_LITERAL_EXEMPTIONS.get(relative_path)
    if not declaration:
        return False
    lines = declaration["lines"]
    if not isinstance(lines, dict):
        return False
    allowed_terms = lines.get(line_number, ())
    digest = hashlib.sha256(term.casefold().encode("utf-8")).hexdigest()
    return digest in allowed_terms


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
                if not identity_scan_path(relative_path):
                    continue
                if is_identity_literal_exempt(relative_path, line_number, term):
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
    scan_globs = append_required_patterns(neutrality.get("scan_globs") or [], REQUIRED_SCAN_GLOBS)
    exempt_globs = append_required_patterns(
        neutrality.get("exempt_globs") or [], REQUIRED_EXEMPT_GLOBS
    )
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
