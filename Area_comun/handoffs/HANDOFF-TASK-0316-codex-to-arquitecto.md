# HANDOFF TASK-0316 - nested neutrality coverage remediation 1

task_id: TASK-0316
status: in_review
executive_summary: Implementation commit `52d0a38` restores identity scanning at every scripts depth, uses two explicit file allowlist entries for the 60 legitimate findings, removes the four real instance-specific defaults/literals, and closes the CI, falsification-inventory, and portable-scratch gaps without modifying pinned config.
artifacts:
  - path_or_commit: 52d0a380
  - path_or_commit: scripts/scan_domain_neutrality.py
  - path_or_commit: scripts/scan_domain_neutrality.ps1
  - path_or_commit: scripts/test_scan_domain_neutrality.py
  - path_or_commit: scripts/memory/query_memory_db.py
  - path_or_commit: scripts/memory/build_memory_db.py
  - path_or_commit: scripts/harness/peer_mailbox_cron.ps1
  - path_or_commit: scripts/harness/README.md
  - path_or_commit: .github/workflows/validate.yml
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS (57 tests)
  - command: python scripts/test_anthropic_checker_harness.py and PowerShell parser
    result: PASS
  - command: python scripts/test_scan_domain_neutrality.py
    result: PASS (3 tests, Python and PowerShell entrypoints plus depth-cutoff mutant)
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS (27 permanent negatives, 27 declarations, 0 missing)
  - command: python and PowerShell domain-neutrality scanners
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS (one pre-existing context_refs warning)
  - command: clean clone at 52d0a38 - requested gates and status
    result: PASS (status empty)
next_recommended: Arquitecto recomputes commit `52d0a38` and routes it to Analista for independent remediation review.
risks: The two file allowlist entries are intentionally whole-file because the scanner ships file-scoped legacy exceptions; the reviewer should confirm they cover only the classified fixture roster and third-party provider-name collision.

## Remediation mapping

- F1: both scanners again apply identity terms to nested `scripts/**/*.py` and
  `scripts/**/*.ps1`. The prior handoff phrase claiming that root-only behavior was preserved was
  incorrect; the original rule was recursive, and this remediation restores that surface.
- The 60 legitimate findings are explicit and greppable in
  `LEGACY_IDENTITY_LITERAL_FILES`: `scripts/memory/test_memory_db.py` for its synthetic roster and
  `scripts/harness/peer_mailbox_cron.ps1` for the third-party provider-name collision.
- The four real defects are removed. Retrieval no longer defaults to an instance agent id and
  requires `--requested-by` only with `--retrieve`; the two instance-local status strings are gone
  from the core enum; the exported cron requires an explicit `-CoordinatorId`, with matching docs.
- F2.1: the fixture uses the same configured identity at script depth 1 and depth 2. Both scanner
  entrypoints must report both paths. The permanent Python negative applies the former cutoff as a
  mutant and proves that only the nested identity finding disappears.
- F2.2/F2.3: CI now runs the regression, and
  `NEG-NEUTRALITY-NESTED-IDENTITY` is declared in the falsification inventory.
- F2.4: fixture storage uses `tempfile.TemporaryDirectory`; no drive-root or repository-relative
  scratch path is embedded.

## Reproducible clean-clone coverage at 52d0a38

- Configured raw globs: 124 files.
- Effective scanner globs: 136 files.
- Delta: +12, with all six `scripts/memory/` Python files and the required policy JSON coverage.
- Effective `runtime/memory/` files: 0.
- The counts differ from the review-time 147 -> 159 baseline because the canonical tracked tree
  changed between commits; the invariant delta remains +12. No `__pycache__` file entered this
  clean-clone measurement.

`protocol.config.json` remains byte-unchanged. Codex is the maker only and did not review or
ratify this remediation.
