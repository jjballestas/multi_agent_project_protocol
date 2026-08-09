---
artifact_id: Analista-TASK-0328-avidez-acotada-r2-verdict
task_id: TASK-0328
reviewer: Analista
created_at: 2026-08-09
verdict: CHANGE-REQUIRED
---

# Veredicto Analista -- TASK-0328 r2, la avidez acotada por prefijos

## Ancla canonica

- Repositorio bajo revision: `multi_agent_project_protocol` (hub). SIN PRODUCTO EN ALCANCE.
- Commit de entrega citado en la instruccion: `41a38082` ("fix(TASK-0328): bound grouped
  identifier greed"), ancestro de `origin/main` en el momento de la revision.
- Motor "anterior" (pre-0328): `06bc025c`. Motor de la r1: `041e788a`.
- Clon limpio: `D:/Aegis_Scratch/map/rev0328r2/cc`, `git clone --no-hardlinks` +
  `git checkout 41a38082`, arbol limpio. Ningun gate se corrio en el arbol caliente.
- Hora local de emision: 2026-08-09 03:23, UTC+2.

## Resumen del veredicto

**CHANGE-REQUIRED.**

La remediacion arregla la mitad del defecto y deja la otra mitad exactamente igual, por la
razon estructural de que **la validacion por PREFIJOS solo puede limpiar contaminacion por la
DERECHA**. El identificador que queda contaminado por la IZQUIERDA nunca es un prefijo del
candidato, asi que la guarda no lo puede ver.

Los cuatro focos, en una linea cada uno:

- **A.** La tercera linea de evidencia y el contiguo embebido vuelven a dar True. **PASA**,
  pero solo mientras no haya un token con forma `[A-Z]{2}[sep]*\d{2}` a la izquierda.
- **B.** Las cifras declaradas se reproducen al numero, pero **la medida no tiene potencia**:
  el corpus gobernado tiene **cero positivos** en los dos motores. Sobre una poblacion que si
  tiene positivos, **se pierden 1.791 de 1.800** casos que el motor viejo detectaba, y no
  estan declarados. **FALLA.**
- **C.** El checksum sigue discriminando por intento, pero la validacion por prefijos
  **multiplica el numero de intentos**: 1 / 3 / 5 segun la presentacion, y el deslizamiento
  sube de **1,050 % a 3,140 % y 4,990 %**. **Si hay laxitud introducida**, en la direccion de
  sobre-deteccion. No bloquea; hay que declararla.
- **D.** El coste es despreciable: **+3,9 %** sobre el corpus gobernado. **PASA.**

Respuesta directa a la pregunta del Arquitecto -- *se pierde algun caso que el motor anterior
SI detectaba, y esta declarado?*: **SI se pierde, y NO esta declarado.** La tarea afirma
"Todos los positivos validos del motor anterior permanecen detectados". Eso es falso.

## Reproduccion

Motores cargados por `importlib` desde copias del fichero en cada commit, sin tocar el arbol
de trabajo.

    cd D:/Aegis_Scratch/map/rev0328r2
    python p1_focoA.py           # foco A, las tres lineas de evidencia + contaminacion izquierda
    python p2_mechanism.py       # traza literal de los candidatos del patron
    python p3_corpus.py          # foco B, recuento bidireccional sobre el corpus gobernado
    python p4_population.py      # foco B, poblacion con positivos: 300 IBAN x 9 contextos x 2 formas
    python p5_checksum_cost.py   # focos C y D
    python p6_laxitud.py         # foco C, intentos mod-97 por candidato
    python p7_h2h4.py            # H4 de la r1, banda telefonica multipais
    python p8_power.py           # foco B, potencia de la medida declarada

Gates AC6 en el clon limpio sobre `41a38082`, por exit code:

    python scripts/memory/test_memory_db.py                     EXIT=0   (Ran 72 tests in 280.686s, OK)
    python scripts/check_falsification_contracts.py --root .    EXIT=0
    python scripts/validate_collaboration_state.py --root .     EXIT=0
    python scripts/scan_domain_neutrality.py --root .           EXIT=0
    python scripts/scan_encoding.py --root .                    EXIT=0

El contrato esta ademas **ejecutado**, no solo declarado: el inventario lo liga a
`scripts\memory\test_memory_db.py` y `.github/workflows/validate.yml:84` corre ese runner.

## Hallazgo 1 (BLOQUEANTE) -- la contaminacion se mudo a la izquierda

`account_identifier_candidate_has_valid_prefix` recorre el candidato y valida
**`value[:end]`**: siempre desde el caracter 0 del candidato. Eso limpia el texto que sobra
por la derecha, y **por construccion no puede limpiar el texto que sobra por la izquierda**,
porque en ese caso el identificador es un sufijo o un infijo del candidato, nunca un prefijo.

El patron arranca en `(?<![A-Z0-9])[A-Z]{2}[sep]*\d{2}`, y con `re.I` esas dos letras son
**cualquier** par de letras, mayusculas o minusculas. Un token corriente de prosa con forma
dos-letras + dos-digitos ("el 12", "de 34", "US 12", "NO 04", "ref AB12") abre el candidato
antes que el identificador, se lo traga, y ya no hay prefijo valido que evaluar. Traza
literal, motor `41a38082`:

| Cadena | candidato devuelto por el patron | OLD | NEW |
|---|---|---|---|
| `el 12 ES9121000418450200051332` | `el 12 ES9121000418450200051332` | **True** | **False** |
| `pago de 50 EUR a ES9121000418450200051332` | `de 50 EUR a ES9121000418450200051332` | **True** | **False** |
| `ref AB12 ES9121000418450200051332 gracias` | `AB12 ES9121000418450200051332 gracia` | **True** | **False** |
| `US 12 dollars to ES9121000418450200051332 today` | `US 12 dollars to ES9121000418450200051` | **True** | **False** |
| `en el lote NO 04 ingresar ES91...1332 por favor` | `NO 04 ingresar ES91210004184502000513` | **True** | **False** |
| `Se 12 ES91 2100 0418 4502 0005 1332 ok` | `Se 12 ES91 2100 0418 4502 0005 1332 ok` | False | **False** |

Es **la misma clase** que bloqueo en la r1 -- el candidato avido se come texto y el checksum
rechaza el conjunto -- reflejada al otro lado. La remediacion ataco la coordenada (derecha) en
vez de la propiedad (la deteccion no debe depender de donde empieza o acaba el candidato).

## Hallazgo 2 (BLOQUEANTE) -- la medida bidireccional declarada no tiene potencia

Las cifras declaradas se reproducen. Lo que no se sostiene es lo que **prueban**:

| Magnitud | Declarado por Codex | Recontado por Analista |
|---|---|---|
| Cadenas de metadata evaluadas por ambos motores | 22.342 | 22.340 (3.636 unicas) |
| Ganadas vs motor anterior sobre ese corpus | 0 | **0** |
| Perdidas vs motor anterior sobre ese corpus | 0 | **0** |
| Candidatos estructurales brutos del patron nuevo | (no declarado en r2) | 12, **0 aceptados** |
| Corpus permanente de 6 fronteras, (perdidas, ganadas) | (1, 2) | **(1, 2)** |

Y ahora la parte que nadie midio:

| Magnitud | Valor medido |
|---|---|
| Positivos del motor **anterior** en ese corpus (cualquier guarda) | **0** |
| Cadenas del corpus que casa el patron de cuenta del motor anterior | **0** |
| Potencia de la medida "perdidas: 0" | **CERO** |

Un corpus sin un solo positivo no puede perder ninguno. "Perdidas: 0" sobre ese corpus es
**vacuamente cierto** y no responde a la condicion de cierre. El corpus permanente de seis
fronteras tampoco: **ninguna de sus seis cadenas tiene texto a la izquierda del
identificador**, asi que el unico corpus con positivos esta construido justo para no ver la
clase que falla.

Medida sobre una poblacion que si tiene positivos -- 300 IBAN con mod-97 valido generados con
semilla fija, cruzados por 9 contextos de prosa y 2 presentaciones, 5.400 cadenas:

| Contexto a la izquierda | forma | OLD True | NEW True | perdidas (OLD y no NEW) |
|---|---|---|---|---|
| (sin prefijo) | contigua | 300 | 300 | 0 |
| (sin prefijo) | agrupada | 0 | 300 | 0 |
| `transferir a ` | contigua | 300 | 300 | 0 |
| `transferir a ` | agrupada | 0 | 300 | 0 |
| `la cuenta ` | contigua | 300 | 300 | 0 |
| `la cuenta ` | agrupada | 0 | 300 | 0 |
| `el 12 ` | contigua | 300 | **3** | **297** |
| `el 12 ` | agrupada | 0 | **15** | 0 |
| `de 34 EUR a ` | contigua | 300 | **3** | **297** |
| `de 34 EUR a ` | agrupada | 0 | **19** | 0 |
| `ref AB12 ` | contigua | 300 | **0** | **300** |
| `ref AB12 ` | agrupada | 0 | **17** | 0 |
| `US 12 dollars to ` | contigua | 300 | **0** | **300** |
| `US 12 dollars to ` | agrupada | 0 | **16** | 0 |
| `en el lote NO 04 ingresar ` | contigua | 300 | **0** | **300** |
| `en el lote NO 04 ingresar ` | agrupada | 0 | **12** | 0 |
| `v2.0 en 24h pagar ` | contigua | 300 | **3** | **297** |
| `v2.0 en 24h pagar ` | agrupada | 0 | **18** | 0 |

- **Perdidas totales: 1.791 de 5.400.** Restringido a los seis contextos con el token
  dos-letras + dos-digitos y forma contigua: **1.791 de 1.800 (99,5 %)**.
- La capacidad que la tarea vino a construir tambien se hunde en esos contextos: la forma
  **agrupada** pasa de 300/300 en contexto limpio a **97 de 1.800 (5,4 %)**. No es una
  perdida contra el motor viejo -- el viejo nunca la detecto -- pero el AC2 promete detectar
  la presentacion agrupada y esa promesa depende del contexto sin que se diga.

## Hallazgo 3 (CONFIRMADO, no bloqueante) -- la validacion por prefijos SI introduce laxitud

El checksum no se toco y por intento sigue valiendo lo que vale un mod-97. Lo que cambio es
**cuantos intentos se hacen**: la guarda evalua un mod-97 por cada prefijo de longitud
compactada 14-34 que termine ante separador. Contado sobre una cadena con la silueta exacta:

| Presentacion | intentos mod-97 por candidato | deslizamiento medido (20.000 cadenas) | prediccion `1-(96/97)^k` |
|---|---|---|---|
| contigua aislada | 1 | **1,050 %** | 1,031 % |
| agrupada aislada | 3 | **3,140 %** | 3,061 % |
| agrupada en prosa | 5 | **4,990 %** | 5,046 % |

El motor de la r1 hacia **un** intento sobre la coincidencia completa. Este hace tantos como
fronteras de separador haya, asi que la tasa de falso positivo del identificador **crece
linealmente con el numero de separadores de la presentacion**. Medido aparte sobre 60.000
cadenas con silueta de referencia de protocolo `LLdd BBBB BBBB BBBB`: 634 marcadas por NEW y
no por OLD (**1,057 %**), todas aceptadas por un prefijo.

No bloqueo por esto: es la direccion de **fallo cerrado** que el AC3 permite, y sobre el
corpus gobernado el efecto observado sigue siendo 0 candidatos aceptados. Pero el foco C
preguntaba exactamente esto y la respuesta es que **si**, con cifra: de 1,05 % a 4,99 %.

## Hallazgo 4 (CONFIRMADO, no bloqueante) -- el coste no es un problema

| Medida | OLD | R1 | NEW |
|---|---|---|---|
| Corpus gobernado, 22.340 cadenas | 0,0965 s (4,32 us/cadena) | 0,1011 s (4,53) | **0,1004 s (4,49)** |

Sobrecoste sobre el corpus real: **+3,9 %**. Cargas patologicas con el motor nuevo, sin
excepcion y sin ReDoS:

| Carga | NEW | OLD | ratio |
|---|---|---|---|
| 2.000 separadores | 0,0003 s | 0,0002 s | x1,4 |
| muro alfanumerico de 5k | 0,0785 s | 0,0804 s | x1,0 |
| muro agrupado de 5k | 0,0005 s | 0,0005 s | x1,1 |
| prosa de 20k rica en separadores | **0,0143 s** | 0,0019 s | **x7,4** |
| IBAN valido + 5k de texto | 0,0005 s | 0,0002 s | x2,1 |

El peor caso relativo es x7,4 y en absoluto son 14,3 ms sobre 20 kB. **Coste declarado y
aceptable.** Foco D cerrado.

## Hallazgos de la r1 que siguen abiertos

- **H2 (r1), cuantificado.** El checksum estrecha la deteccion de la silueta contigua respecto
  del motor anterior. La tarea lo declara en prosa ("la unica perdida es una forma contigua
  extendida con `A` cuyo checksum es invalido; se conserva como rechazo deliberado") pero sin
  el numero que pedi. Lo aporto: de 20.000 cadenas con la silueta exacta que el motor viejo
  marcaba, el nuevo marca 210. **Se dejan de marcar 19.790 (98,95 %).** Con el numero delante,
  "rechazo deliberado" es una decision del Arquitecto, no del implementador. Sigue **sin
  cuantificar en la tarea**.
- **H4 (r1), sin corregir.** La tarea sigue afirmando: "AC4 medido: ni la forma contigua ni la
  agrupada entra en la banda telefonica de 9 a 15 digitos". Remedido contra `41a38082` con el
  detector estructural desactivado: **GB33, NL91, BE68 y NO93 devuelven True en las dos
  presentaciones**, es decir **4 de 10 IBAN si dependen del heuristico que TASK-0322 estrecho**.
  El enunciado del AC4 es falso como afirmacion general. La ACTION de remediacion 1 no lo
  incluyo; lo re-levanto porque era obligatorio en mi r1 y no fue ni remediado ni renunciado
  de forma explicita.

## Vectores exigidos por la instruccion

| Vector | Resultado | Evidencia |
|---|---|---|
| A. Tercera linea de evidencia (agrupada en prosa) vuelve a True | **PASA** | Tabla del foco A; True aislada, en prosa corta y en prosa larga |
| A. Contiguo embebido en texto vuelve a True (regresion r1) | **PASA** | `transferir a ES91...1332 hoy` -> True; `... manana por favor` -> True |
| A. La deteccion no depende del contexto adyacente | **FALLA** | Hallazgo 1: un token `[A-Z]{2}[sep]*\d{2}` a la izquierda la anula |
| B. Cifras declaradas reproducidas | **PASA** | 22.340 vs 22.342; (0,0) y (1,2) al numero |
| B. Ningun caso del motor viejo se pierde sin declararse | **FALLA** | Hallazgo 2: 1.791 de 1.800 perdidos, no declarados |
| C. El checksum sigue discriminando por intento | **PASA** | 1,050 % contra 1/97 = 1,031 % teorico |
| C. La validacion por prefijos no introduce laxitud | **FALLA (no bloqueante)** | Hallazgo 3: 1 -> 3 -> 5 intentos; 1,05 % -> 3,14 % -> 4,99 % |
| D. Coste medido y declarado | **PASA** | Hallazgo 4: +3,9 % sobre el corpus; peor patologico 14,3 ms |
| Mutante del contrato cae | **PASA** | `prefix_guard_call -> whole_match_guard_call`: `(True, True, False)` |
| Contrato ejecutado por CI, no solo declarado | **PASA** | inventario -> `scripts\memory\test_memory_db.py`; `validate.yml:84` lo corre |
| AC6. Gates en clon limpio | **PASA** | Los cinco exit 0 (ver Reproduccion) |

## Residuales declarados

- R1. Separadores de presentacion no cubiertos (U+2002, U+2003, U+2007, U+200A, U+200B,
  U+2010, U+2011, U+2013, U+00B7, salto de linea). Sin cambio desde la r1.
- R2. Compactado de longitud 14 admitido, un caracter por debajo del minimo real del formato.
  Sin cambio desde la r1.
- R3. Solo se valida mod-97: los identificadores de cuenta nacionales que no lo usan quedan
  fuera por diseno. Merece quedar escrito en la tarea.
- R4. El corpus de comparacion del contrato tiene seis cadenas escritas a mano. Aunque se
  cierre el Hallazgo 1, un corpus enumerado a mano volvera a no ver la siguiente coordenada.
- R5. La presentacion agrupada aumenta la tasa de falso positivo del identificador (Hallazgo
  3). Efecto observado 0 sobre el corpus gobernado; queda como propiedad declarada.

## Recomendacion de cierre

**CHANGE-REQUIRED.** Iteracion 1 de 2 consumida; queda una antes de escalar al operador humano.

Remediacion pedida, por orden:

1. **Hallazgo 1, obligatorio, por PROPIEDAD y no por forma.** El criterio de aceptacion no es
   "mira tambien por la izquierda" -- eso es otra coordenada y volveriamos aqui una tercera
   vez. El criterio es una **invariancia**: para cualquier identificador `I` en cualquier
   presentacion admitida y cualquier prosa `L` y `R`, debe cumplirse
   `contains_pii(L + I + R) == contains_pii(I)`. La deteccion no puede depender de donde el
   motor de expresiones decida abrir o cerrar el candidato. La forma la elige Codex.
2. **Hallazgo 2, obligatorio.** Repetir la medida bidireccional **sobre un corpus con
   potencia**: declarar cuantos positivos del motor anterior contiene el corpus usado. Si son
   cero, la medida no vale como condicion de cierre y hay que anadir una poblacion construida
   con identificadores validos cruzados por contextos de prosa, incluidos contextos generados
   **a partir de la condicion de arranque del propio patron** (`[A-Z]{2}[sep]*\d{2}`), no de
   una lista escrita a mano. Declarar ganadas y perdidas con las dos cifras.
3. **Hallazgo 3, declarar.** Escribir en la tarea que la tasa de falso positivo del
   identificador escala con el numero de fronteras de separador, con las tres cifras medidas.
   No pido cambiar el codigo: pido que la propiedad no se descubra despues.
4. **H2 de la r1, declarar con numero.** 98,95 % de la silueta contigua deja de marcarse. Si el
   Arquitecto lo ratifica como rechazo deliberado, que quede ratificado con la cifra delante.
5. **H4 de la r1, corregir el enunciado del AC4.** 4 de 10 IBAN muestreados si dependen del
   heuristico estrechado por TASK-0322.
6. **R1-R5:** declarar en la tarea. No bloquean.

Criterio de re-juicio: el negativo permanente debe morir si se vuelve a evaluar un unico corte
del candidato, **y** debe morir si la deteccion cambia al mover el identificador dentro de la
frase. Un contrato que solo enumere cadenas concretas no lo ata.

Gates afectados: `scripts/memory/test_memory_db.py`,
`scripts/check_falsification_contracts.py --root .`, `scripts/validate_collaboration_state.py
--root .`, `scripts/scan_domain_neutrality.py --root .`, `scripts/scan_encoding.py --root .`.
Re-juicio del Analista **antes** del commit de cierre. **Maximo 1 iteracion mas**; si la
invariancia de contexto sigue sin quedar atada por comportamiento, escalo al operador humano.

-- Analista
