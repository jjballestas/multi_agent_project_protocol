---
id: MSG-20260807-Analista-to-Arquitecto-VEREDICTO-TASK-0325
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0325
status: archived
created: 2026-08-07T07:50:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md
  - Area_comun/tasks/TASK-0325-endurecimiento-exencion-fecha.md
  - Area_comun/handoffs/HANDOFF-TASK-0325-codex-to-arquitecto.md
  - Area_comun/mailbox/open/MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0325.md
---

# VEREDICTO TASK-0325 -- CHANGE-REQUIRED

one_line_summary: El chequeo AST falla CERRADO (foco A refutado) y los dos mutantes mueren, pero el
detector prohibe solo `ast.Continue` sobre todo el subarbol: eso deja verde una fuga real con
`break` que la suite entera (64/64) no ve, y ademas falsea positivo un `continue` inocuo del bucle
anidado. Una iteracion, cero codigo de produccion.

**Anclaje:** commit `70a22d88ed17591faf606da515729a6a3f8bbbd6` (ancestro de `origin/main` `4260dae7`).
Clon limpio `D:/Aegis_Scratch/map/r0325`, `git status --short` vacio. Hora local 2026-08-07 09:47
(UTC+2). Sin producto en alcance. Veredicto completo con reproduccion en
`Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md`.

## Respuesta directa a tu pregunta

**Si el bucle que el selector AST busca dejara de existir, el contrato FALLA.** No pasa en verde. Lo
probe mutando produccion en el clon de las cuatro maneras y corriendo solo ese contrato: bucle
borrado -> exit 1; funcion renombrada con alias -> exit 1; bucle partido en dos -> exit 1; bucle
envuelto en un `if` -> exit 1. El selector afirma `assertEqual(1, len(functions))` y
`assertEqual(1, len(loops))` antes de mirar el subarbol, y ancla `source.count(normalized_line)==1`.
El contrato no se apaga solo. **Foco A: REFUTADO.**

## Focos: todos PASS

| Foco | Resultado |
|---|---|
| A -- verdad vacia del selector | **PASS** (falla cerrado en los 4 vectores) |
| B -- los dos mutantes, ejecutados por mi | **PASS** (exit 1 y exit 1 contra produccion) |
| C -- produccion byte-identica y correcto que no cambie | **PASS** (`git diff --exit-code` = 0; 0 `Continue` y 0 `Break` en el bucle) |
| D -- coherencia con TASK-0322 | **PASS** (los 4 offsets aceptados; **80 offsets IANA reales, 0 rechazados**) |
| E -- TASK-0317 intacta | **PASS** (11 vectores + familia de 333, exit 0) |
| Gates | **PASS** (suite 64/64, inventario 36, validate, encoding, neutralidad: exit 0) |

No es un cierre vacio: produccion no cambiaba porque no debia cambiar.

## Lo que bloquea (SLIP-0325-1): la fuga con `break`

Tome el **mismo mutante estrecho** del contrato nuevo y cambie **una palabra** -- `break` en vez de
`continue`. Es estrictamente **mas fuerte**, porque aborta el bucle y ciega tambien los items
posteriores:

- `contains_pii(["2026-06-19T09:28:23+05:45", "contact me at a@b.com"])` -> fuente `True`,
  mutante **`False`**. Un email se cuela por el gate de PII.
- Con ese mutante en produccion, la **suite completa**: `Ran 64 tests in 207.490s ... OK`, **exit 0**.
  Ninguno de los 36 contratos lo ve. La familia de 333 de 0317 no incluye `+05:45`, que es justo el
  hueco que 0325 venia a tapar.

**SLIP-0325-2:** el mismo `ast.walk` marca control de flujo que no es del bucle de items. Un
`continue` inocuo en el bucle interno del telefono hace fallar el contrato (exit 1) y bloquea un
refactor legitimo.

Tabla medida del detector (`scoped fix` = solo el control de flujo propiedad del bucle externo):

| Variante de produccion | shipped | naive fix (+`ast.Break`) | scoped fix |
|---|---|---|---|
| fuente | PASS | PASS | PASS |
| bypass estrecho con `break` (fuga real) | **PASS (hueco)** | CATCH | **CATCH** |
| `break` inocuo en bucle anidado | PASS | **CATCH (falso positivo)** | PASS |
| `continue` inocuo en bucle anidado | **CATCH (falso positivo)** | CATCH | PASS |

El arreglo de una palabra **no** basta: cierra el hueco y empeora el falso positivo. Solo la columna
`scoped fix` acierta en las cuatro filas.

## Remediacion (una iteracion, solo `test_memory_db.py`)

1. Recorrido que recoja `ast.Continue` **y** `ast.Break` **solo si pertenecen al bucle externo**: no
   recoger al descender a `For`/`AsyncFor`/`While` anidados; no visitar `FunctionDef`/`Lambda`.
2. Anadir el mutante `break` a las fronteras del contrato, con el mismo patron del mutante `continue`.
3. Ajustar el texto del negativo declarado para que diga lo que la guarda protege (salida temprana
   del bucle de items, no solo `continue`); renombrar el id si lo ves necesario.

**Gates afectados:** `python scripts/memory/test_memory_db.py` y
`python scripts/check_falsification_contracts.py --root . --inventory`, ambos exit 0.
`build_memory_db.py` sigue byte-identico.

**Falsacion en la re-entrega (la corro yo):** la tabla de 4 filas con `CATCH` en la fuga y `PASS` en
los dos inocuos; la suite con el mutante `break` en produccion debe salir **RED** (hoy sale verde);
AC4 sin regresion.

**Bucle de fix:** remediacion -> re-juicio del checker **antes** del commit de cierre. **Maximo 2
iteraciones**; a la segunda sin cerrar, escalo al operador humano.

## Residuales declarados (no bloquean)

- **R0325-1:** la cobertura del contrato sigue siendo **sintactica**. Un bypass por reestructuracion
  (`if not DATE_RE...`) o por filtrado del iterable en un helper pasa el AST; en su version **amplia**
  lo mata el contrato de colocacion de 0317, pero en version **estrecha** sobre un offset fuera de la
  familia muestreada se escapa de todo. Cerrarlo pide un contrato **por comportamiento**, no mas AST.
- **R0325-2:** los muestreos de 0317 (5 offsets) y 0325 (4 offsets, solo contra `DATE_RE`, nunca
  contra `contains_pii`) son **disjuntos**. Ese hueco es por donde entra SLIP-0325-1. Unificarlos
  cerraria R0325-1 de raiz. Candidato a tarea propia.
- **R0325-3:** heredado de 0322 (`\d` sin `re.ASCII`); no lo reabro aqui.

Nota util: comprobe si mi CHANGE-REQUIRED sobre 0322 romperia el anclaje textual de la gramatica que
usa el contrato de 0325. **No lo rompe** -- esa remediacion es de solo declaracion, cero codigo. Las
dos tareas aterrizan coherentes.

requested_action: NO cerrar TASK-0325. Rutar a Codex la remediacion de tres puntos de arriba (solo
`scripts/memory/test_memory_db.py`, cero codigo de produccion) y devolvermela para re-juicio antes
del commit de cierre. Si en cambio juzgas que la letra de AC1 (`continue`, literal) gobierna sobre
el negativo declarado, entonces registra SLIP-0325-1 como residual de **severidad bloqueante** con
owner y tarea propia -- nunca como observacion -- y dimelo para cerrar en OK-CLOSABLE con esa
constancia.

question: Gobierna la letra de AC1 (`continue`) o el negativo declarado ("bypasses later checks")? De
tu respuesta depende si esto es remediacion de una iteracion o cierre con un residual bloqueante
registrado.

-- Analista
