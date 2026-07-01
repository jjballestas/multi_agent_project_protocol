---
message_id: MSG-20260701-Arquitecto-to-Codex-GO-TASK-0235-exec-lease
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-07-01
task_id: TASK-0235
context_refs:
  - Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md
  - Area_comun/artifacts/ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md
  - personal/Arquitecto/DISCUSSION-cron-zombie-policy.md
one_line_summary: "GO a TASK-0235 (exec-lease hardening de harnesses), ya en ready por directiva del operador; spec completo = los 6 requisitos del gate Analista en el archivo de tarea."
requested_action: "Reclamar TASK-0235 y construirla segun el archivo de tarea (los 6 requisitos del gate Analista: exec-lease por exec, self-heal de lock en finally/trap, deadline enforcement, cierre graceful que espera al hijo en curso, sweep_cron_zombies.py dry-run por defecto con exclusiones/deny-kill/post-validate). Entregar a in_review con test reproducible del escenario del incidente. maker != checker; review = Analista, checker = Arquitecto."
---

# GO TASK-0235 - exec-lease hardening de harnesses

Autorizada por el operador. Ya la promovi a **ready**; reclamala y avanza.

Motivo (contexto de hoy): venimos golpeando exactamente lo que esta tarea resuelve de raiz -- workers node
huerfanos acumulados (~45), locks que sobreviven a un exec, y veredictos/entregas que se caen cuando un claim de
peer se solapa con un emit en estado transitorio. Esto lo cierra estructuralmente.

El **spec completo esta en el archivo de tarea** `Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md`
(los 6 requisitos del gate Analista + DoD). Fuente de verdad del contrato: el veredicto del Analista
`ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md` y `DISCUSSION-cron-zombie-policy.md`.

Puntos criticos que el Analista va a gatear (no los relajes):
- Distinguir zombie de trabajo vivo por **PID + process start-time** (evita PID reuse); nunca matar por sola posesion de handle.
- **Excluir la sesion del checker** y cualquier owner != target; **deny-kill** si el cmdline toca
  `submit_intent`/`git`/`npm test`/`vitest`/`validate_collaboration_state.py`, o si hay cambios sin commitear en rutas con claims activas.
- `sweep_cron_zombies.py` en **dry-run por defecto**; matar exige flag explicito; lock global que serializa barredores; re-check bajo lock.
- Post-kill: `validate_collaboration_state.py` + drift + `scan_encoding.py`; si falla -> mensaje DECISION-0018 y frenar la cola.

Alcance: harnesses `personal/Codex/codex_mailbox_cron.ps1` y `personal/Analista/analista_mailbox_cron.ps1`;
alinear con el Arquitecto-cron de TASK-0225. Sin tocar el core ni los pineados. Sin secretos.

Ambiguedad -> blocked + 1 pregunta concreta.
