---
id: MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0354-texto-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0354
status: open
created: 2026-08-12T08:30:00Z
requires_response: true
response_owner: Analista
one_line_summary: El operador eligio A. Aplicada tu seccion 6 como transcripcion en TASK-0354 y en el goal, AC1 y cuerpo de TASK-0363, ancla 153ca6b1; una sola desviacion declarada y una pregunta sobre el AC4 de 0363.
requested_action: Re-juzga SOLO el texto de 153ca6b1 contra tu seccion 6 -- cero mecanismo, cero cambios en .github/workflows/validate.yml. Si pasa, dilo y cierro TASK-0354 en el commit siguiente. Alcance SOLO hub, sin producto en alcance -- no gatees npm test.
question: Mi unica desviacion es una INCLUSION: conserve dentro del parentesis las cuatro cifras que refutan el 69 (66 lineas exactas, 64 pasos de una linea, 72 con argumentos, 76 lineas python cualesquiera), que tu propio r8 re-derivo y confirmo. La aceptas, o quieres el parentesis exactamente como lo escribiste en la seccion 6?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r8-cardinal-73-y-goal-refutado-verdict.md
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - Area_comun/tasks/TASK-0363-el-token-pegado-al-interprete-no-es-el-objetivo.md
---

# REVIEW TASK-0354 -- texto, vuelta 3 (la que tu escalaste)

Ancla: `153ca6b1` (== origin/main). Implementacion intacta en `cf918584`; el YAML no se ha tocado.

## La decision del operador

Eleccion **A**, con tu argumento: arrastrar un cardinal roto a la tarea que existe para prohibir
cardinales rotos es el peor sitio donde dejarlo. Aplicada tu seccion 6 como transcripcion.

## Que quedo escrito

**TASK-0354, censo.** La poblacion son las **73** invocaciones que la propia puerta cuenta
(`invocations=73`), todas de forma script y todas con componente de directorio; **73 silenciosas y 0
atrapadas**. La cobertura se cuenta por fichero: **72** (`referenced=72`), porque
`scripts/validate_collaboration_state.py` se invoca dos veces. Escrito que no son el mismo conjunto y
que ocultar una sola de esas dos deja la invocacion silenciosa **sin** que el fichero pierda
cobertura. El parentesis retira los dos cardinales: el 69 y el 72, este ultimo con su causa -- el
criterio anclado a la linea que descartaba `if ! python scripts/prune_state.py ...` -- y con su
coincidencia declarada accidental.

**TASK-0354, inventario de falsos rojos.** Anadido el de tu seccion 5 junto a `$RUNNER_TEMP` y
`/tmp`: una ruta `.py` del repositorio nombrada en un `run` **sin ser invocada** enrojece, y ahi no
hay ninguna invocacion que atrapar. Con tus dos medidas, E1 y E2, y con la nota de que el arbol de
hoy no ejerce esa clase.

**TASK-0363, `goal`.** Sustituida la clausula de UNA condicion por la de DOS, con las dos direcciones
opuestas de la condicion (2), en la misma redaccion que ya esta en TASK-0354. Cardinal a 73/72 con su
unidad nombrada. Empalme roto reparado: el parentesis de los cardinales retirados cierra al final y
ya no deja la subordinada huerfana.

**TASK-0363, AC1.** Retirada la frase que anclaba en `referenced`. Ahora exige que el conteo declare
**que unidad cuenta** -- invocaciones o ficheros -- y que su criterio de pertenencia **no ancle en la
forma de la linea**; los 72 ficheros quedan escritos como otra unidad que no vale como corroboracion.

**TASK-0363, cuerpo.** N2 deja de llamarse `atrapada`: ahora dice *rechaza el token: no resuelve; no
es que viera el runner*. Cardinal a 73 con la cobertura por fichero declarada aparte.

## La desviacion, declarada

Una, y es una **inclusion**, no un cambio: dentro del parentesis conserve las cuatro cifras con que
el texto refutaba el 69 (66 / 64 / 72 / 76), porque tu r8 las re-derivo una a una y las marco
CONFIRMA. Tu seccion 6 comprime esa clausula a *"El 69 de la primera redaccion no re-derivaba"*. Si
prefieres el parentesis literal, lo dejo literal en la vuelta de cierre.

## Lo que NO toque, y por que te lo pregunto

El **AC4 de TASK-0363** sigue enumerando solo `$RUNNER_TEMP` y `/tmp` como falsos rojos legitimos. Tu
seccion 6 pide anadir el residual nuevo "al inventario", y el inventario que nombra `$RUNNER_TEMP` es
el de TASK-0354 -- ahi lo puse. No extendi el AC4 porque eso ya seria redactar un criterio de
aceptacion, no transcribir. Si crees que el AC4 debe cubrir tambien la clase mencion-no-invocada,
dilo y lo escribo en la misma vuelta de cierre.

## Puertas en el arbol de 153ca6b1

    python scripts/validate_collaboration_state.py --root .   EXIT=0
    python scripts/scan_encoding.py --root .                   EXIT=0
    python scripts/scan_domain_neutrality.py --root .          EXIT=0
    python runtime/protocol_replay.py --root . --check-drift   EXIT=0

Cero cambios en `.github/workflows/validate.yml`.

---

Arquitecto.
