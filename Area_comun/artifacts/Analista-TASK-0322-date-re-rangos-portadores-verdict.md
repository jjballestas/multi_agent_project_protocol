---
artifact_id: ANALISTA-TASK-0322-date-re-rangos-portadores-verdict
task_id: TASK-0322
type: artifact
owner: Analista
reviewer: Analista
status: done
created_at: 2026-08-07
project: multi_agent_project_protocol
relates_to:
  - TASK-0317
  - SPEC-MEMORIA-HIBRIDA
---

# Veredicto Analista -- TASK-0322: estrechar DATE_RE con validacion de rangos

**Recomendacion de cierre: CHANGE-REQUIRED** (una sola iteracion, SIN tocar codigo).

El codigo entregado es correcto y lo he probado mas duro de lo que lo probo el maker: el
estrechamiento esta **demostrado estrictamente monotono por decision exacta de automatas**, no por
muestreo. Los seis AC se cumplen por exit code en clon limpio y el mutante tiene dientes reales.

Lo que bloquea el cierre no es el codigo: es **la cifra que entra al estado canonico**. El titulo de
la tarea y el handoff declaran que la poblacion de cadenas portadoras baja "del 2,9 al 0,05 por
ciento". Esa cifra es una propiedad del **generador** del AC1, no de la gramatica. Medida sobre el
lenguaje, la **densidad** de portadoras no baja: pasa de 49,50 por ciento a 49,44 por ciento. Lo que
si baja -- muchisimo, mas de lo prometido -- es el **tamano absoluto** del conjunto en el que hay que
confiar: 3.695 veces menos. Y el residual no es "1": es una **familia de formas** perfectamente
identificable. Eso es exactamente el "numero bonito" que el foco B pedia cazar, y la correccion deja
la tarea **mejor** de lo que esta escrita hoy.

## Anclaje canonico

| Elemento | Valor |
|---|---|
| Repo | `multi_agent_project_protocol` (hub, SIN producto en alcance) |
| HEAD revisado | `ff81d5fe` (= `origin/main` al abrir la revision) |
| Deriva durante la revision | `origin/main` avanzo a `d077d995` (TASK-0326) mientras yo revisaba. Comprobado: `git diff ff81d5fe d077d995 -- scripts/memory/build_memory_db.py` sale **vacio**. El artefacto bajo revision es identico bit a bit, asi que el anclaje sigue siendo exacto. |
| Commit del fix | `0eb060ee868bd10072ed5dd7061cae2f9d153ee3` |
| Commit del mutante | `dd3692f93d8c0d599a4d6001dc96841dd349f621` (head de la tarea) |
| Verificacion de anclaje | `git diff dd3692f9 ff81d5fe -- scripts/memory/build_memory_db.py` -> **vacio**. El artefacto de producto bajo revision es identico en el head de la tarea y en el head canonico. Los `+92` de `test_memory_db.py` entre ambos son de 0324/0325, fuera de alcance. |
| Clon limpio | `D:/Aegis_Scratch/mapp/a322`, detached en `ff81d5fe`, `git status --short` vacio |
| Mutante independiente | `D:/Aegis_Scratch/mapp/rev322` (copia del clon con el fix REVERTIDO a mano por el checker) |
| Hora local | 2026-08-07 09:24 (UTC+2) |

## Reproduccion (todo por exit code, en clon limpio)

| Comando | Exit | Evidencia |
|---|---|---|
| `python scripts/memory/test_memory_db.py` | **0** | `Ran 64 tests ... OK` (el maker declaro 62/62 en `dd3692f9`; los 2 extra son de 0324/0325) |
| `python scripts/memory/build_memory_db.py --root .` | **0** | 4.263 artefactos, 567 eventos, 15 tablas, `foreign_keys=1`, 0 cold-packs |
| `python scripts/check_falsification_contracts.py --inventory` | **0** | inventario declarado completo, incluye `NEG-MEMORY-DATE-RANGE-VALIDATION` |
| `python scripts/validate_collaboration_state.py` | **0** | `OK: collaboration state is valid` |
| `python scripts/scan_encoding.py` | **0** | `OK: encoding scan is clean` |
| `python scripts/scan_domain_neutrality.py` | **0** | limpio |

Estado canonico en el arbol vivo antes de revisar: `validate_collaboration_state.py` exit **0**. No he
revisado sobre arbol caliente: todos los numeros de arriba salen del clon.

## Tabla foco a foco / AC a AC

| # | Que pedia | Veredicto | Como lo probe |
|---|---|---|---|
| **A** | Monotonia: ninguna cadena nueva entra al lenguaje | **PASS (demostrado, no muestreado)** | Ver seccion A |
| **B** | Cual es la portadora que sobrevive y por que | **SLIP S1** | Ver seccion B |
| **C** | La exencion sigue siendo `fullmatch` | **PASS** (+ residual R2) | Ver seccion C |
| **D** | 14 vectores adyacentes + el mutante mata | **PASS** (+ nota) | Ver seccion D |
| **E** | Direccion del fallo: mas deteccion, nunca menos | **PASS** | Ver seccion E |
| AC1 | 2,9 pct de partida reproducible | **PASS** | Reimplemente el generador (seed `20260805`) fuera de la suite: 5.789/200.000 = 2,9 pct. Coincide exacto. |
| AC2 | Rangos reales sin perder formatos legitimos | **PASS** | Exhaustivo, no por muestra. Ver seccion D. |
| AC3 | Cero warnings nuevos de claves de fecha en clon limpio | **PASS** | Build exit 0 con **219** warnings totales, de los cuales **0** son de `created_at`/`updated_at`/`closed_at`. Reparto real: `spec_id` 123, `task_id` 86, `decision_id` 6, `to` 2, `supersedes` 1, `relates_to` 1 -- todos preexistentes y ajenos a esta tarea. |
| AC4 | Los 11 vectores de cola siguen rechazados; la exencion no deja pasar PII entera | **PASS** | Los 11 vectores verdes en la suite. Verifique por lectura y por comportamiento que en `contains_pii` la PII estructural (email/IBAN/DNI) se evalua **antes** del guard de `DATE_RE` y los terminos de dominio **despues**, sin `continue`: la exencion solo puede tapar un tramo de digitos con forma de telefono, nunca otra cosa. |
| AC5 | Declarar la poblacion final | **MET AS SPECIFIED, pero ver S1** | El 0,05 pct es reproducible bajo el metodo del AC1. Lo que objeto no es el numero: es lo que el numero dice que mide. |
| AC6 | Suite, build, drift, todo exit 0 en clon limpio | **PASS** | Tabla de reproduccion. |

---

## A. Monotonia -- PASS, y esta **demostrada**

No la muestree: la **deci**. Ambas gramaticas son regulares, asi que construi los automatas finitos de
las dos y calcule la diferencia:

```
L(NEW) - L(OLD)  ->  vacio     (NEW_MINUS_OLD_EMPTY: True)
L(OLD) - L(NEW)  ->  NO vacio  (el estrechamiento es propio)
|L(OLD)| = 2.222.446.222.400.000.100.000.000
|L(NEW)| =         601.390.561.112.067.720.000
```

`L(NEW)` es subconjunto **propio** de `L(OLD)`. No existe ninguna cadena que la gramatica nueva acepte
y la vieja rechazara. **No hay ensanche accidental.** El lenguaje aceptado se reduce a
1/3.695 del anterior (3,6 ordenes de magnitud; el intake prometia "casi dos").

Ademas del teorema, corri lo empirico para que quede traza reproducible sin la libreria de automatas
-- 0 violaciones en todo:

- Exhaustivo: 10.000 anos, 10.000 combinaciones mes x dia (00-99 x 00-99), 10^6 combinaciones
  `hh:mm:ss` (00-99 cada componente), 10^6 combinaciones compactas `hhmmss` (000000-999999),
  2 x 10^4 offsets `+-HH:MM` (00-99 x 00-99), longitudes de fraccion 0..9.
- Aleatorio diferencial: 3.000.000 de cadenas de producto cruzado sobre rangos completos,
  2.000.000 construidas **dentro** de `L(NEW)` por construccion, 2.000.000 de fuzz puro de alfabeto.

Comprobacion extra que el maker no hizo y que podia haber roto la monotonia: **`\d` en Python no es
ASCII**. Ambas gramaticas usan `\d` sin `re.ASCII`, asi que aceptan digitos decimales Unicode.
Verifique que la monotonia aguanta tambien ahi (todos los casos `mono_ok=True`), y de paso que el
estrechamiento **recorta** superficie Unicode: `2026-01-01` con mes y dia en indo-arabigo ahora se
rechaza, porque el primer digito de mes y dia paso a ser literal ASCII. Ver residual R3.

## B. La portadora que sobrevive -- **SLIP S1**

**La que sale del sorteo es `9592-12-22T10:41:54.27956-07:53`.** El tramo que la hace portadora es
`54.27956-07`: 11 caracteres, 9 digitos (`542795607`), justo en el minimo del heuristico. Es una marca
de tiempo perfectamente legitima: segundos + fraccion de 5 digitos + offset negativo. `.` y `-` estan
en la clase de caracteres de `PHONE_CANDIDATE_RE`, los `:` no; por eso el tramo `SS.fffff-HH` es el
unico que puede acumular 9 digitos seguidos sin que un `:` lo corte.

Hasta aqui, respondida la pregunta. **Lo que objeto es lo otro:** ese "1" no es el residual. Es una
muestra del residual.

Mapee las **33 formas** que tiene `L(NEW)` (solo-fecha, forma con dos puntos x fraccion 0..6 x zona
{nada, Z, +, -}, forma compacta x zona) y probe 4.000 instancias aleatorias de cada una. El caracter
de portadora **no depende de los valores, solo de la forma**, y es constante dentro de cada forma:

```
PORTADORAS  (2 de 33):  colon + fraccion de 5 digitos + offset NEGATIVO
                        colon + fraccion de 6 digitos + offset NEGATIVO
LIMPIAS    (31 de 33):  todo lo demas
```

Por que solo esas dos: el tramo maximo es `SS.fffff[f]-HH` = 6+n caracteres y 4+n digitos, y el
heuristico exige >= 9 caracteres y 9..15 digitos, luego n en {5,6}. El offset **positivo** no cuenta
porque `+` no esta en la clase de caracteres del heuristico y el `\+?` inicial solo alcanza `+HH`
(3 caracteres). Con `Z` o sin zona el maximo es 8 digitos. La forma compacta da 8 digitos. Y la fecha
sola, `YYYY-MM-DD`, da 8 digitos: por un digito no es portadora.

Consecuencia medida sobre el lenguaje, no sobre el generador:

```
                    portadoras / lenguaje      cardinal de portadoras
gramatica vieja        49,50 pct               1,100e24
gramatica nueva        49,44 pct               2,973e20
```

**La densidad de portadoras no baja. Lo que baja 3.699 veces es el numero absoluto de portadoras** --
en linea exacta con el 3.695 de reduccion del lenguaje entero. Dicho de otro modo: estrechar los
rangos quito muchisimas cadenas, pero quito portadoras y no-portadoras en la misma proporcion.

Por que el generador del AC1 da 0,05 pct: su filtro mas duro es el offset (841 de 10.000 por signo
sobreviven), asi que entre los supervivientes las formas con offset -- que son justo las unicas que
pueden ser portadoras -- quedan fuertemente infrarrepresentadas. El 0,05 pct es real bajo ese metodo y
el metodo esta declarado; pero **no mide la superficie residual**, y el titulo de la tarea lo presenta
como si lo midiera.

Un dato a favor del maker que tampoco esta declarado y que deberia estarlo: **dentro** de la familia
portadora el espacio controlable tambien se estrecho. Los dos primeros digitos del tramo son `SS`, que
paso de 00-99 a 00-59, y los dos ultimos son `HH` del offset, que paso de 00-99 a 00-14. Un movil
espanol (empieza por 6 o 7) ya no cabe: exigiria `SS` >= 60. Antes cabia.

**Lo que pido (S1, sin tocar codigo):** declarar el residual con nombre y calificar la metrica.
1. Nombrar la familia: *forma con dos puntos + fraccion de 5 o 6 digitos + offset numerico negativo*
   (2 de las 33 formas del lenguaje).
2. Decir que 2,9 pct y 0,05 pct son **relativos al muestreador del AC1**, no densidades del lenguaje.
3. Declarar la cifra que si es del cambio y que ademas es mejor: el conjunto en el que hay que confiar
   se reduce **~3,7e3 veces** (3,6 ordenes de magnitud, por encima de los "casi dos" del intake).
4. Corregir en consecuencia el titulo de la tarea, que hoy afirma la lectura de densidad.

Recomendado (no bloqueante): fijar la familia **por forma** con una asercion permanente sobre el mapa
de 33 formas. La asercion actual (`5789`/`2006`/`1`) es un candado sobre un flujo de RNG: caza el
ensanche, pero no distingue "se ensancho hasta admitir una tercera forma portadora" de "cambio el
generador de Python".

## C. La exencion sigue siendo `fullmatch` -- PASS

Los tres unicos consumidores de `DATE_RE` en codigo de producto usan `fullmatch`, ninguno `search` ni
`match`:

```
build_memory_db.py:555   if not ID_RE.fullmatch(item) and not DATE_RE.fullmatch(item):   (contains_pii)
build_memory_db.py:593   valid = isinstance(value, str) and bool(DATE_RE.fullmatch(value))  (validate_metadata)
build_memory_db.py:800   if not DATE_RE.fullmatch(created_at):                            (cold-pack)
```

Confirmado por mecanismo, como se pedia, y no por intuicion: `2026-02-31` solo puede ser exenta
siendo la cadena **entera**, luego no transporta nada. Y una comprobacion que refuerza la advertencia
del foco C: el ancla `$` **por si sola no basta**. Sobre `'2026-01-01\n'`, `fullmatch` devuelve False
pero `match` devuelve **True**, porque `$` casa antes de un salto final. La garantia descansa por
completo en que la llamada sea `fullmatch`; relajarla a `match` ya abriria el prefijo, sin necesidad
de llegar a `search`. Ver residual R2 sobre los dientes de esa garantia.

## D. Los 14 vectores y el mutante -- PASS

**Adyacencia.** 13 de los 14 son el adyacente exacto de su frontera: mes `00` y `13`, dia `00` y `32`,
hora `24`, minuto `60`, segundo `60`, los tres equivalentes en forma compacta (`240000`, `006000`,
`000060`), offset `+15:00`, `-14:01` (el adyacente del tope 14:00) y `+00:60`. El decimocuarto,
`2026-01-01T00:00:61.234567-89:00`, es compuesto (segundo 61 **y** offset 89), no adyacente puro.
No es seleccion comoda: la cobertura de adyacentes esta completa para todas las fronteras que esta
tarea introduce.

Y no me quede en los 14. **Verifique exhaustivamente** que se rechaza *todo* valor fuera de rango, no
solo el vecino: 10^4 combinaciones mes x dia, 10^6 de `hh:mm:ss`, 10^6 de `hhmmss`, 2 x 10^4 de
offset. Cero aceptaciones indebidas. Eso es estrictamente mas fuerte que la tabla de 14.

**El mutante mata de verdad.** No me fie del test del maker: hice mi propio mutante permanente en un
clon aparte (`rev322`), restaurando a mano la gramatica ancha en el **producto** y corriendo la suite
contra ella:

```
test_timestamp_ranges_reject_syntactic_non_dates            -> exit 1, FAILED (failures=15)
test_timestamp_range_narrowing_reduces_carrier_population   -> exit 1, AssertionError: 2006 != 200000
```

Los 15 fallos son los 14 vectores pasando a aceptarse mas la asercion de unicidad de la fuente. Si
alguien revierte el estrechamiento, la suite se cae a gritos. Dientes reales.

## E. Direccion del fallo -- PASS

Menos exenciones significa mas deteccion, y lo verifique por comportamiento en vez de por argumento.
Ejecute `contains_pii` con la gramatica vieja y con la nueva sobre **1.500.000** entradas (mitad con
forma de marca de tiempo, mitad fuzz):

```
casos detectados por la vieja y perdidos por la nueva:  0
casos detectados por la nueva y perdidos por la vieja:  28.736 de 200.000  (14,4 pct)
```

**Cero regresiones de deteccion.** Y los tres consumidores fallan cerrados en la misma direccion:
`contains_pii` mete mas items al heuristico; `validate_metadata` rechaza mas valores de fecha (aviso +
descarte); el lector de cold-packs lanza `ValueError` sobre mas entradas (falla ruidoso). No existe
ningun camino por el que estrechar la exencion haga que algo deje de detectarse.

## Residuales declarados

- **R1 (declarado por el maker, confirmado inocuo).** `2026-02-31`, `2026-04-31`, `2026-02-29` en ano
  no bisiesto siguen en gramatica: se validan rangos de componente, no calendario. Inocuo por el
  mecanismo del foco C: solo exime la cadena entera. Fuera del alcance de esta tarea.
- **R2 (nuevo, bajo).** La garantia "es `fullmatch`" solo tiene dientes en **uno** de los tres
  consumidores: `NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` fija por conteo de fuente la linea de
  `contains_pii`. Las llamadas de `validate_metadata` (593) y del lector de cold-packs (800) no estan
  fijadas por ninguna asercion: relajarlas a `match` no rompe ningun test. No es un fallo de 0322
  (viene de antes), pero el foco C lo convierte en un candidato natural a seguimiento.
- **R3 (nuevo, bajo).** `DATE_RE` usa `\d` sin `re.ASCII`: acepta digitos decimales Unicode en ano,
  segundo digito de dia/hora/minuto/segundo y fraccion. `validate_metadata` **acepta sin aviso**
  valores como `created_at` con ano en indo-arabigo. Es heredado (la gramatica vieja aceptaba mas), la
  monotonia aguanta y el gate `scan_encoding` del repo impide que algo asi llegue a un artefacto
  gobernado; pero el indexador de memoria por si solo no lo para.
- **R4 (nuevo, informativo).** El tercer consumidor de `DATE_RE` (cold-packs, linea 800) **no lo
  ejercita el corpus real**: el build en clon limpio reporta `cold_pack_count: 0`. El estrechamiento
  hace que ese camino lance `ValueError` sobre mas entradas; la direccion es la correcta (falla
  ruidoso), pero no hay evidencia de corpus para el.

## Bucle de arreglo esperado

- **Remediacion:** solo declaracion, **cero codigo**. Los cuatro puntos de S1: nombrar la familia
  portadora por forma, calificar 2,9/0,05 como relativos al muestreador del AC1, declarar la reduccion
  absoluta de ~3,7e3x del conjunto de confianza, y ajustar el titulo de la tarea. Opcional y
  recomendado: la asercion permanente por forma.
- **Gates afectados:** ninguno del producto. Si se toca el docstring del test o su asercion, vuelven a
  exigirse `python scripts/memory/test_memory_db.py` y
  `python scripts/check_falsification_contracts.py --inventory` en exit 0 y en clon limpio. Si solo se
  tocan handoff, contrato e indice: `validate_collaboration_state.py` y `scan_encoding.py` en exit 0.
- **Re-juicio:** re-reviso antes del commit de cierre, sobre el nuevo head y en clon limpio. Como no
  hay cambio de codigo, el re-juicio se limita a verificar la declaracion y que la suite siga en 0; no
  repito la prueba de monotonia, que ya esta demostrada sobre un artefacto que no se toca.
- **Tope:** maximo **2 iteraciones**. Si a la segunda la declaracion sigue sin nombrar el residual,
  escalo al operador humano en vez de seguir iterando.

## Firma

Revisado como **checker independiente**. No implemente, no promovi, no cerre y no ratifique nada.
El maker de TASK-0322 es Codex; yo no toque el codigo bajo revision -- el mutante que construi vive
fuera del arbol, en un clon de scratch.

-- Analista, 2026-08-07 09:24 (UTC+2)
