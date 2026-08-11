# Analista -- veredicto TASK-0353 r4: el CASO B muere, la resta lo resucita en otra clave

Reviewer: Analista (independent adversarial checker)
Date: 2026-08-11 15:39 (hora local UTC+2)
Task: TASK-0353 -- remediacion 4
Instruction: `Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0353-r4.md`
Scope declarado por Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE.

**Recommendation: CHANGE-REQUIRED.** Iteracion 2 de 2 ya se consumio en r3: la eleccion es del
operador humano, no mia ni tuya.

Tus dos preguntas, en una linea cada una:

1. **El CASO B deja de commitear. Medido por el proceso real: exit 1, cero commits, tarea en
   `ready`.** Cerrado.
2. **El conjunto se DERIVA de verdad** -- de los enums del propio esquema y de
   `REVIEW_QA_EVENTS`, ejecutando produccion con una sonda de lectura. No esta escrito a mano. Y el
   mutante MP4 que sobrevivio en r3 ahora **muere** contra una mutacion real de produccion.

Y aun asi no cierra, por una razon nueva y mas simple que las anteriores: **el contrato le RESTA al
conjunto derivado la lista `required` del esquema del hub**, y la puerta no vigila esa resta. Con un
esquema enrutado que no declara `changed_paths`, un turno que escribe **fuera del scope de su claim**
se acepta y se **commitea**. Es el CASO B verbatim, una clave mas alla, y la puerta que se apaga es
la del alcance de claim.

---

## 1. Ancla canonica y reproduccion

| item | value |
|---|---|
| ancla de la review | `02c58629d11c7f5b4b6f109e313c8bd656cd3658` |
| commit de implementacion | `1e178f3c` (ancestro de la ancla: verificado) |
| protocol HEAD al abrir | `6cd15d9c` (= `origin/main`; la ancla es ancestro) |
| delta ancla->HEAD en rutas de codigo revisadas | **ninguno** (solo ledger, `runtime/state/*` y `scripts/scan_encoding.ps1`, gemelo pwsh fuera de mi alcance) |
| clon limpio A (puertas + contrato) | `D:/Aegis_Scratch/map/rev0353r4/clone` @ `02c58629` |
| clon limpio B (sondas y mutantes) | `D:/Aegis_Scratch/map/rev0353r4/clone2` @ `02c58629` |
| python | 3.12.10 |

Nada se midio en arbol caliente. Cada veredicto es un exit code real del proceso. El arbol de los dos
clones quedo limpio tras cada sonda y tras cada mutante (`git status --short` vacio).

### Puertas de protocolo en el ancla, exit codes reales (clon limpio A)

```
python scripts/validate_collaboration_state.py --root .   EXIT=0   OK: collaboration state is valid.
python scripts/scan_encoding.py --root .                  EXIT=0   OK: encoding scan is clean.
python scripts/scan_domain_neutrality.py --root .         EXIT=0
python scripts/check_falsification_contracts.py --root .  EXIT=0
python runtime/protocol_replay.py --check-drift --root .  EXIT=0   verdict=CLEAN up_to_seq=8769
python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py  EXIT=0
```

La ancla esta verde. Drift 0.

---

## 2. Tabla vector por vector

| vector | veredicto | evidencia |
|---|---|---|
| PREGUNTA 1 -- el CASO B deja de commitear (proceso real) | **PASS -- cerrado** | seccion 3 |
| PREGUNTA 2 -- el conjunto se deriva o esta enumerado | **DERIVADO** (con dos puntos ciegos) | secciones 4 y 6 |
| AC4 -- la clase, no el campo | **SLIP** (clase abierta por la resta) | seccion 5 |
| AC5 -- negativo permanente por mutacion de produccion | **PASS en el eje que fallaba** (MP4 de r3 ahora muere) / **SLIP de estilo de lectura** | seccion 6 |
| (nuevo) CASO C -- `changed_paths`: falso negativo con commit | **ESCAPE VIVO** | seccion 5 |
| (nuevo) CASO D -- `outcome`: intento de saltar la puerta humana | **refutado por mi propia medicion** (no es escape) | seccion 7 |

No re-mido lo que ya firme: convergencia de anclas, premisa `additionalProperties`, MP1..MP3.

---

## 3. PREGUNTA 1 -- el CASO B muere, por el proceso real

Misma configuracion que en r3 seccion 8: raiz enrutada cuyo esquema **no declara `actions`**, y un
productor que declara `contract_change` **sin** `decision_refs`. Proceso real
(`orchestrator.py --run --once --replay-report`), no llamada directa; conteo de commits del propio
fixture antes y despues.

```
B1  raiz enrutada SIN actions + contract_change sin decision_refs
  guard raised          : ...turn_schema.json: routed schema omits top-level keys read by
                          orchestrator validation gates: actions
  PROCESS exit          : 1
  COMMITS before/after  : 1 -> 1     NOT COMMITTED
  task status after     : ready

B0  CONTROL, esquema vivo, el mismo turno
  guard raised          : NO (passes silently)
  keys erased by filter : []
  validate_turn(filtered): ['semantic: gate.decision_required: action contract_change requires decision_refs']
  PROCESS exit          : 0    turn outcome: rejected    turn commit: None
  COMMITS before/after  : 1 -> 1     NOT COMMITTED
  task status after     : ready
```

En r3 esta configuracion devolvia `outcome: ok` y **commiteaba** (`1e1abbd`). Hoy no llega ni a la
puerta: la raiz se rechaza antes de filtrar. **CASO B cerrado**, y el CASO A (`decision_refs`) cae
con el mismo guard porque `decision_refs` esta en las ocho.

Persiste **R11** sin cambio: el guard revienta con `ValueError` y traceback dentro de `run_loop`, sin
entrada de runlog. Ruidoso, que es lo que pedi; sigue siendo operabilidad, no correccion.

---

## 4. PREGUNTA 2 -- derivado, y bien derivado

No esta enumerado. `branch_covering_turn_corpus` construye el corpus **desde el propio esquema**:

- `schema["properties"]["outcome"]["enum"]` -- un turno por outcome;
- `schema["properties"]["actions"]["items"]["properties"]["type"]["enum"]` -- un turno por accion;
- `review_qa.REVIEW_QA_EVENTS` -- un turno por par (from, to) declarado en produccion;
- mas las formas de concurrencia (`aggregate_version`/`fencing_token`) y de `tools`.

`behaviorally_consumed_turn_keys` ejecuta `turn_validate.validate_turn` **de produccion** sobre cada
forma con `TurnReadProbe`, un `dict` que graba las lecturas de primer nivel, y hace la union. Y
`assert_branch_coverage` acredita que cada familia **entra por la rama que dice cubrir** (exige el
error concreto de cada rama: `objective friction`, `gate.decision_required`, `gate.diff_required`,
`gate.human_required`, `stale aggregate_version`, Review/QA). Es el corolario de TASK-0328 aplicado
bien: la poblacion sale de la condicion evaluada y se acredita el alcance de la rama.

Si manana alguien anade una regla que lea una novena clave **en una de esas ramas y con `.get()`**,
el conjunto crece y la igualdad exacta lo caza. Eso lo firmo, y lo mido en la seccion 6.

---

## 5. El escape nuevo: la RESTA de `required` (CASO C)

El contrato compara asi:

```python
optional_consumed = consumed_keys - set(base_schema["required"])
assert optional_consumed == set(orchestrator.VALIDATION_CONSUMED_TURN_KEYS)
assert optional_consumed <= orchestrator.turn_schema_keys(fixture_root)
```

La resta usa la lista `required` **del esquema del hub**:

```
required = ['turn_id', 'task_id', 'agent', 'outcome', 'summary', 'changed_paths', 'commit_message']
```

Toda clave que una puerta lee **y que ademas esta en esa lista** queda fuera de
`VALIDATION_CONSUMED_TURN_KEYS`, y por tanto **fuera del guard**. `turn_schema_keys` solo exige
`VALIDATION_CONSUMED_TURN_KEYS <= properties de la raiz enrutada`; **nadie exige que la raiz enrutada
conserve el `required` del hub**. La suposicion tacita -- "toda raiz enrutada comparte la lista
`required` del hub" -- es exactamente la que la clase de TASK-0353 declara falsa.

`changed_paths` es una de esas claves. La lee la puerta de alcance de claim
(`turn_validate.py:340`), y no esta en las ocho.

### CASO C -- medido, proceso real, con control

Raiz enrutada a la que le quito `changed_paths` de `properties` **y** de `required`. El productor
declara una escritura **fuera del scope de su claim** (`Area_comun/other/OUT_OF_SCOPE.md`).

```
C1  raiz enrutada SIN changed_paths
  guard raised          : NO (passes silently)
  keys erased by filter : ['changed_paths']
  validate_turn(filtered): []
  PROCESS exit          : 0    turn outcome: done    turn commit: fa2b670
  COMMITS before/after  : 1 -> 2     COMMITTED
  task status after     : done

C0  CONTROL, esquema vivo, el MISMO turno
  guard raised          : NO
  keys erased by filter : []
  validate_turn(filtered): ['semantic: write outside active claim scope: Area_comun/other/OUT_OF_SCOPE.md']
  PROCESS exit          : 0    turn outcome: rejected    turn commit: None
  COMMITS before/after  : 1 -> 1     NOT COMMITTED
  task status after     : ready
```

**La unica variable entre aceptado-y-commiteado y rechazado es la lista de propiedades del esquema de
la raiz enrutada.** El filtro borra la entrada, la puerta de alcance de claim no ve nada que gatear,
`validate_turn` devuelve `[]`, el turno se acepta, se commitea y la tarea salta a `done`.

Es el CASO B con otra clave, y la consecuencia es peor: lo que se apaga no es un aviso de contrato,
es **la frontera de escritura del sistema de claims**.

Alcance honesto, igual que en r3: ninguna raiz **embarcada hoy** dispara el CASO C. La clase es
alcanzable por la misma via que la tarea ya acepta como real -- `new_instance.py` copia el esquema del
momento y nada re-sincroniza la raiz cuando el hub avanza. Lo declaro como **clase abierta**, no como
escape vivo en un artefacto publicado. Y la resta deja sin cubrir, por la misma razon, a `task_id`,
`agent`, `outcome`, `summary`, `turn_id` y `commit_message`; solo probe dos de ellas.

---

## 6. AC5 -- mutantes de PRODUCCION: el de r3 muere, y aparece uno de estilo

Mutaciones aplicadas solo a `runtime/turn_validate.py` en el clon limpio B; el fichero se restauro
tras cada corrida (`git status --short` vacio). Gate por exit code real de
`examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`.

| mutante de PRODUCCION | resultado |
|---|---|
| BASELINE | exit 0 |
| **M0** -- regla condicional nueva sin declarar, leida con `report.get()` (= el MP4 que sobrevivio en r3) | **KILLED** (exit 1, `assert optional_consumed == set(orchestrator.VALIDATION_CONSUMED_TURN_KEYS)`) |
| **M1** -- **la misma regla**, leida a traves de `payload = dict(report)` | **SOBREVIVE** (exit 0) |

M0 es credito real y cierra el hallazgo central de r3.

M1 acredita el segundo punto ciego. `TurnReadProbe` graba `get`, `__getitem__` y `__contains__`; no
graba iteracion ni copia. Aislado, sin nada mas en medio:

```
after dict(probe).get      -> read_keys = []
after items() copy .get    -> read_keys = []
after iteration            -> read_keys = []
after direct .get          -> read_keys = ['next_hint']
```

Y acredito que la mutacion **esta viva**, que no es un edit nulo:

```
ALL errors (blocked, sin next_hint) : [... 'semantic: blocked turn must carry next_hint']
mutation fired                      : True
mutation silent WITH hint           : True
```

Una regla de produccion viva, que lee una clave no declarada, con el contrato en **exit 0**. La
promesa del handoff ("a new semantic requirement cannot silently diverge from this declaration") vale
para un estilo de lectura, no para la propiedad.

Consecuencia menor que la del CASO C -- necesita ademas una raiz que omita la clave -- pero es el
mismo patron que ya te firme dos veces: **se ata la FORMA (leer con `.get`) en lugar de la
PROPIEDAD (la clave se consume)**.

---

## 7. CASO D -- lo que intente romper y no rompi

Probe saltar la puerta humana: raiz enrutada sin `outcome`, turno `decision_required` declarando
`gate.human_required=false`. **No es escape.** Variante y control se comportan igual (`turn outcome:
rejected`, `schema: True was expected`, sin commit, tarea en `ready`): el propio esquema enrutado lo
caza antes por otra clausula. Lo dejo escrito porque un negativo medido vale tanto como un positivo.

---

## 8. Residuales declarados

- **R1**: sin cambios (monkey-patch acotado en AC3).
- **R2 -- SIN CI REAL.** Todo lo de arriba, lo mio incluido, es **LOCAL**. El negativo permanente
  vive en `falsification-runners`, que nadie ha visto correr en Actions.
- **R3**: los pasos `pwsh` siguen UNSUPPORTED en este host; no los juzgo. No re-corri el replicador
  completo en r4 (encargo corto): el saldo 63/6/8 que firme en r3 no lo re-mido aqui.
- **R4**: cerrada en r3. La frase de la declaracion sigue pasandose de alcance en el mismo sentido
  (ahora dice "todas las claves que la puerta lee", y la resta deja siete fuera).
- **R10 (de r3)**: el CASO B queda **cerrado**; la clase que nombraba **sigue abierta** por el CASO C.
- **R11**: sin cambio -- el guard aborta con traceback y sin runlog.
- **R12 (nuevo)**: la sonda de lectura es ciega a iteracion y copia (seccion 6).
- **R13 (nuevo)**: la resta de `required` deja sin cubrir `task_id`, `agent`, `outcome`, `summary`,
  `turn_id` y `commit_message`; solo medi `changed_paths` (escape) y `outcome` (no escape).

---

## 9. Lazo de correccion esperado

**CHANGE-REQUIRED.** La iteracion 2 de 2 se consumio en r3, asi que **la eleccion es del operador
humano**. Mi recomendacion, para que reciba una eleccion y no un dilema:

**(1) Si se sigue dentro de TASK-0353, la forma minima que cierra el eje es dejar de restar.** El
conjunto derivado no debe restarse el `required` del hub, porque ese `required` no es una propiedad
de las raices enrutadas: exigir `consumed_keys <= turn_schema_keys(root)` entero. Es un cambio de una
linea en el contrato y de una linea en el guard, y cierra el CASO C sin corpus nuevo. La forma que
cierra ademas R12 es la inversion que ya recomende en r3: que el guard afirme la **cobertura del
filtro** -- ninguna clave que la validacion lea puede desaparecer entre `schema_report()` y
`validate_turn()` -- en lugar de mantener una lista.

**(2) La alternativa legitima**: declarar cerrado el alcance de TASK-0353 en las ocho claves
derivadas -- que estan cerradas y demostradas, CASO A y CASO B incluidos -- y abrir tarea propia para
la clase, con el **CASO C como AC de partida** por ser el unico con consecuencia de commit y de
frontera de claims.

Lo que no acepto es cerrar con el **AC4 marcado como cumplido**: el AC4 pide propiedad y no
enumeracion, y lo que hay es una enumeracion de ocho -- derivada, que es progreso real -- vigilada
por un contrato que se resta a si mismo otras siete claves consumidas.

Puertas afectadas: `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`,
`runtime/orchestrator.py`, `runtime/turn_validate.py`, `scripts/validate_collaboration_state.py`,
`scripts/scan_encoding.py`, `scripts/scan_domain_neutrality.py`,
`scripts/check_falsification_contracts.py`, `runtime/protocol_replay.py --check-drift`.
Re-juicio mio en clon limpio ANTES del commit de cierre.

---

## 10. Respuesta directa a tus dos preguntas

> El CASO B deja de commitear?

**Si.** Proceso real: `exit 1`, commits `1 -> 1`, tarea en `ready`. El control con el esquema vivo
rechaza con el error honesto y tampoco commitea. Cerrado.

> El conjunto se deriva ejecutando las ramas o esta enumerado?

**Se deriva**, y bien: de los enums del esquema y de `REVIEW_QA_EVENTS`, ejecutando produccion, con
acreditacion de que cada forma entra por su rama. No esta escrito a mano.

**Pero el contrato le resta la lista `required` del hub antes de comparar**, y esa resta es la que
reabre la clase: con `changed_paths` fuera del guard, un turno que escribe fuera del scope de su
claim se acepta y se commitea (`fa2b670`).

-- Analista
