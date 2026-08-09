---
artifact_id: Analista-TASK-0327-derivacion-completa-verdict
task_id: TASK-0327
type: review_verdict
author: Analista
created_at: 2026-08-09
status: final
verdict: OK-CLOSABLE
iteration: 3
implementation_commit: 784dd470985e41472de4ef117cdec55c6af1ab21
verified_head: 5f72263f
supersedes: Analista-TASK-0327-quinto-portador-verdict
---

# TASK-0327 remediacion 2 -- la derivacion: veredicto OK-CLOSABLE

Voz: Analista (revisor adversarial independiente). Hora local de emision: 2026-08-09 02:57 (UTC+2).
Alcance declarado por el encargo: **SOLO el hub. SIN PRODUCTO EN ALCANCE.** No ejecute nada del
producto.

## Ancla canonica y reproduccion

Clon limpio `D:/Aegis_Scratch/mapp/rev0327r3/cc` desde el repo, `git checkout 784dd470`,
`git status --porcelain` vacio antes de medir. Banco de mutacion en un clon SEPARADO
`D:/Aegis_Scratch/mapp/rev0327r3/mut`; cada mutante reinicia con `git checkout -- .` +
`git clean -fdq scripts/memory`, borra todo `__pycache__` y aborta si `git status --porcelain` no
esta vacio. Nunca mido un gate mientras un driver mio muta el mismo arbol.

Los cinco gates, por EXIT CODE real (sin tuberia), en el clon limpio del ancla:

    python scripts/memory/test_memory_db.py                   -> exit 0   (72 tests, OK, 271.6s)
    python scripts/check_falsification_contracts.py --root .  -> exit 0
    python scripts/validate_collaboration_state.py --root .   -> exit 0
    python scripts/scan_encoding.py --root .                  -> exit 0
    python scripts/scan_domain_neutrality.py --root .         -> exit 0

`git status --porcelain` vacio DESPUES de correr los cinco.

**Alcance real del commit:** `784dd470` toca UN fichero, `scripts/memory/test_memory_db.py`, +7/-6.
`domain_pii_default_violations` tiene **un solo llamador** (`test_memory_db.py:246`, dentro de
`test_p01`). Nada fuera de `test_p01` puede haber cambiado de comportamiento por esta entrega; lo
verifico ademas con un control al padre mas abajo.

## Respuesta a tu pregunta

> Un portador en un modulo que hoy no existe muere sin tocar el test, o seguimos enumerando con
> otra sintaxis?

**Muere sin tocar el test.** Lo medi con cuatro modulos que no existen en el ancla, tres formas de
portador distintas y dos nombres distintos:

    scripts/memory/publish_memory_db.py :: def publish_is_clean(value, domain_pii_terms=())
        -> test_p01 exit 1   VIOLATIONS ['publish_memory_db.py:4']
    scripts/memory/publish_memory_db.py :: publish_is_clean = lambda value, domain_pii_terms=(): True
        -> test_p01 exit 1   VIOLATIONS ['publish_memory_db.py:3']
    scripts/memory/publish_memory_db.py :: async def publish_is_clean(value, *, domain_pii_terms=())
        -> test_p01 exit 1   VIOLATIONS ['publish_memory_db.py:4']
    scripts/memory/pii_policy.py        :: def policy_is_clean(value, domain_pii_terms=None)
        -> test_p01 exit 1   VIOLATIONS ['pii_policy.py:4']

Y **no es enumerar con otra sintaxis en la mitad que mas me preocupaba.** La segunda lista, la de
tipos de nodo, dejo de ser una lista: el chequeo pregunta por la ESTRUCTURA (`getattr(node, "args")`
que sea `ast.arguments`). Recorri `ast` entero en CPython 3.12 y los nodos con campo `args` son
exactamente cuatro: `FunctionDef`, `AsyncFunctionDef`, `Lambda` y `Call`. Los tres primeros llevan
un `ast.arguments`; `Call.args` es una `list`, asi que el `isinstance` lo descarta solo. Es decir:
el conjunto {`FunctionDef`, `AsyncFunctionDef`, `Lambda`} no esta escrito en ningun sitio, **se
deriva**, y es demostrablemente el conjunto completo de nodos de Python que declaran defaults. Un
tipo de nodo nuevo en una version futura de Python entraria solo si llevase `ast.arguments`, que es
justo el criterio de pertenencia correcto.

La primera lista, la de modulos, tambien dejo de ser una lista, pero su criterio de pertenencia
("colocacion en el directorio") es mas estrecho que su enunciado. Lo detallo en el foco C: son fugas
declaradas, no bloqueantes, y ninguna es la clase por la que se abrio la tarea.

## Banco de mutacion -- 26 colocaciones, gateadas por el exit code de `test_p01`

Baseline `test_p01` exit 0 en el ancla. Cada fila es una mutacion aislada sobre arbol limpio.

### Regresion: las 7 que ya morian en r2 (deben seguir muriendo)

| # | Colocacion | Modulo | test_p01 | Violacion descubierta |
|---|-----------|--------|----------|----------------------|
| N1 | `def` top-level, default posicional `()` | build | **exit 1 MUERE** | `build_memory_db.py:1247` |
| N2 | `def` top-level, default keyword-only `()` | drift | **exit 1 MUERE** | `check_memory_db_drift.py:236` |
| N3 | `def` top-level, default posicional `None` | query | **exit 1 MUERE** | `query_memory_db.py:287` |
| N4 | metodo de clase, default posicional | build | **exit 1 MUERE** | `build_memory_db.py:1248` |
| N5 | funcion ANIDADA, default posicional | build | **exit 1 MUERE** | `build_memory_db.py:1248` |
| N9 | parametro POSICIONAL-ONLY con default | build | **exit 1 MUERE** | `build_memory_db.py:1247` |
| N10 | `async def`, default posicional | build | **exit 1 MUERE** | `build_memory_db.py:1247` |

**7 de 7 siguen muriendo.**

### Foco A: los tres escapes que medi en r2 (deben morir ahora)

| # | Colocacion | Modulo | r2 | r3 |
|---|-----------|--------|----|----|
| N6 | **`lambda value, domain_pii_terms=(): ...`** | build | exit 0 SOBREVIVIA | **exit 1 MUERE** |
| N12 | `def ... domain_pii_terms=()` | **revive_pack.py** | exit 0 SOBREVIVIA | **exit 1 MUERE** |
| N13 | `def ... domain_pii_terms=()` | **dump_memory_db.py** | exit 0 SOBREVIVIA | **exit 1 MUERE** |

No me quedo en los tres del encargo; probe la lambda en las otras coordenadas por si el arreglo
cerraba el ejemplo y no la familia:

| # | Colocacion | Modulo | test_p01 |
|---|-----------|--------|----------|
| N6b | lambda, default posicional | revive_pack | **exit 1 MUERE** |
| N6c | lambda, default KEYWORD-ONLY | query | **exit 1 MUERE** |
| N6d | lambda INLINE como argumento de llamada (`sorted(..., key=lambda ...)`) | build | **exit 1 MUERE** |
| N6e | lambda con parametro POSICIONAL-ONLY | dump | **exit 1 MUERE** |

**Los tres escapes de r2 estan cerrados, y la familia entera con ellos: 7 de 7 formas de lambda x
coordenada mueren.**

### Foco B: un SEXTO modulo que hoy no existe

| # | Colocacion | test_p01 | r2 |
|---|-----------|----------|----|
| N8 | modulo NUEVO `publish_memory_db.py`, `def` portador | **exit 1 MUERE** | exit 0 sobrevivia (era el residual R2) |
| N8b | modulo NUEVO, LAMBDA portadora | **exit 1 MUERE** | -- |
| N8c | modulo NUEVO, `async def` keyword-only | **exit 1 MUERE** | -- |
| N8d | SEPTIMO modulo con nombre no relacionado (`pii_policy.py`) | **exit 1 MUERE** | -- |

**Cae sin tocar el test.** R2 de r2 queda cerrado de paso, como anticipe.

### Foco C: el glob no se pasa de ancho -- y donde SI se queda corto

Conjunto derivado en el ancla, recomputado por mi de forma independiente:

    build_memory_db.py, check_memory_db_drift.py, dump_memory_db.py,
    query_memory_db.py, revive_pack.py            -> COUNT = 5

Son exactamente los cinco modulos de produccion del motor. Ni uno de mas.

| # | Prueba de anchura | test_p01 | Lectura |
|---|------------------|----------|---------|
| C4 | `.py` inocuo NO del motor soltado en el directorio, sin portador | exit 0 | **No hay falso positivo.** El glob se ensancha sin gritar: arrastra el fichero, no encuentra portador, no rompe |
| C1b | modulo nuevo `tests_util.py` (prefijo `tests`, sin guion bajo) con portador | **exit 1 MUERE** | La exclusion es literal `test_`, no atrapa de mas |
| C1 | modulo nuevo `test_helpers.py` (**de produccion**, prefijo `test_`) con portador | exit 0 **SOBREVIVE** | La exclusion por prefijo tapa un portador real |
| C2 | **SUBPAQUETE** `scripts/memory/adapters/pii_adapter.py` con portador | exit 0 **SOBREVIVE** | `glob` no es recursivo |
| C3 | modulo `publish_memory_db.pyw` con portador | exit 0 **SOBREVIVE** | El criterio esta atado a la extension `.py` |

Sobre C1 medi ademas el dato que decide si es barato cerrarlo: **la exclusion `test_` NO es
portante.** Corri el propio chequeo sobre `test_memory_db.py` y da **cero violaciones**, asi que hoy
el fichero de test podria excluirse por identidad (`p != Path(__file__)`) en vez de por prefijo, sin
poner nada en rojo. Lo dejo escrito porque es un dato falsable a favor del arreglo futuro, no una
condicion de cierre.

### Foco D: sin regresion

**F1 sigue cerrado, verificado de forma independiente.** Barrido AST propio sobre **todos** los
`*.py` del repo (no grep, no la lista del test), buscando `domain_pii_terms` con default posicional,
posicional-only o keyword-only, en `def`, `async def`, lambda, metodo o funcion anidada:

    TOTAL_CARRIERS_REPO_WIDE = 0

**AC2 (omision = error de firma), las cuatro guardas, medido llamando de verdad:**

    contains_pii('x')                 -> TypeError: missing 1 required positional argument
    title_is_safe('x')                -> TypeError: missing 1 required positional argument
    validate_metadata({}, [])         -> TypeError: missing 1 required positional argument
    require_safe_text('x','k')        -> TypeError: missing 1 required keyword-only argument

**AC4 (contrato por consecuencia): los tres negativos permanentes conservan los dientes.** Corte la
fontaneria en el corazon semantico -- `contains_pii` devolviendo siempre `False`, con la llamada
textualmente presente en los tres call sites:

| Mutante | NEG-...-PUBLICATION | NEG-...-INGESTION | NEG-...-RETRIEVAL-REASON |
|---------|--------------------|-------------------|--------------------------|
| M1 `contains_pii` neutralizado | **exit 1 MUERE** | **exit 1 MUERE** | **exit 1 MUERE** |

Probe ademas cortes de **una sola** rama, y el resultado es informativo y juega a favor de la
entrega: `title_is_safe` neutralizado (M4) o la rama PII de `validate_metadata` hecha INALCANZABLE
(M2, `if False and ...` en `build_memory_db.py:642`) **no** ponen en rojo a `NEG-...-PUBLICATION`.
No es un punto ciego: es que el artefacto con PII **lo sigue rechazando la guarda hermana**. Cortar
una sola no basta porque la otra atrapa; cortar el `contains_pii` comun mata las tres. Eso es
profundidad de defensa medida, no un agujero.

**Control de que M2/M3/M4 no son regresion de esta entrega:** repeti M2 sobre el commit PADRE
`f732292a` y `NEG-...-PUBLICATION` sale exit 0 igual. Comportamiento identico antes y despues, como
tenia que ser dado que el commit toca un unico fichero de test y un helper con un solo llamador.

## Tabla foco por foco

| Foco del encargo | Que exigia | Veredicto | Evidencia |
|------------------|-----------|-----------|-----------|
| **A -- los tres escapes de r2 mueren** | lambda + `def` en revive_pack + `def` en dump_memory_db | **PASS** | N6, N12, N13 pasan de exit 0 a **exit 1**. Y la familia completa: N6b/N6c/N6d/N6e (lambda x posicional / keyword-only / inline / posicional-only x cuatro modulos) tambien mueren. El conjunto de tipos de nodo esta DERIVADO de `ast.arguments`, no enumerado: comprobado contra el `ast` de CPython 3.12 -- solo `FunctionDef`, `AsyncFunctionDef`, `Lambda` y `Call` llevan campo `args`, y el `isinstance` descarta `Call` porque su `args` es `list`. |
| **B -- un sexto modulo cae sin tocar el test** | crear uno nuevo y comprobar | **PASS** | N8/N8b/N8c en `publish_memory_db.py` y N8d en un septimo modulo `pii_policy.py`, con `def`, lambda y `async def` keyword-only: **los cuatro exit 1**, sin editar `test_memory_db.py`. |
| **C -- el glob no se pasa de ancho** | no arrastrar lo que no es del motor; la exclusion `test_*` no tapa un portador real | **PASS de anchura / PARCIAL de estrechez** | No se pasa de ancho: el conjunto derivado en el ancla son **exactamente** los 5 modulos del motor y un `.py` ajeno sin portador no produce falso positivo (C4). **Si se queda corto en tres formas**: prefijo `test_` (C1), subdirectorio (C2), extension `.pyw` (C3). Las tres las declaro como residuales R6/R7/R8 -- ninguna existe hoy en el arbol y ninguna es la clase por la que se abrio 0327. Dato para el arreglo barato: la exclusion `test_` **no es portante** (el fichero de test da 0 violaciones). |
| **D -- sin regresion** | F1 cerrado y los 7 de 7 siguen muriendo | **PASS** | 7 de 7 mueren. F1: **0 portadores en TODO el repo** por barrido AST propio. AC2: `TypeError` en las cuatro guardas. AC4: M1 mata los tres negativos permanentes. Los cinco gates exit 0 en clon limpio; suite completa 72 tests OK en 271.6s. Control al padre confirma que nada de M2/M3/M4 es regresion. |

## Residuales declarados (no bloquean)

- **R1 -- portador por default SEMANTICO, sin default sintactico.** Sigue abierto y le anadi dos
  formas nuevas, las tres medidas con `test_p01` exit 0:
  `def f(value, **kwargs): kwargs.setdefault('domain_pii_terms', ())` (R1a),
  `functools.partial(base, domain_pii_terms=())` (R1b) y
  `f.__defaults__ = ((),)` inyectado en tiempo de ejecucion (R1c). La propiedad ata la SINTAXIS del
  default; la semantica de la omision no es decidible estaticamente. Lo mantengo como residual por
  la misma razon que en r2, ahora con tres testigos en vez de uno.
- **R6 -- la exclusion `test_` tapa un portador real (C1).** Un modulo de produccion llamado
  `test_*` es invisible. Coste de cierre: cambiar el filtro de prefijo por identidad del fichero,
  que hoy no rompe nada (medido: el test da 0 violaciones sobre si mismo).
- **R7 -- el glob no es recursivo (C2).** Un subpaquete `scripts/memory/<algo>/` es invisible. Hoy
  `scripts/memory/` es plano (unico subdirectorio: `__pycache__`). Coste de cierre: `rglob`.
- **R8 -- el criterio esta atado a la extension `.py` (C3).** Un `.pyw` es invisible. Es el mas
  teorico de los tres.
- **R9 -- el conjunto derivado no tiene suelo: puede quedar VACIO y el chequeo pasa en verde.**
  Forzando el glob a un conjunto vacio y anadiendo a la vez un portador real en `build_memory_db.py`,
  `test_p01` sale **exit 0** (V2). No hay ninguna asercion de que el conjunto descubierto sea no
  vacio, asi que una reorganizacion benigna del directorio deja la propiedad vacia sin que nadie se
  entere. Es el residual que mas me interesa de los cuatro nuevos, porque se dispara por refactor
  ordinario y no por adversario. Coste de cierre: una linea.
- **R4 (heredado de r2, ahora medido) -- `test_p01` no es negativo permanente declarado.**
  Cortocircuitando `domain_pii_default_violations` a `return []` con un portador real presente,
  `test_p01` sale **exit 0** (V1) y `check_falsification_contracts.py` no lo delata, porque
  `test_p01` no lleva marcador `PERMANENT_NEGATIVE:` ni contrato en el registro. Mi F2 no lo pedia;
  sigue siendo deuda barata.
- **R5 (heredado) -- la medicion sigue siendo 0-a-0.** La politica viva declara cero
  `domain_pii_terms` y el corpus cero artefactos publicables. Toda la evidencia positiva es de
  fixture, que es lo legitimo con corpus vacio.
- **F5 de r2, parcialmente atendido.** El comentario bajo la asercion pasa de "every function in all
  three memory-engine modules" (falso por partida doble) a "Directory placement and structural
  ast.arguments define both complete sets". La mitad estructural de esa frase es **verdad
  demostrada**. La mitad de directorio afirma completitud que el recuento no respalda: el criterio
  real es "`*.py` plano del directorio, menos los `test_*`", con las tres fugas R6/R7/R8. No bloqueo
  por la redaccion -- en r2 declare F5 recomendado y no obligatorio, y no muevo la porteria -- pero
  lo dejo escrito: una afirmacion de completitud que el recuento no respalda es la misma clase de
  defecto que trajo esta tarea hasta aqui.

## Limite propio declarado

CPython 3.12.10 en Windows. Clon limpio para medir, clon separado para mutar, `git status
--porcelain` verificado vacio antes y despues de cada mutante y al terminar los dos bancos. La suite
completa (72 tests, 271.6 s) la corri entera una vez en el ancla; los 26 mutantes se gatearon por el
metodo de test que corresponde a cada uno, no por la suite entera. No ejecute nada del producto: el
encargo declara SIN PRODUCTO EN ALCANCE. No juzgo aqui la cobertura de CI de otros runners
(particion de TASK-0330); para este chequeo concreto ya verifique en r2 que
`.github/workflows/validate.yml` corre `python scripts/memory/test_memory_db.py`.

## Recomendacion de cierre: OK-CLOSABLE

Los dos obligatorios que declare en r2 estan cerrados y medidos:

- **F3** (descubrir los modulos en vez de enumerarlos): N12 y N13 pasan de exit 0 a exit 1, y de
  paso cae R2 -- un modulo nuevo con portador muere sin tocar el test (N8, N8b, N8c, N8d).
- **F4** (cubrir `ast.Lambda`): N6 pasa de exit 0 a exit 1, y con el las siete combinaciones de
  lambda x coordenada x modulo.

Y lo hizo sin las dos trampas que esperaba encontrar. No ensancho la enumeracion de tres a cinco
nombres, que es lo que pedia mi letra y habria dejado la clase abierta: derivo del directorio. Y en
los tipos de nodo no anadio `ast.Lambda` a una tercera lista escrita a mano, que era la remediacion
obvia y estrecha: sustituyo la lista por el criterio de pertenencia estructural, que es
demostrablemente completo. Esa segunda mitad es una derivacion de verdad, no una enumeracion mejor.

Cierro **sin** bloquear por R6/R7/R8/R9 y lo justifico con el mismo baremo que use para bloquear en
r2. Alli bloquee porque N12/N13 eran *"un `def` top-level con el default vacio, la forma EXACTA del
defecto original, en un modulo del motor que YA EXISTE"*. Ninguno de los cuatro residuales nuevos
cumple ese baremo: los tres primeros exigen que el motor adopte una forma de fichero que hoy no
tiene (subdirectorio, prefijo `test_`, extension `.pyw`) y el cuarto exige que el conjunto quede
vacio. Aplicar hoy un baremo mas duro que el que aplique en r2 seria mover la porteria, y ademas
seria pedir otra forma mas estrecha en lugar de una propiedad -- exactamente el patron contra el que
esta tarea existe.

**No pido tercera iteracion de TASK-0327.** R6, R7 y R9 son tres lineas en total y estan
falsablemente descritas arriba (C1 -> exit 1, C2 -> exit 1, V2 -> exit 1 como criterio de
aceptacion); recomiendo al Arquitecto abrirlas como una tarea de endurecimiento aparte, con R9
primero por ser la unica que se dispara por refactor ordinario. Esa decision de alcance es suya, no
mia: yo la dejo medida.

-- Analista
