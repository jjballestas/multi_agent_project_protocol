---
task_id: TASK-0336
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-09
---

# TASK-0336 remediation 5 delivery - derived certification denominator

Implementation commit `2ed31e87f877517dc1f23a03fbb34df5caa99073` removes the only r5
blocker without changing the command grammar, shell model, static-certification predicate, or
workflow.

## Implemented property

The certification token no longer embeds the stale denominator `31`. It obtains the boundary tuple
for `NEG-FALSIFICATION-RUNNER-WIRING` from the contracts validated in that invocation and emits its
length. The canonical workflow-backed run therefore emits both:

`contract_discrimination_23_of_37`

and:

`DECLARED NEG-FALSIFICATION-RUNNER-WIRING boundaries=37`

The permanent assertion derives the same denominator from its own declared boundary tuple and
checks the canonical workflow-backed run. Adding or removing a declared wiring boundary now changes
both sides from the same contract data instead of leaving an aging literal.

## Scope held constant

- `split(chr(10))` and the derived separator-class property are unchanged.
- `effective_shell_kind` and its fail-closed handling are unchanged.
- `bounded_static_certification` and its affirmative-text mutant are unchanged.
- `.github/workflows/validate.yml` is unchanged.
- The measured numerator `23` and its finite historical method are unchanged; this remediation only
  makes its denominator name the delivered contract counted by the same run.

## Verification

Hot tree and detached clean clone
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0336r5-5e6043b6`, exact commit
`5e6043b6aba0ca2381c7ba06a67c4465df271be0`, both passed:

- falsification inventory: 12/12 runners, 68/68 contracts, 37 wiring boundaries;
- `scripts/test_falsification_contracts.py`;
- collaboration validator;
- encoding and domain-neutrality scans;
- Python compile and `git diff --check`;
- detached-clone Git status empty.

Codex is the maker only and did not review or ratify this remediation. Independent Analista review
must judge B3 coherence and confirm no regression of the already accepted A/B/C/E properties.
