"""CI read-only connector with deny-by-default classification."""

from __future__ import annotations

import json
import shlex
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from connectors.framework import Connector, ConnectorDisabledError, Decision, ReadOnlyDeniedError, TrustBoundary


ALLOWED_VERBS = {"list_runs", "run_status", "run_conclusion", "job_status", "run_summary"}
MUTATING_VERBS = {
    "approve",
    "cancel",
    "delete_artifact",
    "dispatch",
    "edit_workflow",
    "rerun",
    "set_secret",
    "set_variable",
    "trigger",
    "update_secret",
    "workflow_dispatch",
}
DANGEROUS_CHARS = {";", "|", "&", ">", "<", "`", "$", "!", "\n", "\r"}
ALLOWED_FLAGS = {"--repo", "--workflow", "--run-id", "--job-id", "--branch", "--limit"}


@dataclass(frozen=True)
class CiClassification:
    decision: str
    reason_class: str
    normalized: str
    verb: str
    args: tuple[str, ...]


def _has_shell_metacharacters(value: str) -> bool:
    return any(char in value for char in DANGEROUS_CHARS)


def _tokenize(command: str | Sequence[str], args: Sequence[str] | None) -> tuple[str, ...]:
    if args is not None:
        tokens = [str(command), *[str(item) for item in args]]
    elif isinstance(command, str):
        if _has_shell_metacharacters(command):
            return ("__shell_injection__",)
        try:
            tokens = shlex.split(command, posix=True)
        except ValueError:
            return ("__shell_injection__",)
    else:
        tokens = [str(item) for item in command]
    return tuple(item.strip() for item in tokens if item and item.strip())


def _normalize(tokens: Sequence[str]) -> str:
    return " ".join(tokens)


def _is_safe_value(value: str) -> bool:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./:@{}~^+=,-")
    return bool(value) and all(char in allowed for char in value)


def _args_are_safe(args: tuple[str, ...]) -> bool:
    index = 0
    while index < len(args):
        arg = args[index]
        if arg.startswith("--"):
            if "=" in arg:
                flag, value = arg.split("=", 1)
                if flag not in ALLOWED_FLAGS or not _is_safe_value(value):
                    return False
                index += 1
                continue
            if arg not in ALLOWED_FLAGS or index + 1 >= len(args) or not _is_safe_value(args[index + 1]):
                return False
            index += 2
            continue
        if not _is_safe_value(arg):
            return False
        index += 1
    return True


def classify_ci_operation(
    operation: str | Sequence[str],
    args: Sequence[str] | None = None,
    policy: dict[str, Any] | None = None,
) -> CiClassification:
    tokens = _tokenize(operation, args)
    normalized = _normalize(tokens)
    if not tokens:
        return CiClassification(Decision.DENY, "empty_operation", normalized, "", ())
    if tokens == ("__shell_injection__",):
        return CiClassification(Decision.DENY, "shell_injection", "", "", ())
    if any(_has_shell_metacharacters(token) for token in tokens):
        return CiClassification(Decision.DENY, "shell_injection", normalized, "", ())
    if tokens[0] in {"ci", "gha", "github-actions"}:
        tokens = tokens[1:]
    if not tokens:
        return CiClassification(Decision.DENY, "empty_operation", normalized, "", ())
    if any(token in {"ci", "gha", "github-actions"} for token in tokens[1:]):
        return CiClassification(Decision.DENY, "multi_command", normalized, tokens[0], tuple(tokens[1:]))

    verb = tokens[0]
    verb_args = tuple(tokens[1:])
    allowed_verbs = set(policy.get("allow_verbs") or ALLOWED_VERBS) if isinstance(policy, dict) else ALLOWED_VERBS
    if verb in MUTATING_VERBS:
        return CiClassification(Decision.DENY, "mutating_verb", normalized, verb, verb_args)
    if verb not in ALLOWED_VERBS:
        return CiClassification(Decision.DENY, "unknown_verb", normalized, verb, verb_args)
    if verb not in allowed_verbs:
        return CiClassification(Decision.DENY, "verb_not_allowlisted", normalized, verb, verb_args)
    if not _args_are_safe(verb_args):
        return CiClassification(Decision.DENY, "unsafe_argument", normalized, verb, verb_args)
    return CiClassification(Decision.ALLOW, "read", normalized, verb, verb_args)


class FixtureBackend:
    """Deterministic in-memory backend used by golden tests."""

    def __init__(self, outputs_by_operation: dict[str, list[dict[str, Any]]]) -> None:
        self.outputs_by_operation = {self._key(key): deepcopy(value) for key, value in outputs_by_operation.items()}
        self.calls: list[str] = []

    @staticmethod
    def _key(operation: str) -> str:
        return " ".join(str(operation or "").strip().split())

    def execute_read(self, operation: str) -> list[dict[str, Any]]:
        key = self._key(operation)
        self.calls.append(key)
        return deepcopy(self.outputs_by_operation.get(key, []))


class CiReadOnlyConnector(Connector):
    def __init__(
        self,
        *,
        connector_id: str,
        trust_boundary: TrustBoundary,
        enabled: bool,
        backend: FixtureBackend | None = None,
        policy: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(connector_id=connector_id, trust_boundary=trust_boundary, enabled=enabled)
        self.backend = backend
        self.policy = policy or {"allow_verbs": list(ALLOWED_VERBS)}

    def read(self, operation: str) -> list[dict[str, Any]]:
        classification = classify_ci_operation(operation, policy=self.policy)
        if classification.decision != Decision.ALLOW:
            raise ReadOnlyDeniedError(classification.reason_class, f"CI read denied: {classification.reason_class}")
        if self.backend is None:
            if not self.enabled:
                raise ConnectorDisabledError("live connector disabled")
            raise ConnectorDisabledError("live backend requires a later operator GO and s9 verification")
        return self.backend.execute_read(classification.normalized)

    def open_live(self) -> None:
        if not self.enabled:
            raise ConnectorDisabledError("live connector disabled")
        raise ConnectorDisabledError("live backend requires a later operator GO and s9 verification")


def load_connector_from_config(
    path: Path,
    connector_id: str,
    *,
    backend: FixtureBackend | None = None,
) -> CiReadOnlyConnector:
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    for entry in config.get("connectors") or []:
        if isinstance(entry, dict) and entry.get("id") == connector_id:
            return CiReadOnlyConnector(
                connector_id=connector_id,
                enabled=entry.get("enabled") is True,
                trust_boundary=TrustBoundary.from_dict(entry.get("trust_boundary") or {}),
                backend=backend,
                policy=entry.get("tool_policy") if isinstance(entry.get("tool_policy"), dict) else None,
            )
    raise KeyError(f"connector not found: {connector_id}")
