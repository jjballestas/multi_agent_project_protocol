---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0236-harness-remediacion-0235
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/tasks/TASK-0236-remediacion-0235-harness-prompt-por-exec-tree-kill-instancia-unica.md
  - Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md
task_id: TASK-0236
one_line_summary: "GO a TASK-0236 (remediacion de 0235: fixes al harness), ya en ready. Hazla DESPUES de 0237 (hang-proof). Incluye un 5o fix nuevo: el detector de corte debe ser match EXACTO, no contains."
requested_action: "Reclamar TASK-0236 y aplicar los fixes a los tres harnesses (codex + analista + arquitecto-cron) segun el archivo de tarea: (1) prompt POR-EXEC en runs/ con timestamp, nunca un path fijo compartido (un exec colgado que retiene su prompt NO debe bloquear el lanzamiento del siguiente); (2) deadline-kill de ARBOL COMPLETO (taskkill /PID /T /F) con los deny-kill checks de 0235, no Stop-Process de un solo pid; (3) guard de instancia unica al arranque (si el pid file nombra un loop vivo por pid+start-time, salir); (4) enforcement de lease huerfana (una instancia nueva que encuentre lease ajena con deadline vencido hace tree-kill por pid+start-time y self-heal); (5) NUEVO: el detector de la orden de corte (Test-ArquitectoStopOrder) debe exigir que el valor de requested_action del mensaje sea EXACTAMENTE la orden (comparacion de igualdad de la linea completa), NO un match 'contains' -- hoy un mensaje que solo MENCIONA la orden en una frase dispara el stop y tumba el cron (este mismo GO lo hizo). Conservar el resto de lo verde de 0235 (self-heal por PID-muerto, deny-kill, dry-run, y la orden de corte unica). DoD: test reproducible del escenario de hoy (prompt retenido no bloquea, tree-kill mata el arbol, segunda instancia sale, lease huerfana se limpia) + test de que un mensaje que MENCIONA la orden de corte en prosa NO detiene el cron. Entregar a in_review; review Analista con repro; checker Arquitecto."
---

# GO TASK-0236 - remediacion de 0235 (fixes al harness) + 5o fix: detector de corte por igualdad exacta

Autorizada por el operador; ya en **ready**. **Hazla DESPUES de 0237**: 0237 arregla la causa (la suite cuelga),
0236 endurece el harness que la corre.

Los fixes 1-4 atacan lo confirmado hoy: prompt compartido retenido por un exec colgado -> LOOP_ERROR; deadline-kill
de un solo pid dejo el arbol de hijos vivo; DOS instancias del cron corriendo a la vez; y una lease vieja que
sobrevive a un relanzamiento.

**Fix 5 (nuevo, aprendido a las 01:44 de hoy):** el detector de la orden de corte usa `-cmatch` de un token en el
`requested_action`, o sea un match "contains". Eso reintroduce el footgun: este GO, que solo MENCIONA la orden para
pedir conservarla, disparo el "stop order detected" y **tumbo el cron de Codex**. El detector debe exigir que el
`requested_action` sea EXACTAMENTE la orden (igualdad de la linea completa tras trim), no que la contenga. Asi la
orden sigue siendo unica e inequivoca, pero describirla en prosa ya no detiene el agente.

Spec completo en el archivo de tarea. Sin tocar el core. Ambiguedad -> blocked + 1 pregunta concreta.
