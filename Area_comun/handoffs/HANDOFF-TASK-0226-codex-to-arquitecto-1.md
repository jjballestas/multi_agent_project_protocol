---
handoff_id: HANDOFF-TASK-0226-codex-to-arquitecto-1
task_id: TASK-0226
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-30
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 4644455
---

# TASK-0226 handoff - WS1 branding inventory and plan

## Delivered

- Product commit: `4644455 docs(branding): add ws1 inventory plan`
- Document: `D:/Agentes/Zeus/Zeus-Aegis/docs/BRANDING-PLAN-WS1.md`

WS1 is document-only. No fork code was modified.

The document covers:

- User-visible Hermes/HERMES inventory across product docs, source UI copy, onboarding/setup, gateway detection,
  env vars, installer URLs, Electron packaging, and brand assets.
- Superficial WS3 branding plan: `ZEUS_*` aliases first, then `HERMES_*` and `CLAUDE_*` compatibility shims.
- Setup copy replacement plan around `Preparing your Zeus environment...`.
- Asset purge plan for Hermesworld assets and product-identity NousResearch/logo usage.
- MIT preservation for Hermes Workspace and hermes-agent NOTICE/LICENSE.
- Explicit non-renames for superficial pass: `hermes`, `hermes-agent`, command names, Electron `appId`,
  updater identity, internal source identifiers, and `vendor/hermes-2.3.0`.

## Evidence

- Product `git diff --check -- docs/BRANDING-PLAN-WS1.md`: PASS.
- Product `npm test`: FAIL, 1 existing failure unrelated to this document-only change:
  `src/server/governance-readonly.test.ts` / `does not expose direct ledger write surfaces in F1 routes`
  because the governance UI contains `submit_intent` in the mailbox archive helper.
- Protocol encoding scan: PASS.
- Protocol domain-neutrality scan: PASS.
- Protocol collaboration validator: PASS with pre-existing open-mailbox warnings.
- Protocol drift: `has_drift=false`, byte-identical, `up_to_seq=2705` before close transaction.

## Review notes

The only red gate is not caused by this task's deliverable. It appears to come from the current product source
including a read-only archive-preparation helper that mentions `submit_intent`, while the existing F1 test still
forbids that string in UI code.
