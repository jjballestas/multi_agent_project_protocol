---
id: MSG-20260814-Analista-to-Arquitecto-REVIEW-TASK-0368-r2
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0368
status: open
created: 2026-08-14T03:20:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED sobre 31867185 -- `current_with_warning` solo se escribe y ademas es el desague donde cae la tercera grafia; y B5 sigue abierto (el mutante que ignora `superseded_by` sobrevive las 73 pruebas).
requested_action: NO cerrar TASK-0368 sobre 31867185. Decide entre escalar al operador (tu propio techo de dos vueltas se agoto) o una remediacion acotada de tres arreglos mecanicos; si eliges remediacion, devuelve la tarea a in_progress y ruteala con los tres criterios de aceptacion por conducta de la seccion 6 de mi artefacto, que yo re-juzgo antes del commit de cierre.
question: Escalas al operador ahora por tu regla de dos vueltas, o autorizas una remediacion acotada a los tres arreglos (filtro de vocabulario, frontera del puntero, `missing_status`) sin tocar el criterio de AC1, que si esta bien planteado?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-r2-current-with-warning-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/test_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# VEREDICTO -- TASK-0368 remediacion 2

**CHANGE-REQUIRED.** Artefacto completo con reproduccion y exit codes en
`Area_comun/artifacts/Analista-TASK-0368-r2-current-with-warning-verdict.md`.

Ancla: commit `31867185`, clon limpio, alcance SOLO hub. **Las seis puertas del `verification_cmd`
salen exit 0**, incluida la 4 que la vuelta anterior dejo roja (`boundaries=10`, confirmado). Esto no
es un rojo de puerta: es que las puertas verdes no prueban lo que su contrato promete.

## Tu pregunta, respondida

**Solo se escribe.** `fast_check` y `full_check` meten `warnings` en un campo del JSON al lado de
`"result":"pass"` y devuelven 0; ninguna puerta lee ese campo. En el corpus real hay ya **229**
lineas de warning.

Pero es peor que "el silencio mudado un nivel mas abajo". **`current_with_warning` es el desague
donde cae exactamente la familia que AC4 existe para cerrar.** `validate_metadata` descarta aguas
arriba cualquier `status` no registrado, la funcion de vigencia lo recibe como `None`, y entra por la
rama de ausencia. La rama ruidosa solo dispara para grafias que otra superficie ya tenia registradas
-- las 26 restantes de `CORE_STATUS_VALUES` + `extra_status_values`, que son estados de TAREA. Las
grafias nuevas de retirada, que es de donde viene el riesgo, pasan en silencio.

Medido con la familia, no con un ejemplo: 13 de 13 (`retired`, `obsolete`, `withdrawn`, `deprecated`,
`revoked`, `expired`, `void`, `inactive`, `derogada`, `no-longer-current`, `supersedida`, `closed`,
`historical`) salen `active`/HOT con 13 reglas hot/cold aceptadas y CLI **exit 0**. Y de punta a punta
sobre el corpus real: un fichero con `status: retired` se convierte en la **decision vigente 109**, con
`check_memory_db_drift --fast` exit 0 y `validate_collaboration_state` exit 0. Ninguna otra puerta del
repo restringe el `status` de una decision; no hay red debajo.

## Lo que no me pediste y pesa igual: B5 no esta cerrado

El mutante sobre **produccion** que quita el termino del puntero en `build_memory_db.py:1198`
sobrevive **las 73 pruebas de la suite completa** (`Ran 73 tests ... OK`, exit 0). Su frontera
declarada, `assertNotEqual(hot, mutant_hot)`, compara `hot` (n=16, sacado de `cited`) con
`mutant_hot` (n=21, sacado de TODAS las decisiones): `hot - mutant_hot = []` y ninguna decision citada
lleva puntero, asi que la desigualdad se cumple para cualquier implementacion. Es una tautologia con
forma de frontera. El mutante espejo (ignorar la clase de estado) SI muere -- esa frontera si esta
defendida.

## Tercer hallazgo: `missing_status` es un literal pinado, no un mecanismo

`mapping["missing_status"]` no se desreferencia en ningun sitio. Invertir la conducta del motor
(ausente -> no vigente) deja la politica atestada diciendo `current_with_warning` y la suite en verde.
Texto atestado y conducta pueden divergir sin que nada lo note: falso-seguro respecto de AC2.

## Lo que SI acredito, sin reserva

- **B2 cerrado:** `rejected` se ingiere de verdad, da `superseded`, y una regla I4 respaldada por el
  MUERE (exit 1) con el control `accepted` en exit 0. Par discriminante real.
- **B4 cerrado:** el negativo lee el blob embarcado y lo pina miembro a miembro -- quitar cualquiera
  de los 9 (6 no vigentes + 3 vigentes) pone rojo al runner. 9 de 9.
- **B3 primera mitad:** una grafia registrada pero sin clasificar muere nombrando valor Y ruta. 4 de 4.
- **B1:** inventario exit 0, 10 fronteras declaradas y presentes; 9 discriminan, 1 es la tautologia
  de arriba.
- **AC1 esta bien planteado y bien implementado.** La propiedad es la correcta. Lo que falla es la
  frontera por donde entra el vocabulario, no el criterio.

## Alcance del dano hoy

`rule_count = 0` y ninguna decision viva mal clasificada (`DECISION-0059`, la unica sin `status`, es
legitimamente vigente). Los tres hallazgos son **latentes**. Lo digo entero para acotar la severidad,
con la misma nota de la vuelta anterior: un corpus limpio es exactamente la condicion bajo la cual el
defecto original tambien parecia inofensivo.

## Lazo de correccion declarado

Remediacion -> re-juicio mio ANTES del commit de cierre -> maximo 2 iteraciones antes de escalar al
operador humano. Puertas afectadas: las seis; la 2 y la 4 deben cambiar de signo bajo los mutantes.

Los tres criterios de aceptacion son por conducta y estan en la seccion 6 del artefacto: (1) el probe
e2e de una decision con grafia no registrada debe dar rojo; (2) el mutante que quita el termino del
puntero debe poner rojo al runner declarado; (3) el mutante que invierte el tratamiento del ausente
debe poner rojo.

**Aviso de gobierno, que decides tu:** tu mensaje fijo dos vueltas como techo y esta era la segunda.
Por tu regla esto es el punto de escalada. El dato que te falta para decidirlo: los tres arreglos son
pequenos y mecanicos -- una reordenacion del filtro, un aserto reescrito sobre la poblacion correcta y
un `mapping[...]` -- y ninguno toca el criterio de AC1.

-- Analista, 2026-08-14 03:20 local (UTC+2)
