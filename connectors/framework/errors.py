"""Connector error classes."""


class ConnectorError(RuntimeError):
    """Base connector error."""


class TrustBoundaryError(ConnectorError):
    """The connector declaration violates its trust boundary."""


class ReadOnlyDeniedError(ConnectorError):
    """The read-only classifier denied an operation before backend access."""

    def __init__(self, reason_class: str, message: str) -> None:
        super().__init__(message)
        self.reason_class = reason_class


class ConnectorDisabledError(ConnectorError):
    """A live connector path was requested while the connector is disabled."""
