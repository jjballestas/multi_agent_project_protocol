#!/usr/bin/env python3
"""Deterministic improvement offers from runtime and mailbox delivery obstacles.

This module can draft and record offers, but intentionally has no protocol/skill
write or task/decision creation capability. Accepted offers still require the normal
human-approved DECISION + task flow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

STATUSES = {"offered", "accepted", "rejected", "parked"}


@dataclass(frozen=True)
class Obstacle:
    source: str
    delivery_id: str
    what: str
    root_cause: str
    resolution: str
    recurrence_risk: str

    @property
    def root_key(self) -> str:
        # Public, reproducible identity rule: NFKC, case-fold, trim, collapse whitespace.
        return " ".join(unicodedata.normalize("NFKC", self.root_cause).casefold().split())

    @property
    def evidence_id(self) -> str:
        material = "\0".join((self.source, self.delivery_id, self.what, self.root_key, self.resolution))
        return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _obstacles(report: dict[str, Any], source: str, delivery_id: str) -> list[Obstacle]:
    result = []
    for item in report.get("obstacles", []):
        if not isinstance(item, dict):
            continue
        required = ("what", "root_cause", "resolution", "recurrence_risk")
        if not all(isinstance(item.get(k), str) and item[k].strip() for k in required):
            continue
        risk = item["recurrence_risk"].strip().casefold()
        if risk not in {"low", "medium", "high"}:
            continue
        result.append(Obstacle(source, delivery_id, *(item[k].strip() for k in required)))
    return result


def read_runtime(path: Path) -> list[Obstacle]:
    rows: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        value = json.loads(text)
        rows = value if isinstance(value, list) else [value]
    result: list[Obstacle] = []
    for index, row in enumerate(rows, 1):
        report = row.get("report", row)
        delivery_id = str(report.get("turn_id") or report.get("task_id") or f"row-{index}")
        result.extend(_obstacles(report, f"runtime:{path.as_posix()}", delivery_id))
    return result


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    return {m.group(1): m.group(2).strip().strip('"') for m in re.finditer(r"(?m)^([a-z_]+):\s*(.+)$", block)}


def read_mailbox(path: Path) -> list[Obstacle]:
    text = path.read_text(encoding="utf-8")
    meta = _frontmatter(text)
    if meta.get("type", "").upper() != "REPORTE":
        return []
    found: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        first = re.match(r"^\s*-\s+what:\s*(.+?)\s*$", line)
        field = re.match(r"^\s+(root_cause|resolution|recurrence_risk):\s*(.+?)\s*$", line)
        if first:
            if current:
                found.append(current)
            current = {"what": first.group(1).strip().strip('"')}
        elif field and current is not None:
            current[field.group(1)] = field.group(2).strip().strip('"')
    if current:
        found.append(current)
    delivery_id = meta.get("task_id") or meta.get("message_id") or path.stem
    return _obstacles({"obstacles": found}, f"mailbox:{path.as_posix()}", delivery_id)


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": "1.0", "offers": []}
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "1.0" or not isinstance(value.get("offers"), list):
        raise ValueError("registry must have schema_version 1.0 and offers[]")
    return value


def proposal_id(root_key: str) -> str:
    return "OFFER-" + hashlib.sha256(root_key.encode("utf-8")).hexdigest()[:12]


def evaluate(obstacles: Iterable[Obstacle], registry: dict[str, Any], new_evidence: set[str] | None = None) -> list[dict[str, Any]]:
    grouped: dict[str, list[Obstacle]] = {}
    for obstacle in obstacles:
        grouped.setdefault(obstacle.root_key, []).append(obstacle)
    prior = {row["proposal_id"]: row for row in registry["offers"]}
    declared = new_evidence or set()
    offers = []
    for key, items in sorted(grouped.items()):
        deliveries = {item.delivery_id for item in items}
        reasons = []
        if any(item.recurrence_risk.casefold() == "high" for item in items):
            reasons.append("recurrence_risk_high")
        if len(deliveries) >= 2:
            reasons.append("root_cause_repeated_across_deliveries")
        if not reasons:
            continue
        pid = proposal_id(key)
        evidence = sorted(item.evidence_id for item in items)
        old = prior.get(pid)
        if old:
            if old.get("status") == "accepted":
                continue
            if old.get("status") in {"rejected", "parked"}:
                changed = evidence != sorted(old.get("evidence_ids", []))
                if not (changed and pid in declared):
                    continue
            elif evidence == sorted(old.get("evidence_ids", [])):
                continue
        exemplar = sorted(items, key=lambda item: item.evidence_id)[0]
        citations = sorted(f"{item.source}#{item.delivery_id}:{item.evidence_id}" for item in items)
        offers.append({
            "proposal_id": pid,
            "status": "offered",
            "root_cause_key": key,
            "trigger": reasons,
            "evidence_ids": evidence,
            "citations": citations,
            "draft_change": (
                f"Proposed rule: When '{exemplar.root_cause}' occurs, the implementer MUST "
                f"apply this control: {exemplar.resolution}. Verification MUST include a regression "
                f"that reproduces '{exemplar.what}' and fails when the control is removed."
            ),
            "requires_human_response": True,
            "allowed_responses": ["accepted", "rejected", "parked"],
            "application_path": "human acceptance -> DECISION -> governed task",
        })
    return offers


def record_offers(registry: dict[str, Any], offers: list[dict[str, Any]]) -> None:
    existing = {row["proposal_id"]: index for index, row in enumerate(registry["offers"])}
    for offer in offers:
        if offer["proposal_id"] in existing:
            registry["offers"][existing[offer["proposal_id"]]] = offer
        else:
            registry["offers"].append(offer)


def record_response(registry: dict[str, Any], pid: str, status: str, response_ref: str) -> None:
    if status not in STATUSES - {"offered"}:
        raise ValueError("response must be accepted, rejected, or parked")
    for offer in registry["offers"]:
        if offer.get("proposal_id") == pid:
            offer["status"] = status
            offer["response_ref"] = response_ref
            return
    raise ValueError(f"unknown proposal_id: {pid}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", action="append", default=[], type=Path)
    parser.add_argument("--mailbox", action="append", default=[], type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--record-offers", action="store_true")
    parser.add_argument("--new-evidence", action="append", default=[])
    parser.add_argument("--respond", choices=sorted(STATUSES - {"offered"}))
    parser.add_argument("--proposal-id")
    parser.add_argument("--response-ref")
    args = parser.parse_args()
    registry = load_registry(args.registry)
    if args.respond:
        if not args.proposal_id or not args.response_ref:
            parser.error("--respond requires --proposal-id and --response-ref")
        record_response(registry, args.proposal_id, args.respond, args.response_ref)
        args.registry.write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        return 0
    obstacles = [item for path in args.runtime for item in read_runtime(path)]
    obstacles += [item for path in args.mailbox for item in read_mailbox(path)]
    offers = evaluate(obstacles, registry, set(args.new_evidence))
    if args.record_offers:
        record_offers(registry, offers)
        args.registry.write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"offers": offers}, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
