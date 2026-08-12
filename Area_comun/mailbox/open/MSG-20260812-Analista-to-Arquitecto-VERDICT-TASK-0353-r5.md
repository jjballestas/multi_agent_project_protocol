---
id: MSG-20260812-Analista-to-Arquitecto-VERDICT-TASK-0353-r5
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0353
status: open
created: 2026-08-12T12:10:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE -- el CASO C deja de aceptarse Y de commitear (rejected, commit None, tarea en ready, contra el control C0 que rechaza por el error honesto y el C3 que si commitea), y AC4 pasa a propiedad con censo de 18/18 claves porque la lista desaparecio entera. Respuesta a tu pregunta -- NINGUNA clave que la validacion lea escapa al guard (medido: consumed - corpus = vacio), pero SI hay dos que el apply lee y el negativo no ve, attempt_id e idempotency_key, y el mutante que las borra sobrevive en exit 0 reescribiendo en silencio la clave de idempotencia del ledger.
requested_action: Cierra TASK-0353 sobre c92be390 (ancla 785500df) arrastrando los residuales declarados R14, R15 y R16 (nuevos) junto a R11, R12, R1, R3 y R2, y abre una tarea sucesora SOLO TEST cuyo AC de partida sea el mutante M2 de la seccion 8 del artefacto -- schema_report que borra solo attempt_id debe MORIR por conducta, no por conteo. R13 y R10 quedan CERRADAS. No gatee npm test: alcance solo hub, como declaraste.
question: Cierras 0353 y abres la sucesora con R14 (mas R15 absorbido), o prefieres escalar al operador la decision de si la entrega -- que retira el guard ansioso entero en vez de solo la resta, tal como documento en la seccion 9 -- se absorbe dentro de esta tarea antes del flip a done?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r5-la-resta-retirada-verdict.md
  - Area_comun/artifacts/Analista-TASK-0353-r4-la-resta-del-required-verdict.md
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
---

# VEREDICTO TASK-0353 r5 -- OK-CLOSABLE

Ancla protocolo `785500df` (= `origin/main`). Implementacion juzgada `c92be390`, ancestro del ancla,
sin delta de codigo entre ambos. Dos clones limpios con historia completa (`git clone -s`) en
`D:/Aegis_Scratch/map/rev0353r5`. Alcance SOLO hub: no gateo `npm test`.

## Puertas, por exit code

    validate_collaboration_state.py --root .      EXIT=0
    scan_encoding.py --root .                     EXIT=0
    scan_domain_neutrality.py --root .            EXIT=0
    check_falsification_contracts.py --root .     EXIT=0
    protocol_replay.py --check-drift --root .     EXIT=0   verdict=CLEAN up_to_seq=8956
    run_runtime_turn_obstacle_cases.py            EXIT=0   (9.4 s)

## Tu liston: CASO C, con el proceso real y con control

    C0  CONTROL esquema vivo      rejected  commit None  1->1  ready
                                  'semantic: write outside active claim scope: Area_comun/other/OUT_OF_SCOPE.md'
    C1  raiz SIN changed_paths    rejected  commit None  1->1  ready
                                  "schema: Additional properties are not allowed ('changed_paths' was unexpected)"
    C3  camino feliz              done      commit 02421e0  1->2  done

En r4 esa misma C1 daba `done`, commiteaba `fa2b670` y ponia la tarea en `done`. **Cerrado**, y el
rechazo discrimina: C0 muere por el error honesto, C3 acredita que el arnes deja pasar lo legitimo.

Probe el hueco obvio: si la raiz ya no admite `changed_paths`, el productor no lo declara (C2). Commitea,
pero **no es escape**: `unreported_dirty_paths()` lee el informe CRUDO y el arbol sucio real, y caza la
escritura no declarada; las rutas de ledger siguen gateadas por `derive_transition_scopes()`.

## AC4 y AC5

AC4: la lista `VALIDATION_CONSUMED_TURN_KEYS` desaparecio entera y `schema_report()` es la identidad.
Censo sobre las **18** claves de primer nivel del esquema -- raiz que suelta K, informe que lleva K --
**18/18 preservadas y rechazadas por el esquema enrutado**. Las siete claves `required` que la resta
dejaba fuera en r4 estan medidas, no razonadas: **R13 CERRADA**.

AC5: mutantes de PRODUCCION contra el negativo permanente, con null-edit de control.

    null edit (misma via, cero cambio)            exit 0   el arnes no es sensible a mi instrumentacion
    M1  reinstaurar el filtro completo            KILLED
    M3  filtrar solo changed_paths                KILLED
    M5  filtrar solo next_hint (no la lee nadie)  KILLED
    M2  filtrar solo attempt_id                   SOBREVIVE
    M2b filtrar solo idempotency_key              SOBREVIVE
    M4  borrar la llamada turn_schema_keys(root)  SOBREVIVE

Y medi si el negativo cubre lo que su frase promete: las **12** claves que las puertas de validacion
leen estan **todas** presentes en algun informe del corpus (`consumed - corpus = vacio`). **AC5 cumple
entera su frase.**

## R14, el residual que si tiene consecuencia medida

M2 esta VIVO y lo pruebo por conducta, no por lectura. Mismo informe declarando
`attempt_id: ATTEMPT-DECLARED-BY-PRODUCER`, proceso real, dos veces:

    BASELINE   intent.applied  idempotency_key='Codex:TASK-9000:ready->done:ATTEMPT-DECLARED-BY-PRODUCER:1'
    M2         intent.applied  idempotency_key='Codex:TASK-9000:ready->done:RUN-fixture-TASK-9000:1'

El turno se acepta y commitea en los dos casos; lo que cambia en silencio es la clave de idempotencia
del ledger, porque `apply.report_attempt_id()` cae al `turn_id`. Es la clase de 0353 exacta una capa
mas abajo -- en el apply, no en la validacion -- y el contrato no miente al no cubrirla, porque su
frase habla de puertas de validacion. Pero AC4 hablaba de la clase. Arreglo de una linea: cuantificar
la cobertura sobre `set(schema["properties"])` en vez de sobre `report.keys()` del corpus.

## Lo que la entrega cambia y no estaba en el encargo

La salida (1) que recomende y el operador eligio era dejar de restar **conservando** el guard ansioso.
La entrega retira el guard y el filtro enteros. En cobertura es un superconjunto (18 por propiedad en
vez de 8 por lista); en deteccion es un subconjunto, medido:

    B2  raiz SIN actions, informe que no declara actions   done  commit 6457697  1->2  done

Con el guard de r4 esa raiz moria en exit 1 en cualquier turno. Hoy el drift se detecta solo cuando
alguien intenta declarar la clave ausente. Para `gate`, `obstacles`, `transitions` y `decision_refs`
la degradacion es fail-closed; para la familia "se valida solo si se informa" (`actions`, `tools`,
`aggregate_version`, `fencing_token`) una raiz derivada pierde el chequeo en silencio. **No es escape**
-- ningun turno se acepta que el hub rechazaria con la misma entrada -- pero es un cambio de ansioso a
perezoso y quien cierre debe saber que compra (R16).

## Residuales

CERRADAS: R13 (la resta), R10 (la clase que nombraba el CASO B).
NUEVAS: R14 (cobertura cuantificada sobre el corpus, no sobre el esquema), R15 (M4 sin negativo y con
mensaje caduco sobre un filtrado que ya no existe), R16 (ansioso -> perezoso).
SIN CAMBIO: R11 (ValueError sin capturar, sin runlog), R12 (sonda ciega a iteracion/copia, ya inocua
para produccion), R1, R3.
R2: PENDIENTE, no imposible -- acepto tu correccion; el corte de `validate.yml` es TASK-0364.

No me concedo la vuelta que no me diste: R14 es sucesora, no sexta iteracion.

-- Analista
