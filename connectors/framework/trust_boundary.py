"""Trust-boundary descriptor for connectors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .errors import TrustBoundaryError


@dataclass(frozen=True)
class TrustBoundary:
    read_only: bool
    grants_no_authority: bool
    persists_outputs: bool
    allowed_schemas: tuple[str, ...]
    allowed_objects: tuple[str, ...]
    live_principal_least_privilege_required: bool = True

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TrustBoundary":
        access = payload.get("access") if isinstance(payload.get("access"), dict) else {}
        allow = access.get("allow") if isinstance(access.get("allow"), dict) else {}
        live = payload.get("live_connection") if isinstance(payload.get("live_connection"), dict) else {}
        boundary = cls(
            read_only=payload.get("read_only") is True,
            grants_no_authority=payload.get("grants_no_authority") is True,
            persists_outputs=payload.get("persists_outputs") is True,
            allowed_schemas=tuple(str(item).lower() for item in allow.get("schemas") or [] if str(item).strip()),
            allowed_objects=tuple(str(item).lower() for item in allow.get("objects") or [] if str(item).strip()),
            live_principal_least_privilege_required=live.get("principal_least_privilege_required") is True,
        )
        boundary.validate()
        return boundary

    def validate(self) -> None:
        if not self.read_only:
            raise TrustBoundaryError("trust_boundary.read_only must be true")
        if not self.grants_no_authority:
            raise TrustBoundaryError("trust_boundary.grants_no_authority must be true")
        if self.persists_outputs:
            raise TrustBoundaryError("trust_boundary.persists_outputs must be false")
        if not self.allowed_objects:
            raise TrustBoundaryError("trust_boundary.access.allow.objects must not be empty")
        if not self.live_principal_least_privilege_required:
            raise TrustBoundaryError("live principal least privilege must be required")
