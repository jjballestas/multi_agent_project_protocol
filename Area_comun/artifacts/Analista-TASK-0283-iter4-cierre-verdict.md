---
artifact: Analista-TASK-0283-iter4-cierre-verdict
task: TASK-0283
reviewer: Analista
verdict: OK-CLOSABLE
iteration: 4
remediation_loop: 2 of 2 (converges)
created_at: 2026-07-22
anchors:
  product_commit: none (SIN PRODUCTO EN ALCANCE)
  reviewed_commit: 2267f2c
  protocol_head: b32ab02 (local; origin/main=26ec5c2)
---

# Analista - Re-juicio de cierre TASK-0283 iteracion 4 (ast.walk / recorrido completo)

Hora local: 2026-07-22 16:02 (reloj del sistema, sin convertir).

## Ancla canonica

- Commit del entregable juzgado: `2267f2c` (test: walk complete AST for marked
  negatives), el que cita la instruccion.
- HEAD local del protocolo: `b32ab02`; origin/main=`26ec5c2`. Los tres commits
  posteriores a `2267f2c` (fcbc41f, 3c1d3d9, 26ec5c2) y `b32ab02` NO tocan los scripts
  del guardian: `git diff --stat 2267f2c..b32ab02 -- check_falsification_contracts.py
  test_falsification_contracts.py falsification_contracts.py new_instance.py` sale VACIO.
  Juzgar en `2267f2c` equivale a juzgar en HEAD para el codigo bajo revision.
- Escrutinio en CLON LIMPIO en `D:/c283i4`, checkout `2267f2c`, gates por exit code.
  No juzgue sobre el arbol caliente. Cada ataque de descubrimiento lo corri en un root
  de fixture AISLADO (el checker escanea `<root>/examples` y `<root>/scripts`); los de
  regresion (A3/A4) los aplique sobre el fichero real y restaure con `git checkout` (tree
  limpio verificado tras cada uno).
- SIN PRODUCTO EN ALCANCE (respetado; fondo pineado y dataset N=500 no tocados).

## Que cambio en iter4

`permanent_negatives()` y `function_source()` pasan de iterar `tree.body` (solo nivel de
modulo) a `ast.walk(tree)` (recorrido COMPLETO del AST). Un `FunctionDef`/`AsyncFunctionDef`
a cualquier profundidad -- metodo, funcion anidada, clase dentro de funcion -- ahora entra
en el inventario. El self-test del maker anade un control de mutacion que reescribe ambos
`ast.walk` de vuelta a `tree.body` en un checker aislado y exige que el metodo marcado se
vuelva invisible (0/0/0): el recorrido completo es load-bearing y su control mata la
regresion pedida.

## Reproduccion (exit codes en el clon limpio)

Gates base, todos verdes:

```
python scripts/check_falsification_contracts.py --root . --inventory  -> 0  (permanent_negatives=15 declared=15 missing=0)
python scripts/test_falsification_contracts.py                         -> 0  (self-test del maker, complete-AST + limite)
python scripts/validate_collaboration_state.py --root .                -> 0
python scripts/scan_encoding.py                                        -> 0
python scripts/scan_domain_neutrality.py                               -> 0
```

Ataques de DESCUBRIMIENTO (blancos mios, negativos MARCADOS que deben verse; root aislado):

```
V1) metodo de clase                  -> exit 1  permanent_negatives=1 missing=1  VISIBLE
V2) funcion anidada (func en func)    -> exit 1  1/0/1                            VISIBLE
V3) metodo de CLASE-DENTRO-DE-FUNCION -> exit 1  1/0/1                            VISIBLE
V4) funcion triple-anidada            -> exit 1  1/0/1                            VISIBLE
V5) metodo async                      -> exit 1  1/0/1                            VISIBLE
V6) metodo @staticmethod              -> exit 1  1/0/1                            VISIBLE
```

Regresion sobre el suite REAL (fichero mutado y restaurado):

```
A3) quito el marcador de retry-destructive-reset (linea de marker)
    -> exit 1  permanent_negatives=10  ERROR: ...declared contract has no permanent-negative marker  (marker load-bearing)
A4) relajo la frontera 'assert not survivors' en run_nondestructive_rollback_contract
    -> exit 1  ERROR: ...assertion boundary not found beside the test: assert not survivors  (degradacion cazada)
```

## Tabla vector-a-vector

| # | Lo que pedia la instruccion | Blanco que elegi | Resultado | Dictamen |
|---|------------------------------|------------------|-----------|----------|
| Base | inventario + self-test + 4 gates verdes | -- | 15/15/0, exit 0 en los 5 gates | PASS |
| 1a | metodo | negativo marcado como metodo | exit 1, VISIBLE | PASS |
| 1b | funcion anidada | marker en func-en-func | exit 1, VISIBLE | PASS |
| 1c | clase dentro de funcion | marker en metodo de clase-en-func | exit 1, VISIBLE | PASS |
| 1d | profundidad arbitraria | triple-anidada / async / staticmethod | exit 1, VISIBLE | PASS |
| 2 | el limite declarado, no un hueco | doc: "runtime generation is not mechanically decidable here" + "unmarked ... cannot be inferred from the static source" | limite escrito | PASS |
| 3a | A3 marcador load-bearing | quitar marker -> stale-loud | exit 1 | PASS |
| 3b | A4 degradacion de contrato | relajar frontera declarada | exit 1, mensaje exacto | PASS |

## Juicio

**El bloqueante de iter3 esta CERRADO, exhaustivamente.** El escape que abri en iter3 --
un negativo MARCADO escrito como metodo de clase (A2a) o funcion anidada (A2b) era
SILENCIOSAMENTE INVISIBLE (15/15/0, exit 0) -- ya no existe. Probe seis colocaciones
distintas del `FunctionDef` (metodo, func anidada, metodo de clase-en-funcion,
triple-anidada, async, staticmethod) y las SEIS aparecen missing/rojo. `ast.walk` es
exhaustivo por construccion sobre el universo `FunctionDef`/`AsyncFunctionDef`: recorre
todo nodo alcanzable, y un `def` no puede vivir en una comprension ni en una lambda (que no
lleva docstring), de modo que ningun nivel de anidamiento de FUNCION deja escapar un
negativo marcado. El control de mutacion del maker (reescribir `ast.walk` a `tree.body`
vuelve el metodo invisible) confirma que el recorrido es load-bearing y no decorativo.

**El limite esta DECLARADO como indecidibilidad, no como hueco.** La doc del checker ahora
dice que el inventario es completo "for source definitions that follow the convention" y
que "runtime generation is not mechanically decidable here"; un negativo sin marcador o
generado en runtime es "a prohibited review/CI defect, but cannot be inferred from the
static source". Eso es el limite correcto: lo que un recorrido del FUENTE no puede ver no es
un fallo del recorrido.

**Regresion intacta.** A3 (quitar el marcador de un negativo declarado -> stale-loud) y A4
(relajar una frontera declarada -> ROJO con el mensaje exacto) siguen cazando sobre el suite
real. No retrocedio nada.

Respuesta directa a la pregunta del REVIEW: **con `ast.walk` NO queda ningun nivel de
anidamiento donde un negativo MARCADO pueda esconderse invisible. El hueco estructural de
descubrimiento (clase C de iteraciones previas: fichero fuera del glob; y clase A2:
definicion anidada) esta genuinamente cerrado.**

## Recomendacion de cierre

**GO -- OK-CLOSABLE.** Iteracion 4, remediacion 2 de 2 sobre el acceptance refinado: el
maker implemento exactamente la direccion F1 que mi veredicto de iter3 declaro suficiente
("recorrer todo el arbol con `ast.walk`... A2a/A2b pasan a visibles/rojo"), y la verificacion
por comportamiento lo confirma. La unidad converge. El Arquitecto puede cerrar TASK-0283
(flip in_review -> done + liberar claim). YO NO CIERRO NI PROMUEVO (checker-only).

## Residuales declarados (informativos, NO bloqueantes; ver justificacion)

- **R-1 (function_source por nombre, no por nodo -- hardening A4, PRIORIDAD ALTA de los
  residuales):** `function_source(path, name)` re-resuelve `exercised_by` por NOMBRE con el
  PRIMER match del `ast.walk` (orden BFS = nivel de modulo primero), DESACOPLADO del nodo
  que realmente lleva el marcador. Construi un contra-ejemplo (Probe2): un negativo marcado
  REAL escrito como METODO y DEGRADADO (perdio su frontera), con una funcion senuelo de
  MODULO del MISMO nombre que SI contiene las cadenas de mutacion/frontera. El checker
  descubre el metodo (missing=0) pero valida el contrato contra el senuelo de modulo ->
  exit 0 FALSO-VERDE. Es un bypass de A4 (degradacion) por colision de nombre, y en esa
  configuracion exacta iter4 es incluso mas silencioso que el checker viejo (tree.body la
  daba stale-roja porque ni descubria el metodo). PERO: (a) es un contra-ejemplo CONSTRUIDO
  -- exige una colision de nombre modulo/metodo Y que el senuelo contenga por casualidad la
  mutacion + todas las fronteras; (b) NO afecta al artefacto entregado: verifique que los 8
  `exercised_by` de los contratos embarcados son todos de MODULO y UNICOS
  (total_defs_named=1), asi que la colision es INALCANZABLE en el suite y en el export
  `new_instance.py`; (c) no es una invisibilidad (el negativo marcado SI se descubre), por
  lo que NO responde en afirmativo a la pregunta de esta iteracion (niveles de anidamiento).
  Fix exacto cuando el operador quiera endurecer A4: enlazar `function_source` al qualname
  del nodo YA descubierto que lleva el marcador (no re-resolver por nombre), o hacer error
  duro si `exercised_by` resuelve a mas de un nodo. Recomiendo capturarlo como TAREA de
  hardening propia (un residual sin acceptance se evapora -- leccion TASK-0275), NO como
  bloqueante de esta unidad de HIGIENE ya time-boxeada.

- **R-2 (precision de doc -- menor):** el marcador se descubre solo en el docstring de un
  `def`/`async def`. Un `PERMANENT_NEGATIVE:` colocado en el docstring de una CLASE, en el
  docstring de MODULO, en un string que no es docstring, o en un COMENTARIO es invisible
  (lo probe: E1 clase, E2 modulo, E3 string no-docstring, E4 comentario -> los cuatro 0/0/0
  exit 0). Esto NO es un negativo-marcado que se escape: en los cuatro casos el TEST real (si
  lo hay) es un `def` SIN marcador en su propio docstring, y un negativo sin marcador es
  precisamente el limite YA declarado (indecidible / defecto de review-CI). Se reduce al
  residual R-B. Recomendacion: una frase en la doc/convencion aclarando que el marcador debe
  ir en el docstring del `def`/`async def` del propio test (no en clase/modulo/comentario).
  Cosmetico.

- **R-B (retirado por indecidible, limite vivo):** un negativo permanente REAL SIN marcador
  sigue invisible por diseno. Es el limite documentado; no es el bloqueante de hoy.

- **R-Q1b (menor, diferible):** el chequeo de frontera sigue siendo presencia-de-subcadena
  (`if boundary not in source`), no liveness; una frontera conservada pero vuelta vacua no
  se caza. Limite conocido de iteracion 1. R-1 compone con este.

- Fondo intocable (protocol.config pineado, dataset N=500): fuera de alcance, no tocado.

## Bucle de correccion

Ninguno pendiente para el cierre: veredicto GO. Los residuales R-1 y R-2 son follow-up
opcional (R-1 como tarea de hardening si el operador quiere A4 a prueba de colision de
nombre; R-2 como aclaracion de doc). No reabren TASK-0283.

-- Analista
