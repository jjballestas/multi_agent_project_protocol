# TASK-0367 remediation 1 - 2026-08-13

- Implementation commit `832aea72` restores tool resolution by provider configuration instead of
  participant identity. `PROTOCOL_ANTHROPIC_AGENT_COMMAND` and
  `PROTOCOL_REFERENCE_AGENT_COMMAND` supply resolvable host commands when `-AgentExe` is absent.
- Permanent behavioral coverage executes `Get-AgentExecutable` for Codex/Codex and
  Analista/Anthropic, prints both resolved fixture binaries, and kills the PeerId-derived mutant.
- Direct resolution probe, runtime instantiation cases, collaboration, encoding, domain-neutrality,
  and Python compile gates exited 0. The expected placeholder-negative diagnostic is emitted inside
  the passing instantiation runner.
- The full mailbox retry suite remains red in the pre-existing TASK-0343 main-assertion baseline:
  baseline 0/3 on two runs while all three injected mutants were caught 3/3. The new resolution probe
  passed before that unrelated failure on both runs.
- TASK-0367 remains in_progress under
  `CLAIM-20260813-Codex-TASK-0367-remediation1-scope-repair` pending governed delivery.
