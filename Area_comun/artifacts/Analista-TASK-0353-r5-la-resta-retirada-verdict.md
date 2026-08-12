# Analista -- veredicto TASK-0353 r5: la resta se retiro y con ella el filtro entero

Reviewer: Analista (independent adversarial checker)
Date: 2026-08-12 14:05 (hora local UTC+2)
Task: TASK-0353 -- remediacion 5
Instruction: `Area_comun/mailbox/open/MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0353-r5.md`
Scope declarado por Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE (no gateo `npm test`).

**Recommendation: OK-CLOSABLE**, con residuales declarados y una sucesora concreta.

Tu liston se cumple y esta medido con el proceso real: **el CASO C deja de aceptarse y deja de
commitear**. Y AC4 deja de descansar en una enumeracion, porque **ya no hay lista**: `schema_report()`
es la identidad, asi que no hay clave que pueda desaparecer -- lo verifique sobre las **18** claves de
primer nivel del esquema, no sobre un ejemplo.

Respuesta directa a tu pregunta, en dos partes porque la honesta tiene dos:

1. **En produccion, ninguna.** Ninguna clave desaparece entre `schema_report()` y `validate_turn()`,
   porque no se filtra nada. Censo de las 18: preservadas las 18.
2. **En el guard, dos** -- pero fuera de lo que el contrato promete. `attempt_id` e
   `idempotency_key` no aparecen en ningun informe del corpus, asi que un filtro que borre
   exactamente esas dos **sobrevive en exit 0**. No las lee la validacion (por eso el negativo no
   miente), las lee `apply.report_attempt_id()`, y el efecto medido es que la clave de idempotencia
   del ledger se reescribe en silencio.

---

## 1. Ancla canonica y reproduccion

| item | value |
|---|---|
| ancla de la review (protocol HEAD) | `785500dfa5ea68d7e3d72a4ab719846e66374de4` (= `origin/main`) |
| commit de implementacion juzgado | `c92be390` (ancestro del ancla: verificado) |
| delta `c92be390..785500df` en rutas de codigo | **ninguno** (`runtime/state/events.jsonl` y `snapshot.json` solamente) |
| clon limpio A (puertas) | `D:/Aegis_Scratch/map/rev0353r5/clone` @ `785500df` |
| clon limpio B (sondas y mutantes) | `D:/Aegis_Scratch/map/rev0353r5/clone2` @ `785500df` |
| clonado con | `git clone -s` (historia completa; un `--depth 1` da rojo falso) |
| python | 3.12.10 |

Nada se midio en arbol caliente. Cada veredicto es un exit code real o la salida JSON del proceso.
Los dos clones quedaron con `git status --short` vacio al terminar.

### Puertas de protocolo en el ancla, exit codes reales (clon limpio A)

```
python scripts/validate_collaboration_state.py --root .   EXIT=0   OK: collaboration state is valid.
python scripts/scan_encoding.py --root .                  EXIT=0   OK: encoding scan is clean.
python scripts/scan_domain_neutrality.py --root .         EXIT=0
python scripts/check_falsification_contracts.py --root .  EXIT=0
python runtime/protocol_replay.py --check-drift --root .  EXIT=0   verdict=CLEAN up_to_seq=8956
python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py  EXIT=0  (9.4 s)
```

Ancla verde, drift 0.

---

## 2. Tabla vector por vector

| vector | veredicto | evidencia |
|---|---|---|
| **CASO C -- el liston**: raiz sin `changed_paths`, escritura fuera del scope del claim | **PASS -- cerrado** (rechazado, sin commit, tarea en `ready`) | seccion 3 |
| CASO C-2: la raiz omite `changed_paths` y el productor tambien | **PASS -- no es escape** (segunda puerta independiente) | seccion 4 |
| CASO B (r4): raiz sin `actions` + `contract_change` sin `decision_refs` | **PASS -- sigue cerrado**, ahora por rechazo de esquema | seccion 5 |
| AC4 -- propiedad, no enumeracion | **PASS** -- censo de 18/18 claves, la lista desaparecio | seccion 6 |
| AC5 -- negativo permanente por mutacion de PRODUCCION | **PASS en todo lo que promete** (M1, M3, M5 mueren) / **SLIP de poblacion** (M2, M2b, M4 sobreviven) | secciones 7 y 8 |
| (nuevo) el negativo cubre toda clave que la validacion lee? | **SI, medido**: `consumed - corpus = (vacio)` | seccion 7 |
| (nuevo) deteccion de drift: ansiosa -> perezosa | **REGRESION declarada, no escape** | seccion 9 |

---

## 3. El liston: CASO C, proceso real, con control

Misma configuracion que el escape que firme en r4: raiz enrutada a la que le quito `changed_paths`
de `properties` **y** de `required`; el productor declara una escritura fuera del scope de su claim
(`Area_comun/other/OUT_OF_SCOPE.md`). Proceso real (`orchestrator.py --run --once --replay-report`),
conteo de commits del propio fixture antes y despues.

```
C0  CONTROL, esquema vivo, el mismo turno
  PROCESS exit   : 0   outcome: rejected   commit: None
  errors         : ['semantic: write outside active claim scope: Area_comun/other/OUT_OF_SCOPE.md']
  COMMITS        : 1 -> 1     NOT COMMITTED      task status: ready

C1  raiz enrutada SIN changed_paths           <-- el escape de r4
  PROCESS exit   : 0   outcome: rejected   commit: None
  errors         : ["schema: Additional properties are not allowed ('changed_paths' was unexpected)"]
  COMMITS        : 1 -> 1     NOT COMMITTED      task status: ready

C3  camino feliz, esquema vivo (control de que el arnes discrimina)
  PROCESS exit   : 0   outcome: done       commit: 02421e0
  COMMITS        : 1 -> 2     COMMITTED          task status: done
```

En r4 esta misma configuracion devolvia `outcome: done`, commiteaba (`fa2b670`) y ponia la tarea en
`done`. Hoy no. **CASO C cerrado.** La frontera de escritura del sistema de claims deja de apagarse
por la lista de propiedades de una raiz enrutada.

Y no cierra por casualidad: el control C0 rechaza por el error honesto y C3 acredita que el arnes si
deja pasar un turno legitimo. El rechazo de C1 discrimina.

---

## 4. Lo que intente colar por el hueco que abre C1

Si el esquema enrutado ya no admite `changed_paths`, un productor deshonesto no lo declara. Medi esa
variante:

```
C2  raiz SIN changed_paths, informe que OMITE changed_paths
  PROCESS exit   : 0   outcome: done   commit: a7c0469   COMMITTED   task status: done
```

Commitea -- pero **no es escape**, y lo acredito en vez de suponerlo. La frontera tiene una segunda
puerta que no depende del esquema enrutado: `orchestrator.unreported_dirty_paths()` compara el arbol
sucio real contra el informe **crudo**. Con la escritura fuera de scope presente y sin declarar:

```
routed schema declares changed_paths : False
report declares changed_paths        : False
unreported_dirty_paths(...)          : ['Area_comun/other/OUT_OF_SCOPE.md', 'runtime/turn_schema.json']
validate_turn(filtered)              : []
```

`validate_turn` no ve nada que gatear, pero el turno muere antes en la puerta de arbol sucio. Y las
rutas de ledger que si toca C2 (`TASK_INDEX`, `PROJECT_STATE`, `CLAIMS`) siguen gateadas contra el
scope por `derive_transition_scopes()`, que lee `transitions`, no `changed_paths`. La frontera de
claims queda defendida en profundidad.

---

## 5. El CASO B sigue muerto, por otro camino

```
B0  CONTROL esquema vivo   : rejected, commit None, 'semantic: gate.decision_required: action contract_change requires decision_refs'
B1  raiz SIN actions       : rejected, commit None, "schema: Additional properties are not allowed ('actions' was unexpected)"
```

En r4 moria por el guard ansioso con `ValueError`; ahora muere por el esquema enrutado, que es quien
manda. Sin commit en ninguno de los dos. Lo que firme en r4 no se reabre.

---

## 6. AC4: el censo, no el ejemplo

AC4 pide propiedad y no enumeracion. La entrega retira `VALIDATION_CONSUMED_TURN_KEYS` entera y deja
`schema_report()` como identidad (`turn_schema_keys(root); return dict(report)`). No queda lista que
mantener, asi que no hay lista que pueda divergir.

No me quedo con el argumento. Censo sobre **las 18 claves de primer nivel del esquema del hub**: para
cada clave K, una raiz enrutada que suelta K de `properties` (y de `required` si estaba) mas un
informe que **lleva** K.

```
key                  in report  preserved  schema err names K  verdict
turn_id              True       True       True                PASS
task_id              True       True       True                PASS
agent                True       True       True                PASS
outcome              True       True       True                PASS
summary              True       True       True                PASS
changed_paths        True       True       True                PASS
obstacles            True       True       True                PASS
tools                True       True       True                PASS
actions              True       True       True                PASS
decision_refs        True       True       True                PASS
attempt_id           True       True       True                PASS
idempotency_key      True       True       True                PASS
aggregate_version    True       True       True                PASS
fencing_token        True       True       True                PASS
transitions          True       True       True                PASS
commit_message       True       True       True                PASS
gate                 True       True       True                PASS
next_hint            True       True       True                PASS
SUMMARY: PASS = 18 / 18
```

Las siete claves que la resta dejaba fuera en r4 (`turn_id`, `task_id`, `agent`, `outcome`,
`summary`, `changed_paths`, `commit_message`) estan medidas aqui, no razonadas. **R13 de r4:
CERRADA.** Y el criterio ya no es "que la lista contenga los campos": es "que nada se borre". Esa si
es la propiedad que AC4 pedia.

---

## 7. AC5: el negativo cubre exactamente lo que promete

El contrato declara: *"A top-level field read by any routed validation gate cannot be removed by the
orchestrator schema filter."* La pregunta adversarial correcta no es si el mutante central muere,
sino si la asercion **cuantifica sobre la poblacion que la frase nombra**. La asercion recorre los
informes del corpus:

```python
for report in corpus.values():
    assert report.keys() <= orchestrator.schema_report(report, fixture_root).keys()
```

Eso cubre las claves **presentes en el corpus**, no las claves que la validacion **lee**. No son lo
mismo: `TurnReadProbe.get` registra la clave aunque el informe no la lleve. Asi que lo medi:

```
consumed_keys (leidas por las puertas de validacion):
  actions, agent, aggregate_version, changed_paths, decision_refs, fencing_token,
  gate, obstacles, outcome, task_id, tools, transitions      (12)

LEIDAS POR VALIDACION pero NUNCA PRESENTES en ningun informe del corpus  ->  (ninguna)
```

**El negativo mantiene su promesa entera.** Toda clave que una puerta de validacion lee esta presente
en al menos un informe del corpus, luego un filtro que la borre muere. AC5 cumplido en la poblacion
que su frase nombra.

---

## 8. Mutantes de PRODUCCION: cuales mueren, cuales no, y por que importa

Mutaciones aplicadas solo a `runtime/orchestrator.py` en el clon limpio B, cuerpo de `schema_report()`.
Gate = exit code real de `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`. Fichero
restaurado tras cada corrida (`git status --short` vacio al final).

| mutante de PRODUCCION | resultado |
|---|---|
| BASELINE | exit 0 |
| **null edit** (mismo cuerpo, reescrito por la misma via que los mutantes) | exit 0 -- el arnes no es sensible a mi instrumentacion |
| **M1** -- reinstaurar el filtro completo (`if key in allowed_keys`) | **KILLED** (exit 1) |
| **M3** -- filtrar solo `changed_paths` | **KILLED** (exit 1) |
| **M5** -- filtrar solo `next_hint` (clave que la validacion NO lee) | **KILLED** (exit 1) |
| **M2** -- filtrar solo `attempt_id` | **SOBREVIVE** (exit 0) |
| **M2b** -- filtrar solo `idempotency_key` | **SOBREVIVE** (exit 0) |
| **M4** -- borrar la llamada de efecto `turn_schema_keys(root)` | **SOBREVIVE** (exit 0) |

M1 es el credito central y cierra el eje: la regresion exacta que reintroduciria la clase muere. M5
acredita ademas que la asercion es mas fuerte que su frase (mata el borrado de una clave que la
validacion ni lee) -- su unico punto ciego es la ausencia del corpus.

**M2 esta VIVO, y lo pruebo por conducta, no por lectura.** Un informe que declara
`attempt_id: "ATTEMPT-DECLARED-BY-PRODUCER"`, por el proceso real, dos veces:

```
BASELINE
  claim.acquired   idempotency_key='Codex:TASK-9000:claim:ATTEMPT-DECLARED-BY-PRODUCER:0'
  intent.applied   idempotency_key='Codex:TASK-9000:ready->done:ATTEMPT-DECLARED-BY-PRODUCER:1'
                   payload.attempt_id='ATTEMPT-DECLARED-BY-PRODUCER'

M2-drop-attempt_id
  claim.acquired   idempotency_key='Codex:TASK-9000:claim:RUN-fixture-TASK-9000:0'
  intent.applied   idempotency_key='Codex:TASK-9000:ready->done:RUN-fixture-TASK-9000:1'
                   payload.attempt_id='RUN-fixture-TASK-9000'
```

El turno se acepta y commitea en los dos casos; lo que cambia en silencio es **la clave de
idempotencia del ledger**, porque `apply.report_attempt_id()` cae al `turn_id` cuando el campo no
esta. Es la clase de TASK-0353 exacta -- produccion borra el campo que produccion consume -- una capa
mas abajo: no en la validacion, en el apply. El contrato no miente al no cubrirlo (su frase habla de
puertas de validacion), pero **AC4 hablaba de la clase**, y en la clase este hueco esta abierto.

M4 sobrevive porque `assert_open_schema_is_rejected()` llama a `orchestrator.turn_schema_keys()`
**directamente**, no a traves de `schema_report()`. Esa llamada es hoy el unico consumidor de
`turn_schema_keys` en la ruta de produccion, nadie la defiende, y su diagnostico
(`orchestrator filtering requires additionalProperties=false`) describe un filtrado que ya no existe.
Severidad baja y lo digo con la razon medida: sin filtro, un esquema abierto ya no borra nada, asi
que perder esa comprobacion no abre ninguna puerta -- pero es una linea de produccion sin negativo y
un mensaje caduco.

---

## 9. Lo que la entrega cambia y no estaba en el encargo

Te lo marco porque no es lo que el operador autorizo palabra por palabra. La salida (1) que yo
recomende y el operador eligio era: **dejar de restar** y exigir `consumed_keys <=
turn_schema_keys(root)` entero -- es decir, conservar el guard ansioso y ampliarlo. La entrega hace
algo distinto: **retira el guard y el filtro**, y deja que el esquema enrutado rechace.

En cobertura es un superconjunto (18 claves por propiedad en vez de 8 por lista, y R12 deja de morder
la garantia de produccion). En deteccion es un subconjunto, y lo medi:

```
B2  raiz enrutada SIN actions, informe que NO declara actions
  PROCESS exit: 0   outcome: done   commit: 6457697   COMMITTED   task status: done
```

Con el guard de r4, esa raiz moria en exit 1 en **cualquier** turno: el drift se detectaba solo. Hoy
se detecta solo cuando alguien intenta declarar la clave ausente. Para `gate`, `obstacles`,
`transitions` y `decision_refs` la degradacion es fail-closed (el turno que las necesita se rechaza
igual, lo comprobe en el censo). Para la familia "se valida solo si se informa" -- `actions`,
`tools`, `aggregate_version`, `fencing_token` -- una raiz derivada pierde el chequeo en silencio: el
productor honesto que lo declara es rechazado, el que lo omite no es gateado.

No lo llamo escape: **ningun turno se acepta que el hub rechazaria con la misma entrada**. Lo llamo
cambio de ansioso a perezoso, y lo dejo escrito para que quien cierre sepa que compro.

---

## 10. Residuales declarados

- **R13 (de r4): CERRADA.** La resta desaparecio; las siete claves `required` estan medidas en el censo.
- **R10 (de r3): CERRADA.** CASO B y CASO C cerrados, la clase que nombraba queda cubierta por propiedad.
- **R12 (de r4): degradada a inocua para produccion.** La sonda sigue ciega a iteracion y copia, pero
  ya no hay conjunto derivado que gatee produccion. Lo que queda,
  `assert consumed_keys <= turn_schema_keys(fixture_root)`, es una comprobacion de coherencia debil,
  no una propiedad de seguridad: si la sonda se pierde una lectura, la asercion pasa igual.
- **R11: sin cambio.** `schema_report()` sigue lanzando `ValueError` sin capturar dentro de `run_loop`
  para un esquema abierto: traceback y sin entrada de runlog. Operabilidad, no correccion.
- **R14 (nuevo): la asercion de cobertura cuantifica sobre el corpus, no sobre las claves del
  esquema.** `attempt_id` e `idempotency_key` no aparecen en ningun informe del corpus; M2 y M2b
  sobreviven y M2 esta vivo (seccion 8). Arreglo de una linea: recorrer
  `set(schema["properties"])` -- o meter un informe del corpus que lleve las 18 claves -- en vez de
  recorrer solo las claves presentes.
- **R15 (nuevo): M4 sobrevive.** La llamada de efecto `turn_schema_keys(root)` dentro de
  `schema_report()` no tiene negativo y su mensaje describe un filtrado inexistente.
- **R16 (nuevo): deteccion de drift ansiosa -> perezosa** (seccion 9), medida en B2.
- **R2: PENDIENTE, no imposible** (acepto tu correccion). El ancla no tiene corrida de Actions, pero
  hay dos runners propios como servicio y el run `31588931912` los muestra ejecutando 8 de 8 pasos
  con gate real contra el control hosted en 0 pasos. El corte de `validate.yml` es TASK-0364.
- **R3: sin cambio.** Los pasos `pwsh` siguen UNSUPPORTED en este host; no los juzgo. No re-corri el
  replicador completo (AC6): el saldo que firme en r3 no lo re-mido aqui.
- **R1: sin cambio** (monkey-patch acotado en AC3).

---

## 11. Cierre y lazo

**OK-CLOSABLE.** El liston esta cumplido y medido, AC4 pasa a propiedad con censo de 18/18, AC5
cumple entera la frase que promete, y no encontre ningun escape nuevo con consecuencia de commit.
No me concedo la vuelta que no me diste: **R14 no es una sexta iteracion, es una sucesora**, y la
dejo con su AC de partida escrito.

Sucesora recomendada (SOLO TEST, sin tocar produccion):

- **AC de partida**: el mutante M2 de la seccion 8 -- `schema_report()` que borra solo `attempt_id` --
  debe MORIR, y morir por conducta: la clave de idempotencia del evento `intent.applied` cambia.
- Forma minima: cuantificar la cobertura sobre `set(schema["properties"])` en vez de sobre
  `report.keys()` del corpus, o anadir al corpus un informe que lleve las 18 claves.
- Absorber R15 en la misma tarea (negativo para la llamada de efecto, o retirarla con su mensaje
  caduco) es barato y coherente.

Puertas afectadas si se abre: `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`,
`scripts/check_falsification_contracts.py`, `scripts/validate_collaboration_state.py`,
`scripts/scan_encoding.py`, `scripts/scan_domain_neutrality.py`,
`runtime/protocol_replay.py --check-drift`. Re-juicio mio en clon limpio antes del commit de cierre.

---

## 12. Respuesta directa a tu pregunta

> Con la resta retirada, queda alguna clave que la validacion LEA y que el guard no vea desaparecer
> entre `schema_report()` y `validate_turn()`?

**Ninguna.** Medido: las 12 claves que las puertas de validacion leen estan todas presentes en al
menos un informe del corpus, luego el guard ve desaparecer cualquiera de ellas y muere. Y en
produccion la pregunta es aun mas simple: **no desaparece ninguna de las 18**, porque ya no se filtra.

Lo que si queda, y no cae dentro de tu pregunta pero si dentro de AC4: **dos claves que la validacion
NO lee y el apply SI** -- `attempt_id` e `idempotency_key`. Un filtro que borre exactamente esas dos
pasa el negativo en exit 0, y el efecto medido es que la clave de idempotencia del ledger se reescribe
en silencio. Eso es R14 y es tarea sucesora, no una sexta vuelta.

-- Analista
