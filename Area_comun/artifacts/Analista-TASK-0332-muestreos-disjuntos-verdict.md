# Veredicto Analista -- TASK-0332: los muestreos disjuntos, unificados por comportamiento

- Revisor: Analista (voz adversarial independiente; no implemento, no cierro, no promuevo)
- Fecha: 2026-08-08 13:46 hora local (UTC+2)
- Instruccion: `Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0332.md`
- Alcance declarado por el Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE
- **Recomendacion de cierre: CHANGE-REQUIRED**

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit de la entrega | `4205d04d` (`test(TASK-0332): cover date offsets by behavior`) |
| Diff de la entrega | `scripts/memory/test_memory_db.py`, 107 insertions, 1 deletion (un solo archivo) |
| HEAD del protocolo al emitir | `851a23e4`, en sincronia con `origin/main` (0/0) |
| Clon limpio | `D:/Aegis_Scratch/protocol/0332-review/clone`, `git checkout 4205d04d` |
| Estado canonico al arrancar | `validate_collaboration_state.py` exit 0 |
| Claims activas al escribir | 0 |

Todo lo que sigue se midio en el clon limpio sobre `4205d04d`, no en el arbol caliente.
Cada mutante se escribio, se midio y se restauro; la restauracion se verifico por igualdad
de texto del modulo (`restored: True` en las tres tandas).

## Reproduccion, con exit codes

Puertas del protocolo en el clon limpio, en `4205d04d`:

| Comando | Exit | Salida relevante |
|---|---|---|
| `python scripts/validate_collaboration_state.py --root .` | 0 | `OK: collaboration state is valid.` |
| `python scripts/scan_encoding.py --root .` | 0 | `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py --root .` | 0 | -- |
| `python scripts/check_falsification_contracts.py --root . --inventory` | 0 | `FALSIFICATION_INVENTORY permanent_negatives=58 declared=58 missing=0` |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | 0 | `FALSIFICATION_STATIC_WIRING runners=8/8 contracts=58/58` |
| `python scripts/test_falsification_contracts.py` | 0 | rechaza fronteras relajadas y negativos no declarados |
| `python runtime/protocol_replay.py --check-drift --root .` | 0 | `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=7960` |
| `python scripts/memory/test_memory_db.py` | 0 | `Ran 71 tests in 254.889s / OK` |

Drift 0. Inventario 58/58, `missing=0`, sin stale. El contrato nuevo aparece declarado:
`DECLARED NEG-MEMORY-DATE-OFFSET-PII-BEHAVIOR boundaries=4 runner=scripts\memory\test_memory_db.py`.

## Foco A -- los 1.684, derivados por mi: CUADRA EXACTO

No tome el numero de la entrega. Derive el alfabeto de offsets por fuerza bruta contra
`DATE_RE` cargado del modulo de produccion, con prefijo fijo `2026-06-19T09:28:23` y probando
mucho mas de lo que la entrega supone: signo `+`/`-`, horas 0..99, minutos 0..99, con separador
`:` y sin separador, offsets de solo hora, `Z` y `z`, y la cadena vacia.

```
ASCII-derived accepted offset count: 1684
delivered set size:                  1684
in ASCII-derived but NOT in delivered: []
in delivered but NOT accepted:         []
```

La diferencia simetrica es vacia. La gramatica lo confirma a mano: la alternativa de offset es
`(?:Z|[+-](?:(?:0\d|1[0-3]):[0-5]\d|14:00))?`, o sea 14 horas x 60 minutos + `14:00` = 841 por
signo, 1.682 numericos, mas `""` y `"Z"` = 1.684. **Foco A: PASS.** El numero es real y el
conjunto es el correcto para el alfabeto ASCII.

Con una salvedad que hay que declarar (residual R0332-3, abajo): `DATE_RE` usa `\d` sin
`re.ASCII`, asi que el lenguaje que de verdad acepta es estrictamente mayor que 1.684. Un sondeo
mio, deliberadamente estrecho (3 plantillas, un solo digito sustituido, 670 codepoints Nd
no-ASCII), ya encontro **1.340 offsets adicionales aceptados** -- por ejemplo `+0<U+0660>:15`.
Eso es R3 de TASK-0322, declarado fuera de alcance, y **no lo cuento contra la tarea**; lo que si
cuento es que la entrega afirma exhaustividad sin acotarla al alfabeto ASCII.

## Foco B -- AC3, por COMPORTAMIENTO y no por AST: PASS, y lo verifique

No lo acepto declarado: introduje el bypass por reestructuracion en PRODUCCION
(`if not (DATE_RE.fullmatch(item) and item.endswith("+06:15")): <los 12 renglones de chequeos>`)
y mire **que assert muere primero**. Mapa de asserts del test nuevo:

- linea 2235: `assertEqual((True, True), source_results)` -- el barrido de comportamiento
- lineas 2259 / 2271 / 2284 / 2294: anclas SINTACTICAS sobre el texto de produccion
- lineas 2316 / 2317 / 2318: asserts sobre los mutantes que el propio test compone

Resultado, en orden de fallo:

| Vector inyectado en produccion | Exit | Asserts que fallan, en orden |
|---|---|---|
| V1 reestructuracion, clave `+06:15` | 1 (MUERE) | **2235**, luego 2259 |
| V3 retorno falsy temprano, clave `+06:15` | 1 (MUERE) | **2235**, luego 2316 |
| V2 filtrado del iterable en helper externo, clave `+06:15` | 1 (MUERE) | 2318 solamente |

V1 y V3 mueren **primero en 2235**, el assert de comportamiento, antes de tocar cualquier ancla
sintactica. La forma que el AST no ve queda cazada por comportamiento. **AC3: PASS**, verificado
por mi, no aceptado por declaracion.

## Foco C -- AC4, las tres formas atribuidas: PARCIAL

La atribucion que la entrega declara ("mata reestructuracion, filtrado del iterable en helper
externo y salida temprana") es correcta en dos de tres y **sobredeclarada en la tercera**.

V2, el filtrado del iterable en un helper externo, no muere por comportamiento: muere solo en
2318, `assertEqual((False, False), mutant_results["early_return"])`, es decir porque mi mutacion
perturba lo que el test espera de **su propio** mutante. Es una muerte incidental, no una
observacion del efecto. El barrido no la ve porque su unica carga de tipo lista es
`[timestamp, email]`: si se filtra el timestamp, el email sigue detectandose. Medido bajo V2:

```
contains_pii([ts], ["2026"])   -> False     (la fuente devuelve True)   <-- fuga que el barrido no mira
contains_pii([ts, email], [])  -> True      (por eso 2235 no se entera)
```

El barrido nunca emite una lista cuyo UNICO PII sea el timestamp exento, que es justo la carga
que haria visible esta clase.

## Los dos escapes NUEVOS: la suite entera verde con fuga de PII real

Esto es lo que decide el veredicto. Los dos son de la MISMA clase que la tarea dice cerrar --
un miembro del lenguaje que `DATE_RE` exime, jamas ejercitado contra el gate real, y un bypass
clavado ahi sobrevive -- y los dos son ASCII puro, asi que **R3 de 0322 no los tapa**.

### SLIP-0332-1 (el mas grave): el barrido es unidimensional, no exhaustivo

El barrido recorre los 1.684 offsets con **todas las demas coordenadas congeladas** en
`2026-06-19T09:28:23`. Un retorno falsy temprano clavado en otro prefijo de fecha sobrevive,
aunque el offset este DENTRO del conjunto declarado exhaustivo.

Mutante en produccion, dentro del bucle de `contains_pii`:

```python
    for item in value_list(value):
        if DATE_RE.fullmatch(item) and item.startswith("2027-"):
            return False
```

Medicion:

```
payload[0]='2027-06-19T09:28:23+06:15'   DATE_RE.fullmatch=True
contains_pii(payload, []) -> False        (esperado True: el email es PII real)
DELIVERED SUITE exit=0    Ran 71 tests in 241.483s    OK
```

El offset `+06:15` esta dentro de los 1.684. La fuga es la fuerte: el `return False` aborta el
barrido completo y **oculta el email de un item hermano**, que es exactamente la forma de
SLIP-0325-1. La suite entera en verde.

### SLIP-0332-2: la forma basica de hora, aceptada y nunca ejercitada

`DATE_RE` acepta tambien la forma basica de hora (verificado: `2026-06-19T092823+06:15` ->
ACCEPT, igual que `2026-06-19`, `2026-06-19T092823Z` y `2026-06-19T09:28:23.5+06:15`). Ningun
contrato ejercita esas formas contra `contains_pii`. Filtrado del iterable en el helper externo
`value_list`, clavado ahi:

```python
        if any(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{6}(?:Z|[+-]\d{2}:\d{2})?", i) for i in items):
            return []
```

Medicion:

```
payload[0]='2026-06-19T092823+06:15'     DATE_RE.fullmatch=True
contains_pii(payload, []) -> False        (esperado True: el email es PII real)
DELIVERED SUITE exit=0    Ran 71 tests in 249.174s    OK
```

Otra vez: fuga de PII real, suite entera verde, exit 0.

Las anclas sintacticas de 2259/2271/2284 no salvan ninguno de los dos: SLIP-0332-1 no toca el
cuerpo del bucle que 2259 cuenta (la linea `for item in ...` queda fuera del literal) y
SLIP-0332-2 vive en otra funcion.

## Tabla vector por vector

| # | Vector | Resultado | Evidencia |
|---|---|---|---|
| A | Los 1.684 son TODOS los offsets ASCII que `DATE_RE` acepta | **PASS** | derivacion independiente, diferencia simetrica vacia |
| A' | Exhaustividad sobre el lenguaje real de `DATE_RE` (Unicode `\d`) | **SLIPS (residual R0332-3)** | 1.340 offsets no-ASCII aceptados en un sondeo estrecho; R3 de 0322, fuera de alcance, pero sin declarar |
| B | AC3: muere ante reestructuracion, por comportamiento | **PASS** | muere primero en 2235, no en las anclas sintacticas |
| C1 | AC4: reestructuracion, atribuida | **PASS** | 2235 |
| C2 | AC4: salida temprana falsy, atribuida | **PASS** | 2235 |
| C3 | AC4: filtrado del iterable en helper externo, atribuida | **SLIPS** | muere solo en 2318, por composicion de mutantes, no por comportamiento |
| C4 | La clase entera cerrada (cambio de COORDENADA) | **SLIPS -- SLIP-0332-1** | offset dentro de los 1.684, prefijo `2027-`: fuga real, suite verde exit 0 |
| C5 | La clase entera cerrada (cambio de FORMATO) | **SLIPS -- SLIP-0332-2** | forma basica de hora aceptada por `DATE_RE`: fuga real, suite verde exit 0 |
| D | AC5: 0317/0322/0325 verdes, sin cambio de semantica, sin duplicar | **PASS** | 107+/1-; la unica baja es una linea en blanco; 71/71 OK; inventario 58/58 sin stale |
| E | AC6/coste de ejecucion | **PASS** | contrato nuevo aislado: **0,173 s**; suite completa 71 tests / 254,9 s exit 0 |
| F | Cableado en CI y su fallo tumba el job | **PASS en cableado** | job `validate`, paso sin `if:`, sin `continue-on-error`, sin `needs`, ultimo comando del bloque |
| F' | EJECUTADO de verdad en CI | **NO se ejecuta** (no imputable a 0332) | ver abajo |
| G | Puertas del repo en clon limpio | **PASS** | siete puertas exit 0, drift CLEAN |

## Foco E -- el coste, que resulta ser un no-problema

El contrato nuevo aislado tarda **0,173 s**:

```
python scripts/memory/test_memory_db.py MemoryDbTests.test_date_offset_pii_behavior_is_falsifiable
ISOLATED_NEW_TEST_EXIT=0   ELAPSED_S=0.3   (Ran 1 test in 0.173s)
```

La suite completa: 71 tests / 254,9 s. El baseline citado era ~240 s con 70 tests; los 1.684
offsets por comportamiento no explican ese delta -- ejecutar el barrido cuesta dos decimas.
**No hay nada que particionar**, y esto importa para la remediacion: ampliar el barrido a mas
coordenadas es practicamente gratis. El argumento de coste no puede usarse para no cerrar la
clase.

## Foco F -- cableado si, ejecutado no

Cableado, verificado en el YAML y no por declaracion: el runner
`scripts/memory/test_memory_db.py` esta en el job `validate`, paso
"Validate falsification contracts and guardian controls", sin `if:`, sin `continue-on-error`,
sin `needs`, y es el ULTIMO comando de su bloque `run: |`, de modo que su fallo tumba el paso y
el job. El gate estatico lo confirma: `runners=8/8 contracts=58/58`.

Y sin embargo, la realidad de ejecucion, consultada a la API de Actions
(run 31254474638, HEAD `b78322a5`):

```
job validate -> conclusion=failure
  paso que falla:  "Validate repository dogfood instance"
  paso del contrato: "Validate falsification contracts and guardian controls" -> SKIPPED
  (y los 60+ pasos siguientes, tambien SKIPPED)
```

El contrato nuevo se ha ejecutado en CI **cero veces**. Los ultimos 200 runs del repo tienen
`conclusion=failure` sin excepcion. Ademas: **no existe run de CI para el commit `4205d04d`** --
no aparece en los ultimos 200 runs; la entrega nunca fue ejercitada por CI.

Respeto lo que el Arquitecto declara: la causa es TASK-0340 y **no la imputo a 0332**. Pero si
dejo dicho, porque es la leccion de 0330 medida con numeros: el gate estatico declara
`residuals=trigger_filters,working_directory,yaml_1_1_scalars` y **no incluye "un paso anterior
del mismo job falla primero, y el paso no llega a correr"**. Hoy eso significa 58/58 contratos
cableados y 0/58 ejecutados durante 300 runs seguidos. Es un hueco del certificador, no de esta
tarea; lo senalo para que alguien lo contrate.

## Residuales declarados

- **R0332-1 (nuevo, bloqueante):** el barrido es exhaustivo sobre UNA coordenada (el offset) con
  todas las demas congeladas en `2026-06-19T09:28:23`. Fuera de ese prefijo la clase sigue
  abierta. Demostrado: SLIP-0332-1.
- **R0332-2 (nuevo, bloqueante):** el lenguaje que `DATE_RE` exime incluye la forma basica de
  hora, la forma de solo fecha y los segundos fraccionarios; ningun contrato las ejercita contra
  `contains_pii`. Demostrado: SLIP-0332-2.
- **R0332-3 (nuevo, no bloqueante, solo declarar):** `assertEqual(1_684, len(valid_offsets))` es
  exacto para el alfabeto ASCII, no para el lenguaje de `DATE_RE`, que con `\d` sin `re.ASCII`
  acepta muchos mas. Es R3 de TASK-0322, fuera de alcance por decision previa: pide una linea de
  declaracion, no codigo.
- **R0332-4 (no bloqueante):** el contrato se apoya en anclas de TEXTO EXACTO sobre produccion
  (2259, 2271, 2284). Un reformateo benigno de `contains_pii` lo pone rojo sin que haya defecto.
  Fragilidad conocida, no fuga.
- **R0332-5 (ajeno a 0332):** cero ejecucion efectiva en CI por TASK-0340, y el certificador no
  declara ese modo de fallo entre sus residuales.

## Por que CHANGE-REQUIRED y no un residual mas

Porque la tarea no promete cubrir mas offsets: promete **cerrar la familia** por comportamiento,
y su propio texto dice que lo que todas las formas comparten es que cambian el comportamiento
observable de `contains_pii`. Tengo dos bypasses que cambian ese comportamiento, ocultan un
email real, y dejan la suite entera en verde con exit 0. Uno de ellos usa un offset **que esta
dentro de los 1.684 declarados exhaustivos**. El muestreo dejo de ser disjunto en el eje del
offset y sigue siendo disjunto en el eje del prefijo y en el eje del formato: es el mismo hueco
de 0317-vs-0325 con otra coordenada. Y con el contrato costando 0,17 s, no hay razon de coste
para no cerrarlo.

## Bucle de correccion esperado

Remediacion propuesta (barata; el coste medido lo permite de sobra):

1. Variar la COORDENADA, no solo el offset: construir la carga como {prefijos} x {offsets},
   con prefijos que cubran las ramas que `DATE_RE` acepta -- solo fecha, hora extendida, hora
   basica `T092823`, segundos fraccionarios -- y al menos un ano distinto de 2026. Mantener los
   1.684 offsets para un prefijo y un subconjunto representativo para los demas. Esto mata
   SLIP-0332-1 y SLIP-0332-2.
2. Anadir una carga de tipo lista cuyo UNICO PII sea el timestamp exento
   (`contains_pii([timestamp], [domain_term])`), para que el filtrado del iterable en helper
   externo muera **en 2235, por comportamiento**, y no incidentalmente en 2318.
3. Declarar R0332-3 en el propio contrato: el barrido es sobre el alfabeto ASCII; `\d` sin
   `re.ASCII` admite un conjunto estrictamente mayor (R3 de TASK-0322, fuera de alcance).
4. No aceptare un estrechamiento de la clave. Anadir `2027-` o `+06:15` a una lista de casos
   especiales reduce el dano sin cambiar la clase: el contrato debe sobrevivir a un cambio de
   coordenada, de orden y de formato elegido por quien lo ataque, no por quien lo escribe.

Puertas afectadas para el re-juicio, en clon limpio sobre el commit nuevo:
`python scripts/memory/test_memory_db.py`,
`python scripts/check_falsification_contracts.py --root . --inventory`,
`python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory`,
`python scripts/validate_collaboration_state.py --root .`,
`python scripts/scan_encoding.py --root .`,
`python scripts/scan_domain_neutrality.py --root .`,
`python runtime/protocol_replay.py --check-drift --root .`.

Re-juicio adversarial ANTES del commit de cierre, con los mismos dos escapes reinyectados como
prueba minima de que ahora mueren. **Maximo 2 iteraciones**; si a la segunda la clase sigue
abierta, escalo al operador humano.

## Respuesta a la pregunta del Arquitecto

Si a la primera mitad y no a la segunda. Los 1.684 son de verdad todos los offsets que `DATE_RE`
acepta en el alfabeto ASCII, y lo derive yo: diferencia simetrica vacia contra mi propia fuerza
bruta. El contrato lo cablea un job real de CI cuyo fallo tumbaria el job -- pero hoy no lo
ejecuta nadie, porque un paso anterior del mismo job falla y el paso queda SKIPPED, y el commit
`4205d04d` no tiene ni un run. Eso ultimo es TASK-0340 y no lo imputo a esta tarea. Lo que si
imputo: exhaustivo sobre 1.684 offsets con el resto de coordenadas congeladas no es exhaustivo
sobre la familia, y tengo dos fugas de PII reales con la suite entera verde para demostrarlo.

-- Analista
