---
artifact_id: Analista-TASK-0328-identificador-agrupado-verdict
task_id: TASK-0328
reviewer: Analista
created_at: 2026-08-08
verdict: CHANGE-REQUIRED
---

# Veredicto Analista -- TASK-0328, el identificador agrupado

## Ancla canonica

- Repositorio bajo revision: `multi_agent_project_protocol` (hub). SIN PRODUCTO EN ALCANCE.
- Commit de entrega citado en la instruccion: `041e788a` ("feat(TASK-0328): detect grouped
  account identifiers"), ancestro de `origin/main` en el momento de la revision.
- Commit padre usado como motor "antes": `06bc025c`.
- Clon limpio: `D:/Aegis_Scratch/protocol/analista-0328/clone` (nuevo) y
  `D:/Aegis_Scratch/protocol/analista-0328/old` (padre). Los dos con `git clone --no-hardlinks`
  + `git checkout <commit>`, arbol limpio. Ningun gate se corrio en el arbol caliente.
- Hora local de emision: 2026-08-08, UTC+2.

## Resumen del veredicto

**CHANGE-REQUIRED.**

El ensanchamiento con separadores mas checksum mod-97 es, en abstracto, la forma correcta de
atacar el problema, y en las presentaciones **aisladas** funciona. Pero el ensanchamiento
introduce una propiedad nueva que nadie midio: **el separador admitido es el espacio y el cuerpo
admitido es `[A-Z0-9]`, asi que las palabras corrientes que siguen al identificador son
indistinguibles de bloques del identificador**. El patron las absorbe con avidez, el checksum
evalua la cadena absorbida, y falla.

Consecuencia medida, en las dos direcciones:

1. **El caso de evidencia que la propia tarea declara como el defecto a arreglar sigue dando
   False.** `"cuenta: ES91 2100 0418 4502 0005 1332 del ..."` -> False despues del arreglo.
2. **Aparece un escape NUEVO que el motor viejo NO tenia**: el identificador **contiguo**
   embebido en texto corriente pasa de detectado a no detectado.
   `"transferir a ES9121000418450200051332 hoy"` -> antes True, ahora False.

El punto 2 es un retroceso neto de cobertura de PII causado por esta entrega, en la direccion
que el AC3 prohibe expresamente ("nunca relajando la deteccion").

Respuesta directa a la pregunta del Arquitecto: **el checksum si discrimina** (tasa de deslizamiento
medida 1,055% sobre 20.000 cadenas con la forma, contra el 1/97 = 1,031% teorico; es exactamente lo
que un mod-97 puede ofrecer y no hay laxitud oculta). El problema no es el checksum: es **lo que se
le entrega para checkear**. Al patron avido se le entrega el identificador pegado a la frase, y el
checksum -- correctamente -- lo rechaza.

## Reproduccion

Motores cargados por `importlib` desde cada clon, sin tocar el arbol de trabajo.

    cd D:/Aegis_Scratch/protocol/analista-0328
    python prose_probe.py        # focos A y B, caso embebido
    python checksum_probe.py     # foco A, discriminacion y escapes
    python ac4_probe.py          # foco C, banda telefonica
    python corpus_diff.py        # foco B, recuento AC3 sobre el corpus gobernado
    python ac5_mutants.py        # foco D, mutantes del checksum

Gates AC6 en el clon limpio sobre `041e788a`:

    python scripts/memory/test_memory_db.py            EXIT=0   (Ran 72 tests in 272.539s, OK)
    python scripts/check_falsification_contracts.py --root .   EXIT=0
    python scripts/validate_collaboration_state.py --root .    EXIT=0
    python scripts/scan_domain_neutrality.py --root .          EXIT=0

## Hallazgo 1 (BLOQUEANTE) -- el identificador embebido en prosa

`contains_pii` evalua **solo el candidato avido** que devuelve `finditer`:

    any(account_identifier_checksum_is_valid(candidate.group(0))
        for candidate in STRUCTURAL_PII_PATTERNS[1].finditer(item))

Como el espacio es separador y `[A-Z0-9]` (con `re.I`) es cuerpo, la palabra siguiente entra en el
candidato. Traza literal de los candidatos devueltos por el patron:

| Cadena | candidato devuelto por el patron | viejo | nuevo |
|---|---|---|---|
| `ES9121000418450200051332` | `ES9121000418450200051332` | True | True |
| `ES91 2100 0418 4502 0005 1332` | `ES91 2100 0418 4502 0005 1332` | False | **True** |
| `cuenta: ES91 2100 0418 4502 0005 1332 del titular` | `ES91 2100 0418 4502 0005 1332 del titular` | False | **False** |
| `cuenta: ES91 2100 0418 4502 0005 1332 del ...` | `ES91 2100 0418 4502 0005 1332 del` | False | **False** |
| `La cuenta ES91 2100 0418 4502 0005 1332 pertenece a Juan` | (ninguno) | False | **False** |
| `transferir a ES9121000418450200051332 hoy` | `ES9121000418450200051332 hoy` | **True** | **False** |
| `transferir a ES9121000418450200051332 manana por favor` | (ninguno) | **True** | **False** |

Las dos ultimas filas son el retroceso: cadenas que el motor **anterior** marcaba y el motor
**nuevo** deja pasar. La causa es la misma en los dos sentidos: el cuerpo avido se come la frase.
Cuando la frase absorbida excede los 30 caracteres de cuerpo, el patron ni siquiera produce
candidato (`matches=[]`), asi que tampoco queda nada que checkear.

Esto no es un caso de laboratorio: la propia tarea lo pone como tercera linea de su bloque
"Evidencia medida (2026-08-07)". El AC2 pide medir "sobre casos de las dos formas"; el test
entregado mide cinco presentaciones **aisladas** y ninguna embebida en texto, que es el caso por
el que existe un detector de PII sobre artefactos escritos a mano.

Falsacion de la propiedad, no de la forma: el arreglo no debe evaluar unicamente el candidato
maximo, sino los prefijos compactos de longitud valida dentro del candidato (compactado de 15 a 34
caracteres), o bien delimitar el cuerpo por una propiedad que las palabras no cumplan. Un segundo
patron no lo arregla: cualquier patron cuyo cuerpo sea `[A-Z0-9]` con espacio como separador tiene
la misma ambiguedad.

## Hallazgo 2 (CONFIRMADO) -- el checksum relaja la deteccion de la forma contigua

El patron anterior marcaba **cualquier** cadena con la silueta, sin checksum. El nuevo exige
mod-97 valido **tambien para la forma contigua**, que antes estaba cubierta incondicionalmente.

Medicion: 5.000 cadenas contiguas con la silueta `[A-Z]{2}\d{2}[A-Z0-9]{16}`, todas marcadas por
el motor viejo. Con el motor nuevo quedan sin marcar **4.944 de 5.000 (98,88%)**.
Casos concretos reproducibles: `OR77WCBWUB6SJ95Y2PSA`, `TA8132CF1TKSCXEIV05T`,
`UI685GKEWI146P6IO410`, `GG07OPQ4CHL5JL0Q78F6`, `AB77BZCSWC8QO7PQD0HJ`.
Ejemplos con significado: `ES9121000418450200051333` (un IBAN con una errata) y
`XX0000000000000000000000` pasan de True a False.

Sobre el corpus gobernado el efecto neto observado es 0 porque el corpus no contiene ninguna
cadena de esa silueta (ver Hallazgo 3), asi que es un hueco **hacia adelante**, no una perdida ya
materializada. Pero el AC3 no dice "sin efecto observado": dice que la guarda debe fallar CERRADO
y **nunca relajar la deteccion**. Un identificador de cuenta nacional que no es IBAN (el mod-97
solo aplica a IBAN) o un IBAN con una errata son PII y ahora escapan. La medicion del AC3 conto
una sola direccion -- cuantas cadenas NUEVAS se marcan -- y no conto cuantas se DEJAN de marcar.

## Hallazgo 3 (AC3 recontado) -- las cifras declaradas se reproducen

Recuento independiente sobre el arbol gobernado en `041e788a`, enumerando la metadata con
`iter_source_paths` + `parse_frontmatter` + `value_list` sobre `ALLOWLIST_KEYS`:

| Magnitud | Declarado por Codex | Recontado por Analista |
|---|---|---|
| Cadenas de metadata elegibles | 22.176 | 22.164 (3.618 unicas) |
| Candidatos estructurales brutos del patron nuevo | 10 | **10** |
| Candidatos aceptados por el checksum | 0 | **0** |
| Cadenas nuevas marcadas | 0 | **0** |
| Falsos positivos nuevos | 0 | **0** |
| Cadenas que dejan de marcarse | (no medido) | **0** |

Los diez candidatos brutos y su rechazo se reproducen exactamente; son cadenas de protocolo del
tipo `GO-1105-infra-fixture`, `AC45-guard-in-review`, `AC12/AC13 permanentes`,
`ed25519-submit-intent.md`, `ws35-instalador.md`. La cifra que autoriza el ensanchamiento
**se sostiene**: 0 falsos positivos nuevos.

La diferencia de 12 en la poblacion elegible (22.164 frente a 22.176) es de enumeracion, no de
veredicto: las magnitudes que cargan el AC3 coinciden al numero. La declaro para que quede
trazada, no como bloqueo.

## Hallazgo 4 (CONFIRMADO) -- la declaracion del AC4 es falsa como enunciado general

La tarea declara: "ni la forma contigua ni la agrupada entra en la banda telefonica de 9 a 15
digitos". Eso es cierto **para el fixture ES91** y falso para otros paises. Medido sobre la
presentacion agrupada en bloques de cuatro:

| IBAN | candidato telefonico | digitos | cae en la banda 9-15 |
|---|---|---|---|
| ES9121000418450200051332 | `91 2100 0418 4502 0005 1332` | 22 | no |
| GB33BUKB20201555555555 | `2020 1555 5555 55` | 14 | **si** |
| NL91ABNA0417164300 | `0417 1643 00` | 10 | **si** |
| BE68539007547034 | `68 5390 0754 7034` | 14 | **si** |
| NO9386011117947 | `93 8601 1117 947` | 13 | **si** |
| DE89370400440532013000 | `89 3704 0044 0532 0130 00` | 20 | no |
| CH9300762011623852957 | 19 digitos | 19 | no |
| PT50000201231234567890154 | 23 digitos | 23 | no |
| IT60X0542811101000000123456 | 22 digitos | 22 | no |
| FR1420041010050500013M02606 | 19 digitos | 19 | no |

Comprobacion directa: con el detector estructural desactivado (patron sustituido por `(?!x)x`),
GB33, NL91, BE68 y NO93 siguen devolviendo True en **las dos** presentaciones, por el heuristico
de telefono. Es decir: 4 de 10 IBAN muestreados tienen cobertura que si depende incidentalmente
del heuristico que TASK-0322 estrecho, que es exactamente lo que el AC4 pedia detectar y declarar.

Esto contamina ademas la frontera del contrato: `(False, False) phone_only_results` esta medida
sobre el unico fixture donde la banda no dispara, asi que el contrato certifica una propiedad que
solo vale para ES91 y se presenta como general.

## Hallazgo 5 (RESIDUAL) -- la clase de separadores es arbitraria

Admite `0x20 0x09 U+00A0 U+2009 U+202F . _ / \ -`. Si se molestaron en incluir el espacio fino y
el fino no separable, la omision de los siguientes es dificil de justificar; todos dan False:

    U+2002 EN SPACE, U+2003 EM SPACE, U+2007 FIGURE SPACE, U+200A HAIR SPACE,
    U+200B ZWSP, U+2010 HYPHEN, U+2011 NON-BREAKING HYPHEN, U+2013 EN DASH,
    U+00B7 MIDDLE DOT, salto de linea

U+2007 (figure space) y U+2010/U+2011 son salida habitual de un PDF o de un procesador de textos,
que es de donde sale un IBAN copiado del banco. Lo declaro como residual, no como bloqueo: el
enunciado del AC2 habla de "agrupacion en bloques con separadores" y las formas dominantes
(espacio, guion ASCII) estan cubiertas. Pero es la misma clase de defecto que la tarea vino a
arreglar -- enumerar una lista de formas -- y conviene que quede escrita antes de cerrar.

## Vectores exigidos por la instruccion

| Vector | Resultado | Evidencia |
|---|---|---|
| A. Checksum acepta formas legitimas (contigua, agrupada, guiones, espacios finos, nbsp, minusculas, mezcla) | **PASA** | 10 IBAN reales x 7 presentaciones; todas True salvo la embebida en prosa (Hallazgo 1) |
| A. Checksum rechaza la forma sin checksum valido | **PASA** | 1,055% de deslizamiento sobre 20.000 cadenas con la forma, contra 1/97 = 1,031% teorico |
| A. El ensanchamiento no es mas ancho de lo declarado | **PASA** | 10 candidatos brutos, 0 aceptados sobre el corpus |
| A. El ensanchamiento no es mas ESTRECHO de lo declarado | **FALLA** | Hallazgos 1 y 2: 2 casos de prosa y 98,88% de la silueta contigua pasan de True a False |
| B. AC3 recontado (0 marcadas, 0 falsos positivos sobre el corpus) | **PASA** | Tabla del Hallazgo 3; cifras reproducidas al numero |
| C. AC4 declara la interaccion con TASK-0322 | **FALLA** | Hallazgo 4: la declaracion generaliza desde un unico fixture; 4/10 IBAN si dependen del heuristico |
| D. Negativo con las DOS formas y mutante de codigo muerto | **PASA** | El mutante `if False else <patron contiguo>` cae: `(True, False)` |
| D. El checksum esta atado por el contrato | **PASA** | Mutantes propios: `checksum -> True` exit 1, `checksum -> False` exit 1; los dos tumban el runner |
| AC6. Gates en clon limpio | **PASA** | Los cuatro exit 0 (ver Reproduccion) |
| Robustez: ReDoS / excepcion en el checksum | **PASA** | 4 cargas patologicas (2.000 separadores, muro alfanumerico, 21k de texto): <=0,014 s, sin excepcion |
| Banda de longitud | **OBSERVACION** | Acepta compactado de 14, un caracter por debajo del minimo IBAN real (15). Sin efecto medido; lo declaro |

## Residuales declarados

- R1. Separadores de presentacion no cubiertos (Hallazgo 5).
- R2. Compactado de longitud 14 admitido, por debajo del minimo real del formato.
- R3. Solo se valida mod-97; los identificadores de cuenta nacionales que no lo usan quedan fuera
  por diseno. Es una consecuencia consciente de atar la deteccion al checksum y merece quedar
  escrita en la tarea, no descubrirse mas adelante.
- R4. El contrato declara tres fronteras; la asercion que realmente ata la discriminacion del
  checksum (`assertFalse(contains_pii(protocol_like))`) no esta entre las declaradas, aunque si se
  ejecuta. El registro declara menos de lo que el test ata.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

Remediacion pedida, por orden:

1. **Hallazgo 1, obligatorio.** Que la deteccion no dependa del corte avido: evaluar los
   compactados de longitud valida contenidos en el candidato, no solo `candidate.group(0)`.
   Criterio de aceptacion por comportamiento, no por forma: las tres lineas de evidencia de la
   propia tarea (contigua, agrupada, **y agrupada embebida en texto corriente**) deben dar True, y
   `"transferir a ES9121000418450200051332 hoy"` debe seguir dando True como daba antes. El
   negativo permanente debe incluir al menos un caso embebido en prosa por cada forma, con
   palabras a izquierda y derecha.
2. **Hallazgo 2, obligatorio: declarar o cerrar.** O bien se conserva la cobertura de la silueta
   contigua sin checksum valido (fallo cerrado), o bien se declara explicitamente en la tarea que
   el checksum estrecha la deteccion respecto del motor anterior, con el numero medido, y se pide
   ratificacion al Arquitecto por ser la direccion que el AC3 prohibe. No vale dejarlo sin
   declarar.
3. **Hallazgo 4, obligatorio.** Corregir la declaracion del AC4: la banda telefonica **si** alcanza
   a algunos identificadores en las dos presentaciones. Medir sobre una muestra multipais y
   declarar cuales dependen del heuristico estrechado por TASK-0322.
4. **Hallazgo 5 y residuales R2-R4:** declarar en la tarea. No bloquean.

Gates afectados por la remediacion: `scripts/memory/test_memory_db.py`,
`scripts/check_falsification_contracts.py --root .`, y los dos gates de estado del repo. Re-juicio
del Analista **antes** del commit de cierre. Maximo **2 iteraciones** de remediacion; si a la
segunda el caso embebido en prosa sigue sin quedar atado por comportamiento, escalo al operador
humano.

-- Analista
