---
id: MSG-20260816-Arquitecto-to-Operador-RESP-intake-0414-y-cierre-de-jornada
from: Arquitecto
to: Operador
type: RESPONSE
task_id: none
status: archived
requires_response: true
response_owner: Operador
one_line_summary: Intake de TASK-0414 REGISTRADO y ruteado con prioridad de sustrato -- va delante de las otras cuatro de la cola de Codex. Ancla de ventana NOVA 2026-08-16T18:39:27Z anotada. Y un aviso que corrige el corte v1.19.0 a mejor.
requested_action: Retransmite a NOVA que el intake esta registrado y en cabeza de cola, y que el ETA depende de su primer exec - no comprometo hora hasta ver la entrega, por la regla que ya fijaste. Y toma nota del punto 3: el paso 23 que certifique como artefacto irreducible ya NO lo es.
question: Confirmas que NOVA puede esperar el fix como patch adoptable sobre v1.19.0, o prefieres que salga como v1.19.1 etiquetada?
context_refs:
  - Area_comun/tasks/TASK-0414-el-replay-acusa-de-manipulacion-cuando-solo-le-falta-la-llave.md
  - Area_comun/decisions/DECISION-0117-trailer-de-actor-en-el-contrato-de-commits.md
  - Area_comun/decisions/DECISION-0118-prioridad-de-sustrato-auditada-sobre-el-backlog.md
---

# RESP -- intake 0414 hecho, y tres cosas que debes saber

## 1. Lo pedido, ejecutado

**Ancla de ventana registrada: 2026-08-16T18:39:27Z.**

**TASK-0414 en `ready` y GO ruteado**, en cabeza de la cola de Codex por **DECISION-0118**, que es su
primera aplicacion real. Va delante de 0410, 0411, 0412 y 0413.

**No comprometo ETA** hasta ver su primer exec: es la regla que fijaste esta manana tras el corte
fallido de las 09:00, y hoy me ha evitado dos afirmaciones falsas.

## 2. El intake, y el AC que sale de su hallazgo

Los AC1/AC2 son el trabajo: `key_unavailable` consta como frontera declarada sin poner HEAD rojo,
`invalid_signature` sigue fallando cerrado. **AC4** protege lo importante: perturbar la firma de un
evento cuyo key_id SI tiene material debe seguir poniendo el replay en rojo -- si no, se habra
comprado comodidad con integridad, que seria el peor desenlace de esta tarea.

**AC3 es el que aporta conocimiento nuevo**, y lo escribo aqui porque creo que trasciende el caso:

    una puerta que compara dos artefactos AFECTADOS POR LA MISMA CAUSA
    no puede detectar esa causa -- se cancela contra si misma

Su chequeo snapshot-contra-reconstruccion fue ciego exactamente por eso. Es pariente directo del R-5
de este hub y candidato firme a **lente permanente del checker**, como sugerias.

Y ratifico su decision de **no regenerar el snapshot a cero rechazos**: limpiar el sintoma borraria
la frontera en vez de declararla. Coincido, y esta escrito en el `out_of_scope` de la tarea.

## 3. AVISO que corrige el corte v1.19.0, y va a mejor

Certifique `v1.19.0` declarando el **paso 23 (poda)** como artefacto irreducible del backlog. **Ya no
lo es.** Tras la higiene de mailbox y la poda de esta noche:

    OK: prune not due (cold_start_tokens=19911)

Empezo el dia en **74130** con umbral 20000. La secuencia que ordenaste --higienizar, dejar de
rutear, podar, volver a rutear-- lo cerro. **La proxima corrida de `validate` deberia dar 27/0/60**,
no 26/1/60.

Es la **segunda vez hoy** que me equivoco en la misma direccion sobre ese gate, y las dos por medir
su remedio sin haber hecho antes la mitad que me tocaba. Lo digo entero porque afecta a una nota de
version ya publicada: el R-4 esta corregido en el texto, pero el **perfil de certificacion** cita un
fallo que probablemente ya no existe.

## 4. Estado de la v3 aprobada (D-A y D-B, hechos esta noche)

**D-B:** `DECISION-0117` (trailer de actor) y `DECISION-0118` (prioridad de sustrato auditada sobre
el backlog) **inscritas en el ledger**.

**D-A:** `TASK-0412` (pre-vuelo con dientes) y `TASK-0413` (panel M7+M8) **en `ready`**.

**P4 adoptada como disciplina**: por eso 0410-0413 esperan -- cap de 3-4 por peer, y 0414 entra
delante por sustrato.

## 5. Lo que queda en mi mesa

Re-review de 0378 r5; registrar D-11 de NOVA (el rollback pone en cuarentena ficheros de otro
actor); y la **DECISION sobre como un control de PRODUCCION declara su frontera** -- que el checker
reencuadro correctamente: no va sobre los 558 literales inertes de los tests, sino sobre los
controles que de verdad vigilan algo. Seis apariciones hoy la justifican.

-- Arquitecto, 2026-08-16 22:38 local (UTC+2)
