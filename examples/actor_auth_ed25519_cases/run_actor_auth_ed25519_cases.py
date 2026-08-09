#!/usr/bin/env python3
"""Golden cases for submit_intent actor_auth Ed25519."""

from __future__ import annotations

import base64
import builtins
import json
import re
import shutil
import sys
from types import ModuleType
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives import serialization  # type: ignore
from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore

from runtime.eventlog import EventLogError, EventWriter, actor_auth_signable_event, canonical_hash, verify_actor_auth
from runtime.protocol_replay import protocol_state_drift
from runtime.submit_intent import IntentError, submit_intent
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


PRIVATE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
OTHER_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(2, 34)))

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-ACTOR-AUTH-CRYPTO-DEPENDENCY",
        "negative": "Actor-auth verification must fail explicitly, never crash through an unbound exception type, when cryptography is absent.",
        "mutation": "mutant_source = source.replace(",
        "boundaries": (
            "assert shipped_reason == missing_dependency_reason",
            "assert isinstance(mutant_error, UnboundLocalError)",
        ),
        "exercised_by": "case_cryptography_dependency_contract",
    },
    {
        "id": "NEG-ACTOR-AUTH-CI-DEPENDENCY",
        "negative": "Every workflow job that reaches the canonical validator, directly or through a local wrapper, must install cryptography.",
        "mutation": "missing_install_override = {",
        "boundaries": (
            "assert validator_jobs_install_cryptography(ROOT)",
            "assert not validator_jobs_install_cryptography(ROOT, workflow_overrides=missing_install_override)",
            "assert not validator_jobs_install_cryptography(ROOT, workflow_overrides=new_workflow_override)",
            "assert not validator_jobs_install_cryptography(ROOT, workflow_overrides=module_workflow_override)",
            "assert not validator_jobs_install_cryptography(",
            "assert validator_jobs_install_cryptography(ROOT, workflow_overrides=pinned_install_override)",
            "assert validator_jobs_install_cryptography(ROOT, workflow_overrides=separate_install_override)",
        ),
        "exercised_by": "case_cryptography_dependency_contract",
    },
    {
        "id": "NEG-ACTOR-AUTH-CI-REACHABILITY",
        "negative": "The actor-auth falsification runner must execute even when an earlier validate-job step fails.",
        "mutation": "unreachable_override = {",
        "boundaries": (
            "assert actor_auth_negative_is_reachable(ROOT)",
            "assert not actor_auth_negative_is_reachable(ROOT, workflow_overrides=unreachable_override)",
        ),
        "exercised_by": "case_cryptography_dependency_contract",
    },
)


def public_b64(key: ed25519.Ed25519PrivateKey) -> str:
    raw = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return base64.b64encode(raw).decode("ascii")


def private_pem(key: ed25519.Ed25519PrivateKey) -> str:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n", encoding="ascii", newline="\n")


def config(*, enforce: bool, keyid: str = "codex-test-key", public_key: str | None = None) -> dict[str, Any]:
    payload = {
        "schema_version": "1.0",
        "protocol_version": "1.14.0",
        "adoption_tier": "runtime",
        "event_auth": {"enabled": False},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "slim_views_enabled": False,
            "chain_enabled": False,
            "agent_signatures_enabled": False,
            "signature_config": {
                "backend": "local-ed25519",
                "public_keys": {keyid: public_key or public_b64(PRIVATE_KEY)},
            },
            "anchor_enabled": False,
        },
        "agent_registry": {"enabled": True, "agents": [{"id": "Codex", "enabled": True, "capabilities": ["implementer"]}]},
        "state_invariants": [{"path": "status", "equals": "active"}],
    }
    return payload


def actor_auth_override(*, enforce: bool, keyid: str = "codex-test-key") -> dict[str, Any]:
    return {
        "event_state": {
            "actor_auth_enforce": enforce,
            "actor_auth_config": {
                "private_key_files": {"Codex": "secrets/codex.pem"},
                "keyids": {"Codex": keyid},
            },
        }
    }


def seed_repo(root: Path, *, enforce: bool, with_secret: bool = True, public_key: str | None = None) -> None:
    write_json(root / "protocol.config.json", config(enforce=False, public_key=public_key))
    if enforce:
        write_json(root / "event-state.runtime.json", actor_auth_override(enforce=True))
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active", "decisions": [], "active_tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    if with_secret:
        (root / "secrets").mkdir(parents=True, exist_ok=True)
        (root / "secrets/codex.pem").write_text(private_pem(PRIVATE_KEY), encoding="ascii")


def intent() -> dict[str, Any]:
    return {
        "type": "claim",
        "op": "acquire",
        "claim": {
            "claim_id": "CLAIM-ACTOR-AUTH",
            "task_id": "TASK-0001",
            "owner": "Codex",
            "status": "active",
            "started_at": "2026-06-27T00:00:00Z",
            "updated_at": "2026-06-27T00:00:00Z",
            "expires_at": "2026-06-28T00:00:00Z",
            "scope": ["runtime/"],
            "notes": "actor auth golden",
        },
    }


def block_cryptography_imports(name: str, *args: object, **kwargs: object) -> object:
    if name == "cryptography" or name.startswith("cryptography."):
        raise ModuleNotFoundError("blocked cryptography import for dependency contract")
    return ORIGINAL_IMPORT(name, *args, **kwargs)


ORIGINAL_IMPORT = builtins.__import__


def missing_dependency_result(verify: object) -> tuple[str | None, BaseException | None]:
    event = {
        "actor": "Codex",
        "actor_auth": {
            "method": "ed25519",
            "keyid": "codex:v1",
            "sig": base64.b64encode(b"not-a-real-signature").decode("ascii"),
        },
    }
    try:
        builtins.__import__ = block_cryptography_imports
        verify(event, config(enforce=False, keyid="codex:v1"))  # type: ignore[operator]
    except EventLogError as exc:
        return str(exc), None
    except BaseException as exc:  # The negative must classify the former UnboundLocalError.
        return None, exc
    finally:
        builtins.__import__ = ORIGINAL_IMPORT
    return None, None


def workflow_sources(
    root: Path,
    workflow_overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    sources = {
        path.relative_to(root).as_posix(): path.read_text(encoding="utf-8-sig")
        for pattern in ("*.yml", "*.yaml")
        for path in sorted((root / ".github/workflows").glob(pattern))
    }
    sources.update(workflow_overrides or {})
    return sources


def referenced_local_scripts(command: str) -> tuple[str, ...]:
    normalized = command.replace("\\", "/")
    matches = re.findall(
        r"(?<![A-Za-z0-9_.-])((?:\./)?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:sh|ps1|py|cmd|bat))(?![A-Za-z0-9_.-])",
        normalized,
        flags=re.IGNORECASE,
    )
    return tuple(dict.fromkeys(match.removeprefix("./") for match in matches))


def executable_wrapper_lines(source: str) -> tuple[str, ...]:
    executable = re.compile(
        r"^\s*(?:(?:if|while|until)\s+!?\s*)?(?:python(?:3(?:\.\d+)?)?|py|bash|sh|pwsh|powershell|cmd|\./)",
        re.IGNORECASE,
    )
    return tuple(line for line in source.splitlines() if executable.search(line))


def command_reaches_validator(
    root: Path,
    command: str,
    *,
    script_overrides: dict[str, str] | None = None,
    visited: frozenset[str] = frozenset(),
) -> bool:
    normalized = command.replace("\\", "/").casefold()
    if re.search(r"(?<![a-z0-9_.])scripts/validate_collaboration_state\.py(?![a-z0-9_.])", normalized):
        return True
    if re.search(r"(?<![a-z0-9_.])scripts\.validate_collaboration_state(?![a-z0-9_.])", normalized):
        return True

    overrides = script_overrides or {}
    for relative in referenced_local_scripts(command):
        key = relative.replace("\\", "/")
        if key in visited:
            continue
        if Path(key).suffix.casefold() == ".py":
            continue
        source = overrides.get(key)
        if source is None:
            candidate = (root / key).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                continue
            if not candidate.is_file():
                continue
            source = candidate.read_text(encoding="utf-8-sig")
        for wrapper_line in executable_wrapper_lines(source):
            if command_reaches_validator(
                root,
                wrapper_line,
                script_overrides=overrides,
                visited=visited | {key},
            ):
                return True
    return False


def command_installs_cryptography(command: str) -> bool:
    install = re.search(r"(?:python(?:3(?:\.\d+)?)?\s+-m\s+pip|pip(?:3(?:\.\d+)?)?)\s+install\b(?P<args>[^\r\n]*)", command, re.IGNORECASE)
    if install is None:
        return False
    return re.search(
        r"(?:^|\s)[\"']?cryptography(?:\[[^\]\s]+\])?(?:(?:===|==|~=|!=|<=|>=|<|>)[^\s;|&\"']+)?[\"']?(?=$|[\s;|&])",
        install.group("args"),
        re.IGNORECASE,
    ) is not None


def validator_jobs_install_cryptography(
    root: Path,
    *,
    workflow_overrides: dict[str, str] | None = None,
    script_overrides: dict[str, str] | None = None,
) -> bool:
    validator_jobs: list[list[str]] = []
    for workflow_text in workflow_sources(root, workflow_overrides).values():
        document = yaml.safe_load(workflow_text)
        jobs = document.get("jobs") if isinstance(document, dict) else None
        if not isinstance(jobs, dict):
            continue
        for raw_job in jobs.values():
            if not isinstance(raw_job, dict) or not isinstance(raw_job.get("steps"), list):
                continue
            commands = [
                str(step.get("run") or "")
                for step in raw_job["steps"]
                if isinstance(step, dict)
            ]
            if any(
                command_reaches_validator(root, command, script_overrides=script_overrides)
                for command in commands
            ):
                validator_jobs.append(commands)
    return bool(validator_jobs) and all(
        any(command_installs_cryptography(command) for command in commands)
        for commands in validator_jobs
    )


def actor_auth_negative_is_reachable(
    root: Path,
    *,
    workflow_overrides: dict[str, str] | None = None,
) -> bool:
    runner_steps: list[dict[str, Any]] = []
    for workflow_text in workflow_sources(root, workflow_overrides).values():
        document = yaml.safe_load(workflow_text)
        jobs = document.get("jobs") if isinstance(document, dict) else None
        if not isinstance(jobs, dict):
            continue
        for raw_job in jobs.values():
            if not isinstance(raw_job, dict) or not isinstance(raw_job.get("steps"), list):
                continue
            runner_steps.extend(
                step
                for step in raw_job["steps"]
                if isinstance(step, dict)
                and "examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py"
                in str(step.get("run") or "").replace("\\", "/")
            )
    return bool(runner_steps) and all(str(step.get("if") or "").strip() == "always()" for step in runner_steps)


def case_cryptography_dependency_contract() -> tuple[str, bool, str]:
    """PERMANENT_NEGATIVE: NEG-ACTOR-AUTH-CRYPTO-DEPENDENCY, NEG-ACTOR-AUTH-CI-DEPENDENCY, NEG-ACTOR-AUTH-CI-REACHABILITY"""
    missing_dependency_reason = "actor_auth verification unavailable: cryptography package is required"
    shipped_reason, shipped_error = missing_dependency_result(verify_actor_auth)
    assert shipped_error is None
    assert shipped_reason == missing_dependency_reason

    source = (ROOT / "runtime/eventlog.py").read_text(encoding="utf-8-sig")
    mutant_source = source.replace(
        "    except ImportError as exc:\n"
        "        raise EventLogError(\"actor_auth verification unavailable: cryptography package is required\") from exc\n"
        "    try:\n"
        "        raw_signature",
        "        raw_signature",
        1,
    )
    if mutant_source == source:
        return "AC6-cryptography-dependency-contract", False, "eventlog mutation did not apply"
    mutant = ModuleType("mutant_eventlog")
    exec(compile(mutant_source, "mutant_eventlog.py", "exec"), mutant.__dict__)
    _mutant_reason, mutant_error = missing_dependency_result(mutant.verify_actor_auth)
    assert isinstance(mutant_error, UnboundLocalError)

    workflow_path = ".github/workflows/validate.yml"
    workflow_text = (ROOT / workflow_path).read_text(encoding="utf-8-sig")
    assert validator_jobs_install_cryptography(ROOT)
    assert actor_auth_negative_is_reachable(ROOT)

    missing_install_override = {
        workflow_path: workflow_text.replace("cryptography jsonschema pyyaml", "jsonschema pyyaml", 1)
    }
    assert not validator_jobs_install_cryptography(ROOT, workflow_overrides=missing_install_override)

    added_job_prefix = (
        "name: dependency mutant\n"
        "on: [push]\n"
        "jobs:\n"
        "  probe:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - run: "
    )
    new_workflow_override = {
        ".github/workflows/nightly.yml": added_job_prefix
        + "python ./scripts/validate_collaboration_state.py --root .\n"
    }
    assert not validator_jobs_install_cryptography(ROOT, workflow_overrides=new_workflow_override)

    module_workflow_override = {
        ".github/workflows/nightly.yml": added_job_prefix
        + "python -m scripts.validate_collaboration_state --root .\n"
    }
    assert not validator_jobs_install_cryptography(ROOT, workflow_overrides=module_workflow_override)

    wrapper_workflow_override = {
        ".github/workflows/nightly.yml": added_job_prefix + "bash scripts/ci_validate.sh\n"
    }
    assert not validator_jobs_install_cryptography(
        ROOT,
        workflow_overrides=wrapper_workflow_override,
        script_overrides={
            "scripts/ci_validate.sh": "python -m scripts.validate_collaboration_state --root .\n"
        },
    )

    pinned_install_override = {
        workflow_path: workflow_text.replace("cryptography jsonschema pyyaml", "cryptography==43.0.0 jsonschema pyyaml", 1)
    }
    assert validator_jobs_install_cryptography(ROOT, workflow_overrides=pinned_install_override)

    separate_install_override = {
        workflow_path: workflow_text.replace(
            "      - name: Install Python test dependencies\n"
            "        run: python -m pip install cryptography jsonschema pyyaml\n",
            "      - name: Install Python test dependencies\n"
            "        run: python -m pip install jsonschema pyyaml\n\n"
            "      - name: Install actor-auth dependency\n"
            "        run: python -m pip install 'cryptography>=43'\n",
            1,
        )
    }
    assert validator_jobs_install_cryptography(ROOT, workflow_overrides=separate_install_override)

    unreachable_override = {
        workflow_path: workflow_text.replace(
            "        if: always()\n"
            "        run: python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py",
            "        run: python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py",
            1,
        )
    }
    assert not actor_auth_negative_is_reachable(ROOT, workflow_overrides=unreachable_override)
    return (
        "AC6-cryptography-dependency-contract",
        True,
        "missing dependency is explicit; all-workflow, module, wrapper, install, and reachability mutants diverge",
    )


def case_submit_intent_signs() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-case-")
    try:
        seed_repo(root, enforce=True)
        result = submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        auth = result["event"]["actor_auth"]
        ok = auth.get("method") == "ed25519" and auth.get("keyid") == "codex-test-key"
        return "AC1-submit-intent-signs", ok and verify_actor_auth(result["event"], config(enforce=False), root)["valid"], str(auth)
    finally:
        remove_root_temp_dir(root)


def case_off_byte_identical() -> tuple[str, bool, str]:
    roots = [make_root_temp_dir(ROOT, ".actor-auth-off-a-"), make_root_temp_dir(ROOT, ".actor-auth-off-b-")]
    try:
        write_json(roots[0] / "protocol.config.json", config(enforce=False))
        write_json(roots[1] / "protocol.config.json", config(enforce=False))
        event_a = EventWriter(roots[0]).append_event(event_type="intent.applied", aggregate_id="TASK-0001", actor_id="Codex", payload={"x": 1}, ts="2026-06-27T00:00:00Z")
        event_b = EventWriter(roots[1]).append_event(event_type="intent.applied", aggregate_id="TASK-0001", actor_id="Codex", payload={"x": 1}, ts="2026-06-27T00:00:00Z")
        return "AC2-off-byte-identical", canonical_hash(event_a) == canonical_hash(event_b), event_a["actor_auth"]["method"]
    finally:
        for root in roots:
            remove_root_temp_dir(root)


def case_cross_attribution_rejected() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-cross-")
    try:
        seed_repo(root, enforce=True, public_key=public_b64(OTHER_KEY))
        try:
            result = submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError:
            return "AC3-cross-attribution-rejected", True, "write rejected"
        auth_result = verify_actor_auth(result["event"], config(enforce=False, public_key=public_b64(OTHER_KEY)), root)
        return "AC3-cross-attribution-rejected", auth_result["valid"] is False, str(auth_result)
    finally:
        remove_root_temp_dir(root)


def case_secret_independent_verify() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-secretless-")
    clone = make_root_temp_dir(ROOT, ".actor-auth-secretless-clone-")
    try:
        seed_repo(root, enforce=True)
        submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        shutil.copytree(root, clone, dirs_exist_ok=True, ignore=shutil.ignore_patterns("secrets"))
        drift = protocol_state_drift(clone)
        return "AC4-secret-independent-verify", drift.get("has_drift") is False, json.dumps(drift, sort_keys=True)
    finally:
        remove_root_temp_dir(root)
        remove_root_temp_dir(clone)


def case_sign_without_secret_fails() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-no-secret-")
    try:
        seed_repo(root, enforce=True, with_secret=False)
        try:
            submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError as exc:
            return "AC4-sign-without-secret-fails", "private signing key missing" in str(exc), str(exc)
        return "AC4-sign-without-secret-fails", False, "unexpected success"
    finally:
        remove_root_temp_dir(root)


def case_runtime_override_flip_clean() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-override-flip-")
    try:
        seed_repo(root, enforce=False)
        before = (root / "protocol.config.json").read_bytes()
        write_json(root / "event-state.runtime.json", actor_auth_override(enforce=True))
        result = submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        after = (root / "protocol.config.json").read_bytes()
        drift = protocol_state_drift(root)
        auth = result["event"]["actor_auth"]
        ok = (
            before == after
            and auth.get("method") == "ed25519"
            and verify_actor_auth(result["event"], config(enforce=False), root)["valid"] is True
            and drift.get("has_drift") is False
        )
        return "AC5-runtime-override-flip-clean", ok, json.dumps({"auth": auth, "drift": drift}, sort_keys=True)
    finally:
        remove_root_temp_dir(root)


def main() -> int:
    cases = [
        case_submit_intent_signs,
        case_off_byte_identical,
        case_cross_attribution_rejected,
        case_secret_independent_verify,
        case_sign_without_secret_fails,
        case_runtime_override_flip_clean,
        case_cryptography_dependency_contract,
    ]
    results = [case() for case in cases]
    print(json.dumps({"actor_auth_ed25519_cases.v1": [{"name": name, "ok": ok, "detail": detail} for name, ok, detail in results]}, indent=2, sort_keys=True))
    return 0 if all(ok for _name, ok, _detail in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
