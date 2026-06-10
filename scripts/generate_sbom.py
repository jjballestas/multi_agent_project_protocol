#!/usr/bin/env python3
"""Generate a deterministic package SBOM for the protocol repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_INCLUDE_GLOBS = [
    ".github/workflows/**",
    "AGENTS.md",
    "AGENTS.template.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "LICENSE",
    "README.md",
    "README_INSTANCIACION.md",
    "protocol.config.json",
    "protocol.config.template.json",
    "Area_comun/README.md",
    "Area_comun/README.template.md",
    "Area_comun/artifacts/**",
    "Area_comun/decisions/**",
    "Area_comun/protocol/**",
    "Area_comun/reports/*TEMPLATE*",
    "Area_comun/specs/**",
    "Area_comun/state/*.template.json",
    "examples/**",
    "profiles/**",
    "runtime/**",
    "scripts/**",
]

DEFAULT_EXCLUDE_GLOBS = [
    ".git/**",
    "dist/**",
    "personal/**",
    "Area_comun/handoffs/**",
    "Area_comun/mailbox/**",
    "Area_comun/reports/REPORT-*",
    "Area_comun/state/*.json",
    "Area_comun/tasks/**",
    "runtime/runs/**",
    "runtime/state/**",
    "**/__pycache__/**",
    "**/*.pyc",
]


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


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, dict) else {}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_source_files(root: Path, include_globs: list[str], exclude_globs: list[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root).as_posix()
        if matches_any(relative_path, include_globs) and not matches_any(relative_path, exclude_globs):
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def profile_versions(root: Path) -> list[dict[str, str]]:
    profiles: list[dict[str, str]] = []
    for manifest in sorted(root.glob("profiles/*/profile.manifest.json")):
        payload = read_json(manifest)
        profile_id = str(payload.get("profile_id") or manifest.parent.name)
        profile_version = str(payload.get("profile_version") or "")
        profiles.append({"profile_id": profile_id, "profile_version": profile_version})
    return profiles


def build_sbom(
    root: Path,
    *,
    commit: str,
    timestamp: str,
    include_globs: list[str],
    exclude_globs: list[str],
) -> dict[str, Any]:
    config = read_json(root / "protocol.config.json")
    turn_schema = read_json(root / "runtime/turn_schema.json")
    files = [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_file(path),
            "size": path.stat().st_size,
        }
        for path in iter_source_files(root, include_globs, exclude_globs)
    ]
    return {
        "schema_version": "protocol_sbom.v1",
        "generated_by": "scripts/generate_sbom.py",
        "commit": commit,
        "timestamp": timestamp,
        "version_axes": {
            "protocol": str(config.get("protocol_version") or ""),
            "runtime": str(config.get("runtime_version") or ""),
            "schema": {"turn_schema": str(turn_schema.get("schema_version") or "")},
            "profiles": profile_versions(root),
        },
        "source_globs": {
            "include": include_globs,
            "exclude": exclude_globs,
        },
        "file_count": len(files),
        "files": files,
    }


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic protocol package SBOM.")
    parser.add_argument("--root", default=".", help="Repository root to inventory.")
    parser.add_argument("--commit", required=True, help="Commit identifier to record in the SBOM.")
    parser.add_argument("--timestamp", required=True, help="Timestamp to record; provided by caller for determinism.")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    parser.add_argument(
        "--include-glob",
        action="append",
        dest="include_globs",
        help="Additional source include glob. Defaults are used unless --no-default-globs is set.",
    )
    parser.add_argument("--exclude-glob", action="append", dest="exclude_globs", help="Additional exclude glob.")
    parser.add_argument("--no-default-globs", action="store_true", help="Use only explicitly provided include globs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    include_globs = [] if args.no_default_globs else list(DEFAULT_INCLUDE_GLOBS)
    include_globs.extend(args.include_globs or [])
    exclude_globs = list(DEFAULT_EXCLUDE_GLOBS)
    exclude_globs.extend(args.exclude_globs or [])
    payload = build_sbom(
        root,
        commit=args.commit,
        timestamp=args.timestamp,
        include_globs=include_globs,
        exclude_globs=exclude_globs,
    )
    rendered = canonical_json(payload)
    if args.output == "-":
        sys.stdout.buffer.write(rendered.encode("utf-8"))
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(rendered.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
