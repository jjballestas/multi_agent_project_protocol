#!/usr/bin/env python3
"""Scan protocol files for coordination-channel encoding drift."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ASCII_CHANNEL_GLOBS = (
    "Area_comun/mailbox/**/*",
    "Area_comun/state/*.json",
)
MOJIBAKE_ROOTS = ("Area_comun", "runtime")
MOJIBAKE_SIGNATURES = (
    "\u00c3",
    "\u00c2",
    "\u00e2\u20ac",
    "\u00e2\u20ac\u2122",
    "\u00e2\u20ac\u0153",
    "\u00e2\u20ac\ufffd",
    "\u00e2\u20ac\u201c",
    "\u00e2\u20ac\u201d",
    "\u00e2\u20ac\u00a6",
    "\ufffd",
)
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}
SKIP_RELATIVE_DIRS = {"runtime/memory"}
SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip"}


@dataclass(frozen=True)
class Finding:
    kind: str
    path: Path
    line: int
    detail: str


def shared_suffix(name: str) -> str:
    """Return the normalized final suffix; a leading dot alone is not a suffix."""
    dot = name.rfind(".")
    return name[dot:].lower() if dot > 0 else ""


def iter_files(root: Path, patterns: tuple[str, ...]) -> set[Path]:
    files: set[Path] = set()
    for pattern in patterns:
        for path in root.glob(pattern):
            if should_scan(path, root):
                files.add(path)
    return files


def should_scan(path: Path, root: Path | None = None) -> bool:
    if not path.is_file():
        return False
    if shared_suffix(path.name) in SKIP_SUFFIXES:
        return False
    if root is not None:
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            relative = ""
        if any(relative == item or relative.startswith(f"{item}/") for item in SKIP_RELATIVE_DIRS):
            return False
    return not any(part in SKIP_DIRS for part in path.parts)


def line_number_for_offset(data: bytes, offset: int) -> int:
    return data.count(b"\n", 0, offset) + 1


def scan_ascii_channel(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(iter_files(root, ASCII_CHANNEL_GLOBS)):
        data = path.read_bytes()
        for index, byte in enumerate(data):
            if byte > 0x7F:
                findings.append(
                    Finding(
                        kind="non_ascii_channel",
                        path=path.relative_to(root),
                        line=line_number_for_offset(data, index),
                        detail=f"byte 0x{byte:02x}",
                    )
                )
                break
    return findings


def scan_mojibake(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for root_name in MOJIBAKE_ROOTS:
        scan_root = root / root_name
        if not scan_root.exists():
            continue
        for path in sorted(p for p in scan_root.rglob("*") if should_scan(p, root)):
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            for line_number, line in enumerate(text.splitlines(), start=1):
                for signature in MOJIBAKE_SIGNATURES:
                    if signature in line:
                        findings.append(
                            Finding(
                                kind="mojibake",
                                path=path.relative_to(root),
                                line=line_number,
                                detail=signature,
                            )
                        )
                        break
                else:
                    continue
                break
    return findings


def scan(root: Path) -> list[Finding]:
    root = root.resolve()
    return scan_ascii_channel(root) + scan_mojibake(root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan protocol files for encoding drift.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="Instance root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    findings = scan(Path(args.root))
    if findings:
        print("ENCODING ERRORS:")
        for finding in findings:
            print(f"- {finding.kind}: {finding.path}:{finding.line} ({finding.detail})")
        return 1
    print("OK: encoding scan is clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
