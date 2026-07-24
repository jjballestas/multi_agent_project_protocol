#!/usr/bin/env python3
"""Bridge Agent Teams hook events into protocol gates and audit."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HOOK_EVENTS = {"TaskCreated", "TaskCompleted", "TeammateIdle"}
GATED_EVENTS = {"TaskCompleted", "TeammateIdle"}
KNOWN_LAYERS = {"gate", "audit"}


def runtime_config(config: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(config, dict):
        return {}
    runtime = config.get("runtime")
    return runtime if isinstance(runtime, dict) else {}


def team_bridge_config(config: dict[str, Any] | None) -> dict[str, Any]:
    raw = runtime_config(config).get("team_bridge")
    return raw if isinstance(raw, dict) else {}


def configured_layers(raw: dict[str, Any]) -> list[str]:
    layers: list[str] = []
    for layer in raw.get("layers") or []:
        text = str(layer or "").strip()
        if text and text not in layers:
            layers.append(text)
    return layers


def team_bridge_activation_error(config: dict[str, Any] | None) -> str | None:
    raw = team_bridge_config(config)
    if raw.get("enabled") is not True:
        return "runtime.team_bridge.enabled is not true"
    missing = [
        name
        for name, value in (
            ("activation_decision", str(raw.get("activation_decision") or raw.get("decision_id") or "").strip()),
            ("approved_by", str(raw.get("approved_by") or raw.get("approver") or "").strip()),
            ("approved_at", str(raw.get("approved_at") or raw.get("ratified_at") or "").strip()),
        )
        if not value
    ]
    if missing:
        return "runtime.team_bridge missing " + ", ".join(missing)
    invalid = [layer for layer in configured_layers(raw) if layer not in KNOWN_LAYERS]
    if invalid:
        return "runtime.team_bridge.layers has unsupported values: " + ", ".join(invalid)
    return None


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_config(root: Path) -> dict[str, Any]:
    path = root / "protocol.config.json"
    if not path.exists():
        return {}
    return read_json(path)


def utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        return {"payload": payload}
    return payload


def audit_payload(*, observed_at: str, event: str, payload: dict[str, Any]) -> dict[str, Any]:
    entry = dict(payload)
    entry["observed_at"] = observed_at
    entry["hook"] = event
    return entry


def append_audit(root: Path, *, observed_at: str, event: str, payload: dict[str, Any]) -> dict[str, Any]:
    path = root / "Area_comun" / "state" / "team_audit.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = audit_payload(observed_at=observed_at, event=event, payload=payload)
    with path.open("a", encoding="ascii", newline="\n") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True, sort_keys=True) + "\n")
    return {"path": str(path), "written": True}


def run_command(root: Path, label: str, args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=root, text=True, capture_output=True, check=False)
    return {
        "label": label,
        "args": args,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "ok": completed.returncode == 0,
    }


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def turn_report_from_payload(root: Path, payload: dict[str, Any]) -> Path | None:
    path_value = payload.get("turn_report_path") or payload.get("turn_report")
    if isinstance(path_value, str) and path_value.strip():
        path = Path(path_value)
        return path if path.is_absolute() else root / path
    report = payload.get("turn_report") or payload.get("report")
    if isinstance(report, dict):
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
        with handle:
            json.dump(report, handle, ensure_ascii=True, sort_keys=True)
            handle.write("\n")
        return Path(handle.name)
    return None


def gate_commands(root: Path, payload: dict[str, Any]) -> list[tuple[str, list[str]]]:
    scripts = repo_root() / "scripts"
    commands: list[tuple[str, list[str]]] = [
        (
            "validate_collaboration_state",
            [sys.executable, str(scripts / "validate_collaboration_state.py"), "--root", str(root)],
        ),
        (
            "scan_domain_neutrality",
            [sys.executable, str(scripts / "scan_domain_neutrality.py"), "--root", str(root)],
        ),
    ]
    report_path = turn_report_from_payload(root, payload)
    if report_path is not None:
        commands.append(
            (
                "turn_validate",
                [sys.executable, str(repo_root() / "runtime" / "turn_validate.py"), str(report_path), "--root", str(root)],
            )
        )
    return commands


def run_gates(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    checks = [run_command(root, label, args) for label, args in gate_commands(root, payload)]
    return {"ok": all(check["ok"] for check in checks), "checks": checks}


def stderr_for_gate_failure(gate: dict[str, Any]) -> str:
    lines = ["team_bridge gate failed"]
    for check in gate.get("checks") or []:
        if check.get("ok"):
            continue
        lines.append(f"- {check.get('label')} exited {check.get('returncode')}")
        stdout = str(check.get("stdout") or "").strip()
        stderr = str(check.get("stderr") or "").strip()
        if stdout:
            lines.append(stdout)
        if stderr:
            lines.append(stderr)
    return "\n".join(lines) + "\n"


def handle_event(root: Path, *, event: str, payload: dict[str, Any], observed_at: str) -> tuple[int, dict[str, Any], str]:
    config = read_config(root)
    activation_error = team_bridge_activation_error(config)
    if activation_error:
        return 0, {"ok": True, "active": False, "event": event, "reason": activation_error}, ""

    layers = configured_layers(team_bridge_config(config))
    result: dict[str, Any] = {"ok": True, "active": True, "event": event, "layers": layers}
    stderr = ""

    if "audit" in layers:
        try:
            result["audit"] = append_audit(root, observed_at=observed_at, event=event, payload=payload)
        except Exception as exc:  # noqa: BLE001 - hooks must not crash on audit failures
            result["audit"] = {"written": False, "error": str(exc)}
            stderr += f"team_bridge audit warning: {exc}\n"

    if "gate" in layers and event in GATED_EVENTS:
        gate = run_gates(root, payload)
        result["gate"] = gate
        if not gate["ok"]:
            stderr += stderr_for_gate_failure(gate)
            return 2, result, stderr
    elif "gate" in layers:
        result["gate"] = {"ok": True, "skipped": True, "reason": f"{event} is not a gated hook"}

    return 0, result, stderr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agent Teams hook bridge for protocol gates and audit.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="Protocol instance root.")
    parser.add_argument("--event", required=True, choices=sorted(HOOK_EVENTS), help="Agent Teams hook event.")
    parser.add_argument("--observed-at", default="", help="Deterministic observed_at timestamp for tests.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    try:
        payload = read_payload()
    except json.JSONDecodeError as exc:
        print(f"team_bridge invalid JSON payload: {exc}", file=sys.stderr)
        return 1

    code, result, stderr = handle_event(
        root,
        event=args.event,
        payload=payload,
        observed_at=str(args.observed_at or "").strip() or utc_now_text(),
    )
    if stderr:
        print(stderr, end="", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
