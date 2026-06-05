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


VALID_CLAIM_STATUSES = {"active", "released", "blocked"}
REVIEWED_TASK_STATUSES = {"in_review", "done"}
PROFILE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def validate_mailbox(root: Path, validation: Validation) -> None:
    mailbox_root = root / "Area_comun" / "mailbox"
    for state in ("open", "answered", "archived"):
        mailbox_state_path = mailbox_root / state
        if not mailbox_state_path.exists():
            validation.fail(f"Missing mailbox folder: Area_comun/mailbox/{state}")

    open_mailbox_dir = mailbox_root / "open"
    if not open_mailbox_dir.exists():
        return
    for message_path in open_mailbox_dir.glob("MSG-*.md"):
        content = message_path.read_text(encoding="utf-8-sig")
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

    active_claims = [claim for claim in claim_entries if claim.get("status") == "active"]
    for left_index, left in enumerate(active_claims):
        for right in active_claims[left_index + 1 :]:
            if left.get("owner") == right.get("owner"):
                continue
            for left_scope in as_list(left.get("scope")):
                for right_scope in as_list(right.get("scope")):
                    if not left_scope or not right_scope:
                        continue
                    left_scope = str(left_scope)
                    right_scope = str(right_scope)
                    if (
                        left_scope == "Area_comun/state/CLAIMS.json"
                        or right_scope == "Area_comun/state/CLAIMS.json"
                    ):
                        continue
                    if left_scope.startswith("Area_comun/mailbox/") or right_scope.startswith(
                        "Area_comun/mailbox/"
                    ):
                        continue
                    if left_scope == right_scope:
                        validation.fail(
                            "Overlapping active claims: "
                            f"{left.get('claim_id')} and {right.get('claim_id')} "
                            f"both scope '{left_scope}'"
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

    state = read_json_file(root / "Area_comun" / "state" / "PROJECT_STATE.json", validation)
    index = read_json_file(root / "Area_comun" / "state" / "TASK_INDEX.json", validation)
    claims = read_json_file(root / "Area_comun" / "state" / "CLAIMS.json", validation)

    validate_state_invariants(state if isinstance(state, dict) else None, config, validation)
    validate_adopted_profiles(root, state if isinstance(state, dict) else None, config, validation)
    validate_tasks(root, index if isinstance(index, dict) else None, validation)
    validate_mailbox(root, validation)
    validate_reports(root, validation)
    validate_claims(claims if isinstance(claims, dict) else None, validation)
    validate_handoffs(root, validation)
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
