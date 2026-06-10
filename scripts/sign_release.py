#!/usr/bin/env python3
"""Sign a protocol release digest with a configurable backend."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from generate_sbom import canonical_json


FIXTURE_BACKEND = "fixture-hmac-sha256"
EXTERNAL_COMMAND_BACKEND = "external-command"
EXTERNAL_SIGNATURE_FIELDS = {"signature", "bundle"}


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


def split_command(command: str) -> list[str]:
    parts = shlex.split(command, posix=os.name != "nt")
    if not parts:
        raise ValueError("external signing command is empty")
    return parts


def render_command(command: str, values: dict[str, str]) -> tuple[list[str], bool]:
    used_placeholder = False
    rendered: list[str] = []
    for part in split_command(command):
        updated = part
        for key, value in values.items():
            placeholder = "{" + key + "}"
            if placeholder in updated:
                if not value:
                    raise ValueError(f"external signing command uses unavailable placeholder: {placeholder}")
                updated = updated.replace(placeholder, value)
                used_placeholder = True
        rendered.append(updated)
    return rendered, used_placeholder


def run_external_sign_command(command: str, *, subject_digest: str, manifest_path: Path | None) -> str:
    values = {
        "digest": subject_digest,
        "manifest": manifest_path.as_posix() if manifest_path is not None else "",
    }
    args, used_placeholder = render_command(command, values)
    stdin = None if used_placeholder else subject_digest + "\n"
    try:
        result = subprocess.run(args, input=stdin, text=True, capture_output=True, check=False)
    except OSError as exc:
        raise ValueError(f"external signing command failed to start: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        suffix = f": {detail}" if detail else ""
        raise ValueError(f"external signing command failed with exit code {result.returncode}{suffix}")
    signature = result.stdout.strip()
    if not signature:
        raise ValueError("external signing command produced no stdout")
    return signature


def build_signature(
    subject_digest: str,
    *,
    backend: str,
    key_reference: str | None = None,
    key_id: str | None = None,
    sign_command: str | None = None,
    manifest_path: Path | None = None,
    identity: str | None = None,
    issuer: str | None = None,
    signature_field: str = "signature",
) -> dict[str, Any]:
    if not subject_digest:
        raise ValueError("subject digest is empty")
    if backend == FIXTURE_BACKEND:
        if key_reference is None:
            raise ValueError(f"--key is required for backend {FIXTURE_BACKEND}")
        material = read_material(key_reference)
        return {
            "schema_version": "protocol_release_signature.v1",
            "generated_by": "scripts/sign_release.py",
            "subject_digest": subject_digest,
            "backend": backend,
            "key_id": key_id or fixture_key_id(material),
            "signature": sign_fixture(subject_digest, material),
        }
    if backend == EXTERNAL_COMMAND_BACKEND:
        if not sign_command:
            raise ValueError(f"--sign-command is required for backend {EXTERNAL_COMMAND_BACKEND}")
        if signature_field not in EXTERNAL_SIGNATURE_FIELDS:
            allowed = ", ".join(sorted(EXTERNAL_SIGNATURE_FIELDS))
            raise ValueError(f"--signature-field must be one of: {allowed}")
        external_output = run_external_sign_command(sign_command, subject_digest=subject_digest, manifest_path=manifest_path)
        payload: dict[str, Any] = {
            "schema_version": "protocol_release_signature.v1",
            "generated_by": "scripts/sign_release.py",
            "subject_digest": subject_digest,
            "backend": backend,
            signature_field: external_output,
        }
        if key_id:
            payload["key_id"] = key_id
        if identity:
            payload["identity"] = identity
        if issuer:
            payload["issuer"] = issuer
        return payload
    raise ValueError(f"unsupported signing backend: {backend}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sign a protocol release digest.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--manifest", help="Release manifest JSON path; signs manifest.sbom_hash.")
    source.add_argument("--digest", help="Digest to sign directly.")
    parser.add_argument("--backend", required=True, help=f"Signing backend id, e.g. {FIXTURE_BACKEND} or {EXTERNAL_COMMAND_BACKEND}.")
    parser.add_argument("--key", help="Local signing material reference for fixture signing. Do not commit real keys.")
    parser.add_argument("--key-id", help="Public key identifier to record. Defaults to a fixture-derived id.")
    parser.add_argument("--identity", help="Public signer identity to record for external-command signatures.")
    parser.add_argument("--issuer", help="Public identity issuer to record for external-command signatures.")
    parser.add_argument("--sign-command", help="External signing command. Supports {digest} and {manifest}; otherwise digest is sent on stdin.")
    parser.add_argument(
        "--signature-field",
        default="signature",
        choices=sorted(EXTERNAL_SIGNATURE_FIELDS),
        help="Field used to store external-command stdout in the signature payload.",
    )
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve() if args.manifest else None
    subject_digest = args.digest or digest_from_manifest(manifest_path)
    try:
        payload = build_signature(
            subject_digest,
            backend=args.backend,
            key_reference=args.key,
            key_id=args.key_id,
            sign_command=args.sign_command,
            manifest_path=manifest_path,
            identity=args.identity,
            issuer=args.issuer,
            signature_field=args.signature_field,
        )
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
