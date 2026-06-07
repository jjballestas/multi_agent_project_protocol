#!/usr/bin/env python3
"""Generate a deterministic release manifest wrapping the protocol SBOM."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from generate_sbom import DEFAULT_EXCLUDE_GLOBS, DEFAULT_INCLUDE_GLOBS, build_sbom, canonical_json


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_manifest(
    root: Path,
    *,
    commit: str,
    timestamp: str,
    include_globs: list[str],
    exclude_globs: list[str],
) -> dict[str, Any]:
    sbom = build_sbom(
        root,
        commit=commit,
        timestamp=timestamp,
        include_globs=include_globs,
        exclude_globs=exclude_globs,
    )
    sbom_hash = sha256_text(canonical_json(sbom))
    manifest: dict[str, Any] = {
        "schema_version": "protocol_release_manifest.v1",
        "generated_by": "scripts/generate_manifest.py",
        "commit": commit,
        "timestamp": timestamp,
        "version_axes": sbom["version_axes"],
        "file_count": sbom["file_count"],
        "sbom_hash": sbom_hash,
        "sbom": sbom,
    }
    manifest["manifest_hash"] = sha256_text(canonical_json(manifest))
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic protocol release manifest.")
    parser.add_argument("--root", default=".", help="Repository root to inventory.")
    parser.add_argument("--commit", required=True, help="Commit identifier to record in the manifest.")
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
    payload = build_manifest(
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
