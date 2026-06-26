#!/usr/bin/env python3
"""Golden cases for the H1-H3 experiment harness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.experiment_h1h3.harness import hash_live_guard, run
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


def case_disposable_and_thresholds() -> tuple[str, bool, str]:
    output = make_root_temp_dir(ROOT, ".h1h3-results-")
    before = hash_live_guard(ROOT)
    try:
        report = run(ROOT, seed=104, k=9, output_dir=output, run_id="golden")
        after = hash_live_guard(ROOT)
        ok = (
            before == after
            and report["live_root_byte_identical"] is True
            and report["detection"]["tpr"] == 1.0
            and report["detection"]["fpr"] == 0.0
            and all(item["pass"] for item in report["threshold_mapping"].values())
            and (output / "golden.json").exists()
            and (output / "golden.md").exists()
        )
        return "AC1-AC6-disposable-thresholds", ok, json.dumps(report["threshold_mapping"], sort_keys=True)
    finally:
        remove_root_temp_dir(output, strict=True)


def case_seed_reproducible() -> tuple[str, bool, str]:
    out_a = make_root_temp_dir(ROOT, ".h1h3-repro-a-")
    out_b = make_root_temp_dir(ROOT, ".h1h3-repro-b-")
    try:
        first = run(ROOT, seed=66, k=7, output_dir=out_a, run_id="same")
        second = run(ROOT, seed=66, k=7, output_dir=out_b, run_id="same")
        comparable_keys = ["seed", "K", "detection", "overhead", "external_verifier", "threshold_mapping"]
        ok = {key: first[key] for key in comparable_keys} == {key: second[key] for key in comparable_keys}
        return "AC2-AC6-seed-reproducible", ok, json.dumps(first["detection"]["attacks"], sort_keys=True)
    finally:
        remove_root_temp_dir(out_a, strict=True)
        remove_root_temp_dir(out_b, strict=True)


def main() -> int:
    results = [case_disposable_and_thresholds(), case_seed_reproducible()]
    print(json.dumps({"experiment_h1h3_cases.v1": [{"name": name, "ok": ok, "detail": detail} for name, ok, detail in results]}, indent=2, sort_keys=True))
    return 0 if all(ok for _name, ok, _detail in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
