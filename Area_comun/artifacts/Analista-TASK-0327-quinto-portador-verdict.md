---
artifact_id: Analista-TASK-0327-quinto-portador-verdict
task_id: TASK-0327
type: review_verdict
author: Analista
created_at: 2026-08-08
status: final
verdict: CHANGE-REQUIRED
iteration: 2
implementation_commit: f732292ad6588aebdbd00e9ff2e46938fd2b0439
verified_head: 7000b8ba
supersedes: Analista-TASK-0327-default-contains-pii-verdict
---

# TASK-0327 remediacion 1 -- el quinto portador: veredicto CHANGE-REQUIRED

Voz: Analista (revisor adversarial independiente). Hora local de emision: 2026-08-08 20:54 (UTC+2).
Alcance declarado por el encargo: **SOLO el hub. SIN PRODUCTO EN ALCANCE.** No ejecute nada del
producto.

## Ancla canonica y reproduccion

Clon limpio `D:/Aegis_Scratch/mapp/rev0327r2/cc` desde el repo, `git checkout f732292a`,
`git status --short` vacio. Banco de mutacion en un clon SEPARADO
`D:/Aegis_Scratch/mapp/rev0327r2/mut` -- nunca mido un gate mientras un driver mio muta el mismo
arbol; cada mutante reinicia con `git checkout -- .`, borra `__pycache__` y verifica
`git status --porcelain` vacio antes de correr.

Los cinco gates, por EXIT CODE real (sin tuberia), en el clon limpio del ancla:

    python scripts/memory/test_memory_db.py                  -> exit 0   (71 tests, OK, 240.2s)
    python scripts/check_falsification_contracts.py --root .  -> exit 0
    python scripts/validate_collaboration_state.py --root .   -> exit 0
    python scripts/scan_encoding.py --root .                  -> exit 0
    python scripts/scan_domain_neutrality.py --root .         -> exit 0

`git status --porcelain` vacio DESPUES de correr los cinco.

**Contraste con HEAD `7000b8ba`:** entre el ancla y HEAD cambian `build_memory_db.py` (+6/-... por
TASK-0328) y `test_memory_db.py` (+181 por 0328/0332). `domain_pii_default_violations` y el cuerpo de
`test_p01` son **byte-identicos** en ambos, y el barrido de portadores en HEAD sigue dando 0. El
bloqueante de abajo esta vivo tambien en `7000b8ba`.

## Respuesta a tu pregunta

> El chequeo de propiedad mata un quinto portador escrito manana, o solo los cuatro que ya conocemos?

**Mata muchisimo mas que los cuatro conocidos, y no mata "cualquier portador".** Mata un portador
nuevo si es un `def` (o `async def`) y vive en uno de los TRES modulos que el test enumera. No lo
mata si es una **lambda** en esos mismos tres modulos, ni si es un `def` en **los otros dos modulos
de produccion del mismo motor**.

Lo medi. Once colocaciones de un quinto portador, cada una en el banco de mutacion, gateadas por el
exit code de `test_p01_domain_pii_parameters_are_required` (baseline exit 0):

| # | Colocacion del quinto portador | Modulo | test_p01 |
|---|-------------------------------|--------|----------|
| N1 | `def` top-level, default posicional `()` | build | **exit 1 -- MUERE** |
| N2 | `def` top-level, default keyword-only `()` | drift | **exit 1 -- MUERE** |
| N3 | `def` top-level, default posicional `None` | query | **exit 1 -- MUERE** |
| N4 | metodo de clase, default posicional | build | **exit 1 -- MUERE** |
| N5 | funcion ANIDADA dentro de otra, default posicional | build | **exit 1 -- MUERE** |
| N9 | parametro POSICIONAL-ONLY con default | build | **exit 1 -- MUERE** |
| N10 | `async def`, default posicional | build | **exit 1 -- MUERE** |
| N6 | **`lambda value, domain_pii_terms=(): ...`** | build | **exit 0 -- SOBREVIVE** |
| N12 | **`def ... domain_pii_terms=()`** | **revive_pack.py** | **exit 0 -- SOBREVIVE** |
| N13 | **`def ... domain_pii_terms=()`** | **dump_memory_db.py** | **exit 0 -- SOBREVIVE** |
| N8 | `def` en un modulo NUEVO `scripts/memory/publish_memory_db.py` | nuevo | exit 0 -- sobrevive |
| N7 | `**kwargs` + `kwargs.setdefault('domain_pii_terms', ())` | build | exit 0 -- sobrevive |
| N11 | parametro renombrado con fallback interno | drift | exit 0 -- sobrevive (fuera de la propiedad) |

Los siete primeros son el avance real y es grande: el chequeo entregado **no se rodea por
colocacion** (metodo, anidada, async, posicional-only, keyword-only, los tres modulos), que es
exactamente la clase de escape que costo tres iteraciones en TASK-0283. N11 no es defecto: nombra
otro parametro y la propiedad no habla de el. N7 y N8 los declaro como residuales.

N6, N12 y N13 son el bloqueante.

## SLIP-0327-2 (BLOQUEANTE) -- el chequeo cambio dos nombres de funcion codificados por dos enumeraciones codificadas

El diagnostico de la iteracion 1 fue: *"el contrato ata el helper, no el efecto; un test que afirma
dos `assertRaises(TypeError)`, uno por cada nombre citado en el AC, es un test de FORMA"*. La
remediacion retiro esos dos nombres. Pero el chequeo que los sustituye descansa en otras dos listas
escritas a mano, y por las dos se escapa un portador:

    module_paths = (MODULE_PATH, DRIFT_MODULE_PATH, QUERY_MODULE_PATH)   # tres de cinco
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):    # falta ast.Lambda
        continue

### Escape 1 -- dos modulos de produccion del mismo motor quedan fuera del barrido (forma dominante)

`scripts/memory/` contiene CINCO modulos de produccion: `build_memory_db.py`,
`check_memory_db_drift.py`, `query_memory_db.py`, **`dump_memory_db.py`** y **`revive_pack.py`**. La
propiedad recorre tres. Falsado por comportamiento:

    # revive_pack.py, apendice:
    def revive_is_clean(value, domain_pii_terms=()):
        return True
    -> test_p01 exit 0   (VIOLATIONS: [] -- invisible)

    # dump_memory_db.py, apendice:
    def dump_is_clean(value, domain_pii_terms=()):
        return True
    -> test_p01 exit 0   (VIOLATIONS: [] -- invisible)

No es una forma exotica: es un `def` top-level con el default vacio, la forma EXACTA del defecto
original, en un modulo del mismo motor. `revive_pack.py` revive cold packs y `dump_memory_db.py`
vuelca la base -- las dos son vecindades naturales para que alguien escriba manana un chequeo de PII
de conveniencia.

**Declaro la atenuante que juega en mi contra:** el alcance de tres modulos es el que escribi YO en
F2 de la iteracion 1 ("ninguna funcion de `build_memory_db.py`, `check_memory_db_drift.py` ni
`query_memory_db.py`"), y `scope_routes` de la tarea tampoco nombra los otros dos. **La entrega
cumple mi letra.** Bloqueo por el proposito, que es la pregunta que tu encargo pone como decisiva:
el motor tiene cinco modulos y el barrido enumera tres, asi que la clase no esta cerrada. Y el
arreglo no toca los dos modulos huerfanos: se hace entero dentro de `test_memory_db.py`, que SI es
ruta de alcance -- descubrir los modulos en vez de enumerarlos.

### Escape 2 -- `ast.Lambda` no es `ast.FunctionDef`

    # build_memory_db.py, apendice:
    lambda_carrier = lambda value, domain_pii_terms=(): contains_pii(value, domain_pii_terms)
    -> test_p01 exit 0   (VIOLATIONS: [] -- invisible)

En Python una lambda ES una funcion con parametros por defecto. El comentario que la entrega dejo
bajo la asercion dice *"The property covers every function in all three memory-engine modules"*, y
el handoff dice *"recorre todas las funciones de los tres modulos"*. Las dos afirmaciones son falsas
tal como esta escrito el chequeo, y lo son dentro de los tres modulos enumerados: es el criterio C
de tu encargo incumplido en su propio terreno.

### El limite del dano, medido y declarado porque juega en contra de mi tesis

Un portador por lambda que **ciega una guarda YA EXISTENTE** sigue muriendo por consecuencia. Lo
comprobe end to end (N14): sustitui la llamada de `_publicable_pii_errors` por una lambda portadora
con default vacio, dejando la guarda textualmente presente:

    test_p01 (propiedad)                     -> exit 0   (no lo ve)
    NEG-MEMORY-DOMAIN-PII-PUBLICATION        -> exit 1   (SI lo mata)

Es decir: la profundidad de defensa funciona para las tres puertas que 0327 cerro. Lo que queda
descubierto es el caso que el chequeo de propiedad existe justamente para cubrir -- **una guarda
NUEVA, escrita manana, que ningun negativo por consecuencia ejercita todavia**. Por eso el
bloqueante es acotado y de cuatro lineas, no un rechazo de la entrega.

## Tabla foco por foco

| Foco del encargo | Que exigia | Veredicto | Evidencia |
|------------------|-----------|-----------|-----------|
| **A -- F1 de verdad cerrado** | Sin default en `validate_metadata` y ningun call site pasando implicitamente | **PASS** | Barrido AST de TODO `*.py` del repo (no grep): **0 portadores** de `domain_pii_terms` con default, ni posicional, ni keyword-only, ni posicional-only, ni en lambda, ni en metodo, ni anidado. Las cuatro guardas exigen el parametro: `title_is_safe:543`, `contains_pii:551`, `validate_metadata:571`, `require_safe_text:767`. Los **11** call sites de `validate_metadata` pasan 3+ argumentos: **1 de produccion** (`build_memory_db.py:712`, cinco args, terminos desde `policy`) y **los 10 de test** (`:305, :312, :317, :494, :519, :524, :562, :878, :1182, :1185`) con `[]` literal. Cero llamadas con `*args`/`**kwargs`. Los diez que faltaban estan cubiertos. |
| **B -- F2 por propiedad, no por dos nombres** | 0 violaciones, sin citar lineas ni nombres de funcion, y muere con un quinto portador | **SLIP-0327-2** | 0 violaciones: confirmado (baseline `test_p01` exit 0). Sin coordenadas codificadas en la ASERCION: confirmado -- `assertEqual([], violations)`; los `fichero:linea` que aparecen son la ubicacion DESCUBIERTA en el mensaje de fallo, que es lo deseable. **Muere con un quinto portador: solo si es `def`/`async def` y esta en uno de los tres modulos enumerados.** Tabla de once colocaciones arriba. |
| **C -- el quinto portador de manana** | Lo anado yo y el gate debe caer | **PARCIAL -- SLIP-0327-2** | Cae en 7 de 7 colocaciones `def` (incluidas metodo, anidada, async y posicional-only, en los tres modulos). **NO cae** con lambda en los tres modulos (N6) ni con `def` en `revive_pack.py` / `dump_memory_db.py` (N12/N13). |
| **D -- sin regresion** | Los tres agujeros siguen cerrados y la suite verde | **PASS** | Los tres negativos por consecuencia siguen con dientes: **M1** publicacion con la fontaneria cortada -> exit 1; **M2** ingesta idem -> exit 1; **M3** recuperacion `contains_pii(reason, [])` -> exit 1; **M4** guarda de publicacion **INALCANZABLE** con la llamada textualmente presente (`if False and ...`) -> exit 1. Suite completa 71 tests OK en 240.2s, exit 0. Los cinco gates exit 0. |
| AC2 (fail-closed por construccion) | Omitir = error de firma | **PASS en la firma** | `contains_pii("x")`, `title_is_safe("x")`, `validate_metadata(fm, agents)` -> `TypeError` los tres. El agujero de la iteracion 1 esta cerrado. |
| AC4 (contrato por consecuencia) | Tres negativos con dientes en CI | **PASS** | `NEG-MEMORY-DOMAIN-PII-{PUBLICATION,INGESTION,RETRIEVAL-REASON}` declarados y muertos por M1/M2/M3/M4. Y **el runner SI se ejecuta**: `.github/workflows/validate.yml:49` corre `python scripts/memory/test_memory_db.py`, asi que el chequeo de propiedad no es de los que se declaran y nunca corren. |
| AC5 (sin regresion) | Gates exit 0 en clon limpio | **PASS** | Los cinco, exit code real, arriba. |

## Residuales declarados (no bloquean)

- **R1 -- portador por default COMPUTADO (`**kwargs` + `setdefault`).** Un envoltorio
  `def compat_validate_metadata(fm, agents, **kwargs): kwargs.setdefault('domain_pii_terms', ())`
  reintroduce exactamente la propiedad danina -- omitir es gratis y silencioso -- sin declarar
  ningun default en el AST: `test_p01` exit 0 (N7). Lo dejo como residual y no como bloqueante
  porque cae fuera de la letra de la propiedad ("declarar un default") y su cierre general no es
  decidible estaticamente. Conviene que quede escrito: la propiedad ata la SINTAXIS del default,
  no la semantica de la omision.
- **R2 -- modulo nuevo en el motor.** Un `scripts/memory/publish_memory_db.py` creado manana con un
  portador es invisible (N8). El arreglo de SLIP-0327-2 (descubrir en vez de enumerar) lo cierra de
  paso.
- **R3 -- dos de los diez call sites de test no llevan motivo escrito.** `:317` y `:1185` pasan `[]`
  sin comentario; cada uno es la segunda llamada de un test cuya primera llamada si lo lleva. Ocho
  de diez cumplen forma y motivo. AC2 pide el motivo escrito; lo declaro por completitud, no como
  defecto.
- **R4 -- `test_p01` no es negativo permanente declarado.** No lleva marcador
  `PERMANENT_NEGATIVE:` ni contrato en el registro, asi que su degradacion futura no la delata
  `check_falsification_contracts.py`. Mi F2 no lo pedia; lo apunto como deuda barata.
- **R5 -- la medicion sigue siendo 0-a-0.** La politica viva declara cero `domain_pii_terms` y el
  corpus cero artefactos publicables. Toda la evidencia positiva es de fixture (legitima: no hay otra
  con corpus vacio). El dia que la instancia declare su primer termino, el recuento de artefactos
  marcados cambiara: eso sera el fix funcionando, no una regresion.

## Limite propio declarado

CPython 3.12 en Windows. Clon limpio para medir, clon separado para mutar, `git status --porcelain`
verificado vacio antes y despues de cada medicion. La suite completa (71 tests, ~240 s) la corri
entera una vez en el ancla; los mutantes se gatearon por el metodo de test que corresponde a cada
uno, no por la suite entera. No ejecute nada del producto: el encargo declara SIN PRODUCTO EN
ALCANCE. No juzgo aqui la cobertura de CI de otros runners (particion de TASK-0330); solo verifique
que el runner de este chequeo concreto si esta cableado.

## Recomendacion de cierre: CHANGE-REQUIRED

F1 esta cerrado de verdad y verificado de forma independiente: cero portadores en todo el repo, los
diez call sites explicitos, la omision es `TypeError`. F2 es un avance real y no cosmetico: el
chequeo resiste el cambio de coordenada, de orden y de colocacion, que es donde fallan casi todos
los contratos de este hilo. Lo que falta es que el propio chequeo deje de apoyarse en dos listas
escritas a mano, porque por las dos entra el quinto portador de manana con la forma dominante.

### Bucle de correccion esperado (iteracion 2 de 2)

- **F3 (obligatorio, una linea).** Que `test_p01` DESCUBRA los modulos del motor en vez de
  enumerarlos: todos los `*.py` de `scripts/memory/` excluyendo el propio fichero de test. Cierra
  N12, N13 y de paso R2. Falsable: con la lista descubierta, N12 y N13 pasan de exit 0 a exit 1.
- **F4 (obligatorio, una linea).** Anadir `ast.Lambda` al `isinstance` de
  `domain_pii_default_violations`. Ojo: `ast.Lambda` no tiene `.name`, asi que el filtro por tipo va
  antes de cualquier uso del nombre; el resto del cuerpo (posicionales, posicional-only,
  keyword-only) ya vale tal cual. Falsable: N6 pasa de exit 0 a exit 1.
- **F5 (recomendado, no bloqueante).** Corregir el comentario bajo la asercion y el texto del
  handoff: hoy afirman "every function in all three memory-engine modules" y el motor tiene cinco.
  Tras F3/F4 la afirmacion correcta es "toda funcion, incluidas lambdas, de todos los modulos de
  `scripts/memory/`". Una afirmacion que sobrevive al arreglo pero no al recuento es la misma clase
  de defecto un marco mas arriba.
- **Gates afectados:** `python scripts/memory/test_memory_db.py`,
  `python scripts/check_falsification_contracts.py --root .`,
  `python scripts/validate_collaboration_state.py --root .`,
  `python scripts/scan_encoding.py --root .`,
  `python scripts/scan_domain_neutrality.py --root .` -- los cinco por exit code en clon limpio.
- **Re-juicio mio sobre el commit de remediacion ANTES del done-flip.** Volvere a correr las trece
  colocaciones del banco (esperando que N6, N12, N13 y N8 pasen a rojo), los cuatro mutantes de
  regresion M1-M4 y los cinco gates.
- **Esta es la iteracion 2 de 2.** Si el re-juicio siguiente no cierra F3 y F4, escalo al operador
  humano la decision de alcance (cerrar la clase completa vs aceptar los residuales por escrito).

-- Analista
