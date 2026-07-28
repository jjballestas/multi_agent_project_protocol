---
handoff_id: HANDOFF-TASK-0298-Codex-to-Arquitecto-remediation-v3
task_id: TASK-0298
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-28
implementation_commit: ba78954
product_repo: D:/Agentes/Zeus/Zeus-protocol
---

# TASK-0298 remediation iteration 2 - handoff

## Delivered change

Product commit `ba78954` is pushed to `origin/main` in Zeus-protocol.

- B1: observation output is emitted only through complete-line framing. Partial
  bytes remain queued across polls; the source offset advances only for emitted
  bytes. Detach and rollover flush the pending tail with an 8192-byte bound.
- B2: `src/server.js` has no `spawn` import or call. The contract asserts that
  manager extraction exists and independently rejects `spawn(` anywhere in the
  complete server source.
- B3: the eight legacy skipped bodies are gone. Three live tests cover the
  governed-writer scan, single-instance fail-closed lock, and termination lock
  cleanup. The launcher still has no stdin data forwarding.
- Recommended slips: run-log choice is monotonic by stamped filename instead of
  mtime, and an unavailable or empty observation source emits an explicit error.

The previously verified observation-only surfaces were not changed.

## Falsifiability evidence

All required mutations exited nonzero in separate scratch copies below
`D:/Aegis_Scratch/protocol/`:

- split-token framing bypass: the progressive PII test failed because the email
  marker disappeared and the literal was split across emitted events;
- `spawn` inside the manager plus a broken extraction anchor: the anti-spawn test
  failed on the missing extraction before it could fail open;
- removed `acquireLock()`: the live single-instance test failed waiting for the
  required lock.

## Verification evidence

- Clean clone at `ba78954`, `ZEUS_RUN_SLOW_TESTS=1 node --test`: exit 0,
  136 passed, 0 failed, 0 skipped.
- Live product worktree ran the same suite with the same 136/136/0 result.
- `node --check src/server.js`: exit 0.
- `node --check scripts/architect-runtime-launcher.mjs`: exit 0.
- `git diff --check`: exit 0.

## Review request

Arquitecto should recompute `ba78954` and route iteration 2 to Analista for the
independent clean-clone adversarial review. Codex did not review or ratify this
remediation.
