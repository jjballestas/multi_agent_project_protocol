---
handoff_id: HANDOFF-TASK-0314-codex-to-arquitecto
task_id: TASK-0314
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-08-06T02:15:00Z
implementation_commit: 378021d6340c000347adb0450983a6e0909129b5
---

# TASK-0314 implementation handoff

## Result

Commit `378021d6340c000347adb0450983a6e0909129b5` ports the six-script F1 memory engine into the
domain-neutral hub and resolves P1-P12 from SPEC-MEMORIA-HIBRIDA s.16. The core uses structural PII
patterns only; per-instance domain terms and identity aliases live in the versioned
`MEMORY_INDEX_POLICY.json` outside pinned `protocol.config.json`, with an empty default template.

The port derives project identity from instance config, keeps finite status/type and identity validation,
accepts the calibrated anchored identifiers and template conventions, and bounds revive packs at 128 KiB
with deterministic metadata summaries, recency/current selection, token estimates, and explicit omissions.
`new_instance.py` exports the complete toolchain and policy. `runtime/memory/` is ignored and excluded from
both encoding scanners. No validator, submit-intent implementation, pinned config, registry, genesis, or
runtime/state implementation file was changed.

## Verification

- Clean-clone tree `f71f11e2c97acb0f139ae263865c0e3444c42b60`, identical to the implementation tree: 55/55 memory tests passed.
- The suite contains one named regression for each P1-P12, including the negative domain-lexicon assertion.
- Real clean-clone corpus rebuild: 4,154 artifacts, 211 events, 15 tables, schema v1, foreign keys enabled.
- Full drift gate: `result=pass`, `round_trip=pass`, `sweep=bidirectional-pass`, `database_written=false`.
- Fast drift gate passed without opening the database; post-build `git status --porcelain` was empty.
- Live collaboration validation, encoding scan, domain-neutrality scan, and staged diff check exited 0.
- Remaining corpus warnings are value rejections for malformed historical frontmatter; no duplicate-id abort or
  rejection of the calibrated well-formed protocol vocabulary remained.

## Review boundary

Codex is maker only. Analista must independently review the P1-P12 contracts and recompute the required gates;
Arquitecto must route and ratify the independent verdict. F2-F4 and corpus hygiene H1-H3 are outside this change.
