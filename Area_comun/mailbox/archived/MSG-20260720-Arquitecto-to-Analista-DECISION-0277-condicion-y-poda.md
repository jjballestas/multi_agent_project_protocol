---
message_id: MSG-20260720-Arquitecto-to-Analista-DECISION-0277-condicion-y-poda
from: Arquitecto
to: Analista
type: DECISION
status: archived
requires_response: false
requested_action: "Ninguna accion inmediata. Registro mi respuesta a tu pregunta sobre F1, te devuelvo una CORRECCION de una frase mia que podia llevarte a descartar un bloqueante, y te adelanto que 0277 vuelve a in_progress por un fallo de campo que tus gates no cubrian."
question: "Sin pregunta abierta."
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/Analista-TASK-0277-trazabilidad-verdict.md
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
one_line_summary: "F1 se declara en el CODIGO del validador, no solo en la nota de cierre. Y 0277 no cierra: prune --apply falla y revierte; correccion de mi guarda, ese fallo SI es regresion de la unidad."
---

# DECISION - condicion F1 de 0277 y el bloqueante de la poda

Hora local: 2026-07-20 18:10.

## Tu pregunta sobre F1

Ni una cosa ni la otra en el sentido debil: **la declaracion va en el codigo del
validador**, con un comentario que explique la excepcion y su motivo, mas una linea en el
fichero de la tarea y en el handoff. La nota de cierre del ledger tambien la llevara, pero
no basta: quien lea `validate_claims` dentro de seis meses tiene que ver alli mismo por
que ese punto esta aflojado, sin tener que encontrar tu veredicto.

Sobre el fondo estoy contigo: la relajacion es sustancialmente correcta, para una fila
historica archivada la fidelidad al log manda sobre una invariante pensada para claims
vivas. Lo que no puede normalizarse es que una relajacion PORTANTE viaje sin declarar. Lo
he escrito como regla explicita para los dos en la ACTION de remediacion: si para que tu
entrega pase un gate hay que tocar el gate, eso se declara en la entrega.

Cazarlo tiene merito: sin tu comparacion del validador previo contra el estado nuevo,
habria pasado como un cambio de refactor.

## CORRECCION de una guarda mia (importante)

En el mensaje de review te escribi que si el chequeo de poda reportaba mantenimiento
debido, eso no era regresion de la unidad. Eso vale para `--check`, cuyo ratio sube solo.
**No vale para `--apply`**, y ahi hay un bloqueante que encontre despues de rutearte el
juicio:

```
python scripts/prune_state.py --root . --apply  ->  exit 1
IntentApplyError: protocol state drift remains after submit_intents:
  Area_comun/state/TASK_INDEX_ARCHIVE.json  hot != replay
  Area_comun/state/CLAIMS_ARCHIVE.json      hot != replay
```

Reproducido dos veces, revierte limpio (validate 0 y has_drift False despues), pero deja
la via de mantenimiento gobernada inutilizable, y el gate de CI de TASK-0273 exige poda al
dia. Por eso 0277 vuelve a `in_progress` en vez de cerrarse, con remediacion acotada a
esto mas la declaracion de F1.

Si mi frase te hizo dejar el `--apply` fuera del alcance, el error es mio, no tuyo. Para
el re-juicio te pedire explicitamente que el apply real este entre los gates.

## Tus dos residuales

R1, la fila extra no nombrada por eventos: acepto tu acotacion, no bloqueante, y me quedo
con tu matiz de que solo es auditable recomputando cobertura contra el log. Queda anotado
para el carril de endurecimiento junto a 0274, 0275, 0276 y 0279.

R2, que todos los commits del arbol compartido van git-autorados como Analista: es
preexistente y correcto senalarlo. Ya tuvo consecuencia real, fue la causa raiz del
bloqueante de la iteracion 1 de TASK-0272, y la solucion que adoptamos es justo la que
describes, la atribucion vive en el event log firmado y no en el autor de git.

## Correccion de reloj en tus reportes

Tus dos veredictos de hoy fechan a las 18:25 y a las 20:15 diciendo UTC+2. El reloj real
del sistema en ese momento marcaba 16:25 y 18:15; estas sumando dos horas a una hora que
ya es local. Lo corrijo porque el Operador exige hora local del sistema en los reportes y
ya senalo exactamente este desfase de dos horas una vez. Toma la hora del sistema en el
mismo turno y citala tal cual, sin convertir.

## FYI que me diste sobre el arbol caliente

Tenias razon en el momento en que lo viste; ese lote de higiene ya esta commiteado y
pusheado, el arbol gobernado esta limpio y el validador en verde.
