#!/usr/bin/env python3
"""Prune hot protocol state into archives when measured thresholds are exceeded."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from measure_context_cost import measure
except ImportError:  # pragma: no cover
    from .measure_context_cost import measure

try:
    from runtime.protocol_replay import protocol_state_enforcement_enabled, protocol_state_drift
    from runtime.submit_intent import submit_intents
except ImportError:  # pragma: no cover
    from ..runtime.protocol_replay import protocol_state_enforcement_enabled, protocol_state_drift
    from ..runtime.submit_intent import submit_intents


DEFAULT_CONFIG = {
    "enabled": True,
    "cold_start_tokens_hard": 20000,
    "done_ratio_hard": 85,
    "released_ratio_hard": 90,
    "recent_done_tasks": 2,
    "recent_released_claims": 4,
    "mailbox_keep_recent": 8,
    # 0 (o ausente) preserva el comportamiento previo: el prune NO condensa next_actions.
    # Un valor > 0 conserva esas N entradas mas recientes y condensa el resto en un centinela.
    "recent_next_actions": 0,
}


STATUS_FIELD_RE = re.compile(r"(?m)^status:\s*.*$")
FRONTMATTER_FIELD_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$")

# Centinela determinista para next_actions condensadas (mismo patron que la poda manual historica).
NEXT_ACTIONS_SENTINEL_MARK = "[HISTORICO PODADO]"
NEXT_ACTIONS_SENTINEL_RE = re.compile(r"\[HISTORICO PODADO\]\s*(\d+)")


@dataclass(frozen=True)
class Assessment:
    due: bool
    reasons: list[str]
    before_tokens: int


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=True) + "\n", encoding="utf-8")


def archive_removed_entries(
    archive_path: Path,
    hot_entries: list[Any],
    ids: set[str] | list[str],
    field: str,
    id_field: str,
    actor: str,
) -> int:
    """Persist entries removed from the governed hot state into the (ungoverned,
    convenience-mirror) *_ARCHIVE.json file, so their ids remain discoverable
    (e.g. by validate_collaboration_state's commit_trailers check) after a
    submit_intent-mode protocol_prune removes them from the live TASK_INDEX/CLAIMS.
    This file is NOT part of PROTOCOL_STATE_PATHS / drift enforcement (DECISION-0022
    only covers TASK_INDEX.json/PROJECT_STATE.json/CLAIMS.json); writing it directly
    here is the same convention apply_prune_direct already used for non-runtime
    instances, just also applied in submit_intent (runtime-authoritative) mode.
    """
    ids_set = {str(item) for item in ids if str(item)}
    if not ids_set:
        return 0
    to_archive = [
        entry
        for entry in hot_entries
        if isinstance(entry, dict) and str(entry.get(id_field) or "") in ids_set
    ]
    if not to_archive:
        return 0
    archive_doc = read_json(archive_path)
    existing_ids = {str(entry.get(id_field)) for entry in archive_doc.get(field, []) if isinstance(entry, dict)}
    archived_count = 0
    for entry in to_archive:
        entry_id = str(entry.get(id_field) or "")
        if entry_id and entry_id not in existing_ids:
            archive_doc.setdefault(field, []).append(entry)
            existing_ids.add(entry_id)
            archived_count += 1
    if archived_count:
        archive_doc["updated_by"] = actor
        write_json(archive_path, archive_doc)
    return archived_count


def maintenance_config(root: Path) -> dict[str, Any]:
    config = read_json(root / "protocol.config.json")
    maintenance = dict(DEFAULT_CONFIG)
    maintenance.update(config.get("maintenance") or {})
    return maintenance


def assess(root: Path) -> Assessment:
    cfg = maintenance_config(root)
    measured = measure(root)
    cold_tokens = int(measured["cold_start"]["total_tokens"])
    task_weight = measured["dead_weight"]["tasks"]
    claim_weight = measured["dead_weight"]["claims"]
    done_ratio = float(task_weight["done_percent"])
    released_ratio = float(claim_weight["released_percent"])
    done_count = int(task_weight["done"])
    released_count = int(claim_weight["released"])
    reasons: list[str] = []
    if cfg.get("enabled") is False:
        return Assessment(False, ["maintenance disabled"], cold_tokens)
    if cold_tokens >= int(cfg["cold_start_tokens_hard"]):
        reasons.append(f"cold_start_tokens {cold_tokens} >= {cfg['cold_start_tokens_hard']}")
    if done_count > int(cfg["recent_done_tasks"]) and done_ratio >= float(cfg["done_ratio_hard"]):
        reasons.append(f"done_ratio {done_ratio} >= {cfg['done_ratio_hard']}")
    if released_count > int(cfg["recent_released_claims"]) and released_ratio >= float(cfg["released_ratio_hard"]):
        reasons.append(f"released_ratio {released_ratio} >= {cfg['released_ratio_hard']}")
    return Assessment(bool(reasons), reasons, cold_tokens)


def archive_entries(
    hot_doc: dict[str, Any],
    archive_doc: dict[str, Any],
    field: str,
    id_field: str,
    terminal_status: str,
    keep_recent: int,
) -> tuple[int, dict[str, Any], dict[str, Any]]:
    hot_entries = [entry for entry in hot_doc.get(field, []) if isinstance(entry, dict)]
    terminal = [entry for entry in hot_entries if str(entry.get("status", "")).lower() == terminal_status]
    keep_ids = {str(entry.get(id_field)) for entry in terminal[-keep_recent:]} if keep_recent > 0 else set()
    to_archive = [entry for entry in terminal if str(entry.get(id_field)) not in keep_ids]
    archive_ids = {str(entry.get(id_field)) for entry in archive_doc.get(field, []) if isinstance(entry, dict)}

    hot_doc[field] = [
        entry
        for entry in hot_entries
        if str(entry.get("status", "")).lower() != terminal_status or str(entry.get(id_field)) in keep_ids
    ]
    for entry in to_archive:
        if str(entry.get(id_field)) not in archive_ids:
            archive_doc.setdefault(field, []).append(entry)
            archive_ids.add(str(entry.get(id_field)))
    return len(to_archive), hot_doc, archive_doc


def terminal_ids(entries: list[Any], id_field: str, terminal_status: str, keep_recent: int) -> list[str]:
    hot_entries = [entry for entry in entries if isinstance(entry, dict)]
    terminal = [entry for entry in hot_entries if str(entry.get("status", "")).lower() == terminal_status]
    keep_ids = {str(entry.get(id_field)) for entry in terminal[-keep_recent:]} if keep_recent > 0 else set()
    return [
        str(entry.get(id_field))
        for entry in terminal
        if str(entry.get(id_field) or "") and str(entry.get(id_field)) not in keep_ids
    ]


def condense_next_actions(state: dict[str, Any], keep_recent: int) -> int:
    """Condensa next_actions historicas en un centinela determinista, idempotente.

    Conserva las `keep_recent` entradas regulares mas recientes y reemplaza el resto por UNA
    entrada centinela que acumula el conteo de todo lo condensado. Centinelas previos se
    preservan (fusionados en el conteo). Con keep_recent <= 0 no hace nada. Una segunda corrida
    no re-condensa ni duplica el centinela.
    """
    if keep_recent <= 0:
        return 0
    items = state.get("next_actions", [])
    if not isinstance(items, list):
        return 0
    str_items = [entry for entry in items if isinstance(entry, str)]
    other = [entry for entry in items if not isinstance(entry, str)]
    sentinels = [entry for entry in str_items if NEXT_ACTIONS_SENTINEL_MARK in entry]
    regulars = [entry for entry in str_items if NEXT_ACTIONS_SENTINEL_MARK not in entry]
    if len(regulars) <= keep_recent:
        return 0
    to_condense = regulars[:-keep_recent]
    kept = regulars[-keep_recent:]
    prior = 0
    for entry in sentinels:
        match = NEXT_ACTIONS_SENTINEL_RE.search(entry)
        if match:
            prior += int(match.group(1))
    total = prior + len(to_condense)
    sentinel = (
        f"{NEXT_ACTIONS_SENTINEL_MARK} {total} next_actions historicas condensadas por el prune "
        "(DECISION-0014); trazabilidad en git history + memoria de Claude."
    )
    state["next_actions"] = [sentinel] + kept + other
    return len(to_condense)


def prune_project_state(root: Path, keep_recent: int, keep_next_actions: int = 0) -> tuple[int, int]:
    path = root / "Area_comun/state/PROJECT_STATE.json"
    state = read_json(path)
    tasks = [task for task in state.get("active_tasks", []) if isinstance(task, dict)]
    done = [task for task in tasks if str(task.get("status", "")).lower() == "done"]
    keep_ids = {str(task.get("id")) for task in done[-keep_recent:]} if keep_recent > 0 else set()
    kept = [
        task
        for task in tasks
        if str(task.get("status", "")).lower() != "done" or str(task.get("id")) in keep_ids
    ]
    removed = len(tasks) - len(kept)
    state["active_tasks"] = kept
    condensed = condense_next_actions(state, keep_next_actions)
    state["updated_by"] = "Codex"
    write_json(path, state)
    return removed, condensed


def condensed_next_actions(state: dict[str, Any], keep_next_actions: int) -> tuple[int, list[Any] | None]:
    working = deepcopy(state)
    condensed = condense_next_actions(working, keep_next_actions)
    if condensed <= 0:
        return 0, None
    values = working.get("next_actions")
    return condensed, values if isinstance(values, list) else []


def prune_mailbox(root: Path, keep_recent: int) -> int:
    mailbox = root / "Area_comun/mailbox"
    open_dir = mailbox / "open"
    answered = mailbox / "answered"
    archived = mailbox / "archived"
    open_dir.mkdir(parents=True, exist_ok=True)
    archived.mkdir(parents=True, exist_ok=True)
    messages = sorted(answered.glob("MSG-*.md"), key=lambda path: path.name)
    eligible: list[Path] = []
    for path in messages:
        if requires_unresolved_response(path):
            set_mailbox_status(path, "open")
            target = open_dir / path.name
            if not target.exists():
                shutil.move(str(path), str(target))
            continue
        eligible.append(path)
    move = eligible[:-keep_recent] if keep_recent > 0 else eligible
    for path in move:
        target = archived / path.name
        if not target.exists():
            set_mailbox_status(path, "archived")
            shutil.move(str(path), str(target))
    return len(move)


def set_mailbox_status(path: Path, status: str) -> None:
    content = path.read_text(encoding="utf-8-sig")
    replacement = f"status: {status}"
    if STATUS_FIELD_RE.search(content):
        updated = STATUS_FIELD_RE.sub(replacement, content, count=1)
    elif content.startswith("---\n"):
        updated = content.replace("---\n", f"---\n{replacement}\n", 1)
    else:
        updated = f"---\n{replacement}\n---\n\n{content}"
    if updated != content:
        path.write_text(updated, encoding="utf-8")


def markdown_fields(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8-sig")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = FRONTMATTER_FIELD_RE.match(line)
        if match:
            key, value = match.groups()
            fields[key.strip().lower()] = value.strip().strip("\"'")
    return fields


def is_truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"true", "yes", "1"}


def requires_unresolved_response(path: Path) -> bool:
    fields = markdown_fields(path)
    if not is_truthy(fields.get("requires_response")):
        return False
    status = str(fields.get("status") or "").strip().lower()
    return status not in {"answered", "archived", "closed", "resolved", "done"}


def apply_prune(
    root: Path,
    *,
    actor_id: str | None = None,
    timestamp: str | None = None,
    commit: str | None = None,
) -> dict[str, Any]:
    cfg = maintenance_config(root)
    config = read_json(root / "protocol.config.json")
    if protocol_state_enforcement_enabled(config):
        return apply_prune_via_submit_intent(root, cfg, actor_id=actor_id, timestamp=timestamp, commit=commit)

    return apply_prune_direct(root, cfg)


def apply_prune_direct(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    state_dir = root / "Area_comun/state"
    task_hot_path = state_dir / "TASK_INDEX.json"
    task_archive_path = state_dir / "TASK_INDEX_ARCHIVE.json"
    claims_hot_path = state_dir / "CLAIMS.json"
    claims_archive_path = state_dir / "CLAIMS_ARCHIVE.json"

    before = measure(root)["cold_start"]["total_tokens"]

    tasks_moved, task_hot, task_archive = archive_entries(
        read_json(task_hot_path),
        read_json(task_archive_path),
        "tasks",
        "id",
        "done",
        int(cfg["recent_done_tasks"]),
    )
    claims_moved, claims_hot, claims_archive = archive_entries(
        read_json(claims_hot_path),
        read_json(claims_archive_path),
        "claims",
        "claim_id",
        "released",
        int(cfg["recent_released_claims"]),
    )
    task_hot["updated_by"] = "Codex"
    claims_hot["updated_by"] = "Codex"
    task_archive["updated_by"] = "Codex"
    claims_archive["updated_by"] = "Codex"
    write_json(task_hot_path, task_hot)
    write_json(task_archive_path, task_archive)
    write_json(claims_hot_path, claims_hot)
    write_json(claims_archive_path, claims_archive)
    project_removed, next_actions_condensed = prune_project_state(
        root,
        int(cfg["recent_done_tasks"]),
        int(cfg.get("recent_next_actions", 0)),
    )
    mailbox_moved = prune_mailbox(root, int(cfg["mailbox_keep_recent"]))

    after = measure(root)["cold_start"]["total_tokens"]
    return {
        "tasks_archived": tasks_moved,
        "claims_archived": claims_moved,
        "project_state_done_removed": project_removed,
        "next_actions_condensed": next_actions_condensed,
        "mailbox_archived": mailbox_moved,
        "before_tokens": before,
        "after_tokens": after,
        "recovered_tokens": before - after,
    }


def default_actor_id(root: Path) -> str:
    config = read_json(root / "protocol.config.json")
    roles = config.get("agent_roles") if isinstance(config.get("agent_roles"), dict) else {}
    return str(roles.get("architect") or "Claude")


def default_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_commit(root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 and completed.stdout.strip() else "unknown"


def claim_intent(claim_id: str, task_id: str, actor_id: str, timestamp: str, scope: list[str]) -> dict[str, Any]:
    return {
        "claim": {
            "op": "acquire",
            "idempotency_key": f"prune-state:{timestamp}:claim-acquire",
            "claim": {
                "claim_id": claim_id,
                "task_id": task_id,
                "owner": actor_id,
                "status": "active",
                "started_at": timestamp,
                "updated_at": timestamp,
                "expires_at": timestamp.split("T", 1)[0],
                "notes": "Maintenance prune via submit_intent under event_state.enforce.",
                "scope": scope,
            },
        }
    }


def claim_release_intent(claim_id: str, timestamp: str) -> dict[str, Any]:
    return {
        "claim": {
            "op": "release",
            "claim_id": claim_id,
            "idempotency_key": f"prune-state:{timestamp}:claim-release",
        }
    }


def apply_prune_via_submit_intent(
    root: Path,
    cfg: dict[str, Any],
    *,
    actor_id: str | None = None,
    timestamp: str | None = None,
    commit: str | None = None,
) -> dict[str, Any]:
    actor = str(actor_id or default_actor_id(root)).strip()
    ts = str(timestamp or default_timestamp()).strip()
    commit_ref = str(commit or current_commit(root)).strip()
    state_dir = root / "Area_comun/state"
    before = measure(root)["cold_start"]["total_tokens"]
    task_hot = read_json(state_dir / "TASK_INDEX.json")
    claims_hot = read_json(state_dir / "CLAIMS.json")
    project = read_json(state_dir / "PROJECT_STATE.json")

    task_ids = terminal_ids(task_hot.get("tasks") or [], "id", "done", int(cfg["recent_done_tasks"]))
    active_task_ids = terminal_ids(project.get("active_tasks") or [], "id", "done", int(cfg["recent_done_tasks"]))
    # The submit_intent transaction leaves its own maintenance claim as released after pruning.
    # Keep one fewer pre-existing released claim so the post-transaction hot set still satisfies
    # recent_released_claims and a second --check is not immediately due again.
    keep_released_before_maintenance = max(int(cfg["recent_released_claims"]) - 1, 0)
    claim_ids = terminal_ids(
        claims_hot.get("claims") or [],
        "claim_id",
        "released",
        keep_released_before_maintenance,
    )
    next_actions_condensed, next_actions = condensed_next_actions(project, int(cfg.get("recent_next_actions", 0)))

    scopes = ["Area_comun/state/CLAIMS.json"]
    if task_ids:
        scopes.append("Area_comun/state/TASK_INDEX.json")
    if active_task_ids or next_actions is not None:
        scopes.append("Area_comun/state/PROJECT_STATE.json")
    if claim_ids:
        scopes.append("Area_comun/state/CLAIMS.json")
    scopes = list(dict.fromkeys(scopes))

    intents: list[dict[str, Any]] = []
    if next_actions is not None:
        intents.append(
            {
                "project_narrative": {
                    "set": {"next_actions": next_actions},
                    "idempotency_key": f"prune-state:{ts}:project-narrative",
                }
            }
        )
    if task_ids or active_task_ids or claim_ids:
        intents.append(
            {
                "protocol_prune": {
                    "task_ids": task_ids,
                    "active_task_ids": active_task_ids,
                    "claim_ids": claim_ids,
                    "idempotency_key": f"prune-state:{ts}:protocol-prune",
                }
            }
        )

    submit_result: dict[str, Any] | None = None
    if intents:
        task_id = "MAINTENANCE-PRUNE"
        actor_slug = re.sub(r"[^a-z0-9]+", "-", actor.lower()).strip("-") or "actor"
        claim_id = f"CLAIM-{ts.replace(':', '').replace('-', '').replace('T', '-').replace('Z', '')}-prune-{actor_slug}"
        transaction = [
            claim_intent(claim_id, task_id, actor, ts, scopes),
            *intents,
            claim_release_intent(claim_id, ts),
        ]
        submit_result = submit_intents(
            root,
            actor,
            transaction,
            timestamp=ts,
            commit=commit_ref,
            transaction_key=f"prune-state:{ts}:tx",
        )
        if submit_result is not None and submit_result.get("applied"):
            archive_removed_entries(
                state_dir / "TASK_INDEX_ARCHIVE.json",
                task_hot.get("tasks") or [],
                task_ids,
                "tasks",
                "id",
                actor,
            )
            archive_removed_entries(
                state_dir / "CLAIMS_ARCHIVE.json",
                claims_hot.get("claims") or [],
                claim_ids,
                "claims",
                "claim_id",
                actor,
            )

    after = measure(root)["cold_start"]["total_tokens"]
    drift = protocol_state_drift(root)
    return {
        "mode": "submit_intent",
        "actor_id": actor,
        "tasks_archived": len(task_ids),
        "claims_archived": len(claim_ids),
        "project_state_done_removed": len(active_task_ids),
        "next_actions_condensed": next_actions_condensed,
        "mailbox_archived": 0,
        "before_tokens": before,
        "after_tokens": after,
        "recovered_tokens": before - after,
        "drift": {"has_drift": drift.get("has_drift"), "up_to_seq": drift.get("up_to_seq")},
        "transaction": (submit_result or {}).get("transaction"),
    }


def run_check(root: Path) -> int:
    assessment = assess(root)
    if not assessment.due:
        print(f"OK: prune not due (cold_start_tokens={assessment.before_tokens}).")
        return 0
    print("PRUNE DUE:")
    for reason in assessment.reasons:
        print(f"- {reason}")
    print("Run: python scripts/prune_state.py --root . --apply")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check or apply systematic protocol state pruning.")
    parser.add_argument("--root", default=".", help="Repository or instance root.")
    parser.add_argument("--actor-id", help="Actor id used for submit_intent mode; defaults to configured architect.")
    parser.add_argument("--timestamp", help="Timestamp used for submit_intent mode.")
    parser.add_argument("--commit", help="Commit recorded for submit_intent mode.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Read-only threshold check.")
    mode.add_argument("--apply", action="store_true", help="Archive terminal hot state entries.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if args.check:
        return run_check(root)
    result = apply_prune(root, actor_id=args.actor_id, timestamp=args.timestamp, commit=args.commit)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
