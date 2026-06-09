#!/usr/bin/env python3
"""Regression golden: materialize_to_disk must stage on the SAME filesystem as the targets.

Background: on Windows, when the OS temp dir lives on a different drive than the repo,
materialize_to_disk used to stage files in the OS temp dir and then os.replace() them onto
the repo, which raises OSError WinError 17 ("cannot move file to another drive"). This broke
submit_intent on the live instance while every existing golden stayed green (their fixture
root and the OS temp share a drive). The fix stages under `root` so the rename is intra-FS.

This test simulates the cross-FS failure portably by monkeypatching os.replace to reject any
rename whose SOURCE is not under the fixture root (i.e. staged in some other location). With
the fix (staging under root) the source IS under root and the rename is allowed; without the
fix (staging in the OS temp) the source is outside root and the rename raises -> the case fails.
"""

from __future__ import annotations

import errno
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZE_CASES = ROOT / "examples/runtime_protocol_materialize_cases"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MATERIALIZE_CASES))

from run_runtime_protocol_materialize_cases import (  # noqa: E402
    event,
    hot_docs,
    read_json,
    replay_protocol_state,
)
from runtime.protocol_replay import materialize_protocol_state, materialize_to_disk  # noqa: E402
from runtime.temp_paths import root_temp_dir  # noqa: E402


def _is_under(child: Path, parent: Path) -> bool:
    child = child.resolve()
    parent = parent.resolve()
    return child == parent or parent in child.parents


def case_materialize_succeeds_when_temp_would_be_cross_fs() -> None:
    """Staging must be under root so the atomic rename never crosses filesystems."""
    with root_temp_dir(ROOT, ".materialize-cross-fs-") as root:
        snapshot = replay_protocol_state(
            [event(1, "protocol.genesis", {"state": hot_docs("done", "released")})]
        )

        real_replace = os.replace
        observed_sources: list[Path] = []

        def guarded_replace(src, dst, *args, **kwargs):  # noqa: ANN001
            src_path = Path(src)
            observed_sources.append(src_path)
            # Simulate an EXDEV failure for any staged source that is NOT on the same
            # filesystem as the targets (modeled here as "not under the repo root").
            if not _is_under(src_path, root):
                raise OSError(errno.EXDEV, "Invalid cross-device link (simulated)")
            return real_replace(src, dst, *args, **kwargs)

        os.replace = guarded_replace
        try:
            result = materialize_to_disk(root, snapshot)
        finally:
            os.replace = real_replace

        expected = materialize_protocol_state(snapshot)
        assert result["paths"] == sorted(expected), result["paths"]
        assert observed_sources, "materialize_to_disk performed no rename"
        for src in observed_sources:
            assert _is_under(src, root), f"staging escaped root (cross-FS regression): {src}"
        for relative, document in expected.items():
            assert read_json(root / relative) == document, relative


def case_materialize_is_still_idempotent_under_guard() -> None:
    """A second materialize over identical state is a no-op and stays intra-FS."""
    with root_temp_dir(ROOT, ".materialize-cross-fs-idem-") as root:
        snapshot = replay_protocol_state(
            [event(1, "protocol.genesis", {"state": hot_docs("done", "released")})]
        )
        materialize_to_disk(root, snapshot)
        before = {p: (root / p).read_bytes() for p in materialize_protocol_state(snapshot)}

        real_replace = os.replace

        def guarded_replace(src, dst, *args, **kwargs):  # noqa: ANN001
            if not _is_under(Path(src), root):
                raise OSError(errno.EXDEV, "Invalid cross-device link (simulated)")
            return real_replace(src, dst, *args, **kwargs)

        os.replace = guarded_replace
        try:
            materialize_to_disk(root, snapshot)
        finally:
            os.replace = real_replace

        after = {p: (root / p).read_bytes() for p in materialize_protocol_state(snapshot)}
        assert after == before


def main() -> int:
    cases = [
        case_materialize_succeeds_when_temp_would_be_cross_fs,
        case_materialize_is_still_idempotent_under_guard,
    ]
    for case in cases:
        case()
    print(f"OK: {len(cases)} materialize cross-FS golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
