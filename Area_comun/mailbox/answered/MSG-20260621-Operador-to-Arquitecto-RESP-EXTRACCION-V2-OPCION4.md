---
message_id: MSG-20260621-Operador-to-Arquitecto-RESP-EXTRACCION-V2-OPCION4
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: answered
requires_response: false
response_owner: Arquitecto
requested_action: "Specear la v2 (carga por archivo) con el mecanismo de extraccion OPCION 4 (detallado abajo), NO con tu opcion 2 (server llama al LLM = egress del server, descartada). Resumen: el SERVER no extrae; al subir, (a) guarda el archivo en una RUTA especifica y (b) emite una TAREA de extraccion; un AGENTE (LLM-backed, modelo de confianza existente) extrae historias candidatas; las candidatas viven en estado `candidate` (fuera de PROPOSED); el operador revisa/edita/aprueba en un panel; solo las aprobadas pasan por el intake gobernado actual -> requisitos. PII-gate en el INGEST (antes de guardar / antes de que un agente lo toque). Plumbing determinista ya; la extraccion es trabajo de agente."
question: "Speceas la v2 con la opcion 4 (server no-egress emite tarea de extraccion + agente extrae + PII-gate en ingest + ruta de guardado + estado candidate + panel de revision + aprobar->intake)?"
one_line_summary: "Respuesta a tu pregunta de extraccion v2: ni opcion 1 (heuristica local pobre) ni opcion 2 (server llama LLM=egress). OPCION 4: el server NO extrae; subir = guardar archivo en ruta + emitir TAREA de extraccion; un AGENTE (ya LLM-backed) extrae candidatas (estado candidate, fuera de PROPOSED); operador revisa/aprueba; aprobadas -> intake gobernado. Server queda no-egress/determinista/#4-limpio; el LLM vive donde ya vive (agentes); no-determinismo fuera de #4. Gate: PII en ingest."
context_refs:
  - Area_comun/tasks/req-31100eaf-requirement-seed.md
deadline_or_blocking_level: normal
---

# RESP - mecanismo de extraccion v2: OPCION 4 (extraccion = trabajo de agente)

Tus 3 opciones asumen que la extraccion ocurre DENTRO del server (op1 heuristica local en server;
op2 el server llama al LLM = egress). Mi posicion: **el server no extrae nada.** Eso disuelve el
trilema.

## Mecanismo (OPCION 4)
1. **Subir = accion gobernada** que: (a) guarda el archivo en una **RUTA especifica** (p.ej.
   `Area_comun/intake/uploads/<id>/<archivo>`, server-derived, acotada); (b) **emite una TAREA**
   de extraccion ("leer el archivo X, extraer historias/casos de uso, generar candidatas"). Esto
   es determinista, sin egress, atestable en #4 (solo registra "archivo subido + extraccion pedida").
2. **Un AGENTE (Codex, ya LLM-backed) toma la tarea** y extrae -> produce **historias candidatas**.
   Es trabajo de agente del de siempre, NO una superficie de egress nueva del server.
3. Las candidatas viven en estado **`candidate`** (fuera de PROPOSED, no ensucian el backlog). El
   operador las **consulta / revisa / edita / aprueba** en un **panel de revision**.
4. Solo las **aprobadas** pasan por el **intake gobernado actual** -> requisitos/tareas (camino
   determinista y atestado que ya existe; el operador valida, con el formato requerido).

## Por que (responde tu preocupacion)
- El **server queda no-egress, determinista y #4-limpio** -- tu guard intacto. El LLM vive donde
  YA vive (los agentes); la metodologia ya acepta agentes LLM-backed procesando el dataset.
- El **no-determinismo del LLM queda FUERA de #4**: a lo atestado solo entra lo que yo apruebo,
  por el intake determinista (mismo patron que los SPECs: el agente genera no-determinista, el
  write gobernado es determinista y gateado por humano/checker).

## Gate innegociable: PII en el INGEST
El archivo subido es contenido EXTERNO nuevo (puede traer PII de terceros) y el dataset debe ser
PII-free. El screening de PII ocurre en el **ingest** (antes de guardar / antes de que un agente
lo toque), para que **ningun LLM de agente vea PII de terceros**. Consistente con la guarda PII
estructural del intake + DEF-PII/TASK-0118.

## Relacion con tus opciones
Es tu opcion 3 (plumbing determinista YA) pero corrigiendo el "LLM despues": ese paso NO es "el
server hace egress", es "**un agente extrae**" (modelo de confianza existente), gateado por
PII-en-ingest. Specea YA el plumbing (subir -> ruta -> tarea -> estado candidate -> panel de
revision -> aprobar -> intake); la extraccion la hace un agente.

## Matices para la SPEC (no bloqueantes)
- Las candidatas en estado `candidate` (no PROPOSED) hasta aprobarse.
- Ata la extraccion a que **un agente este en el loop** (no es instantaneo como un parse local).
- Definir la ruta de guardado acotada y su limpieza/retencion.

Descarto tu opcion 2 (egress directo del server). Canal ASCII.
