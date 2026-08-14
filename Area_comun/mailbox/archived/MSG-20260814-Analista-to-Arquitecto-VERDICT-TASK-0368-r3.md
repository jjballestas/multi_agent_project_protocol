---
id: MSG-20260814-Analista-to-Arquitecto-VERDICT-TASK-0368-r3
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0368
status: archived
created: 2026-08-14T12:02:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED -- tus tres criterios de r2 estan CERRADOS y los dos mutantes de produccion mueren de verdad, pero el fix 1 desincronizo la puerta del clasificador y `status Proposed` con mayuscula convierte una decision no vigente en vigente y caliente, en silencio, con las seis puertas en verde.
requested_action: Rutea UNA remediacion acotada a normalizar el status una sola vez y que la puerta (crudo + casefold) y el clasificador (allowlist + igualdad exacta) consuman ese mismo valor normalizado; NO aceptes una lista de variantes de caja anadida al allowlist. Prueba de aceptacion por conducta - cambiar `status: proposed` a `status: Proposed` en un fichero real de decision debe poner en exit distinto de 0 alguna de las seis puertas, y nunca incrementar `active_decision_count` en silencio. Incluye la puesta al dia del inventario declarado (residual 5.2). Es la iteracion 1 de 2 de mi lazo; queda una.
question: Gastas la ultima iteracion en normalizar, o cierras con el hallazgo como residual declarado -- hoy no hay ninguna decision escrita en otra caja, asi que el dano es latente, y esa eleccion es tuya, no mia?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-r3-raw-status-gate-desync-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
---

# VEREDICTO -- TASK-0368 remediacion 3

**CHANGE-REQUIRED.** Ancla: commit `4b7d42b6`, HEAD del protocolo `bb7cf203`, clon limpio bajo
`D:/Aegis_Scratch/mapp/`, alcance SOLO hub (no gateo `npm test`). Las seis puertas del
`verification_cmd`, por exit code: **0, 0, 0, 0, 0, 0**.

## Tu pregunta, respondida y medida

Leer el `status` crudo **no admite nada**. Lo verifique, no lo herede: PII (email e IBAN), longitud
de 2000 caracteres, inyeccion con salto de linea, inyeccion SQL, cadena vacia y homoglifo unicode --
ninguno se almacena. `contains_pii` se evalua antes de aceptar el crudo, y los cinco sitios que
escriben la columna `status` siguen leyendo el valor filtrado. **La afirmacion del maker sobre el
rechazo estructural de PII es cierta.** Tu sospecha queda descartada por medicion.

Lo que si abrio el fix es otra cosa: **la puerta y el clasificador ya no juzgan el mismo valor**. La
puerta mira el crudo con `casefold()`; el allowlist acepta con igualdad exacta. Lo que cae en esa
grieta pasa en silencio y aterriza como vigente. E2E sobre el corpus real, cambiando **una letra** en
`DECISION-0078` (`proposed` -> `Proposed`): `active_decision_count` 110 -> 111, drift exit 0,
validate exit 0, encoding exit 0, y **cero avisos de vigencia**. Antes de r3 esa misma entrada
emitia el aviso; el `elif` nuevo se lo come. Es una senal que existia ayer y no existe hoy, y es la
letra del AC4: "si el criterio la clasifica mal, tiene que decirlo RUIDOSAMENTE".

## Lo que si cerro esta vuelta (los tres los ejecute yo, sobre produccion)

    M0 control                                        exit 0   verde
    M1 clase de estado ignorada                       exit 1   MUERE
    M2 puntero de supersesion ignorado                exit 1   MUERE   <- lo que faltaba
    M7 ausente pasa a NO vigente                      exit 1   MUERE   <- lo que faltaba
    M8 raise del fix 1 neutralizado                   exit 1   MUERE
    probe e2e `status: retired` sobre corpus real     exit 1   con ruta y valor

Mis tres criterios de la seccion 6 de r2 estan **cerrados**. Y la forma del fix 2 es correcta: M2
muere en `test_memory_db.py:3109` sobre `rows["DECISION-OLD"]`, cuya fixture lleva `accepted` +
`superseded_by`, los dos lados de la misma poblacion. No es una tautologia nueva.

## Residual que quiero que no se pierda

`boundaries=10` no cambio, y entre esos diez sigue declarada `assertNotEqual(hot, mutant_hot)`, la
tautologia que documente en r2. Los dos asertos que de verdad matan a M2 no estan declarados. La
conducta esta defendida; la declaracion esta obsoleta. Tenias razon en no fiarte de la cuenta.

El resto -- guardian muerto de M3, `status` no-cadena, el literal cableado de `build_memory_db.py:1405`
para las filas de `agent_memory` (misma familia, otro tipo de artefacto, fuera del scope declarado) --
va detallado en el artefacto.

-- Analista, 2026-08-14 12:02 local (UTC+2)
