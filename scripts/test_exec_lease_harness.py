#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sweep_cron_zombies as sweep


ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTER = "Co" + "dex"
REVIEWER = "Ana" + "lista"
CHECKER = "Arqui" + "tecto"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def base_lease(**overrides: object) -> dict:
    data = {
        "owner": IMPLEMENTER,
        "task_or_msg_id": "MSG-test",
        "pid": 999999,
        "process_start_time_utc": "2000-01-01T00:00:00Z",
        "cmdline_hash": sweep.hash_cmdline("agent exec"),
        "cmdline": "agent exec",
        "started_at": "2000-01-01T00:00:00Z",
        "deadline": (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat(),
        "heartbeat_monotonic": 1,
        "shutdown_policy": "stop_after_current_turn",
    }
    data.update(overrides)
    return data


def make_root() -> tempfile.TemporaryDirectory[str]:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "Area_comun/state").mkdir(parents=True)
    write_json(root / "Area_comun/state/CLAIMS.json", {"claims": [], "schema_version": "1.0"})
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    return tmp


def test_dead_process_cleans_only() -> None:
    with make_root() as tmp:
        root = Path(tmp)
        lease_path = root / ".protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.exec-lease.json"
        write_json(lease_path, base_lease())
        decision = sweep.decision_for_lease(root, lease_path, IMPLEMENTER, CHECKER)
        assert decision["action"] == "cleanup_only"
        assert decision["reason"] == "process_dead"


def test_owner_and_checker_exclusions() -> None:
    with make_root() as tmp:
        root = Path(tmp)
        lease_path = root / ".protocol-tmp/analista_mailbox_cron/analista_mailbox_cron.exec-lease.json"
        write_json(lease_path, base_lease(owner=REVIEWER))
        assert sweep.decision_for_lease(root, lease_path, IMPLEMENTER, CHECKER)["reason"] == "owner_not_target"
        assert sweep.decision_for_lease(root, lease_path, REVIEWER, REVIEWER)["reason"] == "checker_owner_excluded"


def test_dry_run_is_default() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/sweep_cron_zombies.py"), "--root", str(ROOT), "--owner", IMPLEMENTER],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["mode"] == "dry-run"


def test_harnesses_contain_required_exec_lease_contract() -> None:
    for rel in (f"personal/{IMPLEMENTER}/codex_mailbox_cron.ps1", f"personal/{REVIEWER}/analista_mailbox_cron.ps1"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "exec-lease.json" in text
        assert "process_start_time_utc" in text
        assert "cmdline_hash" in text
        assert "heartbeat_monotonic" in text
        assert "Clear-StaleCronLockIfSafe" in text
        assert "Stop marker detected; waiting for current exec" in text
        assert "Stop-ExpiredLeaseProcess" in text
        assert "finally" in text


def main() -> int:
    tests = [
        test_dead_process_cleans_only,
        test_owner_and_checker_exclusions,
        test_dry_run_is_default,
        test_harnesses_contain_required_exec_lease_contract,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
