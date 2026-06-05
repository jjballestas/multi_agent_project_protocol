# Codex Memory

Last updated: 2026-06-05

## Repository

`multi_agent_project_protocol` is the canonical, domain-neutral repository for the reusable
multi-agent software project protocol.

It dogfoods itself:

- `AGENTS.md` is the live project contract.
- `AGENTS.template.md` is the shipped template master.
- `protocol.config.json` is the live instance config.
- `protocol.config.template.json` is the shipped template master.
- `Area_comun/` contains the protocol docs and will contain live project state once initialized.

Pilot applied instance:

- `bot_spot_ai_strategy_pack`

## Current Sync Notes

- The live dogfood instance has been initialized by Claude.
- `TASK-0002` is delivered by Codex and left in `in_review`.
- TASK-0002 deliverables:
  - `scripts/validate_collaboration_state.py`
  - `.github/workflows/validate.yml`
  - `Area_comun/handoffs/HANDOFF-TASK-0002-codex-to-claude-1.md`
- The Python validator is stdlib-only and mirrors the PowerShell validator.
- Validation performed before closing:
  - `python scripts\validate_collaboration_state.py --root .`
  - `python scripts\validate_collaboration_state.py --root examples\minimal_instance`
  - `powershell -NoProfile -File scripts\validate_collaboration_state.ps1`
  - `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance`
- Temporary negative cases checked: broken state invariant, task status mismatch, missing
  deliverable.

## Startup Checklist

1. Read `AGENTS.md`.
2. Read `Area_comun/README.md` or `Area_comun/README.template.md` if the live README is not
   created yet.
3. Check for live state:
   - `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.json`
4. Check `Area_comun/mailbox/open/`.
5. Check `git status --short --branch`.
6. Do not edit routes with another active claim.
7. If TASK-0002 is still `in_review`, wait for Claude review before claiming new implementation
   tasks unless the operator explicitly redirects.

## Safety Notes

- Keep the protocol core domain-neutral.
- Do not introduce secrets.
- Do not change backward compatibility or release policy without a decision.
- Prefer creating explicit tasks/claims before shared edits once the live state exists.
