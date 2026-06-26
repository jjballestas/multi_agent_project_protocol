---
handoff_id: HANDOFF-TASK-0184-codex-to-arquitecto-1
task_id: TASK-0184
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-26
implementation_commit: d589318
---

# Handoff TASK-0184 - profile skills content

## Summary

Implemented SPEC-0097 AC1-AC6 in the protocol repo.

- Added minimal profile shell: `profiles/financiero_presupuesto/profile.manifest.json`.
- Added three profile-hosted skill documents:
  - `profiles/financiero_presupuesto/skills/ddl-conventions.skill.md`
  - `profiles/financiero_presupuesto/skills/business-rule-vs-legacy.skill.md`
  - `profiles/financiero_presupuesto/skills/migration-verification.skill.md`
- Registered all three in `skills/skills.config.json` as `enabled:false`, `neutral_core:false`,
  `profile: financiero_presupuesto`, with read-only/no-authority/no-persistence trust boundaries.
- Hardened `skills/loader.py` so profile skills must declare `neutral_core:false` in frontmatter.
- Extended `examples/skills_loader_cases/run_skills_loader_cases.py` with an AC6 golden that enables only the
  three profile skills in a fixture, loads them through the loader, verifies deterministic output, and validates
  path containment under `profiles/financiero_presupuesto/skills/`.

## Evidence

- `python -m py_compile skills/loader.py examples/skills_loader_cases/run_skills_loader_cases.py` OK.
- `python examples/skills_loader_cases/run_skills_loader_cases.py` PASS, including
  `AC6-profile-skills-load-under-profile` with 3 loaded skills.
- `python scripts/scan_encoding.py --root .` OK.
- `python scripts/scan_domain_neutrality.py --root .` OK.
- `python scripts/validate_collaboration_state.py --root .` OK.
- `powershell -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` OK.
- `git diff --check -- skills/loader.py skills/skills.config.json examples/skills_loader_cases/run_skills_loader_cases.py profiles/financiero_presupuesto` OK.
- Drift false / #4 byte-identica at `up_to_seq` 2031 after implementation.

## Boundary Notes

- `protocol.config.json` and chain genesis were not changed.
- The skills remain off-by-default.
- The profile shell contains only manifest + skills; no domain policy docs/prompts/templates were added.
- No product repo changes were made.
