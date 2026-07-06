---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-autoriza-aegis-firmantes-paso2-recuerda-html
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-ACTION-corte-aegis-cola-reqs-contabilidad.md
  - Area_comun/decisions/DECISION-0088-asiento-escalonado-instancia-aegis.md
  - personal/operador/vision-nova/pipeline-vision-nova.html
one_line_summary: "AUTORIZACIONES del Operador sobre la directiva Aegis (e749c0a): (1) verificar firmantes operativos en Aegis (seccion 1.2); (2) paso 2 (cola de los 4 REQs). Ademas: al REINICIAR sesion, actualizar el HTML del operador con el nuevo trabajo del track Aegis."
requested_action: "(1) Proceder con la verificacion de los 3 firmantes operativos en Aegis (llaves + capabilities maker/checker + e2e humo del ledger Aegis) -- AUTORIZADO. (2) Proceder con el paso 2 de la directiva Aegis: preparar/rutear las DECISIONes de los 4 REQs (orden anti-vibecoding -> intake -> memoria-hibrida que supersede DECISION-0071; aprendizajes-externos absorbidos) e implementarlos en ambito Aegis/Zeus-Aegis, nunca el core pineado -- AUTORIZADO. (3) AL REINICIAR SESION (cold-start): actualizar personal/operador/vision-nova/pipeline-vision-nova.html con el nuevo trabajo del track Aegis (corte hub->Aegis, 4 REQs, analisis Contabilidad, peones/Etapa 2, declaracion de trabajo paralelo) + sello de hora local; el panel del operador debe reflejar la realidad post-directiva."
question: "Confirmas pickup de las 2 autorizaciones y el orden? Recuerda actualizar el HTML del operador en tu primer turno tras el reinicio (no dejarlo stale)."
---

# ACTION - Autorizaciones Aegis (firmantes + paso 2) + recordatorio HTML

El Operador AUTORIZA dos pasos de la directiva Aegis (`MSG-...-corte-aegis-cola-reqs-contabilidad`, e749c0a):

## 1. AUTORIZADO: verificar firmantes operativos en Aegis (seccion 1.2)
Procede con la verificacion de los 3 firmantes en la instancia Aegis (`D:/Agentes/Zeus/NOVA/Aegis`): llaves
(event_auth/actor_auth), capabilities maker/checker cruzado equivalentes al hub, y el ciclo e2e de humo
(task_upsert -> claim -> flip -> release) verde en el ledger de Aegis ANTES de la primera tarea real.
Recordatorio del Asesor (refinamiento que el Operador ya te paso): cablea la CROSS-ATESTACION DUAL de
DECISION-0088 (el #4 del hub registra el sha256 de las atestaciones de Aegis por gate); no levantes un #4
independiente sin ese enlace.

## 2. AUTORIZADO: paso 2 (cola de los 4 REQs)
Procede a preparar y rutear las DECISIONes de los 4 REQs en el orden fijado (anti-vibecoding -> intake ->
memoria-hibrida, esta ultima SUPERSEDE DECISION-0071 explicitamente; aprendizajes-externos se absorben con
cita, no es entregable propio). Implementacion en ambito Aegis/Zeus-Aegis; PROHIBIDO tocar el core pineado
del hub (epoch 1.14.0). No son unidades medidas; si algo roza la linea roja Q4 o el aparato de Etapa 1, se
marca y se difiere.

## 3. RECORDATORIO: al reiniciar sesion, actualiza el HTML del operador
Vas a reiniciar sesion. En tu PRIMER turno tras el cold-start, actualiza
`personal/operador/vision-nova/pipeline-vision-nova.html` con el nuevo trabajo del track Aegis (corte
hub->Aegis, 4 REQs, analisis Contabilidad, peones/Etapa 2, declaracion de trabajo paralelo) + sello de hora
local (UTC+2). El panel del operador es su tablero; stale = reporte falso.

-- Operador
