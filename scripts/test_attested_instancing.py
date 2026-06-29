#!/usr/bin/env python3
"""Golden checks for attested instance scaffolding."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="ascii")


def assert_ok(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise AssertionError(f"{label} failed: {result.stderr or result.stdout}")


def assert_fails(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly succeeded")


def prepare_empty(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def test_keygen(repo: Path, work: Path) -> None:
    root = work / "keygen"
    prepare_empty(root)
    public = root / "public.json"
    result = run(
        [
            sys.executable,
            str(repo / "scripts" / "keygen_agent.py"),
            "--root",
            str(root),
            "--agent-id",
            "agent-a",
            "--keyid",
            "agent-a:v1",
            "--output",
            str(public),
        ],
        cwd=repo,
    )
    assert_ok(result, "keygen first run")
    data = json.loads(public.read_text(encoding="ascii"))
    if "PRIVATE" in result.stdout or "eventauth" in result.stdout:
        raise AssertionError("keygen leaked secret-bearing paths to stdout")
    for key in ("private_key_file", "hmac_secret_file", "public_key"):
        if key not in data:
            raise AssertionError(f"keygen output missing {key}")
    second = run(
        [
            sys.executable,
            str(repo / "scripts" / "keygen_agent.py"),
            "--root",
            str(root),
            "--agent-id",
            "agent-a",
            "--keyid",
            "agent-a:v1",
        ],
        cwd=repo,
    )
    assert_fails(second, "keygen idempotency")


def test_attested_instance(repo: Path, work: Path) -> None:
    target = work / "instance"
    clone = work / "clone"
    roster = work / "roster.json"
    prepare_empty(work)
    write_json(
        roster,
        {
            "agents": [
                {"id": "agent-a", "role": "architect", "tier": "signer", "llm_preset": "model-a"},
                {"id": "agent-b", "role": "implementer", "tier": "signer", "llm_preset": "model-b"},
                {"id": "agent-c", "role": "reviewer", "tier": "signer", "llm_preset": "model-c"},
                {"id": "agent-worker", "role": "worker", "tier": "worker", "llm_preset": "model-worker"},
            ]
        },
    )
    result = run(
        [
            sys.executable,
            str(repo / "scripts" / "new_instance.py"),
            "--source-template",
            str(repo),
            "--target",
            str(target),
            "--project-name",
            "AttestedCase",
            "--project-goal",
            "Exercise attested ceremony.",
            "--project-description",
            "Disposable golden instance.",
            "--architect",
            "agent-a",
            "--implementer",
            "agent-b",
            "--human-owner",
            "operator",
            "--phase-id",
            "P0",
            "--phase-name",
            "Bootstrap",
            "--phase-goal",
            "Validate generated instance.",
            "--tier",
            "attested",
            "--roster",
            str(roster),
        ],
        cwd=repo,
    )
    assert_ok(result, "attested new_instance")
    config = json.loads((target / "protocol.config.json").read_text(encoding="utf-8"))
    agents = {agent["id"]: agent for agent in config["agent_registry"]["agents"]}
    if agents["agent-worker"]["tier"] != "worker":
        raise AssertionError("worker tier missing")
    if "agent-worker" in config["event_state"]["signature_config"]["public_keys"]:
        raise AssertionError("worker unexpectedly has public signing key")
    if len(config["event_state"]["signature_config"]["public_keys"]) != 3:
        raise AssertionError("expected three signer public keys")
    if json.loads((target / "event-state.runtime.json").read_text(encoding="utf-8"))["event_state"][
        "actor_auth_enforce"
    ]:
        raise AssertionError("actor_auth_enforce must end off by default")
    assert_ok(
        run([sys.executable, str(repo / "scripts" / "validate_collaboration_state.py"), "--root", str(target)], cwd=repo),
        "generated instance validate",
    )
    shutil.copytree(target, clone, ignore=shutil.ignore_patterns("protocol-secrets", ".git"))
    assert_ok(
        run([sys.executable, str(clone / "scripts" / "validate_collaboration_state.py"), "--root", str(clone)], cwd=clone),
        "clone without secrets validate",
    )
    override = json.loads((target / "event-state.runtime.json").read_text(encoding="utf-8"))
    override["event_state"]["actor_auth_enforce"] = True
    write_json(target / "event-state.runtime.json", override)
    negative = {
        "claim": {
            "op": "acquire",
            "claim": {
                "claim_id": "CLAIM-WORKER-NEGATIVE",
                "task_id": "TASK-NONE",
                "owner": "agent-worker",
                "status": "active",
                "scope": ["Area_comun/state/CLAIMS.json"],
                "started_at": "1970-01-01T00:00:01Z",
                "updated_at": "1970-01-01T00:00:01Z",
                "expires_at": "1970-01-02T00:00:01Z",
                "notes": "worker keyless negative proof",
            },
        }
    }
    negative_path = work / "worker-negative.json"
    write_json(negative_path, negative)
    worker_result = run(
        [
            sys.executable,
            str(target / "runtime" / "submit_intent.py"),
            "--root",
            str(target),
            "--actor-id",
            "agent-worker",
            "--timestamp",
            "1970-01-01T00:00:01Z",
            "--commit",
            "negative",
            "--intent",
            str(negative_path),
            "--output",
            "-",
        ],
        cwd=target,
    )
    assert_fails(worker_result, "worker keyless submit")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run attested instancing golden checks.")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--work", default="C:/t/attested-instancing-golden")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    work = Path(args.work).resolve()
    prepare_empty(work)
    try:
        test_keygen(repo, work)
        test_attested_instance(repo, work / "ceremony")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("OK: attested instancing golden checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
