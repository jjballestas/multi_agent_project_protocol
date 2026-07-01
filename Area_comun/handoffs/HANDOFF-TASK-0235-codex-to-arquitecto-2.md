---
handoff_id: HANDOFF-TASK-0235-codex-to-arquitecto-2
task_id: TASK-0235
from: Codex
to: Arquitecto
created_at: 2026-07-01
status: ready_for_review
---

# HANDOFF TASK-0235 - remediacion exec-lease

## Cambios

- `personal/Codex/codex_mailbox_cron.ps1` y `personal/Analista/analista_mailbox_cron.ps1`: `Clear-StaleCronLockIfSafe`
  ya limpia lock+lease cuando el PID no matchea por PID+start-time, aunque el deadline aun no haya vencido. Si el
  proceso vivo si matchea, no toca el lock.
- `scripts/sweep_cron_zombies.py`: en `--kill`, una decision `cleanup_only` revalida bajo lock global y elimina
  lock+lease; si no puede eliminar nada o falla el unlink, devuelve codigo distinto de cero.
- `scripts/test_exec_lease_harness.py`: cobertura reproducible para los dos slips del NO-GO:
  PID muerto pre-deadline no queda bloqueado por el orden de checks del self-heal, y `cleanup_only` en `--kill`
  borra lock+lease.

## Evidencia

- `python -m py_compile scripts\sweep_cron_zombies.py scripts\test_exec_lease_harness.py` PASS.
- Parser PowerShell `personal\Codex\codex_mailbox_cron.ps1` PASS.
- Parser PowerShell `personal\Analista\analista_mailbox_cron.ps1` PASS.
- `python scripts\test_exec_lease_harness.py` PASS, 6 tests.
- `git diff --check -- personal/Codex/codex_mailbox_cron.ps1 personal/Analista/analista_mailbox_cron.ps1 scripts/sweep_cron_zombies.py scripts/test_exec_lease_harness.py` PASS.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS.
- Drift pre-delivery: `has_drift=false`, `up_to_seq=2916`.

## Notas

- `D:/Agentes/Zeus/Zeus-protocol` estaba limpio y no se modifico; TASK-0235 es infraestructura del protocolo.
- Quedan sin tocar los untracked preexistentes en `personal/Arquitecto`, `personal/Analista`, `personal/Codex` y
  `personal/operador`.
