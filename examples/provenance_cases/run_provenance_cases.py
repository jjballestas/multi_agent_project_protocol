#!/usr/bin/env python3
"""Golden cases for release provenance generation and verification."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PY = ROOT / "scripts" / "generate_manifest.py"
PROVENANCE_PY = ROOT / "scripts" / "generate_provenance.py"
PROVENANCE_PS = ROOT / "scripts" / "generate_provenance.ps1"
COMMIT = "def456"
TIMESTAMP = "2026-06-07T00:00:00Z"
PROVENANCE_TIMESTAMP = "2026-06-07T00:01:00Z"
BUILDER_ID = "Codex"
INVOCATION_PROCESS = "scripts/generate_manifest.py --root ."


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write(path, canonical_json(payload))


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def generate_provenance(manifest: Path, output: str = "-") -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            str(PROVENANCE_PY),
            "--manifest",
            str(manifest),
            "--builder-id",
            BUILDER_ID,
            "--commit",
            COMMIT,
            "--process",
            INVOCATION_PROCESS,
            "--timestamp",
            PROVENANCE_TIMESTAMP,
            "--output",
            output,
        ]
    )


def verify_provenance(manifest: Path, provenance: Path) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(PROVENANCE_PY), "--verify", "--manifest", str(manifest), "--provenance", str(provenance)])


def generate_provenance_ps(manifest: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run(
        [
            shell,
            "-NoProfile",
            "-File",
            str(PROVENANCE_PS),
            "-Manifest",
            str(manifest),
            "-BuilderId",
            BUILDER_ID,
            "-Commit",
            COMMIT,
            "-InvocationProcess",
            INVOCATION_PROCESS,
            "-Timestamp",
            PROVENANCE_TIMESTAMP,
        ]
    )


def verify_provenance_ps(manifest: Path, provenance: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run([shell, "-NoProfile", "-File", str(PROVENANCE_PS), "-Verify", "-Manifest", str(manifest), "-Provenance", str(provenance)])


def load_json_result(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def write_manifest(root: Path) -> Path:
    output = root / "out/manifest.json"
    result = generate_manifest(root, str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    return output


def write_provenance(manifest: Path) -> Path:
    output = manifest.parent / "provenance.json"
    result = generate_provenance(manifest, str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    return output


def expected_provenance(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "protocol_provenance.v1",
        "generated_by": "scripts/generate_provenance.py",
        "subject": {
            "name": "multi_agent_project_protocol@9.8.7",
            "digest": {"sha256": manifest["sbom_hash"]},
        },
        "builder": {"id": BUILDER_ID},
        "invocation": {"commit": COMMIT, "process": INVOCATION_PROCESS},
        "metadata": {"schema": "provenance.v1", "timestamp": PROVENANCE_TIMESTAMP},
    }


def case_provenance_expected_payload() -> None:
    with tempfile.TemporaryDirectory(prefix="provenance-expected-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        result = generate_provenance(manifest_path)
        payload = load_json_result(result)
        expected = expected_provenance(manifest)
        assert payload == expected
        assert result.stdout == canonical_json(expected)
        assert payload["subject"]["digest"]["sha256"] == sha256_text(canonical_json(manifest["sbom"]))


def case_deterministic_provenance_bytes() -> None:
    with tempfile.TemporaryDirectory(prefix="provenance-deterministic-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        first = generate_provenance(manifest_path)
        second = generate_provenance(manifest_path)
        assert first.returncode == 0, first.stderr
        assert second.returncode == 0, second.stderr
        assert first.stdout == second.stdout


def case_verify_ok_for_matching_digest() -> None:
    with tempfile.TemporaryDirectory(prefix="provenance-verify-ok-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        provenance_path = write_provenance(manifest_path)
        result = verify_provenance(manifest_path, provenance_path)
        payload = load_json_result(result)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert payload["ok"] is True
        assert payload["expected_sbom_hash"] == manifest["sbom_hash"]
        assert payload["actual_subject_digest"] == manifest["sbom_hash"]


def case_verify_fails_for_digest_mismatch() -> None:
    with tempfile.TemporaryDirectory(prefix="provenance-verify-fail-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        provenance_path = write_provenance(manifest_path)
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        provenance["subject"]["digest"]["sha256"] = "0" * 64
        write_json(provenance_path, provenance)
        result = verify_provenance(manifest_path, provenance_path)
        assert result.returncode != 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert payload["actual_subject_digest"] == "0" * 64
        assert payload["error"] == "subject.digest.sha256 does not match manifest.sbom_hash"


def case_powershell_wrapper_parity_if_available() -> None:
    with tempfile.TemporaryDirectory(prefix="provenance-ps-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        py_provenance = generate_provenance(manifest_path)
        ps_provenance = generate_provenance_ps(manifest_path)
        if ps_provenance is None:
            return
        assert py_provenance.returncode == 0, py_provenance.stderr
        assert ps_provenance.returncode == 0, ps_provenance.stdout + ps_provenance.stderr
        assert py_provenance.stdout.replace("\r\n", "\n") == ps_provenance.stdout.replace("\r\n", "\n")
        provenance_path = write_provenance(manifest_path)
        py_verify = verify_provenance(manifest_path, provenance_path)
        ps_verify = verify_provenance_ps(manifest_path, provenance_path)
        assert ps_verify is not None
        assert py_verify.returncode == ps_verify.returncode == 0
        assert py_verify.stdout.replace("\r\n", "\n") == ps_verify.stdout.replace("\r\n", "\n")


def main() -> int:
    cases = [
        case_provenance_expected_payload,
        case_deterministic_provenance_bytes,
        case_verify_ok_for_matching_digest,
        case_verify_fails_for_digest_mismatch,
        case_powershell_wrapper_parity_if_available,
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
    print(f"OK: {len(cases)} provenance golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
