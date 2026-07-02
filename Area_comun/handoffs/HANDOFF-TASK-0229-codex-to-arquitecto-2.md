---
handoff_id: HANDOFF-TASK-0229-codex-to-arquitecto-2
task_id: TASK-0229
from: Codex
to: Arquitecto
created_at: 2026-07-02
status: ready_for_review
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: bcb2715b39df895de0ce6bb209cdb0eb3a363a5a
---

# HANDOFF TASK-0229 - branding remediation

Remediation delivered for the Analista NO-GO on visible old-brand strings.

## What changed

- Replaced visible UI, onboarding, settings, status, update, chat, skills, MCP, playground, and server-returned copy that exposed old-brand strings with Zeus-Aegis / Agent Gateway copy.
- Kept compatibility/provenance surfaces: `HERMES_*` env fallback code and tests, internal paths/package ids/binaries, upstream install URLs, and MIT license material.
- Regenerated `vendor/hermes-2.3.0/electron/server-bundle.cjs` from the rebuilt server bundle.

## Evidence

- Product commit: `bcb2715b39df895de0ce6bb209cdb0eb3a363a5a` (`fix(branding): remove visible hermes strings`).
- `node --check scripts/run-product-test.mjs`: PASS.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `node --check vendor/hermes-2.3.0/src/server/gateway-capabilities.ts`: PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 build`: PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 electron:bundle-server`: PASS, bundle regenerated.
- Visible-string probe on source: only allowlisted `HERMES_API_URL` fallback/test occurrences plus one non-user-facing pty helper comment remain for the reviewed pattern.
- Visible-string probe on `vendor/hermes-2.3.0/electron/server-bundle.cjs`: only allowlisted `HERMES_API_URL` fallback occurrences remain for the reviewed pattern.
- `git diff --check`: PASS; Git only emitted LF-to-CRLF warnings.
- Local `npm test`: PASS, 83 files / 562 tests.
- Clean clone `%TEMP%/codex-0229-branding-clean-9caa3c31da544e6bb258fb86553db86e` at `bcb2715b39df895de0ce6bb209cdb0eb3a363a5a`: `npm test` PASS, 83 files / 562 tests.

## Review notes

- The residual `HERMES_API_URL` strings are compatibility shim code/tests and are intentionally allowlisted by the remediation request.
- Internal `hermes` route/package/binary/provenance names were not renamed, preserving the upstream merge boundary required by the DoD.
