#!/usr/bin/env python3
"""Sweep leftover repo-local temporary directories.

The runtime write-path and the golden test harnesses create repo-local inherited-ACL temp dirs
(DECISION-0023 boundary / TASK-0094 hardening: avoid %TEMP% 0o700 dirs that the Windows unelevated
sandbox token cannot access). They are transient and regenerable; the live runtime removes its own,
but test harnesses can leak them on Windows when shutil.rmtree(ignore_errors=True) hits a locked file.
New temp dirs live under .protocol-tmp/; this sweeper also removes legacy root-level leftovers from
before that consolidation. It NEVER touches tracked content or .git/.

Default is a dry-run (prints what it would remove). Pass --apply to delete.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_FOR_IMPORT = Path(__file__).resolve().parents[1]
if str(ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(ROOT_FOR_IMPORT))

from runtime.temp_paths import PROTOCOL_TEMP_PARENT_NAME, remove_root_temp_dir  # noqa: E402

# Legacy repo-root temp-dir prefixes (dir name = "<prefix><hex>"). Keep specific to avoid
# deleting anything legitimate. New temp dirs should live under PROTOCOL_TEMP_PARENT_NAME.
TEMP_PREFIXES = (
    ".protocol-state-materialize-",
    ".runtime-state-backup-",
    ".submit-intent-runtime-backup-",
    ".protocol-materialize-",
    ".protocol-replay-nested-temp-",
    ".runtime-real-",
    ".debug-replay-temp-",
    ".smoke-fixture-",
)

# Never remove these, even if a prefix somehow matched.
PROTECTED = {".git", ".github", ".githooks", ".claude"}


def find_temp_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name in PROTECTED:
            continue
        if any(child.name.startswith(prefix) for prefix in TEMP_PREFIXES):
            found.append(child)
    parent = root / PROTOCOL_TEMP_PARENT_NAME
    if parent.is_dir():
        for child in sorted(parent.iterdir()):
            if child.is_dir():
                found.append(child)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep leftover repo-local temp dirs.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--apply", action="store_true", help="Delete the dirs (default: dry-run).")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    targets = find_temp_dirs(root)
    if not targets:
        print("clean: no leftover temp dirs at repo root.")
        return 0

    print(f"{'removing' if args.apply else 'would remove'} {len(targets)} leftover temp dir(s):")
    removed = 0
    for path in targets:
        print(f"  {path.relative_to(root)}")
        if args.apply:
            if remove_root_temp_dir(path):
                removed += 1
    if args.apply:
        print(f"removed {removed}/{len(targets)} (locked dirs, if any, are skipped; re-run later).")
    else:
        print("dry-run: pass --apply to delete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
