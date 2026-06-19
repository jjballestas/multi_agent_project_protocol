"""SQL Server read-only connector with fixture backend."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from connectors.framework import (
    Connector,
    ConnectorDisabledError,
    Decision,
    ReadOnlyDeniedError,
    TrustBoundary,
    classify_readonly_sql,
)


class FixtureBackend:
    """Deterministic in-memory backend used by golden tests."""

    def __init__(self, rows_by_query: dict[str, list[dict[str, Any]]]) -> None:
        self.rows_by_query = {self._key(key): deepcopy(value) for key, value in rows_by_query.items()}
        self.calls: list[str] = []

    @staticmethod
    def _key(query: str) -> str:
        return " ".join(str(query or "").strip().split()).lower().rstrip(";")

    def execute_read(self, query: str) -> list[dict[str, Any]]:
        key = self._key(query)
        self.calls.append(key)
        return deepcopy(self.rows_by_query.get(key, []))


class SqlServerReadOnlyConnector(Connector):
    def __init__(
        self,
        *,
        connector_id: str,
        trust_boundary: TrustBoundary,
        enabled: bool,
        backend: FixtureBackend | None = None,
        allowed_procedures: set[str] | None = None,
    ) -> None:
        super().__init__(connector_id=connector_id, trust_boundary=trust_boundary, enabled=enabled)
        self.backend = backend
        self.allowed_procedures = {item.lower() for item in (allowed_procedures or set())}

    def read(self, operation: str) -> list[dict[str, Any]]:
        classification = classify_readonly_sql(
            operation,
            allowed_objects=set(self.trust_boundary.allowed_objects),
            allowed_procedures=self.allowed_procedures,
        )
        if classification.decision != Decision.ALLOW:
            raise ReadOnlyDeniedError(classification.reason_class, f"read-only denied: {classification.reason_class}")
        if self.backend is None:
            if not self.enabled:
                raise ConnectorDisabledError("live connector disabled")
            raise ConnectorDisabledError("live backend not configured")
        return self.backend.execute_read(classification.normalized)

    def open_live(self) -> None:
        if not self.enabled:
            raise ConnectorDisabledError("live connector disabled")
        raise ConnectorDisabledError("live backend requires a later operator GO")


def load_connector_from_config(
    path: Path,
    connector_id: str,
    *,
    backend: FixtureBackend | None = None,
) -> SqlServerReadOnlyConnector:
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    for entry in config.get("connectors") or []:
        if isinstance(entry, dict) and entry.get("id") == connector_id:
            return SqlServerReadOnlyConnector(
                connector_id=connector_id,
                enabled=entry.get("enabled") is True,
                trust_boundary=TrustBoundary.from_dict(entry.get("trust_boundary") or {}),
                backend=backend,
            )
    raise KeyError(f"connector not found: {connector_id}")
