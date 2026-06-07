#!/usr/bin/env python3
"""Verify a release tree against a deterministic protocol release manifest."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path
from typing import Any

from generate_sbom import DEFAULT_EXCLUDE_GLOBS, DEFAULT_INCLUDE_GLOBS, build_sbom, canonical_json
from sign_release import FIXTURE_BACKEND, fixture_key_id, read_material, sign_fixture


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def verify_signature(
    signature_path: Path,
    *,
    expected_subject_digest: str,
    backend: str | None,
    material_reference: str | None,
) -> dict[str, Any]:
    signature_payload = read_json(signature_path)
    selected_backend = backend or str(signature_payload.get("backend") or "")
    actual_subject_digest = str(signature_payload.get("subject_digest") or "")
    payload: dict[str, Any] = {
        "requested": True,
        "ok": False,
        "signature": signature_path.as_posix(),
        "backend": selected_backend,
        "expected_subject_digest": expected_subject_digest,
        "actual_subject_digest": actual_subject_digest,
        "key_id": str(signature_payload.get("key_id") or ""),
    }
    if not material_reference:
        payload["error"] = "signature verification requested but no --pubkey/--key material was provided"
        return payload
    if selected_backend != FIXTURE_BACKEND:
        payload["error"] = f"unsupported signature backend: {selected_backend}"
        return payload
    material = read_material(material_reference)
    expected_signature = sign_fixture(expected_subject_digest, material)
    expected_key_id = fixture_key_id(material)
    actual_signature = str(signature_payload.get("signature") or "")
    if actual_subject_digest != expected_subject_digest:
        payload["error"] = "signature subject_digest does not match manifest.sbom_hash"
        return payload
    if str(signature_payload.get("backend") or "") != selected_backend:
        payload["error"] = "signature backend does not match requested backend"
        return payload
    if str(signature_payload.get("key_id") or "") != expected_key_id:
        payload["error"] = "signature key_id does not match verification material"
        return payload
    if not hmac.compare_digest(actual_signature, expected_signature):
        payload["error"] = "signature does not verify for manifest.sbom_hash"
        return payload
    payload["ok"] = True
    return payload


def sbom_globs(manifest: dict[str, Any]) -> tuple[list[str], list[str]]:
    sbom = manifest.get("sbom") if isinstance(manifest.get("sbom"), dict) else {}
    source_globs = sbom.get("source_globs") if isinstance(sbom.get("source_globs"), dict) else {}
    include = source_globs.get("include")
    exclude = source_globs.get("exclude")
    return (
        [str(item) for item in include] if isinstance(include, list) else list(DEFAULT_INCLUDE_GLOBS),
        [str(item) for item in exclude] if isinstance(exclude, list) else list(DEFAULT_EXCLUDE_GLOBS),
    )


def file_map(sbom: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in sbom.get("files") or []:
        if isinstance(entry, dict) and str(entry.get("path") or "").strip():
            result[str(entry["path"])] = entry
    return result


def diff_sboms(expected: dict[str, Any], actual: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    expected_files = file_map(expected)
    actual_files = file_map(actual)
    missing = [{"path": path, **expected_files[path]} for path in sorted(set(expected_files) - set(actual_files))]
    extra = [{"path": path, **actual_files[path]} for path in sorted(set(actual_files) - set(expected_files))]
    changed: list[dict[str, Any]] = []
    for path in sorted(set(expected_files) & set(actual_files)):
        expected_entry = expected_files[path]
        actual_entry = actual_files[path]
        if expected_entry.get("sha256") != actual_entry.get("sha256") or expected_entry.get("size") != actual_entry.get("size"):
            changed.append(
                {
                    "path": path,
                    "expected_sha256": expected_entry.get("sha256"),
                    "actual_sha256": actual_entry.get("sha256"),
                    "expected_size": expected_entry.get("size"),
                    "actual_size": actual_entry.get("size"),
                }
            )
    return {"changed": changed, "missing": missing, "extra": extra}


def verify_release(
    root: Path,
    manifest_path: Path,
    *,
    signature_path: Path | None = None,
    signature_backend: str | None = None,
    signature_material: str | None = None,
) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    include_globs, exclude_globs = sbom_globs(manifest)
    actual_sbom = build_sbom(
        root,
        commit=str(manifest.get("commit") or ""),
        timestamp=str(manifest.get("timestamp") or ""),
        include_globs=include_globs,
        exclude_globs=exclude_globs,
    )
    actual_hash = sha256_text(canonical_json(actual_sbom))
    expected_hash = str(manifest.get("sbom_hash") or "")
    expected_sbom = manifest.get("sbom") if isinstance(manifest.get("sbom"), dict) else {}
    diffs = diff_sboms(expected_sbom, actual_sbom)
    ok = actual_hash == expected_hash
    payload: dict[str, Any] = {
        "schema_version": "protocol_release_verify.v1",
        "ok": ok,
        "manifest": manifest_path.as_posix(),
        "root": root.as_posix(),
        "expected_sbom_hash": expected_hash,
        "actual_sbom_hash": actual_hash,
        "file_count": actual_sbom["file_count"],
        "diff": diffs,
    }
    if signature_path is not None or signature_backend is not None or signature_material is not None:
        if signature_path is None:
            payload["ok"] = False
            payload["signature"] = {
                "requested": True,
                "ok": False,
                "error": "signature verification requested but no --signature path was provided",
            }
        else:
            signature_result = verify_signature(
                signature_path,
                expected_subject_digest=expected_hash,
                backend=signature_backend,
                material_reference=signature_material,
            )
            payload["signature"] = signature_result
            payload["ok"] = ok and bool(signature_result["ok"])
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a protocol release tree against a manifest.")
    parser.add_argument("--root", default=".", help="Release tree root to verify.")
    parser.add_argument("--manifest", required=True, help="Manifest JSON path.")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    parser.add_argument("--signature", help="Optional release signature JSON path to verify.")
    parser.add_argument("--backend", help="Signature backend id. Defaults to the backend recorded in the signature.")
    parser.add_argument("--pubkey", help="Public verification material reference for signature verification.")
    parser.add_argument("--key", help="Verification material reference; accepted for fixture HMAC parity.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = verify_release(
        Path(args.root).resolve(),
        Path(args.manifest).resolve(),
        signature_path=Path(args.signature).resolve() if args.signature else None,
        signature_backend=args.backend,
        signature_material=args.pubkey or args.key,
    )
    rendered = canonical_json(payload)
    if args.output == "-":
        sys.stdout.buffer.write(rendered.encode("utf-8"))
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(rendered.encode("utf-8"))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
