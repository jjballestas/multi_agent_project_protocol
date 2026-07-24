# RUNBOOK - Windows sandbox temp ACL

## When this applies

Use this runbook when an agent runs under the Windows unelevated sandbox and sees
`PermissionError` or `WinError 5` while reading or writing a temporary working path.

## Rule

No crear rutas de trabajo con ACL `0o700` en `%TEMP%`.

Runtime staging, rollback backups, harness fixtures, and any other working route that a sandboxed
agent must read or write must be repo-local, or another explicitly approved workspace path with
normal inherited ACLs. Clean the route after use.

## Why

On this setup, Python temp helpers such as `tempfile.TemporaryDirectory()` and `mkdtemp()` can create
paths whose effective ACL blocks the sandboxed token that created them. This is environment-specific,
but it can break authoritative write-path operations if staged files or backups inherit those ACLs.

## Operational Guidance

- Prefer `runtime.temp_paths.root_temp_dir()` or `make_root_temp_dir()` for runtime write-path staging
  and rollback backups.
- Keep temporary directories under the repository root unless a different inherited-ACL workspace path
  has been explicitly approved.
- Treat a `%TEMP%` `WinError 5` from a test harness as an environment failure first. Re-run outside the
  sandbox only to confirm, then harden the harness if it must pass inside the sandbox.
- Do not edit hot state JSON manually to recover from this class of error. Use `submit_intent` after
  repairing the temporary path behavior or rematerializing from the event log.
