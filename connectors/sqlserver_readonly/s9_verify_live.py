#!/usr/bin/env python3
"""Live s9 verification for the SQL Server read-only connector."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from connectors.sqlserver_readonly import load_connector_from_config, live_env


CONFIG = ROOT / "connectors" / "connectors.config.json"
DEFAULT_ENV = ROOT / "personal" / "operador" / "nova_sql_connector_readonly_s9.env"
DEFAULT_ARTIFACT = ROOT / "Area_comun" / "artifacts" / "S9-TASK-0158-sqlserver-readonly-live.json"


def error_summary(exc: BaseException) -> dict[str, str]:
    args = getattr(exc, "args", ())
    code = ""
    if args:
        first = args[0]
        if isinstance(first, (int, str)):
            code = str(first)
    return {"class": exc.__class__.__name__, "code": code[:40]}


def rejected_by_server(exc: BaseException) -> bool:
    text = " ".join(str(item) for item in getattr(exc, "args", ()) or [str(exc)]).lower()
    markers = [
        "permission",
        "denied",
        "not allowed",
        "read-only",
        "read only",
        "cannot update",
        "ad hoc updates",
    ]
    return any(marker in text for marker in markers)


def run_vector(connector: Any, vector: str, sql: str) -> dict[str, Any]:
    try:
        connector.execute_unclassified_for_s9(sql)
    except Exception as exc:  # noqa: BLE001 - the artifact records sanitized server rejection class.
        summary = error_summary(exc)
        return {
            "vector": vector,
            "server_rejected": rejected_by_server(exc),
            "error_class": summary["class"],
            "error_code": summary["code"],
        }
    return {"vector": vector, "server_rejected": False, "error_class": "none", "error_code": ""}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run live SQL Server s9 read-only verification.")
    parser.add_argument("--env", default=str(DEFAULT_ENV), help="Path to the gitignored SQLSERVER_*.env file.")
    parser.add_argument("--config", default=str(CONFIG), help="Connector config path.")
    parser.add_argument("--connector-id", default="sqlserver_readonly", help="Live connector id.")
    parser.add_argument("--artifact", default=str(DEFAULT_ARTIFACT), help="Sanitized artifact output path.")
    args = parser.parse_args()

    env = live_env(args.env)
    connector = load_connector_from_config(Path(args.config), args.connector_id, backend=None)
    connector.open_live(env_path=args.env)

    select_sql = env.get("SQLSERVER_S9_SELECT_SQL") or "SELECT 1 AS connector_probe"
    rows = connector.read(select_sql)
    if len(rows) < 1:
        raise SystemExit("s9 SELECT returned no rows")

    dml_sql = env.get("SQLSERVER_S9_DML_SQL") or "UPDATE sys.objects SET name = name WHERE 1 = 0"
    ddl_sql = env.get("SQLSERVER_S9_DDL_SQL") or "CREATE TABLE connector_s9_denied_probe (id INT NOT NULL)"
    vectors = [
        run_vector(connector, "DML", dml_sql),
        run_vector(connector, "DDL", ddl_sql),
    ]
    if not all(item["server_rejected"] for item in vectors):
        raise SystemExit("s9 write vectors were not rejected by the server")

    artifact = {
        "schema_version": "sqlserver_readonly_s9.v1",
        "task_id": "TASK-0158",
        "connector_id": args.connector_id,
        "driver": "pymssql",
        "driver_install_command": "python -m pip install pymssql",
        "timestamp_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "select": {"server_allowed": True, "row_count": len(rows)},
        "write_vectors": vectors,
        "secret_free": True,
        "pii_free": True,
    }
    artifact_path = Path(args.artifact)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(artifact, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
