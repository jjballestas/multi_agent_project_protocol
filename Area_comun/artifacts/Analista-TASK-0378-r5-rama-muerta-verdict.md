# Veredicto Analista -- TASK-0378 r5 (bb419bc0): borrar `claim_gate_applicable`

**Reviewer:** Analista (checker independiente)
**Fecha:** 2026-08-18 01:20 local (UTC+2)
**Instruccion:** `Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0378-r5.md`
**Veredicto:** **OK-CERRABLE** (con residuo declarado, de otra capa -- ver seccion 6)

---

## 1. Ancla canonica y reproduccion

| Concepto | Valor |
|---|---|
| Commit de producto bajo revision | `bb419bc08a274439569c0daaff598685d180433c` (`bb419bc0`) |
| Control historico (padre) | `9ad9b6a5` (`bb419bc0^`) |
| Ancestro de `origin/main` | SI (`git merge-base --is-ancestor bb419bc0 origin/main` -> 0) |
| Clon limpio NUEVO | `git clone -s -n <repo> an0378r5 && git checkout bb419bc0` |
| Clon limpio VIEJO | `git clone -s -n <repo> an0378old && git checkout bb419bc0^` |
| Raiz de scratch | `D:/Aegis_Scratch/protocol/` (DECISION-0104) |

Ningun gate se corrio en el arbol caliente: el arbol de trabajo tiene una entrega de Codex a medias
(TASK-0414 r5b) y habria mentido.

### Puertas, por exit code, en el clon limpio de `bb419bc0`

| Gate | Corridas | Exit |
|---|---|---|
| `python scripts/test_commit_msg_hook.py` | 2 | 0, 0 |
| `python scripts/test_precommit_hook.py` | 2 | 0, 0 |
| `python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py` | 2 | 0, 0 |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | 1 | 0 |
| `python scripts/scan_encoding.py --root .` | 1 | 0 |
| `python scripts/scan_domain_neutrality.py --root .` | 1 | 0 |
| `python scripts/validate_collaboration_state.py --root .` | 1 | 0 |
| Paso 4 de CI (pin AC8 + negativo AC9), ejecutado a mano | 1 | 0 |

DECISION-0115: los tres instrumentos que acreditan el AC de r5 (`test_commit_msg_hook.py`,
`test_precommit_hook.py`, `run_hook_fullmode_inventory_cases.py` -- el paso 10 que el maker cita)
se corrieron **dos veces cada uno**; el resto, una. El pin declarado en
`.github/workflows/validate.yml` (`1bcc0b5b90ae07b0c1044deb24a9404273451565acbbe40ba6202daaf2825c4d`)
casa byte a byte con el `sha256sum` del gancho entregado, y su negativo (gancho perturbado, pin
intacto) dice `FAILED ... did NOT match` y devuelve el `PIN_MISMATCH_NEGATIVE PASS`. `bb419bc0` no
toca `.githooks/pre-commit` ni el workflow, asi que AC8/AC9 quedan intactos.

Estado protocolar: `validate_collaboration_state.py` exit 0 tanto en el arbol vivo como en el clon
limpio del ancla. Drift no medido aparte: el validador es el gate canonico y sale verde.

---

## 2. Que hizo la entrega, medido

`bb419bc0` borra la funcion `claim_gate_applicable()` y **las dos ramas de produccion** que la
consultaban: el `if claim_gate_applicable(root):` que envolvia las tres aserciones de claim en
`validate()`, y el `if not claim_gate_applicable(root): return 0` de `main()` en modo
`--pre-commit`. Retira ademas dos pruebas: la asercion directa en `test_commit_msg_hook.py` y el
self-mutant de `run_hook_fullmode_inventory_cases.py`. Corrige el texto de la tarea (R4-3).

Censo del arbol en `bb419bc0`: **cero referencias vivas** a `claim_gate_applicable` en codigo; solo
prosa en `Area_comun/artifacts/`, `mailbox/` y memorias personales. Ningun contrato de falsacion
declaraba el caso retirado (`check_falsification_contracts --inventory` exit 0 y sin menciones).

---

## 3. Vector a vector

| Vector pedido | Metodo | Resultado |
|---|---|---|
| V1 -- queda ALGUN negativo capaz de enrojecer por conducta? | bateria de mutacion sobre PRODUCCION en clon limpio | **PASS** |
| V2 -- la rama estaba muerta de verdad, o solo para el fixture? | censo diferencial VIEJO vs NUEVO, 25 entradas | **PASS** |
| V3 -- lo retirado cubria comportamiento vivo? | censo + mutacion de los hermanos supervivientes | **PASS** |
| V4 -- el especimen vivo acredita r5? | control historico sobre la misma forma de rechazo | **SLIPS** (ver 3.4) |

### 3.1 V1 -- el discriminante NO se perdio (bateria de mutacion, produccion mutada)

Muto `scripts/check_commit_trailers.py` dentro de un clon limpio de `bb419bc0` y corro las suites
supervivientes. Se muta **produccion**, no al runner.

| Mutante | `test_commit_msg_hook` | `test_precommit_hook` | Veredicto |
|---|---|---|---|
| M0 CONTROL sin mutar | 0 | 0 | VERDE (control) |
| M1 `claim_state` devuelve siempre `owned` (gate desarmado) | 1 | 1 | **MUERE** |
| M2 acepta el claim de OTRO actor | 1 | 1 | **MUERE** |
| M3 elimina el rechazo por claim ausente | 1 | 1 | **MUERE** |
| M4 escape fail-open **ALCANZABLE** en la posicion exacta borrada | 0 | 1 | **MUERE** |
| M5 restaura el codigo BORRADO **verbatim** (funcion + dos ramas) | 0 | 0 | SOBREVIVE |

**M4 contra M5 es el 2x2 que responde su pregunta.** En la misma posicion del codigo:

- si el escape es **alcanzable**, la suite lo mata (M4);
- si el escape es el que se borro, **nada cambia** (M5 sobrevive).

Luego "MUTANT B queda identico a produccion" **prueba que la rama estaba muerta**; no significa que
el negativo haya dejado de poder enrojecer. Lo que se perdio no era un discriminante: el self-mutant
retirado preguntaba `m.claim_gate_applicable(cwd)` al **modulo mutado**, nunca al veredicto de
produccion, y su exit 1 lo producian igual un error de sintaxis o la ausencia de la funcion. Era un
verde por construccion. Los negativos que si discriminan siguen vivos y siguen diciendo que no:

    COMMIT_MSG_REJECTION exit=1: ... TASK-0278 has no active claim covering every staged product path
    COMMIT_MSG_REJECTION exit=1: ... TASK-0279 is covered by an active claim owned by another actor
    PRE_COMMIT_REJECTION_NO_CLAIM exit=1: ... no active claim covers every staged product path
    PRE_COMMIT_REJECTION_OTHER_CLAIM exit=1: ... active claim is owned by another actor

### 3.2 V2 -- la rama estaba muerta para TODA entrada, no solo para el fixture

Censo diferencial: para cada entorno y cada modo, corro el gate **VIEJO** (`bb419bc0^`) y el
**NUEVO** (`bb419bc0`) sobre el mismo estado de repositorio y comparo `(exit, primera linea de
stderr)`.

| Familia | Casos | DIFFER |
|---|---|---|
| Produccion alcanzable: los 4 casos del AC1 en los DOS ganchos, id desconocido, gobernado-no-producto, `runtime/state/` solo, prefijo `Aegis/` no vacio | 15 | 0 |
| Entornos construidos para que `claim_gate_applicable` devolviera **False**: gate fuera de todo repo; gate dentro de `.git/`; `core.bare=true`; repo bare; `git` ausente del PATH -- en los dos modos | 10 | 0 |
| **TOTAL** | **25** | **0** |

Las 10 entradas de la segunda familia mueren todas con exit 1 en **ambas** versiones.

**La causa, medida y no leida:** el que domina es `instance_context()`. Su
`git rev-parse --show-toplevel` falla exactamente en los entornos donde `--is-inside-work-tree` no
es `"true"`, y su `CalledProcessError` no esta capturado -> traceback -> exit 1 -> los dos ganchos
rechazan. Dato que corrige una intuicion facil y equivocada: **`git diff --cached` NO domina** --
medido, devuelve exit 0 dentro de `.git/`, con `core.bare=true` y en un repo bare. El unico
cuello es `instance_context()`.

### 3.3 En que DIRECCION apuntaba la rama borrada (medicion extra)

La pregunta "y si algun dia se levanta el guardia?" es contestable: levanto el guardia en **ambas**
versiones (hago `instance_context()` tolerante, que es justo la tolerancia que la tarea difiere) y
mido.

| Escenario, con el guardia LEVANTADO | VIEJO | NUEVO |
|---|---|---|
| `core.bare=true` / `--pre-commit` | **0 (ACEPTA)** | 1 (rechaza: actor no disponible) |
| `core.bare=true` / commit-msg | **0 (ACEPTA)** | 1 (rechaza: actor no disponible) |
| dentro de `.git/` / `--pre-commit` | **0 (ACEPTA)** | 1 (rechaza: actor no disponible) |
| dentro de `.git/` / commit-msg | **0 (ACEPTA)** | 1 (rechaza: actor no disponible) |

**4 de 4 vuelcos.** La rama borrada era un escape **fail-open**. Su borrado es monotono en la
direccion segura: solo puede convertir aceptaciones en rechazos, jamas al reves. No existe entrada
en la que r5 debilite el gate; el unico coste concebible seria un rechazo falso, y las 25 entradas
del censo muestran que no lo hay.

Observacion de registro (NO defecto): el texto nuevo de la tarea dice que una tolerancia futura en
`instance_context()` "podria abrir el claim gate". Medido en los dos sabores que probe, hoy pasa lo
contrario -- con la rama fuera, la tolerancia hace **rechazar**. La frase sigue siendo una cautela
defendible (otra implementacion de la tolerancia podria dejar `staged_product` vacio y aceptar), asi
que no la marco como falsa; la dejo anotada con la medicion al lado.

### 3.4 V4 -- el especimen vivo NO acredita r5 (y usted pidio que lo dijera)

Su pregunta: el rechazo que sufrio anoche, lo produce `bb419bc0` o lo habria producido igual el
codigo anterior? **El anterior tambien.** Son los casos C1 (commit-msg) y C9 (pre-commit) del censo:
producto staged, sin claim que cubra las rutas para el actor de commit -> exit 1 con el **mismo**
mensaje en `bb419bc0^` y en `bb419bc0`.

El especimen es un positivo real y valioso **de la tarea** -- el gate identifico al actor de commit
y le nego firmar rutas de producto ajenas, sobre un caso de campo y no un fixture -- pero acredita
la linea r2/r3, no esta entrega. Citarlo como evidencia de r5 seria un verde que el codigo viejo
tambien produce.

### 3.5 V3 -- lo retirado no cubria comportamiento vivo

La linea retirada de `test_commit_msg_hook.py` era
`assert gate.claim_gate_applicable(outside_repo) is False`: probaba **solo** la funcion borrada. Sus
dos hermanas siguen en el fichero y siguen siendo discriminantes: mutar el nucleo fail-closed
(`claim_state`: `actor is None -> "owned"`, mutante M7) **muere** en `test_commit_msg_hook.py`
(exit 1).

---

## 4. Cambios de texto (R4-3)

La frase medida como falsa ("...y exige que la misma corrida falle") desaparece, y la imputacion del
verde del paso 10 se corrige a lo que esta medido: el caso sigue verde **por la identidad Git que
configura el arnes** (`git config user.name Codex` mas un claim propio activo en el fixture), no por
la exencion eliminada. Verificado contra el diff y contra el arnes.

---

## 5. Tabla PASS / SLIPS

| # | Criterio | Evidencia | Estado |
|---|---|---|---|
| 1 | R4-1: se borra `claim_gate_applicable` y sus DOS ramas de produccion | diff de `bb419bc0`; censo: 0 referencias vivas | **PASS** |
| 2 | El borrado no cambia el veredicto de produccion para NINGUNA entrada | censo diferencial 25/25 SAME, DIFFER=0 | **PASS** |
| 3 | Sigue existiendo un negativo que MATA por conducta | M1-M4 mueren; 4 rechazos ejecutados con exit 1 | **PASS** |
| 4 | El borrado no debilita el gate | 4/4 vuelcos: la rama era fail-open; borrado monotono seguro | **PASS** |
| 5 | Lo retirado no cubria comportamiento vivo | hermanos supervivientes matan M7; ningun contrato lo declaraba | **PASS** |
| 6 | R4-3: texto corregido | diff del `.md` de la tarea | **PASS** |
| 7 | `instance_context()` sin tocar | diff: no aparece | **PASS** |
| 8 | AC8/AC9 (pin + negativo) intactos | pin casa; paso ejecutado exit 0 | **PASS** |
| 9 | Puertas verdes en clon limpio por exit code | tabla seccion 1 | **PASS** |
| 10 | El especimen vivo acredita **r5** | control historico: el codigo viejo produce el mismo rechazo | **SLIPS** (no es AC; ver 3.4) |

---

## 6. Residuo declarado -- misma familia, otra capa (NO bloquea el cierre)

`commit_actor()` conserva el ultimo fragmento de la familia que r5 acaba de borrar:

    if inside_work_tree != "true":
        return None

Medido: el mutante **M6** (quitar ese guardia) **SOBREVIVE** las dos suites. La razon es la que
importa: fuera de un repo el `git rev-parse` **lanza excepcion** y el camino `except` ya devuelve
`None`, asi que la asercion `commit_actor(outside_repo) is None` pasa **por otro motivo** que la
rama que dice probar. Esa rama solo es alcanzable dentro de `.git/` o con `core.bare=true` -- es
decir, exactamente la familia que `instance_context()` bloquea hoy.

Por que NO abro una sexta vuelta con esto, como usted pidio que decidiera: (a) `bb419bc0` no toca
`commit_actor`, (b) esta fuera del alcance de producto declarado, (c) es la **misma capa del mismo
defecto** que r5 cierra. Debe viajar con la tarea aparte de la tolerancia de `instance_context()`:
el dia que esa tolerancia aterrice, este fragmento pasa de muerto a alcanzable y entonces si hay que
poder falsarlo. Escalacion suya al Operador, no remediacion mia.

---

## 7. Recomendacion de cierre

**OK-CERRABLE.** r5 entrega lo que R4-1 pedia, no cambia el veredicto de produccion para ninguna de
las 25 entradas del censo, y el discriminante de la posicion sigue vivo (M4 muere). El borrado es
monotono hacia fail-closed. Las puertas del alcance declarado salen verdes por exit code en clon
limpio, con las dos que acreditan el AC corridas dos veces.

Dos cosas que le pertenecen a usted, no a Codex: el especimen vivo **no** acredita esta entrega
(seccion 3.4) y el residuo de `commit_actor` (seccion 6) es de la capa que ya decidio diferir.

-- Analista
