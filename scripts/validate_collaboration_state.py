#!/usr/bin/env python3
"""Validate a multi-agent protocol instance.

This is the cross-platform counterpart to ``validate_collaboration_state.ps1``.
It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from runtime.eventlog import EventLogError, assert_snapshot_matches, runtime_state_has_content
from runtime.protocol_replay import drift_paths, event_state_enabled, protocol_state_drift, protocol_state_enforcement_enabled


VALID_CLAIM_STATUSES = {"active", "released", "blocked"}
REVIEWED_TASK_STATUSES = {"in_review", "review_approved", "qa_pending", "architect_review", "done"}
IMPLEMENTABLE_TASK_TYPES = {
    "implementation",
    "refactor",
    "integration",
    "migration",
    "security",
    "release",
}
LIGHTWEIGHT_TASK_TYPES = {"discovery", "analysis", "review", "documentation", "triage"}
IMPLEMENTABLE_SDD_STATUSES = {
    "ready",
    "claimed",
    "in_progress",
    "in_review",
    "changes_requested",
    "review_approved",
    "qa_pending",
    "qa_failed",
    "architect_review",
    "done",
}
FULL_SDD_FIELDS = [
    "spec_id",
    "execution_pipeline",
    "acceptance_criteria",
    "linked_decisions",
    "test_plan",
    "closure_criteria",
]
LIGHTWEIGHT_SDD_FIELDS = [
    "objective",
    "expected_output",
    "question_to_resolve",
    "closure_criterion",
]
PROFILE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TASK_ROW_SELECTOR_PATTERN = re.compile(r"^TASK-\d{4}$")
PROJECT_STATE_SELECTOR_PATTERN = re.compile(r"^(active_tasks/TASK-\d{4}|[A-Za-z_][A-Za-z0-9_]*)$")
ROW_SCOPED_LEDGER_SELECTORS = {
    "Area_comun/state/TASK_INDEX.json": TASK_ROW_SELECTOR_PATTERN,
    "Area_comun/state/PROJECT_STATE.json": PROJECT_STATE_SELECTOR_PATTERN,
}
VALID_ADOPTION_TIERS = {"coordination", "runtime"}
RUNTIME_TIER_REQUIRED_PATHS = [
    "runtime",
    "runtime/turn_schema.json",
    "scripts/validate_collaboration_state.py",
    "scripts/validate_collaboration_state.ps1",
    "scripts/scan_encoding.py",
    "scripts/scan_encoding.ps1",
    "scripts/scan_domain_neutrality.py",
    "scripts/scan_domain_neutrality.ps1",
    "scripts/measure_context_cost.py",
    "scripts/prune_state.py",
    "scripts/prune_state.ps1",
    ".github/workflows/validate.yml",
]


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_json_file(path: Path, validation: Validation) -> Any | None:
    if not path.exists():
        validation.fail(f"Missing file: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # json.JSONDecodeError plus filesystem/encoding errors.
        validation.fail(f"Invalid JSON: {path} :: {exc}")
        return None


def get_task_status_from_markdown(path: Path) -> str | None:
    if not path.exists():
        return None
    pattern = re.compile(r"^\s*status:\s*(\S+)\s*$")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1)
    return None


def parse_frontmatter_value(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("\"'") for part in inner.split(",")]
    return value.strip("\"'")


def parse_task_markdown(path: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {"frontmatter": {}, "sections": {}}
    if not path.exists():
        return metadata

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    body_start = 0
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                body_start = index + 1
                break
            match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
            if match:
                key, value = match.groups()
                metadata["frontmatter"][key] = parse_frontmatter_value(value)

    current_section: str | None = None
    section_lines: list[str] = []
    for line in lines[body_start:]:
        heading = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if heading:
            if current_section:
                metadata["sections"][current_section] = section_lines
            current_section = heading.group(1).strip().lower().replace(" ", "_")
            section_lines = []
            continue
        if current_section:
            section_lines.append(line)
    if current_section:
        metadata["sections"][current_section] = section_lines
    return metadata


def get_task_field(task: dict[str, Any], parsed_markdown: dict[str, Any], field: str) -> Any | None:
    frontmatter = parsed_markdown.get("frontmatter", {})
    if isinstance(frontmatter, dict) and field in frontmatter:
        return frontmatter[field]
    if field in task:
        return task[field]
    sections = parsed_markdown.get("sections", {})
    if isinstance(sections, dict) and field in sections:
        section_lines = [line.strip() for line in sections[field] if line.strip()]
        return section_lines
    return None


def has_sdd_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().lower() != "none"
    if isinstance(value, list):
        return any(has_sdd_value(item) for item in value)
    return True


def is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def is_presdd_task(task: dict[str, Any], parsed_markdown: dict[str, Any], adopted_at: str) -> bool:
    if is_truthy(get_task_field(task, parsed_markdown, "sdd_exempt")):
        return True
    task_type = get_task_field(task, parsed_markdown, "type")
    if not has_sdd_value(task_type):
        return True
    created_at = get_task_field(task, parsed_markdown, "created_at")
    if isinstance(created_at, str) and DATE_PATTERN.match(created_at) and created_at < adopted_at:
        return True
    return False


def spec_id_exists(root: Path, spec_id: Any) -> bool:
    if not isinstance(spec_id, str) or not spec_id.strip():
        return False
    spec_text = spec_id.strip()
    candidates = [root / spec_text]
    if "/" not in spec_text and "\\" not in spec_text:
        candidates.append(root / "Area_comun" / "specs" / spec_text)
        if not spec_text.endswith(".md"):
            candidates.append(root / "Area_comun" / "specs" / f"{spec_text}.md")
    return any(candidate.exists() for candidate in candidates)


def has_markdown_field(content: str, field: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(field)}\s*:\s*\S+", content, flags=re.MULTILINE))


def is_compact_mailbox_message(content: str) -> bool:
    compact_fields = (
        "one_line_summary",
        "question",
        "context_refs",
        "changed_refs",
        "validation_refs",
        "deadline_or_blocking_level",
    )
    return any(has_markdown_field(content, field) for field in compact_fields)


def get_markdown_field(content: str, field: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(field)}\s*:\s*(.*?)\s*$", content, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def is_false_value(value: str | None) -> bool:
    return isinstance(value, str) and value.strip().lower() == "false"


def references_existing_work(content: str) -> bool:
    reference_patterns = (
        r"\bTASK-\d{4}\b",
        r"\bDECISION-\d{4}\b",
        r"\bSPEC-\d{4}\b",
        r"Area_comun/",
        r"scripts/",
        r"examples/",
        r"README",
    )
    return any(re.search(pattern, content) for pattern in reference_patterns)


def get_value_by_path(obj: Any, dotted_path: str) -> Any | None:
    current = obj
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_scope_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def split_scope(scope: str) -> tuple[str, str | None]:
    path, separator, selector = normalize_scope_path(scope).partition("#")
    if not separator:
        return path, None
    return path, selector


def validate_claim_scope_selector(scope: str, validation: Validation, claim_id: str | None) -> None:
    path, selector = split_scope(scope)
    if selector is None:
        return
    if not path or not selector:
        validation.fail(f"Claim {claim_id} has malformed scoped path: {scope}")
        return
    pattern = ROW_SCOPED_LEDGER_SELECTORS.get(path)
    if pattern is None:
        validation.fail(f"Claim {claim_id} uses row selector on unsupported path: {scope}")
        return
    if not pattern.match(selector):
        validation.fail(f"Claim {claim_id} has invalid row selector: {scope}")


def scope_entries_overlap(left_scope: str, right_scope: str) -> bool:
    left_path, left_selector = split_scope(left_scope)
    right_path, right_selector = split_scope(right_scope)
    if left_path != right_path:
        return False
    if left_path in ROW_SCOPED_LEDGER_SELECTORS:
        return left_selector is None or right_selector is None or left_selector == right_selector
    return left_selector == right_selector


def merge_by_array_field(
    hot: dict[str, Any] | None,
    archive: dict[str, Any] | None,
    field: str,
    id_field: str,
    label: str,
    validation: Validation,
) -> dict[str, Any] | None:
    if not hot:
        return hot
    merged = dict(hot)
    entries: list[Any] = []
    seen: set[str] = set()
    for source_name, source in (("hot", hot), ("archive", archive or {})):
        for entry in as_list(source.get(field) if isinstance(source, dict) else None):
            if not isinstance(entry, dict):
                entries.append(entry)
                continue
            entry_id = str(entry.get(id_field) or "")
            if entry_id:
                if entry_id in seen:
                    validation.fail(f"Duplicate {label} across hot/archive: {entry_id}")
                seen.add(entry_id)
            item = dict(entry)
            item.setdefault("_state_source", source_name)
            entries.append(item)
    merged[field] = entries
    return merged


def parse_semver(version: Any) -> tuple[int, int, int] | None:
    if not isinstance(version, str):
        return None
    match = SEMVER_PATTERN.match(version)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def compare_semver(left: tuple[int, int, int], right: tuple[int, int, int]) -> int:
    if left == right:
        return 0
    return -1 if left < right else 1


def satisfies_version_comparator(
    protocol_version: tuple[int, int, int], operator: str, required_version: tuple[int, int, int]
) -> bool:
    comparison = compare_semver(protocol_version, required_version)
    if operator == "==":
        return comparison == 0
    if operator == ">=":
        return comparison >= 0
    if operator == ">":
        return comparison > 0
    if operator == "<=":
        return comparison <= 0
    if operator == "<":
        return comparison < 0
    return False


def protocol_version_satisfies(
    protocol_version: Any, requirement: Any
) -> tuple[bool, bool]:
    """Return (satisfies, parseable) for exact SemVer and simple comparator ranges."""
    parsed_protocol = parse_semver(protocol_version)
    if parsed_protocol is None or not isinstance(requirement, str) or not requirement.strip():
        return (False, False)

    requirement = requirement.strip()
    if SEMVER_PATTERN.match(requirement):
        return (parsed_protocol == parse_semver(requirement), True)

    for token in requirement.split():
        match = re.match(r"^(>=|<=|>|<|==)(\d+\.\d+\.\d+)$", token)
        if not match:
            return (False, False)
        operator, version = match.groups()
        parsed_required = parse_semver(version)
        if parsed_required is None or not satisfies_version_comparator(
            parsed_protocol, operator, parsed_required
        ):
            return (False, True)
    return (True, True)


def validate_state_invariants(
    state: dict[str, Any] | None,
    config: dict[str, Any] | None,
    validation: Validation,
) -> None:
    if not state or not config:
        return
    for invariant in as_list(config.get("state_invariants")):
        if not isinstance(invariant, dict):
            validation.fail("State invariant must be an object")
            continue
        path = invariant.get("path")
        if not path:
            validation.fail("State invariant without path")
            continue
        actual = get_value_by_path(state, str(path))
        if "equals" in invariant and str(actual) != str(invariant["equals"]):
            validation.fail(
                f"State invariant failed at '{path}': expected "
                f"'{invariant['equals']}', found '{actual}'"
            )
        if invariant.get("required") is True and actual is None:
            validation.fail(f"State invariant failed at '{path}': value is required")


def validate_adoption_tier(
    root: Path,
    config: dict[str, Any] | None,
    validation: Validation,
) -> None:
    if not config:
        return
    tier = config.get("adoption_tier", "coordination")
    if tier is None:
        tier = "coordination"
    if not isinstance(tier, str):
        validation.fail("adoption_tier must be a string: coordination or runtime")
        return
    if tier not in VALID_ADOPTION_TIERS:
        validation.fail(f"Unsupported adoption_tier: {tier}")
        return
    if tier != "runtime":
        return
    for relative in RUNTIME_TIER_REQUIRED_PATHS:
        if not (root / relative).exists():
            validation.fail(f"Runtime adoption tier missing required path: {relative}")


def validate_adopted_profiles(
    root: Path,
    state: dict[str, Any] | None,
    config: dict[str, Any] | None,
    validation: Validation,
) -> None:
    if not state or "adopted_profiles" not in state:
        return

    adopted_profiles = state.get("adopted_profiles")
    if adopted_profiles in (None, []):
        return
    if not isinstance(adopted_profiles, list):
        validation.fail("adopted_profiles must be an array")
        return

    profile_ids: set[str] = set()
    adopted_by_id: dict[str, dict[str, Any]] = {}

    for index, profile in enumerate(adopted_profiles):
        label = f"adopted_profiles[{index}]"
        if not isinstance(profile, dict):
            validation.fail(f"{label} must be an object")
            continue

        profile_id = profile.get("profile_id")
        profile_version = profile.get("profile_version")
        adopted_at = profile.get("adopted_at")

        if not isinstance(profile_id, str) or not profile_id:
            validation.fail(f"{label} missing profile_id")
        elif not PROFILE_ID_PATTERN.match(profile_id):
            validation.fail(f"{label} profile_id has invalid format: {profile_id}")
        elif profile_id in profile_ids:
            validation.fail(f"Duplicate adopted profile: {profile_id}")
        else:
            profile_ids.add(profile_id)
            adopted_by_id[profile_id] = profile

        if not isinstance(profile_version, str) or parse_semver(profile_version) is None:
            validation.fail(f"{label} profile_version must be SemVer MAJOR.MINOR.PATCH")
        if not isinstance(adopted_at, str) or not DATE_PATTERN.match(adopted_at):
            validation.fail(f"{label} adopted_at must be YYYY-MM-DD")

        decision_ref = profile.get("decision_ref")
        if isinstance(decision_ref, str) and decision_ref:
            if not (root / decision_ref).exists():
                validation.warn(f"{label} decision_ref not found: {decision_ref}")

    for profile_id, profile in adopted_by_id.items():
        profile_root = root / "profiles" / profile_id
        manifest_path = profile_root / "profile.manifest.json"
        if not manifest_path.exists():
            validation.warn(
                f"Adopted profile '{profile_id}' is not locally verifiable: "
                f"missing profiles/{profile_id}/profile.manifest.json"
            )
            continue

        manifest = read_json_file(manifest_path, validation)
        if not isinstance(manifest, dict):
            continue

        if manifest.get("profile_id") != profile_id:
            validation.fail(
                f"Adopted profile '{profile_id}' manifest profile_id mismatch: "
                f"'{manifest.get('profile_id')}'"
            )
        if manifest.get("profile_version") != profile.get("profile_version"):
            validation.fail(
                f"Adopted profile '{profile_id}' version mismatch: "
                f"state='{profile.get('profile_version')}' "
                f"manifest='{manifest.get('profile_version')}'"
            )

        requirement = manifest.get("requires_protocol_version")
        satisfies, parseable = protocol_version_satisfies(
            config.get("protocol_version") if config else None, requirement
        )
        if not parseable:
            validation.warn(
                f"Adopted profile '{profile_id}' has unsupported "
                f"requires_protocol_version: {requirement}"
            )
        elif not satisfies:
            validation.fail(
                f"Adopted profile '{profile_id}' requires protocol version "
                f"'{requirement}', found '{config.get('protocol_version') if config else None}'"
            )

        for dependency in as_list(manifest.get("depends_on_profiles")):
            if dependency and dependency not in adopted_by_id:
                validation.fail(
                    f"Adopted profile '{profile_id}' depends on missing profile '{dependency}'"
                )


def validate_tasks(root: Path, index: dict[str, Any] | None, validation: Validation) -> None:
    if not index:
        return
    for task in as_list(index.get("tasks")):
        if not isinstance(task, dict):
            validation.fail("Task entry must be an object")
            continue
        task_id = task.get("id", "<unknown>")
        task_file = task.get("file") or task.get("task_file")
        if not task_file:
            validation.fail(f"Task {task_id} has no file/task_file field")
            continue
        task_path = root / str(task_file)
        if not task_path.exists():
            validation.fail(f"Task {task_id} references missing task file: {task_file}")
            continue
        md_status = get_task_status_from_markdown(task_path)
        if not md_status:
            validation.warn(f"Task {task_id} file has no status metadata: {task_file}")
        elif md_status != task.get("status"):
            validation.fail(
                f"Task {task_id} status mismatch: "
                f"index='{task.get('status')}' file='{md_status}'"
            )
        if task.get("status") in REVIEWED_TASK_STATUSES:
            for deliverable in as_list(task.get("deliverables")):
                if not deliverable:
                    continue
                deliverable_path = root / str(deliverable)
                if not deliverable_path.exists():
                    validation.fail(f"Task {task_id} deliverable missing: {deliverable}")


def validate_sdd(
    root: Path,
    index: dict[str, Any] | None,
    config: dict[str, Any] | None,
    validation: Validation,
) -> None:
    if not index or not config:
        return
    sdd_config = config.get("sdd")
    if not isinstance(sdd_config, dict) or sdd_config.get("enabled") is not True:
        return

    enforcement = sdd_config.get("enforcement") or "new_implementable_tasks"
    if enforcement != "new_implementable_tasks":
        validation.fail(f"Unsupported sdd.enforcement: {enforcement}")
        return
    adopted_at = sdd_config.get("adopted_at") or "2026-06-05"
    if not isinstance(adopted_at, str) or not DATE_PATTERN.match(adopted_at):
        validation.fail(f"Invalid sdd.adopted_at: {adopted_at}")
        return

    for task in as_list(index.get("tasks")):
        if not isinstance(task, dict):
            continue
        task_id = task.get("id", "<unknown>")
        task_file = task.get("file") or task.get("task_file")
        if not task_file:
            continue
        task_path = root / str(task_file)
        parsed = parse_task_markdown(task_path)

        if is_presdd_task(task, parsed, adopted_at):
            continue

        task_type = str(get_task_field(task, parsed, "type")).strip()
        task_status = str(task.get("status", "")).strip()

        if task_type in IMPLEMENTABLE_TASK_TYPES:
            if task_status not in IMPLEMENTABLE_SDD_STATUSES:
                continue
            for field in FULL_SDD_FIELDS:
                if not has_sdd_value(get_task_field(task, parsed, field)):
                    validation.fail(f"Task {task_id} missing SDD field: {field}")
            spec_id = get_task_field(task, parsed, "spec_id")
            if has_sdd_value(spec_id) and not spec_id_exists(root, spec_id):
                validation.fail(f"Task {task_id} spec_id not found: {spec_id}")
        elif task_type in LIGHTWEIGHT_TASK_TYPES:
            if task_status == "proposed":
                continue
            for field in LIGHTWEIGHT_SDD_FIELDS:
                if not has_sdd_value(get_task_field(task, parsed, field)):
                    validation.warn(f"Task {task_id} missing lightweight SDD field: {field}")
        else:
            validation.warn(f"Task {task_id} has unrecognized type: {task_type}")


def validate_mailbox(root: Path, validation: Validation) -> None:
    mailbox_root = root / "Area_comun" / "mailbox"
    for state in ("open", "answered", "archived"):
        mailbox_state_path = mailbox_root / state
        if not mailbox_state_path.exists():
            validation.fail(f"Missing mailbox folder: Area_comun/mailbox/{state}")

    for state in ("open", "answered", "archived"):
        mailbox_state_path = mailbox_root / state
        if not mailbox_state_path.exists():
            continue
        for message_path in mailbox_state_path.glob("MSG-*.md"):
            content = message_path.read_text(encoding="utf-8-sig")
            message_status = (get_markdown_field(content, "status") or "").lower()
            relative = message_path.relative_to(root).as_posix()
            if message_status != state:
                validation.fail(
                    "Mailbox status/folder mismatch: "
                    f"{relative} has status '{message_status or '<missing>'}', expected '{state}'"
                )

            if state != "open":
                continue

            message_type = (get_markdown_field(content, "type") or "").upper()
            requires_response = get_markdown_field(content, "requires_response")

            if message_type in {"ACK", "FYI"} and is_false_value(requires_response):
                validation.warn(
                    "Mailbox message does not require response; consider archiving: "
                    f"{message_path.name}"
                )
            if re.search(r"requires_response:\s*true", content):
                if not re.search(r"response_owner:\s*\S+", content):
                    validation.fail(
                        "Mailbox message requires response but has no response_owner: "
                        f"{message_path.name}"
                    )
                if "requested_action" not in content:
                    validation.fail(
                        "Mailbox message requires response but has no requested_action: "
                        f"{message_path.name}"
                    )
                if is_compact_mailbox_message(content) and not has_markdown_field(content, "question"):
                    validation.fail(
                        "Compact mailbox message requires response but has no question: "
                        f"{message_path.name}"
                    )
            if (
                is_compact_mailbox_message(content)
                and references_existing_work(content)
                and not has_markdown_field(content, "context_refs")
            ):
                validation.warn(
                    "Compact mailbox message references existing work but has no context_refs: "
                    f"{message_path.name}"
                )


def validate_reports(root: Path, validation: Validation) -> None:
    reports_path = root / "Area_comun" / "reports"
    if not reports_path.exists():
        validation.fail("Missing reports folder: Area_comun/reports")
        return
    report_template = reports_path / "HUMAN_REPORT_TEMPLATE.md"
    if not report_template.exists():
        validation.fail("Missing human report template: Area_comun/reports/HUMAN_REPORT_TEMPLATE.md")


def validate_claims(claims: dict[str, Any] | None, validation: Validation) -> None:
    if not claims:
        return
    claim_entries = [claim for claim in as_list(claims.get("claims")) if isinstance(claim, dict)]
    if len(claim_entries) != len(as_list(claims.get("claims"))):
        validation.fail("Claim entry must be an object")

    for claim in claim_entries:
        claim_id = claim.get("claim_id")
        if not claim_id:
            validation.fail("Claim without claim_id")
        if not claim.get("task_id"):
            validation.fail(f"Claim without task_id: {claim_id}")
        if not claim.get("owner"):
            validation.fail(f"Claim without owner: {claim_id}")
        if claim.get("status") not in VALID_CLAIM_STATUSES:
            validation.fail(f"Claim {claim_id} has invalid status '{claim.get('status')}'")
        for scope in as_list(claim.get("scope")):
            if scope:
                validate_claim_scope_selector(str(scope), validation, claim_id)

    active_claims = [claim for claim in claim_entries if claim.get("status") == "active"]
    for left_index, left in enumerate(active_claims):
        for right in active_claims[left_index + 1 :]:
            if left.get("owner") == right.get("owner"):
                continue
            for left_scope in as_list(left.get("scope")):
                for right_scope in as_list(right.get("scope")):
                    if not left_scope or not right_scope:
                        continue
                    left_scope = normalize_scope_path(str(left_scope))
                    right_scope = normalize_scope_path(str(right_scope))
                    if (
                        split_scope(left_scope)[0] == "Area_comun/state/CLAIMS.json"
                        or split_scope(right_scope)[0] == "Area_comun/state/CLAIMS.json"
                    ):
                        continue
                    if split_scope(left_scope)[0].startswith("Area_comun/mailbox/") or split_scope(right_scope)[0].startswith(
                        "Area_comun/mailbox/"
                    ):
                        continue
                    if scope_entries_overlap(left_scope, right_scope):
                        validation.fail(
                            "Overlapping active claims: "
                            f"{left.get('claim_id')} and {right.get('claim_id')} "
                            f"both scope '{left_scope}' / '{right_scope}'"
                        )


def validate_handoff_release(
    index: dict[str, Any] | None,
    claims: dict[str, Any] | None,
    validation: Validation,
) -> None:
    if not index or not claims:
        return
    reviewed_tasks = {
        str(task.get("id")): task
        for task in as_list(index.get("tasks"))
        if isinstance(task, dict) and task.get("status") in REVIEWED_TASK_STATUSES
    }
    if not reviewed_tasks:
        return
    for claim in as_list(claims.get("claims")):
        if not isinstance(claim, dict) or claim.get("status") != "active":
            continue
        task_id = str(claim.get("task_id") or "")
        task = reviewed_tasks.get(task_id)
        if not task:
            continue
        if claim.get("owner") == task.get("owner"):
            validation.fail(
                "Handoff-release violation: "
                f"task {task_id} is {task.get('status')} but owner {claim.get('owner')} "
                f"still has active claim {claim.get('claim_id')}"
            )


def validate_handoffs(root: Path, validation: Validation) -> None:
    handoff_dir = root / "Area_comun" / "handoffs"
    if not handoff_dir.exists():
        return
    for handoff_path in handoff_dir.glob("HANDOFF-*.md"):
        content = handoff_path.read_text(encoding="utf-8-sig")
        if re.search(r"requires_response:\s*(yes|true)", content):
            if not re.search(r"response_owner:\s*\S+", content):
                validation.fail(
                    "Handoff requires response but has no response_owner: "
                    f"{handoff_path.name}"
                )
            if "requested_action" not in content:
                validation.fail(
                    "Handoff requires response but has no requested_action: "
                    f"{handoff_path.name}"
                )


def validate_eventlog_snapshot(root: Path, validation: Validation) -> None:
    if not runtime_state_has_content(root):
        return
    try:
        assert_snapshot_matches(root)
    except EventLogError as exc:
        validation.fail(f"Runtime event log snapshot mismatch: {exc}")


def validate_protocol_state_drift(
    root: Path,
    config: dict[str, Any] | None,
    validation: Validation,
) -> None:
    if not event_state_enabled(config):
        return
    if not runtime_state_has_content(root):
        return
    drift = protocol_state_drift(root)
    if drift.get("has_drift"):
        paths = drift_paths(drift)
        if protocol_state_enforcement_enabled(config):
            validation.fail(
                "Runtime protocol state drift detected under event_state.enforce "
                f"(hard-fail B.3): {paths}. Reconcile by re-materializing from replay(log) "
                "or writing a fresh genesis."
            )
        else:
            validation.warn(f"Runtime protocol state drift detected (warning-only B.1): {paths}")


def validate(root: Path, config_path: Path | None = None) -> Validation:
    validation = Validation()
    root = root.resolve()
    config_path = config_path or (root / "protocol.config.json")

    config = None
    if config_path.exists():
        loaded_config = read_json_file(config_path, validation)
        if isinstance(loaded_config, dict):
            config = loaded_config
    else:
        validation.warn(f"Missing protocol config: {config_path}. No state invariants will be enforced.")

    state_dir = root / "Area_comun" / "state"
    state = read_json_file(state_dir / "PROJECT_STATE.json", validation)
    index_hot = read_json_file(state_dir / "TASK_INDEX.json", validation)
    claims_hot = read_json_file(state_dir / "CLAIMS.json", validation)
    index_archive = read_json_file(state_dir / "TASK_INDEX_ARCHIVE.json", validation) if (state_dir / "TASK_INDEX_ARCHIVE.json").exists() else None
    claims_archive = read_json_file(state_dir / "CLAIMS_ARCHIVE.json", validation) if (state_dir / "CLAIMS_ARCHIVE.json").exists() else None
    index = merge_by_array_field(
        index_hot if isinstance(index_hot, dict) else None,
        index_archive if isinstance(index_archive, dict) else None,
        "tasks",
        "id",
        "task",
        validation,
    )
    claims = merge_by_array_field(
        claims_hot if isinstance(claims_hot, dict) else None,
        claims_archive if isinstance(claims_archive, dict) else None,
        "claims",
        "claim_id",
        "claim",
        validation,
    )

    validate_state_invariants(state if isinstance(state, dict) else None, config, validation)
    validate_adoption_tier(root, config, validation)
    validate_adopted_profiles(root, state if isinstance(state, dict) else None, config, validation)
    validate_tasks(root, index if isinstance(index, dict) else None, validation)
    validate_sdd(root, index if isinstance(index, dict) else None, config, validation)
    validate_mailbox(root, validation)
    validate_reports(root, validation)
    validate_claims(claims if isinstance(claims, dict) else None, validation)
    validate_handoff_release(
        index if isinstance(index, dict) else None,
        claims if isinstance(claims, dict) else None,
        validation,
    )
    validate_handoffs(root, validation)
    validate_eventlog_snapshot(root, validation)
    validate_protocol_state_drift(root, config, validation)
    return validation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a multi-agent protocol instance.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="Instance root")
    parser.add_argument("--config", default=None, help="Path to protocol.config.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate(Path(args.root), Path(args.config) if args.config else None)
    if result.warnings:
        print("WARNINGS:")
        for warning in result.warnings:
            print(f"- {warning}")
    if result.errors:
        print("ERRORS:")
        for error in result.errors:
            print(f"- {error}")
        return 1
    print("OK: collaboration state is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
