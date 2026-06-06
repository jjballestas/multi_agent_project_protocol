#!/usr/bin/env python3
"""Golden cases for the handoff-release validator rule."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_collaboration_state.py"
MINIMAL = ROOT / "examples" / "minimal_instance"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(VALIDATOR), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def set_claim_status(root: Path, status: str) -> None:
    claims_path = root / "Area_comun" / "state" / "CLAIMS.json"
    claims = load_json(claims_path)
    claims["claims"][0]["status"] = status
    write_json(claims_path, claims)


def assert_case(name: str, claim_status: str, expected: int) -> None:
    with tempfile.TemporaryDirectory(prefix=f"handoff-{name}-") as temp:
        fixture = Path(temp)
        shutil.copytree(MINIMAL, fixture, dirs_exist_ok=True)
        set_claim_status(fixture, claim_status)
        result = run_validator(fixture)
        if result.returncode != expected:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError(f"{name}: expected exit {expected}, got {result.returncode}")


def main() -> int:
    assert_case("released_done", "released", 0)
    assert_case("active_done", "active", 1)
    print("OK: handoff-release cases passed (2).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
