---
artifact_id: Analista-TASK-0277-remediacion-iter1-verdict
task_id: TASK-0277
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-20
verdict: CHANGE-REQUIRED
blockers: 2
majors: 1
residuals: 3
---

# Verdict TASK-0277 remediation iteration 1 -- governed prune apply (adversarial review)

I am the Analista, independent checker of this instance. I did not implement any of this
and I did not touch the canonical tree while reviewing: every probe ran in a disposable
clone (D:/ccv0277) and in throwaway fixtures under the system temp dir. Review requested by
MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0277-remediacion-iter1. No product in
scope; the scope is this hub. Local time of this verdict: 2026-07-20 19:43 (system clock).

I did not need the exclusive window: nothing I ran writes canonical state.

## Canonical anchor

- Fix commit under review: 7337b30 (fix(TASK-0277): unblock governed prune apply).
- Delivery commit: 6e3bcc5 (coord(TASK-0277): deliver prune apply remediation).
- Protocol HEAD at review time: 5e581c4 == origin/main.
- Clean clone at D:/ccv0277 (short path), gates run there by exit code, never in the
  shared hot tree.

## Gates reproduced (clean clone, by exit code)

| Gate | At 7337b30 | At HEAD 5e581c4 |
|---|---|---|
| python scripts/validate_collaboration_state.py | exit 0 | exit 0 |
| python scripts/scan_encoding.py | not re-run | exit 0 |
| python scripts/scan_domain_neutrality.py | not re-run | exit 0 |
| python examples/prune_state_cases/run_prune_state_cases.py | exit 0, 5 cases | exit 0, 5 cases |
| python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py | not re-run | exit 0, 8 cases |
| protocol_state_drift() | not measured | has_drift=False, up_to_seq 5434 |

The canonical tree at review start also validated exit 0 (only the known archiving
warning). No half-written peer delivery in the tree, no active claims (CLAIMS.json
active set is empty), so my commit window is safe.

## Reproduction rig

Because a `--check` proves nothing here, I exercised the real `--apply` path four ways:

1. Real enforced `--apply` in the clean clone at 7337b30 against canonical state.
2. Real enforced `--apply` on the maker's own fixture (regenesis, enforce+authoritative),
   as the happy path.
3. Fault injection at four distinct points of `apply_prune_via_submit_intent`, by
   monkeypatching `scripts.prune_state.submit_intents` in-process:
   `pre` (raise before any event), `notapplied` (return applied=False),
   `post` (call the real submit, let it apply, then raise), `kbint` (raise
   KeyboardInterrupt, i.e. an operator Ctrl-C or any BaseException).
4. Residue probes on the real repo shape: unbacked archive row, and hot row duplicated
   into the archive.

Exit codes were read directly, never through a pipe.

## Vector-by-vector

| # | Vector asked | Result |
|---|---|---|
| A1 | `--apply` works again under enforce | PASS |
| A2 | Failure BEFORE the event write restores both mirrors | PASS |
| A3 | Failure AFTER the event write leaves the tree recoverable | **SLIPS -- F-0277R1-01 (blocker)** |
| A4 | No path leaves rows without a backing event | **SLIPS -- F-0277R1-02 (blocker)** |
| A5 | The repaired path cannot re-block itself | **SLIPS -- F-0277R1-03 (major)** |
| B | F1 relaxation declared in the validator code, with motive | PASS |
| B2 | The relaxation loses no live collision guard | PASS |
| C | No regression on reconstruction fidelity / bidirectional invariant | PASS |

### A1 -- the apply works (PASS)

On the maker's fixture, real enforced apply: exit 0, `has_drift` False, `--check`
afterwards exit 0, mirrors go from empty to the 4 task rows and 7 claim rows that the
signed prune event names. The pre-write ordering is the right attack on the problem
(it fixes the order instead of relaxing the gate). At 7337b30 against canonical state
the apply refused with `claim acquire overlaps active claim
CLAIM-20260720-Codex-TASK-0277-remediation-1` -- correct behaviour for that snapshot,
not a defect, and the mirrors came back byte-identical (`git status` clean).

### A2 -- pre-event failure (PASS)

`pre` and `notapplied` injections: mirrors byte-identical to the pre-run bytes, hot
state unchanged, events unchanged. All-or-nothing holds on this side.

### A3 -- F-0277R1-01: the rollback destroys a transaction that DID apply (BLOCKER)

The compensating restore is triggered by **any** exception out of `submit_intents`,
including one raised after the governed transaction was already applied and signed.
That is exactly the class of failure you hit ("post-write event verification failed").

Falsifiable trace (fixture, `post` injection):

```
[POST2] drift right after successful submit (before rollback): False
[POST2] mirrors after rollback: {'TASK_INDEX_ARCHIVE.json': [], 'CLAIMS_ARCHIVE.json': []}
[POST2] drift after rollback: True
[POST2] validate_exit: 1
[POST2] drift after manual mirror repair: False
[POST2] rerun --apply exit: 0   drift after rerun: True
```

Read it in order: the ledger was consistent (drift False) the instant the transaction
applied; the rollback then deleted the mirror rows that the signed prune event requires,
and drift went True. Putting the exact bytes back returns drift to False, which proves
the rollback is the cause and nothing else.

Two consequences, both bad:

- The residue is the mirror image of the one you saw: instead of rows without an event,
  you get **an event without its rows** -- signed attestation that entries were archived,
  over mirrors that no longer contain them.
- It does not heal by itself. Re-running `python scripts/prune_state.py --apply`
  **exits 0** while drift stays True (`"transaction": null`, nothing left to prune).
  The maintenance path reports green over a drifted tree; only `validate` (exit 1) and
  an explicit drift call dissent.

This is a defect introduced by this iteration, on the exact path that is failing in
production right now (TASK-0280 open). It is why I cannot sign the closure.

### A4 -- F-0277R1-02: `except Exception` does not cover Ctrl-C or a kill (BLOCKER)

`except Exception` misses `BaseException`: `KeyboardInterrupt` (operator Ctrl-C),
`SystemExit`, and any hard kill of the process. Injection `kbint`:

```
[KBINT] exc=KeyboardInterrupt mirrors_restored=False hot_unchanged=True events_unchanged=True drift=False
   orphan rows: TASK-9000..TASK-9003 / CLAIM-0000..CLAIM-0006
```

So the answer to your question is: **yes, rows can stay without an event that backs
them**, precisely when the run is interrupted between the pre-write and the submit.

How visible is that residue, on the real repo shape (probes in the clean clone at HEAD,
restored afterwards with `git checkout --`):

- Row pre-written while its twin is still hot: `validate` exit 1, message
  `Duplicate task across hot/archive: <id>` / `Duplicate claim across hot/archive: <id>`.
  Detected, and a later successful prune absorbs it (re-run: exit 0, drift False, no
  duplicated rows). Recoverable without manual surgery in this shape.
- Archive row with no backing event and no hot twin (`CLAIM-FABRICATED-NO-EVENT`
  appended to CLAIMS_ARCHIVE.json): **validate exit 0 and drift False**. Completely
  invisible. Extra mirror rows really are ignored, as the new code comment claims --
  which is what makes pre-staging drift-safe, and equally what makes an orphan of this
  shape silent.

The window is small but it is the same window an operator is most likely to interrupt
(the apply is the long, scary step run under peer pressure).

### A5 -- F-0277R1-03: a stale pre-written row re-blocks the prune permanently (MAJOR)

`archive_removed_entries` dedupes by id only (`if entry_id not in existing_ids`), so it
never refreshes a row already in the mirror, while `verify_archived_entries` compares the
row content in full. Chain it: interrupted prune leaves the pre-written copy of row X,
then X is legitimately mutated by a governed transaction, then any future prune sees a
stale mirror row it will not refresh and cannot verify:

```
[STALE] interrupt: KeyboardInterrupt          (orphan rows written)
[STALE] governed mutation applied: True  drift= False
[STALE] later prune exit= 1  ->  RuntimeError: prune archive verification failed for TASK_INDEX_ARCHIVE.json: TASK-9000
[STALE] retry  exit= 1  (same error)
```

That is the same class of blockage TASK-0277 exists to remove, reachable again through
the new pre-write path, and it needs manual editing of the mirror to clear.

### B -- the F1 declaration (PASS)

The comment is where the code is read: `scripts/validate_collaboration_state.py:1142-1144`,
immediately above the `if claim.get("status") == "active":` guard, and it states the
motive (live collision guard vs. archive rows faithful to their signed legacy scope).
I did not take the comment on trust; I drove `validate_claims` directly:

| status | scope | result |
|---|---|---|
| active | `CLAIMS.json#claim-lowercase-bad` | FAIL (invalid row selector) |
| released / blocked | same | PASS (relaxed) |
| active | `Area_comun/mailbox/open` | FAIL (mailbox claim must be file-scoped) |
| released / blocked | same | PASS (relaxed) |
| active | `UNSUPPORTED.json#row/1` | FAIL (unsupported path) |
| active | `CLAIMS.json#CLAIM-20260720-Codex-ok` | PASS |

B2: the relaxation exempts `released` **and** `blocked`. I checked both consumers of
"live": the validator's overlap check filters `status == "active"`
(validate_collaboration_state.py:1151) and the runtime's `active_claims`
(runtime/context.py:189-191) does the same. A blocked claim guards nothing, so no live
guard is lost. Declared as residual R3 only because the exemption is wider than the
comment's wording suggests.

### C -- regression on my previous verdict (PASS)

Independent recount at HEAD, from the raw event log, not from any handoff: 207
event-named task ids and 1426 event-named claim ids, **zero** missing from the mirrors
(archive totals 303 tasks / 1665 claims); hot-vs-archive intersection empty in both
directions. Drift False at up_to_seq 5434, replay golden cases 8/8, validate/encoding/
neutrality all exit 0. Reconstruction fidelity and the bidirectional invariant I closed
in the previous round are intact.

## Residuals declared

- **R1 -- the rollback path has no test.** The new regression
  (`case_enforced_apply_prestages_archive_rows`) covers only the happy path. The claim
  this iteration is built on ("restore both mirrors if the transaction fails") is
  untested, which is how F-0277R1-01 survived to delivery.
- **R2 -- the enforced fixture does not exercise signing.** It sets
  `event_auth: {enabled: false}` and no `agent_signatures_enabled`, so the regression
  proves the drift gate but not the signed path an operator actually runs.
- **R3 -- the F1 exemption covers `blocked` too**, which is safe today only because
  nothing treats a blocked claim as live. If a future status transition reactivates a
  blocked row, its unvalidated legacy scope becomes an active claim.
- **R4 (cross-cutting, not this unit) -- git author metadata contradicts the signed
  actor.** 7337b30 and 6e3bcc5 are git-authored `Analista <analista@local>` while their
  events (seq 5411-5412 Codex, 5413-5415 Arquitecto) are signed by the actors who really
  did the work; 5b76643 is the inverse. The ledger attribution is correct and remains the
  authoritative one, but anyone reading `git log`/`git blame` will misattribute maker work
  to the checker. Raised under DECISION-0018 for whoever owns the runtime git identity.

## Answer to the question you asked

> If the prune transaction dies AFTER pre-writing the mirrors, is the tree recoverable
> without manual intervention, or can rows remain with no event to back them?

Both failure modes exist, and neither is fully self-recovering:

1. Interrupted by Ctrl-C / SystemExit / kill: **rows remain with no backing event**
   (F-0277R1-02). If their hot twin is still there, `validate` catches it and the next
   successful prune absorbs it; if the row is mutated in the meantime, the prune is
   permanently blocked (F-0277R1-03); and an orphan with no hot twin is invisible to both
   validate and drift.
2. Died after the transaction applied -- your actual case: **the opposite residue**, an
   applied signed event whose rows the rollback deleted, drift True, and `--apply`
   re-runs exit 0 without repairing it (F-0277R1-01). Manual reconstruction required.

## Closure recommendation

**CHANGE-REQUIRED (NO-GO).** The unit does restore the maintenance path and the F1
declaration is properly done, but this iteration introduces a destructive rollback on the
exact failure path that is live today, and it does not close the unbacked-row window it
was written to close.

### Expected fix loop (iteration 2 of a maximum of 2)

1. Make the restore conditional on "no event was written": snapshot the event-log head
   (seq/hash) before `submit_intents` and restore the mirrors only if the head is
   unchanged. If the transaction did apply, keep the mirrors and fail loudly with the
   manual-recovery instruction.
2. Catch `BaseException` (or use `try/finally` with an explicit success flag) so Ctrl-C
   and SystemExit take the same path; consider a marker file so a killed run is
   detectable afterwards.
3. Refresh, do not skip, a mirror row whose content differs from the hot row, so a stale
   pre-written row cannot block the prune forever.
4. Do not exit 0 when `has_drift` is True at the end of `--apply`.
5. Regressions for all four: post-apply failure must not delete mirror rows; interrupted
   prune must be recoverable; stale row must not block; drifted tree must not exit 0.

Affected gates for the re-judgement: `examples/prune_state_cases`, `protocol_state_drift`,
`scripts/validate_collaboration_state.py`. Re-judgement by me BEFORE the closing commit.
If iteration 2 does not close F-0277R1-01 and F-0277R1-02, escalate to the human owner.

-- Analista, independent checker
