---
artifact_id: Analista-TASK-0314-remediacion-r2-verdict
reviewer: Analista
task_id: TASK-0314
spec_id: SPEC-MEMORIA-HIBRIDA
type: review-verdict
verdict: OK-CLOSABLE
closable: true
created_at: 2026-08-06
local_time: "2026-08-06 07:21 (reloj del sistema, UTC+2, sin convertir)"
anchors:
  implementation_commit: d1252f49d4b8f2b8bdae01f18035759468d972e0
  protocol_head: 0a66a3688a0d090e1e3adae5c8eeb9741c88dab1
  origin_main: 0a66a3688a0d090e1e3adae5c8eeb9741c88dab1
  clean_clone_suite: D:/Aegis_Scratch/protocol/ana314b
  clean_clone_corpus: D:/Aegis_Scratch/protocol/ana314c
  clean_clone_mutation: D:/Aegis_Scratch/protocol/ana314d
---

# Veredicto Analista -- TASK-0314 r2 (remediacion de F1, F2, F3 y R4)

**OK-CLOSABLE.** Los cuatro items del lazo estan cerrados y verificados por comportamiento en clon
limpio. Declaro un residual **nuevo (R5) que introdujo la propia remediacion** y que no rompe ningun
criterio de aceptacion sobre el corpus anclado, pero que debe quedar registrado antes de exportar el
motor a cualquier instancia.

Alcance de producto: NINGUNO, tal como declaro la instruccion. No corri `npm test` de ningun repo de
producto. Todos los gates de abajo son los de Python del hub.

## 1. Ancla canonica y reproduccion

Tres clones limpios propios (`git clone` del hub + `git checkout d1252f4`), fuera del arbol caliente,
en rutas cortas bajo el scratch root de DECISION-0104. `git status --porcelain` vacio tras cada
checkout. Gateo por EXIT CODE directo, sin pipe.

| Gate | Comando | Exit | Evidencia |
|---|---|---|---|
| Suite | `python scripts/memory/test_memory_db.py` | **0** | `Ran 57 tests in 341.612s -- OK` |
| Build corpus real | `python scripts/memory/build_memory_db.py --root .` | **0** | 4162 artefactos, 226 eventos, 15 tablas, `schema_version` 1, `foreign_keys` 1, **219** warnings |
| I2 read-only | `git status --porcelain` tras el build | **vacio** | ningun archivo trackeado modificado |
| Drift rapido | `check_memory_db_drift.py --fast --root .` | **0** | `result: pass`, `database_read: false` (I5 respetado) |
| Drift completo | `check_memory_db_drift.py --full --root .` | **0** | `result: pass`, `round_trip: pass`, `sweep: bidirectional-pass`, `database_written: false` |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** | `OK: encoding scan is clean.` |
| Neutralidad | `python scripts/scan_domain_neutrality.py --root .` | **0** | sin hallazgos (ver salvedad en s.5: solo vale si NO hay pack materializado en el repo) |
| Estado canonico | `python scripts/validate_collaboration_state.py --root .` | **0** | `OK: collaboration state is valid.` |
| revive_pack x4 | `revive_pack.py <agente> --root .` | **0** | Arquitecto 119309, Codex 95219, Analista 48775, Operador 3008 bytes (techo 131072) |

Mis cifras de los tres agentes que tu recomputaste coinciden **byte a byte** con las tuyas y con las
del maker, sobre tres arboles independientes. Anado `Operador`, el cuarto registrado, que tampoco
estaba cubierto antes.

Frontera respetada: el diff de `d1252f4` toca 3 archivos (`build_memory_db.py`, `revive_pack.py`,
`test_memory_db.py`), +158/-48. No toca `validate_collaboration_state.*`, `submit_intent.py`,
`protocol.config.json`, `agent_registry`, el genesis ni `runtime/state/`.

## 2. Los cuatro items del lazo

### F1 (AC7) -- CERRADO. El lazo converge, termina y es determinista

No me quede en la prueba de aceptacion; ataque las tres propiedades que pediste.

**(a) Terminacion, incluido el peor caso.** El lazo es
`detail_limit = len(omitted_entries)` y luego `detail_limit //= 2` hasta 0. En enteros, `1 // 2 == 0`,
asi que la secuencia es estrictamente decreciente y alcanza 0 en `floor(log2(n)) + 1` pasos; en 0
renderiza una vez mas y, si no cabe, lanza. **No existe entrada que lo haga divergir ni entrar en
bucle**: no hay rama que aumente `detail_limit` ni que lo deje igual. Lo falsee ademas por
comportamiento, forzando el peor caso absoluto (`max_bytes` = 1 por monkeypatch de la politica, que
es tu "un solo archivo cuyo agregado minimo ya no quepa"):

    raised in 13.35s: revive pack fixed content exceeds declared budget after
    deterministic omission degradation: 55750 > 1 bytes

Termino, con mensaje distinto y explicito, sin colgarse. **La garantia es "converge o aborta con
diagnostico", no "siempre emite"**: el fix acota la seccion 6, no las secciones 1-5 ni la atestacion.
Eso es correcto para AC7 y esta medido en s.3 (R6).

**(b) Convergencia real, no asercion movida de sitio.** El lazo degrada de verdad sobre el corpus
real, y queda holgura:

| Agente | omisiones | detalles emitidos | detalles recortados | bytes omitidos | pack final |
|---|---|---|---|---|---|
| Arquitecto | 291 | 145 | 146 | 1346388 | 119309 |
| Codex | 300 | 75 | 225 | 1112044 | 95219 |
| Analista | 1 | 1 | 0 | 494779 | 48775 |
| Operador | 0 | -- | -- | -- | 3008 |

La declaracion de exclusion sigue siendo completa en agregado (`omitted_entries_total`,
`omitted_bytes_total`, `by_kind` con conteo y bytes por tipo) aunque el detalle se recorte: AC7 pide
"declaracion explicita de lo que quedo fuera" y eso se cumple sin depender del detalle. La inversion
de diseno que reporte en r1 (cuanto mas degrada, mas crece) esta invertida de vuelta.

**(c) Determinismo entre corridas.** Compuse cada pack dos veces en el mismo arbol y compare bytes:

    Arquitecto deterministic=True | Codex deterministic=True
    Analista   deterministic=True | Operador deterministic=True

El orden viene de `sorted(..., key=(recency, kind, path), reverse=True)`; `path` es unico por
entrada, asi que el desempate es total y no depende del orden de llegada. `_omission_recency` cae a
`""` cuando falta la fecha (caso `kind: decision`, que no lleva ninguna de las cuatro claves), lo que
es estable, no aleatorio.

Nota menor, no defecto: el halving entrega el primer limite que cabe, no el mayor que cabria (Codex
baja 300 -> 150 -> 75 cuando ~140 habrian cabido). AC7 pide acotado, declarado y determinista; las
tres se cumplen. Lo dejo dicho por si algun dia interesa afinar.

### F2 (AC2) -- CERRADO, y las dos capas son independientes

**Capa 1 (la que cierra el agujero): quitada la exencion.** `validate_metadata` ahora aplica
`contains_pii` a **todas** las claves. Eso solo ya hace imposible el escape original, con
independencia de la gramatica.

**Capa 2: `DATE_RE` anclada a gramatica finita.** Verifique que no admite cola inyectable de forma
constructiva, no por muestreo: genere sistematicamente la familia completa de la gramatica (333
cadenas: 3 fechas x {HH:MM:SS, HHMMSS, 00:00:00, 23:59:59} x 7 fracciones x 5 offsets) y extraje el
**alfabeto alcanzable** a traves de `DATE_RE`:

    +-.0123456789:TZ

Sin `@`, sin dos letras consecutivas y sin ninguna letra fuera de `T`/`Z`. Por construccion, **ninguna
cadena aceptada por `DATE_RE` puede contener un email, un IBAN (`[A-Z]{2}\d{2}[A-Z0-9]{10,30}`) ni
`NIF|NIE|NIT|DNI|SSN`**. No es que no los haya encontrado: no caben en el alfabeto.

Cola por cola, los 11 vectores que la gramatica vieja admitia y la nueva debe rechazar:

    OLD=True NEW=False  2026-06-19Tperson@example.invalid      (tu payload de r1)
    OLD=True NEW=False  2026-06-19TES9121000418450200051332    (IBAN)
    OLD=True NEW=False  2026-06-19T+34612345678                (telefono)
    OLD=True NEW=False  2026-06-19T612345678                   (telefono sin prefijo)
    OLD=True NEW=False  2026-06-19T0000000000000               (13 digitos)
    OLD=True NEW=False  2026-06-19TDNI                         (identificador)
    OLD=True NEW=False  2026-06-19Ttrading                     (termino de dominio)
    OLD=True NEW=False  2026-06-19T../../etc/passwd            (ruta)
    OLD=True NEW=False  2026-06-19T<script>                    (markup)
    OLD=True NEW=False  2026-06-19T09:28:23Z;DROP              (cola SQL)
    OLD=True NEW=False  2026-06-19T\x00                        (byte nulo)

Los 11 quedan ademas rechazados por `validate_metadata` (`accepted={}`). El payload exacto de mi r1
sale `({}, ['rejected frontmatter key created_at'])`.

**Sin regresion en el corpus real.** Escanee los 4586 archivos de texto del clon en `d1252f4`,
extraje los **134 valores distintos** de `created_at`/`updated_at`/`closed_at` y compare gramatica
vieja contra nueva: **0 valores aceptados antes y rechazados ahora**, y **0 valores que la gramatica
nueva acepte y `contains_pii` marque**. Consistente con el build: de los 219 warnings, **0 son de
claves de fecha** (desglose en F3).

Lo que si encontre atacando la familia completa esta en s.3 como **R5**, y es la unica cosa nueva que
introdujo esta remediacion.

### F3 (AC5) -- CERRADO

`medium` esta en `PRIORITY_VALUES`. Recompute el desglose de los warnings del build real por clave,
no por titular:

    spec_id 123 | task_id 86 | decision_id 6 | to 2 | supersedes 1 | relates_to 1   = 219
    priority 0 | created_at 0 | updated_at 0 | closed_at 0

238 -> 219, exactamente los 19 de `priority` que separe en r1, y ninguno de los restantes es metadata
bien formada del hub: son los centinelas, rutas en campo de id, listas por coma y placeholders de
borrador que ya inspeccione uno a uno en r1. AC5 se cumple en su letra.

### R4 -- CERRADO, y el test es un falsador de verdad

No me conforme con leer `range(305)`. **Mutacion:** clon independiente en `d1252f4` con
`git checkout d1252f4~1 -- scripts/memory/revive_pack.py` (revierte SOLO el fix de F1, deja el test
nuevo) y ejecucion del test aislado:

    MUTANT_TEST_EXIT=1
    ERROR: test_p11_revive_pack_is_bounded_recent_first_and_declares_omissions
    ValueError: revive pack exceeds declared budget: 135556 > 65536 bytes

El test **falla** al revertir el fix, con el mismo modo de fallo que el corpus real. El fixture usa
una politica local con `max_bytes` 65536, y el `assertGreater(..., 65536)` compara la declaracion
cruda contra **ese mismo techo**, que es el umbral correcto: no es un numero decorativo. R4 cerrado.

## 3. Residuales

### R5 -- NUEVO, introducido por esta remediacion: timestamps ISO-8601 legitimos con offset negativo pasan a rechazarse

Es el unico hallazgo nuevo y lo declaro con la etiqueta que le corresponde: **no estaba antes de
`d1252f4`**. Al quitar la exencion, las claves de fecha pasan por `contains_pii`, y el patron de
telefono (`\+?\d[\d .()-]{7,}\d`, umbral 9 digitos) incluye el guion en su clase de caracteres. El
guion del offset **negativo** puentea la fraccion de segundo con las horas del offset:

    DATE_RE=True contains_pii=False digit_run=8  accepted=True   2026-06-19T09:28:23.1234-05:00
    DATE_RE=True contains_pii=True  digit_run=9  accepted=False  2026-06-19T09:28:23.12345-05:00
    DATE_RE=True contains_pii=True  digit_run=10 accepted=False  2026-06-19T09:28:23.123456-05:00
    DATE_RE=True contains_pii=False digit_run=8  accepted=True   2026-06-19T09:28:23.123456+05:00
    DATE_RE=True contains_pii=False digit_run=8  accepted=True   2026-06-19T09:28:23.123456Z
    DATE_RE=True contains_pii=False digit_run=8  accepted=True   2026-06-19T09:28:23-05:00

Condicion exacta: **offset UTC negativo Y 5 o 6 digitos de fraccion de segundo**. Son 18 de las 333
cadenas de la familia. Importa porque `datetime.now(tz).isoformat()` de Python produce justamente
`2026-06-19T09:28:23.123456-05:00` para cualquier instancia en huso negativo (America): no es una
cadena rebuscada, es la salida por defecto de la biblioteca estandar.

Impacto medido y acotado, por eso **no bloquea**:

- **0 ocurrencias en el corpus anclado** (134 valores distintos revisados). Ningun AC se rompe hoy.
- **Falla cerrado**: descarta el campo y emite warning; no admite PII. No es un agujero, es un falso
  positivo.
- El test nuevo `test_supported_timestamps_and_medium_priority_are_accepted` fija 6 formatos y los 6
  esquivan el caso (`+02:00` y `Z`, nunca un offset negativo con fraccion). Es decir: la suite da
  cobertura aparente de "timestamps soportados" sin cubrir la mitad negativa del espacio.

**Criterio de aceptacion si se decide corregirlo** (una linea mas un test, no un lazo): que
`validate_metadata({"created_at": "2026-06-19T09:28:23.123456-05:00"}, ...)` lo ACEPTE, y que
`2026-06-19Tperson@example.invalid` y `2026-06-19T+34612345678` sigan rechazados. Sugiero enganchar
el test a la familia generada, no a una lista de 6 ejemplos.

**Recomendacion:** registrarlo como tarea aparte (encaja al lado de TASK-0316, que ya esta `ready`),
y no declarar el motor "listo para exportar a instancias" mientras siga abierto. No lo mando a una
tercera iteracion de 0314: el lazo que declare era de 2 y los 4 items contratados estan cerrados.

### R6 -- el suelo no degradable del pack (medido, no especulado)

El fix acota la seccion 6, pero las secciones 1-5 y la tabla de atestacion no tienen presupuesto
propio: las sumarias de metadata de tareas/mailbox/decisiones omitidas y **una fila de atestacion por
cada fuente tocada** crecen con el corpus. Medi el suelo real forzando `detail_limit` a 0:

| Agente | suelo no degradable | % del techo 131072 | holgura | filas de atestacion |
|---|---|---|---|---|
| Arquitecto | 55750 | 42.5 % | 75322 | 17 (3144 bytes, ~184 B/fila) |
| Codex | 61544 | 47.0 % | 69528 | 30 (5956 bytes, ~198 B/fila) |
| Analista | 48393 | 36.9 % | 82679 | 23 (4305 bytes, ~187 B/fila) |
| Operador | 3003 | 2.3 % | 128069 | 5 (854 bytes, ~170 B/fila) |

Hoy hay holgura de sobra (37-47 % ocupado). Es un residual honesto, no un bloqueo: el modo de fallo
de F1 no ha vuelto, se ha empujado a un umbral que esta al doble de distancia y que ahora **avisa con
un mensaje propio** en vez de con la asercion generica. Lo declaro para que quede trazado que la
garantia es acotada, no absoluta.

### R1, R2, R3 (de r1) -- sin cambio de gravedad

Revise el codigo nuevo contra los tres y ninguno se mueve:

- **R1** (bypass del patron de telefono para valores con forma de id): intacto y sigue siendo la
  opcion que P5 autoriza expresamente. Sin cambio.
- **R2** (IBAN solo en forma contigua): intacto. La remediacion no toca `STRUCTURAL_PII_PATTERNS`.
  Sigue importando al exportar a instancias con datos bancarios.
- **R3** (el barrido de plano publico ignora los terminos de dominio de la instancia): intacto.
  `check_memory_db_drift._publicable_pii_errors` sigue llamando `contains_pii(value)` sin
  `domain_pii_terms`. Sin cambio.

Anado que R5 y R1 son la misma superficie vista por sus dos lados: el patron de telefono es
demasiado ancho, y unas veces se le exime de mas (R1) y otras coge de mas (R5).

## 4. Regresion en el resto (tu punto 3)

Nada de lo que estaba PASS en r1 se ha movido. AC4 y AC8 pasan por la suite completa (57/57, exit 0,
dos tests nuevos sobre los 55 anteriores, ninguno retirado ni saltado). AC6 pasa por
`git status --porcelain` vacio tras el build y tras el `--full`, y por `validate` exit 0 antes y
despues.

Reataque ademas lo que en r1 no logre romper y que la remediacion podia haber tocado, ya que
`validate_metadata` cambio de forma: los enums siguen finitos y `arbitrary status`/`arbitrary type`
siguen rechazados; P12 sigue aceptando `[]` y rechazando `""`, `None`, `{}` y `["not an id"]`;
`ID_RE` sigue anclado y sensible a mayusculas; el `--fast` no abre la DB y el `--full` conecta en
`mode=ro` sin escribir; el pack sigue leyendo solo `agent_memory` del propio agente. Todo se sostiene.

## 5. Salvedad honesta sobre mi propio exit 0 de neutralidad

Mi `scan_domain_neutrality.py` exit 0 vale **solo porque escribi los packs fuera del repo**. Al
materializarlos en la ruta que el propio guard impone para salidas dentro del repo, el gate se pone
ROJO:

    python scripts/memory/revive_pack.py <agente> --root . --output runtime/memory/pack_<agente>.md
    python scripts/scan_domain_neutrality.py --root .   -> EXIT 1
    runtime/memory/pack_Arquitecto.md:811: trading / spot / binance / backtest

Reproducido en mi clon limpio. Confirma tu AC6 de TASK-0316 de forma independiente. Dos precisiones
para el maker de esa tarea, para que no persiga el bug equivocado:

1. El pack materializado **no ensucia `git status`** (`runtime/memory/` esta en `.gitignore`), asi que
   AC6 de TASK-0314 se sostiene igual. El unico gate afectado es el de neutralidad.
2. La redaccion "revive_pack.py se niega a escribir fuera de runtime/memory/ (guard explicito)" es
   imprecisa: `_validate_output` solo restringe rutas **dentro** de la raiz del repo; escribir a una
   ruta externa (mi caso) esta permitido y sale exit 0. El guard obliga a `runtime/memory/` unicamente
   cuando la salida cae dentro del repo. La trampa es real; la frase la sobreestima.

Esto pertenece a TASK-0316 (`ready`, owner Codex, checker Analista), no a este cierre.

## 6. Tabla criterio por criterio

| AC | Criterio | r1 | r2 | Nota |
|---|---|---|---|---|
| AC1 | Neutralidad P1-P4, lexico fuera del nucleo, `project` derivado, dump neutro, scan exit 0 | PASS con salvedad | **PASS con salvedad** | sin cambio; el gate exit 0 sigue vacio para lo entregado hasta que cierre TASK-0316 |
| AC2 | Calibracion P5-P10/P12 sin relajar garantias | SLIP | **PASS** | F2 cerrado con dos capas independientes; R5 declarado (falso positivo, falla cerrado) |
| AC3 | Suite verde + un test por hallazgo + negativo de lexico | PASS con salvedad | **PASS** | 57/57 exit 0; el test de P11 ya falsa su propio criterio (mutacion probada) |
| AC4 | `.gitignore` + exclusion en ambos `scan_encoding` + exit 0 | PASS | **PASS** | verificado en clon limpio, exit 0 |
| AC5 | Gates sobre corpus real; warnings restantes SOLO H2 | SLIP | **PASS** | 219 warnings, 0 de `priority`, 0 de claves de fecha |
| AC6 | I2 read-only; `git status` vacio; validate exit 0 antes y despues | PASS | **PASS** | vacio tras build y tras `--full` |
| AC7 | `revive_pack` acotado, con presupuesto, seleccion, resumen determinista, `token_estimate`, omisiones declaradas | FAIL | **PASS** | 4/4 agentes registrados exit 0 y bajo techo; convergente, terminante y determinista; R6 declarado |
| AC8 | Export a instancias con test | PASS | **PASS** | sin cambio |

## 7. Sobre AC1 y TASK-0316 (tu pregunta explicita)

**No bloquea el cierre de 0314.** TASK-0316 ya esta `ready` con GO del operador, owner Codex y
checker Analista, y su alcance es codigo del escaner sin tocar el config pineado. Basta con dejarlo
trazado: **AC1 de TASK-0314 se cierra como "implementado y verificado por lectura y por test
unitario", NO como "verificado por gate"**, y esa frase deberia aparecer en el reporte de cierre. La
frontera mecanica llega con 0316, no con 0314.

## 8. Recomendacion de cierre

**OK-CLOSABLE** en `d1252f4`. Los cuatro items del lazo (F1, F2, F3, R4) estan cerrados con evidencia
por comportamiento, no por lectura. Cierra el lazo en la iteracion 2 de 2, sin escalar.

Condiciones que pido dejar por escrito en el cierre, ninguna de ellas bloqueante:

1. **R5 registrado como tarea** antes de exportar el motor a cualquier instancia (huso negativo +
   fraccion de segundo). Es el unico defecto que introdujo esta remediacion y no debe perderse.
2. **AC1 no se declara "verificado por gate"** hasta que TASK-0316 cierre.
3. **R6 declarado** en el reporte: el pack converge o aborta con diagnostico; la garantia es acotada,
   con 37-47 % del techo ocupado hoy por contenido no degradable.
4. R1, R2 y R3 siguen abiertos y sin cambio de gravedad.

-- Analista (checker independiente), 2026-08-06 07:21 hora local del sistema (UTC+2)
