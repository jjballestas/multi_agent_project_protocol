# Veredicto Analista -- TASK-0332 remediacion 2: la produccion si se arreglo, pero el contrato ata el TEXTO del arreglo, no su propiedad

- Revisor: Analista (voz adversarial independiente; no implemento, no cierro, no promuevo)
- Fecha: 2026-08-11 03:10 hora local (UTC+2)
- Instruccion: `Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0332-r3.md`
- Alcance declarado por el Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE
- **Recomendacion de cierre: CHANGE-REQUIRED**, y con ella **escalo al operador humano** por segunda
  vez. A diferencia de r2, lo que queda abierto es **pequeno y acotado**, y el cierre-con-residual
  declarado es una alternativa legitima siempre que se corrija la frase de R0332-9 (abajo).

## Ancla canonica

| Elemento | Valor |
|---|---|
| Ancla de la entrega | `647ba7e3` (`memory(Codex): record TASK-0332 remediation 2 delivery`) |
| Commit de implementacion | `29175f01` (`fix(TASK-0332): bind date exemption by behavior`) |
| Produccion tocada | **si**: `scripts/memory/build_memory_db.py` (+70/-34) |
| HEAD del protocolo al arrancar | `e7f85428`, en sincronia con `origin/main` |
| Clon limpio | `D:/Aegis_Scratch/protocol/0332-r3/clone`, `git checkout 647ba7e3` |
| Worktrees de mutantes | `.../0332-r3/{m5,m8,m9,n1,n2,n3}`, todos sobre `647ba7e3` |
| Estado canonico al arrancar | `validate_collaboration_state.py` exit 0 |
| Claims activas sobre mis rutas | 0 |
| Hora de arranque / cierre | 02:05 / 03:10 local |

Todo lo que sigue se midio en clones limpios sobre `647ba7e3`. Cada mutante se escribio en
**produccion** y se juzgo por ejecucion de la suite entera, nunca por lectura.

## Reproduccion, con exit codes

| Comando (en el clon limpio) | Exit | Salida relevante |
|---|---|---|
| `python scripts/validate_collaboration_state.py --root .` | 0 | `OK: collaboration state is valid.` |
| `python scripts/scan_encoding.py --root .` | 0 | `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py --root .` | 0 | -- |
| `python scripts/check_falsification_contracts.py --root . --inventory` | 0 | `DECLARED NEG-MEMORY-DATE-OFFSET-PII-BEHAVIOR boundaries=5` |
| `python scripts/test_falsification_contracts.py` | 0 | -- |
| `python runtime/protocol_replay.py --check-drift --root .` | 0 | `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8696` |
| `python scripts/memory/test_memory_db.py` | 0 | `Ran 72 tests in 487.989s / OK` |

Drift 0, siete puertas verdes. Nada de lo que sigue es un fallo de puerta: es lo que las puertas
**no ven**.

## Lo que esta remediacion SI cierra, y hay que decirlo

1. **Toca produccion y la arregla en la raiz.** `contains_pii` pasa a dos fases: primero evalua
   TODO el PII no-telefonico sobre la lista completa, y solo despues aplica la exencion de fecha a
   la heuristica de telefono. En el codigo entregado un item con forma de fecha ya **no puede**
   abortar la evaluacion antes de un email hermano. Es un arreglo estructural, no un muestreo mas.
2. **El refactor no cambia el comportamiento.** Diferencial viejo-contra-nuevo
   (`29175f01~1` vs `29175f01`), 60.000 entradas aleatorias con semilla `20260811` sobre un alfabeto
   de 12 valores (fechas de las tres formas, email, telefono, IBAN contiguo y agrupado, termino de
   instancia, texto inocuo), 1-3 items, con y sin `coordinate`: **0 divergencias**. AC5 sostenido
   por medicion, no por lectura.
3. **El corpus es un producto de verdad en cuatro coordenadas**, y eso mata dos de mis tres escapes
   de r2. Ver la respuesta a la PREGUNTA 2.

## PREGUNTA 1 -- los tres escapes de r2: mueren DOS, sobrevive UNO

Reinyectados en produccion como bypass real, no como mutante del runner. Los tres son fuga fuerte:
la fuente devuelve `(True, True, True)` y el mutante `(False, False, False)` sobre las tres sondas
`contains_pii([sonda, email], [])` / `contains_pii([email, sonda], [])` / `contains_pii(sonda, [termino])`.

| # | Clave del bypass | Suite | Muere en | Veredicto |
|---|---|---|---|---|
| M8 | mes `03` | **exit 1** | `test_date_offset_pii_behavior_is_falsifiable`, `:2287`, `AssertionError: 1454976 != 1333728` | **MUERE** |
| M9 | hora `05` | **exit 1** | mismo assert, `AssertionError: 1454976 != 1394352` | **MUERE** |
| M5 | `2027-` **y** `+06:15` a la vez | **exit 0** | -- | **ESCAPA** |

M8 pierde `1454976/12 = 121.248` casos y M9 pierde `1454976/24 = 60.624`: exactamente un mes y
exactamente una hora. Mueren **por comportamiento y por la coordenada correcta**, en el assert que
la tarea creo. Eso es progreso real y lo firmo.

M5 es la conjuncion, y sigue viva por la misma razon que en r2: sus dos coordenadas estan
muestreadas por separado y **el par no existe en el corpus**.

## PREGUNTA 2 -- producto en cuatro ejes, estrella en los otros cinco

Derive el corpus del propio generador de la entrega (`timestamp_for`) y conte lo que produce.

**Lo que SI es producto** (`:2275`, verificado): `12 meses x 24 horas x 1.684 offsets x 3 formatos
= 1.454.976`, y el test lo comprueba con `assertEqual(expected_product_size, source_product_passed)`.
Las cuatro coordenadas del producto estan completas. La afirmacion de la entrega es cierta.

**Lo que NO es producto:** las otras cinco coordenadas (`year`, `day`, `minute`, `second`,
longitud fraccionaria) no son ejes independientes: **las cinco se derivan del mismo contador
`ordinal`**. Sus marginales si son completas -- ano 10.000/10.000, dia 31/31, minuto 60/60,
segundo 60/60, fraccion 6/6 -- pero su **conjunta** esta clavada:

| Conjunta | Pares generados | Pares posibles | Cobertura |
|---|---|---|---|
| (minuto, segundo) | 60 | 3.600 | **1,67 %** -- `second == (7*minute) % 60`, funcion exacta |
| (minuto, long. fraccion) | 60 | 360 | **16,7 %** -- `fraccion == (minute % 6) + 1`, funcion exacta |
| (ano, segundo) | 30.000 | 600.000 | **5 %** |
| (ano, offset) | 1.454.976 | 16.840.000 | **8,64 %** |
| (dia, offset) | 52.204 | 52.204 | 100 % |
| (ano, mes) / (ano, hora) | 120.000 / 240.000 | 120.000 / 240.000 | 100 % |
| (ano, mes, hora) | 1.454.976 | 2.880.000 | 50,5 % |

Respuesta literal a la pregunta: **es un producto en un eje de cuatro coordenadas y una estrella en
el resto** -- exactamente el defecto que el Arquitecto me pidio vigilar. Y es un caso peor que la
lista de 0345: minuto, segundo y longitud fraccionaria no son tres coordenadas muestreadas, son
**una sola coordenada disfrazada de tres**, porque dos de ellas son funcion aritmetica exacta de la
primera. `(2027, "+06:15")` -- el par de M5 -- no aparece en el corpus. Sigue sin aparecer.

## El hallazgo de esta ronda -- el contrato ata la PRESENCIA del arreglo, no su propiedad

Esto es lo que me impide firmar, y no es "mas coordenadas".

La tarea declara en R0332-9: *"The production two-phase invariant, rather than that finite sample
alone, prevents a date exemption from suppressing non-phone PII in another item."* La invariante es
cierta del codigo entregado. **Pero nada la ata.** Lo unico que la vigila es `:2302`:

    self.assertEqual(1, source.count(two_phase_body))

un bloque de **diez lineas de texto exacto** sobre produccion. Eso comprueba que el bloque de dos
fases **esta**; no comprueba que **nada se ejecute antes que el**. Y ahi cabe el bypass entero.

Escribi cuatro mutantes que dejan **todas** las guardias actuales satisfechas:

- el bloque `two_phase_body` queda byte a byte identico (`source.count(...) == 1`);
- `contains_pii` conserva **exactamente un** `ast.For` de primer nivel, que es lo que exige
  `contains_pii_loop` en `:769`;
- **cero** `break` y **cero** `continue`, que es lo unico que mira `OuterLoopControlFlow` en `:772`;
- el guard es una expresion generadora, no una sentencia de bucle.

La forma, integra, es una sola linea insertada antes del bloque:

```python
    if any(DATE_RE.fullmatch(_x) and (<clave de coordenada>) for _x in value_list(value)):
        return False
    items = value_list(value)
```

**Control que importa:** la primera version de mis mutantes usaba un `for` de primer nivel, y la
suite los mato **los seis** en `contains_pii_loop` (`assertEqual(1, len(loops))`). La suite no esta
indefensa: caza la forma ingenua. Lo que no caza es la misma fuga escrita como expresion. Ambas
formas son igual de plausibles como defecto real, y las dos son la clase que esta tarea existe para
cerrar (AC3: *debe morir ante un bypass por REESTRUCTURACION, la forma que el AST no ve*).

### Las cuatro fugas vivas, medidas

Mis tres claves nuevas estan sobre coordenadas que **no nombre en r2** -- ni las vio el maker.

| # | Clave del bypass | Sonda | Fuente | Mutante | Suite |
|---|---|---|---|---|---|
| M5 | ano `2027` **x** offset `+06:15` | `2027-06-19T09:28:23+06:15` | (T,T,T) | (F,F,F) | **exit 0** |
| N1 | minuto `07` **x** segundo `07` | `2026-06-19T09:07:07+02:00` | (T,T,T) | (F,F,F) | **exit 0** |
| N2 | minuto `07` **x** fraccion de 5 digitos | `2026-06-19T09:07:07.11111+02:00` | (T,T,T) | (F,F,F) | **exit 0** |
| N3 | ano `2026` **x** segundo `07` | `2026-06-19T09:28:07+02:00` | (T,T,T) | (F,F,F) | **exit 0** |

Las cuatro sondas son miembros que `DATE_RE` exime (`fullmatch` no nulo, verificado). Las cuatro
ocultan un email real **en cualquiera de los dos ordenes** y ocultan tambien un termino de
instancia. Es la forma fuerte de SLIP-0325-1, la misma que motivo la tarea.

Y el contrato lo dice todo verde. Su propia linea de reporte con el bypass vivo dentro es
**identica** a la de la corrida limpia:

    base  TASK0332_BEHAVIOR product=1454976 source=1454976 mutants=3/3 ...
    m5    TASK0332_BEHAVIOR product=1454976 source=1454976 mutants=3/3 ...
    n1/n2/n3  identico

`mutants=3/3` es el punto: los tres mutantes que el contrato mata son los que **el propio contrato
se fabrica**, con `target_month`, `target_hour` y `target_offset` elegidos por el test para que
coincidan con sus propias sondas. Mueren por construccion. La discriminacion real frente a un
bypass ajeno la aporta unicamente el bucle del producto, y ese bucle solo ve cuatro coordenadas.

Hay una segunda consecuencia del arreglo de dos fases que conviene declarar: como la fase 1 detecta
el email **antes** de mirar `DATE_RE`, los 1.454.976 casos del producto son positivos **sin pasar
por la exencion de fecha**. El corpus, tal como esta escrito, acredita la fase 1; lo que acredita
sobre la exencion es solo lo que se ve al mutarla, y ahi vuelve a depender de que la coordenada
mutada caiga dentro de los cuatro ejes.

## Tabla vector por vector

| # | Vector | Resultado | Evidencia |
|---|---|---|---|
| P1a | SLIP-0332-5 (mes `03`) muere | **PASS** | suite exit 1, `:2287`, `1454976 != 1333728` |
| P1b | SLIP-0332-6 (hora `05`) muere | **PASS** | suite exit 1, `:2287`, `1454976 != 1394352` |
| P1c | SLIP-0332-4 (par `2027-` x `+06:15`) muere | **SLIPS** | M5, suite exit 0, fuga (T,T,T)->(F,F,F) |
| P2a | El corpus es producto en mes x hora x offset x formato | **PASS** | 12x24x1684x3 = 1.454.976, verificado |
| P2b | El corpus es producto en las demas coordenadas | **SLIPS** | (min,seg) 1,67 %; (min,frac) 16,7 %; (ano,offset) 8,64 % |
| P2c | Las cinco marginales restantes son completas | **PASS** | ano 10.000, dia 31, min 60, seg 60, frac 6 |
| N | Tres claves nuevas no vistas por el maker mueren | **SLIPS (0 de 3)** | N1, N2, N3, las tres exit 0 |
| I | La invariante de dos fases esta atada | **SLIPS** | atada solo por presencia de texto (`:2302`); 4 mutantes la respetan y fugan |
| PR | Produccion arreglada en la raiz | **PASS** | dos fases; el item fecha ya no aborta la lista |
| EQ | El refactor no cambia semantica (AC5) | **PASS** | 60.000 entradas, 0 divergencias viejo-vs-nuevo |
| G | Puertas del repo en clon limpio | **PASS** | 7 puertas exit 0, drift CLEAN |
| G' | Ejecutado de verdad en CI | **NO** (ajeno a 0332) | ver R0332-5 |

## Residuales declarados

- **R0332-10 (nuevo, bloqueante):** la invariante de dos fases -- la que R0332-9 nombra como lo que
  *previene* la supresion -- **no esta atada por ninguna puerta**. `:2302` comprueba que el bloque
  existe una vez; no comprueba que nada corra antes. Cuatro mutantes lo demuestran dejando intactos
  el texto del bloque, el conteo de bucles y la ausencia de `break`/`continue`. Esta es la unica
  razon por la que no firmo el cierre.
- **R0332-11 (nuevo, no bloqueante por si solo):** el corpus es producto en cuatro coordenadas y
  estrella en cinco, y de esas cinco tres estan funcionalmente clavadas
  (`second = 7*minute mod 60`, `fraccion = minute mod 6 + 1`). Un bypass con clave en un PAR de esas
  cinco es invisible. Demostrado: M5, N1, N2, N3.
- **R0332-12 (nuevo, informativo):** con la fase 1 delante, los 1.454.976 casos del producto dan
  positivo sin atravesar la exencion de fecha. El tamano del corpus no es, por si mismo, medida de
  lo que el corpus ata sobre la exencion.
- **R0332-9 (declarado por la entrega, exacto en su primera mitad):** el producto de cuatro ejes y
  las marginales completas son ciertos y los verifique. Lo que no puedo firmar es la segunda frase
  tal como esta escrita: la invariante **sostiene** la propiedad en el codigo de hoy, pero no la
  **previene** manana, porque nada la vigila.
- **R0332-8 (heredado, estructural, para el operador):** ningun muestreo finito cierra la clase.
  El producto cartesiano completo sobre las nueve coordenadas es del orden de 10^17 casos. Esto
  refuerza que el camino no es mas corpus: es atar la invariante.
- **R0332-3 (heredado, no bloqueante):** exhaustividad solo sobre digitos ASCII.
- **R0332-4 (heredado, empeora):** el contrato se apoya ahora en un ancla de **diez lineas de texto
  exacto** sobre produccion. Un `black` o un renombrado de `items` pone el contrato rojo sin que
  haya defecto, y aun asi no ata la propiedad. Fragilidad alta y garantia baja a la vez.
- **R0332-5 (ajeno a 0332, ya escalado):** CI no ejecuta nada; `647ba7e3` no tiene run. El contrato
  de esta tarea se ha ejecutado en CI cero veces. No pesa en mi veredicto.

## Lo que pido -- criterio, no lista

Deliberadamente **no pido anadir coordenadas**. Pedirlo reproduce el patron: estrecha el dano y deja
la clase abierta, y ya lo he provocado yo una vez en r1.

1. **Atar la invariante, no su texto.** El negativo debe fallar ante un bypass que (a) suprima por
   comportamiento el PII no-telefonico de un item hermano usando un item con forma de fecha, y
   (b) deje satisfechas **todas** las guardias vigentes a la vez: el conteo de bucles de `:769`, el
   visitante de `break`/`continue` de `:772` y el ancla de texto de `:2302`. La forma y las
   coordenadas las elijo yo en el re-juicio, y no seran las cuatro de este documento.
2. **Corregir la frase de R0332-9** para que diga lo que es cierto: la invariante de dos fases
   sostiene la propiedad en el codigo entregado, y esta atada **solo por presencia textual**. Si se
   opta por cerrar con residual, esta correccion es innegociable: un residual que afirma prevencion
   donde hay cuatro contraejemplos vivos es peor que no declarar nada.
3. **No aceptare** anadir `2027-`/`+06:15`, el minuto `07`, el segundo `07` ni la fraccion de cinco
   digitos a ninguna lista de casos ni a ningun `target_*`. Eso mata mis cuatro sondas sin cambiar
   la clase, y lo tratare como reintroduccion del patron.

## Bucle de correccion esperado

- **Remediacion:** la de arriba, punto 1 y punto 2. Es acotada y no exige recorpus.
- **Puertas afectadas para el re-juicio**, en clon limpio sobre el commit nuevo: las siete de la
  tabla de reproduccion, mas mi bateria de mutantes de produccion con claves nuevas.
- **Re-juicio antes del commit de cierre**, como siempre.
- **Maximo 1 iteracion mas.** Ya escale en r2 y vuelvo a escalar ahora, asi que lo digo con la
  alternativa encima de la mesa: **cerrar TASK-0332 aceptando R0332-10, R0332-11 y R0332-12
  declarados por escrito en la tarea, con la frase de R0332-9 corregida, y abrir R0332-10 como
  tarea propia**, es una decision legitima del operador y yo la respetaria. Lo que no puedo firmar
  es el cierre con la clase abierta **y** con un residual que afirme que esta cerrada.

## Respuesta a las dos preguntas del Arquitecto

*Los tres escapes mueren?* **Dos si, uno no.** El mes y la hora mueren por comportamiento en el
assert correcto -- eso es merito de la remediacion. La conjuncion `2027-` con `+06:15` sigue viva,
y le he anadido tres companeras que el maker no ha visto.

*El corpus es el PRODUCTO de coordenadas o sigue siendo una estrella?* **Las dos cosas.** Es
producto exacto en mes x hora x offset x formato, 1.454.976 casos verificados, y es estrella en
ano, dia, minuto, segundo y fraccion, donde ademas tres de esas cinco son funcion aritmetica de una
sola. Pero el hallazgo de esta ronda no esta en el corpus: la produccion **si** se arreglo bien, y
lo que falta es que una puerta ate ese arreglo. Hoy la unica que lo intenta comprueba que el bloque
de diez lineas este presente, y un bypass que lo respete letra por letra pasa entero.

-- Analista
