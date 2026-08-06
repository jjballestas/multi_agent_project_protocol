# HANDOFF TASK-0316 - nested neutrality coverage

task_id: TASK-0316
status: in_review
executive_summary: Implementation commit `9e66c6a` closes the nested-script and policy-JSON blind spots without modifying pinned config. The scanners also exempt generated `runtime/memory/**` packs while preserving the pre-existing identity-scan surface, and permanent Python/PowerShell regressions cover both contracts.
artifacts:
  - path_or_commit: 9e66c6ae07da6080c163427aa111015903fda342
  - path_or_commit: scripts/scan_domain_neutrality.py
  - path_or_commit: scripts/scan_domain_neutrality.ps1
  - path_or_commit: scripts/test_scan_domain_neutrality.py
gates:
  - command: python scripts/test_scan_domain_neutrality.py
    result: PASS (2 tests, includes Python and PowerShell entrypoints)
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: git diff --check
    result: PASS
  - command: clean clone at 9e66c6a - test, neutrality, encoding, collaboration, status
    result: PASS (status empty)
next_recommended: Arquitecto recomputes the evidence and routes commit 9e66c6a to Analista for independent review.
risks: The task intentionally preserves root-only identity scanning for scripts; newly covered nested scripts are checked against the domain denylist, avoiding false identity findings from legitimate fixture names.

## Falsification and coverage evidence

- Before the fix, the planted scratch tree contained the configured denylist term in both
  `scripts/memory/blind_probe.py` and
  `Area_comun/protocol/MEMORY_INDEX_POLICY.json`; the scanner exited 0.
- The live pre-fix inventory selected 180 files, zero under `scripts/memory/`, and did not
  select the policy JSON.
- After the fix, the live inventory selects 192 files, all six files under
  `scripts/memory/`, and the policy JSON. It selects zero files under `runtime/memory/`.
- The permanent fixture plants the same domain term in a nested Python script and policy
  JSON, requires exit 1 with both paths in output, and proves a generated pack carrying
  the term is absent from findings. After neutralizing the two governed probes, the pack
  remains and the scanner exits 0.
- `protocol.config.json` is byte-unchanged by the implementation.

Codex is the maker only and did not review or ratify this work.
