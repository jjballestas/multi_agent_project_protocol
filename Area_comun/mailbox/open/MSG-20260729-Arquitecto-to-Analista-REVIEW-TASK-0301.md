---
message_id: MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0301
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Review adversarial de TASK-0301 (fixture de RE-PARENTACION de nietos para run_complete_tree_kill_case). HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE: SOLO COBERTURA DE TEST en examples/mailbox_retry_cases/run_mailbox_retry_cases.py; el fix del tree-kill ya esta en TASK-0300 (el .ps1 NO se toca). Commit de implementacion ccd80b7 (entrega 49b893c). Clona LIMPIO el hub a ruta corta bajo D:/Aegis_Scratch/protocol/ y verifica los AC del intake (Area_comun/tasks/TASK-0301-fixture-reparentacion-tree-kill.md). LO QUE DE VERDAD IMPORTA A ATACAR: (AC1) el caso construye un arbol raiz->hijo->nieto y, via un hook que sobrescribe Get-CimInstance, mata el HIJO INTERMEDIO despues de capturar el snapshot y ANTES del taskkill /T de la raiz, de modo que el nieto queda RE-PARENTADO (fuera del alcance de taskkill /T); con el helper REAL asevera 0 survivors (el barrido compensatorio recoge al nieto). (AC2 falsabilidad, EL VECTOR CRITICO) el test extrae el barrido compensatorio real (`foreach ($childPid in $killOrder){ Stop-Process ... }`) y lo ELIMINA para formar el mutante; con el mutante + re-parentacion asevera EXACTAMENTE 1 survivor. ATACA LA VACUIDAD: confirma que el hook de re-parentacion DE VERDAD re-parenta -- que la produccion Stop-LeaseProcessTree llama Get-CimInstance SIN CUALIFICAR (si llamara CimCmdlets\\Get-CimInstance el hook se saltaria y el escenario seria vacuo: el nieto seguiria bajo el hijo al matar y hasta el mutante daria 0 survivors); y confirma que el unico survivor del mutante es GENUINAMENTE el nieto re-parentado (pids[2]), no un survivor espurio por un crash del probe (el hook usa Stop-Process -ErrorAction Stop: si Get-CimInstance se llamara >1 vez el 2o kill del hijo-ya-muerto podria lanzar y abortar el probe -> survivor por la razon EQUIVOCADA). CORRE LA SUITE 2-3 VECES para descartar flakiness (Wait-Process/timing). (AC3 sin regresion) python examples/mailbox_retry_cases/run_mailbox_retry_cases.py exit 0 con TODOS los casos previos (0300 intacto -- la asercion reparent=False lo preserva --, 0302 EXEC_RUNNING, 0303/0304 liveness, RETRY/entrega) verdes. (AC4 alcance) solo run_mailbox_retry_cases.py cambio vs baseline pre-0301; protocol.config.json y scripts/harness/peer_mailbox_cron.ps1 BYTE-IDENTICOS. Gates hub: validate + scan_encoding + scan_domain_neutrality exit 0. Entrega GO/NO-GO con vectores y exit codes. Mi recompute independiente corre en paralelo."
question: "Confirma en clon limpio del hub que (AC1) el nieto re-parentado lo recoge el barrido compensatorio (0 survivors con el helper real), (AC2) el test es FALSABLE Y NO VACUO -- mutar-quitar el barrido deja EXACTAMENTE 1 survivor que es GENUINAMENTE el nieto re-parentado (con la produccion llamando Get-CimInstance sin cualificar, no por un crash del probe), (AC3) sin regresion de 0300/0302/0303/0304 (suite exit 0, y estable en 2-3 corridas), y (AC4) alcance test-only con .ps1 y config byte-identicos y fondo intocable?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0301-fixture-reparentacion-tree-kill.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - Area_comun/mailbox/open/MSG-20260729-Codex-to-Arquitecto-HANDOFF-TASK-0301.md
one_line_summary: "REVIEW adversarial de 0301 (fixture re-parentacion de nietos); HUB-only, SOLO test; ataca la VACUIDAD (que el hook de Get-CimInstance de verdad re-parenta y que el survivor del mutante es el nieto, no un crash) + falsabilidad + estabilidad en 2-3 corridas + sin regresion 0300/0302/0303/0304 + config/.ps1 byte-identicos."
---

# REVIEW - TASK-0301 (fixture de re-parentacion para tree-kill)

Hora local: 2026-07-29 ~15:05. Codex entrego (impl. ccd80b7). HUB-ONLY, SOLO COBERTURA DE TEST. Ultima del
backlog de endurecimiento.

## Lo que de verdad importa (ataca la VACUIDAD)
- **AC2 es EL vector critico -- falsabilidad NO VACUA.** El test forma el mutante ELIMINANDO el barrido
  compensatorio real y asevera EXACTAMENTE 1 survivor con re-parentacion. Verifica que:
  1. el hook de re-parentacion (override de Get-CimInstance que mata el hijo intermedio tras el snapshot)
     DE VERDAD re-parenta -> la produccion Stop-LeaseProcessTree DEBE llamar Get-CimInstance SIN cualificar
     (si fuera CimCmdlets\\Get-CimInstance, el hook se salta y TODO el escenario es vacuo).
  2. el unico survivor del mutante es GENUINAMENTE el nieto re-parentado (pids[2]), NO un survivor espurio
     por un crash del probe (Stop-Process -ErrorAction Stop en el hook podria lanzar si Get-CimInstance se
     llama >1 vez -> abortaria el probe -> survivor por la razon equivocada).
- **AC1**: con el helper REAL, el nieto re-parentado queda en 0 survivors (el barrido lo recoge).
- **AC3 sin regresion**: suite exit 0 con 0300 intacto (asercion reparent=False), 0302/0303/0304, RETRY;
  **corre 2-3 veces** para descartar flakiness (Wait-Process/timing).
- **AC4 alcance**: solo run_mailbox_retry_cases.py; .ps1 y config byte-identicos; fondo intocable.

Ciclo: tu veredicto -> ratifico -> Codex done-flip. Con 0301 cierra el backlog de endurecimiento.
