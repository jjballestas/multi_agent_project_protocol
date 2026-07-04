#!/usr/bin/env python3
"""Golden checks for the governed skill loader."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skills.loader import load_skills


PINNED_HUB_PATHS = [
    "runtime/eventlog.py",
    "scripts/validate_collaboration_state.py",
    "protocol.config.json",
    "Area_comun/decisions/DECISION-0069-instancing-attestation-ceremony.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    ledger_paths = [
        "Area_comun/state/CLAIMS.json",
        "Area_comun/state/PROJECT_STATE.json",
        "Area_comun/state/TASK_INDEX.json",
        "runtime/state/events.jsonl",
        "runtime/state/snapshot.json",
    ]
    watched = [root / item for item in ledger_paths + PINNED_HUB_PATHS]
    missing = [str(path.relative_to(root)) for path in watched if not path.exists()]
    if missing:
        raise AssertionError(f"missing watched paths: {missing}")

    before = {path.relative_to(root).as_posix(): sha256(path) for path in watched}

    registry = json.loads((root / "skills" / "skills.config.json").read_text(encoding="utf-8-sig"))
    matches = [entry for entry in registry["skills"] if entry.get("id") == "delegate-to-worker"]
    if len(matches) != 1:
        raise AssertionError("delegate-to-worker must be registered exactly once")
    if matches[0].get("enabled") is not False:
        raise AssertionError("delegate-to-worker must be off by default")
    boundary = matches[0].get("trust_boundary") or {}
    if boundary != {"read_only": True, "grants_no_authority": True, "persists_outputs": False}:
        raise AssertionError("delegate-to-worker must grant no authority and persist no output")

    loaded_default = load_skills(root)
    if any(item["id"] == "delegate-to-worker" for item in loaded_default["skills"]):
        raise AssertionError("delegate-to-worker must not load from the default disabled registry")

    enabled_registry = dict(registry)
    enabled_entries = []
    for entry in registry["skills"]:
        cloned = dict(entry)
        if cloned.get("id") == "delegate-to-worker":
            cloned["enabled"] = True
        enabled_entries.append(cloned)
    enabled_registry["skills"] = enabled_entries

    with tempfile.TemporaryDirectory(prefix="skill-loader-") as tmp:
        temp_registry = Path(tmp) / "skills.config.json"
        temp_registry.write_text(json.dumps(enabled_registry, indent=2) + "\n", encoding="utf-8")
        loaded_enabled = load_skills(root, temp_registry)

    loaded_ids = [item["id"] for item in loaded_enabled["skills"]]
    if loaded_ids != ["delegate-to-worker"]:
        raise AssertionError(f"unexpected loaded skills: {loaded_ids}")
    skill = loaded_enabled["skills"][0]
    if skill["neutral_core"] is not True or skill["path"] != "skills/delegate-to-worker.skill.md":
        raise AssertionError("delegate-to-worker loaded with unexpected metadata")
    for required in ["TASK-0213", "TASK-0214", "runtime/submit_intent.py", "keyless"]:
        if required not in skill["procedure"]:
            raise AssertionError(f"delegate-to-worker procedure missing {required}")

    after = {path.relative_to(root).as_posix(): sha256(path) for path in watched}
    if before != after:
        changed = [path for path, digest in before.items() if after.get(path) != digest]
        raise AssertionError(f"loader is not read-only; changed hashes: {changed}")

    print(json.dumps({"ok": True, "loaded": loaded_ids, "byte_identical": True}, indent=2))


if __name__ == "__main__":
    main()
