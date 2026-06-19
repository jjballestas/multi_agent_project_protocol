"""Base connector contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .trust_boundary import TrustBoundary


class Connector(ABC):
    """Read-only connector interface."""

    def __init__(self, *, connector_id: str, trust_boundary: TrustBoundary, enabled: bool = False) -> None:
        self.connector_id = connector_id
        self.trust_boundary = trust_boundary
        self.enabled = bool(enabled)

    @abstractmethod
    def read(self, operation: str) -> list[dict[str, Any]]:
        """Return in-memory evidence for a read operation."""
