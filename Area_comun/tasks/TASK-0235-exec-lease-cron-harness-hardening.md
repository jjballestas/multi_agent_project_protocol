---
task_id: TASK-0235
title: "[INFRA] Contrato exec-lease en harnesses de crons: self-heal de locks huerfanos + kill por deadline + barrido seguro (spec del gate Analista)"
type: build
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-07-01
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001]
linked_decisions: [DECISION-0057, DECISION-0018, DECISION-0022]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md
---

# TASK-0235 - [INFRA] Contrato exec-lease en los harnesses de crons

- **Owner build:** Codex - **Review:** Analista - **Checker:** Arquitecto
- **Origen:** el cron de Codex quedo JAMMED ~14h por un exec que COMPLETO pero no libero lock/prompt (zombie).
  El barrido quirurgico ad-hoc (Restart Manager) desatasco el incidente, pero el Analista dio **NO-GO a
  automatizarlo** porque Restart Manager prueba POSESION de handle, no que el proceso sea zombie -> puede matar
  trabajo vivo (incluido el del checker). **Spec = veredicto Analista** `Area_comun/artifacts/ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md`
  y `personal/Arquitecto/DISCUSSION-cron-zombie-policy.md`.
- **Alcance:** harnesses de cron de peers `personal/Codex/codex_mailbox_cron.ps1` y
  `personal/Analista/analista_mailbox_cron.ps1`; alinear con el Arquitecto-cron TASK-0225.

## Alcance (los 6 requisitos del gate Analista)
1. **exec lease por exec:** cada exec escribe un lease separado con PID + process start-time + cmdline hash +
   owner + task/msg id + started_at + **deadline** + **heartbeat monotono** + shutdown policy.
2. **Self-heal:** el cron libera el `.lock` en un `finally`/`trap` aunque el exec termine mal; si el lease esta
   VENCIDO y el PID que nombra esta muerto (PID + start-time, no solo PID -> evita PID reuse) -> auto-limpiar y seguir.
3. **Deadline enforcement:** un exec que excede su deadline se mata y el lock se libera; ningun exec puede colgarse indefinido.
4. **Parada graceful = "stop after current turn":** el cron deja de tomar trabajo nuevo, espera al hijo en curso,
   libera el lock en finally y reporta salida. NO mata al hijo en curso.
5. **Barrido seguro (`sweep_cron_zombies.py`, dry-run por DEFECTO):** solo mata holders que matcheen un lease
   VENCIDO por PID + start-time; **excluye la sesion del checker y cualquier owner != target**; lock global de
   mantenimiento (serializa barredores); **deny-kill** si el cmdline contiene `submit_intent`/`git`/`npm test`/
   `vitest`/`node --test`/`validate_collaboration_state.py`, o si hay cambios sin commitear en rutas con claims
   activas del owner; re-check bajo lock antes de matar.
6. **Post-kill:** correr `validate_collaboration_state.py` + drift + `scan_encoding.py`; si falla -> mensaje
   DECISION-0018 y frenar la cola (no continuar).

## DoD
- Harnesses con exec-lease + self-heal + deadline + parada graceful implementados; el escenario del incidente
  (exec completado-pero-colgado reteniendo lock/prompt) **ya no atasca** (test reproducible: simular el exec y ver
  que el cron se auto-recupera).
- `sweep_cron_zombies.py` con dry-run por defecto, todas las exclusiones/deny-kill/post-kill del gate; matar exige flag explicito.
- Gate Analista: **GO** (reproduce sus 6 requisitos: falso positivo, PID reuse, auto-dano al checker, carreras, ledger). maker!=checker.
- Sin tocar el core del protocolo ni los pineados. Sin secretos.

## Handoff
Autocontenida. maker!=checker. Ambiguedad -> blocked + 1 pregunta concreta.
