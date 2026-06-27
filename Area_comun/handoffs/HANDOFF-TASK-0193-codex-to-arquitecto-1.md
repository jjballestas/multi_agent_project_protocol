---
handoff_id: HANDOFF-TASK-0193-codex-to-arquitecto-1
task_id: TASK-0193
from: Codex
to: Arquitecto
status: ready
created_at: 2026-06-27T13:30:00Z
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: f87317c
---

# TASK-0193 - F0 Gate Handoff

## Result

Zeus-Aegis F0 is delivered for review at product commit `f87317c feat(f0): import Hermes v2.3.0 baseline`.
Commit author is Arquitecto, with `Co-Authored-By: Codex <codex@openai.com>`.

## Delivered

- Imported Hermes Workspace v2.3.0 into `D:/Agentes/Zeus/Zeus-Aegis/vendor/hermes-2.3.0`.
- Preserved MIT attribution at root `LICENSE`, `NOTICE.md`, and `vendor/hermes-2.3.0/LICENSE`.
- Created branch `vendor/hermes-2.3.0` pointing to the F0 import commit.
- Added `docs/SEAMS.md` with stack, routes, env seams, smoke evidence, rebrand boundary, and prune plan.
- Added `docs/REUSE-INVENTORY.md` with portable governance inventory from `D:/Agentes/Zeus/Zeus-protocol`.
- Kept F1+ out of scope: no `/api/governance/*`, no submit_intent UI path, no live ledger writer path.

## Pin

- Upstream: `outsourc-e/hermes-workspace`
- Version: `v2.3.0`
- Tag object: `0218dbafce50fa69ba9ce045e2c8a3f5383bd1db`
- Commit checked out by tag clone: `15fa9cd706f5c04e4db288fb958e21d10fc776da`

## Evidence

- `node --check vendor/hermes-2.3.0/server-entry.js` PASS.
- `corepack pnpm approve-builds --all` PASS.
- `corepack pnpm install --frozen-lockfile` PASS after the first install failed closed on ignored build scripts.
- Vite started on `http://127.0.0.1:3000` using the Windows-safe direct command
  `node node_modules/vite/bin/vite.js dev --host 127.0.0.1`.
- Bounded local stub gateway on `127.0.0.1:8642` returned `/health` HTTP 200.
- Bounded local stub dashboard on `127.0.0.1:9119` returned `/api/status` HTTP 200.
- App probe logged zero-fork mode with gateway/dashboard capabilities:
  `core=[health, chatCompletions, models, streaming, dashboard]` and
  `enhanced=[sessions, skills, memory, config, jobs]`.

## Caveats For Review

- The real `hermes` CLI is not installed in PATH on this Windows host.
- `uvx --from git+https://github.com/NousResearch/hermes-agent.git hermes --version` failed while building
  `hermes-agent` because the package build could not delete a locked `build\lib\gateway\platforms\webhook.py`.
- `/api/sessions` reached the app against the bounded stub but returned `{"error":"Dashboard index failed: 404"}`;
  full real dashboard parity remains pending a working `hermes dashboard` on the host.
- `corepack pnpm exec tsc --noEmit` is red in the vanilla upstream snapshot. The errors are documented in
  `docs/SEAMS.md` and cluster around upstream 3D/playground, swarm, and route-test surfaces.
- `git diff --cached --check` was red only on upstream vendor whitespace/newline issues; Codex did not normalize
  the vendor snapshot to keep F0 source fidelity.

## Reviewer Focus

- Confirm license/attribution is acceptable for the imported snapshot.
- Confirm F0 caveats are acceptable for Gate 0, or request a follow-up to get a real Hermes Agent/dashboard
  running on this Windows host before approving.
- Confirm that F1 remains read-only only; F2 write-through remains post-TFM gated by DECISION-0064.
