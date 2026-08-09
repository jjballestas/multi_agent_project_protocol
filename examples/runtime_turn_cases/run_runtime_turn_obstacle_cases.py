#!/usr/bin/env python3
"""Conditional obstacle cases for authoritative delivery and friction signals."""

from __future__ import annotations

import ast
import sys
import tempfile
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import runtime.turn_validate as turn_validate  # noqa: E402
import runtime.orchestrator as orchestrator  # noqa: E402
from examples.runtime_turn_cases.run_runtime_turn_semantic_cases import build_fixture_root  # noqa: E402


FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES",
        "negative": "A delivery transition cannot be hidden by a divergent outcome label.",
        "mutation": "turn_validate.is_delivery_turn = lambda report: False",
        "boundaries": (
            "assert workflow_delivery_constructor_violations(ROOT) == []",
            "assert turn_validate.validate_delivery_obstacles(delivery_missing) == [DELIVERY_ERROR]",
            "assert turn_validate.validate_delivery_obstacles(delivery_clean) == []",
            "assert turn_validate.validate_delivery_obstacles(delivery_missing) == []",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-STATUS-FRICTION-OBSTACLES",
        "negative": "An authoritative friction status transition cannot carry empty obstacles.",
        "mutation": "sensor for sensor in original_friction(report) if not sensor.startswith(\"task_status:\")",
        "boundaries": (
            "assert STATUS_ERROR in turn_validate.validate_turn(blocked_empty, fixture_root)",
            "assert STATUS_ERROR not in turn_validate.validate_turn(blocked_empty, fixture_root)",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-REVIEW-FRICTION-OBSTACLES",
        "negative": "An authoritative review/QA friction event cannot carry empty obstacles.",
        "mutation": "sensor for sensor in original_friction(report) if not sensor.startswith(\"review_qa:\")",
        "boundaries": (
            "review_errors = turn_validate.validate_turn(review_empty, fixture_root)",
            "assert all(\"review_qa:assign_fix\" not in error for error in mutated_review_errors)",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-CHECKS-FRICTION-OBSTACLES",
        "negative": "Non-empty failed checks cannot carry empty obstacles.",
        "mutation": "sensor for sensor in original_friction(report) if sensor != \"review_qa:checks_failed\"",
        "boundaries": (
            "assert CHECKS_ERROR in turn_validate.validate_turn(checks_empty, fixture_root)",
            "assert CHECKS_ERROR not in turn_validate.validate_turn(checks_empty, fixture_root)",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-REVERT-PROXY-OBSTACLES",
        "negative": "A declared revert action proxy cannot carry empty obstacles.",
        "mutation": "sensor for sensor in original_friction(report) if sensor != \"revert:action-summary-proxy\"",
        "boundaries": (
            "assert REVERT_ERROR in turn_validate.validate_turn(revert, fixture_root)",
            "assert REVERT_ERROR not in turn_validate.validate_turn(revert, fixture_root)",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-ATTEMPT-ID-NOT-A-COUNTER",
        "negative": "An idempotency attempt_id suffix cannot create friction.",
        "mutation": "[\"attempt>1\"] if report.get(\"attempt_id\") == \"TASK-0259-codex-0042\" else []",
        "boundaries": (
            "assert turn_validate.validate_turn(first_attempt_0042, fixture_root) == []",
            "assert ATTEMPT_ERROR in turn_validate.validate_turn(first_attempt_0042, fixture_root)",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-UNTRACKED-SUBTREE-MUST-BE-DECLARED",
        "negative": "The unreported-change gate must reject every undeclared file inside an untracked subtree, even when the report declares the collapsed directory record.",
        "mutation": "removed_source = source.replace",
        "boundaries": (
            'assert collapsed_paths == ["work/"]',
            "assert collapsed_unreported == []",
            "assert healthy_unreported == expected_paths",
            "assert correctly_declared == []",
            "assert mirror_paths == expected_paths",
            "assert removed_unreported == []",
            "assert dead_code_unreported == []",
        ),
        "exercised_by": "exercise_untracked_subtree_gate",
    },
)

DELIVERY_ERROR = "semantic: delivery turn is missing the obstacles block; use [] when there was no friction"
STATUS_ERROR = "semantic: objective friction (task_status:blocked) requires non-empty obstacles"
REVIEW_ERROR = "semantic: objective friction (review_qa:assign_fix) requires non-empty obstacles"
CHECKS_ERROR = "semantic: objective friction (review_qa:checks_failed) requires non-empty obstacles"
REVERT_ERROR = "semantic: objective friction (revert:action-summary-proxy) requires non-empty obstacles"
ATTEMPT_ERROR = "semantic: objective friction (attempt>1) requires non-empty obstacles"


def workflow_python_runners(root: Path) -> list[Path]:
    """Derive Python runner sources from the validate job, never from a maintained list."""
    workflow = yaml.safe_load((root / ".github/workflows/validate.yml").read_text(encoding="utf-8-sig"))
    steps = workflow["jobs"]["validate"]["steps"]
    paths: set[Path] = set()
    pattern = re.compile(r"(?:^|\s)(?:python(?:3(?:\.\d+)*)?|py(?:\.exe)?(?:\s+-3)?)\s+([^\s]+\.py)(?:\s|$)")
    for step in steps:
        command = step.get("run") if isinstance(step, dict) else None
        if not isinstance(command, str):
            continue
        for match in pattern.finditer(command):
            token = match.group(1).strip("\"'")
            path = (root / token).resolve()
            if path.is_file() and root in path.parents:
                paths.add(path)
    return sorted(paths)


def string_keyed_dict(node: ast.AST | None) -> dict[str, ast.AST]:
    if not isinstance(node, ast.Dict):
        return {}
    return {
        key.value: value
        for key, value in zip(node.keys, node.values)
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }


def delivery_constructor(node: ast.Dict) -> bool:
    """Recognize a literal capable of reporting an in_review/done transition."""
    report = string_keyed_dict(node)
    task_status = string_keyed_dict(string_keyed_dict(report.get("transitions")).get("task_status"))
    target = task_status.get("to")
    if target is None:
        return False
    if isinstance(target, ast.Constant):
        return target.value in {"in_review", "done"}
    return True


def workflow_delivery_constructor_violations(root: Path) -> list[str]:
    """Return workflow-derived delivery literals that omit explicit obstacle consideration."""
    violations: list[str] = []
    for path in workflow_python_runners(root):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict) or not delivery_constructor(node):
                continue
            if "obstacles" not in string_keyed_dict(node):
                violations.append(f"{path.relative_to(root).as_posix()}:{node.lineno}")
    return violations


def load_dirty_path_functions(source: str) -> dict[str, object]:
    wanted = {
        "normalize_report_path",
        "parse_porcelain_v1_z",
        "dirty_worktree_paths",
        "unreported_dirty_paths",
    }
    tree = ast.parse(source)
    body = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    assert {node.name for node in body} == wanted
    namespace: dict[str, object] = {"Path": Path, "subprocess": subprocess, "Any": object}
    exec(compile(ast.Module(body=body, type_ignores=[]), "<orchestrator-dirty-functions>", "exec"), namespace)
    return namespace


def exercise_untracked_subtree_gate() -> None:
    """PERMANENT_NEGATIVE: NEG-TURN-UNTRACKED-SUBTREE-MUST-BE-DECLARED"""
    with tempfile.TemporaryDirectory(prefix="runtime-turn-untracked-") as temp:
        root = Path(temp)
        subprocess.run(("git", "init"), cwd=root, check=True, capture_output=True)
        subprocess.run(("git", "config", "user.email", "fixture@example.invalid"), cwd=root, check=True)
        subprocess.run(("git", "config", "user.name", "Fixture"), cwd=root, check=True)
        (root / ".gitkeep").write_text("", encoding="ascii")
        subprocess.run(("git", "add", ".gitkeep"), cwd=root, check=True)
        subprocess.run(("git", "commit", "-m", "fixture"), cwd=root, check=True, capture_output=True)

        expected_paths = [
            "work/declared_note.md",
            "work/hidden/backdoor.py",
            "work/hidden/deep/more.py",
        ]
        for relative in expected_paths:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("probe\n", encoding="ascii")

        collapsed_raw = subprocess.run(
            ("git", "status", "--porcelain=v1", "-z"),
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout
        collapsed_paths = orchestrator.parse_porcelain_v1_z(collapsed_raw)
        declared_directory = {"changed_paths": ["work/"]}
        collapsed_unreported = [
            path
            for path in collapsed_paths
            if orchestrator.normalize_report_path(path) != orchestrator.normalize_report_path("work/")
        ]
        healthy_unreported = orchestrator.unreported_dirty_paths(
            root, declared_directory, baseline_dirty=set()
        )
        correctly_declared = orchestrator.unreported_dirty_paths(
            root, {"changed_paths": expected_paths}, baseline_dirty=set()
        )

        mirror_source = (ROOT / "examples/full_runtime_instance/runtime/orchestrator.py").read_text(
            encoding="utf-8"
        )
        mirror = load_dirty_path_functions(mirror_source)
        mirror_paths = mirror["dirty_worktree_paths"](root)

        source = (ROOT / "runtime/orchestrator.py").read_text(encoding="utf-8")
        live_command = '["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"]'
        removed_source = source.replace(live_command, '["git", "status", "--porcelain=v1", "-z"]', 1)
        dead_code_source = source.replace(live_command, f"{live_command}[:4]", 1)
        assert removed_source != source
        assert dead_code_source != source
        removed = load_dirty_path_functions(removed_source)
        dead_code = load_dirty_path_functions(dead_code_source)
        removed_unreported = removed["unreported_dirty_paths"](
            root, declared_directory, baseline_dirty=set()
        )
        dead_code_unreported = dead_code["unreported_dirty_paths"](
            root, declared_directory, baseline_dirty=set()
        )

        assert collapsed_paths == ["work/"]
        assert collapsed_unreported == []
        assert healthy_unreported == expected_paths
        assert correctly_declared == []
        assert mirror_paths == expected_paths
        assert removed_unreported == []
        assert dead_code_unreported == []


def main() -> int:
    """PERMANENT_NEGATIVE: NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES, NEG-TURN-STATUS-FRICTION-OBSTACLES, NEG-TURN-REVIEW-FRICTION-OBSTACLES, NEG-TURN-CHECKS-FRICTION-OBSTACLES, NEG-TURN-REVERT-PROXY-OBSTACLES, NEG-TURN-ATTEMPT-ID-NOT-A-COUNTER"""
    exercise_untracked_subtree_gate()
    assert workflow_delivery_constructor_violations(ROOT) == []
    delivery_missing = {
        "outcome": "ok",
        "transitions": {"task_status": {"from": "in_progress", "to": "in_review"}},
    }
    delivery_clean = {**delivery_missing, "obstacles": []}
    obstacle = [{"what": "Gate failed.", "root_cause": "Invalid state.", "resolution": "State repaired.", "recurrence_risk": "low"}]

    assert turn_validate.is_delivery_turn(delivery_missing)
    assert turn_validate.validate_delivery_obstacles(delivery_missing) == [DELIVERY_ERROR]
    assert turn_validate.validate_delivery_obstacles(delivery_clean) == []
    assert turn_validate.validate_delivery_obstacles({"outcome": "ok"}) == []

    with tempfile.TemporaryDirectory(prefix="runtime-turn-obstacles-") as temp:
        fixture_root = Path(temp)
        build_fixture_root(fixture_root)
        full_delivery = json.loads((ROOT / "examples/runtime_turn_cases/semantic_valid.json").read_text(encoding="utf-8"))
        full_delivery["outcome"] = "ok"
        full_delivery.pop("obstacles")
        full_errors = turn_validate.validate_turn(full_delivery, fixture_root)
        assert DELIVERY_ERROR in full_errors

        clean = json.loads((ROOT / "examples/runtime_turn_cases/semantic_valid.json").read_text(encoding="utf-8"))
        clean["obstacles"] = []
        assert turn_validate.validate_turn(clean, fixture_root) == []

        blocked_empty = {**clean, "outcome": "blocked", "transitions": {**clean["transitions"], "task_status": {"from": "in_progress", "to": "blocked"}}}
        blocked_with_obstacle = {**blocked_empty, "obstacles": obstacle}
        assert STATUS_ERROR in turn_validate.validate_turn(blocked_empty, fixture_root)
        assert STATUS_ERROR not in turn_validate.validate_turn(blocked_with_obstacle, fixture_root)

        review_empty = {
            **clean,
            "outcome": "blocked",
            "transitions": {
                **clean["transitions"],
                "task_status": {"from": "in_progress", "to": "blocked"},
                "review_qa": {"event": "assign_fix"},
            },
        }
        review_errors = turn_validate.validate_turn(review_empty, fixture_root)
        assert REVIEW_ERROR.replace("review_qa:assign_fix", "task_status:blocked, review_qa:assign_fix") in review_errors

        checks_empty = {
            **clean,
            "outcome": "blocked",
            "transitions": {
                **clean["transitions"],
                "review_qa": {
                    "event": "approve_review",
                    "checks_failed": [{"check_id": "gate", "error_class": "failure", "artifact_path": "runtime/gate.log"}],
                },
            },
        }
        assert CHECKS_ERROR in turn_validate.validate_turn(checks_empty, fixture_root)

        revert = {**clean, "actions": [{"type": "local_exec", "summary": "Reverted the failed change."}]}
        assert REVERT_ERROR in turn_validate.validate_turn(revert, fixture_root)

        first_attempt_0042 = {**clean, "attempt_id": "TASK-0259-codex-0042"}
        assert turn_validate.validate_turn(first_attempt_0042, fixture_root) == []

        original_friction = turn_validate.friction_sensors
        try:
            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if not sensor.startswith("task_status:")
            ]
            assert STATUS_ERROR not in turn_validate.validate_turn(blocked_empty, fixture_root)

            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if not sensor.startswith("review_qa:")
            ]
            mutated_review_errors = turn_validate.validate_turn(review_empty, fixture_root)
            assert all("review_qa:assign_fix" not in error for error in mutated_review_errors)

            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if sensor != "review_qa:checks_failed"
            ]
            assert CHECKS_ERROR not in turn_validate.validate_turn(checks_empty, fixture_root)

            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if sensor != "revert:action-summary-proxy"
            ]
            assert REVERT_ERROR not in turn_validate.validate_turn(revert, fixture_root)

            turn_validate.friction_sensors = lambda report: original_friction(report) + (
                ["attempt>1"] if report.get("attempt_id") == "TASK-0259-codex-0042" else []
            )
            assert ATTEMPT_ERROR in turn_validate.validate_turn(first_attempt_0042, fixture_root)
        finally:
            turn_validate.friction_sensors = original_friction

    original_delivery = turn_validate.is_delivery_turn
    try:
        turn_validate.is_delivery_turn = lambda report: False
        assert turn_validate.validate_delivery_obstacles(delivery_missing) == []
    finally:
        turn_validate.is_delivery_turn = original_delivery

    print("OK: authoritative delivery and in-schema friction controls are mutation-proved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
