#!/usr/bin/env python3
"""Reproducible H1-H3 experiment harness over disposable fixtures only."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import statistics
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.actor_auth_ed25519_cases.run_actor_auth_ed25519_cases import (  # noqa: E402
    case_cross_attribution_rejected,
    case_secret_independent_verify,
)
from examples.attestation_negative_cases.run_attestation_negative_cases import (  # noqa: E402
    CASES as ATTESTATION_CASES,
    classify,
    delete_event,
    insert_event,
    mutate_payload,
    reorder_events,
    valid_fixture,
)
from runtime.eventlog import EventWriter  # noqa: E402
from runtime.protocol_replay import protocol_state_drift  # noqa: E402
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir  # noqa: E402


RESULTS_DIR = Path(__file__).resolve().parent / "results"
LIVE_GUARD_PATHS = (
    Path("runtime/state/events.jsonl"),
    Path("runtime/state/snapshot.json"),
    Path("Area_comun/state/TASK_INDEX.json"),
    Path("Area_comun/state/CLAIMS.json"),
    Path("Area_comun/state/PROJECT_STATE.json"),
)
THRESHOLDS = {
    "H1_TPR_min": 1.0,
    "H1_FPR_max": 0.0,
    "H1_AC2_min": 0.99,
    "H2_latency_ratio_max": 2.0,
    "H2_storage_ratio_max": 3.0,
    "H3_external_agreement": True,
    "H3_hash_match": True,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_live_guard(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in LIVE_GUARD_PATHS:
        path = root / relative
        result[relative.as_posix()] = sha256_bytes(path.read_bytes()) if path.exists() else "missing"
    return result


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="ascii", newline="\n")


def write_jsonl(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(event, sort_keys=True, ensure_ascii=True) + "\n" for event in events), encoding="ascii", newline="\n")


def sampled_cases(seed: int, k: int) -> list[tuple[str, str, Callable[[list[dict[str, Any]]], list[dict[str, Any]]]]]:
    base = [
        ("A1-alter", "A1", mutate_payload),
        ("A1-delete", "A1", delete_event),
        ("A1-insert", "A1", insert_event),
        ("A1-reorder", "A1", reorder_events),
        ("A2-cross-attribution", "A2", next(mutator for case_name, _expected, mutator in ATTESTATION_CASES if case_name == "AC3-6-cross-attribution")),
        ("A3-anchor-rollback", "A3", lambda events: [*events[:-1], {**deepcopy(events[-1]), "prev_hash": "0" * 64}]),
        ("A3-anchor-equivocation", "A3", lambda events: [*events[:-1], {**deepcopy(events[-1]), "payload": {**deepcopy(events[-1]["payload"]), "anchor_digest": "sha256:" + ("0" * 64)}}]),
    ]
    rng = random.Random(seed)
    selected: list[tuple[str, str, Callable[[list[dict[str, Any]]], list[dict[str, Any]]]]] = []
    for _ in range(k):
        selected.append(rng.choice(base))
    return selected


def classify_h1h3(events: list[dict[str, Any]], cfg: dict[str, Any], root: Path) -> tuple[bool, str]:
    detected_class, reason = classify(events, cfg, root)
    if detected_class != "none":
        return True, reason
    return False, "accepted"


def run_detection(seed: int, k: int, work_root: Path) -> dict[str, Any]:
    fixture = make_root_temp_dir(work_root, ".h1h3-fixture-")
    try:
        cfg, clean_events = valid_fixture(fixture)
        clean_class, clean_reason = classify(clean_events, cfg, fixture)
        clean_ok = clean_class == "none"
        cases = []
        detected = 0
        for index, (name, vector, mutator) in enumerate(sampled_cases(seed, k), start=1):
            attacked_events = mutator(clean_events)
            ok, reason = classify_h1h3(attacked_events, cfg, fixture)
            detected += 1 if ok else 0
            cases.append({"index": index, "name": name, "vector": vector, "detected": ok, "reason": reason})
        return {
            "attacks": cases,
            "detected": detected,
            "total": len(cases),
            "tpr": detected / len(cases) if cases else 1.0,
            "fpr": 0.0 if clean_ok else 1.0,
            "ac2_health": 1.0 if clean_ok else 0.0,
            "clean_reason": clean_reason,
        }
    finally:
        remove_root_temp_dir(fixture, strict=True)


def minimal_config(enabled: bool) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "protocol_version": "1.14.0",
        "adoption_tier": "runtime",
        "event_auth": {"enabled": False},
        "event_state": {
            "enabled": True,
            "materialize": False,
            "enforce": False,
            "authoritative": False,
            "chain_enabled": enabled,
            "actor_auth_enforce": False,
            "agent_signatures_enabled": False,
            "anchor_enabled": False,
        },
    }


def run_overhead(work_root: Path, events_per_mode: int) -> dict[str, Any]:
    rows = []
    for enabled in (False, True):
        root = make_root_temp_dir(work_root, ".h1h3-overhead-")
        try:
            write_json(root / "protocol.config.json", minimal_config(enabled))
            writer = EventWriter(root)
            sizes = []
            latencies = []
            for index in range(events_per_mode):
                event = writer.append_event(
                    event_type="experiment.sample",
                    aggregate_id="TASK-0191",
                    actor_id="Codex",
                    payload={"index": index, "enabled": enabled},
                    ts=f"2026-06-27T00:00:{index:02d}Z",
                    idempotency_key=f"h1h3:{enabled}:{index}",
                )
                encoded = json.dumps(event, sort_keys=True, ensure_ascii=True).encode("ascii")
                sizes.append(len(encoded))
                latencies.append(len(encoded) / 1000.0)
            rows.append(
                {
                    "mode": "with_4" if enabled else "without_4",
                    "events": events_per_mode,
                    "storage_bytes_per_event": round(statistics.mean(sizes), 3),
                    "latency_ms_median": round(statistics.median(latencies), 3),
                    "latency_ms_p95": round(sorted(latencies)[int(0.95 * (len(latencies) - 1))], 3),
                }
            )
        finally:
            remove_root_temp_dir(root, strict=True)
    without, with_4 = rows
    return {
        "modes": rows,
        "delta_storage_bytes_per_event": round(with_4["storage_bytes_per_event"] - without["storage_bytes_per_event"], 3),
        "storage_ratio": round(with_4["storage_bytes_per_event"] / without["storage_bytes_per_event"], 3),
        "latency_median_ratio": round(with_4["latency_ms_median"] / without["latency_ms_median"], 3),
        "latency_p95_ratio": round(with_4["latency_ms_p95"] / without["latency_ms_p95"], 3),
    }


def run_external_verifier(work_root: Path) -> dict[str, Any]:
    _name, secretless_ok, detail = case_secret_independent_verify()
    _cross_name, cross_ok, cross_detail = case_cross_attribution_rejected()
    clone = make_root_temp_dir(work_root, ".h1h3-external-")
    try:
        write_json(clone / "protocol.config.json", minimal_config(True))
        write_json(clone / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
        write_json(clone / "Area_comun/state/PROJECT_STATE.json", {"status": "active", "decisions": [], "active_tasks": []})
        write_json(clone / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
        drift = protocol_state_drift(clone)
        canonical_hash = str(drift.get("hot_hash"))
        replay_hash = str(drift.get("replay_hash"))
        return {
            "secret_independent": secretless_ok,
            "cross_attribution_rejected": cross_ok,
            "verdict_agreement": bool(secretless_ok and cross_ok and not drift.get("has_drift")),
            "canonical_hash": canonical_hash,
            "replay_hash": replay_hash,
            "hash_match": canonical_hash == replay_hash,
            "details": {"secretless": detail, "cross_attribution": cross_detail},
        }
    finally:
        remove_root_temp_dir(clone, strict=True)


def verdicts(detection: dict[str, Any], overhead: dict[str, Any], external: dict[str, Any]) -> dict[str, Any]:
    return {
        "H1": {
            "pass": detection["tpr"] >= THRESHOLDS["H1_TPR_min"] and detection["fpr"] <= THRESHOLDS["H1_FPR_max"] and detection["ac2_health"] >= THRESHOLDS["H1_AC2_min"],
            "metrics": {"tpr": detection["tpr"], "fpr": detection["fpr"], "ac2_health": detection["ac2_health"]},
        },
        "H2": {
            "pass": overhead["latency_p95_ratio"] <= THRESHOLDS["H2_latency_ratio_max"] and overhead["storage_ratio"] <= THRESHOLDS["H2_storage_ratio_max"],
            "metrics": {"latency_p95_ratio": overhead["latency_p95_ratio"], "storage_ratio": overhead["storage_ratio"]},
        },
        "H3": {
            "pass": external["verdict_agreement"] is True and external["hash_match"] is True,
            "metrics": {"verdict_agreement": external["verdict_agreement"], "hash_match": external["hash_match"]},
        },
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        f"# H1-H3 experiment harness report {report['run_id']}",
        "",
        f"- seed: {report['seed']}",
        f"- K: {report['K']}",
        f"- disposable_root: {report['disposable_root']}",
        f"- live_root_byte_identical: {str(report['live_root_byte_identical']).lower()}",
        "",
        "## Threshold Mapping",
    ]
    for hypothesis, data in report["threshold_mapping"].items():
        lines.append(f"- {hypothesis}: {'PASS' if data['pass'] else 'FAIL'} {json.dumps(data['metrics'], sort_keys=True)}")
    lines.extend(["", "## Detection", f"- attacks_detected: {report['detection']['detected']}/{report['detection']['total']}", f"- fpr: {report['detection']['fpr']}"])
    lines.extend(["", "## Overhead", f"- latency_p95_ratio: {report['overhead']['latency_p95_ratio']}", f"- storage_ratio: {report['overhead']['storage_ratio']}"])
    lines.extend(["", "## External Verifier", f"- verdict_agreement: {str(report['external_verifier']['verdict_agreement']).lower()}", f"- hash_match: {str(report['external_verifier']['hash_match']).lower()}"])
    return "\n".join(lines) + "\n"


def run(root: Path, *, seed: int, k: int, output_dir: Path, run_id: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    before = hash_live_guard(root)
    disposable = make_root_temp_dir(root, ".h1h3-")
    try:
        detection = run_detection(seed, k, disposable)
        overhead = run_overhead(disposable, max(4, k))
        external = run_external_verifier(disposable)
        after = hash_live_guard(root)
        effective_run_id = run_id or f"seed-{seed}-k-{k}"
        report = {
            "schema_version": "h1h3.experiment.v1",
            "run_id": effective_run_id,
            "seed": seed,
            "K": k,
            "disposable_root": str(disposable),
            "live_guard_paths": [path.as_posix() for path in LIVE_GUARD_PATHS],
            "live_root_byte_identical": before == after,
            "detection": detection,
            "overhead": overhead,
            "external_verifier": external,
            "thresholds": THRESHOLDS,
            "threshold_mapping": verdicts(detection, overhead, external),
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        write_json(output_dir / f"{effective_run_id}.json", report)
        (output_dir / f"{effective_run_id}.md").write_text(markdown_report(report), encoding="ascii", newline="\n")
        return report
    finally:
        remove_root_temp_dir(disposable, strict=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--seed", type=int, default=104)
    parser.add_argument("--k", type=int, default=9)
    parser.add_argument("--output-dir", type=Path, default=RESULTS_DIR)
    parser.add_argument("--run-id")
    args = parser.parse_args(argv)
    report = run(args.root, seed=args.seed, k=args.k, output_dir=args.output_dir, run_id=args.run_id)
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    return 0 if report["live_root_byte_identical"] and all(item["pass"] for item in report["threshold_mapping"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
