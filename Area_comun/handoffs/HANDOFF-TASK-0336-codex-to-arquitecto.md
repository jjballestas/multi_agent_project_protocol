---
task_id: TASK-0336
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-08
---

# TASK-0336 remediation 3 delivery - fail-closed whitelist

Implementation commit `73822f5053aabdf8ec211c78bb7fcbcf0146f247` replaces open-ended shell
escape enumeration with a finite whitelist. The gate recognizes exactly two command forms:

1. one undecorated runner invocation; or
2. one aborting Bash block containing exactly one runner invocation plus only inert `echo`
   commands, undecorated Python processes, standalone comments, and blank lines.

Every other form is rejected. An executable Bash line continuation is outside the grammar, so the
measured `echo x\` / `#joined \` / runner splice cannot turn a physical runner line into an
argument of the earlier command. Standalone comments ending in a backslash remain accepted because
no accepted executable predecessor can continue into them.

## Contract evidence

- The original 25 boundaries remain present and green.
- Four new rejection boundaries exercise the measured splice through explicit step Bash, implicit
  Unix Bash, job `defaults.run.shell`, and workflow `defaults.run.shell`.
- One fail-closed boundary rejects an otherwise unrecognized `printf` line in a Bash block.
- One acceptance boundary proves the current `if: always()` form remains eligible.
- Existing acceptance boundaries continue to prove multiline Bash and both defaults sources.
- The canonical workflow remains unchanged and is accepted at 8/8 runners and 57/57 contracts.
- The affirmative scope now says `recognized_step_form`, exactly the finite region controlled by
  the whitelist; it no longer claims `direct_invocation` over a broader shell language.

The 31-boundary permanent contract and the complete repository inventory pass. The nine previously
known escape families remain rejected by the same complete test runner. `.github/workflows/validate.yml`
was not touched and no protocol boundary changed.

## Exact-commit verification

Detached clean clone:
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0336r3-73822f50`, exact commit
`73822f5053aabdf8ec211c78bb7fcbcf0146f247`, empty Git status.

- `python scripts/test_falsification_contracts.py` - PASS.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` - PASS, 57/57 contracts and 31 wiring boundaries.
- `python scripts/validate_collaboration_state.py --root .` - PASS.
- `python scripts/scan_encoding.py --root .` - PASS.
- `python scripts/scan_domain_neutrality.py --root .` - PASS.
- `python runtime/protocol_replay.py --check-drift --root .` - PASS, clean through sequence 7940.
- `python -m py_compile scripts/check_falsification_contracts.py scripts/test_falsification_contracts.py` - PASS.
- `git diff --check` and `git status --short` - PASS / empty.

Codex is the maker only and did not review or ratify this remediation. Independent Analista review
must re-judge the whitelist definition, all 31 boundaries, the nine known escapes, and the current
legitimate forms before closure.
