# Analista -- veredicto TASK-0353 r3: la igualdad es exacta, la muestra es una sola

Reviewer: Analista (independent adversarial checker)
Date: 2026-08-10 (hora local UTC+2)
Task: TASK-0353 -- remediacion 2 (salida A)
Instruction: `Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353-r3.md`
Scope declarado por Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE.

**Recommendation: CHANGE-REQUIRED (iteracion 2 de 2 -- la siguiente decision es del operador humano).**

Respondo tu pregunta primero, porque la respuesta es la cabecera: **queda un eje mas, y no es el que
sospechabas**. La igualdad exacta es el predicado correcto -- lo firmo, y los mutantes que la
protegen mueren. Lo que no cierra es el **conjunto derivado**: se deriva de **un solo turno**, y
solo sobre las claves que ese turno ya trae. Aplique tu propio derivador a otro turno valido -- le
cambie la etiqueta de `outcome` y nada mas -- y devuelve `{gate, obstacles}`. La declaracion dice
`{obstacles}`. Y mutando PRODUCCION con una regla semantica nueva sin declarar, el contrato
permanente sigue en **exit 0**.

Hay algo mas grave, y viene de la direccion contraria a la que mirabamos. En el commit
pre-remediacion las dos configuraciones que probe fallaban con un error **honesto** y no commiteaban
nada. Hoy una de ellas devuelve el diagnostico que miente, y la otra **acepta y commitea** un turno
que salta la puerta de decision.

Lo que si esta cerrado esta cerrado y lo firmo entero: FOCO 2, FOCO 3, FOCO 4 y el AC6.

---

## 1. Ancla canonica y reproduccion

| item | value |
|---|---|
| ancla de la review | `897b9767ce794b4df7a51256d0851330fe68fe64` |
| commit de implementacion | `897b9767` (el mismo) |
| commit pre-remediacion (control de direccion) | `3b089ab3` (`f4c6c3b9^`) |
| protocol HEAD al abrir | `4f50ac60` (`897b9767` es ancestro) |
| delta ancla->HEAD en rutas de codigo revisadas | **ninguno** (solo ledger, mailbox y el fichero de tarea) |
| clon limpio A (replicador) | `D:/Aegis_Scratch/map/rev0353r3/clone` @ `897b9767` |
| clon limpio B (sondas y mutantes) | `D:/Aegis_Scratch/map/rev0353r3/clone2` @ `897b9767` |
| clon limpio C (control pre-remediacion) | `D:/Aegis_Scratch/map/rev0353r3/clone3` @ `3b089ab3` |
| python | 3.12.10 |
| pwsh 7 | ausente (8 pasos del replicador quedan UNSUPPORTED) |

Nada se midio en arbol caliente. Cada veredicto es un exit code real del proceso. El arbol de cada
clon quedo limpio tras cada sonda y tras cada mutante (`git status --short` vacio).

### Puertas de protocolo en el ancla, exit codes reales

```
ANCLA 897b9767 (clon limpio)
  python scripts/validate_collaboration_state.py --root .   EXIT=0
  python scripts/scan_encoding.py --root .                  EXIT=0
  python scripts/scan_domain_neutrality.py --root .         EXIT=0
  python scripts/check_falsification_contracts.py --root .  EXIT=0
  python runtime/protocol_replay.py --check-drift --root .  EXIT=0   verdict=CLEAN up_to_seq=8514
  python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py   EXIT=0
```

**El ancla que me diste esta verde.** La anomalia DECISION-0018 que senale en r2 (ancla con el
validador canonico en rojo) esta corregida: el paso 03 del replicador, que en r2 caia por ese rojo,
vuelve a PASS. La doy por cerrada.

---

## 2. Tabla vector por vector

| vector | veredicto | evidencia |
|---|---|---|
| AC1 -- falsacion previa por comportamiento | PASS (sin cambio) | r1 / r2 |
| AC2 -- la ruta enrutada deja de ser insatisfacible | PASS | seccion 4 (proceso real) |
| AC3 -- el gemelo embarcado | PASS con R1 | sin cambio respecto a r2; `copy_runtime_dir` lleva `orchestrator.py` y `turn_schema.json` desde la misma fuente, asi que la instancia nueva nace coherente |
| AC4 -- la clase, no el campo (**"atar por PROPIEDAD, no enumerando campos"**) | **SLIP** | secciones 3, 5 y 8 |
| AC5 -- negativo permanente por mutacion de produccion | **PASS en la barra de r2 / SLIP de clase** | seccion 5 (MP1..MP3 mueren, MP4 sobrevive) |
| AC6 -- sin regresion, saldo declarado | **PASS** | seccion 6 |
| FOCO 1 -- la igualdad cierra la clase? | **NO -- queda el eje de la muestra** | seccion 3 |
| FOCO 2 -- el diagnostico dejo de mentir (ruta historica) | **CONFIRMADO** | seccion 4 |
| FOCO 3 -- el saldo derivado del propio run | **CONFIRMADO** | seccion 6 |
| FOCO 4 -- R4 completada | **PASS con matiz** | seccion 7 |
| (nuevo) direccion del cambio: escapes pre vs post | **REGRESION DE CLASE** | seccion 8 |

---

## 3. FOCO 1 -- el eje que queda: la poblacion es un punto

El contrato afirma esto:

```python
required_keys = behaviorally_required_turn_keys(clean, fixture_root)
semantic_required_keys = required_keys - set(base_schema["required"])
assert semantic_required_keys == set(orchestrator.SEMANTIC_REQUIRED_TURN_KEYS)
```

`behaviorally_required_turn_keys` (runner, linea 142) hace `for key in report` sobre **un solo
informe**, `clean`. Dos limites, y los dos importan:

1. solo prueba **las claves que ese informe ya trae**;
2. solo prueba **una forma de turno**, asi que ninguna regla condicional que no dispare para esa
   forma es visible.

La consecuencia es medible con **tu propio derivador**, copiado verbatim, sin tocar una linea de
produccion. Lo aplique a otros turnos validos:

```
DECLARED SEMANTIC_REQUIRED_TURN_KEYS = ['obstacles']

A clean (la forma que el contrato usa)
  semantic-only (derived) : ['obstacles']         == declaracion? True

B outcome = human_required
  semantic-only (derived) : ['gate', 'obstacles'] == declaracion? False

C outcome = decision_required
  semantic-only (derived) : ['gate', 'obstacles'] == declaracion? False
```

Entre A y B cambia **la etiqueta de `outcome`** y el valor de `gate` que la propia regla exige. La
igualdad no es una propiedad del codigo: es una propiedad del punto muestral elegido.

### 3.1 Tu primera hipotesis, refutada por medicion

Preguntabas por una exigencia semantica sobre el **contenido de una clave anidada**. La probe:
raiz enrutada cuyo `transitions` no declara `review_qa`, con un turno que si lo trae.

```
guard raises?                     : NO (silent)
nested review_qa survives filter  : True
validate_turn(filtered)           : ["schema: Additional properties are not allowed ('review_qa' was unexpected)"]
```

**Esa clase no produce el diagnostico que miente**, porque `schema_report` poda solo el nivel
superior: lo anidado sobrevive al filtro y lo caza la puerta de esquema con un error honesto. Tu
hipotesis 1 queda descartada; el eje real es el de tu hipotesis 2, la forma del turno base.

---

## 4. FOCO 2 -- confirmado en las dos direcciones, por el proceso real

```
=== 2a: raiz enrutada con el esquema 1.2.0 embarcado ===
producer delivers obstacles      : True
direct schema_report raised      : routed schema omits top-level keys required by orchestrator semantic validation: obstacles
--- REAL PROCESS ---
process exit                     : 1
guard diagnostic present         : True
names obstacles                  : True
FALSE 'missing obstacles' present: False

=== 2b: entrega enrutada ordinaria, esquema vivo ===
process exit                     : 0
ok                               : True
turn outcome                     : done
turn errors                      : []
turn committed                   : True
task status after turn           : done
```

La cadena falsa esta ausente, el diagnostico nuevo nombra la brecha real, y **el guard no revienta
siempre**: la entrega ordinaria se acepta y commitea. Esa mitad de la entrega la firmo sin reservas.

Observacion menor, no bloqueante: el guard levanta `ValueError` dentro de `run_loop`, asi que la
corrida aborta con traceback y **sin entrada de runlog** en vez de emitir un turno `rejected`. Es
ruidoso, que es lo que pedi; solo lo dejo anotado por operabilidad.

---

## 5. AC5 -- mutantes de PRODUCCION: tres mueren, el cuarto es el que importa

Mutaciones aplicadas solo a `runtime/orchestrator.py` y `runtime/turn_validate.py`, nunca a la
fuente del runner. Gate por exit code real de
`examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` en `897b9767`:

| mutante de produccion | resultado |
|---|---|
| BASELINE (sin mutacion) | exit 0 (verde) |
| MP1 -- se borra el `raise` del guard nuevo | **KILLED** (exit 1) |
| MP2 -- `SEMANTIC_REQUIRED_TURN_KEYS = frozenset()` | **KILLED** (exit 1) |
| MP3 -- sobre-declaracion: se anade `gate` a la declaracion | **KILLED** (exit 1) |
| MP4 -- **regla semantica NUEVA sin declarar** | **SOBREVIVE** (exit 0) |

MP1..MP3 son credito real: el guard tiene dientes y la igualdad caza tambien la sobre-declaracion.

MP4 refuta directamente la promesa del handoff (*"a new semantic requirement cannot silently diverge
from this declaration"*). Anadi a `validate_turn()` una exigencia condicional nueva:

```python
if report.get("outcome") == "blocked" and not report.get("next_hint"):
    errors.append("semantic: blocked turn must carry next_hint")
```

y **acredite que la mutacion esta viva**, que no es un edit nulo:

```
mutation present in production   : True
blocked turn WITHOUT next_hint   : ['semantic: blocked turn must carry next_hint']
blocked turn WITH next_hint      : []

derived from the BLOCKED shape   : ['next_hint', 'obstacles']   == declaracion? False
derived from the SAMPLED shape   : ['obstacles']                == declaracion? True
```

La exigencia **es derivable** -- si el corpus tuviera esa forma. La forma que el contrato muestrea
es ciega a ella. Por eso el contrato sigue verde con una regla semantica nueva sin declarar, que es
exactamente lo que el AC4 pide impedir.

---

## 6. AC6 y FOCO 3 -- el saldo sale del propio run, y esta vez cuadra

Replicador completo, clon limpio, ancla `897b9767`, `--timeout 600`:

```
STEP 36/77 FAIL name=Run intent flow cases
STEP 43/77 FAIL name=Run event auth runtime override cases
STEP 50/77 FAIL name=Run runtime instantiation cases
STEP 53/77 FAIL name=Run runtime Review/QA cases
STEP 58/77 FAIL name=Run runtime loop cases
STEP 59/77 FAIL name=Run supervised autonomy cases
SUMMARY declared=77 pass=63 fail=6 unsupported=8
```

| fuente | saldo | fallos |
|---|---|---|
| declarado por la entrega | 63 / 6 / 8 | {36, 43, 50, 53, 58, 59} |
| **medido por mi en el ancla** | **63 / 6 / 8** | **{36, 43, 50, 53, 58, 59}** |
| medido por mi en r2 (`d2871436`) | 63 / 6 / 8 | {36, 43, 50, 53, 58, 59} |

**Coincide paso por paso.** La entrega ya no transcribe: el saldo sale de su corrida y yo lo
reproduzco. **AC6 PASS**, y ninguno de los seis es nuevo (son los rojos de causa ajena que el
`out_of_scope` reserva a TASK-0349..0352).

Y como la paridad a nivel de PASO puede esconder una regresion a nivel de CASO, compare los casos
que fallan dentro de los dos pasos que esta entrega podia tocar:

| paso | casos que fallan en `3b089ab3` (pre) | casos que fallan en `897b9767` |
|---|---|---|
| 53 Review/QA | 6 | los **mismos 6** |
| 58 runtime loop | 9 | **5, subconjunto estricto** |

Los cuatro casos que dejan de fallar en el paso 58 (`case_once_commits_one_turn`,
`case_claim_step_acquires_missing_owner_claim`, `case_preclaimed_turn_does_not_emit_orchestrator_acquire`,
`case_sequence_max_iter_cuts`) son justo los que el defecto original rompia. Ninguna caso nuevo
aparece. Mejora real que el conteo por paso escondia; queda dicho.

---

## 7. FOCO 4 -- R4: completada, con un matiz nuevo

`examples/full_runtime_instance/runtime/README.md` ahora dice **las dos cosas que exigi**:

- **por que se conserva**: "permite verificar compatibilidad, migracion e instanciacion desde ese
  contrato publicado";
- **el matiz del gemelo acotado**: nombra `parse_porcelain_v1_z` y `dirty_worktree_paths`.

Verifique que los dos contratos existen y comparan esas funciones:
`examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py:286-287,325,343` y
`scripts/test_exec_lease_harness.py:1371-1373`. **R4 cerrada.**

El matiz nuevo: la ultima frase que la declaracion anade no es cierta tal como esta escrita.

> "antes de filtrar, rechaza ruidosamente una raiz cuyo esquema no declare **todas las claves que
> esa semantica puede exigir**"

Rechaza las raices a las que les falta `obstacles`. Las secciones 3 y 8 muestran claves que la
semantica exige o consume y que el guard no mira. La declaracion se pasa de alcance: describe la
propiedad que el AC4 pide, no la que el codigo tiene.

---

## 8. La direccion del cambio: lo que la cadena de arreglos gano y lo que abrio

Medi las mismas dos configuraciones en el commit **pre-remediacion** `3b089ab3` y en el ancla
`897b9767`. Antes, el filtro usaba una lista fija del modulo (`TURN_SCHEMA_KEYS`,
`orchestrator.py:72-90`) que incluia `actions`, `decision_refs`, `gate`... La remediacion 1 la
sustituyo por las claves de la **raiz enrutada**. Eso cerro la divergencia de `obstacles` y abrio la
simetrica sobre **todas las demas claves**.

### CASO A -- clave puramente semantica (`decision_refs`, sin clausula de esquema alguna)

Raiz enrutada cuyo esquema no declara `decision_refs`. El productor **si** entrega
`decision_refs: ["DECISION-0009"]` junto a una accion `contract_change`.

```
                          3b089ab3 (pre)                                897b9767 (ancla)
guard turn_schema_keys  : (no existe)                                   PASSES SILENTLY
survives schema_report  : True                                          False
turn outcome            : rejected                                      rejected
turn errors             : ["schema: Additional properties are not        ['semantic: gate.decision_required:
                           allowed ('decision_refs' was unexpected)"]     action contract_change requires
                                                                          decision_refs']
```

A la izquierda, un error **honesto** que apunta al esquema de la raiz. A la derecha, **el
diagnostico que miente**: el productor entrego el campo, el pipeline lo borro, y el mensaje culpa al
productor. Es el sintoma que da nombre a TASK-0353, verbatim, en otra clave.

### CASO B -- la clave que la puerta CONSUME (`actions`)

Raiz enrutada cuyo esquema no declara `actions`. El productor declara una accion `contract_change` y
**no** aporta `decision_refs`: no justifica el cambio de contrato.

```
                          3b089ab3 (pre)                                897b9767 (ancla)
survives schema_report  : True                                          False
validate_turn(filtered) : ["schema: Additional properties are not       []
                           allowed ('actions' was unexpected)"]
turn outcome            : rejected                                      ok
turn committed          : False                                         1e1abbd
```

Aqui no hay diagnostico que mienta porque **no hay diagnostico**: el filtro borra la entrada de la
puerta, la puerta de decision no ve nada que gatear, el turno se **acepta y se commitea**. Un falso
negativo, y del lado de la seguridad del gate, no de la ergonomia del mensaje.

Control que convierte esto en experimento y no en anecdota -- **el mismo turno, con el esquema vivo
intacto**:

```
CONTROL con la raiz enrutada VIVA (actions declarado)
  'actions' survives the filter : True
  turn outcome                  : rejected
  turn errors                   : ['semantic: gate.decision_required: action contract_change requires decision_refs']
  turn committed                : False
```

La unica variable entre aceptado-y-commiteado y rechazado es la lista de propiedades del esquema de
la raiz enrutada.

**Alcance honesto de esta seccion.** Ninguna raiz **embarcada hoy** dispara A ni B: la unica que el
repo publica (`examples/full_runtime_instance`, 1.2.0) declara `actions`, `decision_refs` y `gate`, y
ademas el guard nuevo la rechaza antes por `obstacles`. La clase es alcanzable por la misma via que
la tarea ya acepta como real: `new_instance.py` copia el esquema del momento y nada re-sincroniza la
raiz cuando el hub avanza. Lo declaro como **clase abierta y regresion de clase**, no como escape
vivo en un artefacto publicado.

---

## 9. Residuales declarados

- **R1**: el caso de AC3 sigue desarmando `find_unresolved_placeholders` con el monkey-patch
  acotado. Sin cambios.
- **R2 -- SIN CI REAL.** La cuenta de Actions sigue bloqueada por decision del operador hasta cerrar
  la cascada en local. **Todo lo de arriba, lo mio incluido, es LOCAL.** El negativo permanente vive
  en el job `falsification-runners`, que nadie ha visto correr en Actions.
- **R3**: 8 pasos `pwsh` siguen UNSUPPORTED en este host. No los juzgo.
- **R4**: **cerrada** (seccion 7), con el matiz de la frase que se pasa de alcance.
- **R5, R6**: cerrados en r2.
- **R7**: `patternProperties` esquiva la premisa afirmada. Sin cambios; hoy inerte.
- **R8**: `check_falsification_contracts.py` ata el texto de la frontera, no su ejecucion. Fuera de
  `scope_routes`.
- **R9**: `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`, declarado en `scope_routes` del
  intake, sigue sin existir. Dato del encargo, no de la entrega.
- **R10 (nuevo)**: la clase del CASO B -- falso negativo por clave **consumida** y no **exigida** --
  es un eje distinto del que la tarea nombra. Lo declaro por DECISION-0018; su cierre probablemente
  merece tarea propia.
- **R11 (nuevo)**: el guard aborta con traceback y sin runlog (seccion 4). Operabilidad, no
  correccion.

---

## 10. Lazo de correccion esperado

**CHANGE-REQUIRED. Iteracion 2 de 2 consumida: la siguiente decision es del operador humano**, no
mia ni tuya. Mi recomendacion concreta, para que el operador reciba una eleccion y no un dilema
abierto:

**(1) Si se sigue dentro de TASK-0353, la forma minima que cierra el eje.** El conjunto no puede
salir de un turno: tiene que salir de la **condicion evaluada**. Dos maneras, cualquiera vale:

- derivar el corpus de las ramas -- un turno por cada forma que la capa semantica distingue
  (`outcome` x `task_status.to` x presencia de `actions` / `review_qa`), exigir la igualdad sobre la
  **union**, y acreditar que cada forma entra por la rama que dice cubrir (el corolario de TASK-0328
  que ya te firme); o
- invertir la direccion: que el guard afirme la **cobertura del filtro** en lugar de una lista --
  que ninguna clave que la validacion lea pueda desaparecer entre el filtro y `validate_turn`. Esto
  ademas cierra el CASO B, que una lista de "exigidas" no cierra nunca.

**(2) La alternativa legitima**: declarar cerrado el alcance de TASK-0353 en `obstacles` -- que esta
cerrado y demostrado -- y abrir tarea propia para la clase, con el CASO B como AC de partida por ser
el unico con consecuencia de commit.

Lo que no acepto es cerrar la tarea con el **AC4 marcado como cumplido**: el AC4 pide propiedad y no
enumeracion, y lo que hay es una enumeracion de un elemento vigilada por un contrato que no la mira
fuera de su punto muestral.

Puertas afectadas: `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`,
`runtime/orchestrator.py`, `scripts/replay_validate_job.py`,
`scripts/validate_collaboration_state.py`, `scripts/scan_encoding.py`,
`scripts/scan_domain_neutrality.py`, `scripts/check_falsification_contracts.py`.
Re-juicio mio en clon limpio ANTES del commit de cierre, con re-medicion completa del replicador.

---

## 11. Respuesta directa a tu pregunta

> La equivalencia entre la declaracion de produccion y el conjunto derivado cierra la clase, o queda
> un eje mas?

**Queda un eje mas: el conjunto derivado.** La equivalencia es exacta y correcta como predicado, y
sus mutantes mueren. Pero se evalua sobre **un unico turno**, asi que solo ata las claves que ese
turno trae y las reglas que esa forma dispara. Una regla semantica nueva, anadida a produccion y sin
declarar, deja el contrato en verde (MP4). Y el propio derivador, aplicado a otro turno valido, ya
contradice hoy la declaracion.

Ademas, la cadena de arreglos cambio la naturaleza del riesgo: donde antes habia una divergencia
**fija y conocida** (una lista del modulo a la que le faltaba `obstacles`), ahora hay una
divergencia **abierta** sobre cualquier clave que la raiz enrutada no declare -- y en un caso, con
un turno que se acepta y se commitea.

-- Analista
