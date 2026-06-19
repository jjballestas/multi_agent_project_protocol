"""Git inspection connector with deny-by-default classification."""

from __future__ import annotations

import json
import shlex
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from connectors.framework import Connector, ConnectorDisabledError, Decision, ReadOnlyDeniedError, TrustBoundary


ALLOWED_VERBS = {"status", "log", "diff", "show", "ls-files", "rev-parse", "blame"}
MUTATING_VERBS = {
    "add",
    "am",
    "apply",
    "branch",
    "checkout",
    "clean",
    "commit",
    "fetch",
    "merge",
    "pull",
    "push",
    "rebase",
    "reset",
    "restore",
    "revert",
    "rm",
    "stash",
    "switch",
    "tag",
}
DANGEROUS_CHARS = {";", "|", "&", ">", "<", "`", "$", "!", "\n", "\r"}
DANGEROUS_FLAGS = {
    "-c",
    "--config",
    "--exec-path",
    "--git-dir",
    "--work-tree",
    "--upload-pack",
    "--receive-pack",
    "--output",
}
ALLOWED_FLAGS = {
    "status": {"--short", "--porcelain", "--branch"},
    "log": {"--oneline", "--decorate", "--stat", "--graph", "--no-merges"},
    "diff": {"--stat", "--name-only", "--cached"},
    "show": {"--stat", "--name-only", "--format=short"},
    "ls-files": {"--stage", "--others", "--cached", "--deleted"},
    "rev-parse": {"--short", "--verify", "--abbrev-ref"},
    "blame": {"--line-porcelain", "--show-name", "--show-number"},
}


@dataclass(frozen=True)
class GitClassification:
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


def _is_safe_ref_or_path(value: str) -> bool:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./:@{}~^+=,-")
    return bool(value) and all(char in allowed for char in value)


def _is_allowed_flag(verb: str, arg: str) -> bool:
    if arg in ALLOWED_FLAGS[verb]:
        return True
    if verb == "log" and (arg.startswith("--max-count=") or (arg.startswith("-n") and arg[2:].isdigit())):
        return True
    if verb == "rev-parse" and arg.startswith("--short=") and arg.removeprefix("--short=").isdigit():
        return True
    return False


def classify_git_operation(
    operation: str | Sequence[str],
    args: Sequence[str] | None = None,
    policy: dict[str, Any] | None = None,
) -> GitClassification:
    tokens = _tokenize(operation, args)
    normalized = _normalize(tokens)
    if not tokens:
        return GitClassification(Decision.DENY, "empty_operation", normalized, "", ())
    if tokens == ("__shell_injection__",):
        return GitClassification(Decision.DENY, "shell_injection", "", "", ())
    if any(_has_shell_metacharacters(token) for token in tokens):
        return GitClassification(Decision.DENY, "shell_injection", normalized, "", ())
    if tokens[0] == "git":
        tokens = tokens[1:]
    if not tokens:
        return GitClassification(Decision.DENY, "empty_operation", normalized, "", ())
    if "git" in tokens[1:]:
        return GitClassification(Decision.DENY, "multi_command", normalized, tokens[0], tuple(tokens[1:]))

    verb = tokens[0]
    verb_args = tuple(tokens[1:])
    allowed_verbs = set(policy.get("allow_verbs") or ALLOWED_VERBS) if isinstance(policy, dict) else ALLOWED_VERBS
    if verb in MUTATING_VERBS:
        return GitClassification(Decision.DENY, "mutating_verb", normalized, verb, verb_args)
    if verb not in ALLOWED_VERBS:
        return GitClassification(Decision.DENY, "unknown_verb", normalized, verb, verb_args)
    if verb not in allowed_verbs:
        return GitClassification(Decision.DENY, "verb_not_allowlisted", normalized, verb, verb_args)

    for arg in verb_args:
        if arg in DANGEROUS_FLAGS or any(arg.startswith(f"{flag}=") for flag in DANGEROUS_FLAGS if flag.startswith("--")):
            return GitClassification(Decision.DENY, "unsafe_argument", normalized, verb, verb_args)
        if arg.startswith("-") and not _is_allowed_flag(verb, arg):
            return GitClassification(Decision.DENY, "unsafe_argument", normalized, verb, verb_args)
        if not arg.startswith("-") and not _is_safe_ref_or_path(arg):
            return GitClassification(Decision.DENY, "unsafe_argument", normalized, verb, verb_args)

    return GitClassification(Decision.ALLOW, "inspection", normalized, verb, verb_args)


class FixtureBackend:
    """Deterministic in-memory backend used by golden tests."""

    def __init__(self, outputs_by_command: dict[str, list[dict[str, Any]]]) -> None:
        self.outputs_by_command = {self._key(key): deepcopy(value) for key, value in outputs_by_command.items()}
        self.calls: list[str] = []

    @staticmethod
    def _key(command: str) -> str:
        return " ".join(str(command or "").strip().split())

    def execute_inspection(self, command: str) -> list[dict[str, Any]]:
        key = self._key(command)
        self.calls.append(key)
        return deepcopy(self.outputs_by_command.get(key, []))


class GitInspectionConnector(Connector):
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
        classification = classify_git_operation(operation, policy=self.policy)
        if classification.decision != Decision.ALLOW:
            raise ReadOnlyDeniedError(classification.reason_class, f"git inspection denied: {classification.reason_class}")
        if self.backend is None:
            if not self.enabled:
                raise ConnectorDisabledError("live connector disabled")
            raise ConnectorDisabledError("live backend requires a later operator GO and s9 verification")
        return self.backend.execute_inspection(classification.normalized)

    def open_live(self) -> None:
        if not self.enabled:
            raise ConnectorDisabledError("live connector disabled")
        raise ConnectorDisabledError("live backend requires a later operator GO and s9 verification")


def load_connector_from_config(
    path: Path,
    connector_id: str,
    *,
    backend: FixtureBackend | None = None,
) -> GitInspectionConnector:
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    for entry in config.get("connectors") or []:
        if isinstance(entry, dict) and entry.get("id") == connector_id:
            return GitInspectionConnector(
                connector_id=connector_id,
                enabled=entry.get("enabled") is True,
                trust_boundary=TrustBoundary.from_dict(entry.get("trust_boundary") or {}),
                backend=backend,
                policy=entry.get("tool_policy") if isinstance(entry.get("tool_policy"), dict) else None,
            )
    raise KeyError(f"connector not found: {connector_id}")
