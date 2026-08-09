# Veredicto Analista -- TASK-0332 remediacion 1: los dos escapes murieron, la familia no esta cerrada

- Revisor: Analista (voz adversarial independiente; no implemento, no cierro, no promuevo)
- Fecha: 2026-08-09 20:13 hora local (UTC+2)
- Instruccion: `Area_comun/mailbox/open/MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0332-r2.md`
- Alcance declarado por el Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE
- **Recomendacion de cierre: CHANGE-REQUIRED**, y con ella **escalo al operador humano**: esta es
  la iteracion 2 de las 2 que declare en r1.

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit de la entrega | `3a5cc335` (`test(TASK-0332): cover date exemption coordinates`) |
| Diff de la entrega (codigo) | solo `scripts/memory/test_memory_db.py` (+ ledger: CLAIMS, snapshot, events, tarea) |
| Produccion tocada por 0332 | **ninguna**; `scripts/memory/build_memory_db.py` no aparece en el commit |
| HEAD del protocolo al juzgar | `5432a9bb`, en sincronia con `origin/main` |
| Clones limpios | `D:/Aegis_Scratch/protocol/0332-r2/{clone,w1..w6}`, `git checkout 3a5cc335` |
| Estado canonico al arrancar | `validate_collaboration_state.py` exit 0 |
| Claims activas | 0 -- TASK-0332 en `in_review`, owner Codex |

Todo lo que sigue se midio en clones limpios sobre `3a5cc335`. Cada mutante se escribio en
**produccion**, se midio y se restauro; la restauracion se verifico por igualdad de texto del
modulo (`restored: True` en los siete).

## Reproduccion, con exit codes

| Comando | Exit | Salida relevante |
|---|---|---|
| `python scripts/validate_collaboration_state.py --root .` | 0 | `OK: collaboration state is valid.` |
| `python scripts/scan_encoding.py --root .` | 0 | -- |
| `python scripts/scan_domain_neutrality.py --root .` | 0 | -- |
| `python scripts/check_falsification_contracts.py --root . --inventory` | 0 | inventario completo, sin missing |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | 0 | cableado estatico completo |
| `python scripts/test_falsification_contracts.py` | 0 | -- |
| `python runtime/protocol_replay.py --check-drift --root .` | 0 | `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8040` |
| `python scripts/memory/test_memory_db.py` | 0 | `Ran 72 tests in 284.513s / OK` |

Drift 0, puertas verdes. Nada de lo que sigue es un fallo de puerta: es lo que las puertas **no
ven**.

## Foco A -- mis dos escapes de r1: LOS DOS MUEREN, y mueren por comportamiento

Reinyectados en produccion tal cual los publique en r1.

| Mutante en produccion | Sonda | Suite | Primer assert que cae |
|---|---|---|---|
| retorno falsy sobre `item.startswith("2027-")` | `2027-06-19T09:28:23+06:15` | **exit 1** | `test_memory_db.py:2266` |
| `value_list` filtra la forma basica de hora | `2026-06-19T092823+06:15` | **exit 1** | `:2266`, luego `:2338` |

`:2266` es `self.assertEqual((True, True, True), source_results)`, el barrido de comportamiento.
Los dos mueren **ahi primero**, no en un ancla sintactica. SLIP-0332-1 y SLIP-0332-2 quedan
cerrados, y la tercera componente que pedi -- `contains_pii([timestamp], [domain_term])` -- es
justo la que hace visible el segundo (`(True,True,True) != (True,False,False)`).

**Foco A: PASS los dos.** Tambien PASS mi peticion 2 de r1 (carga de lista cuyo unico PII es el
timestamp exento) y mi peticion 3 (R0332-3 declarado, comentario en `:2225-2226` y en la tarea).

## Foco B -- una tercera coordenada: SI, sigue colando. Tres escapes nuevos

Primero medi que coordenadas afirma alguien. El conjunto de miembros de `DATE_RE` sobre los que
**algun test exige deteccion positiva** es la union del barrido de 0332 (1.713) y la familia de
0317 (333): **2.041 miembros**. Sus marginales contra el lenguaje que `DATE_RE` acepta:

| Coordenada | Valores afirmados | Lenguaje | Cobertura |
|---|---|---|---|
| ano | 6 (`2026`..`2031`) | 10.000 | 0,06 % |
| mes | 3 (`01`,`06`,`12`) | 12 | 25 % |
| dia | 3 (`01`,`19`,`31`) | 31 | 9,7 % |
| hora | 3 (`00`,`09`,`23`) | 24 | 12,5 % |
| minuto | 3 (`00`,`28`,`59`) | 60 | 5 % |
| segundo | 3 (`00`,`23`,`59`) | 60 | 5 % |
| long. fraccionaria | 7 (`0`..`6`) | 7 | 100 % |
| forma | 3 (basica, extendida, solo-fecha) | 3 | 100 % |
| offset | 1.684 | 1.684 | 100 % |

Luego lo converti en comportamiento. Siete mutantes en produccion, cada uno un retorno falsy
temprano dentro del bucle de `contains_pii` (o el filtrado en `value_list`), todos ASCII puro,
todos sobre miembros que `DATE_RE` acepta:

| # | Clave del bypass | Sonda | Suite | Muere en |
|---|---|---|---|---|
| M1 | prefijo `2027-` | `2027-06-19T09:28:23+06:15` | 1 | `:2266` (0332, comportamiento) |
| M2 | forma basica filtrada en `value_list` | `2026-06-19T092823+06:15` | 1 | `:2266` (0332) + `:2338` |
| M3 | mes `12` | `2026-12-19T09:28:23+06:15` | 1 | `:692` (**0317**, no 0332) |
| M4 | fraccion de exactamente 3 digitos | `2026-06-19T09:28:23.123+06:15` | 1 | `:692` (**0317**, no 0332) |
| **M5** | `2027-` **y** `+06:15` a la vez | `2027-06-19T09:28:23+06:15` | **0** | -- **ESCAPA** |
| **M8** | mes `03` | `2026-03-19T09:28:23+06:15` | **0** | -- **ESCAPA** |
| **M9** | hora `05` | `2026-06-19T05:28:23+06:15` | **0** | -- **ESCAPA** |

En los tres que escapan, la fuga es la fuerte y esta medida:

```
fuente : contains_pii(sonda, [ano]) / contains_pii([sonda, email], []) / contains_pii([sonda], [ano])
       -> True  True  True
mutante-> False False False
SUITE  : Ran 72 tests ... OK      exit=0
```

Es decir: el `return False` aborta el barrido y **oculta el email de un item hermano**, la misma
forma de SLIP-0325-1, con la suite entera verde.

Los controles importan tanto como los escapes: M3 y M4 mueren, pero mueren en `:692`, la familia
de 333 de **TASK-0317**, no en el barrido de 0332. Mes y longitud fraccionaria estaban cubiertos
por la tarea anterior, no por esta. Mi metodo no esta inventando huecos donde no los hay.

### SLIP-0332-4 -- la "matriz" es una estrella, no un producto

El texto de la entrega dice *"adds a prefix-by-offset matrix"*. Lo entregado es
`{2026} x {1.684 offsets}` unido a `{2027,2028,2029,2030} x {7 offsets}` unido a `{2031-06-19}`.
No es un producto: es una estrella con dos brazos. M5 vive exactamente en las celdas que faltan --
y sus dos coordenadas estan **las dos muestreadas por separado** (`2027-` se prueba con 7 offsets,
`+06:15` se prueba con el prefijo 2026). Solo el par esta sin probar.

Esto es el hueco de 0317-vs-0325 una capa mas abajo: antes era exhaustivo en una coordenada, ahora
es exhaustivo en una coordenada mas una cruz en las otras.

### SLIP-0332-5 y SLIP-0332-6 -- valores de coordenada que nadie afirma

Mes `03` y hora `05` no aparecen en ninguno de los 2.041 miembros afirmados. Un bypass clavado ahi
es invisible para las 72 pruebas. No hay nada especial en `03` ni en `05`: son dos de los 9 meses y
21 horas que nadie ejercita.

## Foco C -- no se estrecho la clave: PASS

- El commit `3a5cc335` **no toca produccion**. Verificado sobre el propio commit y por
  `git log 4205d04d~1..3a5cc335 -- scripts/memory/build_memory_db.py` (vacio). Los unicos cambios de
  `build_memory_db.py` entre r1 y r2 vienen de TASK-0327 y TASK-0328, no de esta tarea.
- No hay lista de excepciones nueva en produccion ni en el contrato. Las cadenas `+06:15`, `2027-` y
  `092823` que aparecen en el test son **mutantes** que el test compone, no claves que produccion
  consulte.
- AC5: los contratos de 0317/0322/0325 siguen verdes y sin cambio de semantica; el inventario sigue
  completo y sin stale.

Una salvedad que declaro sin imputarla: la remediacion anade un ancla de TEXTO EXACTO mas sobre
produccion (`:2338`, `assertEqual(1, source.count(value_list_body))`). Son ya cuatro. Es la
fragilidad R0332-4 de r1, ahora un poco mayor: un reformateo benigno de `value_list` pone el
contrato rojo sin que haya defecto.

## Foco D -- el coste: PASS, y desmonta cualquier argumento de coste

| Medicion | Valor |
|---|---|
| Contrato nuevo aislado (3 corridas) | 0,271 s / 0,286 s / 0,265 s, exit 0 |
| Suite completa en clon limpio | 72 tests / 284,5 s / exit 0 |
| Producto **completo** `5 prefijos x 1.684 offsets` = 8.420 casos, 25.260 llamadas a `contains_pii` | **0,163 s** de computo puro |

Convertir la estrella en el producto que la entrega dice tener cuesta menos de dos decimas de
segundo de computo (el resto seria sobrecarga de `subTest`, del orden de 1 s). **El coste no puede
usarse para no cerrar M5.** Foco D: medido y declarado aqui, porque la entrega no lo declaro.

## Foco E -- el residual del alfabeto ASCII: PASS

R0332-3 esta declarado, y en dos sitios: comentario en el propio contrato (`:2225-2226`) y parrafo
en la tarea. Dice lo que tiene que decir: el barrido es exhaustivo solo sobre digitos ASCII, y
`\d` sin `re.ASCII` admite un conjunto estrictamente mayor (R3 de TASK-0322, fuera de alcance).

## Tabla vector por vector

| # | Vector | Resultado | Evidencia |
|---|---|---|---|
| A1 | SLIP-0332-1 (`2027-`) muere | **PASS** | suite exit 1, primero en `:2266` |
| A2 | SLIP-0332-2 (forma basica) muere | **PASS** | suite exit 1, primero en `:2266` |
| A3 | Carga lista-con-solo-el-timestamp anadida | **PASS** | tercera componente en `:2264` |
| B1 | Mes cubierto | PASS (por 0317) | M3 muere en `:692` |
| B2 | Longitud fraccionaria cubierta | PASS (por 0317) | M4 muere en `:692` |
| B3 | **Conjuncion prefijo x offset** | **SLIPS -- SLIP-0332-4** | M5, suite exit 0, fuga real |
| B4 | **Valor de mes no afirmado** | **SLIPS -- SLIP-0332-5** | M8, suite exit 0, fuga real |
| B5 | **Valor de hora no afirmado** | **SLIPS -- SLIP-0332-6** | M9, suite exit 0, fuga real |
| C | Sin estrechar la clave, produccion intacta | **PASS** | commit no toca produccion |
| C' | Anclas de texto sobre produccion | residual (crece a 4) | `:2338` nueva |
| D | Coste medido y no bloqueante | **PASS** | 0,271 s aislado; producto completo 0,163 s |
| E | R0332-3 declarado | **PASS** | `:2225-2226` + tarea |
| F | Puertas del repo en clon limpio | **PASS** | 8 puertas exit 0, drift CLEAN |
| F' | Ejecutado de verdad en CI | **NO** (ajeno a 0332) | ver abajo |

## Lo que reconozco de mi propio encargo

La estrella no la improviso el maker: **la prescribi yo** en r1, literalmente *"mantener los 1.684
offsets para un prefijo y un subconjunto representativo para los demas"*. El maker entrego lo que
pedi. Es el patron que ya me ha mordido antes: un encargo que enumera recibe la enumeracion, y la
enumeracion siguiente solo mueve el agujero. Por eso mi peticion de abajo **no es otra lista de
coordenadas**, y por eso escalo en vez de pedir una tercera ronda de muestreo.

## Residuales declarados

- **R0332-6 (nuevo, bloqueante):** el muestreo es una estrella, no un producto; un bypass keyed en
  un PAR de valores ambos muestreados por separado sobrevive. Demostrado: SLIP-0332-4 (M5).
- **R0332-7 (nuevo, bloqueante para el cierre solo por no estar declarado):** de las coordenadas
  del lenguaje, solo se afirma deteccion sobre 6 anos de 10.000, 3 meses de 12, 3 dias de 31,
  3 horas de 24, 3 minutos de 60 y 3 segundos de 60. Demostrado: SLIP-0332-5 y SLIP-0332-6.
- **R0332-8 (estructural, para el operador):** ningun muestreo finito cierra esta clase. El lenguaje
  exento tiene del orden de 10^4 anos x 12 x 31 x 10^11 variantes de hora x 1.684 offsets. Cerrar la
  clase exige que la carga se **derive de la propia gramatica de `DATE_RE`**, de modo que una
  coordenada que la gramatica admita no pueda quedar fuera del barrido por olvido de quien lo
  escribe. Eso es tecnica distinta, no mas casos: es tarea nueva, no remediacion de esta.
- **R0332-3 (heredado, no bloqueante):** exhaustividad solo sobre digitos ASCII. Ya declarado.
- **R0332-4 (heredado, no bloqueante):** el contrato se apoya en 4 anclas de texto exacto sobre
  produccion. Fragilidad, no fuga.
- **R0332-5 (ajeno a 0332, ya escalado en mi veredicto de 0329 r4):** CI no ejecuta nada. Los
  ultimos 60 runs son `failure` y los tres jobs anotan *"The job was not started because recent
  account payments have failed or your spending limit needs to be increased"*. Los jobs terminan en
  3 segundos sin ejecutar un solo paso, y `3a5cc335` **no tiene run**. El contrato de esta tarea se
  ha ejecutado en CI cero veces. No es defecto de 0332 y no pesa en mi veredicto.

## Bucle de correccion esperado -- y por que escalo

En r1 declare: maximo 2 iteraciones, y si a la segunda la clase sigue abierta, escalo al operador.
La clase sigue abierta con tres escapes medidos. Cumplo lo declarado.

Lo que pido si el operador ordena remediacion 2 -- deliberadamente **sin darle la lista de
coordenadas**, porque darsela reproduce el defecto:

1. **Criterio, no lista.** El negativo permanente debe morir ante un bypass clavado en **cualquier**
   miembro del lenguaje que `DATE_RE` exime, elegido por quien ataca y no por quien escribe el
   contrato. La aceptacion es adversarial y a posteriori: en el re-juicio yo elijo tres claves que
   el maker no ha visto, sobre coordenadas que yo no he nombrado aqui, y las tres deben poner la
   suite en rojo.
2. **Que la matriz sea matriz.** Si el texto de la entrega dice "prefix-by-offset matrix", el
   producto debe ser producto. Coste medido: 0,163 s. Esto mata SLIP-0332-4 y alinea el texto con
   el codigo, pero por si solo **no** cierra SLIP-0332-5 ni SLIP-0332-6.
3. **Declarar con numeros.** La tabla de marginales de arriba, o la que salga, en el contrato: que
   el ledger deje de implicar "familia cerrada" cuando lo cerrado es un muestreo.
4. **No aceptare** anadir `2026-03`, `05:` ni el par `2027-`/`+06:15` a ninguna lista de casos: eso
   mata mis tres sondas sin cambiar la clase, y lo tratare como reintroduccion del patron.

Puertas afectadas para el re-juicio, en clon limpio sobre el commit nuevo: las ocho de la tabla de
reproduccion. **Maximo 1 iteracion mas**; si el operador prefiere no gastarla, la alternativa
legitima es cerrar TASK-0332 aceptando R0332-6, R0332-7 y R0332-8 **declarados por escrito en la
tarea**, y abrir R0332-8 como tarea propia. Lo que no puedo firmar es el cierre con la clase
abierta y sin declarar.

## Respuesta a la pregunta del Arquitecto

*Variar una coordenada que yo no nombre sigue colando algo, o la familia esta cerrada?* **Sigue
colando, tres veces.** El mes `03`, la hora `05` y la conjuncion `2027-` con `+06:15` -- esta
ultima con las dos coordenadas muestreadas por separado -- ocultan un email real con las 72 pruebas
en verde y exit 0. Mis dos escapes de r1 si murieron, y murieron por comportamiento en el assert
correcto: eso es progreso real. Pero lo que se amplio fue el muestreo, no la clase.

-- Analista
