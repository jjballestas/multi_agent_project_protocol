# Analista -- veredicto TASK-0353: derivar el filtro del esquema NO cierra la clase

Reviewer: Analista (independent adversarial checker)
Date: 2026-08-10 02:41 (local time UTC+2)
Task: TASK-0353 -- produccion borra el campo que produccion exige
Instruction: `Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353.md`
Scope declared by Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE.

**Recommendation: CHANGE-REQUIRED.**

AC1, AC2 y AC3 los confirmo por comportamiento. **AC4 esta falsado**, **AC5 no cubre la clase
que declara** y **AC6 no reproduce** (62/7/8 medido, no 60/9/8 declarado). Reproduje el defecto
verbatim de TASK-0353 **en el propio commit de la correccion, sin modificar una sola linea de
codigo**. El arreglo no cerro la clase: la movio un nivel arriba, de "una lista de Python
contra el esquema" a "el esquema del modulo contra el esquema del `--root`". Y el negativo
permanente del AC5 **no muere** ante la mutacion que reabre la clase.

---

## 1. Ancla canonica y reproduccion

| item | value |
|---|---|
| commit bajo revision | `e853cb734f4c37b5cb3e308f5453292322b9207e` |
| commit de implementacion | `f4c6c3b99f471af74a9a19c6519432729f35eb59` |
| protocol HEAD al abrir | `37dd36bf` (`e853cb73` es ancestro) |
| delta anclaje->HEAD en rutas revisadas | ninguno: `git diff --stat e853cb73 37dd36bf -- runtime/ examples/ scripts/` toca solo `runtime/state/events.jsonl` y `snapshot.json` |
| clon limpio | `git clone` del hub a `D:/Aegis_Scratch/map/rev0353/clone`, `git checkout e853cb73` |
| python | 3.12.10 |
| pwsh 7 | ausente (los 8 pasos `pwsh` del replicador quedan UNSUPPORTED, igual que en la entrega) |

Nada se midio en arbol caliente. Cada veredicto de abajo es un exit code. El arbol del clon
quedo limpio (`git status --short` vacio) despues de cada sonda; lo verifique tras cada una.

### Puertas de protocolo en el clon limpio

```
python scripts/validate_collaboration_state.py --root .    EXIT=0   OK: collaboration state is valid.
python scripts/scan_encoding.py --root .                   EXIT=0   OK: encoding scan is clean.
python scripts/scan_domain_neutrality.py --root .          EXIT=0
python scripts/check_falsification_contracts.py --root .   EXIT=0
python runtime/protocol_replay.py --check-drift --root .   EXIT=0   PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8468
```

---

## 2. Tabla vector por vector

| vector | veredicto | evidencia |
|---|---|---|
| AC1 -- falsacion previa por comportamiento | PASS | seccion 3 |
| AC2 -- la ruta enrutada deja de ser insatisfacible | PASS | seccion 4 |
| AC3 -- el gemelo embarcado (tal como esta escrito) | PASS | seccion 5 |
| AC4 -- la clase, no el campo | **SLIP** | seccion 7 (E1b, E1, E3) |
| AC5 -- negativo permanente verificado por mutacion | **SLIP parcial** | seccion 8 (M4 sobrevive) |
| AC6 -- sin regresion | **SLIP** | seccion 9 (62/7/8, no 60/9/8) |
| FOCO 1 -- "la segunda copia sigue rota" | **premisa incorrecta** | seccion 6 |
| FOCO 3 -- "verde por construccion" | **refutado** | seccion 8 (3 de 4 mutantes mueren) |

---

## 3. AC1 -- reproducido en el commit padre, ejecutando

Escribi el `runtime/orchestrator.py` de `f4c6c3b9^` sobre el clon y ejecute:

```
PRE-FIX: TURN_SCHEMA_KEYS exists: True
PRE-FIX: 'obstacles' in it      : False
PRE-FIX: producer delivered     : True
PRE-FIX: survives schema_report : False
PRE-FIX: validate_turn(filtered): ['semantic: delivery turn is missing the obstacles block; use [] when there was no friction']
```

Retenga esa cadena de diagnostico. Vuelve a aparecer, identica, en la seccion 7 **con el
codigo corregido**.

---

## 4. AC2 -- la ruta enrutada, medida por mi, no por su test

No me apoye en `exercise_routed_delivery`. Construi mi propia entrega con un bloque
`obstacles` NO VACIO y la enrute por el orquestador real (`runtime/orchestrator.py --run
--once --replay-report ...`):

```
ok            : True
outcome       : done
trace[:6]     : ['gate_pre', 'route', 'claim', 'adapter', 'validate', 'human_gate']
obstacles reaches the runlog : True
errors        : []
```

El campo sobrevive hasta `validate` y el turno se acepta. AC2 cumplido.

---

## 5. AC3 -- la instancia nueva, ejecutando

`examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` sale **exit 1**,
pero el caso de esta tarea NO esta entre los fallos. Los 8 fallos son todos la misma causa
ajena y preexistente (`ERROR: Unresolved placeholders remain in generated instance:
scripts\memory\test_memory_db.py`), territorio de TASK-0350. El caso
`case_generated_runtime_preserves_validator_fields` no aparece en la lista de `failures` y su
instancia se genero (`OK: created protocol instance at ...tier-runtime-schema-filter-...`).

La entrega declaro esto con exactitud y no reclamo verde el runner completo. Correcto.

**Residual R1:** el caso de AC3 corre `new_instance.main()` con la puerta de produccion
`find_unresolved_placeholders` monkey-parcheada a `[]`. La particion esta acotada por un
`assert normalized <= {"scripts/memory/test_memory_db.py"}`, asi que no puede tapar otra
cosa; pero es una puerta de produccion desarmada dentro de un caso de aceptacion, y eso se
declara, no se hereda en silencio.

---

## 6. FOCO 1 -- la segunda copia NO esta rota. La premisa es incorrecta, y lo medi

Pediste que juzgue "si la clase esta cerrada mientras una copia del repo conserva el
defecto". La respuesta empieza por corregir el hecho: **el espejo no conserva el defecto.**

El defecto de TASK-0353 exige DOS cosas a la vez: (a) el filtro borra el campo, y (b) una
regla de validacion exige ese campo. Tu medida solo comprobo (a). Medido (b):

```
mirror defines validate_delivery_obstacles : False
mirror defines is_delivery_turn            : False
mirror mentions 'obstacles' anywhere       : False    (0 ocurrencias en el fichero entero)
hub  defines validate_delivery_obstacles   : True
```

Y ademas el espejo es internamente coherente:

```
mirror has TURN_SCHEMA_KEYS          : True
mirror list == mirror schema props   : True
in list not in schema                : []
in schema not in list                : []
mirror schema: schema_version 1.2.0, additionalProperties False, sin 'obstacles'
```

En el espejo no hay ninguna regla que exija `obstacles`, su esquema no lo declara y su lista
coincide EXACTAMENTE con su propio esquema. Que `obstacles` no sobreviva a su filtro es el
comportamiento **correcto** para esa instantanea. El espejo esta **viejo**, no roto.

Los dos contratos que lo leen como gemelo de paridad
(`run_runtime_turn_obstacle_cases.py:276` y `test_exec_lease_harness.py:1373`) atan
unicamente `parse_porcelain_v1_z` / `dirty_worktree_paths`. **Ninguno de los dos** ata la
paridad del filtro de esquema. Asi que el espejo tampoco esta bajo contrato por esta
propiedad.

Lo que si es cierto, y es peor que lo que preguntabas: **esa copia vieja es exactamente el
arma que dispara la fuga de la seccion 7.** El repo ya embarca hoy dos `turn_schema.json`
divergentes (1.3.0 y 1.2.0). No hay que imaginar una divergencia futura: ya existe, commiteada.

---

## 7. FOCO 2 / AC4 -- la clase NO esta cerrada. Tres medidas

El arreglo elimina la lista de Python y deriva de `runtime/turn_schema.json`. Eso cierra la
divergencia **por esa via**. La pregunta del AC4 es si cierra la propiedad: *ningun campo
exigido por la validacion puede faltar en el filtro*. No la cierra. La derivacion tiene dos
premisas ocultas que nadie afirma.

### 7.1 Las dos anclas no son la misma

```
filtro : Path(orchestrator.__file__).with_name("turn_schema.json")     runtime/orchestrator.py:113
puerta : (root / "runtime" / "turn_schema.json")                       runtime/turn_validate.py:315
```

El filtro se ancla al **directorio del modulo**; la puerta de esquema se ancla al **`--root`**.
Son dos ficheros distintos y nada exige que coincidan. `--root` es un parametro libre
(`runtime/orchestrator.py:1213`), y el patron cruzado no es hipotetico: **seis runners
embarcados** invocan literalmente `<hub>/runtime/orchestrator.py --root <otra raiz>`:

```
examples/llm_adapter_cases/run_llm_adapter_cases.py:193
examples/runtime_budget_cases/run_runtime_budget_cases.py:138
examples/runtime_eventlog_gate_cases/run_runtime_eventlog_gate_cases.py:204
examples/runtime_loop_cases/run_runtime_loop_cases.py:264
examples/runtime_observability_cases/run_runtime_observability_cases.py:138
examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py:310
```

Los seis siguen verdes porque **cada constructor de fixture copia el esquema del hub a mano**
(`run_runtime_loop_cases.py:148-150`, `run_runtime_turn_semantic_cases.py:34`,
`run_agent_registry_cases.py:29`). Eso no es una derivacion: es una sincronizacion manual de
dos artefactos. Es la misma forma del defecto que TASK-0353 nombra, un nivel mas arriba.

### 7.2 E1b -- el defecto VERBATIM, en el commit corregido, sin tocar codigo

Modelo el caso natural: un orquestador cuyo `runtime/` es mas viejo que la raiz que enruta.
Uso como esquema del modulo **el fichero 1.2.0 que este mismo repo ya embarca**
(`examples/full_runtime_instance/runtime/turn_schema.json`). Cero cambios de codigo.

```
orchestrator runtime/ schema : 1.2.0
--root schema                : 1.3.0
producer delivers obstacles           : True
survives schema_report (post-fix)     : False
validate_turn(filtered) -> ['semantic: delivery turn is missing the obstacles block; use [] when there was no friction']
```

Compara con la seccion 3. **Es la misma cadena, byte a byte.** Un productor entrega el campo
obligatorio, el filtro derivado lo borra, y la validacion lo rechaza por ausente. La ruta
enrutada vuelve a ser INSATISFACIBLE en el commit que dice haberlo arreglado. Esto falsa el
AC4 en su letra: "ningun campo exigido por la validacion pueda faltar en la lista de claves".

### 7.3 E1 -- la direccion contraria tampoco tiene salida

Instancia mas vieja que el hub (lo que produce `new_instance.py` cuando el hub avanza):

```
root schema_version : 1.2.0     hub schema_version : 1.3.0
obstacles survives the hub-anchored filter : True
validate_turn(with obstacles)    -> ["schema: Additional properties are not allowed ('obstacles' was unexpected)"]
validate_turn(without obstacles) -> ['semantic: delivery turn is missing the obstacles block; use [] when there was no friction']
```

Bloqueado en las dos direcciones: con el campo, la puerta de esquema lo rechaza; sin el, la
regla semantica lo exige.

### 7.4 E3 -- la premisa `additionalProperties: false`, a un keyword de distancia

`turn_schema_keys()` deriva de `properties`. El conjunto que la puerta ACEPTA es
`properties` **solo mientras** `additionalProperties` sea `false`. Nada afirma esa premisa.
Cambiando ese unico keyword a `true` (una relajacion plausible: extensiones de proveedor),
con ambas anclas de acuerdo:

```
gate accepts the extra field   : True
survives schema_report         : False
```

La puerta acepta un campo que el filtro borra. Anade manana cualquier regla semantica que lo
lea -- exactamente lo que TASK-0259 hizo con `obstacles` -- y la condicion insatisfacible
vuelve, identica.

### 7.5 La lista hermana sigue cableada a mano, en el mismo paquete

Barri `runtime/` buscando la misma FORMA (un literal de Python que duplica un hecho del
esquema), no el mismo nombre. Queda una:

```
runtime/llm_turn_wrapper.py:32   REQUIRED_REPORT_KEYS = {7 claves literales}
runtime/llm_turn_wrapper.py:48   default_schema_path() -> el MISMO turn_schema.json
runtime/llm_turn_wrapper.py:104  if REQUIRED_REPORT_KEYS.issubset(candidate): return candidate

wrapper list    : ['agent','changed_paths','commit_message','outcome','summary','task_id','turn_id']
schema required : ['agent','changed_paths','commit_message','outcome','summary','task_id','turn_id']
equal today     : True
```

El mismo modulo **ya carga el esquema** (`load_schema`) y a la vez mantiene a mano una copia
de su array `required`. Iguales hoy; nada las ata. Si `required` crece, `extract_report`
elige el candidato JSON equivocado y cae al `candidates[0]` -- consecuencia mas leve que la
insatisfacibilidad, pero **la misma clase**, a tres lineas de una derivacion.

Seamos justos con el maker: `runtime/llm_turn_wrapper.py` **NO esta en los `scope_routes` de
TASK-0353**, asi que esto no es un incumplimiento de la entrega. Lo cuento porque el AC4 no
pide arreglar un fichero: pide **el criterio** que impide la proxima divergencia. Un criterio
que no alcanza al hermano que ya lee el mismo esquema no es todavia un criterio.

---

## 8. FOCO 3 / AC5 -- el mutante es de produccion y NO es verde por construccion; pero no cubre la clase que nombra

Comprobe las dos cosas que pediste, ejecutando cuatro mutantes de **produccion** (no del
runner) contra `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`. Baseline:
EXIT=0 en 3.6 s.

| mutante de produccion | resultado |
|---|---|
| M1 -- `schema_report` vuelve a cablear una lista literal (ignora `turn_schema_keys()`) | **KILLED** (exit 1) |
| M2 -- `turn_schema_keys()` deriva del esquema del espejo (fuente divergente) | **KILLED** (exit 1) |
| M5 -- `turn_schema_keys()` deriva de `required` en vez de `properties` | **KILLED** (exit 1) |
| M4 -- `runtime/turn_schema.json`: `additionalProperties` false -> true | **SOBREVIVE** (exit 0) |

Verifique que M4 se aplico de verdad antes de correr:
`mutation applied, additionalProperties = True` / `runner exit under M4: 0`.

**Tu FOCO 3 queda refutado en su parte principal:** el mutante es de produccion (monkey-patch
del atributo de modulo `orchestrator.turn_schema_keys`, no un `.replace()` sobre la fuente del
propio runner), y el negativo NO esta verde por construccion -- tres de cuatro mutantes de
produccion mueren.

**Pero no cubre la clase que su propio texto declara.** El AC5 pide un contrato que muera "si
un campo exigido por la validacion vuelve a quedar fuera del filtro de esquema". Bajo M4
ocurre exactamente eso y el contrato sigue verde. Y el contrato no puede detectar E1b/E1 por
construccion: `behaviorally_required_turn_keys(clean, fixture_root)` deriva las claves contra
un `fixture_root` **cuyo esquema es una copia del hub**, asi que el test nunca ejerce la unica
configuracion en la que las dos anclas difieren.

Detalle menor del mismo signo: `removed_key = min(required_keys)` muta **una** clave, la
alfabeticamente minima. Ata el helper, no el efecto.

---

## 9. FOCO 4 / AC6 -- el saldo NO reproduce. 62/7/8, no 60/9/8

Corri el replicador entero en el clon limpio, al anclaje que me diste:

```
python scripts/replay_validate_job.py --root .
SUMMARY declared=77 pass=62 fail=7 unsupported=8
EXIT=1
```

**Declarado por la entrega: 60 / 9 / 8. Medido por mi en `e853cb73`: 62 / 7 / 8.**

Los 8 UNSUPPORTED coinciden exactamente ({6,7,12,19,20,21,73,77}, todos `pwsh`). Los fallos no:

```
declarados (9) : 34, 36, 39, 40, 43, 50, 53, 58, 59
medidos    (7) : 17, 36, 43, 50, 53, 58, 59
NUEVO, no declarado        : 17  "Check systematic state pruning"
declarados pero PASAN ahora: 34, 39, 40
```

La aritmetica cierra exactamente: 60 +3 (los tres que pasan) -1 (el nuevo que falla) = 62; y
9 -3 +1 = 7. No hay ningun paso escondido ni desaparecido: los 77 estan.

### 9.1 Los tres declarados que pasan

Los corri sueltos en un worktree del **commit de implementacion** `f4c6c3b9`, que es donde el
maker midio:

```
exit=0  examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py   (paso 34)
exit=0  examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py           (paso 39)
exit=0  examples/runtime_protocol_genesis_ref_cases/run_runtime_protocol_genesis_ref_cases.py   (paso 40)
```

Pasan en su propio commit, y pasan tambien dentro de mi secuencia completa en el anclaje. La
lista de nueve esta equivocada en tres. Caveat honesto: no descarto que sean sensibles al
orden dentro del replicador; lo que si esta medido es que en la secuencia completa, al
anclaje, pasan.

### 9.2 El fallo NUEVO: el paso 17, y no lo causa el codigo de Codex

```
paso 17 "Check systematic state pruning"  ->  scripts/prune_state.py --root . --check

f4c6c3b9  (implementacion, donde se midio 60/9/8)  EXIT=0   OK: prune not due (cold_start_tokens=13950)
e853cb73  (anclaje de esta review)                 EXIT=1   PRUNE DUE: released_ratio 91.3 >= 90
37dd36bf  (HEAD al abrir)                          EXIT=1   PRUNE DUE: released_ratio 92.0 >= 90
```

Exit codes reales, no salida por tuberia. **Esto no es una regresion del arreglo**: es la poda
vencida, deber de mantenimiento del Arquitecto, disparada por los propios commits de ledger
que la entrega y el ruteo anadieron entre `f4c6c3b9` y `e853cb73`. Lo cuento porque el AC6
dice "no empeora; se declara el saldo antes y despues", y el saldo declarado no describe ni
el commit de implementacion (tres de sus nueve pasan) ni el anclaje que me diste (falla uno
que no esta en la lista). **AC6: SLIP.**

**Accion para ti, fuera de esta tarea:** el gate de poda esta ROJO en HEAD (92.0 >= 90). Todo
job `validate` que arranque desde HEAD muere en el paso 17 antes de llegar a los pasos que
esta tarea toca.

---

## 10. Residuales declarados

- **R1** (seccion 5): el caso de AC3 desarma `find_unresolved_placeholders` de
  `new_instance.py`. Acotado por assert, pero es una puerta de produccion apagada dentro de
  una aceptacion.
- **R2 -- SIN CI REAL.** Como avisaste, esta tarea no lleva AC de CI y la cuenta de Actions
  esta bloqueada por facturacion. **Todo lo de arriba, mio incluido, es local.** Lo que MENOS
  se sostiene en local es precisamente la seccion 7: los seis runners cruzados pasan hoy
  porque cada fixture copia el esquema a mano; nadie ha visto correr esos pasos en Actions.
  Declarado como residual, no como verde.
- **R3**: 8 pasos `pwsh` siguen UNSUPPORTED en este host (no hay pwsh 7). No los juzgo.
- **R4** (seccion 6): el repo embarca dos `turn_schema.json` divergentes (1.3.0 y 1.2.0) sin
  ninguna declaracion de que la divergencia sea deliberada. No es un defecto por si mismo; es
  el insumo de E1b.
- **R5** (seccion 9): el gate de poda (paso 17) esta ROJO en HEAD `37dd36bf`
  (`released_ratio 92.0 >= 90`, exit 1). No es de esta tarea ni de Codex, pero mata el job
  `validate` antes de llegar a los pasos que esta tarea toca. Deber del Arquitecto.
- **R6** (seccion 9.1): no descarto sensibilidad al orden en los pasos 34/39/40 dentro del
  replicador; lo medido es que pasan sueltos en `f4c6c3b9` y dentro de la secuencia completa
  en `e853cb73`.

---

## 11. Lazo de correccion esperado

**CHANGE-REQUIRED. Maximo 2 iteraciones antes de escalar al operador humano.**

Lo que tiene que sostener la remediacion (propiedad, no forma -- no aceptare una version mas
estrecha del mismo cableado):

1. **Una sola ancla por turno enrutado.** Para un turno concreto, el filtro y la puerta de
   esquema deben resolver al MISMO artefacto. O el filtro se deriva del `root` contra el que
   se va a validar, o el codigo afirma que las dos anclas son el mismo fichero y falla
   ruidosamente cuando no lo son. El silencio no vale: el sintoma de hoy es un diagnostico
   que miente ("campo ausente" cuando el productor lo entrego).
2. **La premisa se afirma o se elimina.** O el filtro deriva el conjunto que la puerta
   ACEPTA (no `properties` a secas), o algo falla si `additionalProperties` deja de ser
   `false`.
3. **El negativo muere en las dos.** El contrato permanente debe morir ante (a) anclas
   divergentes y (b) `additionalProperties: true`. Hoy M4 sobrevive; ese mutante es el minimo
   de la nueva barra.
4. **R4 se resuelve o se declara.** Si el espejo debe divergir por ser instantanea historica,
   que este escrito. Si no, converge. Hoy no esta declarado.
5. **El saldo se re-declara sobre el arbol remediado**, con la lista de fallos derivada del
   propio run y no transcrita: los tres pasos 34/39/40 no estaban fallando y el 17 si.

Puertas afectadas por la remediacion: `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`,
`scripts/check_falsification_contracts.py`, `scripts/replay_validate_job.py`,
`scripts/validate_collaboration_state.py`, `scripts/scan_encoding.py`,
`scripts/scan_domain_neutrality.py`. Re-juicio mio en clon limpio ANTES del commit de cierre,
e incluyendo la re-medicion completa del replicador (R5).

---

## 12. Respuesta directa a tu pregunta

> Derivar el filtro del schema cierra la CLASE, o queda una via por la que los dos vuelvan a divergir?

**Queda via, y la ejecute.** No una, tres: las dos anclas (`__file__` vs `--root`) en las dos
direcciones, y la premisa `additionalProperties: false` sin afirmar. La primera reproduce el
defecto **verbatim, en tu commit, con cero cambios de codigo**. El arreglo sustituyo "dos
listas que se mantienen por separado" por "dos ficheros que se mantienen por separado con
seis sentencias de copia". Es una forma mas estrecha del mismo patron, no la propiedad.

-- Analista
