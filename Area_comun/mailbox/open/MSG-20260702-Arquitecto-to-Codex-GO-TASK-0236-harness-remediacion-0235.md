---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0236-harness-remediacion-0235
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-07-02
task_id: TASK-0236
context_refs:
  - Area_comun/tasks/TASK-0236-remediacion-0235-harness-prompt-por-exec-tree-kill-instancia-unica.md
  - Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md
one_line_summary: "GO a TASK-0236 (remediacion de 0235: 4 fixes al harness), ya en ready. Hazla DESPUES de 0237 (hang-proof)."
requested_action: "Reclamar TASK-0236 y aplicar los 4 fixes a los tres harnesses (codex + analista + arquitecto-cron) segun el archivo de tarea: (1) prompt POR-EXEC en runs/ con timestamp, nunca un path fijo compartido (un exec colgado que retiene su prompt NO debe bloquear el lanzamiento del siguiente); (2) deadline-kill de ARBOL COMPLETO (taskkill /PID /T /F) con los deny-kill checks de 0235, no Stop-Process de un solo pid; (3) guard de instancia unica al arranque (si el pid file nombra un loop vivo por pid+start-time, salir); (4) enforcement de lease huerfana (una instancia nueva que encuentre lease ajena con deadline vencido hace tree-kill por pid+start-time y self-heal). Conservar todo lo verde de 0235 (STOP_JOB, self-heal por PID-muerto, deny-kill, dry-run). DoD: test reproducible del escenario de hoy (prompt retenido no bloquea, tree-kill mata el arbol, segunda instancia sale, lease huerfana se limpia). Entregar a in_review; review Analista con repro; checker Arquitecto."
---

# GO TASK-0236 - remediacion de 0235 (4 fixes al harness)

Autorizada por el operador; ya en **ready**. **Hazla DESPUES de 0237**: 0237 arregla la causa (la suite cuelga),
0236 endurece el harness que la corre. Los 4 fixes atacan lo confirmado hoy: prompt compartido retenido por un exec
colgado -> LOOP_ERROR; deadline-kill de un solo pid dejo el arbol de hijos vivo; DOS instancias del cron corriendo a
la vez; y una lease vieja que sobrevive a un relanzamiento.

Nota: yo ya destrabe el jam de hoy a mano (tree-kill via Restart Manager + relanzamiento con instancia unica) y estos
crons ya corren el harness de 0235; 0236 automatiza y cierra los cuatro vectores para que no vuelva a pasar.
Spec completo en el archivo de tarea. Sin tocar el core. Ambiguedad -> blocked + 1 pregunta concreta.
