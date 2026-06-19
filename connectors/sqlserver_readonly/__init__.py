"""SQL Server read-only connector."""

from .connector import FixtureBackend, SqlServerReadOnlyConnector, load_connector_from_config

__all__ = ["FixtureBackend", "SqlServerReadOnlyConnector", "load_connector_from_config"]
