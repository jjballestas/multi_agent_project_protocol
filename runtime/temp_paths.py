#!/usr/bin/env python3
"""Root-local temporary directories with inherited filesystem permissions."""

from __future__ import annotations

import os
import shutil
import stat
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class TempPathError(RuntimeError):
    pass


PROTOCOL_TEMP_PARENT_NAME = ".protocol-tmp"
_TEMP_SUFFIX_HEX_CHARS = 16
_CLEANUP_ATTEMPTS = 4
_CLEANUP_RETRY_DELAY_SECONDS = 0.05


def protocol_temp_parent(root: Path) -> Path:
    return root.resolve() / PROTOCOL_TEMP_PARENT_NAME


def _validate_prefix(prefix: str) -> None:
    if not prefix or "/" in prefix or "\\" in prefix or prefix in {".", ".."}:
        raise TempPathError(f"invalid root-local temporary directory prefix: {prefix!r}")


def make_root_temp_dir(root: Path, prefix: str) -> Path:
    root = root.resolve()
    _validate_prefix(prefix)
    parent = protocol_temp_parent(root)
    try:
        parent.mkdir(exist_ok=True)
    except OSError as exc:
        raise TempPathError(f"could not create root-local temporary parent {parent}") from exc
    for _ in range(100):
        temp_root = parent / f"{prefix}{uuid.uuid4().hex[:_TEMP_SUFFIX_HEX_CHARS]}"
        try:
            temp_root.mkdir()
            return temp_root
        except FileExistsError:
            continue
    raise TempPathError(f"could not create root-local temporary directory under {parent}")


def _chmod_and_retry(function: object, path: str, _exc_info: object) -> None:
    try:
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
    except OSError:
        pass
    function(path)  # type: ignore[operator]


def _remove_empty_protocol_parent(temp_root: Path) -> None:
    parent = temp_root.parent
    if parent.name != PROTOCOL_TEMP_PARENT_NAME:
        return
    try:
        parent.rmdir()
    except OSError:
        pass


def remove_root_temp_dir(
    temp_root: Path,
    *,
    strict: bool = False,
    attempts: int = _CLEANUP_ATTEMPTS,
    retry_delay_seconds: float = _CLEANUP_RETRY_DELAY_SECONDS,
) -> bool:
    """Remove a root-local temp dir with bounded Windows-friendly retries."""

    temp_root = Path(temp_root)
    attempts = max(1, attempts)
    last_error: OSError | None = None

    for attempt in range(attempts):
        try:
            shutil.rmtree(temp_root, onerror=_chmod_and_retry)
        except FileNotFoundError:
            _remove_empty_protocol_parent(temp_root)
            return True
        except OSError as exc:
            last_error = exc

        if not temp_root.exists():
            _remove_empty_protocol_parent(temp_root)
            return True
        if attempt + 1 < attempts:
            time.sleep(retry_delay_seconds)

    if strict:
        message = f"could not remove root-local temporary directory {temp_root}"
        if last_error is not None:
            raise TempPathError(message) from last_error
        raise TempPathError(message)
    return False


@contextmanager
def root_temp_dir(root: Path, prefix: str) -> Iterator[Path]:
    temp_root = make_root_temp_dir(root, prefix)
    try:
        yield temp_root
    finally:
        remove_root_temp_dir(temp_root, strict=True)
