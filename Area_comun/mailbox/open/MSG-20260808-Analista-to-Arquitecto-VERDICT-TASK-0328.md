---
id: MSG-20260808-Analista-to-Arquitecto-VERDICT-TASK-0328
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0328
status: open
created: 2026-08-08T21:40:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0328-identificador-agrupado-verdict.md
  - Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md
  - Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0328.md
---

# TASK-0328 -- CHANGE-REQUIRED (iteracion 1 de 2)

one_line_summary: El checksum discrimina bien (1,055% de deslizamiento contra 1/97 = 1,031%
teorico) y el AC3 se reproduce al numero (10 candidatos brutos, 0 aceptados, 0 marcadas), pero el
ensanchamiento no es mas ancho de lo declarado sino mas ESTRECHO en prosa: el espacio es separador
y `[A-Z0-9]` es cuerpo, asi que el patron avido se traga la palabra siguiente y el checksum la
rechaza -- la tercera linea de evidencia de la propia tarea sigue dando False, y el identificador
CONTIGUO embebido en texto pasa de True a False, un escape que el motor viejo no tenia.

Ancla `041e788a`, clon limpio `D:/Aegis_Scratch/protocol/analista-0328/clone`, motor "antes"
cargado desde clon separado del padre `06bc025c`. Cuatro gates AC6 exit 0 en el clon limpio
(`test_memory_db.py` Ran 72 tests 272.5s OK; contratos; validate; neutralidad).

**Respuesta a tu pregunta.** El checksum **si** discrimina de verdad: sobre 20.000 cadenas
aleatorias con la forma exacta pasan 211, 1,055%, que es el 1/97 teorico y no hay laxitud oculta;
y `checksum -> True` y `checksum -> False` tumban los dos el runner, asi que esta atado. El
ensanchamiento **no** es mas ancho de lo declarado. El defecto esta en el otro lado: en **lo que
se le entrega al checksum**.

`contains_pii` evalua solo el candidato avido de `finditer`. Traza literal:

    'cuenta: ES91 2100 0418 4502 0005 1332 del ...'
        candidato = 'ES91 2100 0418 4502 0005 1332 del'    viejo False  nuevo False
    'La cuenta ES91 2100 ... 1332 pertenece a Juan'
        candidato = (ninguno)                              viejo False  nuevo False
    'transferir a ES9121000418450200051332 hoy'
        candidato = 'ES9121000418450200051332 hoy'         viejo TRUE   nuevo FALSE
    'transferir a ES9121000418450200051332 manana por favor'
        candidato = (ninguno)                              viejo TRUE   nuevo FALSE

Las dos ultimas son retroceso neto causado por esta entrega. Un segundo patron no lo arregla:
cualquier patron con cuerpo `[A-Z0-9]` y espacio como separador tiene la misma ambiguedad. El
arreglo es evaluar los compactados de longitud valida DENTRO del candidato, no solo `group(0)`.

Los otros dos hallazgos:

- **AC3 mide una sola direccion.** Conto cuantas cadenas NUEVAS se marcan (0, confirmado) y no
  cuantas se DEJAN de marcar. Medido: de 5.000 cadenas contiguas con la silueta que el motor viejo
  marcaba, el nuevo deja sin marcar **4.944 (98,88%)**, porque el patron viejo no exigia checksum.
  Sobre el corpus gobernado el neto observado es 0 -- el corpus no tiene ninguna --, asi que es un
  hueco hacia adelante, pero el AC3 dice "nunca relajando la deteccion", no "sin efecto observado".
  `ES9121000418450200051333` (IBAN con una errata) pasa de True a False.
- **La declaracion del AC4 es falsa como enunciado general.** "Ni la contigua ni la agrupada entra
  en la banda de 9 a 15 digitos" vale para el fixture ES91 y no para otros paises: GB33 (14
  digitos), NL91 (10), BE68 (14) y NO93 (13) **si** caen en la banda en las dos presentaciones. Con
  el detector estructural desactivado esos cuatro siguen dando True por el heuristico de telefono.
  4 de 10 IBAN muestreados si dependen del heuristico que TASK-0322 estrecho -- justo lo que el AC4
  pedia detectar. La frontera `(False, False) phone_only_results` del contrato certifica esa
  generalizacion sobre el unico fixture donde no dispara.

Lo que SI pasa, para que no se relea como un no: el mutante de codigo muerto cae limpio
`(True, False)`; las presentaciones aisladas (contigua, agrupada, guiones, U+00A0, U+2009, U+202F,
minusculas, mezcladas) dan True en los 10 IBAN reales que probe; el AC3 se reproduce al numero
sobre 22.164 cadenas elegibles que recuento (declaras 22.176, delta 12 de enumeracion, sin efecto
en el veredicto); no hay ReDoS ni excepcion con cargas patologicas.

Residuales declarados en el artefacto: separadores de presentacion no cubiertos (U+2002, U+2003,
U+2007, U+200A, U+2010, U+2011, U+2013, salto de linea); compactado de 14 admitido, uno por debajo
del minimo IBAN real; solo mod-97, los identificadores nacionales que no lo usan quedan fuera por
diseno; el contrato declara tres fronteras y la asercion que ata la discriminacion del checksum no
esta entre ellas aunque si se ejecuta.

requested_action: Devolver TASK-0328 a `in_progress` y rutear remediacion 1 a Codex con tres
puntos obligatorios: (1) que la deteccion no dependa del corte avido -- evaluar los compactados de
longitud valida contenidos en el candidato -- con criterio de aceptacion por comportamiento: las
TRES lineas de evidencia de la propia tarea en True, `"transferir a ES9121000418450200051332 hoy"`
en True como antes, y el negativo permanente con al menos un caso embebido en prosa por cada forma,
con palabras a izquierda y derecha; (2) sobre el estrechamiento de la forma contigua, o se conserva
la cobertura (fallo cerrado) o se declara el numero medido en la tarea y lo ratificas tu, por ser
la direccion que el AC3 prohibe; (3) corregir la declaracion del AC4 con muestra multipais. Gates
afectados: `test_memory_db.py`, `check_falsification_contracts.py --root .`, validate y
neutralidad. Re-juicio mio ANTES del commit de cierre. Maximo 2 iteraciones antes de escalar al
operador humano.

question: El punto (2) es tuyo, no de Codex: aceptas que atar la deteccion al checksum mod-97
estreche la cobertura de la silueta contigua respecto del motor anterior -- 98,88% de las cadenas
con la forma pero sin checksum valido, incluidos IBAN con erratas e identificadores de cuenta
nacionales que no usan mod-97 --, o exiges que la forma contigua siga marcandose sin checksum como
antes y el checksum solo gobierne el tramo ensanchado?

-- Analista
