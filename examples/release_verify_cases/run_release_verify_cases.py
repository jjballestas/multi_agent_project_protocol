#!/usr/bin/env python3
"""Golden cases for release manifest generation and verification."""

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
VERIFY_PY = ROOT / "scripts" / "verify_release.py"
MANIFEST_PS = ROOT / "scripts" / "generate_manifest.ps1"
VERIFY_PS = ROOT / "scripts" / "verify_release.ps1"
COMMIT = "def456"
TIMESTAMP = "2026-06-07T00:00:00Z"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


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


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(["git", "-C", str(root), *args])


def generate_manifest(root: Path, output: str = "-") -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(MANIFEST_PY), "--root", str(root), "--commit", COMMIT, "--timestamp", TIMESTAMP, "--output", output])


def verify_release(root: Path, manifest: Path) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(VERIFY_PY), "--root", str(root), "--manifest", str(manifest)])


def generate_manifest_ps(root: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run([shell, "-NoProfile", "-File", str(MANIFEST_PS), "-Root", str(root), "-Commit", COMMIT, "-Timestamp", TIMESTAMP])


def verify_release_ps(root: Path, manifest: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run([shell, "-NoProfile", "-File", str(VERIFY_PS), "-Root", str(root), "-Manifest", str(manifest)])


def load_json_result(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def write_manifest(root: Path) -> Path:
    output = root / "out/manifest.json"
    result = generate_manifest(root, str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    return output


def assert_base_manifest(manifest: dict[str, Any]) -> None:
    assert manifest["schema_version"] == "protocol_release_manifest.v1"
    assert manifest["commit"] == COMMIT
    assert manifest["timestamp"] == TIMESTAMP
    assert manifest["version_axes"]["protocol"] == "9.8.7"
    assert manifest["version_axes"]["runtime"] == "6.5.4"
    assert manifest["version_axes"]["schema"]["turn_schema"] == "1.2.3"
    assert manifest["file_count"] == len(manifest["sbom"]["files"])
    assert manifest["sbom_hash"] == sha256_text(canonical_json(manifest["sbom"]))
    without_hash = dict(manifest)
    manifest_hash = without_hash.pop("manifest_hash")
    assert manifest_hash == sha256_text(canonical_json(without_hash))
    paths = [entry["path"] for entry in manifest["sbom"]["files"]]
    assert paths == sorted(paths)
    assert "scripts/tool.py" in paths
    assert "runtime/state/snapshot.json" not in paths
    assert ".git/config" not in paths
    assert "personal/Codex/note.md" not in paths


def case_manifest_expected_tree() -> None:
    with tempfile.TemporaryDirectory(prefix="manifest-case-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest = load_json_result(generate_manifest(root))
        assert_base_manifest(manifest)


def case_verify_ok_for_matching_tree() -> None:
    with tempfile.TemporaryDirectory(prefix="manifest-verify-ok-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        result = verify_release(root, manifest_path)
        payload = load_json_result(result)
        assert payload["ok"] is True
        assert payload["diff"] == {"changed": [], "missing": [], "extra": []}


def case_verify_fails_for_changed_file() -> None:
    with tempfile.TemporaryDirectory(prefix="manifest-verify-change-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        write(root / "scripts/tool.py", "print('changed')\n")
        result = verify_release(root, manifest_path)
        assert result.returncode != 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert [entry["path"] for entry in payload["diff"]["changed"]] == ["scripts/tool.py"]


def case_verify_detects_missing_and_extra_files() -> None:
    with tempfile.TemporaryDirectory(prefix="manifest-verify-shape-") as temp:
        root = Path(temp)
        build_fixture(root)
        manifest_path = write_manifest(root)
        (root / "scripts/tool.py").unlink()
        write(root / "scripts/new_tool.py", "print('new')\n")
        result = verify_release(root, manifest_path)
        assert result.returncode != 0
        payload = json.loads(result.stdout)
        assert [entry["path"] for entry in payload["diff"]["missing"]] == ["scripts/tool.py"]
        assert [entry["path"] for entry in payload["diff"]["extra"]] == ["scripts/new_tool.py"]


def case_deterministic_manifest_bytes() -> None:
    with tempfile.TemporaryDirectory(prefix="manifest-deterministic-") as temp:
        root = Path(temp)
        build_fixture(root)
        first = generate_manifest(root)
        second = generate_manifest(root)
        assert first.returncode == 0, first.stderr
        assert second.returncode == 0, second.stderr
        assert first.stdout == second.stdout


def case_powershell_wrappers_parity_if_available() -> None:
    with tempfile.TemporaryDirectory(prefix="manifest-ps-") as temp:
        root = Path(temp)
        build_fixture(root)
        py_manifest = generate_manifest(root)
        ps_manifest = generate_manifest_ps(root)
        if ps_manifest is None:
            return
        assert py_manifest.returncode == 0, py_manifest.stderr
        assert ps_manifest.returncode == 0, ps_manifest.stdout + ps_manifest.stderr
        assert py_manifest.stdout.replace("\r\n", "\n") == ps_manifest.stdout.replace("\r\n", "\n")
        manifest_path = write_manifest(root)
        py_verify = verify_release(root, manifest_path)
        ps_verify = verify_release_ps(root, manifest_path)
        assert ps_verify is not None
        assert py_verify.returncode == ps_verify.returncode == 0
        assert py_verify.stdout.replace("\r\n", "\n") == ps_verify.stdout.replace("\r\n", "\n")


def case_future_release_checkout_lf_with_autocrlf() -> None:
    if not shutil.which("git"):
        return
    with tempfile.TemporaryDirectory(prefix="manifest-future-lf-") as temp:
        root = Path(temp)
        build_fixture(root)
        write(root / ".gitattributes", "* text=auto eol=lf\n")
        manifest_path = write_manifest(root)

        shutil.rmtree(root / ".git")
        assert run_git(root, "init").returncode == 0
        assert run_git(root, "config", "user.email", "release@example.invalid").returncode == 0
        assert run_git(root, "config", "user.name", "Release Verify Case").returncode == 0
        assert run_git(root, "config", "core.autocrlf", "true").returncode == 0
        assert run_git(root, "add", ".").returncode == 0
        assert run_git(root, "commit", "-m", "fixture").returncode == 0

        for path in [
            root / "scripts/tool.py",
            root / "runtime/source.py",
            root / "Area_comun/protocol/GUIDE.md",
            root / "examples/demo_case/input.txt",
        ]:
            path.unlink()
        assert run_git(root, "checkout", "--", ".").returncode == 0

        for path in [
            root / "scripts/tool.py",
            root / "runtime/source.py",
            root / "Area_comun/protocol/GUIDE.md",
            root / "examples/demo_case/input.txt",
        ]:
            assert b"\r\n" not in path.read_bytes(), path.as_posix()

        payload = load_json_result(verify_release(root, manifest_path))
        assert payload["ok"] is True
        assert payload["diff"] == {"changed": [], "missing": [], "extra": []}


def main() -> int:
    cases = [
        case_manifest_expected_tree,
        case_verify_ok_for_matching_tree,
        case_verify_fails_for_changed_file,
        case_verify_detects_missing_and_extra_files,
        case_deterministic_manifest_bytes,
        case_powershell_wrappers_parity_if_available,
        case_future_release_checkout_lf_with_autocrlf,
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
    print(f"OK: {len(cases)} release verify golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
