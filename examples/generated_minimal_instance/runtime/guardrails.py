#!/usr/bin/env python3
"""Guardrails for untrusted runtime content.

Untrusted handoffs, task inputs, and tool outputs are data. They can be
preserved, scanned, and logged, but they do not grant authority.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


TRUSTED_SOURCE_KINDS = {"registry", "state", "config"}
UNTRUSTED_SOURCE_KINDS = {"handoff", "task_input", "tool_output"}
CONTAINMENT_EVENT = "security.handoff_injection_contained"


INJECTION_RULES = [
    {
        "rule_id": "protocol_override",
        "category": "protocol",
        "patterns": [
            r"\b(ignore|disregard|override|bypass)\b.{0,48}\b(protocol|instructions|rules|policy|validator|guardrail)s?\b",
            r"\b(ignora|ignorar|omite|omitir|salta|saltar)\b.{0,48}\b(protocolo|instrucciones|reglas|politica|validador)\b",
        ],
    },
    {
        "rule_id": "scope_expansion",
        "category": "scope",
        "patterns": [
            r"\b(outside|beyond)\b.{0,40}\b(scope|claim|allowlist)\b",
            r"\b(edit|write|modify|change)\b.{0,48}\b(outside|beyond)\b.{0,32}\b(scope|claim|allowlist)\b",
            r"\b(fuera|saltar|saltate|editar|edita)\b.{0,48}\b(scope|claim|alcance)\b",
        ],
    },
    {
        "rule_id": "authority_grant",
        "category": "authority",
        "patterns": [
            r"\b(grant|give|add|assign|set|make)\b.{0,40}\b(capability|permission|role|owner)\b",
            r"\b(concede|conceder|asigna|asignar|cambia|cambiar|fija|fijar)\b.{0,40}\b(capacidad|permiso|rol|owner|propietario)\b",
        ],
    },
    {
        "rule_id": "forced_escalation",
        "category": "escalation",
        "patterns": [
            r"\b(force|require|trigger|set)\b.{0,40}\b(approval|approve|escalation|human_required|human gate)\b",
            r"\b(forzar|fuerza|requiere|aprobar|escala|escalar)\b.{0,40}\b(aprobacion|escalado|humano)\b",
        ],
    },
    {
        "rule_id": "review_qa_bypass",
        "category": "quality",
        "patterns": [
            r"\b(skip|bypass|disable)\b.{0,40}\b(review|qa|validation|validator)\b",
            r"\b(salta|saltar|omite|omitir|desactiva|desactivar)\b.{0,40}\b(review|qa|revision|validacion|validador)\b",
        ],
    },
]


def classify_provenance(source_kind: str | None) -> str:
    """Classify a content source as trusted or untrusted.

    Unknown source kinds are untrusted by default.
    """

    normalized = str(source_kind or "").strip().lower()
    if normalized in TRUSTED_SOURCE_KINDS:
        return "trusted"
    return "untrusted"


def canonical_excerpt(text: str, start: int, end: int, *, limit: int = 80) -> str:
    excerpt = re.sub(r"\s+", " ", text[start:end]).strip()
    if len(excerpt) <= limit:
        return excerpt
    return excerpt[: limit - 3].rstrip() + "..."


def scan_injection(text: Any) -> list[dict[str, Any]]:
    """Return deterministic injection findings for protocol-level hijacking."""

    if not isinstance(text, str) or not text.strip():
        return []
    findings: list[dict[str, Any]] = []
    for rule in INJECTION_RULES:
        for pattern in rule["patterns"]:
            regex = re.compile(pattern, flags=re.IGNORECASE | re.DOTALL)
            for match in regex.finditer(text):
                finding = {
                    "rule_id": rule["rule_id"],
                    "category": rule["category"],
                    "span": [match.start(), match.end()],
                    "excerpt": canonical_excerpt(text, match.start(), match.end()),
                }
                if finding not in findings:
                    findings.append(finding)
    return sorted(findings, key=lambda item: (item["span"][0], item["rule_id"], item["span"][1]))


def read_text_if_exists(root: Path, relative_path: str) -> str | None:
    path = (root / relative_path).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8-sig")


def sources_from_turn_report(report: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    """Collect untrusted content referenced by a turn report."""

    sources: list[dict[str, Any]] = []
    transitions = report.get("transitions") or {}
    handoff = transitions.get("handoff")
    if isinstance(handoff, str) and handoff.strip():
        content = read_text_if_exists(root, handoff.strip())
        if content is not None:
            sources.append({"source_kind": "handoff", "path": handoff.strip(), "content": content})
    return sources


def report_requests_escalation(report: dict[str, Any]) -> bool:
    if report.get("outcome") in {"decision_required", "human_required"}:
        return True
    gate = report.get("gate") or {}
    if isinstance(gate, dict) and gate.get("human_required") is True:
        return True
    transition = (report.get("transitions") or {}).get("task_status")
    return isinstance(transition, dict) and transition.get("to") == "architect_review"


def trusted_quality_escalation(report: dict[str, Any], state: dict[str, Any]) -> bool:
    transition = (report.get("transitions") or {}).get("task_status")
    review_qa = (report.get("transitions") or {}).get("review_qa")
    if not isinstance(transition, dict) or transition.get("to") != "architect_review":
        return False
    if not isinstance(review_qa, dict) or review_qa.get("event") != "fail_qa":
        return False
    task_id = report.get("task_id")
    tasks = {
        item.get("id"): item
        for item in (state.get("task_index", {}).get("tasks") or [])
        if isinstance(item, dict) and item.get("id")
    }
    task = tasks.get(task_id) or {}
    try:
        attempts = int(task.get("qa_attempts") or 0)
    except (TypeError, ValueError):
        attempts = 0
    config = state.get("config") or {}
    policy = config.get("quality_policy") or {}
    try:
        max_cycles = int(policy.get("max_qa_cycles") or 3)
    except (TypeError, ValueError):
        max_cycles = 3
    return attempts >= max_cycles or bool(task.get("defect_log"))


def contain_untrusted(
    report: dict[str, Any],
    state: dict[str, Any],
    registry: dict[str, Any],
    sources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Contain injection attempts from untrusted sources.

    Returns a deterministic report with findings, containment events, and
    semantic errors for security effects that rely only on untrusted content.
    """

    del registry  # Authority comes from the caller's trusted registry checks.
    all_sources = list(sources or [])
    findings: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    errors: list[str] = []

    for index, source in enumerate(all_sources):
        source_kind = str(source.get("source_kind") or "")
        provenance = classify_provenance(source_kind)
        source_findings = scan_injection(source.get("content") or "")
        for finding in source_findings:
            enriched = {
                **finding,
                "source_index": index,
                "source_kind": source_kind,
                "provenance": provenance,
            }
            if source.get("path"):
                enriched["path"] = str(source["path"])
            findings.append(enriched)
        if provenance == "untrusted" and source_findings:
            events.append(
                {
                    "event": CONTAINMENT_EVENT,
                    "source_index": index,
                    "source_kind": source_kind,
                    "finding_count": len(source_findings),
                }
            )

    untrusted_categories = {
        finding["category"]
        for finding in findings
        if finding.get("provenance") == "untrusted"
    }
    if "escalation" in untrusted_categories and report_requests_escalation(report):
        if not trusted_quality_escalation(report, state):
            errors.append("guardrail: untrusted content cannot request or justify escalation")

    return {
        "findings": sorted(findings, key=lambda item: (item.get("source_index", 0), item["span"][0], item["rule_id"])),
        "events": sorted(events, key=lambda item: (item["source_index"], item["event"])),
        "errors": errors,
    }
