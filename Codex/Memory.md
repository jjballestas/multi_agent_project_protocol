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

- Claude appears to be initializing the live protocol instance in this repo.
- Current observed changes before this file was created:
  - `protocol.config.json` staged as renamed to `protocol.config.template.json`;
  - new untracked `AGENTS.md`;
  - new untracked live `protocol.config.json`;
  - no live `Area_comun/state/TASK_INDEX.json` yet;
  - no live `Area_comun/state/CLAIMS.json` yet.
- Because live task/claim state is not initialized yet, Codex must avoid editing shared
  protocol/state files unless the operator explicitly asks or Claude finishes the bootstrap.

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

## Safety Notes

- Keep the protocol core domain-neutral.
- Do not introduce secrets.
- Do not change backward compatibility or release policy without a decision.
- Prefer creating explicit tasks/claims before shared edits once the live state exists.

