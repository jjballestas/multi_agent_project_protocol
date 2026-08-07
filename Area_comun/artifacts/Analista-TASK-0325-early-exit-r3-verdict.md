---
artifact_id: ANALISTA-TASK-0325-early-exit-r3-verdict
task_id: TASK-0325
type: artifact
owner: Analista
reviewer: Analista
status: done
created_at: 2026-08-08
project: multi_agent_project_protocol
relates_to:
  - TASK-0317
  - TASK-0322
  - TASK-0327
  - TASK-0332
  - SPEC-MEMORIA-HIBRIDA
context_refs:
  - Area_comun/artifacts/Analista-TASK-0325-early-exit-r2-verdict.md
  - Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md
  - Area_comun/mailbox/open/MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0325-r3.md
---

# Veredicto Analista -- TASK-0325 r3: el corte por vinculacion

**Recomendacion de cierre: OK-CLOSABLE.** Iteracion 2 de 2. No pido una tercera vuelta.

La remediacion hace exactamente lo que pedi y lo hace por la razon correcta: el corte pasa de ser
por **nodo** a ser por **vinculacion**. SLIP-0325-3 queda **cerrado**, medido con mis mutantes sobre
produccion en dos clones limpios. Las nueve filas salen nueve de nueve. El numero que decidia esta
vuelta -- la suite completa con N1 aplicado a produccion -- pasa de `Ran 66 tests ... OK` (r2) a
**exit 1** ahora. N1 y N2 estan **clavadas por mutacion**, no verificadas de paso: al revertir
`_nested_loop` a su forma de r2 el contrato se pone rojo. R0325-4 esta declarado y ademas he
verificado que su afirmacion de inalcanzabilidad es cierta. Produccion no la toca el commit de
remediacion.

Traigo dos cosas que el Arquitecto debe leer antes de cerrar, ninguna bloqueante:

1. **Una correccion al anclaje.** "Produccion sigue byte-identica" es cierto del commit de
   remediacion, pero **no** respecto a mi ancla de r2: `fef3f6b7` (TASK-0327) movio
   `build_memory_db.py` en medio. Por eso he re-medido **todo** sobre la produccion actual y no he
   reutilizado ni una cifra de r2.
2. **Un escape nuevo, SLIP-0325-4, que NO bloquea esta tarea y SI tiene que quedar con dueno**: un
   `return` falsy estrecho en el bucle de items filtra el mismo email y el mismo telefono que E1 y
   **pasa la suite entera en verde**. No lo cuento contra 0325 porque no es la clase que la guarda
   enumera y porque la guarda **no puede** cubrirlo sin analisis de valor (produccion tiene cuatro
   `return True` legitimos en ese mismo bucle). Cae del lado de R0325-1 y ya tiene dueno: **TASK-0332**,
   cuyo AC3 y AC4 lo nombran. Es evidencia a favor de la tesis de 0332, no un defecto de esta entrega.

## Anclaje canonico

| Elemento | Valor |
|---|---|
| Repo | `multi_agent_project_protocol` (hub). **SIN PRODUCTO EN ALCANCE** -- ningun `npm test` de Nova/Zeus |
| Commit revisado | `7bd785b9817cece8afedbed596e891e938e149f0` (el citado en la instruccion) |
| `origin/main` al abrir | `1c5aa703`; `git merge-base --is-ancestor 7bd785b9 HEAD` exit **0** |
| Clones limpios | `D:/Aegis_Scratch/map/r0325r3` (suites completas) y `D:/Aegis_Scratch/map/r0325r3b` (matriz, sondas y gates), ambos detached en `7bd785b9`, `git status --short` vacio al abrir y al cerrar |
| Estado canonico previo | `validate_collaboration_state.py` exit **0** en el arbol vivo antes de empezar |
| `build_memory_db.py` en el ancla | sha256[:16] **`b42257a39d4faa62`** (en r2 era `5b49ffe9e5eb5180`; ver correccion abajo) |
| `test_memory_db.py` en el ancla | sha256[:16] `3ea25fda4de0c845` |
| Hora local | 2026-08-08 01:16 (UTC+2) |

**Metodo.** Todos los mutantes se aplican **a produccion dentro del clon**, uno por corrida, y se
restauran; cada driver comprueba el sha256 al terminar y el `git status --short` del clon sale vacio.
Las corridas de mutacion van **serializadas**: una suite completa mutando produccion en segundo
plano mientras se mide otra cosa en el mismo clon contamina las dos medidas. Por eso hay dos clones y
por eso cada driver afirma que su mutacion **se aplico de verdad** (`assert mutated != source`) antes
de correr; una sonda cuyo ancla no case devuelve verde por no haber mutado nada y se lee como "no hay
fuga".

## Correccion al anclaje: produccion SI se movio desde mi ancla de r2

El commit de remediacion es limpio: `git diff 7bd785b9^ 7bd785b9 -- scripts/memory/build_memory_db.py`
sale **vacio**. Esa parte de la afirmacion es correcta.

Pero entre `21d12870` (mi ancla de r2) y `7bd785b9` hay **un commit que si toca produccion**:

    fef3f6b7  chore(TASK-0327): commitea el trabajo en curso de Codex y secuencia 0330 antes
    -> 41 inserciones / 14 borrados en scripts/memory/build_memory_db.py

Quita el default `= ()` de `domain_pii_terms` en `title_is_safe` y `contains_pii`, y propaga el
parametro por `require_safe_text` y sus llamantes. Lo comprobe antes de acusar de nada: **el AST del
bucle de items es identico** entre las dos anclas, asi que el area que la guarda vigila no cambia y
ninguna de mis conclusiones de r2 sobre la vinculacion se invalida. Lo dejo escrito por dos razones:
la afirmacion "produccion sigue byte-identica" es ambigua sin decir respecto a que, y **AC4 habia que
re-medirlo sobre la produccion nueva**, que es lo que he hecho.

## Reproduccion (todo por exit code, en clon limpio)

| Comando | Exit | Evidencia |
|---|---|---|
| `python scripts/memory/test_memory_db.py` (suite completa, sin mutar) | **0** | `Ran 70 tests in 244.538s ... OK` |
| `python scripts/memory/test_memory_db.py` **con N1 aplicado a produccion** | **1** | `Ran 70 tests ... FAILED (failures=1)` -- **el numero que decidia: en r2 salia 0** |
| `python scripts/memory/test_memory_db.py` **con X1 (`return False`) aplicado a produccion** | **0** | `Ran 70 tests ... OK` -- **SLIP-0325-4** |
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** | 48 DECLARED; `NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT boundaries=6 runner=scripts\memory\test_memory_db.py` |
| `python scripts/validate_collaboration_state.py` | **0** | `OK: collaboration state is valid` |
| `python scripts/scan_encoding.py` | **0** | limpio |
| `python scripts/scan_domain_neutrality.py` | **0** | limpio |
| `python runtime/protocol_replay.py --check-drift --root .` | **0** | `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=7688` |
| AC4 dirigido (4 tests de 0317/0322/0325) | **0** | `Ran 4 tests ... OK` |

Runner realmente **ejecutado** por CI, no solo declarado: `.github/workflows/validate.yml:49` invoca
`python scripts/memory/test_memory_db.py`. Comprobado otra vez por la leccion de TASK-0330: un
recuento del inventario no es cobertura mientras no se vea al runner correr.

## Punto 1 -- la matriz de nueve filas, con mis mutantes sobre produccion

Contrato aislado (`MemoryDbTests.test_contains_pii_item_loop_has_no_early_exit`), un mutante por
corrida, produccion restaurada y verificada por hash entre corridas. Reproducida **dos veces**, en
los dos clones, con resultado identico:

| # | Mutante aplicado a produccion | Exit | Resultado | Pedido |
|---|---|---|---|---|
| 1 | fuente sin mutar | 0 | PASS | PASS |
| 2 | E0 -- `continue` directo | 1 | **CATCH** | CATCH |
| 3 | E1 -- `break` directo | 1 | **CATCH** | CATCH |
| 4 | **N1 -- `break` en `for ... else` anidado** | 1 | **CATCH** | CATCH |
| 5 | **N2 -- `continue` en `while ... else` anidado** | 1 | **CATCH** | CATCH |
| 6 | N3 -- `break` inocuo en cuerpo anidado | 0 | PASS | PASS |
| 7 | N4 -- `break` inocuo dos niveles abajo | 0 | PASS | PASS |
| 8 | I1 -- `break` inocuo en el bucle del telefono | 0 | PASS | PASS |
| 9 | I2 -- `continue` inocuo en el bucle del telefono | 0 | PASS | PASS |

**Nueve de nueve, sin falsos positivos nuevos.** SLIP-0325-3 queda **cerrado**.

## Punto 2 -- el numero que decidia: la suite completa con N1 sale ROJA

En r2, N1 aplicado a produccion daba `Ran 66 tests ... OK`, exit 0: un mutante con la misma
consecuencia de PII que E1 pasaba la suite entera en verde. Ahora:

    Ran 70 tests in 249.057s
    FAILED (failures=1)
    exit 1

Con el fallo en el sitio correcto: `self.assertEqual([], source_early_exits)` de
`test_contains_pii_item_loop_has_no_early_exit`, no un rojo colateral de otro test.

## Punto 3 -- N1 y N2 como FRONTERAS del contrato, no verificadas de paso

Era la pregunta explicita del Arquitecto. La respuesta es si, y la mido rompiendo el test y dejando
produccion intacta. Si N1/N2 fueran decoracion, revertir el visitante dejaria el contrato verde:

| Mutacion del test | Exit | Resultado |
|---|---|---|
| **T5 -- `_nested_loop` vuelve a `return None` (la regresion exacta de r2)** | **1** | **FALLA CERRADO** |
| T6 -- `visit_Break` deja de recoger | 1 | FALLA CERRADO |
| T9 -- `visit_Continue` deja de recoger | 1 | FALLA CERRADO |
| T7 -- el visitante devuelve siempre lista vacia | 1 | FALLA CERRADO |

**T5 es la fila que contesta la pregunta.** Es el mutante de la clase que importa aqui: no borra el
cableado, lo deja **inalcanzable** -- el metodo sigue existiendo, sigue llamandose desde
`visit_For`/`visit_AsyncFor`/`visit_While`, y solo su cuerpo se vacia. Ese es exactamente el mutante
que un contrato que solo comprobara `assert linea in source` dejaria pasar. Este no lo deja pasar:
`nested_else_break_early_exits` se queda vacia y `assertNotEqual` revienta. Las dos filas nuevas del
inventario (`boundaries` pasa de 4 a 6) tienen dientes.

## Punto 4 -- la vinculacion, probada en las dos direcciones

No me basta con que N1 y N2 caigan: la remediacion cambio la regla de corte, y una regla de corte
nueva puede abrir falsos positivos por un lado mientras cierra fugas por el otro. Barri la familia
entera de formas de propiedad de control de flujo, mutantes sobre produccion, serializado:

| Sonda | Forma | Exit | Resultado | Correcto? |
|---|---|---|---|---|
| X2 | `break` en el `orelse` de un bucle que vive en el `orelse` de otro anidado | 1 | CATCH | si (lo posee el externo) |
| X3 | `break` inocuo en el **cuerpo** de un bucle que vive en un `orelse` anidado | 0 | PASS | si (lo posee el interno) |
| X4 | `break` inocuo en un `finally` dentro del cuerpo de un bucle anidado | 0 | PASS | si |
| X5 | `break` real en el `orelse` de un bucle anidado envuelto en un `if` | 1 | CATCH | si |
| X6 | `break` real en el `orelse` anidado, envuelto en `try/finally` | 1 | CATCH | si |
| X8 | `break` real via `match/case` dentro del `orelse` anidado | 1 | CATCH | si |
| Y1 | `break` en un bucle **dentro de un `def` anidado** | 0 | PASS | si (re-vinculado) |
| Y1b | `break` en el `orelse` de un bucle dentro de un `def` anidado | 0 | PASS | si (re-vinculado) |
| Y6 | `break` real en el `else` de un `try` del cuerpo externo | 1 | CATCH | si |
| Y7 | `break` real en un `except` handler del cuerpo externo | 1 | CATCH | si |
| Y9 | `break` real en el `finally` de un `try` del cuerpo externo | 1 | CATCH | si |
| Y8 | `continue` real en un `orelse` anidado a dos niveles (`while`/`for`) | 1 | CATCH | si |
| Y10 | `break` inocuo en el `orelse` de un `try` **dentro** del cuerpo de un bucle anidado | 0 | PASS | si |

**Trece de trece.** El corte por vinculacion es correcto en las dos direcciones: no se le escapa
ningun `break`/`continue` que el bucle de items posea, y no reclama ninguno que no le pertenezca. La
arista que en r2 estaba mal cortada es la unica que estaba mal cortada.

(X7, `async for` anidado, no es medible: `contains_pii` es un `def` sincrono y un `async for` ahi es
error de sintaxis. `visit_AsyncFor` es defensivo y hoy inalcanzable. Lo declaro, no lo cuento.)

## Punto 5 -- R0325-4 declarado, y su afirmacion verificada

Esta escrito en el fichero de tarea al commit revisado, y dice lo correcto: el visitante recorre
`(*loop.body, *loop.orelse)` del bucle externo, y un `break` en ese `orelse` externo se vincularia a
un bucle que lo encierre, no al bucle de items.

No me quede en leerlo. **La afirmacion de inalcanzabilidad es comprobable y la comprobe**: hoy no se
puede ni escribir. Anadir un `else: break` al bucle externo de `contains_pii` da
`SyntaxError: 'break' outside loop`, porque el bucle de items no esta anidado dentro de ningun otro.
El recorrido conservador no puede producir un falso positivo mientras eso siga siendo cierto, y la
nota deja avisado a un refactor futuro. **Declarado y correcto.**

## Punto 6 -- AC4 sin regresion, re-medido sobre la produccion nueva

| Vector | Resultado |
|---|---|
| `test_timestamp_pii_suffix_is_rejected` (11 vectores de sufijo) | **PASS** |
| `test_timestamp_exemption_is_phone_only_and_falsifiable` (familia de 333) | **PASS** |
| `test_valid_offset_complement_is_falsifiable` (los cuatro offsets) | **PASS** |
| `test_timestamp_ranges_reject_syntactic_non_dates` | **PASS** |
| Suite completa sin mutar | **PASS** (70 tests, exit 0) |

Exit **0** en los cuatro dirigidos y en la suite. La exencion sigue anclada en `DATE_RE` dentro del
bloque del telefono. Sin regresion, y esta vez sobre la produccion que TASK-0327 dejo.

## SLIP-0325-4 -- el `return` falsy: hallazgo nuevo, y por que NO bloquea

Buscando un escape nuevo lo encontre, y lo declaro falsablemente porque es real.

### La fuga

    if DATE_RE.fullmatch(item) and item.endswith("+05:45"):
        return False

Un `return` falsy estrecho, en el mismo sitio donde iba E1. Medido cargando cada variante como
modulo aislado:

| Entrada | fuente | E1 (`break`) | N1 (`break` en else anidado) | **X1 (`return False`)** |
|---|---|---|---|---|
| timestamp `+05:45` + termino de dominio | True | False | False | **False** |
| timestamp `+05:45` + `"contact me at a@b.com"` | True | False | False | **False** |
| timestamp `+05:45` + `"+34 600 123 456"` | True | False | False | **False** |
| control `["a@b.com"]` (sin fecha) | True | True | True | **True** |

Misma consecuencia exacta que E1: el mismo email y el mismo telefono se cuelan por el gate de PII. Y
contra el gate:

| Variante en produccion | Contrato AST | Suite completa |
|---|---|---|
| E1 | exit 1 (CATCH) | exit 1 (RED) |
| N1 | exit 1 (CATCH) | **exit 1 (RED)** -- arreglado esta vuelta |
| **X1 (`return False`)** | **exit 0 (PASS)** | **exit 0 (`Ran 70 tests ... OK`)** |
| X1b (`return bool(0)`) | exit 0 (PASS) | no medida (mismo mecanismo) |

### Por que NO lo cuento contra TASK-0325

Aplico la misma vara con la que bloquee r2, y esta vez cae del otro lado de la raya que yo mismo
dibuje ahi. En r2 escribi que N1 no estaba cubierto por R0325-1 porque **N1 ES un `break`, de la
clase exacta que la guarda enumera, en el nivel de bucle exacto que la guarda dice acotar**. X1 no es
eso: es una **clase de sentencia distinta**, que la guarda nunca enumero.

Y hay una razon estructural, no de conveniencia: **la guarda no puede cubrirlo sin analisis de
valor.** El bucle de items de `contains_pii` contiene **cuatro `return True` legitimos** que son el
comportamiento correcto y deseado. Un `visit_Return` que recoja returns pondria el contrato en rojo
sobre la fuente limpia. Distinguir `return True` de `return False` exige mirar el valor, y eso se
rompe con `return bool(0)`, `return 1 == 2` o cualquier expresion equivalente. **Mas AST no cierra
esta familia**, que es literalmente la tesis de TASK-0332.

### Quien lo tiene

**TASK-0332**, `ready`, priority high, owner Codex, reviewer Analista, ya con GO. No hace falta abrir
nada: su alcance lo nombra.

- **AC2** exige que el muestreo ejercitado **contra `contains_pii`** cubra el rango de offsets que
  `DATE_RE` acepta, `+05:45` incluido. Ese es el offset de X1.
- **AC3** exige un negativo **por comportamiento**, que no inspeccione el AST y exija la respuesta
  correcta de `contains_pii` con entradas reales. Un contrato asi mata X1: con X1 en produccion,
  `contains_pii(["2026-06-19T09:28:23+05:45", "a@b.com"], [])` devuelve `False` y debe devolver `True`.
- **AC4** nombra explicitamente **"la salida temprana"** entre las tres formas a medir.

Lo que si pido que 0332 no deje pasar en silencio, y lo registro como **R0325-5**: hoy el inventario
declara *"An early exit from the contains_pii item loop bypasses later PII checks"* mientras el
perimetro realmente cableado es `break`/`continue`. Eso es una declaracion que **promete de mas**, y
un agente frio que lea el inventario creera cubierto lo que X1 demuestra que no lo esta. El AC4 de
0332 pide justamente declarar cual contrato mata cada forma y por que: ahi es donde toca **o ensanchar
el perimetro o estrechar la redaccion**. No lo arreglo aqui porque el nombre `NO-EARLY-EXIT` fue una
mejora real de r1 -- nombro la propiedad y por eso `break` entro en la guarda -- y estrecharlo a mano
en la ultima iteracion, sin el contrato por comportamiento delante, cambiaria un texto sin cambiar un
diente.

## Tabla vector-por-vector

| # | Vector / criterio de la instruccion | Resultado |
|---|---|---|
| M1-M9 | La matriz de nueve filas con mis mutantes, dos clones | **PASS** (9/9) |
| D1 | Suite completa con N1 en produccion sale ROJA (en r2 era verde) | **PASS** (exit 1) |
| B1 | N1 y N2 clavadas por mutacion: T5 revierte el visitante y el contrato cae | **PASS** (falla cerrado) |
| B2 | Sin verdad vacia: T6/T9/T7 fallan cerrado | **PASS** (3/3) |
| V1 | Vinculacion correcta en las dos direcciones (X2-X8, Y1-Y10) | **PASS** (13/13) |
| R1 | R0325-4 declarado en el fichero de tarea al commit revisado | **PASS** |
| R2 | La inalcanzabilidad que R0325-4 afirma es cierta (SyntaxError) | **PASS** (verificado) |
| A4 | AC4 sin regresion sobre la produccion nueva | **PASS** (exit 0) |
| I1 | Inventario exit 0, `boundaries` 4 -> 6, runner declarado | **PASS** |
| I2 | Runner realmente ejecutado por CI (`validate.yml:49`) | **PASS** |
| P1 | El commit de remediacion no toca produccion (diff vacio) | **PASS** |
| P2 | "Byte-identica" respecto a mi ancla de r2 | **CORRECCION** -- `fef3f6b7` (TASK-0327) la movio; bucle de items AST-identico; todo re-medido |
| G | Gates protocolarios (validate / encoding / neutralidad / drift) | **PASS** (exit 0, drift CLEAN) |
| **S4** | **`return` falsy estrecho: fuga real, suite 70/70 verde** | **SLIP-0325-4** -- no bloqueante, dueno TASK-0332 |

## Residuales declarados

- **R0325-1 y R0325-2** -- contratados como **TASK-0332** (`ready`, high, owner Codex, reviewer
  Analista). No los reabro.
- **R0325-3** (heredado de 0322): `DATE_RE` usa `\d` sin `re.ASCII`. No lo reabro aqui.
- **R0325-4** -- declarado por la entrega, verificado por mi: hoy inalcanzable por sintaxis. Correcto.
- **R0325-5 (nuevo, no bloqueante, con dueno).** SLIP-0325-4: el perimetro cableado del negativo
  `NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT` es `break`/`continue`, no toda salida temprana. Un
  `return` falsy estrecho pasa el contrato y la suite entera con la misma fuga de email y telefono
  que E1. **Dueno: TASK-0332** (AC2 + AC3 + AC4), que debe (a) matarlo por comportamiento y
  (b) dejar el inventario diciendo lo que de verdad cubre. **Aviso de alcance para quien escriba
  0332: esta fila es obligatoria, no opcional; si 0332 se cerrara sin cubrirla, R0325-5 se queda sin
  dueno y hay que abrirle tarea propia.**
- **R0325-6 (informativo).** `visit_AsyncFor` es defensivo e inalcanzable mientras `contains_pii` sea
  un `def` sincrono: un `async for` ahi es error de sintaxis. No se puede falsar hoy; si algun dia
  `contains_pii` se vuelve `async`, esa rama pasa a necesitar su propia frontera.

## Conclusion

La remediacion es correcta y esta bien construida. Cambio la regla, no el sintoma: cortar por
**vinculacion** en vez de por **nodo** es la formulacion correcta de la propiedad, y se nota en que
las trece sondas de propiedad que le tire despues salen las trece bien -- no solo las dos que yo
habia nombrado. El numero que decidia esta vuelta cambio de verde a rojo. Las fronteras nuevas
aguantan el mutante de cableado inalcanzable, que es el que de verdad separa un contrato con dientes
de uno decorativo. Y R0325-4 no solo esta escrito: lo que afirma es cierto.

Queda una fuga viva de la misma consecuencia por una clase de sentencia distinta, y la dejo escrita
con nombre, medida y dueno en vez de esconderla en una observacion. No bloquea 0325 porque no es la
propiedad que 0325 acoto, porque su guarda no puede cubrirla sin analisis de valor, y porque la tarea
que si la cierra ya esta en la cola con GO. Bloquear aqui seria pedir a esta unidad que resuelva lo
que su sucesora tiene contratado, y ademas por un mecanismo que no le sirve.

**OK-CLOSABLE.** Sin fix loop pendiente. Lo unico que pido antes del commit de cierre es que
**R0325-5 quede escrito en el ledger** con TASK-0332 como dueno, para que no se cierre por olvido.

-- Analista
