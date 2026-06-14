#!/usr/bin/env python3
"""Verify a release tree against a deterministic protocol release manifest."""

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

from generate_sbom import DEFAULT_EXCLUDE_GLOBS, DEFAULT_INCLUDE_GLOBS, build_sbom, canonical_json
from sign_release import EXTERNAL_COMMAND_BACKEND, FIXTURE_BACKEND, fixture_key_id, read_material, sign_fixture


PRE_LF_NORMALIZATION_PROTOCOL_RELEASES = {
    "1.1.0": {
        "applies_to": "protocol_release",
        "guarantee": "The LF-reproducible checkout guarantee applies to releases v1.2.0 and newer.",
        "note": "v1.1.0 is documented as pre-normalization in dist/v1.1.0/KNOWN_LIMITATIONS.md; verification diffs under clean LF checkout are expected and are not suppressed.",
    }
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def split_command(command: str) -> list[str]:
    parts = shlex.split(command, posix=os.name != "nt")
    if not parts:
        raise ValueError("external verification command is empty")
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
                    raise ValueError(f"external verification command uses unavailable placeholder: {placeholder}")
                updated = updated.replace(placeholder, value)
                used_placeholder = True
        rendered.append(updated)
    return rendered, used_placeholder


def run_external_verify_command(
    command: str,
    *,
    expected_subject_digest: str,
    manifest_path: Path,
    signature_path: Path,
    signature_payload: dict[str, Any],
) -> str | None:
    values = {
        "digest": expected_subject_digest,
        "manifest": manifest_path.as_posix(),
        "signature_file": signature_path.as_posix(),
        "signature": str(signature_payload.get("signature") or ""),
        "bundle": str(signature_payload.get("bundle") or ""),
        "identity": str(signature_payload.get("identity") or ""),
        "issuer": str(signature_payload.get("issuer") or ""),
        "key_id": str(signature_payload.get("key_id") or ""),
    }
    try:
        args, used_placeholder = render_command(command, values)
    except ValueError as exc:
        return str(exc)
    stdin = None if used_placeholder else canonical_json(signature_payload)
    try:
        result = subprocess.run(args, input=stdin, text=True, capture_output=True, check=False)
    except OSError as exc:
        return f"external verification command failed to start: {exc}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        suffix = f": {detail}" if detail else ""
        return f"external verification command failed with exit code {result.returncode}{suffix}"
    return None


def verify_signature(
    signature_path: Path,
    *,
    expected_subject_digest: str,
    manifest_path: Path,
    backend: str | None,
    material_reference: str | None,
    verify_command: str | None,
) -> dict[str, Any]:
    signature_payload = read_json(signature_path)
    actual_backend = str(signature_payload.get("backend") or "")
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
    if actual_subject_digest != expected_subject_digest:
        payload["error"] = "signature subject_digest does not match manifest.sbom_hash"
        return payload
    if actual_backend != selected_backend:
        payload["error"] = "signature backend does not match requested backend"
        return payload
    if selected_backend == FIXTURE_BACKEND:
        if not material_reference:
            payload["error"] = "signature verification requested but no --pubkey/--key material was provided"
            return payload
        material = read_material(material_reference)
        expected_signature = sign_fixture(expected_subject_digest, material)
        expected_key_id = fixture_key_id(material)
        actual_signature = str(signature_payload.get("signature") or "")
        if str(signature_payload.get("key_id") or "") != expected_key_id:
            payload["error"] = "signature key_id does not match verification material"
            return payload
        if not hmac.compare_digest(actual_signature, expected_signature):
            payload["error"] = "signature does not verify for manifest.sbom_hash"
            return payload
        payload["ok"] = True
        return payload
    if selected_backend == EXTERNAL_COMMAND_BACKEND:
        if not verify_command:
            payload["error"] = f"--verify-command is required for backend {EXTERNAL_COMMAND_BACKEND}"
            return payload
        if not str(signature_payload.get("signature") or signature_payload.get("bundle") or ""):
            payload["error"] = "external-command signature has no signature or bundle field"
            return payload
        error = run_external_verify_command(
            verify_command,
            expected_subject_digest=expected_subject_digest,
            manifest_path=manifest_path,
            signature_path=signature_path,
            signature_payload=signature_payload,
        )
        if error:
            payload["error"] = error
            return payload
        payload["ok"] = True
        return payload
    payload["error"] = f"unsupported signature backend: {selected_backend}"
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


def release_scope_note(manifest: dict[str, Any]) -> dict[str, Any] | None:
    version_axes = manifest.get("version_axes") if isinstance(manifest.get("version_axes"), dict) else {}
    protocol_version = str(version_axes.get("protocol") or "")
    note = PRE_LF_NORMALIZATION_PROTOCOL_RELEASES.get(protocol_version)
    if not note:
        return None
    return {"protocol_version": protocol_version, **note}


def verify_release(
    root: Path,
    manifest_path: Path,
    *,
    signature_path: Path | None = None,
    signature_backend: str | None = None,
    signature_material: str | None = None,
    signature_verify_command: str | None = None,
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
    scope_note = release_scope_note(manifest)
    if scope_note is not None:
        payload["release_scope"] = scope_note
    if signature_path is not None or signature_backend is not None or signature_material is not None or signature_verify_command is not None:
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
                manifest_path=manifest_path,
                backend=signature_backend,
                material_reference=signature_material,
                verify_command=signature_verify_command,
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
    parser.add_argument(
        "--verify-command",
        help="External verification command. Supports {digest}, {manifest}, {signature}, {bundle}, {signature_file}, {identity}, {issuer}, {key_id}; otherwise signature JSON is sent on stdin.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = verify_release(
        Path(args.root).resolve(),
        Path(args.manifest).resolve(),
        signature_path=Path(args.signature).resolve() if args.signature else None,
        signature_backend=args.backend,
        signature_material=args.pubkey or args.key,
        signature_verify_command=args.verify_command,
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
