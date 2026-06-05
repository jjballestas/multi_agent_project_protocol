# AGENTS.md — Shared source of truth for multi_agent_project_protocol

> This file is the project contract. All agents (Claude, Codex) and the human owner read and
> obey it. If a one-off instruction conflicts with this file, this file wins unless the human
> owner explicitly overrides it and records a decision in `Area_comun/decisions/`.
>
> **Dogfooding note:** this repository applies its **own protocol** to its own development. The
> shipped masters for new projects are the `*.template.*` files; this `AGENTS.md` and the
> canonical `Area_comun/state/*.json` are **this project's live instance**.
>
> Last updated: 2026-06-05 · Maintainer: Claude (architect) + human owner. Released version: v0.5.0.

## 0. How to Start

An agent entering cold can operate by reading only:

1. `AGENTS.md`.
2. `Area_comun/` in this order:
   - `Area_comun/README.md`
   - `Area_comun/protocol/TASK_PROTOCOL.md`
   - `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.json`
   - `Area_comun/mailbox/open/`
   - the concrete file in `Area_comun/tasks/`.

Never assume another agent knows your context. Every task and handoff must be self-contained.

## 1. Project Goal

Maintain and **enrich a reusable, domain-neutral multi-agent project protocol** for software
work: task lifecycle, claims, mailbox, handoffs, decisions, human reports and a state validator.
First applied instance (pilot): `bot_spot_ai_strategy_pack` (trading bot, separate repo).

## 2. Current Phase and Scope

- Phase id: `P2`
- Phase name: `Adoption and expansion`
- Phase goal: help real instances adopt the protocol and its profiles, add more profiles/examples
  and docs as needed, and maintain the core — all additively and keeping the core domain-neutral.
  No active breaking work.
- Previous phase `P1` (Professional profiles architecture) closed with the **v0.3.0** release:
  core/profiles/examples layering (DECISION-0002), the `dotnet_enterprise` profile, and the
  `adopted_profiles` contract + profile-aware validators (DECISION-0003).
- Previous phase `P0` (Protocol enrichment) closed with the **v0.2.0** release (cross-platform
  validator + CI, SemVer/CHANGELOG/`protocol_version`, scaffolding script).

In scope: instance adoption support, new profiles/examples, docs, maintenance, versioning.
Out of scope: any business/domain logic in the core (the core stays neutral; stack-specific
content lives only under `profiles/`).

## 3. Agent Roles

| Agent | Main role | Does | Does not do |
|-------|-----------|------|-------------|
| `Claude` | Architect / orchestrator | Designs, reviews, decomposes tasks, keeps the protocol coherent and domain-neutral | Does not own implementation-only work unless assigned |
| `Codex` | Implementation specialist | Scaffolding, scripts, validator, CI, tests, concrete proposals | Does not change protocol/boundaries without a decision |
| `operador humano` | Human owner | Approves protocol policy, breaking changes and releases | — |

## 4. Hard Project Boundaries

- The protocol **core must remain DOMAIN-NEUTRAL**: no trading/business terms, no secrets, no
  domain policy baked into the generic files.
- **Backward-incompatible** protocol changes require a decision in `Area_comun/decisions/` plus
  human approval.
- No secrets committed.

Changes to these boundaries require a decision in `Area_comun/decisions/`.

## 5. Stack Decisions and Quality Gates

- Stack: Markdown + JSON artifacts; validator in PowerShell (to be complemented by a
  cross-platform Python validator).
- Quality gates: validator green on `examples/minimal_instance`; domain-neutrality scan clean.
- Human approval points: incompatible protocol changes; major version releases.

## 6. Task Lifecycle

```text
proposed -> ready -> claimed -> in_progress -> in_review -> done
                              -> blocked
                              -> cancelled
```

Task status must match in `Area_comun/tasks/TASK-XXXX-*.md` and `Area_comun/state/TASK_INDEX.json`.

## 7. Collaboration Protocol

- Small, verifiable, single-owner tasks.
- Shared work in `Area_comun/`; private drafts in `Claude/` and `Codex/`.
- Before editing, check `TASK_INDEX.json`, `CLAIMS.json` and `mailbox/open/`.
- Do not edit routes covered by another owner's active claim.
- Ambiguity becomes `blocked` plus one concrete question.
- Any protocol or boundary change requires a recorded decision.

## 8. Repository Map

```text
multi_agent_project_protocol/
|-- AGENTS.md                 (live instance contract)        AGENTS.template.md (shipped master)
|-- CLAUDE.md                 (Claude-specific rules)
|-- .claude/settings.json     (permissions allowlist)
|-- protocol.config.json      (live)                          protocol.config.template.json (master)
|-- README.md / README_INSTANCIACION.md
|-- Area_comun/               (protocol docs + live state + .template masters)
|-- examples/minimal_instance/(reference instance, validates green)
|-- scripts/validate_collaboration_state.ps1
|-- Claude/ , Codex/          (private agent areas)
```

## 9. Base Definition of Done

A task is not done until: its specific DoD is met; it does not violate the domain-neutrality
boundary; it introduces no secrets; it leaves a self-contained handoff if another agent must use
the output; it updates `TASK_INDEX.json`; and any ambiguity is recorded as `blocked` with a
concrete question.
