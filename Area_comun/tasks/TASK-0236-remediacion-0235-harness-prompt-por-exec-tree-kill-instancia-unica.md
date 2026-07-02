---
task_id: TASK-0236
title: "[INFRA] Remediacion de TASK-0235: prompt por-exec + deadline-kill de arbol + guard de instancia unica + enforcement de lease huerfana"
type: build
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, TASK-0235]
linked_decisions: [DECISION-0057, DECISION-0018, DECISION-0022]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0236-remediacion-0235-harness-prompt-por-exec-tree-kill-instancia-unica.md
---

# TASK-0236 - [INFRA] Remediacion de TASK-0235 (harness): cuatro fixes contra los jams recurrentes

- **Owner build:** Codex - **Review:** Analista - **Checker:** Arquitecto. maker != checker.
- **Alcance:** los tres harnesses de cron: `personal/Codex/codex_mailbox_cron.ps1`,
  `personal/Analista/analista_mailbox_cron.ps1` y el Arquitecto-cron (TASK-0225).
- **Origen (evidencia confirmada 2026-07-02):** TASK-0235 (exec-lease) cerro la causa raiz parcialmente, pero
  se reprodujo un jam: un exec de review/build se colgo (npm test colgado en un clon Temp) reteniendo el
  `prompt.v3.txt` COMPARTIDO -> el loop no pudo lanzar un exec nuevo (LOOP_ERROR); ademas corrieron DOS instancias
  del cron a la vez (log con `count=16` y `count=31`), y el deadline-kill mataba un solo pid dejando el arbol de
  hijos (esbuild/node/cmd) vivo. Estos cuatro fixes cierran esos vectores.

## Alcance (los 4 fixes)
1. **Prompt POR-EXEC en `runs/` con timestamp** (igual que stdout/err), NUNCA un path fijo compartido. Cada exec
   escribe su propio `runs/<ts>-<msg>.prompt.txt`; asi un exec colgado que retiene su prompt NO bloquea el lanzamiento
   del siguiente. Elimina el `LOOP_ERROR` por contencion del prompt compartido.
2. **Deadline-kill de ARBOL COMPLETO** (`taskkill /PID <pid> /T /F`), NO `Stop-Process` de un solo pid. Debe matar el
   proceso Y toda su descendencia (esbuild/node/cmd/powershell hijos), aplicando los mismos deny-kill checks de 0235
   (no matar submit_intent/git/npm test/vitest/validator; excluir checker/owner no-target; re-check bajo lock).
3. **Guard de instancia unica al arranque:** si el `.pid` file nombra un loop VIVO (pid + start-time), la instancia
   nueva SALE limpio (no arranca una segunda). Evita las DOS instancias concurrentes observadas hoy.
4. **Enforcement de lease huerfana:** una instancia nueva que encuentre una lease AJENA con deadline VENCIDO hace
   tree-kill por pid+start-time (fix #2) y self-heal (limpia lock+lease), luego continua. Cierra el caso "exec viejo
   colgado que sobrevive a un relanzamiento".

## DoD
- Los 4 fixes implementados en los tres harnesses; test reproducible del **escenario de hoy**: (a) exec colgado
  reteniendo su prompt NO bloquea al siguiente (prompt por-exec); (b) deadline-kill elimina el arbol entero, no un pid;
  (c) una segunda instancia sale por el guard; (d) una instancia nueva limpia una lease huerfana vencida por tree-kill.
- Conservar todo lo verde de 0235 (STOP_JOB unico token de corte, self-heal por PID-muerto, deny-kill, dry-run del sweeper).
- Gate Analista: **GO** reproduciendo el escenario de hoy (npm test colgado + prompt retenido + doble instancia). maker != checker.
- Sin tocar el core del protocolo ni los pineados. Sin secretos.

## Handoff
Autocontenida. maker (Codex) != checker (Arquitecto), review Analista con repro. Ambiguedad -> blocked + 1 pregunta concreta.
