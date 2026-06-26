#!/usr/bin/env python3
"""Read-only cold-start loader for governed skill documents."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SkillLoaderError(ValueError):
    """Raised when the skill registry or an enabled skill fails closed."""


@dataclass(frozen=True)
class LoadedSkill:
    skill_id: str
    title: str
    profile: str | None
    neutral_core: bool
    path: str
    version: str
    procedure: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.skill_id,
            "title": self.title,
            "profile": self.profile,
            "neutral_core": self.neutral_core,
            "path": self.path,
            "version": self.version,
            "procedure": self.procedure,
        }


def load_skills(root: Path | str = ".", registry_path: Path | str | None = None) -> dict[str, Any]:
    """Load enabled skills into memory without writing protocol state."""

    root_path = Path(root).resolve()
    registry = Path(registry_path) if registry_path is not None else root_path / "skills" / "skills.config.json"
    if not registry.is_absolute():
        registry = (root_path / registry).resolve()
    if not registry.exists():
        return {"schema_version": "skills.loaded.v1", "skills": []}

    payload = json.loads(registry.read_text(encoding="utf-8-sig"))
    if payload.get("schema_version") != "skills.config.v1":
        raise SkillLoaderError("skills registry schema_version must be skills.config.v1")
    entries = payload.get("skills")
    if not isinstance(entries, list):
        raise SkillLoaderError("skills registry must contain a skills list")

    loaded: list[LoadedSkill] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise SkillLoaderError("skill registry entry must be an object")
        if entry.get("enabled") is not True:
            continue
        loaded.append(_load_entry(root_path, entry))

    return {
        "schema_version": "skills.loaded.v1",
        "skills": [item.as_dict() for item in sorted(loaded, key=lambda skill: skill.skill_id)],
    }


def _load_entry(root: Path, entry: dict[str, Any]) -> LoadedSkill:
    skill_id = _required_text(entry, "id")
    title = _required_text(entry, "title")
    version = _required_text(entry, "version")
    relative_path = _required_text(entry, "path")
    neutral_core = entry.get("neutral_core") is True
    profile = entry.get("profile")
    if profile is not None:
        profile = _clean_text(profile, "profile")
    if neutral_core == bool(profile):
        raise SkillLoaderError(f"{skill_id}: declare exactly one of neutral_core:true or profile")
    _validate_trust_boundary(skill_id, entry.get("trust_boundary"))
    skill_path = _resolve_skill_path(root, relative_path)
    if neutral_core:
        _require_under(skill_id, root / "skills", skill_path)
    else:
        expected = root / "profiles" / str(profile) / "skills"
        _require_under(skill_id, expected, skill_path)

    metadata, procedure = _read_skill_doc(skill_path)
    _validate_metadata(skill_id, title, version, profile, neutral_core, metadata)
    if neutral_core:
        _reject_core_domain_terms(root, skill_path, procedure)
    return LoadedSkill(
        skill_id=skill_id,
        title=title,
        profile=str(profile) if profile else None,
        neutral_core=neutral_core,
        path=skill_path.relative_to(root).as_posix(),
        version=version,
        procedure=procedure,
    )


def _required_text(payload: dict[str, Any], key: str) -> str:
    if key not in payload:
        raise SkillLoaderError(f"missing required field: {key}")
    return _clean_text(payload[key], key)


def _clean_text(value: Any, key: str) -> str:
    text = str(value).strip()
    if not text:
        raise SkillLoaderError(f"{key} must not be empty")
    return text


def _validate_trust_boundary(skill_id: str, boundary: Any) -> None:
    if not isinstance(boundary, dict):
        raise SkillLoaderError(f"{skill_id}: trust_boundary must be an object")
    if boundary.get("read_only") is not True:
        raise SkillLoaderError(f"{skill_id}: trust_boundary.read_only must be true")
    if boundary.get("grants_no_authority") is not True:
        raise SkillLoaderError(f"{skill_id}: trust_boundary.grants_no_authority must be true")
    if boundary.get("persists_outputs") is not False:
        raise SkillLoaderError(f"{skill_id}: trust_boundary.persists_outputs must be false")


def _resolve_skill_path(root: Path, relative_path: str) -> Path:
    candidate = Path(relative_path)
    if candidate.is_absolute():
        raise SkillLoaderError("skill path must be relative")
    resolved = (root / candidate).resolve()
    _require_under("path", root, resolved)
    return resolved


def _require_under(skill_id: str, parent: Path, child: Path) -> None:
    try:
        child.relative_to(parent.resolve())
    except ValueError as exc:
        raise SkillLoaderError(f"{skill_id}: path outside allowed skill location") from exc


def _read_skill_doc(path: Path) -> tuple[dict[str, str], str]:
    if not path.exists() or not path.is_file():
        raise SkillLoaderError(f"skill document not found: {path}")
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---\n"):
        raise SkillLoaderError("skill document must start with frontmatter")
    try:
        _, raw_meta, body = text.split("---\n", 2)
    except ValueError as exc:
        raise SkillLoaderError("skill document frontmatter is not closed") from exc
    metadata: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise SkillLoaderError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    procedure = body.strip()
    if not procedure:
        raise SkillLoaderError("skill procedure body must not be empty")
    return metadata, procedure


def _validate_metadata(
    skill_id: str,
    title: str,
    version: str,
    profile: str | None,
    neutral_core: bool,
    metadata: dict[str, str],
) -> None:
    if metadata.get("skill_id") != skill_id:
        raise SkillLoaderError(f"{skill_id}: frontmatter skill_id mismatch")
    if metadata.get("title") != title:
        raise SkillLoaderError(f"{skill_id}: frontmatter title mismatch")
    if metadata.get("version") != version:
        raise SkillLoaderError(f"{skill_id}: frontmatter version mismatch")
    if neutral_core:
        if metadata.get("neutral_core", "").lower() != "true":
            raise SkillLoaderError(f"{skill_id}: neutral core skill must declare neutral_core:true")
        if metadata.get("profile"):
            raise SkillLoaderError(f"{skill_id}: neutral core skill must not declare profile")
    elif metadata.get("profile") != profile:
        raise SkillLoaderError(f"{skill_id}: frontmatter profile mismatch")


def _reject_core_domain_terms(root: Path, path: Path, text: str) -> None:
    config_path = root / "protocol.config.json"
    if not config_path.exists():
        return
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    neutrality = config.get("domain_neutrality") if isinstance(config.get("domain_neutrality"), dict) else {}
    denylist = [str(term).strip() for term in neutrality.get("denylist") or [] if str(term).strip()]
    for term in denylist:
        if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, re.IGNORECASE):
            raise SkillLoaderError(f"{path.relative_to(root).as_posix()}: domain term rejected in core skill")
