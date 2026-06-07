#!/usr/bin/env python3
"""Golden cases for release signing and signature verification."""

from __future__ import annotations

import hashlib
import hmac
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PY = ROOT / "scripts" / "generate_manifest.py"
SIGN_PY = ROOT / "scripts" / "sign_release.py"
VERIFY_PY = ROOT / "scripts" / "verify_release.py"
SIGN_PS = ROOT / "scripts" / "sign_release.ps1"
VERIFY_PS = ROOT / "scripts" / "verify_release.ps1"
COMMIT = "def456"
TIMESTAMP = "2026-06-07T00:00:00Z"
FIXTURE_BACKEND = "fixture-hmac-sha256"
FIXTURE_MATERIAL = "fixture-public-test-material-release-sign-cases"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write(path, canonical_json(payload))


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def fixture_key_id() -> str:
    return "fixture:" + hashlib.sha256(FIXTURE_MATERIAL.encode("utf-8")).hexdigest()[:16]


def fixture_signature(subject_digest: str) -> str:
    return hmac.new(FIXTURE_MATERIAL.encode("utf-8"), subject_digest.encode("utf-8"), hashlib.sha256).hexdigest()


def build_fixture(root: Path) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "protocol_version": "9.8.7",
            "runtime_version": "6.5.4",
        },
    )
    write_json(root / "runtime/turn_schema.json", {"schema_version": "1.2.3"})
    write_json(
        root / "profiles/demo/profile.manifest.json",
        {"schema_version": "1.0", "profile_id": "demo", "profile_version": "0.3.0"},
    )
    write(root / "scripts/tool.py", "print('hello')\n")
    write(root / "runtime/source.py", "# runtime source\n")
    write(root / "Area_comun/protocol/GUIDE.md", "# Guide\n")
    write(root / "examples/demo_case/input.txt", "fixture\n")
    write(root / "runtime/state/snapshot.json", '{"state":"excluded"}\n')
    write(root / ".git/config", "excluded\n")
    write(root / "personal/Codex/note.md", "excluded\n")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def generate_manifest(root: Path, output: str = "-") -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(MANIFEST_PY), "--root", str(root), "--commit", COMMIT, "--timestamp", TIMESTAMP, "--output", output])


def sign_release(manifest: Path, key_file: Path, output: str = "-") -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            str(SIGN_PY),
            "--manifest",
            str(manifest),
            "--backend",
            FIXTURE_BACKEND,
            "--key",
            str(key_file),
            "--output",
            output,
        ]
    )


def sign_digest(digest: str, key_file: Path, output: str = "-") -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            str(SIGN_PY),
            "--digest",
            digest,
            "--backend",
            FIXTURE_BACKEND,
            "--key",
            str(key_file),
            "--output",
            output,
        ]
    )


def verify_release(root: Path, manifest: Path, signature: Path | None = None, key_file: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(VERIFY_PY), "--root", str(root), "--manifest", str(manifest)]
    if signature is not None:
        command += ["--signature", str(signature)]
    if key_file is not None:
        command += ["--pubkey", str(key_file)]
    return run(command)


def sign_release_ps(manifest: Path, key_file: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run(
        [
            shell,
            "-NoProfile",
            "-File",
            str(SIGN_PS),
            "-Manifest",
            str(manifest),
            "-Backend",
            FIXTURE_BACKEND,
            "-Key",
            str(key_file),
        ]
    )


def verify_release_ps(root: Path, manifest: Path, signature: Path, key_file: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run(
        [
            shell,
            "-NoProfile",
            "-File",
            str(VERIFY_PS),
            "-Root",
            str(root),
            "-Manifest",
            str(manifest),
            "-Signature",
            str(signature),
            "-Pubkey",
            str(key_file),
        ]
    )


def load_json_result(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def write_manifest(root: Path) -> Path:
    output = root / "out/manifest.json"
    result = generate_manifest(root, str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    return output


def write_key(root: Path) -> Path:
    key_file = root / "fixture_material.txt"
    write(key_file, FIXTURE_MATERIAL + "\n")
    return key_file


def write_signature(manifest: Path, key_file: Path) -> Path:
    output = manifest.parent / "signature.json"
    result = sign_release(manifest, key_file, str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    return output


def expected_signature(manifest: dict[str, Any]) -> dict[str, Any]:
    subject_digest = manifest["sbom_hash"]
    return {
        "schema_version": "protocol_release_signature.v1",
        "generated_by": "scripts/sign_release.py",
        "subject_digest": subject_digest,
        "backend": FIXTURE_BACKEND,
        "key_id": fixture_key_id(),
        "signature": fixture_signature(subject_digest),
    }


def case_signature_expected_payload() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-expected-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        result = sign_release(manifest_path, key_file)
        payload = load_json_result(result)
        expected = expected_signature(manifest)
        assert payload == expected
        assert result.stdout == canonical_json(expected)


def case_signature_deterministic_bytes() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-deterministic-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        first = sign_release(manifest_path, key_file)
        second = sign_release(manifest_path, key_file)
        assert first.returncode == 0, first.stderr
        assert second.returncode == 0, second.stderr
        assert first.stdout == second.stdout


def case_verify_signature_ok() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-ok-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        signature_path = write_signature(manifest_path, key_file)
        result = verify_release(root, manifest_path, signature_path, key_file)
        payload = load_json_result(result)
        assert payload["ok"] is True
        assert payload["signature"]["ok"] is True
        assert payload["signature"]["actual_subject_digest"] == payload["expected_sbom_hash"]


def case_verify_signature_fails_for_subject_mismatch() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-subject-fail-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        signature_path = manifest_path.parent / "signature.json"
        result = sign_digest("0" * 64, key_file, str(signature_path))
        assert result.returncode == 0, result.stdout + result.stderr
        verify = verify_release(root, manifest_path, signature_path, key_file)
        assert verify.returncode != 0
        payload = json.loads(verify.stdout)
        assert payload["ok"] is False
        assert payload["signature"]["ok"] is False
        assert payload["signature"]["error"] == "signature subject_digest does not match manifest.sbom_hash"


def case_verify_signature_fails_for_altered_signature() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-altered-fail-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        signature_path = write_signature(manifest_path, key_file)
        signature = json.loads(signature_path.read_text(encoding="utf-8"))
        signature["signature"] = "0" * 64
        write_json(signature_path, signature)
        verify = verify_release(root, manifest_path, signature_path, key_file)
        assert verify.returncode != 0
        payload = json.loads(verify.stdout)
        assert payload["ok"] is False
        assert payload["signature"]["error"] == "signature does not verify for manifest.sbom_hash"


def case_verify_without_signature_keeps_integrity_contract() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-off-by-default-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        result = verify_release(root, manifest_path)
        payload = load_json_result(result)
        assert payload["ok"] is True
        assert "signature" not in payload


def case_verify_fails_closed_without_material() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-no-material-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        signature_path = write_signature(manifest_path, key_file)
        result = verify_release(root, manifest_path, signature_path, None)
        assert result.returncode != 0
        payload = json.loads(result.stdout)
        assert payload["signature"]["error"] == "signature verification requested but no --pubkey/--key material was provided"


def case_powershell_wrappers_parity_if_available() -> None:
    with tempfile.TemporaryDirectory(prefix="release-sign-ps-") as temp:
        root = Path(temp)
        build_fixture(root)
        key_file = write_key(root)
        manifest_path = write_manifest(root)
        py_signature = sign_release(manifest_path, key_file)
        ps_signature = sign_release_ps(manifest_path, key_file)
        if ps_signature is None:
            return
        assert py_signature.returncode == 0, py_signature.stderr
        assert ps_signature.returncode == 0, ps_signature.stdout + ps_signature.stderr
        assert py_signature.stdout.replace("\r\n", "\n") == ps_signature.stdout.replace("\r\n", "\n")
        signature_path = write_signature(manifest_path, key_file)
        py_verify = verify_release(root, manifest_path, signature_path, key_file)
        ps_verify = verify_release_ps(root, manifest_path, signature_path, key_file)
        assert ps_verify is not None
        assert py_verify.returncode == ps_verify.returncode == 0
        assert py_verify.stdout.replace("\r\n", "\n") == ps_verify.stdout.replace("\r\n", "\n")


def main() -> int:
    cases = [
        case_signature_expected_payload,
        case_signature_deterministic_bytes,
        case_verify_signature_ok,
        case_verify_signature_fails_for_subject_mismatch,
        case_verify_signature_fails_for_altered_signature,
        case_verify_without_signature_keeps_integrity_contract,
        case_verify_fails_closed_without_material,
        case_powershell_wrappers_parity_if_available,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} release signature golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
