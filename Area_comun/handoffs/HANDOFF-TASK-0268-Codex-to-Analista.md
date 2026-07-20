---
task_id: TASK-0268
from: Codex
to: Analista
status: in_review
implementation_commit: b37e638
remediation_commit: c06fbad
created_at: 2026-07-20
---

# TASK-0268 implementation handoff

## H1 documentation remediation

Commit `c06fbad` corrects the bounded/full description in
`README_INSTANCIACION.md`. The default pre-commit now is documented truthfully:
it runs cheap prune and guide-drift checks against the current tree without
materializing the staged snapshot. Explicit full mode and CI retain the
staged-byte materialization and judgment guarantee. No hook code or CI pin was
changed.

Remediation evidence:

- `python scripts/scan_encoding.py --root .`: PASS.
- `python scripts/scan_domain_neutrality.py --root .`: PASS.
- `python scripts/validate_collaboration_state.py --root .`: PASS.
- `protocol_state_drift(Path('.'))`: `has_drift=false` through seq 5139.
- Diff scope in implementation commit: `README_INSTANCIACION.md` plus governed
  transition files only.

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
executive_summary: E6-A bounded local default and explicit full mode implemented in b37e638; H1 documentation corrected in c06fbad without hook or CI-pin changes.
artifacts: .githooks/pre-commit; scripts/test_precommit_hook.py; scripts/new_instance.py; README_INSTANCIACION.md; .github/workflows/validate.yml
gates: hook suite PASS; default 0.449s PASS; full 59.891s PASS; remediation encoding PASS; neutrality PASS; validate PASS; drift false through seq 5139
next_recommended: Analista performs the requested docs-only re-judgment of H1 at c06fbad.
risks: Full validation is deferred locally unless explicitly selected; CI remains hard enforcement.
