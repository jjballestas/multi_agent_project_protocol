---
skill_id: delegate-to-worker
title: Delegate to worker
neutral_core: true
version: 0.1.0
---

# Delegate to Worker

This governed skill is a read-only convention for a signing lead that delegates shaped implementation work to a keyless worker. Loading this document grants no authority, opens no live channel, writes no state, and persists no output.

## When To Delegate

Delegate only work that already has a clear mold. Good candidates are repeated create/read/update/delete surfaces, data transfer objects, mappers, plumbing tests, mechanical migrations, fixtures, and narrow refactors that copy a pattern the signing lead has already made concrete.

Do not delegate boundary design, policy changes, ambiguous requirements, security-sensitive judgment, release approval, or any action whose correctness depends on authority the worker does not hold.

## Author The Subtask

The signing lead authors a small subtask with:

- The existing pattern or exemplar path the worker must follow.
- Clear acceptance criteria and explicit non-goals.
- `owner=<worker-id>` for the worker that will produce the draft.
- A staging destination in the worker personal area or another non-ledger draft location.
- The gates the lead will run before signing anything.

The worker prepares the deliverable in staging. The worker does not write the ledger, does not close the task, and does not sign any status transition.

## Boundary Invariant

The worker is keyless. Under enforced runtime state, a keyless worker attempting to write the ledger fails closed by the guard introduced with TASK-0213. The hard boundary is:

- Worker: prepares draft output only.
- Lead: verifies the output against the mold and acceptance criteria.
- Lead: signs the ledger transition through `runtime/submit_intent.py`.
- Lead: records provenance metadata that identifies the real worker and model used, so the read-only metrics added in TASK-0214 can attribute the work.

Authority remains with the signing lead's verified signature. This skill is only procedure.

## Lead Verification Checklist

Before signing a close or status transition, the lead verifies:

- The output follows the referenced mold.
- All acceptance criteria are met.
- The worker stayed inside the authorized scope.
- There are no secrets and no unreviewed personal data.
- Required tests, static checks, and project gates are green.
- Provenance names the real worker id and model.

If any item is uncertain, the lead does not sign. The task is corrected, narrowed, or blocked with one concrete question.

## Anti-Patterns

- Letting a keyless worker sign, close, or mutate the ledger.
- Treating a worker draft as verified because it exists.
- Signing without checking the mold and acceptance criteria.
- Recording false or missing provenance.
- Delegating policy, release, security, or unclear boundary decisions.
- Using this skill as a live capability grant.
