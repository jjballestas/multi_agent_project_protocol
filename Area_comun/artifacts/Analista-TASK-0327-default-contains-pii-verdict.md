---
artifact_id: Analista-TASK-0327-default-contains-pii-verdict
task_id: TASK-0327
type: review_verdict
author: Analista
created_at: 2026-08-08
status: final
verdict: CHANGE-REQUIRED
implementation_commit: fef3f6b735a3467c374a39d905dcbc16ddbeae14
verified_head: be54985832ac85e503d75116cf271a32a65be4e7
contrasted_head: 330fb1c5
---

# TASK-0327 -- el default vacio de contains_pii: veredicto CHANGE-REQUIRED

Voz: Analista (revisor adversarial independiente). Hora local de emision: 2026-08-08 11:10 (UTC+2).
Alcance declarado por el encargo: **SOLO el hub. SIN PRODUCTO EN ALCANCE.** No ejecute nada del
producto.

## Ancla canonica y reproduccion

Clon limpio `D:/Aegis_Scratch/mapp/an0327/cc` desde el repo, `git checkout be549858`,
`git status --short` vacio. El commit de implementacion `fef3f6b7` es ancestro de `origin/main`.
Contraste posterior contra `origin/main` = `330fb1c5`: el unico cambio en las rutas de alcance entre
el ancla y HEAD es `scripts/memory/test_memory_db.py` (+35/-3), y pertenece al contrato AST de
TASK-0325 (`nested_else_break` / `nested_else_continue`), no a las guardas de 0327. **El hallazgo
bloqueante de abajo esta vivo tambien en `330fb1c5`.**

Gates recomputados por EXIT CODE real (sin tuberia; `$?` tras una tuberia devuelve el codigo de
`tail`, no el del gate):

    python scripts/memory/test_memory_db.py               -> exit 0   (70 tests, OK, 239.8s)
    python scripts/check_falsification_contracts.py --root . -> exit 0
    python scripts/validate_collaboration_state.py --root .  -> exit 0
    python scripts/scan_encoding.py --root .                 -> exit 0
    python scripts/scan_domain_neutrality.py --root .        -> exit 0

Los cinco verdes son reales. **No es el estado de los gates lo que bloquea el cierre: es lo que
ningun gate mira.**

## Respuesta a la pregunta que hiciste

> El inventario de call sites de `contains_pii` y `title_is_safe` es COMPLETO con los seis que nombra
> mi contrato, o hay alguna invocacion mas que quedo fuera del alcance sin que ningun gate lo delate?

**El inventario de INVOCACIONES es completo. El inventario de PORTADORES del default no lo es.**

Re-derive las invocaciones por AST (no por grep de texto) sobre todo `*.py` del repo, resolviendo
`ast.Call` por nombre y por atributo. Las llamadas de produccion son exactamente estas y ninguna mas:

    build_memory_db.py:547   contains_pii(value, domain_pii_terms)      <- interno a title_is_safe
    build_memory_db.py:604   title_is_safe(value, domain_pii_terms)     <- dentro de validate_metadata
    build_memory_db.py:617   contains_pii(value, domain_pii_terms)      <- dentro de validate_metadata
    build_memory_db.py:776   contains_pii(value, domain_pii_terms)      <- dentro de require_safe_text
    check_memory_db_drift.py:102  memory_db.contains_pii(str(value), domain_pii_terms)
    query_memory_db.py:206        memory_db.contains_pii(reason, policy["domain_pii_terms"])

No hay invocacion indirecta: cero `getattr` sobre el modulo o sobre los nombres de las guardas, cero
`eval`, cero despacho por `__dict__`. No hay copia del motor en el arbol (solo `scripts/memory/*.py`
y sus `.pyc`); no existe una plantilla exportable del motor en este repo que propague la firma vieja.
Tu enumeracion de seis es correcta y esta cerrada.

**Pero la tarea no trata de las seis llamadas.** Tu propio contrato lo dice en "El punto de diseno,
que es lo que de verdad hay que arreglar": *"el defecto es la FORMA del default: un parametro
opcional cuyo valor por defecto debilita el chequeo hace que la omision sea gratis e invisible.
Arreglar solo las tres llamadas deja el motor exactamente igual de expuesto al cuarto call site que
alguien escriba manana."* Barri entonces el eje correcto -- **que funciones DECLARAN
`domain_pii_terms` con default** -- y ahi el inventario del contrato se queda corto por uno.

## SLIP-0327-1 (BLOQUEANTE) -- `validate_metadata` conserva el default debilitante, y es el unico llamador de produccion de las dos funciones arregladas

Barrido AST de firmas en `scripts/**/*.py` del ancla:

    build_memory_db.py:543  def title_is_safe(value, domain_pii_terms)                    <- default retirado (OK)
    build_memory_db.py:551  def contains_pii(value, domain_pii_terms)                     <- default retirado (OK)
    build_memory_db.py:767  def require_safe_text(value, field, *, domain_pii_terms, pii_check=True)  <- requerido (OK)
    check_memory_db_drift.py:68  def _publicable_pii_errors(connection, domain_pii_terms) <- sin default (OK)
    build_memory_db.py:571  def validate_metadata(frontmatter, agents, domain_pii_terms=(), ...)   <- DEFAULT VIVO

`validate_metadata` ya llevaba `domain_pii_terms: Iterable[str] = ()` **antes** del arreglo
(`git show fef3f6b7^:scripts/memory/build_memory_db.py` linea 574) y **lo sigue llevando despues**.
No es una funcion cualquiera: es la que llama a `title_is_safe` (:604) y a `contains_pii` (:617). Es
decir, el unico camino de produccion por el que las dos funciones arregladas reciben la politica de
instancia pasa por un parametro que se puede seguir omitiendo gratis y en silencio.

### Falsacion por comportamiento (no por lectura)

Ejecutado contra el modulo del clon limpio en el ancla `be549858`:

    contains_pii("x")     -> TypeError: contains_pii() missing 1 required positional argument
    title_is_safe("x")    -> TypeError: title_is_safe() missing 1 required positional argument

    validate_metadata({"title": "nomina de Acme SL"}, {"Codex"})
        -> accepted={'title': 'nomina de Acme SL'}   warnings=[]        # ACEPTADO
    validate_metadata({"title": "nomina de Acme SL"}, {"Codex"}, ["Acme SL"])
        -> accepted={}                               warnings=['rejected frontmatter key title']

**Es el mismo par medido que tu contrato usa para probar el defecto** (`contains_pii("nomina de
Acme SL")` -> False / con `["Acme SL"]` -> True), un marco mas arriba, y sobrevive intacto al
arreglo. La garantia que AC2 promete -- *"omitirlo pasa a ser un error de firma, no una degradacion
silenciosa"* -- **no se cumple en el punto de entrada real de las dos guardas**.

### Por que esto no es una nota de estilo

1. **La omision ya es la forma mayoritaria en el arbol.** De las once invocaciones de
   `validate_metadata` en el repo, **una** pasa los terminos (`build_memory_db.py:712`, produccion) y
   **diez** los omiten (test_memory_db.py:303, 310, 315, 492, 517, 522, 560, 846, 1150, 1153). El
   "cuarto call site que alguien escriba manana" no es hipotetico: hay diez escritos hoy corriendo con
   el chequeo debil sin que nadie lo note.
2. **El gate que deberia atraparlo mira nombres, no la propiedad.**
   `test_p01_domain_pii_parameters_are_required` afirma exactamente dos `assertRaises(TypeError)`,
   uno por cada nombre citado en el AC. Es un test de FORMA. Un quinto portador escrito manana --
   o este cuarto, que ya existe -- pasa verde. Esta es la clase de la que ya hablamos: el contrato
   ata el helper, no el efecto.
3. **La entrega aplico el criterio de AC2 a un caso latente y no al otro.** El handoff clasifica
   `title_is_safe` como *"latent shape defect only. Its existing production call site already passed
   the terms"*, y aun asi le quita el default -- correctamente, porque AC2 va por forma y no por
   sintoma. `validate_metadata` esta exactamente en esa misma situacion (latente, produccion pasa los
   terminos) y **es estrictamente mas peligrosa**, porque es la puerta publica que el resto del motor
   usa. Arreglar la hoja latente y dejar el tronco latente con el default identico no es una linea
   defendible.

### Contraste que declaro porque juega en contra de mi tesis

En produccion el agujero esta **cerrado hoy**: `build_memory_db.py:712` pasa
`domain_pii_terms = policy["domain_pii_terms"]`, leido por blob. No hay fuga viva por esta via en el
ancla. SLIP-0327-1 es una **reapertura de la clase de defecto que la tarea existe para erradicar**,
no un fallo abierto medido. Por eso el bloqueante que declaro es acotado y de una linea, no un
rechazo de la entrega.

### Remediacion falsable que verifique yo mismo

Escribi el chequeo de PROPIEDAD que el AC deberia haber pedido -- *ninguna funcion de los tres
modulos del motor declara `domain_pii_terms` con default* -- y lo corri en el ancla:

    VIOLATIONS: 1
       scripts/memory/build_memory_db.py:571 def validate_metadata(... domain_pii_terms=() ...)
    PROPERTY_CHECK_EXIT = 1

Un solo hallazgo, el mio, y verde en cuanto se cierre. Sobrevive a cambio de coordenada, de orden y
de formato: no cita numeros de linea ni nombres de funcion, afirma la propiedad sobre el AST.

## Tabla vector por vector

| Foco | Que exigia | Veredicto | Evidencia |
|------|-----------|-----------|-----------|
| A -- inventario re-derivado | Ninguna invocacion fuera del alcance | **SLIP-0327-1** | Las 6 invocaciones estan completas y cerradas (AST, sin despacho indirecto, sin copia del motor). El **cuarto portador del default** -- `validate_metadata:571` -- quedo fuera y ningun gate lo delata. Falsado por comportamiento arriba. |
| B -- fixture por la ruta de produccion | El fixture no puede esquivar la guarda | **PASS** | Publicacion: el test llama `check_memory_db_drift._sweep_database(root, connection, artifacts, commit)`, la misma funcion que invoca `full_check` (:184), que es la rama `--full` del CLI (`main` -> `full_check`). Ingesta: `memory_db.load_cold_packs`, funcion de produccion usada por `build` y por `full_check`. Recuperacion: `query_memory_db.retrieve`, la API real. Ninguna ruta paralela. |
| C -- lista vacia literal para reproducir el estado ciego | Que nadie use `[]` para volver atras | **PASS** | Cero call sites de produccion pasan `[]`. Los seis pasan `domain_pii_terms` derivado de `memory_index_policy(root, commit)` o `policy["domain_pii_terms"]`. Los `[]` literales estan solo en tests de la capa estructural, donde el vacio es el sujeto de la prueba. Residual R2 abajo. |
| D -- mutantes de codigo muerto | Morir con la guarda presente pero inalcanzable | **PASS** | Cuatro mutantes propios, todos matan su negativo: **M1** (publicacion, fontaneria muerta: `domain_pii_terms = []` tras leer la politica) -> exit 1; **M2** (ingesta, idem en `load_cold_packs`) -> exit 1; **M3** (recuperacion, `contains_pii(reason, [])` con la guarda intacta) -> exit 1; **M4** (publicacion, guarda **inalcanzable**: `if _unreachable and ... contains_pii(...)`, llamada textualmente presente) -> exit 1. Los tres negativos atan que **los terminos LLEGUEN**, no solo que la linea exista. |
| E -- `title_is_safe` "latente, no abierto" | Confirmar o desmentir | **CONFIRMADO** | En `fef3f6b7^`, `title_is_safe` se invoca solo en `validate_metadata:604` con `domain_pii_terms`, y `:712` ya los pasaba desde `policy["domain_pii_terms"]`. El alcance real eran **tres** agujeros abiertos, no cuatro. Corolario incomodo: lo que mantenia a salvo a `title_is_safe` era justamente el parametro de `validate_metadata` cuyo default sigue vivo. |
| AC1 (falsacion previa) | Comportamiento, no lectura | **PASS** | Verificado en el diff pre/post: `check_memory_db_drift:99`, `build_memory_db:762` y `query_memory_db:205` no recibian terminos; `:541`/`:610` si. |
| AC2 (fail-closed por construccion) | Sin default en las funciones que lo llevan | **SLIP-0327-1** | Cumplido a la LETRA (las dos funciones citadas: `TypeError` verificado). Incumplido en el PROPOSITO: el tercer portador, que es el llamador de ambas, conserva el default. |
| AC3 (la politica llega de verdad) | Blob atestado; sin commitear no concede nada | **PASS** | `memory_index_policy` lee `git_blob(root, commit, POLICY_PATH)`. Verificado por comportamiento en la puerta que decide: politica declarada **sin commitear** -> `_sweep_database` no reporta nada; el **mismo** arbol tras commitear -> `publicable artifact contains PII: TASK-DOMAIN-PUBLIC`. El test de ingesta prueba lo mismo (1 fila admitida sin commit, `ValueError` con commit). |
| AC4 (contrato por consecuencia) | Tres negativos permanentes con dientes en CI | **PASS** | `NEG-MEMORY-DOMAIN-PII-{PUBLICATION,INGESTION,RETRIEVAL-REASON}` declarados en `FALSIFICATION_CONTRACTS` con `exercised_by`, y los tres mueren bajo M1/M2/M3/M4. |
| AC5 (sin regresion) | Gates exit 0 en clon limpio | **PASS** | Los cinco gates, exit code real, arriba. |
| F -- el "47/47" | No leerlo como cobertura | **ACEPTADO, no usado** | Lo trato como lo que es: `check_falsification_contracts.py` verifica DECLARACION. Su exit 0 lo cuento como gate verde y **no** como afirmacion de que esos 47 contratos se ejecuten. Mi juicio de dientes no descansa en ese numero sino en los cuatro mutantes que corri yo. |

## Residuales declarados (no bloquean)

- **R1 -- la medicion 0-a-0 sigue siendo 0-a-0.** Confirmo el recuento del handoff: la politica viva
  declara cero `domain_pii_terms` y el corpus cero artefactos publicables. Toda la evidencia positiva
  es de fixture. Es legitimo (no hay otra forma con corpus vacio) y el foco B queda cerrado porque el
  fixture recorre la ruta real, pero conviene que quede escrito: **el dia que la instancia declare su
  primer termino, el recuento de artefactos marcados cambiara y eso sera el fix funcionando, no una
  regresion.** No hay linea base viva contra la que medirlo hoy.
- **R2 -- los `[]` de los tests no llevan motivo escrito.** AC2 pide que un call site que corra sin
  terminos lo declare "pasando una lista vacia LITERAL y el motivo va escrito en el codigo". Los
  `[]` de `test_p01`/`test_p05`/`test_p07` cumplen la forma y no el motivo. Son tests de la capa
  estructural, donde el vacio ES el sujeto; lo declaro por completitud, no como defecto.
- **R3 -- `require_safe_text(..., pii_check=False)` en `created_at` (`:820`).** Es el patron BUENO
  (apagar exige escribirlo) y territorio de TASK-0325. Fuera de alcance, sin objecion.
- **Particion respetada:** no cuento aqui el sexto rojo del fixture de retry, particionado por
  TASK-0330.

## Limite propio declarado

Medi con CPython 3.12 en Windows. Los tres negativos y los cuatro mutantes se ejecutaron en el clon
limpio; la suite completa (70 tests) tarda ~240 s y la corri entera una vez en el ancla, y por test
individual para cada mutante. No ejecute nada del producto: el encargo declara SIN PRODUCTO EN
ALCANCE.

## Recomendacion de cierre: CHANGE-REQUIRED

Un unico bloqueante acotado, SLIP-0327-1. La entrega es solida en todo lo demas: las tres puertas
estan cerradas de verdad, la politica llega por blob atestado, los negativos tienen dientes contra el
mutante de codigo muerto y el fixture no esquiva la guarda. Lo que falta es que el arreglo alcance al
portador que de verdad gobierna la forma.

### Bucle de correccion esperado

- **F1 (obligatorio).** Quitar el default de `domain_pii_terms` en `validate_metadata`
  (`build_memory_db.py:571`), de modo que la omision sea `TypeError` igual que en las otras dos.
  Actualizar los diez call sites de test que hoy lo omiten para que pasen su lista explicita (`[]`
  con motivo escrito donde el vacio sea el sujeto de la prueba).
- **F2 (obligatorio, es lo que evita la quinta ocurrencia).** Convertir
  `test_p01_domain_pii_parameters_are_required` de una lista de dos nombres en una **afirmacion de
  propiedad sobre el AST**: ninguna funcion de `build_memory_db.py`, `check_memory_db_drift.py` ni
  `query_memory_db.py` puede declarar un parametro `domain_pii_terms` con default. Verificado por mi:
  hoy da 1 violacion (la de F1) y quedara en 0 al cerrarla. Sin F2, F1 arregla esta ocurrencia y deja
  la clase abierta.
- **Gates afectados:** `scripts/memory/test_memory_db.py`,
  `scripts/check_falsification_contracts.py --root .`,
  `scripts/validate_collaboration_state.py --root .`, `scripts/scan_encoding.py --root .`,
  `scripts/scan_domain_neutrality.py --root .` -- los cinco por exit code en clon limpio.
- **Re-juicio mio sobre el commit de remediacion ANTES del done-flip.** Volvere a correr el chequeo
  de propiedad y los cuatro mutantes, y anadire un mutante nuevo: un portador de `domain_pii_terms`
  con default inyectado en otro de los tres modulos, que debe enrojecer F2.
- **Maximo 2 iteraciones** antes de escalar al operador humano.

-- Analista
