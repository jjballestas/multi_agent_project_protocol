#!/usr/bin/env python3
"""Safe cron exec-lease sweeper.

Dry-run is the default. A kill requires --kill, an expired lease, PID plus
process start-time match, target-owner match, no deny-listed command, and no
dirty claimed route for that owner.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DENY_CMD_TOKENS = (
    "submit_intent",
    "git",
    "npm test",
    "vitest",
    "node --test",
    "validate_collaboration_state.py",
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def run(args: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=root, text=True, capture_output=True, check=False)


def process_info(pid: int) -> dict[str, str] | None:
    script = (
        "$p=Get-CimInstance Win32_Process -Filter \"ProcessId=%d\";"
        "if($p){[ordered]@{pid=$p.ProcessId;cmdline=$p.CommandLine;"
        "creation=([System.Management.ManagementDateTimeConverter]::ToDateTime($p.CreationDate)."
        "ToUniversalTime().ToString('o'))}|ConvertTo-Json -Compress}"
    ) % pid
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    doc = json.loads(proc.stdout)
    return {
        "pid": str(doc.get("pid")),
        "cmdline": str(doc.get("cmdline") or ""),
        "process_start_time_utc": str(doc.get("creation") or "").replace("+00:00", "Z"),
    }


def hash_cmdline(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def active_claims_for_owner(root: Path, owner: str) -> list[dict]:
    claims_path = root / "Area_comun/state/CLAIMS.json"
    claims = json.loads(claims_path.read_text(encoding="utf-8-sig")).get("claims", [])
    return [c for c in claims if c.get("status") == "active" and c.get("owner") == owner]


def dirty_paths(root: Path) -> set[str]:
    proc = run(["git", "status", "--porcelain=v1"], root)
    paths: set[str] = set()
    for line in proc.stdout.splitlines():
        if not line:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.add(path.replace("\\", "/"))
    return paths


def dirty_claimed_route(root: Path, owner: str) -> bool:
    dirty = dirty_paths(root)
    if not dirty:
        return False
    for claim in active_claims_for_owner(root, owner):
        for scope in claim.get("scope", []):
            route = str(scope).split("#", 1)[0].replace("\\", "/")
            if route.startswith("D:/"):
                continue
            for path in dirty:
                if path == route or path.startswith(route.rstrip("/") + "/"):
                    return True
    return False


@contextlib.contextmanager
def global_lock(root: Path):
    lock_dir = root / ".protocol-tmp/cron_zombie_sweeper.lock"
    try:
        os.makedirs(lock_dir)
    except FileExistsError:
        raise SystemExit("sweeper_lock_busy")
    try:
        yield
    finally:
        with contextlib.suppress(OSError):
            os.rmdir(lock_dir)


def validate_after_kill(root: Path) -> dict[str, int]:
    commands = {
        "validate": [sys.executable, "scripts/validate_collaboration_state.py", "--root", "."],
        "drift": [
            sys.executable,
            "-c",
            "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; "
            "import json,sys; d=protocol_state_drift(Path('.')); print(json.dumps(d, ensure_ascii=False)); "
            "sys.exit(1 if d.get('has_drift') else 0)",
        ],
        "encoding": [sys.executable, "scripts/scan_encoding.py", "--root", "."],
    }
    return {name: run(cmd, root).returncode for name, cmd in commands.items()}


def decision_for_lease(root: Path, lease_path: Path, target_owner: str, checker_owner: str) -> dict:
    lease = json.loads(lease_path.read_text(encoding="utf-8-sig"))
    result = {
        "lease": str(lease_path),
        "owner": lease.get("owner"),
        "pid": lease.get("pid"),
        "action": "skip",
        "reason": "",
    }
    if lease.get("owner") != target_owner:
        result["reason"] = "owner_not_target"
        return result
    if lease.get("owner") == checker_owner:
        result["reason"] = "checker_owner_excluded"
        return result
    if parse_utc(str(lease.get("deadline"))) > utc_now():
        result["reason"] = "lease_not_expired"
        return result
    info = process_info(int(lease["pid"]))
    if not info:
        result["action"] = "cleanup_only"
        result["reason"] = "process_dead"
        return result
    if info["process_start_time_utc"] != str(lease.get("process_start_time_utc")).replace("+00:00", "Z"):
        result["reason"] = "pid_reuse_start_time_mismatch"
        return result
    cmdline = info["cmdline"] or str(lease.get("cmdline") or "")
    lowered = cmdline.lower()
    for token in DENY_CMD_TOKENS:
        if token in lowered:
            result["reason"] = f"deny_cmd_token:{token}"
            return result
    expected_hash = str(lease.get("cmdline_hash") or "")
    if expected_hash and hash_cmdline(str(lease.get("cmdline") or "")) != expected_hash:
        result["reason"] = "lease_cmdline_hash_mismatch"
        return result
    if dirty_claimed_route(root, target_owner):
        result["reason"] = "dirty_active_claim_route"
        return result
    result["action"] = "kill"
    result["reason"] = "expired_matching_lease"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--owner", required=True, help="Only sweep leases for this target owner.")
    parser.add_argument("--checker-owner", default="Arqui" + "tecto")
    parser.add_argument("--kill", action="store_true", help="Actually kill eligible processes.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    lease_paths = sorted((root / ".protocol-tmp").glob("*_mailbox_cron/*.exec-lease.json"))
    killed = []
    with global_lock(root):
        decisions = [decision_for_lease(root, path, args.owner, args.checker_owner) for path in lease_paths]
        if args.kill:
            for decision in decisions:
                if decision["action"] != "kill":
                    continue
                refreshed = decision_for_lease(root, Path(decision["lease"]), args.owner, args.checker_owner)
                if refreshed["action"] != "kill":
                    decision.update({"action": "skip", "reason": "recheck_changed:" + refreshed["reason"]})
                    continue
                subprocess.run(["taskkill", "/PID", str(decision["pid"]), "/T", "/F"], capture_output=True, text=True)
                killed.append(decision["pid"])
            post = validate_after_kill(root) if killed else {}
        else:
            post = {}
    output = {"mode": "kill" if args.kill else "dry-run", "decisions": decisions, "killed": killed, "post_validate": post}
    print(json.dumps(output, indent=2, ensure_ascii=False))
    if killed and any(code != 0 for code in post.values()):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
