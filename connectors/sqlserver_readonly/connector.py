"""SQL Server read-only connector with fixture backend."""

from __future__ import annotations

import json
import os
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


class LivePymssqlBackend:
    """Minimal pymssql backend for live read-only verification."""

    def __init__(self, connection: Any) -> None:
        self.connection = connection
        self.calls: list[str] = []

    def execute_read(self, query: str) -> list[dict[str, Any]]:
        self.calls.append(FixtureBackend._key(query))
        cursor = self.connection.cursor(as_dict=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def execute_unclassified(self, query: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()


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

    def open_live(self, env_path: Path | str | None = None) -> "SqlServerReadOnlyConnector":
        if not self.enabled:
            raise ConnectorDisabledError("live connector disabled")
        self.backend = LivePymssqlBackend(open_live_connection(env_path=env_path))
        return self

    def execute_unclassified_for_s9(self, operation: str) -> None:
        if not isinstance(self.backend, LivePymssqlBackend):
            raise ConnectorDisabledError("live backend not configured")
        self.backend.execute_unclassified(operation)


def _parse_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def load_env_file(path: Path | str | None) -> dict[str, str]:
    values: dict[str, str] = {}
    if path is None:
        return values
    env_path = Path(path)
    if not env_path.exists():
        raise ConnectorDisabledError("live env file not found")
    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def live_env(env_path: Path | str | None = None) -> dict[str, str]:
    values = load_env_file(env_path)
    merged = {**values, **{key: value for key, value in os.environ.items() if key.startswith("SQLSERVER_")}}
    required = [
        "SQLSERVER_HOST",
        "SQLSERVER_PORT",
        "SQLSERVER_DATABASE",
        "SQLSERVER_USER",
        "SQLSERVER_PASSWORD",
    ]
    missing = [key for key in required if not str(merged.get(key) or "").strip()]
    if missing:
        raise ConnectorDisabledError(f"missing live env keys: {', '.join(missing)}")
    if not _parse_bool(merged.get("SQLSERVER_READONLY"), default=False):
        raise ConnectorDisabledError("SQLSERVER_READONLY=true is required")
    return merged


def open_live_connection(env_path: Path | str | None = None) -> Any:
    try:
        import pymssql  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - depends on operator environment
        raise ConnectorDisabledError("pymssql is required for live SQL Server connections") from exc

    env = live_env(env_path)
    try:
        port = int(env["SQLSERVER_PORT"])
    except ValueError as exc:
        raise ConnectorDisabledError("SQLSERVER_PORT must be an integer") from exc
    return pymssql.connect(
        server=env["SQLSERVER_HOST"],
        port=port,
        user=env["SQLSERVER_USER"],
        password=env["SQLSERVER_PASSWORD"],
        database=env["SQLSERVER_DATABASE"],
        appname="multi-agent-protocol-sqlserver-readonly",
        login_timeout=10,
        timeout=30,
        as_dict=True,
    )


def resolve_config_path(path: Path) -> Path:
    runtime_path = path.with_name("connectors.runtime.json")
    return runtime_path if runtime_path.exists() else path


def load_connector_from_config(
    path: Path,
    connector_id: str,
    *,
    backend: FixtureBackend | None = None,
) -> SqlServerReadOnlyConnector:
    config = json.loads(resolve_config_path(path).read_text(encoding="utf-8-sig"))
    for entry in config.get("connectors") or []:
        if isinstance(entry, dict) and entry.get("id") == connector_id:
            return SqlServerReadOnlyConnector(
                connector_id=connector_id,
                enabled=entry.get("enabled") is True,
                trust_boundary=TrustBoundary.from_dict(entry.get("trust_boundary") or {}),
                backend=backend,
            )
    raise KeyError(f"connector not found: {connector_id}")
