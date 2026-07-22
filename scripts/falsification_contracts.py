#!/usr/bin/env python3
"""Machine-readable contracts for permanent negative tests.

A runner owns the actual mutation and assertion.  This module validates the declaration
shape and makes assertion boundaries explicit enough for a repository-wide inventory.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


REQUIRED_FIELDS = ("id", "negative", "mutation", "boundaries", "exercised_by")


@dataclass(frozen=True)
class FalsificationContract:
    id: str
    negative: str
    mutation: str
    boundaries: tuple[str, ...]
    exercised_by: str

    @classmethod
    def from_mapping(cls, raw: Mapping[str, object]) -> "FalsificationContract":
        missing = [field for field in REQUIRED_FIELDS if not raw.get(field)]
        if missing:
            raise ValueError(f"falsification contract missing fields: {missing}")
        boundaries = raw["boundaries"]
        if not isinstance(boundaries, (list, tuple)) or not all(isinstance(item, str) and item for item in boundaries):
            raise ValueError("falsification contract boundaries must be a non-empty string sequence")
        return cls(
            id=str(raw["id"]),
            negative=str(raw["negative"]),
            mutation=str(raw["mutation"]),
            boundaries=tuple(boundaries),
            exercised_by=str(raw["exercised_by"]),
        )


def validate_contracts(raw_contracts: Iterable[Mapping[str, object]]) -> list[FalsificationContract]:
    contracts = [FalsificationContract.from_mapping(raw) for raw in raw_contracts]
    ids = [contract.id for contract in contracts]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        raise ValueError(f"duplicate falsification contract ids: {duplicates}")
    return contracts
