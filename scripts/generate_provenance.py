#!/usr/bin/env python3
"""Generate and verify deterministic SLSA-lite release provenance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from generate_sbom import canonical_json


DEFAULT_PACKAGE_NAME = "multi_agent_project_protocol"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def default_subject_name(manifest: dict[str, Any]) -> str:
    version_axes = manifest.get("version_axes") if isinstance(manifest.get("version_axes"), dict) else {}
    protocol_version = str(version_axes.get("protocol") or "")
    return f"{DEFAULT_PACKAGE_NAME}@{protocol_version}"


def manifest_sbom_hash(manifest: dict[str, Any]) -> str:
    return str(manifest.get("sbom_hash") or "")


def build_provenance(
    manifest: dict[str, Any],
    *,
    builder_id: str,
    commit: str,
    process: str,
    timestamp: str,
    subject_name: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "protocol_provenance.v1",
        "generated_by": "scripts/generate_provenance.py",
        "subject": {
            "name": subject_name or default_subject_name(manifest),
            "digest": {"sha256": manifest_sbom_hash(manifest)},
        },
        "builder": {"id": builder_id},
        "invocation": {"commit": commit, "process": process},
        "metadata": {"schema": "provenance.v1", "timestamp": timestamp},
    }


def provenance_subject(provenance: dict[str, Any]) -> dict[str, Any]:
    subject = provenance.get("subject")
    return subject if isinstance(subject, dict) else {}


def provenance_subject_digest(provenance: dict[str, Any]) -> str:
    subject = provenance_subject(provenance)
    digest = subject.get("digest") if isinstance(subject.get("digest"), dict) else {}
    return str(digest.get("sha256") or "")


def verify_provenance(manifest_path: Path, provenance_path: Path) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    provenance = read_json(provenance_path)
    expected = manifest_sbom_hash(manifest)
    actual = provenance_subject_digest(provenance)
    ok = actual == expected
    payload: dict[str, Any] = {
        "schema_version": "protocol_provenance_verify.v1",
        "ok": ok,
        "manifest": manifest_path.as_posix(),
        "provenance": provenance_path.as_posix(),
        "expected_sbom_hash": expected,
        "actual_subject_digest": actual,
        "subject_name": str(provenance_subject(provenance).get("name") or ""),
    }
    if not ok:
        payload["error"] = "subject.digest.sha256 does not match manifest.sbom_hash"
    return payload


def write_payload(payload: dict[str, Any], output: str) -> None:
    rendered = canonical_json(payload)
    if output == "-":
        sys.stdout.buffer.write(rendered.encode("utf-8"))
    else:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(rendered.encode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or verify deterministic protocol release provenance.")
    parser.add_argument("--manifest", required=True, help="Release manifest JSON path.")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    parser.add_argument("--verify", action="store_true", help="Verify a provenance file against the manifest.")
    parser.add_argument("--provenance", help="Provenance JSON path to verify; required with --verify.")
    parser.add_argument("--builder-id", help="Builder or actor identifier; required unless --verify.")
    parser.add_argument("--commit", help="Commit identifier to record; required unless --verify.")
    parser.add_argument("--process", help="Declared build command or recipe; required unless --verify.")
    parser.add_argument("--timestamp", help="Provided timestamp to record; required unless --verify.")
    parser.add_argument("--subject-name", help="Override subject name. Defaults to multi_agent_project_protocol@<protocol_version>.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.verify:
        if not args.provenance:
            raise SystemExit("--provenance is required with --verify")
        payload = verify_provenance(Path(args.manifest).resolve(), Path(args.provenance).resolve())
        write_payload(payload, args.output)
        return 0 if payload["ok"] else 1

    missing = [
        name
        for name, value in {
            "--builder-id": args.builder_id,
            "--commit": args.commit,
            "--process": args.process,
            "--timestamp": args.timestamp,
        }.items()
        if not value
    ]
    if missing:
        raise SystemExit(f"missing required arguments for provenance generation: {', '.join(missing)}")

    payload = build_provenance(
        read_json(Path(args.manifest).resolve()),
        builder_id=args.builder_id,
        commit=args.commit,
        process=args.process,
        timestamp=args.timestamp,
        subject_name=args.subject_name,
    )
    write_payload(payload, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
