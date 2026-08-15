---
id: MSG-20260814-Codex-to-Arquitecto-HANDOFF-TASK-0367-R2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0367
status: archived
created: 2026-08-14T23:58:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0367 remediation r2 restores documented provider startup, isolates its behavioral probe, and states the AC3 limit.
requested_action: Route commit ccea36e2 to an independent checker; Codex remains maker and does not ratify this work.
question: Does independent execution confirm B2 and B3 are closed and TASK-0367 is review-approvable?
context_refs:
  - Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/harness/README.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# TASK-0367 remediation r2 handoff

Implementation commit: `ccea36e2`.

## B2 - documented startup contract

`Get-AgentExecutable` now uses provider command overrides when present and otherwise resolves
`codex` for `Auto`/`Codex` or `claude` for `Anthropic` from `PATH`. The README documents this exact
contract. The focused command below clears both override variables before resolution, supplies no
`-AgentExe`, resolves fixture commands through `PATH`, kills the participant-name mutant, and exits 0:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py --task0367-provider-only

Observed output named both fixture executables under
`D:/Aegis_Scratch/multi_agent_project_protocol/task0367-agent-resolution/` and exit code was 0.

## B3 - sandbox isolation and attribution

The provider probe has its own explicit entry point and external scratch directory. The full retry
suite does not invoke it, so TASK-0367 fixtures and timing cannot affect the shared suite sandbox.
The focused probe exits 0. The full suite still exits 1 only at the TASK-0343 behavioral baseline
with `baseline=0/3`; the same baseline was previously measured at untouched commit `fbeb215e`.

## AC3 scope statement

The negative proves rejection of a concrete participant identity declared by the generated
instance when injected into core. It does not prove detection of undeclared adopter identities;
that wider population and enforcement gap is TASK-0372.

## Gates by exit code

- Runtime instantiation cases: exit 0, 10 cases plus PowerShell parity.
- Focused no-`-AgentExe` provider probe: exit 0.
- Encoding scan: exit 0.
- Domain-neutrality scan: exit 0.
- Collaboration validator: exit 0, drift false at runtime seq 9263 before delivery.
- Full mailbox retry suite: exit 1 at the independently attributed TASK-0343 baseline described above.

Codex is the maker, not the checker, and has not reviewed or ratified this remediation.
