---
artifact_id: ANALISTA-TASK-0325-early-exit-r2-verdict
task_id: TASK-0325
type: artifact
owner: Analista
reviewer: Analista
status: done
created_at: 2026-08-07
project: multi_agent_project_protocol
relates_to:
  - TASK-0317
  - TASK-0322
  - TASK-0332
  - SPEC-MEMORIA-HIBRIDA
context_refs:
  - Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md
  - Area_comun/mailbox/open/MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0325-r2.md
---

# Veredicto Analista -- TASK-0325 r2: la guarda de salida temprana acotada al bucle externo

**Recomendacion de cierre: CHANGE-REQUIRED** (iteracion 2 de las 2 que fije; la ultima antes de
escalar al operador humano). Sigue sin tocar produccion.

Empiezo por lo que si esta bien, porque es la mayor parte: **la remediacion fue a la columna
correcta**. Las cuatro filas que fije en r1 salen exactamente como pedi, medidas con mis mutantes
sobre produccion en clon limpio, no leidas del handoff. El foco de verdad vacia que el Arquitecto
anadio sobre el visitante nuevo queda **REFUTADO** con ocho mutaciones: el contrato falla cerrado en
las ocho. El id y el negativo declarado ya nombran la propiedad. AC4 sin regresion.

Lo que bloquea el cierre es **un escape nuevo, de la misma familia y con la misma consecuencia**: el
visitante salta el nodo del bucle anidado **completo, incluido su `else`**. Un `break` en el `else`
de un bucle anidado **no lo re-vincula el bucle anidado: lo posee el bucle externo**. Lo verifique en
Python y lo verifique contra el gate: ese `break` es **funcionalmente identico a E1** -- el mismo
email y el mismo telefono se cuelan por `contains_pii` -- y **pasa el contrato en verde**.

No es un poste movido. Es la propiedad que la propia entrega declara en el fichero de tarea:

> "no early exit **owned by the outer** `contains_pii` item loop ... while ignoring control flow
> **rebound by nested** `For`/`AsyncFor`/`While` nodes"

El `else` de un bucle anidado no es control de flujo re-vinculado. La entrega implementa "salta el
nodo anidado", que no es lo mismo que "ignora lo que el nodo anidado re-vincula".

El arreglo son **seis lineas** dentro del mismo fichero de test, **ya verificado por mi**: recorrer
`node.orelse` en `visit_For`/`visit_AsyncFor`/`visit_While` en vez de `return None`. Con el, las
nueve filas de la matriz salen correctas.

## Anclaje canonico

| Elemento | Valor |
|---|---|
| Repo | `multi_agent_project_protocol` (hub). **SIN PRODUCTO EN ALCANCE** -- ningun `npm test` de Nova/Zeus |
| Commit revisado | `21d1287076094d386188a48bff436e88d0d50eb5` (el citado en la instruccion) |
| `origin/main` al abrir | `b33bd86b`; `git merge-base --is-ancestor 21d12870 origin/main` exit **0** |
| Clones limpios | `D:/Aegis_Scratch/map/r0325r2` (matriz de mutantes) y `.../r0325r2b` (suite completa), ambos detached en `21d12870`, `git status --short` vacio |
| Estado canonico previo | `validate_collaboration_state.py` exit **0** en el arbol vivo antes de empezar |
| `build_memory_db.py` | sha256[:16] `5b49ffe9e5eb5180`; restaurado byte-identico tras cada mutante (verificado por hash en cada driver) |
| Hora local | 2026-08-07 17:52 (UTC+2) |

Todos los mutantes se aplicaron **a produccion dentro del clon** y se restauraron; cada driver
comprueba el hash al terminar y `git status --short` del clon sale vacio.

## Reproduccion (todo por exit code, en clon limpio)

| Comando | Exit | Evidencia |
|---|---|---|
| `python scripts/memory/test_memory_db.py` (suite completa, sin mutar) | **0** | `Ran 66 tests in 225.342s ... OK` |
| `python scripts/memory/test_memory_db.py` **con E1 aplicado a produccion** | **1** | `FAILED (failures=1)` -- **el cambio que pedi: en r1 salia verde** |
| `python scripts/memory/test_memory_db.py` **con N1 aplicado a produccion** | **0** | `Ran 66 tests ... OK` -- **el escape nuevo, suite entera en verde** |
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** | 44 DECLARED; `NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT boundaries=4 runner=scripts\memory\test_memory_db.py` |
| `python scripts/validate_collaboration_state.py` | **0** | `OK: collaboration state is valid` |
| `python scripts/scan_encoding.py` | **0** | limpio |
| `python scripts/scan_domain_neutrality.py` | **0** | limpio |
| AC4 dirigido (4 tests de 0317/0322/0325) | **0** | `Ran 4 tests ... OK` |

Runner realmente **ejecutado** por CI, no solo declarado: `.github/workflows/validate.yml:49`
invoca `python scripts/memory/test_memory_db.py` (comprobado otra vez por la leccion de TASK-0330).

## Punto 1 -- mi tabla de cuatro filas, con mis mutantes sobre produccion

Contrato aislado (`MemoryDbTests.test_contains_pii_item_loop_has_no_early_exit`), un mutante por
corrida, produccion restaurada entre corridas:

| Mutante aplicado a produccion | Exit | Resultado | Pedido en r1 |
|---|---|---|---|
| fuente sin mutar | 0 | PASS | PASS |
| **E1 -- `break` estrecho `+05:45` (la fuga real)** | **1** | **CATCH** | CATCH |
| E0 -- `continue` estrecho `+05:45` (vector de r1) | 1 | CATCH | CATCH |
| `break` inocuo en el bucle interno del telefono | 0 | PASS | PASS |
| `continue` inocuo en el bucle interno del telefono | 0 | PASS | PASS |

**Las cuatro filas correctas.** SLIP-0325-1 y SLIP-0325-2 de mi veredicto de r1 quedan **cerrados**.

## Punto 2 -- la suite completa con E1 aplicado a produccion sale ROJA

`Ran 66 tests ... FAILED (failures=1)`, **exit 1**. En r1 esa misma mutacion daba
`Ran 64 tests ... OK` exit 0. Este es el cambio que decide el punto 2 y **esta cumplido**.

## Punto 3 -- AC4 sin regresion

| Vector | Resultado |
|---|---|
| `test_timestamp_pii_suffix_is_rejected` (11 vectores de sufijo) | **PASS** |
| `test_timestamp_exemption_is_phone_only_and_falsifiable` (familia de 333) | **PASS** |
| `test_valid_offset_complement_is_falsifiable` (los cuatro offsets) | **PASS** |
| `test_timestamp_ranges_reject_syntactic_non_dates` | **PASS** |
| Suite completa sin mutar | **PASS** (66 tests, exit 0) |

Exit **0** en los cuatro dirigidos y en la suite. Sin regresion.

## Punto 4 -- el id y el negativo nombran la propiedad

| Antes | Ahora |
|---|---|
| `NEG-MEMORY-DATE-EXEMPTION-NO-CONTINUE` | `NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT` |
| "An early **continue** in the contains_pii item loop bypasses later checks." | "An early **exit** from the contains_pii item loop bypasses later **PII** checks." |
| 2 boundaries | 4 boundaries |
| `exercised_by: ..._has_no_early_continue` | `exercised_by: ..._has_no_early_exit` |

Inventario exit **0**, `boundaries=4`, runner declarado y ejecutado. Barri el arbol buscando
referencias colgadas al id viejo: **cero en codigo, CI o contratos**. Las tres que quedan son
registros historicos correctos (el handoff de 0325, un mensaje ya archivado y la memoria de Codex),
no declaraciones vivas. **Cumplido**, y con la propiedad nombrada -- que era el punto.

## El foco que anadio el Arquitecto -- verdad vacia sobre el visitante nuevo: **REFUTADO**

Su pregunta literal: *"Si el visitante nuevo dejara de encontrar el bucle externo, el contrato falla
o devuelve lista vacia y pasa en verde?"*

**Falla.** Lo probe por los dos lados, ocho mutaciones, y ninguna pasa en verde.

Lado test (rompo el visitante y dejo produccion intacta):

| Mutacion del visitante | Exit | Resultado |
|---|---|---|
| T1 -- `visit_Break` no recoge nada | **1** | falla cerrado |
| T2 -- `visit_Continue` no recoge nada | **1** | falla cerrado |
| T3 -- se entra al visitante por el nodo del bucle (`visit_For` se lo come todo) | **1** | falla cerrado |
| T4 -- el visitante no recorre nada (arbol vacio) | **1** | falla cerrado |

Lado produccion (el bucle externo deja de ser localizable):

| Mutacion de produccion | Exit | Resultado |
|---|---|---|
| A1 -- el bucle se elimina (cuerpo recto) | **1** | falla cerrado |
| A2 -- `contains_pii` renombrada + alias publico | **1** | falla cerrado |
| A4 -- el bucle envuelto en un `if` (deja de ser hijo directo) | **1** | falla cerrado |
| A5 -- aparece un segundo bucle directo de items | **1** | falla cerrado |

La razon es estructural y vale la pena dejarla escrita: el contrato no solo afirma la lista vacia
sobre la fuente; **tambien afirma que los mutantes producen lista NO vacia**
(`assertNotEqual([], mutant_break_early_exits)`). Un visitante que deje de encontrar cosas rompe esa
segunda afirmacion. Las dos direcciones juntas son lo que cierra la familia. Bien construido.

## El bloqueo: SLIP-0325-3, el `else` del bucle anidado

### La semantica

En Python, un `break` en la clausula `else` de un bucle anidado **se vincula al bucle externo**.
Comprobado antes de acusar:

```python
for i in [1, 2, 3]:
    for _n in ():
        pass
    else:
        if i == 2:
            break        # rompe el bucle EXTERNO
    out.append(i)
# out == [1]
```

El visitante entregado hace `visit_For -> return None`: salta el nodo `For` anidado **entero**,
`orelse` incluido. Por tanto no ve ese `break`, que si pertenece al bucle externo.

### La fuga, demostrada por comportamiento

N1 = el mismo bypass estrecho de E1, movido dentro del `else` de un bucle anidado vacio (que
siempre se ejecuta, porque el cuerpo del bucle nunca corre):

```python
        for _nested in ():
            pass
        else:
            if DATE_RE.fullmatch(item) and item.endswith("+05:45"):
                break
        normalized = re.sub(r"[_/\\.-]+", " ", item)
```

`contains_pii` medido cargando cada variante como modulo aislado:

| Entrada | fuente | E1 (`break` directo) | **N1 (`break` en `else` anidado)** | N2 (`continue` en `while ... else`) |
|---|---|---|---|---|
| `"2026-06-19T09:28:23+05:45"` con termino de dominio `2026` | True | False | **False** | False |
| `["2026-06-19T09:28:23+05:45", "contact me at a@b.com"]` | True | False | **False** | True |
| `["2026-06-19T09:28:23+05:45", "+34 600 123 456"]` | True | False | **False** | True |
| `["a@b.com"]` (control, sin fecha) | True | True | **True** | True |

**N1 es indistinguible de E1 en comportamiento**: el email y el telefono se cuelan por el gate de
PII exactamente igual. Y la diferencia decisiva contra el gate:

| Variante en produccion | Contrato AST | Suite completa |
|---|---|---|
| E1 | **exit 1 (CATCH)** | **exit 1 (RED)** |
| **N1** | **exit 0 (PASS -- hueco)** | **exit 0 (`Ran 66 tests ... OK`)** |
| N2 | exit 0 (PASS -- hueco) | no medida (mismo mecanismo) |

Un mutante con la misma consecuencia de PII que el que la tarea acaba de clavar **pasa los 66 tests
en verde**. Eso es lo que no puedo firmar como cerrado.

### Lo que el visitante SI acierta (para acotar el defecto, que es pequeno)

Probe el resto de la familia para no exagerar el alcance. El defecto es **uno solo**:

| Mutante en produccion | Exit | Correcto? |
|---|---|---|
| S1 -- `break` en `try/finally` (lo posee el externo) | 1 CATCH | si |
| S2 -- `break` en un `with` (lo posee el externo) | 1 CATCH | si |
| S3 -- `break` en `match/case` (lo posee el externo) | 1 CATCH | si |
| S4 -- `continue` en un `def` anidado (re-vinculado) | 0 PASS | si |
| N3 -- `break` inocuo en el cuerpo de un bucle anidado | 0 PASS | si |
| N4 -- `break` inocuo dos niveles hacia abajo | 0 PASS | si |
| **N1 -- `break` en el `else` de un `for` anidado** | **0 PASS** | **NO** |
| **N2 -- `continue` en el `else` de un `while` anidado** | **0 PASS** | **NO** |

`generic_visit` cubre bien `If`/`Try`/`With`/`Match`. La unica arista mal cortada es el `orelse` de
los tres tipos de bucle.

## Tabla vector-por-vector

| # | Vector / criterio | Resultado |
|---|---|---|
| P1 | Cuatro filas de r1 con mis mutantes (E1 CATCH, E0 CATCH, dos inocuos PASS) | **PASS** |
| P2 | Suite completa con E1 en produccion sale ROJA | **PASS** (exit 1; en r1 era 0) |
| P3 | AC4 sin regresion (11 sufijos + familia 333 + cuatro offsets) | **PASS** (exit 0) |
| P4 | Id y negativo declarado nombran la propiedad; cero referencias colgadas vivas | **PASS** |
| F1-F4 | Verdad vacia, lado test (visitante roto en cuatro formas) | **PASS** (falla cerrado 4/4) |
| F5-F8 | Verdad vacia, lado produccion (bucle no localizable: A1/A2/A4/A5) | **PASS** (falla cerrado 4/4) |
| C1 | `build_memory_db.py` byte-identico y restaurado tras cada mutante | **PASS** (hash verificado) |
| S1-S4 | `try` / `with` / `match` / `def` anidado bien clasificados | **PASS** (4/4) |
| N3-N4 | Bucles anidados: inocuos no producen falso positivo | **PASS** |
| G | Gates protocolarios (validate / encoding / neutralidad / inventario) | **PASS** (exit 0) |
| G2 | Runner ejecutado por CI, no solo declarado | **PASS** (`validate.yml:49`) |
| **S3-NUEVO** | **`break`/`continue` en el `else` de un bucle anidado: fuga real, suite 66/66 verde** | **SLIP-0325-3** |

## Remediacion pedida (iteracion 2, cero codigo de produccion)

Seis lineas en `scripts/memory/test_memory_db.py`, dentro de `OuterLoopControlFlow`: en vez de
saltar el nodo del bucle anidado completo, saltar **solo su cuerpo** y seguir por su `orelse`.

```python
                def _nested_loop(self, node) -> None:
                    for statement in node.orelse:
                        self.visit(statement)

                def visit_For(self, node: ast.For) -> None:
                    self._nested_loop(node)

                def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
                    self._nested_loop(node)

                def visit_While(self, node: ast.While) -> None:
                    self._nested_loop(node)
```

Y anadir N1 y N2 a las fronteras del contrato, con el mismo patron que ya usan `mutant_break` y
`nested_break`, para que el escape quede clavado por mutacion y no por lectura.

**Este arreglo ya lo verifique yo**, aplicandolo al test en el clon y re-corriendo la matriz entera
sobre produccion. Nueve de nueve filas correctas, sin falsos positivos nuevos:

| Mutante en produccion | Exit con el arreglo | Quiero |
|---|---|---|
| fuente sin mutar | 0 PASS | PASS |
| E0 `continue` directo | 1 CATCH | CATCH |
| E1 `break` directo | 1 CATCH | CATCH |
| **N1 `break` en `for ... else` anidado** | **1 CATCH** | CATCH |
| **N2 `continue` en `while ... else` anidado** | **1 CATCH** | CATCH |
| N3 `break` inocuo en cuerpo anidado | 0 PASS | PASS |
| N4 `break` inocuo dos niveles abajo | 0 PASS | PASS |
| I1 `break` inocuo en bucle del telefono | 0 PASS | PASS |
| I2 `continue` inocuo en bucle del telefono | 0 PASS | PASS |

No estoy pidiendo un diseno: estoy entregando el parche medido. Si Codex lo escribe distinto, lo
que exijo es la tabla de nueve filas, no la forma.

**Gates afectados:** `python scripts/memory/test_memory_db.py` (exit 0) y
`python scripts/check_falsification_contracts.py --root . --inventory` (exit 0). `build_memory_db.py`
sigue sin tocarse.

**Falsacion que exijo en la re-entrega** (la corro yo):

- Las nueve filas de arriba, mutantes sobre produccion, un mutante por corrida.
- La suite completa **con N1 aplicado a produccion debe salir ROJA** (hoy sale
  `Ran 66 tests ... OK`). Ese es el numero que decide, igual que E1 lo fue en esta vuelta.
- AC4 sin regresion otra vez: 11 sufijos + familia de 333 + cuatro offsets, exit 0.
- El negativo declarado debe seguir nombrando la propiedad y sumar las fronteras nuevas.

**Bucle de fix:** remediacion -> re-juicio mio **antes** del commit de cierre. Esta es la
**iteracion 2 de 2**. Si a la tercera vuelta sigue habiendo un escape de la misma familia,
**escalo al operador humano** en vez de pedir una cuarta.

## Residuales declarados (no bloquean, y no los cuento contra este cierre)

- **R0325-1 y R0325-2** -- ya contratados como **TASK-0332** con GO del operador y contrato **por
  comportamiento**. No los reabro. **Aviso de alcance para quien escriba 0332:** SLIP-0325-3 **no**
  esta cubierto por R0325-1. R0325-1 habla de *reestructuracion* y *filtrado en un helper externo*,
  formas que no usan `break`/`continue`. N1 **es** un `break`, de la clase exacta que la guarda
  enumera, en el nivel de bucle exacto que la guarda dice acotar. Es un defecto de la guarda, no una
  limitacion del AST. Si se cerrara 0325 dejandolo a 0332, quedaria un hueco sin dueno.
- **R0325-3** (heredado de 0322): `DATE_RE` usa `\d` sin `re.ASCII`. No lo reabro aqui.
- **R0325-4 (nuevo, informativo, no bloqueante).** El visitante recorre `(*loop.body, *loop.orelse)`
  del bucle **externo**. Un `break` en el `orelse` del bucle externo se vincularia a un bucle que lo
  encierre, no a el; recogerlo ahi es conservador y hoy es inalcanzable (`contains_pii` no anida el
  bucle de items). Lo dejo escrito para que un refactor futuro no lo lea como intencional.

## Conclusion

La remediacion hizo lo que le pedi y lo hizo bien: fue a la columna acotada, mato E1 en la suite
completa, no rompio AC4, dejo produccion byte-identica y renombro el negativo a la propiedad. El
visitante nuevo, ademas, **no admite verdad vacia** en ninguna de las ocho formas en que intente
apagarlo, y clasifica correctamente `try`/`with`/`match`/`def` anidado. Es trabajo solido.

Pero el corte del nodo anidado se hizo por **nodo** y no por **vinculacion**, y eso deja el `else`
de los bucles anidados fuera del radar. Por ese hueco entra un mutante **funcionalmente identico a
E1** -- el mismo email y el mismo telefono colandose por el gate de PII -- **con los 66 tests en
verde**. Es exactamente el mismo criterio con el que bloquee r1, aplicado con la misma vara.

**CHANGE-REQUIRED.** Si el Arquitecto juzga que seis lineas no valen una tercera vuelta, la
alternativa disciplinada es cerrar en OK-CLOSABLE **registrando SLIP-0325-3 como residual de
severidad bloqueante con dueno y tarea propia**, nunca como observacion, y **explicitando que
TASK-0332 no lo cubre**. Mi recomendacion es arreglarlo ahora: el parche esta medido, son seis
lineas, esta dentro del fichero que la tarea ya toco y produccion no se mueve.

-- Analista
