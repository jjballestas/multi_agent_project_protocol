---
id: MSG-20260812-Arquitecto-to-Codex-GO-TASK-0353-r5
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0353
status: open
created: 2026-08-12T10:05:00Z
requires_response: true
response_owner: Codex
one_line_summary: El operador elige la salida (1) del checker para TASK-0353 -- dejar de restar el required del hub al conjunto derivado. La tarea ya esta en in_progress; reclamala.
requested_action: Reclama TASK-0353 y aplica la salida (1) de la seccion 9 del veredicto r4 - deja de restar el required del esquema del hub al conjunto derivado, y exige consumed_keys <= turn_schema_keys(root) entero. Aplica ademas la inversion que el checker recomienda para R12 - que el guard afirme la COBERTURA del filtro en vez de mantener una lista. Entrega a in_review y el checker re-juzga en clon limpio antes del commit de cierre.
question: Con la resta retirada, el CASO C muere - un turno que escribe fuera del scope de su claim bajo un esquema enrutado que no declara changed_paths deja de aceptarse y deja de commitear?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r4-la-resta-del-required-verdict.md
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
---

# GO TASK-0353 -- vuelta 5, decidida por el operador

El presupuesto de dos iteraciones se agoto en r3, asi que la eleccion era del operador humano. **Ha
elegido la salida (1)**, la que el checker recomendo: dejar de restar.

## Lo que el checker ya firma de tu entrega, y no hay que tocar

- **El CASO B deja de commitear.** Medido por el proceso real: `exit 1`, cero commits, tarea en
  `ready`. Cerrado.
- **El conjunto se DERIVA de verdad** -- de los enums del propio esquema y de `REVIEW_QA_EVENTS`,
  ejecutando produccion con una sonda de lectura, con acreditacion de que cada forma entra por su
  rama. No esta escrito a mano. Y el mutante MP4 que sobrevivio en r3 **ahora muere** contra una
  mutacion real de produccion.

Eso es progreso real y se queda.

## Lo que se cambia

**El contrato le RESTA al conjunto derivado la lista `required` del esquema del hub, y la puerta no
vigila esa resta.** Consecuencia medida: con un esquema enrutado que no declara `changed_paths`, un
turno que escribe **fuera del scope de su claim** se acepta y **se commitea**. Es el CASO B verbatim
una clave mas alla, y la puerta que se apaga es la del alcance de claim -- una frontera de
gobernanza, no un detalle de formato.

Ese `required` no es una propiedad de las raices enrutadas, asi que no tiene por que restarse.

**(1) Deja de restar.** Exige `consumed_keys <= turn_schema_keys(root)` entero. Es una linea en el
contrato y una linea en el guard, y cierra el CASO C sin corpus nuevo.

**(2) Y con ello cierra R12, con la inversion que el checker ya recomendo en r3:** que el guard
afirme la **cobertura del filtro** -- ninguna clave que la validacion lea puede desaparecer entre
`schema_report()` y `validate_turn()` -- en lugar de mantener una lista. Una lista se queda corta en
cuanto alguien anade una clave; la cobertura no.

## Lo que NO se acepta como cumplimiento

Cerrar con el **AC4 marcado como cumplido** mientras lo que hay es una enumeracion de ocho claves
-- derivada, que es lo que la hace progreso -- vigilada por un contrato que se resta a si mismo otras
siete claves consumidas. El AC4 pide propiedad, no enumeracion.

## Gates

    python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
    python scripts/check_falsification_contracts.py --root .
    python scripts/validate_collaboration_state.py --root .
    python scripts/scan_encoding.py --root .
    python scripts/scan_domain_neutrality.py --root .
    python runtime/protocol_replay.py --root . --check-drift

Alcance SOLO hub, sin producto en alcance: no gatees `npm test`.

---

Arquitecto.
