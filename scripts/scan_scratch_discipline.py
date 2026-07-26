#!/usr/bin/env python3
"""Report methodology work trees outside a designated scratch root."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable
from urllib.parse import unquote, urlparse


ATTESTED_MARKERS = ("Area_comun", "runtime", "protocol.config.json")
RULE = (
    "DECISION-0018: methodology work must live below the designated scratch "
    "root; notify the responsible owner. This detector never deletes or moves data."
)


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _is_below(path: Path, parent: Path) -> bool:
    try:
        _resolved(path).relative_to(_resolved(parent))
        return True
    except ValueError:
        return False


def _repo_identity(value: str, base: Path) -> str:
    raw = value.strip().replace("\\", "/")
    if not raw:
        return ""
    if re.match(r"^[^/@:\s]+@[^/:\s]+:", raw):
        host, repo_path = raw.split(":", 1)
        raw = f"ssh://{host.split('@', 1)[1]}/{repo_path}"
    parsed = urlparse(raw)
    if parsed.scheme == "file":
        raw = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:/", raw):
            raw = raw[1:]
    elif parsed.scheme and parsed.netloc:
        repo_path = parsed.path.rstrip("/")
        if repo_path.lower().endswith(".git"):
            repo_path = repo_path[:-4]
        return f"{parsed.hostname or parsed.netloc}{repo_path}".casefold()
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = base / candidate
    normalized = os.path.normcase(str(_resolved(candidate))).rstrip("\\/")
    if normalized.lower().endswith(".git"):
        normalized = normalized[:-4]
    return normalized.casefold()


def _remote_urls(directory: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(directory), "config", "--get-regexp", r"^remote\..*\.url$"],
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    urls: list[str] = []
    for line in result.stdout.splitlines():
        fields = line.split(None, 1)
        if len(fields) == 2:
            urls.append(fields[1])
    return urls


def _attested_tree(directory: Path) -> bool:
    return all((directory / marker).exists() for marker in ATTESTED_MARKERS)


def _git_reason(directory: Path, known: set[str]) -> str | None:
    if not (directory / ".git").exists() or not known:
        return None
    for remote in _remote_urls(directory):
        if _repo_identity(remote, directory) in known:
            return f"git remote matches known repository: {remote}"
    return None


def find_anomalies(
    scan_roots: Iterable[Path], scratch_root: Path, known_repositories: Iterable[str]
) -> list[dict[str, str]]:
    known = {
        identity
        for value in known_repositories
        if (identity := _repo_identity(value, Path.cwd()))
    }
    findings: list[dict[str, str]] = []
    for scan_root in scan_roots:
        root = _resolved(scan_root)
        try:
            children = sorted(
                (entry for entry in root.iterdir() if entry.is_dir()),
                key=lambda entry: os.path.normcase(entry.name),
            )
        except OSError as exc:
            raise RuntimeError(f"cannot inspect scan root {root}: {exc}") from exc
        for child in children:
            if _is_below(child, scratch_root):
                continue
            reason = _git_reason(child, known)
            if reason is None and _attested_tree(child):
                reason = "contains attested tree markers: " + ", ".join(ATTESTED_MARKERS)
            if reason is not None:
                findings.append(
                    {"path": str(_resolved(child)), "reason": reason, "rule": RULE}
                )
    return findings


def _load_config(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot read config {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"config {path} must contain a JSON object")
    return value


def _config_values(config: dict) -> tuple[str | None, list[str]]:
    section = config.get("scratch_discipline", {})
    if not isinstance(section, dict):
        section = {}
    scratch = section.get("scratch_root", config.get("scratch_root"))
    repositories = section.get("known_repositories", config.get("known_repositories", []))
    if repositories is None:
        repositories = []
    if not isinstance(repositories, list) or not all(
        isinstance(item, str) for item in repositories
    ):
        raise RuntimeError("known_repositories in config must be a list of strings")
    return scratch if isinstance(scratch, str) else None, repositories


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only scan for methodology trees outside a scratch root."
    )
    parser.add_argument("--scan-root", action="append", required=True, type=Path)
    parser.add_argument("--scratch-root", type=Path)
    parser.add_argument("--known-repo", action="append", default=[])
    parser.add_argument("--config", type=Path, default=Path("protocol.config.json"))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        config = _load_config(args.config) if args.config.exists() else {}
        configured_scratch, configured_repositories = _config_values(config)
        scratch_root = args.scratch_root or (
            Path(configured_scratch) if configured_scratch else None
        )
        if scratch_root is None:
            raise RuntimeError(
                "scratch root is required: use --scratch-root or configure scratch_root"
            )
        findings = find_anomalies(
            args.scan_root,
            scratch_root,
            [*configured_repositories, *args.known_repo],
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps({"findings": findings}, indent=2, ensure_ascii=True))
    elif findings:
        for finding in findings:
            print(f"ANOMALY: {finding['path']}")
            print(f"  reason: {finding['reason']}")
            print(f"  rule: {finding['rule']}")
    else:
        print("OK: no scratch-discipline anomalies found.")
    return 1 if args.check and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
