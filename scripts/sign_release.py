#!/usr/bin/env python3
"""Sign a protocol release digest with a configurable backend."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path
from typing import Any

from generate_sbom import canonical_json


FIXTURE_BACKEND = "fixture-hmac-sha256"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def digest_from_manifest(path: Path) -> str:
    return str(read_json(path).get("sbom_hash") or "")


def read_material(reference: str) -> str:
    candidate = Path(reference)
    if candidate.exists():
        return candidate.read_text(encoding="utf-8-sig").strip()
    return reference.strip()


def fixture_key_id(material: str) -> str:
    return "fixture:" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def sign_fixture(subject_digest: str, material: str) -> str:
    return hmac.new(material.encode("utf-8"), subject_digest.encode("utf-8"), hashlib.sha256).hexdigest()


def build_signature(subject_digest: str, *, backend: str, key_reference: str, key_id: str | None = None) -> dict[str, Any]:
    material = read_material(key_reference)
    if backend != FIXTURE_BACKEND:
        raise ValueError(f"unsupported signing backend: {backend}")
    return {
        "schema_version": "protocol_release_signature.v1",
        "generated_by": "scripts/sign_release.py",
        "subject_digest": subject_digest,
        "backend": backend,
        "key_id": key_id or fixture_key_id(material),
        "signature": sign_fixture(subject_digest, material),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sign a protocol release digest.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--manifest", help="Release manifest JSON path; signs manifest.sbom_hash.")
    source.add_argument("--digest", help="Digest to sign directly.")
    parser.add_argument("--backend", required=True, help=f"Signing backend id, e.g. {FIXTURE_BACKEND}.")
    parser.add_argument("--key", required=True, help="Local signing material reference. Do not commit real keys.")
    parser.add_argument("--key-id", help="Public key identifier to record. Defaults to a fixture-derived id.")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    subject_digest = args.digest or digest_from_manifest(Path(args.manifest).resolve())
    try:
        payload = build_signature(subject_digest, backend=args.backend, key_reference=args.key, key_id=args.key_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
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
