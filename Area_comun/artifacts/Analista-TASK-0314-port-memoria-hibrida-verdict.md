---
artifact_id: Analista-TASK-0314-port-memoria-hibrida-verdict
reviewer: Analista
task_id: TASK-0314
spec_id: SPEC-MEMORIA-HIBRIDA
type: review-verdict
verdict: CHANGE-REQUIRED
closable: false
created_at: 2026-08-06
local_time: "2026-08-06 05:15 (reloj del sistema, UTC+2, sin convertir)"
anchors:
  implementation_commit: 378021d6340c000347adb0450983a6e0909129b5
  protocol_head: 070ddae20c741fe2ee76354f6e0383899cd3256c
  origin_main: 070ddae20c741fe2ee76354f6e0383899cd3256c
  clean_clone: D:/Aegis_Scratch/protocol/ana314
---

# Veredicto Analista -- TASK-0314 (F1-PORT del motor de memoria hibrida al master neutral del hub)

**CHANGE-REQUIRED.** No cerrable en este commit.

Alcance de producto: NINGUNO, tal como declaro la instruccion. No corri `npm test` de ningun repo de
producto; no aplica. Todos los gates de abajo son los de Python del hub.

## 1. Ancla canonica y reproduccion

Clon limpio nuevo (`git clone` del hub + `git checkout 378021d`), fuera del arbol caliente, en ruta
corta bajo el scratch root de DECISION-0104: `D:/Aegis_Scratch/protocol/ana314`.
`git status --porcelain` vacio tras el checkout. Gateo por EXIT CODE directo, sin pipe.

| Gate | Comando | Exit | Evidencia |
|---|---|---|---|
| Suite | `python scripts/memory/test_memory_db.py` | **0** | `Ran 55 tests in 253.104s -- OK` |
| Build corpus real | `python scripts/memory/build_memory_db.py --root .` | **0** | 4154 artefactos, 211 eventos, 15 tablas, `schema_version` 1, `foreign_keys` 1, 238 warnings |
| I2 read-only | `git status --porcelain` tras el build | **vacio** | ningun archivo trackeado modificado |
| Drift rapido | `python scripts/memory/check_memory_db_drift.py --fast --root .` | **0** | `result: pass`, `database_read: false` (I5 respetado) |
| Drift completo | `python scripts/memory/check_memory_db_drift.py --full --root .` | **0** | `result: pass`, `round_trip: pass`, `sweep: bidirectional-pass`, `database_written: false` |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** | `OK: encoding scan is clean.` |
| Neutralidad | `python scripts/scan_domain_neutrality.py --root .` | **0** | sin hallazgos -- **pero ver F4: el gate no cubre lo entregado** |
| Estado canonico | `python scripts/validate_collaboration_state.py --root .` | **0** | `OK: collaboration state is valid.` |

Frontera respetada: verifique el diff de `378021d` y no toca `validate_collaboration_state.*`,
`submit_intent.py`, `protocol.config.json`, `agent_registry`, el genesis ni `runtime/state/`.
12 archivos, +3863/-4. El unico output del indexador es `runtime/memory/index.db`, gitignored.

## 2. Hallazgos

### F1 -- BLOQUEANTE (P11 / AC7): `revive_pack` no acota, aborta. Confirmado, y con causa distinta a la declarada

Reproduje los tres comandos por mi cuenta sobre el corpus real en el clon limpio:

    Arquitecto -> exit 2, ERROR: revive pack exceeds declared budget: 161465 > 131072 bytes
    Codex      -> exit 2, ERROR: revive pack exceeds declared budget: 194752 > 131072 bytes
    Analista   -> exit 0, 37166 bytes

No existe via de degradacion: `parse_args` no expone ninguna bandera de recorte y
`revive_pack.py:483` es una asercion dura (`raise ValueError`) al final de `compose_pack`; `main()`
devuelve 2. Confirmado por lectura y por comportamiento.

**Corrijo el diagnostico de causa de tu capa.** Tu hipotesis era que el exceso lo aportan
"sesiones/tareas/mailbox/decisiones que no entran en ese recorte". No es eso. Instrumente
`compose_pack` (monkeypatch de `memory_index_policy` para elevar `max_bytes` y poder MEDIR el pack
que se descarta) y descompuse los dos packs que fallan:

| Agente | TOTAL | inline declarado | seccion 6 (omisiones) | atestacion | resto (secciones 1-5) |
|---|---|---|---|---|---|
| Arquitecto | 161467 | 35894 | **119293 (74%)** | 2557 (14 filas) | ~3546 |
| Codex | 194754 | 41957 | **139406 (72%)** | 5744 (29 filas) | ~7391 |
| Analista | 37168 | 28604 | 468 | 3897 (21 filas) | ~180 |

El presupuesto por fuente **si funciona**: 35894 y 41957 estan por debajo de los 65536 de
`max_inline_source_bytes`. Lo que revienta el total es **la propia declaracion de exclusion**: un
objeto JSON por archivo omitido, **291 entradas para el Arquitecto y 300 para Codex** (todas de
`kind: memory`), sin presupuesto propio.

Es decir: **el mecanismo de degradacion es lo que rompe el presupuesto**. Cuanto mas degrada el
pack, mas grande se hace. Es una inversion de diseno, no un tope mal calibrado. Consecuencia
practica: la capacidad REVIVE -- el titular que DECISION-0100 adopto por demostracion -- no emite
pack para 2 de los 3 agentes registrados del hub, y empeora conforme crezca `personal/<id>/`.

AC7 pide "presupuesto declarado ... y declaracion explicita de lo que quedo fuera". Se emiten
ambos, pero solo en el pack que no llega a existir. Por comportamiento, AC7 NO se cumple.

**Fix requerido:** acotar tambien la seccion 6 (agregado determinista: conteo por `kind`, bytes
totales, top-N por recencia, o la lista completa en un artefacto lateral referenciado por sha) y
convertir el chequeo de `max_bytes` en un lazo de degradacion que converja, no en una asercion.
**Subir `max_bytes` NO es fix aceptable**: relaja la garantia declarada y no converge, porque la
lista crece con el corpus.

### F2 -- BLOQUEANTE (AC2): la validacion PII por VALOR esta apagada en las claves de fecha, y es gratuito

`build_memory_db.py:579` exime a `created_at`/`updated_at`/`closed_at` del chequeo `contains_pii`.
`DATE_RE` (`^\d{4}-\d{2}-\d{2}(?:T[^\s]+)?$`) admite texto arbitrario sin espacios en la cola `T...`.
Combinados, dejan entrar PII al indice. Probado por comportamiento en el clon limpio:

    validate_metadata({"created_at": "2026-06-19Tperson@example.invalid"}, {"Codex"})
      -> accepted={'created_at': '2026-06-19Tperson@example.invalid'}, warnings=[]
    contains_pii("2026-06-19Tperson@example.invalid") -> True

Y extremo a extremo, construyendo una instancia fixture y corriendo el build real:

    DB ROW: ('TASK-9001', '2026-06-19Tvictim@example.invalid', None)
    check_memory_db_drift._publicable_pii_errors(con) -> []
    contains_pii(valor_almacenado) -> True

El email queda en la columna `artifacts.created_at`, y el barrido de plano publico del `--full` NO
lo caza (solo mira `title`, `summary_short`, `summary_long`, `owner`, `plain_text_excerpt`).

**La exencion no compra nada.** Probe seis formatos de marca de tiempo bien formados y NINGUNO
dispara `contains_pii`:

    2026-06-19 / 2026-06-19T09:28:23Z / 2026-08-06T02:45:00Z /
    2026-01-01T00:00:00+02:00 / 2026-06-19T092823Z / 2026-06-19T09:28:23.123456Z   -> todos False

O sea: se desactivo una validacion que nunca habria disparado sobre entrada legitima, y a cambio se
abrio un hueco. AC2 lo prohibe con esas palabras: "Prohibido resolver un rechazo desactivando su
validacion o admitiendo texto libre en el indice".

No afirmo que el maker introdujera la exencion: no puedo diferenciar contra el original de
Nova-Payroll porque ese arbol no esta en este repo. Afirmo que **esta presente en el master
entregado** y que incumple AC2 tal como esta escrito.

**Fix requerido:** eliminar la exencion de claves de fecha (es innecesaria) y/o anclar `DATE_RE` a
una gramatica real de timestamp. Test de regresion con el payload de arriba.

### F3 -- BLOQUEANTE de AC5 (menor en esfuerzo): `priority: medium` -> 19 rechazos de metadata BIEN FORMADA

Conteo independiente sobre el corpus: `priority: medium` aparece **19 veces**. Descompuse los 238
warnings del build por clave:

    spec_id 123 | task_id 86 | priority 19 | decision_id 6 | to 2 | relates_to 1 | supersedes 1

Los 219 que no son `priority` son malformacion real. Inspeccione los cuatro casos no obvios y los
cuatro son H2 legitimo:

- `SPEC-0057`: `relates_to: [PACKAGE_VERSIONING, SPEC-0043]` -- `PACKAGE_VERSIONING` no es id anclado.
- `ANALISTA-TASK-0276`: `supersedes: <id> (CHANGE-REQUIRED, iter1)` -- cola de texto libre.
- `MSG-20260613-*`: `to: Claude,Claude-analista` -- lista por coma en campo escalar.
- `DRAFT-DECISION-0039`: `decision_id: DECISION-0039 (DRAFT - id final al promover)` -- placeholder.

Los 19 de `priority` NO son eso: `medium` es vocabulario bien formado del hub y `PRIORITY_VALUES` no
lo incluye. AC5 exige literalmente que "los warnings restantes deben ser SOLO frontmatter realmente
malformado (H2 de s.16.4), **no metadata bien formada del hub**". Con estos 19, AC5 no se cumple.

Coincido con tu hallazgo menor; discrepo en la clasificacion: contra la letra de AC5 es el unico
criterio que rompe, no un detalle cosmetico. Es de la misma clase que P9 y el fix es una linea mas
un test.

### F4 -- CONFIRMADO, NO imputable al maker: el gate de neutralidad NO cubre la superficie entregada

`protocol.config.json.domain_neutrality.scan_globs` trae `scripts/*.py`, y `glob_to_regex` mapea `*`
a `[^/]*`, que no cruza `/`. Por tanto **`scripts/memory/*.py` (las 3863 lineas nuevas, el motor
entero) nunca se escanea**, ni tampoco `Area_comun/protocol/MEMORY_INDEX_POLICY.json`
(`Area_comun/protocol/*.md` solo cubre `.md`).

Falsificado, no deducido. En una raiz de scratch con el `protocol.config.json` real:

    scripts/memory/build_memory_db.py  <- contiene "binance spot backtest trading"
    Area_comun/protocol/MEMORY_INDEX_POLICY.json <- domain_pii_terms: ["trading","binance"]
    python scan_domain_neutrality.py --root .   -> EXIT 0    (ciego)

    scripts/flat_poison.py <- contiene "trading"
    python scan_domain_neutrality.py --root .   -> EXIT 1    (lo caza)

Y en el clon limpio real, `iter_scanned_files` selecciona **127 archivos, ninguno bajo
`scripts/memory/`** y ninguno que sea el policy nuevo.

Conclusion: el exit 0 de AC1 / DoD s.16.5 punto 2 es CIERTO pero VACIO para esta entrega. Hoy la
neutralidad P1-P4 del motor la sostiene un unico test unitario con 3 terminos legacy escritos a mano
(`test_p01`), sobre un solo modulo (`build_memory_db.py`), no el gate del repo. Eso es un test util,
pero no es una frontera mecanica: cualquier termino de dominio distinto de esos tres, en cualquiera
de los seis scripts, entra sin que ningun gate lo note.

**Atribucion: no es defecto del maker.** El `out_of_scope` de TASK-0314 prohibe expresamente tocar
`protocol.config.json`, y `scripts/scan_domain_neutrality.py` no esta en `scope_routes`. El maker no
tenia ninguna ruta en alcance para cerrarlo. Es un hueco de contrato que te toca a ti decidir:
extender `scan_globs` (pero el config esta pineado por el hash del genesis, asi que exige frontera de
re-genesis), o anadir en el escaner una regla de auto-append para `scripts/**` con el mismo patron
que ya usa para `connectors/**` y `skills/**` -- eso es codigo, no config pineado, y no requiere
re-genesis. Recomiendo la segunda, en tarea aparte. **No la imputo a este cierre**, pero AC1 no
deberia declararse "verificada por gate" mientras siga asi.

## 3. Residuales declarados (no bloquean)

- **R1 -- bypass del patron de telefono para todo valor con forma de id.** El fix de P5 excluye del
  chequeo de telefono cualquier `item` que case `ID_RE`. Medido: `contains_pii("TEL-34612345678")`
  -> False; `contains_pii("MSG-612345678")` -> False. Lo declaro porque es una superficie real, pero
  **la accion requerida de P5 en s.16.3 autoriza expresamente esta opcion** ("Excluir del patron de
  telefono los ids que casan `ID_RE`"). Es un intercambio sancionado por el contrato, no un defecto.
  Queda como riesgo conocido y decidido.
- **R2 -- IBAN solo en forma contigua.** `contains_pii("ES9121000418450200051332")` -> True, pero
  `"ES91 2100 0418 4502 0005 1332"` y `"ES91-2100-0418-4502-0005-1332"` -> False (los separadores
  rompen el ancla tanto en el crudo como en el normalizado). No lo introdujo el port -- el patron
  fallaba igual antes -- pero importa cuando el motor se exporte a instancias con datos bancarios
  reales. Mismo efecto en `title_is_safe`.
- **R3 -- el barrido de plano publico ignora los terminos de dominio de la instancia.**
  `check_memory_db_drift._publicable_pii_errors` llama `contains_pii(value)` **sin**
  `domain_pii_terms`. En el hub es inocuo (lista vacia); en Nova-Payroll, la instancia de origen, el
  build aplicaria los terminos y el barrido del `--full` NO. Recomiendo pasar la politica tambien
  ahi.
- **R4 -- el test de P11 no puede fallar como falla el corpus real.** Su fixture produce **1** entrada
  omitida, asi que `assertLessEqual(len(pack), 65536)` pasa sin ejercitar nunca el crecimiento de la
  seccion 6, que es exactamente el modo de fallo. AC3 pide un test por hallazgo; el test existe, pero
  no es falsador de su propio criterio. Cualquier fix de F1 debe traer un test con orden de magnitud
  de omisiones comparable al real (300+).

## 4. Sobre los 238 warnings y la enmienda P12b/P12c -- contraste pedido

**Coincido con tu lectura y no se la imputo al maker.** Verifique la muestra: los 215 de
`spec_id`/`task_id`/`decision_id` son centinelas `none`, rutas en campo de id, listas por coma y
placeholders de borrador; los 4 casos no obvios que inspecciono uno a uno son malformacion real por
la gramatica del propio contrato. Reescribir 206 artefactos gobernados para complacer al indice seria
la direccion equivocada: el indexador falla cerrado y eso es correcto. Que la correccion vaya por una
enmienda del contrato al indexador me parece bien.

Mi unica divergencia es de perimetro, no de criterio: dentro de esos 238 venian tambien 19 de
`priority`, que **no** son H2 (F3). Al contarlos todos como "categorias H2" se hacen invisibles.

## 5. Tabla criterio por criterio

| AC | Criterio | Resultado | Nota |
|---|---|---|---|
| AC1 | Neutralidad P1-P4, lexico fuera del nucleo, `project` derivado, dump neutro, scan exit 0 | **PASS con salvedad** | P1-P4 implementados y verificados por lectura + test; el gate exit 0 es **vacio** para lo entregado (F4) |
| AC2 | Calibracion P5-P10/P12 sin relajar garantias | **SLIP** | F2: validacion PII apagada en claves de fecha, con fuga probada extremo a extremo |
| AC3 | Suite verde completa + un test por hallazgo + negativo de lexico | **PASS con salvedad** | 55/55 exit 0; el test de P11 no falsa su propio criterio (R4) |
| AC4 | `.gitignore` + exclusion en ambos `scan_encoding` + exit 0 | **PASS** | verificado en clon limpio, exit 0 |
| AC5 | Gates sobre corpus real; warnings restantes SOLO H2 | **SLIP** | build/fast/full exit 0 y round-trip byte a byte PASS, pero 19 warnings son metadata bien formada (F3) |
| AC6 | I2 read-only; `git status` vacio; validate exit 0 antes y despues | **PASS** | `git status --porcelain` vacio tras build y tras `--full`; validate exit 0 |
| AC7 | `revive_pack` acotado, con presupuesto, seleccion, resumen determinista, `token_estimate`, omisiones declaradas | **FAIL** | F1: aborta para 2 de 3 agentes registrados; no hay via de degradacion |
| AC8 | Export a instancias con test | **PASS** | `test_new_instance_exports_complete_memory_toolchain` ejecuta `copy_gate_scripts` y comprueba los 6 scripts + mapeo del template + `.gitignore` |

Cosas que ataque y NO logre romper, para que conste: la politica configurable esta acotada de verdad
(schema_version fijo, claves cerradas, arrays <= 128, strings <= 100 imprimibles, sin duplicados,
`max_bytes` <= 1 MiB, `max_inline_source_bytes <= max_bytes`); los enums siguen finitos (36 status /
69 type) y `validate_metadata` rechaza `"arbitrary status"`/`"arbitrary type"`; P12 acepta `[]` y
rechaza `""`, `None`, `{}` y `["not an id"]`; `ID_RE` sigue anclado y sensible a mayusculas; el
`--fast` no abre la DB (`database_read: false`) y el `--full` conecta en `mode=ro`; el clon interno
del round-trip usa `tempfile`, no una raiz de disco; y el pack solo lee `agent_memory` del propio
agente, no las areas personales ajenas.

## 6. Recomendacion de cierre

**CHANGE-REQUIRED.** Remediacion minima para volver a juicio:

1. **F1 (AC7):** acotar la seccion 6 y convertir `max_bytes` en degradacion convergente. Prueba de
   aceptacion: `revive_pack.py <agente> --root .` exit 0 y `<= 131072` bytes para **los tres**
   agentes del `agent_registry` sobre el corpus real, con la declaracion de omisiones presente y
   determinista. Sin subir `max_bytes`.
2. **F2 (AC2):** quitar la exencion PII de las claves de fecha y/o anclar `DATE_RE`; test de
   regresion con `created_at: 2026-06-19Tperson@example.invalid` que debe quedar rechazado.
3. **F3 (AC5):** `medium` en `PRIORITY_VALUES` + test; el build debe bajar a 219 warnings, todos H2.
4. **R4:** el test de P11 debe reproducir el orden de magnitud real de omisiones (300+), no 1.

Gates a recomputar tras la remediacion, todos por exit code en clon limpio: `test_memory_db.py`,
`build_memory_db.py --root .`, `check_memory_db_drift.py --fast` y `--full`, `scan_encoding.py`,
`scan_domain_neutrality.py`, `validate_collaboration_state.py`, mas los tres `revive_pack` y
`git status --porcelain` vacio tras el build.

**F4 no entra en el lazo de remediacion del maker** (estaba fuera de su alcance): va como tarea
aparte tuya. Sugiero no declarar AC1 "verificada por gate" hasta que exista.

Lazo declarado: **maximo 2 iteraciones**. Si tras la segunda F1 o F2 siguen abiertos, escalo al
operador humano en vez de seguir iterando.

-- Analista (checker independiente), 2026-08-06 05:15 hora local del sistema (UTC+2)
