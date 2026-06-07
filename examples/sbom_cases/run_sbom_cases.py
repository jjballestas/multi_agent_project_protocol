#!/usr/bin/env python3
"""Golden cases for deterministic protocol SBOM generation."""

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
SBOM_PY = ROOT / "scripts" / "generate_sbom.py"
SBOM_PS = ROOT / "scripts" / "generate_sbom.ps1"
COMMIT = "abc123"
TIMESTAMP = "2026-06-07T00:00:00Z"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


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
    write(root / "runtime/runs/RUN-001.jsonl", "{}\n")
    write(root / ".git/config", "excluded\n")
    write(root / "scripts/__pycache__/tool.pyc", "excluded\n")
    write(root / "personal/Codex/note.md", "excluded\n")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def generate_py(root: Path, output: str = "-") -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(SBOM_PY), "--root", str(root), "--commit", COMMIT, "--timestamp", TIMESTAMP, "--output", output])


def generate_ps(root: Path) -> subprocess.CompletedProcess[str] | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    return run([shell, "-NoProfile", "-File", str(SBOM_PS), "-Root", str(root), "-Commit", COMMIT, "-Timestamp", TIMESTAMP])


def load_sbom(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def paths(sbom: dict[str, Any]) -> list[str]:
    return [entry["path"] for entry in sbom["files"]]


def file_entry(sbom: dict[str, Any], path: str) -> dict[str, Any]:
    for entry in sbom["files"]:
        if entry["path"] == path:
            return entry
    raise AssertionError(f"missing path {path}")


def assert_base_sbom(sbom: dict[str, Any]) -> None:
    listed = paths(sbom)
    assert sbom["schema_version"] == "protocol_sbom.v1"
    assert sbom["commit"] == COMMIT
    assert sbom["timestamp"] == TIMESTAMP
    assert sbom["version_axes"]["protocol"] == "9.8.7"
    assert sbom["version_axes"]["runtime"] == "6.5.4"
    assert sbom["version_axes"]["schema"]["turn_schema"] == "1.2.3"
    assert sbom["version_axes"]["profiles"] == [{"profile_id": "demo", "profile_version": "0.3.0"}]
    assert listed == sorted(listed), listed
    assert "scripts/tool.py" in listed
    assert "runtime/source.py" in listed
    assert "Area_comun/protocol/GUIDE.md" in listed
    assert "runtime/state/snapshot.json" not in listed
    assert "runtime/runs/RUN-001.jsonl" not in listed
    assert ".git/config" not in listed
    assert "scripts/__pycache__/tool.pyc" not in listed
    assert "personal/Codex/note.md" not in listed
    entry = file_entry(sbom, "scripts/tool.py")
    assert entry["sha256"] == sha256_text("print('hello')\n")
    assert entry["size"] == len("print('hello')\n".encode("utf-8"))


def case_canonical_expected_tree() -> None:
    with tempfile.TemporaryDirectory(prefix="sbom-case-") as temp:
        root = Path(temp)
        build_fixture(root)
        result = generate_py(root)
        sbom = load_sbom(result)
        assert_base_sbom(sbom)


def case_deterministic_and_output_file() -> None:
    with tempfile.TemporaryDirectory(prefix="sbom-case-det-") as temp:
        root = Path(temp)
        build_fixture(root)
        first = generate_py(root)
        second = generate_py(root)
        assert first.returncode == 0, first.stderr
        assert second.returncode == 0, second.stderr
        assert first.stdout == second.stdout
        output = root / "out/sbom.json"
        written = generate_py(root, str(output))
        assert written.returncode == 0, written.stdout + written.stderr
        assert output.read_bytes() == first.stdout.encode("utf-8")


def case_file_change_updates_hash() -> None:
    with tempfile.TemporaryDirectory(prefix="sbom-case-change-") as temp:
        root = Path(temp)
        build_fixture(root)
        before = load_sbom(generate_py(root))
        write(root / "scripts/tool.py", "print('changed')\n")
        after = load_sbom(generate_py(root))
        assert file_entry(before, "scripts/tool.py")["sha256"] != file_entry(after, "scripts/tool.py")["sha256"]
        assert file_entry(after, "scripts/tool.py")["sha256"] == sha256_text("print('changed')\n")


def case_powershell_wrapper_parity_if_available() -> None:
    with tempfile.TemporaryDirectory(prefix="sbom-case-ps-") as temp:
        root = Path(temp)
        build_fixture(root)
        py = generate_py(root)
        ps = generate_ps(root)
        if ps is None:
            return
        assert py.returncode == 0, py.stderr
        assert ps.returncode == 0, ps.stdout + ps.stderr
        assert py.stdout.replace("\r\n", "\n") == ps.stdout.replace("\r\n", "\n")


def main() -> int:
    cases = [
        case_canonical_expected_tree,
        case_deterministic_and_output_file,
        case_file_change_updates_hash,
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
    print(f"OK: {len(cases)} SBOM golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
