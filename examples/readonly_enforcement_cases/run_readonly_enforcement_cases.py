#!/usr/bin/env python3
"""DECISION-0041 read-only enforcement negative cases."""

from __future__ import annotations

import ast
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


WRITE_METHODS = {"write_text", "write_bytes", "open"}
WRITE_MODES = {"w", "a", "x", "r+", "w+", "a+", "x+"}


class CoreWriteVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.findings: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802 - ast API
        if isinstance(node.func, ast.Attribute) and node.func.attr in WRITE_METHODS:
            self.findings.append(f"write method call: {node.func.attr}")
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            for arg in node.args[1:2]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and any(mode in arg.value for mode in WRITE_MODES):
                    self.findings.append(f"open write mode: {arg.value}")
        self.generic_visit(node)


def assert_no_core_write_capability(source: str) -> list[str]:
    visitor = CoreWriteVisitor()
    visitor.visit(ast.parse(source))
    return visitor.findings


def case_static_review_rejects_write_api() -> dict[str, Any]:
    read_only_source = """
from pathlib import Path
def read_core(root):
    return (Path(root) / "runtime/state/events.jsonl").read_text(encoding="utf-8")
"""
    write_source = """
from pathlib import Path
def write_core(root):
    (Path(root) / "runtime/state/events.jsonl").write_text("tamper", encoding="utf-8")
"""
    assert assert_no_core_write_capability(read_only_source) == []
    findings = assert_no_core_write_capability(write_source)
    assert findings and "write_text" in findings[0]
    return {"case": "A3-static-review-write-api", "status": "pass", "findings": findings}


def case_os_rejects_write_to_readonly_core_file(tmp: Path) -> dict[str, Any]:
    core_file = tmp / "core" / "runtime" / "state" / "events.jsonl"
    core_file.parent.mkdir(parents=True)
    core_file.write_text('{"seq":1}\n', encoding="ascii")
    original_mode = stat.S_IMODE(core_file.stat().st_mode)
    core_file.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    script = (
        "from pathlib import Path\n"
        "import sys\n"
        "path = Path(sys.argv[1])\n"
        "path.write_text('tamper\\n', encoding='ascii')\n"
    )
    try:
        result = subprocess.run([sys.executable, "-c", script, str(core_file)], text=True, capture_output=True, check=False)
        rejected = result.returncode != 0
        assert rejected, {"stdout": result.stdout, "stderr": result.stderr}
        assert core_file.read_text(encoding="ascii") == '{"seq":1}\n'
        return {"case": "A3-os-negative-write-rejected", "status": "pass", "returncode": result.returncode}
    finally:
        core_file.chmod(original_mode | stat.S_IWRITE)
        if os.name != "nt":
            core_file.chmod(original_mode)


def main() -> int:
    tmp = make_root_temp_dir(ROOT, "readonly-enforcement-")
    try:
        results = [case_static_review_rejects_write_api(), case_os_rejects_write_to_readonly_core_file(tmp)]
    finally:
        remove_root_temp_dir(tmp, strict=True)
    print(json.dumps({"schema_version": "readonly_enforcement_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
