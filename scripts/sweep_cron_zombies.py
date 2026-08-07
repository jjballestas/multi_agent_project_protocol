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


def parse_porcelain_v1_z(raw: bytes) -> set[str]:
    paths: set[str] = set()
    records = raw.split(b"\0")
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise ValueError("malformed git status --porcelain=v1 -z record")
        status = record[:2]
        paths.add(record[3:].decode("utf-8", errors="surrogateescape").replace("\\", "/"))
        if b"R" in status or b"C" in status:
            if index >= len(records) or not records[index]:
                raise ValueError("missing source path in git status --porcelain=v1 -z pair")
            paths.add(records[index].decode("utf-8", errors="surrogateescape").replace("\\", "/"))
            index += 1
    return paths


def dirty_paths(root: Path) -> set[str]:
    root = root.resolve()
    dirty: set[str] = set()
    for repository_root in repository_roots(root):
        dirty.update(repository_dirty_paths(root, repository_root))
    return dirty


def repository_roots(root: Path) -> list[Path]:
    """Return every physical Git worktree below root, at arbitrary depth.

    Detection is one filesystem walk (O(directories)); symlinked directories are not
    followed.  Any traversal error raises, so callers that authorize termination fail
    closed.  Each detected repository adds one Git status invocation.
    """
    root = root.resolve()
    repositories = [root]

    def fail(error: OSError) -> None:
        raise error

    for current, directories, files in os.walk(root, topdown=True, onerror=fail, followlinks=False):
        current_path = Path(current)
        has_marker = ".git" in directories or ".git" in files
        if current_path != root and has_marker:
            repositories.append(current_path)
        directories[:] = [name for name in directories if name != ".git"]
    return repositories


def repository_dirty_paths(root: Path, repository_root: Path) -> set[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repository_root,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("git status --porcelain=v1 -z failed")
    prefix = repository_root.relative_to(root).as_posix()
    paths = parse_porcelain_v1_z(proc.stdout)
    if not prefix or prefix == ".":
        return paths
    return {f"{prefix}/{path}" for path in paths}


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


def lock_path_for_lease(lease_path: Path) -> Path:
    name = lease_path.name.replace(".exec-lease.json", ".lock")
    return lease_path.with_name(name)


def cleanup_dead_lease(lease_path: Path) -> list[str]:
    removed: list[str] = []
    for path in (lock_path_for_lease(lease_path), lease_path):
        if not path.exists():
            continue
        path.unlink()
        removed.append(str(path))
    return removed


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
        cleaned = []
        cleanup_errors = []
        if args.kill:
            for decision in decisions:
                if decision["action"] == "cleanup_only":
                    refreshed = decision_for_lease(root, Path(decision["lease"]), args.owner, args.checker_owner)
                    if refreshed["action"] != "cleanup_only":
                        decision.update({"action": "skip", "reason": "recheck_changed:" + refreshed["reason"]})
                        continue
                    try:
                        removed = cleanup_dead_lease(Path(decision["lease"]))
                    except OSError as exc:
                        decision.update({"action": "error", "reason": f"cleanup_failed:{exc}"})
                        cleanup_errors.append(str(exc))
                        continue
                    if not removed:
                        decision.update({"action": "error", "reason": "cleanup_failed:no_files_removed"})
                        cleanup_errors.append(str(decision["lease"]))
                        continue
                    decision["removed"] = removed
                    cleaned.extend(removed)
                    continue
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
            cleaned = []
            cleanup_errors = []
            post = {}
    output = {
        "mode": "kill" if args.kill else "dry-run",
        "decisions": decisions,
        "killed": killed,
        "cleaned": cleaned,
        "post_validate": post,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    if cleanup_errors:
        return 3
    if killed and any(code != 0 for code in post.values()):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
