"""Conservative read-only SQL classifier."""

from __future__ import annotations

import re
from dataclasses import dataclass


class Decision:
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class Classification:
    decision: str
    reason_class: str
    normalized: str


DML = {"INSERT", "UPDATE", "DELETE", "MERGE"}
DDL = {"CREATE", "ALTER", "DROP", "TRUNCATE"}


def normalize_sql(sql: str) -> str:
    return " ".join(str(sql or "").strip().split())


def _mask_string_literals(sql: str) -> str:
    chars: list[str] = []
    in_quote = False
    index = 0
    while index < len(sql):
        char = sql[index]
        if char == "'":
            chars.append(" ")
            if in_quote and index + 1 < len(sql) and sql[index + 1] == "'":
                chars.append(" ")
                index += 2
                continue
            in_quote = not in_quote
            index += 1
            continue
        chars.append(" " if in_quote else char)
        index += 1
    return "".join(chars)


def _has_multiple_statements(sql: str) -> bool:
    masked = _mask_string_literals(sql)
    parts = [part.strip() for part in masked.split(";")]
    return len([part for part in parts if part]) > 1


def _first_keyword(sql: str) -> str:
    match = re.match(r"\s*(?:--[^\n]*\n\s*)*(/\*.*?\*/\s*)*([A-Za-z_][A-Za-z0-9_]*)", sql, re.DOTALL)
    return match.group(2).upper() if match else ""


def _referenced_objects(sql: str) -> set[str]:
    objects: set[str] = set()
    for match in re.finditer(r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_\.\[\]]*)", sql, re.IGNORECASE):
        value = match.group(1).strip("[]").replace("[", "").replace("]", "")
        if "." in value:
            objects.add(value.lower())
    return objects


def _exec_name(sql: str) -> str:
    match = re.match(r"\s*EXEC(?:UTE)?\s+([A-Za-z_][A-Za-z0-9_\.\[\]]*)", sql, re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip("[]").replace("[", "").replace("]", "").lower()


def classify_readonly_sql(
    sql: str,
    *,
    allowed_objects: set[str] | None = None,
    allowed_procedures: set[str] | None = None,
) -> Classification:
    normalized = normalize_sql(sql)
    if not normalized:
        return Classification(Decision.DENY, "empty_operation", normalized)
    if _has_multiple_statements(normalized):
        return Classification(Decision.DENY, "multi_statement", normalized)

    keyword = _first_keyword(normalized)
    if keyword in DML:
        return Classification(Decision.DENY, "dml", normalized)
    if keyword in DDL:
        return Classification(Decision.DENY, "ddl", normalized)
    if keyword in {"EXEC", "EXECUTE"}:
        proc = _exec_name(normalized)
        if proc and proc in {item.lower() for item in (allowed_procedures or set())}:
            return Classification(Decision.ALLOW, "read_procedure", normalized)
        return Classification(Decision.DENY, "exec_not_allowlisted", normalized)
    if keyword != "SELECT":
        return Classification(Decision.DENY, "unknown_verb", normalized)

    allowed = {item.lower() for item in (allowed_objects or set())}
    referenced = _referenced_objects(normalized)
    if referenced and not referenced.issubset(allowed):
        return Classification(Decision.DENY, "object_not_allowlisted", normalized)
    return Classification(Decision.ALLOW, "select", normalized)
