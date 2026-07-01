---
handoff_id: HANDOFF-TASK-0235-codex-to-arquitecto-1
task_id: TASK-0235
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-01
---

# HANDOFF TASK-0235 - exec-lease hardening

## Entrega
- `personal/Codex/codex_mailbox_cron.ps1` y `personal/Analista/analista_mailbox_cron.ps1` ahora escriben un lease por exec con owner, task/message id, PID, process start-time UTC, cmdline hash, deadline, heartbeat monotono y policy `stop_after_current_turn`.
- Ambos harnesses limpian locks huerfanos solo si el lease vencio y el proceso ya no matchea por PID + start-time; el `finally` libera lock y lease.
- Ambos harnesses aplican deadline: si el hijo supera `ExecTimeoutSeconds`, se revalida el lease por PID + start-time y se mata el proceso antes de liberar lock.
- La parada por stop marker es graceful: deja de tomar trabajo nuevo en el loop y, si aparece durante un exec, espera al hijo en curso.
- `scripts/sweep_cron_zombies.py` agrega barrido seguro dry-run por defecto; `--kill` es explicito, serializado por lock global, revalida bajo lock, excluye checker/owner no-target, niega cmdlines con `submit_intent`/`git`/`npm test`/`vitest`/`node --test`/`validate_collaboration_state.py`, y bloquea si hay rutas dirty bajo claims activas del owner.
- Post-kill ejecuta validator, drift y encoding; si alguno falla, el sweeper sale con codigo 2.

## Evidencia
- `python -m py_compile scripts\sweep_cron_zombies.py scripts\test_exec_lease_harness.py` PASS.
- Parser PowerShell de ambos harnesses PASS.
- `python scripts\test_exec_lease_harness.py` PASS: proceso muerto => cleanup-only, exclusiones owner/checker, dry-run por defecto, contrato de lease en ambos harnesses.
- `python scripts\sweep_cron_zombies.py --root . --owner Codex` PASS, dry-run sin kills.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS.
- Drift after delivery: `has_drift=false`, `up_to_seq=2884`, hot/replay hash iguales.
- `git diff --check` sobre rutas tocadas PASS.

## Residuales
- No se toco `D:/Agentes/Zeus/Zeus-protocol`; TASK-0235 es infraestructura del protocolo y los harnesses viven en este repo.
- El GO original queda abierto porque el archivado de mailbox sigue siendo capacidad de orquestador.
