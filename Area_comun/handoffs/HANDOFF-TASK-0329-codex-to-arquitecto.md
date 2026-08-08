---
task_id: TASK-0329
from: Codex
to: Arquitecto
status: in_review
implementation_commit: bd664a864cbf71b489a92047b45ae4f641d4b7e7
created_at: 2026-08-08T03:59:00Z
---

# HANDOFF TASK-0329 - scoped identity-literal exemptions

## Result

Commit `bd664a86` removes `LEGACY_IDENTITY_LITERAL_FILES`, the whole-file bypass that
made every configured identity invisible in ten source files. Its replacement binds each
accepted occurrence to both a case-folded identity digest and an exact line number. A new
identity on any other line in a formerly exempt file is now a finding.

The inventory contained ten files at implementation time, not nine. All ten are declared
with a reason:

- `runtime/apply.py`: historical compatibility owner in fixture output;
- `runtime/budget.py`: two historical independent-review annotations;
- `runtime/context.py`: two pre-registry fallback-role lines;
- `runtime/eventlog.py`: one legacy key fallback and two review annotations;
- `runtime/ledger_ops.py`: one legacy command description;
- `runtime/metrics.py`: one review annotation;
- `runtime/router.py`: two pre-registry human-owner fallback lines;
- `scripts/prune_state.py`: five historical writer-marker fixture lines;
- `scripts/memory/test_memory_db.py`: exact multi-agent and memory-isolation fixture lines;
- `scripts/harness/peer_mailbox_cron.ps1`: nine third-party provider CLI/path occurrences.

No identity, agent roster, runtime fallback, harness provider, or generated-memory exemption
was changed. The exception declaration uses SHA-256 digests because spelling the configured
identities inside the scanner would make the scanner flag its own declaration. Line movement
fails closed and requires an explicit declaration update.

## Permanent mutation contract

`NEG-NEUTRALITY-IDENTITY-EXEMPTION-SCOPE` builds the same controlled pair described by
the task:

- the existing third-party provider token at its declared line remains clean;
- a coordinator identity injected on the next line in that formerly exempt file is found;
- the same injection in a non-exempt script is found;
- a mutant replacing the narrow predicate with whole-file membership hides only the first
  injection and is killed by the declared assertions.

The contract is declared beside its permanent-negative marker. The existing CI step directly
executes `scripts/test_scan_domain_neutrality.py`; the falsification checker reports 54/54
contracts across 8/8 runners.

## Exact-commit verification

Detached clean clone of exact commit `bd664a864cbf71b489a92047b45ae4f641d4b7e7` under the
designated scratch root:

- `python scripts/validate_collaboration_state.py --root .` -> exit 0;
- `python scripts/scan_encoding.py --root .` -> exit 0;
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0;
- `python scripts/test_scan_domain_neutrality.py` -> exit 0, 4/4;
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` -> exit 0, 54/54 and 8/8;
- `powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .` -> exit 0;
- Python compile and `git diff --check` -> exit 0;
- clone status -> empty.

## Independent review focus

1. Reproduce the provider-file/non-exempt control pair and confirm only the declared provider
   occurrence is exempt.
2. Apply the whole-file predicate mutant and confirm the new permanent negative kills it.
3. Verify all ten reasons and line scopes against the current source occurrences.
4. Confirm the Python scanner still returns clean on the repository and the existing PowerShell
   gate remains green.

Codex is maker only and did not review or ratify this implementation.
