#!/usr/bin/env python3
"""Golden cases for SPEC-0096 / DECISION-0061."""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skills.loader import SkillLoaderError, load_skills


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def state_fingerprint(root: Path = ROOT) -> dict[str, str]:
    paths = [
        root / "runtime" / "state" / "events.jsonl",
        root / "runtime" / "state" / "snapshot.json",
        root / "Area_comun" / "state" / "CLAIMS.json",
        root / "Area_comun" / "state" / "PROJECT_STATE.json",
        root / "Area_comun" / "state" / "TASK_INDEX.json",
    ]
    return {path.relative_to(root).as_posix(): file_hash(path) for path in paths}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def write_skill(
    path: Path,
    skill_id: str,
    title: str,
    version: str,
    body: str,
    *,
    neutral_core: bool = True,
    profile: str | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = [
        "---",
        f"skill_id: {skill_id}",
        f"title: {title}",
        f"version: {version}",
    ]
    if neutral_core:
        frontmatter.append("neutral_core: true")
    else:
        frontmatter.append(f"profile: {profile}")
        frontmatter.append("neutral_core: false")
    frontmatter.append("---")
    path.write_text("\n".join(frontmatter) + f"\n\n{body}\n", encoding="utf-8")


def fixture_root() -> Path:
    temp = Path(tempfile.mkdtemp(prefix="skills-loader-cases-"))
    shutil.copy2(ROOT / "protocol.config.json", temp / "protocol.config.json")
    return temp


def registry_entry(skill_id: str, path: str, *, enabled: bool, title: str | None = None) -> dict[str, Any]:
    return {
        "id": skill_id,
        "title": title or skill_id.replace("-", " ").title(),
        "neutral_core": True,
        "path": path,
        "version": "1.0.0",
        "enabled": enabled,
        "trust_boundary": {
            "read_only": True,
            "grants_no_authority": True,
            "persists_outputs": False,
        },
    }


def profile_registry_entry(skill_id: str, path: str, *, title: str) -> dict[str, Any]:
    entry = registry_entry(skill_id, path, enabled=True, title=title)
    entry["neutral_core"] = False
    entry["profile"] = "financiero_presupuesto"
    return entry


def case_ac1_registry_outside_protocol_config() -> dict[str, Any]:
    protocol_config = json.loads((ROOT / "protocol.config.json").read_text(encoding="utf-8-sig"))
    registry = json.loads((ROOT / "skills" / "skills.config.json").read_text(encoding="utf-8"))
    assert "skills" not in protocol_config
    assert registry["schema_version"] == "skills.config.v1"
    assert all(item.get("enabled") is False for item in registry["skills"])
    return {"case": "AC1-registry-outside-protocol-config", "status": "pass"}


def case_ac2_deterministic_enabled_and_disabled() -> dict[str, Any]:
    root = fixture_root()
    try:
        write_skill(root / "skills" / "first.skill.md", "first", "First", "1.0.0", "# First\n\nRead one.")
        write_skill(root / "skills" / "second.skill.md", "second", "Second", "1.0.0", "# Second\n\nRead two.")
        write_json(
            root / "skills" / "skills.config.json",
            {
                "schema_version": "skills.config.v1",
                "skills": [
                    registry_entry("second", "skills/second.skill.md", enabled=True, title="Second"),
                    registry_entry("first", "skills/first.skill.md", enabled=True, title="First"),
                ],
            },
        )
        first = load_skills(root)
        second = load_skills(root)
        assert first == second
        assert [item["id"] for item in first["skills"]] == ["first", "second"]

        disabled = json.loads((root / "skills" / "skills.config.json").read_text(encoding="utf-8"))
        for item in disabled["skills"]:
            item["enabled"] = False
        write_json(root / "skills" / "skills.config.json", disabled)
        assert load_skills(root)["skills"] == []
        return {"case": "AC2-deterministic-read-only-loader", "status": "pass", "loaded": 2}
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_ac3_no_authority_no_writes() -> dict[str, Any]:
    forbidden_modules = {
        "runtime.eventlog",
        "runtime.ledger_ops",
        "runtime.submit_intent",
        "runtime.apply",
        "runtime.protocol_replay",
    }
    forbidden_names = {"EventWriter", "submit_intent", "apply_turn", "atomic_append_jsonl"}
    findings: list[str] = []
    for path in sorted((ROOT / "skills").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden_modules or alias.name.startswith("runtime."):
                        findings.append(f"{path.relative_to(ROOT)} imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module in forbidden_modules or module.startswith("runtime."):
                    findings.append(f"{path.relative_to(ROOT)} imports {module}")
                for alias in node.names:
                    if alias.name in forbidden_names:
                        findings.append(f"{path.relative_to(ROOT)} imports {alias.name}")
    assert not findings, findings
    before = state_fingerprint()
    _ = load_skills(ROOT)
    after = state_fingerprint()
    assert before == after
    return {"case": "AC3-no-authority-no-writes", "status": "pass"}


def case_ac4_domain_content_rejected_in_core() -> dict[str, Any]:
    root = fixture_root()
    try:
        write_skill(
            root / "skills" / "domain-content.skill.md",
            "domain-content",
            "Domain Content",
            "1.0.0",
            "# Procedure\n\nThis core procedure mentions trading.",
        )
        write_json(
            root / "skills" / "skills.config.json",
            {
                "schema_version": "skills.config.v1",
                "skills": [registry_entry("domain-content", "skills/domain-content.skill.md", enabled=True, title="Domain Content")],
            },
        )
        try:
            load_skills(root)
        except SkillLoaderError as exc:
            assert "domain term rejected" in str(exc)
            return {"case": "AC4-domain-content-in-core-rejected", "status": "pass"}
        raise AssertionError("domain content in core skill was not rejected")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_ac5_fail_closed_missing_and_malformed() -> dict[str, Any]:
    root = fixture_root()
    try:
        assert load_skills(root)["skills"] == []
        write_json(
            root / "skills" / "skills.config.json",
            {
                "schema_version": "skills.config.v1",
                "skills": [
                    {
                        "id": "malformed",
                        "title": "Malformed",
                        "neutral_core": True,
                        "version": "1.0.0",
                        "enabled": True,
                        "trust_boundary": {
                            "read_only": True,
                            "grants_no_authority": True,
                            "persists_outputs": False,
                        },
                    }
                ],
            },
        )
        try:
            load_skills(root)
        except SkillLoaderError as exc:
            assert "missing required field: path" in str(exc)
            return {"case": "AC5-fail-closed-missing-and-malformed", "status": "pass"}
        raise AssertionError("malformed enabled skill was not rejected")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_ac6_profile_skills_load_under_profile() -> dict[str, Any]:
    registry = json.loads((ROOT / "skills" / "skills.config.json").read_text(encoding="utf-8"))
    profile_ids = {"ddl-conventions", "business-rule-vs-legacy", "migration-verification"}
    configured = {item["id"]: item for item in registry["skills"] if item.get("id") in profile_ids}
    assert set(configured) == profile_ids
    assert all(item.get("enabled") is False for item in configured.values())
    assert all(item.get("neutral_core") is False for item in configured.values())
    assert all(item.get("profile") == "financiero_presupuesto" for item in configured.values())

    patched = json.loads(json.dumps(registry))
    patched["skills"] = [item for item in patched["skills"] if item.get("id") in profile_ids]
    for item in patched["skills"]:
        item["enabled"] = True

    root = fixture_root()
    try:
        shutil.copytree(ROOT / "profiles" / "financiero_presupuesto", root / "profiles" / "financiero_presupuesto")
        write_json(root / "skills" / "skills.config.json", patched)

        first = load_skills(root)
        second = load_skills(root)
        assert first == second
        loaded = {item["id"]: item for item in first["skills"]}
        assert set(loaded) == profile_ids
        for skill_id, item in loaded.items():
            assert item["profile"] == "financiero_presupuesto"
            assert item["neutral_core"] is False
            assert item["path"].startswith("profiles/financiero_presupuesto/skills/")
            assert item["procedure"]
            assert configured[skill_id]["path"] == item["path"]
        return {"case": "AC6-profile-skills-load-under-profile", "status": "pass", "loaded": 3}
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_ac7_session_watchdogs_registered_neutral_and_exported() -> dict[str, Any]:
    registry = json.loads((ROOT / "skills" / "skills.config.json").read_text(encoding="utf-8"))
    entries = {item["id"]: item for item in registry["skills"]}
    watchdog = entries["session-watchdogs"]
    assert watchdog["enabled"] is False
    assert watchdog["neutral_core"] is True
    assert watchdog["path"] == "skills/session-watchdogs.skill.md"
    assert watchdog["trust_boundary"] == {
        "read_only": True,
        "grants_no_authority": True,
        "persists_outputs": False,
    }

    body = (ROOT / watchdog["path"]).read_text(encoding="utf-8")
    forbidden_literals = [
        "multi_agent_project_protocol",
        "Arquitecto",
        "Codex",
        "Analista",
        "Nova",
        "Budget",
        "/d/Agentes",
        "D:/Agentes",
    ]
    for literal in forbidden_literals:
        assert literal not in body
    for placeholder in [
        "<WORKSPACE_ROOT>",
        "<MAILBOX_OPEN_DIR>",
        "<STATE_DIR>",
        "<RUNTIME_TMP_DIR>",
        "<WORKER_IDS>",
    ]:
        assert placeholder in body

    root = fixture_root()
    try:
        (root / "skills").mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "skills" / "loader.py", root / "skills" / "loader.py")
        shutil.copy2(ROOT / watchdog["path"], root / watchdog["path"])
        patched = {"schema_version": "skills.config.v1", "skills": [json.loads(json.dumps(watchdog))]}
        patched["skills"][0]["enabled"] = True
        write_json(root / "skills" / "skills.config.json", patched)
        loaded = load_skills(root)
        assert [item["id"] for item in loaded["skills"]] == ["session-watchdogs"]
        return {"case": "AC7-session-watchdogs-registered-neutral-and-loads", "status": "pass"}
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    cases = [
        case_ac1_registry_outside_protocol_config(),
        case_ac2_deterministic_enabled_and_disabled(),
        case_ac3_no_authority_no_writes(),
        case_ac4_domain_content_rejected_in_core(),
        case_ac5_fail_closed_missing_and_malformed(),
        case_ac6_profile_skills_load_under_profile(),
        case_ac7_session_watchdogs_registered_neutral_and_exported(),
    ]
    print(json.dumps({"schema_version": "skills_loader_cases.v1", "cases": cases}, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
