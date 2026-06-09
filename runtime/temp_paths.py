#!/usr/bin/env python3
"""Root-local temporary directories with inherited filesystem permissions."""

from __future__ import annotations

import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class TempPathError(RuntimeError):
    pass


def make_root_temp_dir(root: Path, prefix: str) -> Path:
    root = root.resolve()
    for _ in range(100):
        temp_root = root / f"{prefix}{uuid.uuid4().hex}"
        try:
            temp_root.mkdir()
            return temp_root
        except FileExistsError:
            continue
    raise TempPathError(f"could not create root-local temporary directory under {root}")


@contextmanager
def root_temp_dir(root: Path, prefix: str) -> Iterator[Path]:
    temp_root = make_root_temp_dir(root, prefix)
    try:
        yield temp_root
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
