#!/usr/bin/env python3
"""Read-only agent and worker metrics aggregator for the protocol ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime import metrics as runtime_metrics

QUALITY_REJECTED_STATUSES = {"changes_requested", "cancelled"}
DONE_STATUS = "done"
AUTHOR_STATUSES = {"claimed", "in_progress", "in_review"}
REVIEW_STATUSES = {"changes_requested", "done"}

PINNED_RELATIVE_PATHS = [
    "runtime/state/events.jsonl",
    "runtime/eventlog.py",
    "scripts/validate_collaboration_state.py",
    "protocol.config.json",
    "event-state.runtime.json",
    "runtime/state/snapshot.json",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pinned_hashes(root: Path) -> dict[str, str | None]:
    return {relative: sha256_file(root / relative) for relative in PINNED_RELATIVE_PATHS}


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def seconds_between(start: datetime | None, end: datetime | None) -> int | None:
    if start is None or end is None or end < start:
        return None
    return int((end - start).total_seconds())


def sorted_dict(values: dict[str, Any]) -> dict[str, Any]:
    return {key: values[key] for key in sorted(values)}


def agent_bucket() -> dict[str, Any]:
    return {
        "calidad": {
            "done": 0,
            "rechazadas": 0,
            "tasa_aceptacion": None,
            "ciclos_revision_total": 0,
            "ciclos_revision_promedio": 0.0,
        },
        "tiempo": {
            "lead_time_seconds_total": 0,
            "lead_time_seconds_promedio": None,
            "cycle_time_seconds_total": 0,
            "cycle_time_seconds_promedio": None,
            "tareas_con_lead_time": 0,
            "tareas_con_cycle_time": 0,
        },
        "tokens_coste": {
            "total": 0,
            "autoria": 0,
            "revision": 0,
            "por_tarea": {},
        },
    }


def add_quality(bucket: dict[str, Any], status: str, review_cycles: int) -> None:
    quality = bucket["calidad"]
    if status == DONE_STATUS:
        quality["done"] += 1
    if status in QUALITY_REJECTED_STATUSES:
        quality["rechazadas"] += 1
    quality["ciclos_revision_total"] += review_cycles


def add_time(bucket: dict[str, Any], lead: int | None, cycle: int | None) -> None:
    time_data = bucket["tiempo"]
    if lead is not None:
        time_data["lead_time_seconds_total"] += lead
        time_data["tareas_con_lead_time"] += 1
    if cycle is not None:
        time_data["cycle_time_seconds_total"] += cycle
        time_data["tareas_con_cycle_time"] += 1


def add_tokens(bucket: dict[str, Any], task_id: str, role: str, tokens: int) -> None:
    if tokens <= 0:
        return
    cost = bucket["tokens_coste"]
    cost["total"] += tokens
    cost[role] += tokens
    per_task = cost["por_tarea"].setdefault(task_id, {"total": 0, "autoria": 0, "revision": 0})
    per_task["total"] += tokens
    per_task[role] += tokens


def finalize_bucket(bucket: dict[str, Any], denominator_tasks: int) -> None:
    quality = bucket["calidad"]
    decisions = quality["done"] + quality["rechazadas"]
    quality["tasa_aceptacion"] = None if decisions == 0 else round(quality["done"] / decisions, 6)
    quality["ciclos_revision_promedio"] = (
        0.0 if denominator_tasks == 0 else round(quality["ciclos_revision_total"] / denominator_tasks, 6)
    )
    time_data = bucket["tiempo"]
    lead_count = time_data["tareas_con_lead_time"]
    cycle_count = time_data["tareas_con_cycle_time"]
    time_data["lead_time_seconds_promedio"] = (
        None if lead_count == 0 else round(time_data["lead_time_seconds_total"] / lead_count, 6)
    )
    time_data["cycle_time_seconds_promedio"] = (
        None if cycle_count == 0 else round(time_data["cycle_time_seconds_total"] / cycle_count, 6)
    )
    cost = bucket["tokens_coste"]
    cost["por_tarea"] = sorted_dict(cost["por_tarea"])


def load_events(path: Path) -> list[dict[str, Any]]:
    return runtime_metrics.read_jsonl(path)


def task_entries_from_index(root: Path) -> dict[str, dict[str, Any]]:
    path = root / "Area_comun/state/TASK_INDEX.json"
    if not path.exists():
        return {}
    data = read_json(path)
    return {
        str(task.get("id")): task
        for task in data.get("tasks", [])
        if isinstance(task, dict) and str(task.get("id") or "")
    }


def task_status_transition(event: dict[str, Any]) -> tuple[str, str, str] | None:
    payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
    transitions = payload.get("transitions") if isinstance(payload.get("transitions"), dict) else {}
    status = transitions.get("task_status")
    if not isinstance(status, dict):
        return None
    task_id = str(payload.get("task_id") or event.get("aggregate_id") or "")
    from_status = str(status.get("from") or "")
    to_status = str(status.get("to") or "")
    if not task_id or not to_status:
        return None
    return task_id, from_status, to_status


def provenance_from_event(event: dict[str, Any]) -> dict[str, Any] | None:
    payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
    candidates = [
        payload.get("provenance_metadata"),
        payload.get("attested_instancing", {}).get("provenance_metadata")
        if isinstance(payload.get("attested_instancing"), dict)
        else None,
        payload.get("provenance"),
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            return candidate
    return None


def worker_id_from_provenance(provenance: dict[str, Any]) -> str | None:
    for key in ("real_author", "author_real", "worker", "worker_id", "peon", "peon_id", "actor_real", "author"):
        value = provenance.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def model_from_provenance(provenance: dict[str, Any]) -> str | None:
    for key in ("model", "llm_model", "llm_preset", "preset"):
        value = provenance.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def collect_tasks(events: list[dict[str, Any]], task_index: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for task_id, index_entry in task_index.items():
        tasks[task_id] = {
            "task_id": task_id,
            "owner": index_entry.get("owner"),
            "maker": index_entry.get("maker") or index_entry.get("owner"),
            "checker": index_entry.get("checker") or index_entry.get("reviewer"),
            "status": index_entry.get("status"),
            "created_at": parse_time(index_entry.get("created_at")),
            "first_in_progress_at": None,
            "done_at": None,
            "review_cycles": 0,
            "actors": set(),
            "provenance": None,
        }

    for event in events:
        transition = task_status_transition(event)
        if not transition:
            continue
        task_id, from_status, to_status = transition
        task = tasks.setdefault(
            task_id,
            {
                "task_id": task_id,
                "owner": None,
                "maker": None,
                "checker": None,
                "status": None,
                "created_at": None,
                "first_in_progress_at": None,
                "done_at": None,
                "review_cycles": 0,
                "actors": set(),
                "provenance": None,
            },
        )
        actor = str(event.get("actor") or "")
        if actor:
            task["actors"].add(actor)
        event_time = parse_time(event.get("ts") or event.get("payload", {}).get("timestamp"))
        if to_status == "in_progress" and task["first_in_progress_at"] is None:
            task["first_in_progress_at"] = event_time
        if to_status == DONE_STATUS:
            task["done_at"] = event_time
        if to_status == "changes_requested" or from_status == "in_review" and to_status == "in_progress":
            task["review_cycles"] += 1
        task["status"] = to_status
        provenance = provenance_from_event(event)
        if provenance:
            task["provenance"] = provenance
    return tasks


def runlog_summaries(runlogs_dir: Path) -> list[dict[str, Any]]:
    if not runlogs_dir.exists():
        return []
    summaries: list[dict[str, Any]] = []
    for path in sorted(runlogs_dir.glob("*.jsonl")):
        summary = runtime_metrics.summarize(path)
        summary["path"] = str(path)
        summaries.append(summary)
    return summaries


def entry_tokens(entry: dict[str, Any]) -> int:
    cost = entry.get("cost")
    if isinstance(cost, dict):
        value = cost.get("tokens")
    else:
        value = cost
    return value if isinstance(value, int) else 0


def runlog_cost_rows(runlogs_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not runlogs_dir.exists():
        return rows
    for path in sorted(runlogs_dir.glob("*.jsonl")):
        for entry in runtime_metrics.read_entries(path):
            tokens = entry_tokens(entry)
            if tokens <= 0:
                continue
            rows.append(
                {
                    "task_id": str(entry.get("task_id") or "none"),
                    "agent": str(entry.get("agent") or entry.get("unit", {}).get("owner") or "none"),
                    "tokens": tokens,
                    "path": str(path),
                }
            )
    return rows


def aggregate(root: Path, events_path: Path, runlogs_dir: Path, include_hashes: bool = False) -> dict[str, Any]:
    before_hashes = pinned_hashes(root) if include_hashes else None
    events = load_events(events_path)
    task_index = task_entries_from_index(root)
    tasks = collect_tasks(events, task_index)
    runlog_data = runlog_summaries(runlogs_dir)
    cost_rows = runlog_cost_rows(runlogs_dir)

    by_agent: dict[str, dict[str, Any]] = {}
    by_worker: dict[str, dict[str, Any]] = {}
    by_task: dict[str, Any] = {}

    for task_id in sorted(tasks):
        task = tasks[task_id]
        maker = str(task.get("maker") or task.get("owner") or "none")
        checker = str(task.get("checker") or "none")
        status = str(task.get("status") or "unknown")
        lead = seconds_between(task.get("created_at"), task.get("done_at"))
        cycle = seconds_between(task.get("first_in_progress_at"), task.get("done_at"))
        review_cycles = int(task.get("review_cycles") or 0)
        task_cost_rows = [row for row in cost_rows if row["task_id"] == task_id]
        tokens = sum(int(row["tokens"]) for row in task_cost_rows)
        author_tokens = sum(int(row["tokens"]) for row in task_cost_rows if row["agent"] != checker)
        review_tokens = sum(int(row["tokens"]) for row in task_cost_rows if row["agent"] == checker)
        provenance = task.get("provenance") if isinstance(task.get("provenance"), dict) else {}
        worker = worker_id_from_provenance(provenance) if provenance else None
        model = model_from_provenance(provenance) if provenance else None

        by_task[task_id] = {
            "owner": task.get("owner"),
            "maker": maker,
            "checker": None if checker == "none" else checker,
            "status": status,
            "review_cycles": review_cycles,
            "lead_time_seconds": lead,
            "cycle_time_seconds": cycle,
            "tokens_coste": {"total": tokens, "autoria": author_tokens, "revision": review_tokens},
            "peon": worker,
            "modelo": model,
        }

        maker_bucket = by_agent.setdefault(maker, agent_bucket())
        add_quality(maker_bucket, status, review_cycles)
        add_time(maker_bucket, lead, cycle)
        add_tokens(maker_bucket, task_id, "autoria", author_tokens)

        if checker != "none":
            checker_bucket = by_agent.setdefault(checker, agent_bucket())
            if status in REVIEW_STATUSES or review_tokens:
                add_tokens(checker_bucket, task_id, "revision", review_tokens)

        if worker:
            worker_bucket = by_worker.setdefault(worker, agent_bucket())
            add_quality(worker_bucket, status, review_cycles)
            add_time(worker_bucket, lead, cycle)
            add_tokens(worker_bucket, task_id, "autoria", author_tokens)
            by_worker[worker]["modelo"] = model

    task_count_by_agent: dict[str, int] = {}
    task_count_by_worker: dict[str, int] = {}
    for task in tasks.values():
        maker = str(task.get("maker") or task.get("owner") or "none")
        task_count_by_agent[maker] = task_count_by_agent.get(maker, 0) + 1
        provenance = task.get("provenance") if isinstance(task.get("provenance"), dict) else {}
        worker = worker_id_from_provenance(provenance) if provenance else None
        if worker:
            task_count_by_worker[worker] = task_count_by_worker.get(worker, 0) + 1

    for agent, bucket in by_agent.items():
        finalize_bucket(bucket, task_count_by_agent.get(agent, 0))
    for worker, bucket in by_worker.items():
        finalize_bucket(bucket, task_count_by_worker.get(worker, 0))

    result: dict[str, Any] = {
        "por_agente": sorted_dict(by_agent),
        "por_peon": sorted_dict(by_worker),
        "por_tarea": sorted_dict(by_task),
        "fuentes": {
            "events": str(events_path),
            "runlogs": str(runlogs_dir),
            "runlog_files": [summary["path"] for summary in runlog_data],
        },
        "read_only": {"checked": include_hashes},
    }
    if include_hashes:
        after_hashes = pinned_hashes(root)
        result["read_only"]["sha256_before"] = before_hashes
        result["read_only"]["sha256_after"] = after_hashes
        result["read_only"]["byte_identical"] = before_hashes == after_hashes
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate read-only per-agent protocol metrics.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--events", default=None)
    parser.add_argument("--runlogs", default=None)
    parser.add_argument("--check-readonly", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    events_path = Path(args.events).resolve() if args.events else root / "runtime/state/events.jsonl"
    runlogs_dir = Path(args.runlogs).resolve() if args.runlogs else root / "runtime/runs"
    result = aggregate(root, events_path, runlogs_dir, include_hashes=args.check_readonly)
    print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0 if result.get("read_only", {}).get("byte_identical", True) is not False else 2


if __name__ == "__main__":
    raise SystemExit(main())
