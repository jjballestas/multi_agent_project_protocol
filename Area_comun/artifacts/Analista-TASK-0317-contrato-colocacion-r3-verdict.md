---
title: "Veredicto Analista r3 -- TASK-0317: el contrato de colocacion NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY"
task_id: TASK-0317
type: review
owner: Analista
status: done
created_at: 2026-08-07
---

# Veredicto adversarial r3 -- TASK-0317 (commit f2c6c315)

**Recomendacion de cierre: CAMBIO-REQUERIDO.**

Respondo tu pregunta literal -- *"el contrato de colocacion tiene dientes de verdad, o se puede
mover la exencion sin que ningun gate lo note?"* -- con una medicion, no con una lectura del diff:

**Tiene dientes reales contra cuatro de las cinco formas de moverla que construi. Y si: la quinta
mueve la exencion, rompe la garantia, y pasa el stack de gates COMPLETO en clon limpio con exit 0.**

La escapatoria no es una variante exotica. Es la mitad del espacio que tu propio AC3 senalaba:
el contrato fija **un** timestamp (`2026-06-19T09:28:23.123456-05:00`), y una exencion movida
al tope del bucle que solo capture la forma **fecha sola** (`2026-06-19`) deja intacto ese
payload, deja las dos cadenas-fixture con `count == 1`, y sale limpia. Son **3 de las 333** cadenas
de la familia que el propio `test_supported_timestamps_and_medium_priority_are_accepted` genera
30 lineas mas arriba, en la misma clase.

Aclaro el alcance del bloqueo para que no se re-litigue lo ya cerrado: **el fix funcional que
aprobe en r2 sobre `3d64a7c` esta intacto y sigue correcto** -- lo re-medi. Lo unico que pido
cambiar es la asercion conductual del test nuevo, y la remediacion la deje probada abajo.

---

## 1. Ancla canonica y reproduccion

| Item | Valor |
|---|---|
| Commit bajo revision | `f2c6c3154806d6e27b5ed8b831208c3cce81e30f` |
| Ancla | `origin/main` lo contiene; HEAD local `e6736185` solo anade coordinacion |
| Clon limpio | `D:/Aegis_Scratch/hub/an0317/cc`, `git clone --no-local` + `--unshallow`, checkout de f2c6c315, `git status --short` vacio |
| Alcance de producto | ninguno (hub, gates de Python), tal como declaraste |
| Hora local de emision | 2026-08-07 01:04 (UTC+2) |

Gates recomputados por mi, **en el clon limpio**, gateando por exit code:

| Gate | Comando | Exit |
|---|---|---|
| Estado canonico | `python scripts/validate_collaboration_state.py --root .` | **0** |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** |
| Neutralidad | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Poda | `python scripts/prune_state.py --root . --check` | **0** (no vencida) |
| Contratos de falsacion | `python scripts/check_falsification_contracts.py --root . --inventory` | **0** |
| Suite de memoria (como CI) | `python scripts/memory/test_memory_db.py` | **0** -- `Ran 60 tests ... OK` (323,159 s) |
| Build corpus real | `python scripts/memory/build_memory_db.py --root .` | **0** -- 4225 artefactos, 219 warnings, **0 de clave de fecha** (AC4 al pie de la letra) |
| Drift | `python scripts/memory/check_memory_db_drift.py --root . --fast` / `--full` | **0** / **0**, `"result":"pass"` en ambos |

Nota metodologica: la primera pasada de `validate` me dio exit 1 por
`commit_trailers could not scan git history from 57f6250f...`. **No es un rojo del entregable**:
era mi clon con `--depth`, sin el commit base en el grafo. Tras `git fetch --unshallow` el mismo
comando da exit 0. Lo dejo escrito porque un clon superficial produce ese falso rojo y conviene
que quede en el runbook.

---

## 2. Vector por vector

Metodo: para cada vector construi el mutante **como fuente real** (no como cadena en un test),
lo escribi en `scripts/memory/build_memory_db.py` de un sandbox, y pregunte lo unico que importa:
*si un maker commiteara ESTA regresion, falla el gate?*

| # | Vector | Mutante | Veredicto |
|---|---|---|---|
| V1 | La mutacion declarada es la que de verdad rompe la garantia | la del contrato, reconstruida aparte | **PASS** |
| V2 | Sacar la exencion a una FUNCION APARTE y llamarla al tope del bucle | A | **PASS** (cazado: `AssertionError: False is not true`) |
| V3 | Mover la exencion DEBAJO de la heuristica de telefono y ENCIMA del chequeo de dominio | B | **PASS** (cazado: `AssertionError: 1 != 0`, por la asercion de texto-fuente) |
| V4 | No moverla: ENSANCHAR `DATE_RE` para que la exencion se trague no-fechas | C | **PASS** (el contrato NO lo caza; lo caza `test_timestamp_pii_suffix_is_rejected`, 11 vectores) |
| V5 | Calcular la exencion EN SITIO y reusarla para saltarse el chequeo de dominio | D | **PASS** (cazado: `AssertionError: False is not true`) |
| V6 | **Mover al tope del bucle una exencion de fecha MAS ESTRECHA que el payload del contrato** | **E** | **SLIP** |
| V7 | El negativo esta cableado en el inventario | `--inventory` | **PASS** |
| V8 | CI ejecuta de verdad el `exercised_by` | `.github/workflows/validate.yml:49` + `unittest.main` | **PASS** |
| V9 | Sin regresion (suite, build, drift, protocolo) | clon limpio, por exit code | **PASS** |

### V7/V8 -- el cableado, con nombres

No repetimos 0316. El contrato **si** se dispara:

    DECLARED NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY boundaries=2 runner=scripts\memory\test_memory_db.py

y `scripts/check_falsification_contracts.py` no es decorativo: exige que la cadena `mutation` y
**cada** `boundaries` aparezcan literalmente dentro del cuerpo del `exercised_by`, y falla si el
marcador `PERMANENT_NEGATIVE:` existe sin contrato o al reves. CI corre las tres cosas en el mismo
step (`validate.yml:47-50`): el checker con `--inventory`, `test_falsification_contracts.py` y
`scripts/memory/test_memory_db.py`; el fichero de test cierra con `unittest.main(verbosity=2)`, asi
que el metodo entra en la corrida (`Ran 60 tests`). Verificado, no inferido.

### V4 -- por que lo doy PASS aunque el contrato no lo vea

Ensanchar `DATE_RE` es un escape real (`contains_pii("2026-06-19 +34 600 123 456")` pasa de `True`
a `False`), pero **no lo tapa el silencio**: rompe 11 subtests de
`test_timestamp_pii_suffix_is_rejected` mas `test_supported_timestamps_and_medium_priority_are_accepted`.
Es exactamente el AC2 de la tarea (*"la correccion no puede consistir en ... ensanchar DATE_RE"*)
con dientes mecanicos, no solo con prosa. Lo anoto porque el credito le corresponde a otro test, no
a este contrato -- y porque TASK-0322 va justo a esa superficie.

---

## 3. El SLIP (V6), falsificable

**Mutante E.** Una sola insercion al tope del bucle de `contains_pii`, sin tocar nada mas:

    for item in value_list(value):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", item):
            continue
        normalized = re.sub(r"[_/\\.-]+", " ", item)
        ...

Es literalmente el negativo que el contrato declara -- *"Moving the date exemption above the phone
heuristic bypasses later PII checks"* -- asi que **no es un residual fuera de alcance: es el
contrato fallando en su propio enunciado**.

**Es una regresion de comportamiento real** (medido, mismo interprete, un modulo contra el otro):

| payload | terminos de dominio | f2c6c315 | mutante E |
|---|---|---|---|
| `2026-06-19` | `["2026"]` | `True` | **`False`** |
| `1988-04-11` | `["1988"]` | `True` | **`False`** |
| `2026-06-19T09:28:23.123456-05:00` | `["2026"]` | `True` | `True` (el payload del contrato) |

**Y pasa el stack completo**, en el clon limpio con `.git` (no en un sandbox recortado, para que
`test_current_tree_build_does_not_change_tracked_status` corriera de verdad):

| Gate sobre el mutante E | Exit |
|---|---|
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** |
| `python scripts/memory/test_memory_db.py` | **0** -- `Ran 60 tests ... OK` (337,915 s) |
| `test_timestamp_exemption_is_phone_only_and_falsifiable` aislado | **0** |

Control obligado, para no vender un falso cazado: corri el arbol **sin mutar** en el mismo sandbox
recortado y da el mismo unico `ERROR` (`test_current_tree_build_does_not_change_tracked_status`,
que necesita `.git`). Por eso repeti E en el clon con historia: alli el gate entero es **verde**.

**Por que se cuela, mecanicamente.** El unico diente conductual del contrato sobre la fuente real
es su primera linea:

    self.assertTrue(memory_db.contains_pii(timestamp, [domain_term]))

fijada a **un** ejemplo. Las dos aserciones siguientes son de texto-fuente
(`assertEqual(1, source.count(...))`) y E las respeta: deja `phone_guard` y `normalized_line`
intactas, `count == 1` cada una. Y el medio mutante del propio test sigue funcionando (el `assertFalse`
pasa), porque la mutacion declarada se aplica encima sin conflicto. Resultado: verde con el agujero
dentro.

**Esto es el defecto que abrio esta misma tarea.** El AC3 de TASK-0317 dice, textualmente, que el
test previo *"fija 6 formatos que esquivan justo la mitad negativa del espacio: esa cobertura
aparente es parte del defecto"*. La proteccion que plegaste para blindar la linea recien escrita
reintroduce ese patron: fija 1 formato y la mitad no cubierta (fecha sola) es justo donde vive el
escape.

---

## 4. Remediacion pedida (probada por mi, no propuesta a ciegas)

Barrer la **familia que la propia clase ya genera** en lugar de un ejemplo. El generador esta
30 lineas mas arriba, en `test_supported_timestamps_and_medium_priority_are_accepted`
(`test_memory_db.py:365-381`, 333 cadenas): extraerlo a un helper o replicarlo, y hacer

    for value in family:
        with self.subTest(value=value):
            self.assertTrue(memory_db.contains_pii(value, ["2026"]), value)

Medido por mi sobre las 333:

| Fuente | miembros de la familia que se saltan el chequeo de dominio |
|---|---|
| f2c6c315 (actual) | **0 de 333** -- el barrido queda VERDE hoy, no obliga a tocar codigo de produccion |
| mutante E | **3 de 333** (`2026-01-01`, `2026-06-19`, `2026-12-31`) -- el barrido lo CAZA |

Coste: una iteracion, solo `scripts/memory/test_memory_db.py`, riesgo cero sobre produccion.
Opcional y gratis: barrer tambien el `assertFalse` del mutante con la misma familia (se cumple para
las 333, porque el mutante declarado hace `continue` en cualquier `DATE_RE.fullmatch`), con lo que
la falsabilidad queda fijada a la familia por los dos lados.

---

## 5. Residuales que declaro (NO bloqueantes)

- **R3-1 -- fragilidad de las aserciones de texto-fuente.** `assertEqual(1, source.count(phone_guard))`
  y su gemela atan el contrato a dos lineas literales. Es **fail-closed** (fue lo que cazo el
  mutante B, y lo prefiero asi), pero un refactor inocente de esas lineas rompera el test con un
  mensaje (`1 != 0`) que no explica la garantia. Sugerencia barata: un mensaje en la asercion que
  diga que la fixture quedo obsoleta y hay que re-derivar el mutante.
- **R3-2 -- el credito de AC2 no es de este contrato.** El escape por ensanchar `DATE_RE` lo cazan
  `test_timestamp_pii_suffix_is_rejected` y el test de familia; si alguna vez se relaja alguno de
  esos dos, el ensanchamiento se queda sin ningun gate. Interactua con TASK-0322.
- **R3-3 -- clon superficial produce falso rojo de `validate`.** `commit_trailers` necesita el
  commit base en el grafo; con `--depth` da exit 1 sin que haya nada roto. Vale para el runbook de
  cualquiera que gatee en clon limpio.

---

## 6. Bucle de correccion esperado

1. **Remediacion (r4):** barrido de la familia en la asercion conductual de
   `test_timestamp_exemption_is_phone_only_and_falsifiable`. Solo
   `scripts/memory/test_memory_db.py`. Nada de codigo de produccion.
2. **Gates afectados:** `python scripts/memory/test_memory_db.py` (exit 0),
   `python scripts/check_falsification_contracts.py --root . --inventory` (exit 0) --
   ojo, si se extrae el generador a un helper, el checker exige que `mutation` y las dos
   `boundaries` sigan apareciendo **literalmente** dentro del cuerpo del `exercised_by`.
   Ademas `validate` + `scan_encoding` + drift `--fast`/`--full` en clon limpio.
3. **Re-juicio antes del commit de cierre:** re-corro el mutante E contra el arbol remediado y
   exijo que **falle**; solo entonces ratifico.
4. **Maximo 2 iteraciones** antes de escalar al operador humano.

---

## 7. Lo que NO digo

No digo que el codigo de produccion tenga un defecto: **no lo tiene**, ni hoy ni en el corpus
anclado (4225 artefactos, 0 warnings de clave de fecha). No digo que el contrato sea decorativo:
caza 4 de las 5 formas que probe y esta cableado de verdad en CI. Digo que su unico diente
conductual esta fijado a un ejemplo, que encontre la forma de moverla que ese ejemplo no ve, y que
cerrarlo asi seria firmar "la colocacion esta fijada" cuando lo fijado es un punto del espacio.

-- Analista (voz adversarial independiente), 2026-08-07 01:04 (UTC+2)
