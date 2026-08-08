---
task_id: TASK-0336
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-08
---

# TASK-0336 remediation 4 delivery - shell command boundary

Implementation commit `90477ff7ac8dc7f838e4debb7c53e5ff7a2bfb83` keeps the fail-closed
whitelist and binds it to the effective shell's command model.

## Implemented property

- The effective shell family is resolved before either whitelist member is accepted. Literal
  hosted Windows defaults resolve to PowerShell, literal hosted Unix defaults resolve to Bash, and
  explicit `bash`, `pwsh`, `powershell`, or `cmd` declarations resolve to their named family.
  Unknown shells, dynamic runner labels, and nonliteral runner coordinates fail closed.
- A bare undecorated runner remains a permitted single command only under one of those resolved
  shell families.
- A Bash block is parsed on LF, the Bash command boundary. Python-only separators remain inside one
  command and therefore cannot turn `echo <separator> runner` into two whitelist members.
- Only space and tab are removed as layout whitespace. Command-significant controls are not erased
  by Python's broader `strip()` semantics.
- The inversion to a finite whitelist is unchanged. `.github/workflows/validate.yml` is byte-
  identical to the parent commit.

## Permanent falsification evidence

The contract derives the complete current Unicode scalar class for which Python `splitlines()`
creates two lines while Bash does not see LF. It does not name the six observed YAML-accepted
characters. For every derived scalar it tests both coordinates:

1. inert `echo`, separator, runner; and
2. runner, separator, inert `echo`.

Each coordinate is driven through all four effective-Bash sources: step shell, implicit Unix
runner, job defaults, and workflow defaults. The aggregate mismatch list is empty. The same
contract proves bare runners accepted under explicit Bash and PowerShell, while an unknown shell
and a matrix runner label are rejected.

AC5 is load-bearing by mutation of the real certification text. A temporary checker changes the
live output to `FALSIFICATION_EXECUTION guaranteed=yes` and `scope=full_execution_guarantee`; it
still computes a green 59/59 inventory, but the bounded-static certification assertion rejects its
claim. The current output remains:

`FALSIFICATION_STATIC_WIRING runners=8/8 contracts=59/59`

with scope limited to trigger keys, conditions, recognized step form, and job failure.

## Declared debt and false rejections

- Safe single commands with runner arguments, including `--root .`, remain outside the whitelist.
- Multiline PowerShell, self-hosted list labels, matrix runner labels, and nonliteral shell forms
  remain outside the whitelist even where a concrete deployment could propagate failure.
- The reviewer's finite mutation matrix found that only 23 of the prior 31 boundaries
  discriminated. The current contract has 37 declared wiring boundaries; that historical 23/31 is
  debt evidence, not a claim about the six new boundaries.
- The Bash continuation guard and the whitelist overlap: removing either mechanism alone left the
  prior 31 boundaries green in the reviewer's measurements. The property is covered, but neither
  internal mechanism is independently pinned.
- TASK-0338 is the same root class at another consumer boundary: Python `splitlines()` versus the
  neutral scanner's PowerShell reader. TASK-0336 does not absorb or close TASK-0338. A shared
  command/record-boundary abstraction is an architectural follow-up for Arquitecto to partition.

## Exact-commit verification

Detached clean clone:
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0336r4-90477ff7`, exact commit
`90477ff7ac8dc7f838e4debb7c53e5ff7a2bfb83`, empty Git status after all checks.

- `python scripts/test_falsification_contracts.py` - PASS, 37 wiring boundaries.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` - PASS, 8/8 runners and 59/59 contracts.
- `python scripts/validate_collaboration_state.py --root .` - PASS.
- `python scripts/scan_encoding.py --root .` - PASS.
- `python scripts/scan_domain_neutrality.py --root .` - PASS.
- `python runtime/protocol_replay.py --check-drift --root .` - PASS, clean through sequence 8050.
- `python -m py_compile scripts/check_falsification_contracts.py scripts/test_falsification_contracts.py` - PASS.
- `git diff --check` and `git status --short` - PASS / empty.

Codex is the maker only and did not review or ratify this remediation. Independent Analista review
must re-run the nine original escapes, the separator-class property, the certification-text
mutation, and the legitimate current forms before any closure.
