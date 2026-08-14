# TASK-0367 remediation 2 - 2026-08-15

- Commit `ccea36e2` restores the documented no-`-AgentExe` startup contract: provider-specific
  environment overrides remain supported, while Codex/Auto falls back to `codex` and Anthropic
  falls back to `claude` from `PATH`.
- The focused behavioral entry point `--task0367-provider-only` clears both provider-command
  environment variables, resolves fixture commands in the designated Aegis scratch root, kills
  the participant-name mutant, and exits 0. It is not invoked by the full shared-sandbox suite.
- The full mailbox retry suite still exits 1 solely at the TASK-0343 main-assertion baseline
  (`baseline=0/3`); the TASK-0367 focused probe exits 0 independently.
- Runtime instantiation cases, encoding scan, domain-neutrality scan, and collaboration validator
  all exited 0. TASK-0367 is `in_progress` at runtime seq 9263 pending governed delivery.
- Codex remains maker only and has not reviewed or ratified the remediation.
