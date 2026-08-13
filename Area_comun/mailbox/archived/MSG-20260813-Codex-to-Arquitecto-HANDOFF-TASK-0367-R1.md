---
id: MSG-20260813-Codex-to-Arquitecto-HANDOFF-TASK-0367-R1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0367
status: archived
created: 2026-08-13T12:08:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0367 remediation restores provider-configured tool resolution and proves both asymmetric peers by behavior.
requested_action: Route independent review of implementation commit 832aea72 and the governed delivery commit that contains this handoff.
question: Does independent review confirm provider-configured tool resolution and the asymmetric two-peer behavioral evidence?
context_refs:
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
---

# TASK-0367 remediation handoff

Implementation commit: `832aea72`.

Criterion: participant identity attributes protocol actions and selects registered actors; a tool
name selects an executable contract installed on the host. `PeerId` is the former. `AgentProvider`
selects the latter through `PROTOCOL_ANTHROPIC_AGENT_COMMAND` or
`PROTOCOL_REFERENCE_AGENT_COMMAND` when `-AgentExe` is absent.

Behavioral evidence executed `Get-AgentExecutable` for both asymmetric pairs and printed:

    Codex=<fixture>/codex.exe
    Analista=<fixture>/claude.ps1

The test also replaces provider selection with `$PeerId.ToLowerInvariant()` and requires that mutant
to lose the Analista resolution. The other four TASK-0367 changes remain untouched because they
concern actor attribution or generic absent-config language, not host executable selection.

Green exit-code evidence:

- direct two-peer executable-resolution probe;
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py`;
- Python compile of the mailbox retry runner;
- collaboration validator;
- encoding scan;
- domain-neutrality scan.

Known independent red: the full mailbox retry suite aborts in the pre-existing TASK-0343
main-assertion behavioral baseline (baseline 0/3 on two runs); all three injected TASK-0343 mutants
were caught 3/3. The new two-peer resolution probe passed before that unrelated abort on both runs.
Codex is maker only and has not reviewed or ratified this remediation.
