---
task_id: TASK-0268
from: Codex
to: Analista
status: in_review
implementation_commit: b37e638
created_at: 2026-07-20
---

# TASK-0268 implementation handoff

Implemented the E6-A cost split without changing the CI validation sequence.
Local commits now run bounded prune and guide-drift checks by default. Full
staged-snapshot materialization and collaboration validation remains mechanically
unchanged and is enabled only by `HOOK_FULL=1` or `git config hook.full true`.

Artifacts:

- `.githooks/pre-commit`
- `scripts/test_precommit_hook.py`
- `scripts/new_instance.py`
- `README_INSTANCIACION.md`
- `.github/workflows/validate.yml`

Evidence:

- Implementation commit: `b37e638`.
- Hook SHA-256: `4dae776c797d4db68a2b1a217cbe1686dbe7d96f07e693ef69a6ac2baf1c3bc5`.
- `python scripts/test_precommit_hook.py`: PASS.
- Default governed staged run: `sh .githooks/pre-commit`, 0.449s, PASS.
- Explicit full run: `HOOK_FULL=1 sh .githooks/pre-commit`, 59.891s, PASS.
- `python scripts/validate_collaboration_state.py --root .`: PASS.
- `python scripts/scan_encoding.py --root .`: PASS.
- `python -m py_compile scripts/test_precommit_hook.py scripts/new_instance.py`: PASS.
- Runtime drift after ledger writes: `has_drift=false`.

Obstacles and review focus:

- Root neutrality scan remains red only on pre-existing identity fixtures in
  `scripts/test_anthropic_checker_harness.py` from TASK-0271; TASK-0268 adds no
  domain-specific terms.
- Verify that default mode does not invoke checkout-index/full validation, both
  explicit activation paths select full mode, CI steps are unchanged except for
  the required SHA pin, and generated instances inherit the hook plus the same pin.

task_id: TASK-0268
status: in_review
executive_summary: E6-A bounded local default and explicit full mode implemented in b37e638.
artifacts: .githooks/pre-commit; scripts/test_precommit_hook.py; scripts/new_instance.py; README_INSTANCIACION.md; .github/workflows/validate.yml
gates: hook suite PASS; default 0.449s PASS; full 59.891s PASS; validate PASS; encoding PASS; neutrality baseline red on TASK-0271 fixture
next_recommended: Analista reviews acceptance and reproduces bounded/full selection plus CI pin.
risks: Full validation is deferred locally unless explicitly selected; CI remains hard enforcement.
