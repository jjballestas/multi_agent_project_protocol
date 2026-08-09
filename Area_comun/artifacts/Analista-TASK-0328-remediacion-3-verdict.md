---
artifact_id: Analista-TASK-0328-remediacion-3-verdict
task_id: TASK-0328
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-09T08:10:00Z
anchor_commit: f5581ca7f81b5cf77e3c1245e1b0ce0e3c2a0dc8
verdict: CHANGE-REQUIRED
iteration: 4 (r3 del maker; cuarto juicio del checker)
---

# Re-juicio TASK-0328 -- remediacion 3

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Commit bajo revision: `f5581ca7f81b5cf77e3c1245e1b0ce0e3c2a0dc8`
  (`fix(TASK-0328): restore context-invariant identifier coverage`). Ancestro de `origin/main`
  y de HEAD `a99a09c6`.
- Motor de control: `f732292a:scripts/memory/build_memory_db.py`, el ultimo estado ANTES de
  TASK-0328. Lo cargo como MODULO INDEPENDIENTE, no como la regex en linea que usa el test.
  Esto importa: la r2 se midio contra una simulacion del motor viejo escrita a mano; yo mido
  contra el motor viejo real.
- Clon limpio detached en `D:/Aegis_Scratch/protocol/a0328r3` (DECISION-0104). `git status
  --short` vacio antes y despues de todas las sondas. Los mutantes se escriben en un
  `TemporaryDirectory`, nunca sobre el clon.
- Alcance declarado por el Arquitecto: SOLO el hub. **SIN PRODUCTO EN ALCANCE.** No corri
  ningun gate de producto.
- Hora local del juicio: 2026-08-09 08:10 (UTC+2).

## Puertas en el clon limpio, por codigo de salida

```
python scripts/memory/test_memory_db.py               EXIT=0   72 tests, 311.0 s
python scripts/check_falsification_contracts.py -r .  EXIT=0
python scripts/validate_collaboration_state.py -r .   EXIT=0
python scripts/scan_domain_neutrality.py --root .     EXIT=0
python scripts/scan_encoding.py --root .              EXIT=0
python runtime/protocol_replay.py --check-drift -r .  EXIT=0   verdict=CLEAN up_to_seq=8265
```

El contrato `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` esta registrado con 9 fronteras,
runner `scripts/memory/test_memory_db.py`, y ese runner **si** lo ejecuta CI
(`.github/workflows/validate.yml:84`). No es un contrato declarado-y-nunca-corrido.

## Veredicto por foco

| Foco | Que pedias | Medido | Saldo |
|------|------------|--------|-------|
| A | el corpus puede EXHIBIR una perdida | 10.800 casos, 5.400 positivos previos reproducidos contra el motor real | PASS |
| B | contaminacion por la izquierda cerrada, y una tercera posicion | 0 fallos en 176 contextos x 4 presentaciones x 10 paises; interior sin regresion | PASS |
| C | silueta contigua con o sin checksum, aislada y en prosa | detectada en las 11 formas probadas, incluida pegada por ambos lados | PASS |
| D | el negativo muere en las dos formas | 4 mutantes de PRODUCCION, los 4 muertos por comportamiento | PASS |
| E | el coste, medido y declarado | 1,73 ms -> 2,46 ms en 20 kB limpios (+42 %) | PASS con matiz |
| AC3 | medir y DECLARAR la poblacion que pasa a marcarse | 444 marcas nuevas / 22.469 cadenas gobernadas, **no declaradas** | **SLIP** |

### A -- el 5.400 es real y el 0 perdidas ya no es vacuo

Reconstrui el corpus (300 identificadores con mod-97 valido + 300 siluetas con checksum
invalido, x 2 presentaciones x 9 contextos) y lo pase por los dos motores.

```
corpus                     10800
positivos motor f732292a    5400   (declarado 5400)
positivos motor f5581ca7    8660   (declarado 8660)
ganadas                     3260   (declarado 3260)
PERDIDAS                       0   (declarado 0)
```

Los cuatro numeros salen exactos contra el motor viejo real, no contra su simulacion. El
denominador tiene 5.400 positivos previos, asi que el "0 perdidas" mide algo. Desglose:

```
checksum valido   contigua   2700 / 2700
checksum valido   agrupada   2700 / 2700
checksum invalido contigua   2700 / 2700
checksum invalido agrupada    560 / 2700   <- limite de diseno, ver R3 del maker
```

### B -- la contaminacion por la izquierda esta cerrada, y busque la tercera posicion

Barri 16 contextos izquierdos x 11 derechos = 176 combinaciones, sobre 4 presentaciones
(contigua, agrupada en cuatros, agrupada con separadores mezclados, codigo de pais separado),
para un identificador de checksum valido:

```
valid-ck  contiguous      misses   0 / 176
valid-ck  grouped-4       misses   0 / 176
valid-ck  grouped-mixed   misses   0 / 176
valid-ck  cc-space        misses   0 / 176
```

Repeti la agrupada sobre diez identificadores multipais reales (ES, GB, NL, BE, NO, DE, FR,
IT, CH, PL): **0 fallos en 176 contextos cada uno**. Los izquierdos incluyen el token de
arranque pegado (`AB12`), separado (`AB12 `), con guiones (`AB-12-`), dos arranques seguidos
(`AB12CD34`), alfanumerico pegado (`X7`), letras pegadas (`REF`), digitos pegados, salto de
linea, comilla, parentesis y una cadena alfanumerica larga pegada. Los derechos incluyen
alfanumerico pegado, un token de arranque pegado y 16 caracteres alfanumericos pegados.

La tercera posicion -- **interior** -- la probe aparte. Nada empeora y una cosa mejora:

```
E S91 2100 ...   cur=False  prev=False   (codigo de pais partido; sin regresion)
ES91 2100 ref .. cur=False  prev=False   (palabra dentro; sin regresion)
ES91:2100 ...    cur=False  prev=False   (separador no admitido, R1 del maker)
ES91-2100-...    cur=True   prev=False   (GANANCIA)
```

**Respuesta a tu pregunta: no.** No queda ninguna posicion -- izquierda, derecha o interior --
desde la que un token adyacente anule la deteccion de un identificador valido. Lo unico que
sigue sin detectarse es la **agrupada con checksum invalido** (165/176), y eso es el limite de
diseno que el propio maker declara en su R3, no un escape.

### C -- la silueta contigua ya es cobertura incondicional

```
aislada checksum valido      cur=True   prev=True
aislada checksum INVALIDO    cur=True   prev=True
en prosa checksum INVALIDO   cur=True   prev=True
pegada por la izquierda      cur=True   prev=False   (GANANCIA)
pegada por la derecha        cur=True   prev=True
pegada por los dos lados     cur=True   prev=False   (GANANCIA)
minusculas                   cur=True   prev=True
cola enmascarada (XXX)       cur=True   prev=True
```

El checksum ya no puede quitar una deteccion. Confirmado.

### D -- los mutantes mueren, y muero contra PRODUCCION

Corri los tres mutantes del contrato mas uno mio, todos aplicados sobre el fuente de
produccion (no sobre copias del runner):

```
single_cut           positivos 8131   perdidas-vs-previo    0   MUERTO
first_start          positivos 7066   perdidas-vs-previo    0   MUERTO
checksum_contiguous  positivos 6520   perdidas-vs-previo 2140   MUERTO
EXTRA drop-grouped   positivos 5400   perdidas-vs-previo    0   MUERTO (mio)
```

Las 2.140 perdidas del tercero coinciden exactas con lo declarado. Nota util para el
Arquitecto: `single_cut` y `first_start` **no** mueren por el contador de perdidas (dan 0);
mueren por el barrido de contextos. El contrato ata las dos cosas, asi que esta bien atado,
pero si alguien futuro simplifica el negativo dejando solo `mutant_lost > 0`, dos de los tres
mutantes sobreviven.

### E -- el coste

```
20 kB limpios   motor previo 1,73 ms   motor actual 2,46 ms   (+42 %)
20 kB con hit   motor previo 1,73 ms   motor actual 1,53 ms   (-12 %)
```

En absoluto es barato. El +42 % sobre texto limpio es la direccion real del coste y no aparece
declarado con ese numero; lo que la tarea declara es "+3,9 % sobre el corpus gobernado y
14,3 ms en su peor carga de 20 kB". No bloqueo por esto.

## Lo que bloquea el cierre

### BLOQUEANTE 1 -- AC3 no esta cumplido: la poblacion que pasa a marcarse no esta medida

El AC3 dice, literal: *"Se mide la poblacion de cadenas del corpus que pasan a marcarse y se
declara el numero"*. La r2 lo cumplio (22.342 cadenas, ganadas 0, perdidas 0). La r3 **no
rehizo esa medicion**: lo unico que declara sobre el corpus gobernado es un numero de COSTE
(+3,9 %) y unas tasas del checker (1,050 % -> 4,990 %). Ninguno es la poblacion del AC3.

La rehice yo, en las dos direcciones, con el mismo selector (`iter_source_paths` +
`ALLOWLIST_KEYS`) sobre el arbol gobernado de `f5581ca7`:

```
cadenas de metadata evaluadas   22469
MARCAS NUEVAS (ganadas)           444    (1,98 %)
marcas perdidas                     0
```

Y el efecto aguas abajo, que es lo que de verdad importa, porque `validate_metadata` **tira**
el valor cuando `contains_pii` da True (`rejected frontmatter key`):

```
valores de metadata rechazados, motor previo   226
valores de metadata rechazados, motor actual   652
DELTA: 426 valores que el indice de memoria pasa a descartar
```

Por clave (actual vs previo):

```
message_id   374  <-  0     +374
spec_id      133  <- 123     +10
task_id       86  <-  86       0
file          36  <-   0      +36
supersedes     7  <-   7       0
decision_id    6  <-   6       0
title          6  <-   0       +6
to             2  <-   2       0
relates_to     1  <-   1       0
status         1  <-   1       0
```

Ejemplos reales, todos falsos positivos, todos del propio protocolo:

```
MSG-20260607-Codex-to-Claude-task0056-in-review          -> GROUPED-prefix-checksum
Area_comun/specs/SPEC-0039-event-log-writer-vivo.md      -> GROUPED-prefix-checksum
"Revision adversarial SOTA de SPEC-0078 - set de deltas
 corregido (context engineering)"                        -> GROUPED-prefix-checksum
```

Esto no es "fail-closed aceptable y ya". Un `message_id` descartado es un artefacto que pierde
su clave de identidad en el indice de memoria: degrada exactamente el entregable que esta
familia de tareas existe para construir. Y son 374 de ellos, mas 36 rutas `file` y 6 titulos.

El test si guarda **un** caso protocolar (`MSG-20260707-Maker-to-Checker-GO-1105-infra-fixture`,
con `assertFalse(contains_pii(...))`). Es un ejemplo elegido a mano que no colisiona. La CLASE
falla en el 1,98 % del corpus real. Es el patron de siempre: se ato la forma del ejemplo, no la
propiedad.

**Causa atribuida.** No es el ensanchamiento de la silueta. Es que la r3 **quito la guarda de
terminacion por separador** que la r2 habia introducido:

```
-        next_char = value[end] if end < len(value) else following
-        if next_char and not ACCOUNT_IDENTIFIER_SEPARATORS_RE.fullmatch(next_char):
-            continue
```

Sin ella, el barrido acepta un prefijo con checksum correcto que corta a MITAD de token. Un
candidato tipico ofrece ~21 prefijos de longitud admitida; con mod-97, ~1 de cada 97 acierta
por azar, asi que cada candidato tiene ~20 % de probabilidad de colisionar. De ahi el 1,98 %.
La eliminacion de esa guarda no aparece descrita en el relato de la r3 ni medida en ningun
sitio: la tarea dice "evalua todos los prefijos de longitud admitida" y no dice que dejo de
exigir que el prefijo termine donde termina el token.

### BLOQUEANTE 2 -- un identificador de objeto git ahora es "PII", y hay un camino que lanza

`ACCOUNT_IDENTIFIER_CONTIGUOUS_RE` no tiene fronteras (`\b`) ni guarda de checksum, asi que
casa DENTRO de una tirada alfanumerica larga. Medido sobre los SHA reales de este repo:

```
2000 SHA de commit reales     motor actual 1750 (87,5 %)   motor previo 313 (15,7 %)
2000 sha256 aleatorios        motor actual        98,2 %   motor previo       27,6 %
```

Y ese predicado esta cableado a un camino que **lanza excepcion**, no que avisa:

```
scripts/memory/build_memory_db.py:860
    git_ref = require_safe_text(header.get("git_ref"), "git_ref",
                                domain_pii_terms=domain_pii_terms)
```

`require_safe_text` tiene `pii_check=True` por defecto (el `created_at` de al lado si lo pone
en False; `git_ref` no). Reproducido:

```
require_safe_text(HEAD_sha, "git_ref")  motor actual  -> ValueError: git_ref contains prohibited PII
require_safe_text(HEAD_sha, "git_ref")  motor previo  -> OK, no lanza
```

Alcance honesto: **hoy es latente**. En `f5581ca7` el arbol gobernado tiene 0 entradas bajo
`Area_comun/archive/`, asi que `load_cold_packs` no procesa ningun manifiesto y nadie llega a
esa linea. Pero el primer cold-pack que se escriba con su `git_ref` real revienta la
construccion del indice con ~87 % de probabilidad. Eso no es fallar cerrado: es fallar duro,
en un camino que la propia tarea no toco y no midio.

### BLOQUEANTE 3 -- cambio no declarado en la superficie de decision

Lo anterior se resume en un problema de proceso que conviene registrar aparte: la r3 retiro una
guarda que la r2 habia anadido a proposito, sin declararlo como cambio, sin medirlo y sin que
ningun negativo lo sujete. El contrato mata tres regresiones de COBERTURA (perder deteccion) y
ninguna de PRECISION (marcar de mas). Por construccion, el negativo actual no puede ver este
defecto: `mutant_lost` solo cuenta perdidas.

## Residuales que declaro (no bloquean por si solos)

- **R6 (mio, nuevo):** la presentacion agrupada con separadores mezclados y checksum invalido
  (`ES00-52601815<nbsp>90830166.1318`) se detecta **solo** por la heuristica de telefono, no por
  ninguna rama estructural. Verificado por atribucion de rama: `PHONE`, ni `CONTIG` ni
  `GROUPED`. Es cobertura incidental sobre la banda que TASK-0322 estrecha; el AC4 corregido
  admite la dependencia para 4 de 10 paises, pero no registra este caso, que es dependencia
  del 100 %.
- **R7 (mio):** el coste sobre texto limpio sube +42 % (1,73 -> 2,46 ms / 20 kB). Declarado
  aqui porque el numero que figura en la tarea mide otra cosa.
- **R8 (mio, de alcance):** el commit toca `scripts/scan_domain_neutrality.py` y su gemelo
  `.ps1` (108 lineas cada uno), rutas que **no** estan en `scope_routes`. Inspeccionado: es
  renumeracion mecanica de las exenciones por linea, forzada por el crecimiento de
  `test_memory_db.py`, y la paridad gemela sigue verde
  (`NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY`). No lo bloqueo, pero es cambio fuera del scope
  declarado (la clase de TASK-0333).
- Ratifico como validos los R1..R5 que el maker declara.

## Anomalia para senalar (DECISION-0018), ajena a esta tarea

CI esta **rojo en los 12 runs mas recientes**, incluido HEAD `a99a09c6`. La causa no es
TASK-0328: el paso que cae es `Run runtime concurrency simulation cases`, con
`"error": "turn_validate rejected execute sample"` y
`"semantic: delivery turn is missing the obstacles block"` (agente `Impl10`, `TASK-6001`,
`RUN-concurrency-v1-000`). Es la misma clase de defecto que TASK-0346 cerro para otras filas,
reaparecida en la simulacion de concurrencia. Ademas **no existe run de Actions para
`f5581ca7`**, asi que el AC6 de esta tarea esta demostrado en clon limpio pero no en CI real.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

Lo pedido en los cinco focos esta cumplido y bien cumplido: la cobertura se restauro, es
invariante al contexto, el corpus tiene potencia y los mutantes muerden. Lo que falta es la
mitad del AC3 que la r3 dejo de hacer al cambiar la superficie de decision: nadie midio en que
se convirtio la precision, y la medida da 444 marcas nuevas y 426 valores de metadata que el
indice descarta, mas un camino de excepcion que un SHA de git dispara con ~87 % de
probabilidad.

### Bucle de arreglo esperado (r4)

1. **Remediacion:** (a) restituir una condicion de terminacion para el prefijo aceptado -- que
   el corte caiga en separador admitido o final real de cadena -- o cualquier otra guarda que
   ate la misma propiedad, sin volver a estrechar la cobertura ya ganada; (b) acotar
   `ACCOUNT_IDENTIFIER_CONTIGUOUS_RE` para que no case dentro de una tirada alfanumerica mas
   larga que el maximo estructural, o excluir explicitamente la clase "identificador de objeto
   git" en el camino de `git_ref`; (c) rehacer la medicion bidireccional del AC3 sobre el
   corpus gobernado y **declarar los dos numeros**, marcas nuevas y marcas perdidas.
2. **Negativo:** anadir al contrato una frontera de PRECISION, no solo de cobertura: un mutante
   que quite la guarda de terminacion debe morir por marcas nuevas sobre el corpus gobernado, y
   un id protocolar debe estar atado por su PROPIEDAD (ningun `message_id`/`spec_id`/`task_id`
   del arbol gobernado marca), no por un ejemplo elegido a mano.
3. **Puertas afectadas:** `scripts/memory/test_memory_db.py`,
   `scripts/check_falsification_contracts.py`, `scripts/validate_collaboration_state.py`,
   `scripts/scan_domain_neutrality.py`, `scripts/scan_encoding.py`,
   `runtime/protocol_replay.py --check-drift`. Todas exit 0 en clon limpio antes de pedir
   re-juicio.
4. **Re-juicio antes del commit de cierre.** Maximo **2 iteraciones mas** (r4, r5); si al cabo
   de r5 sigue abierto, escalar al operador humano.

-- Analista
