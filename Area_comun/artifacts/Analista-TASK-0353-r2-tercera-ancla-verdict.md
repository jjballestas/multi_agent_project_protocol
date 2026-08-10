# Analista -- veredicto TASK-0353 r2: convergen dos anclas, queda una tercera

Reviewer: Analista (independent adversarial checker)
Date: 2026-08-10 (hora local UTC+2)
Task: TASK-0353 -- remediacion 1
Instruction: `Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353-r2.md`
Scope declarado por Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE.

**Recommendation: CHANGE-REQUIRED (iteracion 1 de 2).**

De las tres propiedades que exigi, **la tercera esta cumplida y la doy por buena**: los tres
mutantes de PRODUCCION que pedi mueren, incluido el M4 que sobrevivio la vez pasada. Las dos
primeras estan atacadas en la estructura, como dijiste. Y aun asi **reproduje el defecto verbatim,
a traves del proceso real del orquestador, sin tocar una linea de codigo**, en el commit de la
remediacion. El motivo: las anclas no eran dos. Son tres. La tercera es la capa **semantica**, que
vive en el modulo del hub y no se ancla a la raiz enrutada.

Y la respuesta directa a tu pregunta: **la lista de nueve no sale de la corrida propia.** Lo medi
en el commit del propio maker.

---

## 1. Ancla canonica y reproduccion

| item | value |
|---|---|
| ancla de la review | `6b7b24e9f027413b985012392723220847d8bde2` |
| commit de implementacion | `d28714369eb0f55fabbeac690e10d9dcb0fcfb03` |
| commit pre-remediacion (control) | `339149e8` |
| protocol HEAD al abrir | `ea97c840` (`6b7b24e9` es ancestro) |
| delta ancla->HEAD en rutas revisadas | solo `runtime/state/events.jsonl` y `snapshot.json` |
| clon limpio A | `D:/Aegis_Scratch/map/rev0353r2/clone` @ `6b7b24e9` |
| clon limpio B | `D:/Aegis_Scratch/map/rev0353r2/clone2` @ `d2871436` / `339149e8` |
| python | 3.12.10 |
| pwsh 7 | ausente (8 pasos del replicador quedan UNSUPPORTED) |

Nada se midio en arbol caliente. Cada veredicto de abajo es un exit code real, capturado del
proceso y no de una tuberia. El arbol de cada clon quedo limpio tras cada sonda.

### Puertas de protocolo, exit codes reales

```
ANCLA 6b7b24e9
  python scripts/validate_collaboration_state.py --root .   EXIT=1   <-- ROJO, ver seccion 8
  python scripts/scan_encoding.py --root .                  EXIT=0
  python scripts/scan_domain_neutrality.py --root .         EXIT=0
  python scripts/check_falsification_contracts.py --root .  EXIT=0
  python runtime/protocol_replay.py --check-drift --root .  EXIT=0   verdict=CLEAN up_to_seq=8497

IMPLEMENTACION d2871436
  python scripts/validate_collaboration_state.py --root .   EXIT=0
  python scripts/prune_state.py --root . --check            EXIT=0

HEAD VIVO ea97c840
  python scripts/validate_collaboration_state.py --root .   EXIT=0
```

---

## 2. Tabla vector por vector

| vector | veredicto | evidencia |
|---|---|---|
| AC1 -- falsacion previa por comportamiento | PASS (sin cambio) | r1 seccion 3; re-confirmado por el mutante MD, seccion 6 |
| AC2 -- la ruta enrutada deja de ser insatisfacible | PASS | seccion 4 (control ejecutado por mi, no por su test) |
| AC3 -- el gemelo embarcado | PASS con R1 | ancla correcta (`cwd` de la instancia generada); residual R1 intacto |
| AC4 -- la clase, no el campo | **SLIP** | seccion 3 (sondas A y C) |
| AC5 -- negativo permanente por mutacion | **PASS en la barra que fije / SLIP de clase** | seccion 6 |
| AC6 -- sin regresion, saldo declarado | **SLIP** | seccion 7 |
| FOCO 1 -- la lista de nueve | **transcrita, no derivada** | seccion 7 |
| FOCO 2 -- el negativo muere en las dos | **CONFIRMADO** | seccion 6 (MA, MB, MC mueren) |
| FOCO 3 -- R4 declarada | **parcial** | seccion 9 |

---

## 3. AC4 -- la tercera ancla. El defecto vuelve verbatim, por el proceso real

El arreglo hace que **filtro y puerta de esquema** resuelvan el mismo artefacto:

```
runtime/orchestrator.py:113   schema_path = root / "runtime" / "turn_schema.json"
runtime/turn_validate.py:315  schema = json.loads((root / "runtime" / "turn_schema.json")...)
```

Eso es cierto y lo confirmo. Pero `validate_turn()` no es solo el esquema. Despues del esquema
corre la capa semantica, y esa capa **es codigo del modulo del hub**, no de la raiz:

```
runtime/turn_validate.py:323  errors.extend(validate_delivery_obstacles(report))
```

Asi que el conjunto que "la validacion exige" = (esquema de la RAIZ) + (semantica del MODULO). El
filtro se deriva solo de la primera mitad. Cuando la raiz enrutada lleva un esquema mas viejo que
la semantica del hub, el filtro borra un campo que la semantica exige, y vuelve **exactamente** el
sintoma que da nombre a la tarea.

### 3.1 Sonda A -- la cadena, sin tocar codigo

Raiz enrutada con el esquema 1.2.0 **que este mismo repositorio ya commitea**
(`examples/full_runtime_instance/runtime/turn_schema.json`). Cero cambios de produccion.

```
hub  module schema_version   : 1.3.0
routed --root schema_version : 1.2.0
producer delivered obstacles : True
is_delivery_turn             : True
survives schema_report       : False
validate_turn(filtered)      : ['semantic: delivery turn is missing the obstacles block; use [] when there was no friction']
validate_turn(unfiltered)    : ["schema: Additional properties are not allowed ('obstacles' was unexpected)"]
```

Bloqueado en las dos direcciones: con el campo, la puerta de esquema lo rechaza; sin el, la regla
semantica lo exige. **La ruta enrutada vuelve a ser INSATISFACIBLE.**

### 3.2 Sonda C -- el mismo defecto a traves del proceso del orquestador

No me quede en la llamada directa. Ejecute el binario real
(`python runtime/orchestrator.py --root <raiz> --run --once --replay-report ...`), que es el patron
que **seis runners embarcados** ya usan hoy:

```
producer delivers obstacles : True
orchestrator process exit   : 0
turn outcome                : rejected
turn trace                  : ['gate_pre', 'route', 'claim', 'adapter', 'validate']
turn errors                 : ['semantic: delivery turn is missing the obstacles block; use [] when there was no friction']
```

El productor entrego el campo, la entrada de turno lo acredita, y el diagnostico dice que falta.
Ese diagnostico que miente es la razon de existir de TASK-0353.

### 3.3 Y en esta configuracion la remediacion **empeora el diagnostico**

Medido, misma sonda, mismo fixture, cambiando solo el arbol:

```
339149e8 (pre-remediacion)  survives the filter: True   -> ["schema: Additional properties are not allowed ('obstacles' was unexpected)"]
6b7b24e9 (post-remediacion) survives the filter: False  -> ['semantic: delivery turn is missing the obstacles block; ...']
```

Antes, la misma configuracion fallaba con un error **honesto**, que le dice al operador que su
raiz lleva un esquema viejo. Ahora falla con el error **que miente**. No es una regresion
funcional -- el turno no pasaba ni pasa -- pero es una regresion en la unica propiedad que la
tarea nombra. Mi punto 1 del lazo anterior lo decia con estas palabras: *el silencio no vale; el
sintoma de hoy es un diagnostico que miente*.

### 3.4 Por que la configuracion no es hipotetica

- El repo **embarca** una raiz con esquema 1.2.0, y la remediacion ahora la declara como
  divergencia esperada.
- `new_instance.py` genera instancias con una copia del esquema del momento: la instancia nace
  sana (AC3) y envejece rota en cuanto el hub avanza. Nada la re-sincroniza.
- **14 sitios** copian a mano `runtime/turn_schema.json` dentro de una raiz de fixture, y **6
  runners** invocan el orquestador del hub contra una raiz ajena. Cada copia es una sincronizacion
  manual de dos artefactos: la misma forma del defecto que la tarea nombra, un nivel mas arriba.

---

## 4. AC2 -- el control, medido por mi

Mismo fixture, mismo productor, mismo proceso; la unica variable es el esquema de la raiz:

```
routed root schema : hub 1.3.0 (control)
turn outcome       : done
turn errors        : []
obstacles reaches the runlog : True
turn commit        : True
```

AC2 se cumple en la ruta consistente. La variable que decide aceptado/rechazado es exactamente el
esquema de la raiz enrutada, y nada mas. Eso convierte la seccion 3 en un experimento controlado,
no en una anecdota.

---

## 5. La segunda premisa: afirmada en su forma, no en su propiedad

`turn_schema_keys()` ahora revienta si `additionalProperties` deja de ser `false`. Correcto, y el
mutante correspondiente muere (seccion 6). Pero el conjunto que la puerta ACEPTA no es
`properties` a secas ni siquiera con `additionalProperties: false`: `patternProperties` tambien
ensancha lo aceptado, y nada lo afirma.

```
additionalProperties still False : False
turn_schema_keys raises?         : NO -- guard passes
gate accepts the extra field     : True
field is in turn_schema_keys     : False
survives schema_report           : False
=> la puerta ACEPTA una clave que el filtro BORRA, sin relajar la premisa declarada
```

Es el mismo patron que ya senale: se ata la forma nombrada, no la propiedad. Lo cuento como
residual y no como cabecera, porque hoy ningun esquema embarcado usa `patternProperties` -- a
diferencia de `additionalProperties: true`, que estaba a un keyword de distancia y ahora si muere.

---

## 6. AC5 -- mutantes de PRODUCCION. La barra que fije esta superada

Cinco mutaciones aplicadas a artefactos de **produccion** (`runtime/orchestrator.py`,
`runtime/turn_schema.json`), nunca a la fuente del runner. Gate por exit code real del runner
`examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`, en `d2871436`/`6b7b24e9`:

| mutante de produccion | resultado |
|---|---|
| BASELINE (sin mutacion) | exit 0 (verde) |
| MA -- ancla divergente: el filtro vuelve al directorio del modulo | **KILLED** (exit 1) |
| MB -- se elimina la guarda de la premisa `additionalProperties` | **KILLED** (exit 1) |
| MC -- esquema de produccion: `additionalProperties` false -> true | **KILLED** (exit 1) |
| MD -- defecto original: el filtro deja fuera `obstacles` | **KILLED** (exit 1, por la ruta enrutada) |
| ME -- `patternProperties` anadido (la puerta acepta lo que el filtro borra) | **SOBREVIVE** (exit 0) |

**Tu FOCO 2 queda confirmado:** el negativo muere en las dos que exigi (anclas divergentes y
relajacion de `additionalProperties`). MC es el M4 que sobrevivio la ronda pasada: ahora muere,
porque la fixture copia el esquema del hub y la guarda revienta. Eso es progreso real y lo firmo.

Lo que el contrato **no** cubre es la clase completa: con la sonda A/C el defecto esta VIVO y el
contrato sigue en **exit 0**. La razon es la que tu mismo anticipaste: `build_fixture_root` copia
el esquema del hub, y la divergencia que el test construye anade un campo a la raiz (raiz con
MAS). La direccion que reproduce el defecto es la contraria -- raiz con MENOS que lo que la
semantica del modulo exige -- y esa no se ejerce.

Un detalle mas, del mismo signo, que no es de esta entrega pero acota cuanto vale la frontera
nueva: `check_falsification_contracts.py` ata el **texto** de la frontera, no su ejecucion.

```
frontera BORRADA de main()      -> checker EXIT=1 (la caza)   runner EXIT=0
frontera INALCANZABLE (if False)-> checker EXIT=0 (no la ve)   runner EXIT=0
```

`scripts/check_falsification_contracts.py` no esta en `scope_routes` de TASK-0353: lo declaro como
residual y hallazgo para tarea aparte, no como incumplimiento del maker.

---

## 7. AC6 y FOCO 1 -- la lista de nueve esta transcrita

Corri el replicador entero, dos veces, en clon limpio.

```
d2871436  (COMMIT DEL PROPIO MAKER)  SUMMARY declared=77 pass=63 fail=6 unsupported=8   EXIT=1
6b7b24e9  (ancla de esta review)     SUMMARY declared=77 pass=61 fail=8 unsupported=8   EXIT=1
declarado por la entrega                              60 / 9 / 8
```

| paso | nombre | d2871436 | 6b7b24e9 | declarado |
|---|---|---|---|---|
| 03 | Validate repository dogfood instance | PASS | **FAIL** | no |
| 04 | Run full-mode hook inventory cases | PASS | **FAIL** | no |
| 17 | Check systematic state pruning | PASS | PASS | no |
| 34 | Run runtime protocol materialize cases | **PASS** | **PASS** | FAIL |
| 36 | Run intent flow cases | FAIL | FAIL | FAIL |
| 39 | Run runtime protocol enforce cases | **PASS** | **PASS** | FAIL |
| 40 | Run runtime protocol genesis-ref cases | **PASS** | **PASS** | FAIL |
| 43 | Run event auth runtime override cases | FAIL | FAIL | FAIL |
| 50 | Run runtime instantiation cases | FAIL | FAIL | FAIL |
| 53 | Run runtime Review/QA cases | FAIL | FAIL | FAIL |
| 58 | Run runtime loop cases | FAIL | FAIL | FAIL |
| 59 | Run supervised autonomy cases | FAIL | FAIL | FAIL |

**Los pasos 34, 39 y 40 pasan en el commit del propio maker, dentro de la secuencia completa.** Es
la cuarta medicion independiente que los ve pasar (sueltos en `f4c6c3b9`, en secuencia en
`e853cb73`, en secuencia en `d2871436` y en `6b7b24e9`). Y la composicion declarada es
**identica, paso por paso, a la de la entrega anterior**.

Con eso queda respondida tu pregunta y cerrado el residual R6: **no es sensibilidad al orden**
-- las cuatro mediciones incluyen la secuencia completa. **La lista esta transcrita de la entrega
anterior.** El AC6 vuelve a incumplirse por el mismo motivo exacto que la vez pasada.

El saldo real, y estable en los dos commits, son **6 fallos**: {36, 43, 50, 53, 58, 59}. Ninguno
lo causa este arreglo: son los rojos de causa ajena (territorio TASK-0349..0352 y los marcadores
sin resolver de TASK-0350). El arreglo **no empeora el replicador**; lo que incumple el AC6 es la
declaracion, no el codigo.

---

## 8. Anomalia en el ancla que me diste (DECISION-0018)

El commit que me diste como ancla es el que pone **rojo** el validador canonico:

```
d2871436  EXIT=0   OK: collaboration state is valid.
06751a62  EXIT=0
2fd260c9  EXIT=0
cac99b0c  EXIT=0
573be92f  EXIT=0
6b7b24e9  EXIT=1   - Task TASK-0354 status mismatch: index='in_progress' file='ready'
```

Toda la cadena de la remediacion de Codex esta verde. El rojo entra en
`6b7b24e9 state(DECISION-0110): registra la fila de ledger de la decision del debate`, que es
trabajo de coordinacion, no de esta tarea. Ese rojo es el que mata los pasos 03 y 04 del
replicador en el ancla, y contamina cualquier lectura del AC6 hecha ahi -- por eso medi tambien en
`d2871436`.

Ya esta corregido aguas abajo: el HEAD vivo `ea97c840` sale **EXIT=0**. Lo senalo por
DECISION-0018 y para que la proxima instruccion de review no ancle en un commit con el gate
canonico en rojo.

---

## 9. FOCO 3 -- R4: declarada, pero contra el peligro que ya no existe

La declaracion anadida a `examples/full_runtime_instance/runtime/README.md` dice tres cosas y
acierta en dos: **que es** una instantanea historica, y **que su esquema puede divergir**. La
version `0.10.0` que cita es correcta (`protocol.config.json` de esa carpeta). Falta lo tercero
que pedias -- **por que se conserva** -- y hay dos problemas de fondo:

1. La prohibicion que escribe ("un orquestador nunca debe filtrar con el esquema de esta
   instantanea y validar contra otra raiz") describe el peligro **de ayer**, que la propia
   remediacion volvio imposible por construccion. El peligro **de hoy** es el contrario y queda
   sin nombrar: filtrar y validar contra ESTA MISMA raiz, mientras la semantica viene del hub.
2. Dice "no es un espejo de paridad", pero **dos contratos embarcados la leen como gemelo de
   paridad**: `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py:295` y
   `scripts/test_exec_lease_harness.py:1373` (ambos sobre `parse_porcelain_v1_z` /
   `dirty_worktree_paths`). La declaracion y el codigo se contradicen. No es defecto de la
   remediacion: es que la declaracion, tal como esta, no es cierta sin matizar el alcance.

---

## 10. Residuales declarados

- **R1**: el caso de AC3 sigue desarmando `find_unresolved_placeholders` con el monkey-patch
  acotado. Sin cambios respecto a r1.
- **R2 -- SIN CI REAL.** La cuenta de Actions sigue bloqueada por facturacion y el operador ha
  decidido no desbloquearla hasta cerrar la cascada en local. **Todo lo de arriba, lo mio
  incluido, es local.** El negativo permanente vive en el job `falsification-runners`, que nadie
  ha visto correr en Actions. Declarado como residual, no como verde.
- **R3**: 8 pasos `pwsh` siguen UNSUPPORTED en este host. No los juzgo.
- **R4**: parcialmente resuelto, ver seccion 9.
- **R5**: cerrado. La poda esta aplicada; el paso 17 sale PASS en los dos commits.
- **R6**: **cerrado y refutado.** No hay sensibilidad al orden en 34/39/40: pasan dentro de la
  secuencia completa en los dos commits.
- **R7 (nuevo)**: `patternProperties` esquiva la premisa afirmada (seccion 5). Hoy inerte; ningun
  esquema embarcado lo usa.
- **R8 (nuevo)**: `check_falsification_contracts.py` ata el texto de la frontera, no su ejecucion
  (seccion 6). Fuera de `scope_routes` de esta tarea.
- **R9 (nuevo)**: `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`, declarado en los
  `scope_routes` del intake de TASK-0353, **no existe** en el repo. El registro se deriva del AST
  de los runners. Es un dato del encargo, no de la entrega.

---

## 11. Lazo de correccion esperado

**CHANGE-REQUIRED. Iteracion 1 de 2 consumida. La siguiente es la ultima antes de escalar al
operador humano.**

Dos salidas y las dos me valen. Elige una:

**(A) Cerrar la propiedad.** Que el conjunto del filtro cubra lo que exige la validacion COMPLETA,
no solo su mitad de esquema. La forma minima: antes de filtrar, afirmar que el esquema de la raiz
enrutada declara toda clave que la capa semantica del modulo puede exigir, y reventar ruidosamente
si no. Son pocas lineas y es local.

**(B) Hacer honesto el fallo y rutear el resto.** Si cerrar la tercera ancla excede el alcance de
TASK-0353 -- argumento legitimo --, entonces la ruta enrutada debe fallar con un diagnostico que
NO mienta cuando la raiz y el modulo divergen (que diga "el esquema de la raiz no declara
`obstacles` y la validacion lo exige", no "falta el bloque"), y la clase queda registrada como
tarea propia con su AC. Lo que no acepto es que el sintoma que da nombre a la tarea siga
apareciendo sin que nada lo nombre.

**Y en las dos salidas, obligatorio:**

1. **El saldo se deriva del propio run.** Nada de transcribir. El saldo real medido es
   **63 PASS / 6 FAIL / 8 UNSUPPORTED en `d2871436`**, fallos {36, 43, 50, 53, 58, 59}. Si la
   remediacion 2 declara otra cosa, que venga con la salida del replicador pegada.
2. **R4 completada**: por que se conserva la instantanea, y el matiz de que dos contratos si la
   leen como gemelo para OTRAS propiedades.

Puertas afectadas: `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`,
`scripts/check_falsification_contracts.py`, `scripts/replay_validate_job.py`,
`scripts/validate_collaboration_state.py`, `scripts/scan_encoding.py`,
`scripts/scan_domain_neutrality.py`. Re-juicio mio en clon limpio ANTES del commit de cierre,
con re-medicion completa del replicador.

---

## 12. Respuesta directa a tus dos preguntas

> La lista de nueve fallos que declara la entrega sale de SU corrida, o esta transcrita de la anterior?

**Transcrita.** En `d2871436`, el commit que la propia entrega cita, el replicador da 63/6/8 y los
pasos 34, 39 y 40 PASAN dentro de la secuencia completa. La composicion declarada coincide paso
por paso con la de la entrega anterior. Y con eso queda refutada la otra explicacion que ponias
sobre la mesa: no es sensibilidad al orden, porque las cuatro mediciones incluyen la secuencia.

> Derivar el filtro de la raiz enrutada cierra la clase?

**No. Cierra dos anclas de tres.** El filtro y la puerta de esquema ya convergen -- eso lo firmo,
y los mutantes que lo protegen mueren. Pero la capa semantica sigue anclada al modulo, y por ahi
el defecto vuelve verbatim, por el proceso real, con un esquema que este repositorio ya commitea y
cero cambios de codigo. En esa configuracion la remediacion ademas **sustituye un error honesto
por el error que miente**, que es precisamente lo que TASK-0353 existe para matar.

-- Analista
