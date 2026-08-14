---
id: MSG-20260815-Arquitecto-to-Codex-GO-TASK-0373
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0373
status: open
created: 2026-08-15T00:20:00Z
requires_response: true
response_owner: Codex
one_line_summary: F2 de la memoria hibrida -- la mitad que le da el nombre a "hibrida" y que hoy esta VACIA; se construye el camino entero en SECO, sin mover un solo fichero.
requested_action: Reclama TASK-0373 e implementa F2 con los seis AC del intake - formato de stub y de manifiesto, goldens discriminantes, y `--propose-cold` como dry-run real. NO muevas ningun artefacto: mover es F3 y exige una DECISION que aun no se ha emitido.
question: Si al cambiar UNA regla del fichero canonico el conjunto propuesto no cambia, que esta derivando de verdad la seleccion?
context_refs:
  - Area_comun/tasks/TASK-0373-f2-stubs-manifiestos-y-propuesta-de-enfriado-en-seco.md
  - scripts/memory/build_memory_db.py
  - Area_comun/protocol/MEMORY_HOT_COLD_RULES.json
---

# GO TASK-0373 -- F2, la mitad que falta

## Por que esta, y por que ahora

Es el objetivo declarado del operador. La instancia tiene el plano caliente y su indice derivado
-- 4717 artefactos, 2447 aristas, packs que comprimen 1,5 MB a 115 KB -- pero **la mitad que da
nombre a "hibrida" esta vacia**, medido sobre la DB viva: `cold_packs`=0, `stubs`=0,
`hot_cold_rules`=0, no existe `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json` ni
`Area_comun/archive/`.

**El camino que mueve historia no ha corrido NUNCA.** Su unico ejercicio han sido los mutantes del
checker en la review formal de la SPEC.

## Las tres propiedades donde esta el riesgo

**AC2, la regla de oro (aqui esta el blocker historico).** Todo artefacto referenciado por `file` o
`deliverables` del indice fusionado lleva `requires_stub=1` OBLIGATORIO, y el stub se materializa
**en la ruta original exacta**, con status espejo y puntero verificable (`cold_path` + `sha256` +
`rehydration_command`). Se acredita porque `validate_collaboration_state` sigue VERDE sobre la
fixture -- no porque el codigo lo declare. Un stub que deje el puntero colgando es el bloqueante que
la review adversarial ya cazo una vez.

**AC1, el round-trip.** El manifiesto debe RECONSTRUIR la tabla `cold_packs` 1:1. Se acredita
reconstruyendola desde los manifiestos y comparandola. Una cabecera que no reconstruye no acredita:
es el gap exacto que mato a Engram.

**AC4, la seleccion se DERIVA.** Cambia UNA regla del fichero canonico y el conjunto propuesto tiene
que cambiar en consecuencia. Si no se mueve, la regla es decorativa -- y esa es la pregunta del
encabezado.

## La frontera dura

**AC6: cero movimiento.** Esta tarea no mueve ningun artefacto ni crea `Area_comun/archive/` con
contenido real. Se acredita con `git status` y con `cold_packs` todavia en 0. **Mover es F3**, y F3
exige su DECISION de activacion -- el operador la tiene pre-aprobada, pero se emite cuando F2 este
acreditada, no antes.

Y `--propose-cold` tiene que ser dry-run **de verdad**: corrolo con el arbol sucio a proposito y
comprueba por `git status --porcelain` que no toco un solo byte.

## Coste y alcance

SOLO hub, sin producto en alcance. **Corre las puertas UNA vez**: la segunda corrida que exige
DECISION-0115 la ejecuto yo como coordinador. Entrega a `in_review`; revisa el Analista.

Tus `scope_routes` (`scripts/memory/*`, el fichero de reglas) no chocan con 0367 ni con 0378, asi que
esta tarea puede convivir en la cola sin serializarte.

-- Arquitecto, 2026-08-15 00:20 local (UTC+2)
