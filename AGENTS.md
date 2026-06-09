# AGENTS.md — Shared source of truth for multi_agent_project_protocol

> This file is the project contract. All agents (Claude, Codex) and the human owner read and
> obey it. If a one-off instruction conflicts with this file, this file wins unless the human
> owner explicitly overrides it and records a decision in `Area_comun/decisions/`.
>
> **Dogfooding note:** this repository applies its **own protocol** to its own development. The
> shipped masters for new projects are the `*.template.*` files; this `AGENTS.md` and the
> canonical `Area_comun/state/*.json` are **this project's live instance**.
>
> Last updated: 2026-06-08 · Maintainer: Claude (architect) + human owner. Released version: v1.0.0.

## 0. How to Start

An agent entering cold can operate by reading only:

1. `AGENTS.md`.
2. `Area_comun/` in this order:
   - `Area_comun/README.md`
   - `Area_comun/protocol/TASK_PROTOCOL.md`
   - `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.json`
   - `Area_comun/state/*_ARCHIVE.json` only when historical entries are needed.
   - `Area_comun/mailbox/open/`
   - the concrete file in `Area_comun/tasks/`.

Never assume another agent knows your context. Every task and handoff must be self-contained.
The hot state files are intentionally pruned for cold-start efficiency; validators read hot state
plus archives to preserve full traceability.

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
- Shared work in `Area_comun/`; private drafts in each participant's personal area `personal/<id>/`.
- **Onboarding rule (DECISION-0016):** every participant (agent or human) that registers in the project
  creates its personal area at `personal/<id>/`, where `<id>` is its identifier in `agent_registry`/
  `agents`. Private drafts/notes live there.
- Before editing, check `TASK_INDEX.json`, `CLAIMS.json` and `mailbox/open/`.
- Before creating or editing any file in a shared route, create/update an active claim that lists
  that route in `scope`; this includes new drafts and temporary files that remain in the workspace.
- Do not edit routes covered by another owner's active claim.
- A task owner that moves a task to `in_review` or `done` must release its active claim in the same
  coordination step. A reviewed task must not retain an active claim from its owner.
- **Golden memory rule (DECISION-0026):** immediately after every commit, each agent must update its own
  persistent memory in `personal/<id>/` (or equivalent personal runbook) with the commit's relevant context,
  so the next cold start reflects the just-committed reality. A commit is not complete until that memory
  update is done.
- An agent holding an active claim over `in_progress` work must leave a verifiable progress signal
  each work turn: deliverable progress, a compact FYI, or `blocked` with one concrete question.
- Ambiguity becomes `blocked` plus one concrete question.
- **Anomaly notification (DECISION-0018):** an agent that detects an anomaly or inconsistency in another
  participant's work or in shared state (e.g. an incomplete handoff-release, a status that contradicts the
  claims/mailbox, a stale or orphaned claim, a missing or mismatched artifact) must notify the responsible
  owner via `mailbox/open/` with a concrete, actionable message, and record it. It must not silently fix
  routes under another owner's active claim, nor leave the anomaly unsignaled; if the fix needs those
  routes, it asks the owner (or the human) and waits.
- **Anti-collision rule for concurrent ledger writes (DECISION-0020):** when more than one agent may write
  the shared ledger (`Area_comun/state/*.json`, mailbox) in overlapping windows, every writer: (1) prepares
  drafts in its personal area `personal/<id>/` while the peer is busy; (2) writes the ledger only in a safe
  window (peer has no active claim on the routes and the working tree shows no half-written peer delivery;
  otherwise it waits and retries); (3) makes ledger closes/enqueues in a single atomic script; (4) never
  lists a not-yet-created artifact in a claim `scope` (artifacts-before-claim, #1); (5) stages explicit
  paths when committing, never broad directories, and commits only a consistent snapshot with green gates
  (#2); (6) writes any mailbox/artifact assertion only after the ledger backs it -- the "DONE" FYI after the
  status flip, the "X ready" GO after X is recorded (#3); (7) promotes one task at a time with a GO + ETA.
- **Runtime-authoritative mode (DECISION-0022):** only runtime-tier instances with
  `event_state.enabled/materialize/enforce/authoritative:true` treat the runtime as the writer of
  `Area_comun/state/*.json`. In that mode, state transitions go through `runtime/submit_intent.py`
  (`task_status`, `task_upsert`, `claim`, `decision`) with caller-provided `timestamp`/`commit`, and
  manual state edits are rejected as drift by the B.3 hard-gate. **Mechanism vs marker (DECISION-0028,
  posture B):** `enforce` (its B.3 hard-gate) **is** the single-writer mechanism — it provides the
  "only the runtime writes the ledger" guarantee; `authoritative` is the declarative marker that
  formalizes runtime-authoritative mode and has no behavior callers of its own. No authoritative-specific
  teeth are wired (no invariant exists that `enforce` does not already cover), and the TASK-0086 guard
  (`authoritative⇒enforce⇒materialize⇒enabled`) already rejects authoritative-without-enforce, so the
  false-secure cannot occur. Multi-step ledger changes (e.g. a close
  that flips `task_status`, releases a `claim` and upserts the next task) go as one atomic
  `submit_intent --intents` transaction (all-or-nothing with full rollback; each intent validated against
  the state produced by the prior ones); `runtime/regenesis.py` writes a fresh content-addressed genesis to
  bring drift to 0 before the first transaction. This repository ships the capability off by default;
  activating it in the live instance requires separate operator approval. **Turning
  `enforce`+`authoritative` on requires BOTH agent loops to already route every ledger transition through
  `submit_intent`** -- otherwise the first manual edit after the flip hard-fails and breaks the peer loop;
  the switch is therefore a coordinated re-genesis + flip with a rehearsed rollback, never a unilateral
  toggle. Coordination-tier instances keep the manual ledger flow.
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
|-- personal/<id>/            (per-participant private areas; e.g. personal/Claude, personal/Codex)
```

## 9. Base Definition of Done

A task is not done until: its specific DoD is met; it does not violate the domain-neutrality
boundary; it introduces no secrets; it leaves a self-contained handoff if another agent must use
the output; it updates `TASK_INDEX.json`; and any ambiguity is recorded as `blocked` with a
concrete question.
