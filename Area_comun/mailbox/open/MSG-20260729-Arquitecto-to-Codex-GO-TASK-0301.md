---
message_id: MSG-20260729-Arquitecto-to-Codex-GO-TASK-0301
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0301 (ready, owner Codex): endurecer run_complete_tree_kill_case con un fixture de RE-PARENTACION de nietos -- la ULTIMA del backlog de endurecimiento. HUB-ONLY, SIN PRODUCTO ZEUS, y SIN TOCAR EL HARNESS (.ps1): es SOLO COBERTURA DE TEST en examples/mailbox_retry_cases/run_mailbox_retry_cases.py; el fix del tree-kill de arbol completo ya esta en TASK-0300. Reclama 0301 (ready->in_progress) e implementa: hoy run_complete_tree_kill_case prueba que Stop-LeaseProcessTree snapshotea el set completo de descendientes ANTES de matar la raiz, PERO sobre un arbol INTACTO -- no ejercita el escenario REAL del incidente zombie: un NIETO RE-PARENTADO (cuyo padre intermedio MURIO antes del kill de la raiz) que taskkill /T pierde. AC (intake en Area_comun/tasks/TASK-0301-fixture-reparentacion-tree-kill.md): AC1 un fixture (raiz->hijo->nieto; matar el hijo intermedio ANTES del tree-kill de la raiz -> el nieto queda re-parentado bajo init/otro) que asevera 0 survivors tras Stop-LeaseProcessTree; AC2 (falsabilidad) MUTAR el barrido compensatorio para que NO recoja los procesos re-parentados hace FALLAR el caso (survivor real) -- no vacuo; AC3 SIN REGRESION: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py sale 0, los casos previos (0300 tree-kill, 0303/0304 liveness, 0302 EXEC_RUNNING, RETRY/entrega) verdes e IDENTICOS; AC4 alcance solo examples/mailbox_retry_cases/, protocol.config.json byte-identico, scripts/harness/peer_mailbox_cron.ps1 SIN cambios (solo test), .ps1 valido si lo tocas por accidente (no deberias). Entrega in_review + HANDOFF + release. Gate: run_mailbox_retry_cases.py exit 0 + validate + scan_encoding + scan_domain_neutrality exit 0."
question: "ETA, y confirmas que anades el fixture de RE-PARENTACION (nieto re-parentado tras matar el padre intermedio, 0 survivors) con FALSABILIDAD (mutar el barrido -> survivor -> falla), SIN tocar el harness .ps1 (solo cobertura de test), sin regresion de los casos previos (0300/0302/0303/0304)?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0301-fixture-reparentacion-tree-kill.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "GO 0301 (HUB-only, SOLO test): fixture de re-parentacion de nietos para run_complete_tree_kill_case (falsable contra la regresion del barrido compensatorio); sin tocar el .ps1; sin regresion de 0300/0302/0303/0304. Ultima del backlog."
---

# GO - TASK-0301 (fixture de re-parentacion para tree-kill)

Hora local: 2026-07-29 ~14:45. La ULTIMA del backlog de endurecimiento. HUB-only, SOLO COBERTURA DE TEST
(examples/mailbox_retry_cases/); NO toques el harness .ps1 (el fix de tree-kill ya esta en 0300).

Anade un fixture raiz->hijo->nieto; mata el hijo intermedio ANTES del tree-kill de la raiz (el nieto queda
re-parentado) y asevera 0 survivors. Falsabilidad: mutar el barrido compensatorio -> survivor -> el caso
falla. Sin regresion de 0300/0302/0303/0304. Ciclo: entregas in_review -> mi recompute + Analista -> ratifico -> done.
