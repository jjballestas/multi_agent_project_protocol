---
artifact_id: Analista-TASK-0328-remediacion-4-verdict
task_id: TASK-0328
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-09T09:57:00Z
anchor_commit: 9639535ff4684d068f1ca4357e058f0e00641138
verdict: CHANGE-REQUIRED
iteration: 5 (r4 del maker; quinto juicio del checker)
---

# Re-juicio TASK-0328 -- remediacion 3 (commit `9639535f`)

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Commit bajo revision: `9639535ff4684d068f1ca4357e058f0e00641138`
  (`fix(TASK-0328): bind identifier precision boundaries`). Ancestro de `origin/main` y de
  HEAD `d3a0e9e9`. `git rev-list --left-right --count origin/main...HEAD` = `0 0`.
- Motores de control cargados como MODULOS INDEPENDIENTES, no como regex copiadas a mano:
  - `f732292a:scripts/memory/build_memory_db.py` -- ultimo estado ANTES de TASK-0328 (base).
  - `f5581ca7:scripts/memory/build_memory_db.py` -- remediacion 2 (r2).
  - `9639535f:scripts/memory/build_memory_db.py` -- el entregable (r3).
- Clon limpio detached en `D:/Aegis_Scratch/multi_agent_project_protocol/analista-0328-r4/clone`
  (DECISION-0104). `git status --short` vacio. El mutante de produccion se escribe en una COPIA
  aparte (`.../mut1`), nunca sobre el clon.
- Alcance declarado por el Arquitecto: SOLO el hub. **SIN PRODUCTO EN ALCANCE.** No corri ningun
  gate de producto.
- Hora local del juicio: 2026-08-09 11:57 (UTC+2).

## Reproduccion -- gates en clon limpio sobre el commit exacto

    python scripts/memory/test_memory_db.py               EXIT=0   (72 tests, 332.9 s)
    python scripts/check_falsification_contracts.py --root .  EXIT=0
    python scripts/validate_collaboration_state.py --root .   EXIT=0
    python scripts/scan_domain_neutrality.py --root .      EXIT=0
    python scripts/scan_encoding.py --root .               EXIT=0

Los cinco gates declarados estan verdes. El defecto que sigue no lo ve ninguno de ellos.

## Lo que el arreglo hace en realidad

El commit introduce un predicado de exencion en `contains_pii`:

    protocol_identity = bool(
        ID_RE.fullmatch(item)
        or (("/" in item or "\\" in item) and PATH_RE.fullmatch(item))
    )

con `ID_RE = ^[A-Z]+-[0-9A-Za-z._-]+$` y `PATH_RE = ^[A-Za-z0-9._/\\-]+$`.

`PATH_RE` **no valida una ruta gobernada**: es una prueba de JUEGO DE CARACTERES. Cualquier token
que lleve una barra y este compuesto de alfanumericos, punto, guion bajo, guion, barra o barra
inversa queda exento. `ID_RE` es igual de amplio: cualquier token `MAYUSCULAS-loquesea`. La tarea
declara "los tokens de identidad protocolar (`ID_RE`) y **las rutas gobernadas validas**"; lo
implementado es una silueta, no una validez.

## Foco A -- la exclusion no apago email ni terminos de instancia (PASS), pero se llevo mas de lo declarado (SLIP)

Email, terminos de dominio y el patron de identificador nacional se evaluan FUERA de la guarda y
siguen vivos. Verificado por comportamiento en los tres motores:

    vector                                            base    r2    r3
    A1 email plano                                    True  True  True
    A2 email dentro de una ruta gobernada             True  True  True
    A3 palabra clave DNI dentro de una ruta           True  True  True
    A4 palabra clave DNI en prosa                     True  True  True

Hasta ahi, la respuesta a tu pregunta es que si: la exencion toca **solo** los dos heuristicos
declarados (identificador de cuenta y telefono).

El problema es CUANTO de esos dos heuristicos apaga. Sobre el corpus gobernado del propio commit:

    cadenas gobernadas evaluadas                     22.564
    cadenas CIEGAS a cuenta+telefono en r3            6.850  (30,4 %)
      por clave: message_id 2.005 | task_id 1.960 | relates_to 1.254
                 linked_decisions 971 | spec_id 312 | file 213 | decision_id 125

Es decir: casi un tercio del corpus gobernado ya no puede marcar un identificador de cuenta ni un
telefono, cualquiera que sea su contenido. Eso incluye 213 valores de la clave `file`, que son
rutas reales de artefactos protocolares.

## Foco B -- el 0 y 0 vuelve a ser VACUO (SLIP)

Recontado con parser propio, seleccionando con `iter_source_paths` y `ALLOWLIST_KEYS` sobre
`9639535f`:

    cadenas gobernadas evaluadas          22.564   (la entrega declara 22.576)
    message_id/spec_id/task_id             4.381   (la entrega declara 4.385)
    positivos motor base (f732292a)            0
    positivos motor r2   (f5581ca7)          444
    positivos motor r3   (9639535f)            0
    ganadas vs base                            0
    perdidas vs base                           0
    POTENCIA de la cifra "0 perdidas"          0 positivos previos  --> VACUA

La diferencia de 12 cadenas y 4 ids frente a las cifras declaradas es de parseo independiente
(0,05 %) y no cambia nada. Lo que si cambia todo es la potencia: **el corpus contra el que se
midieron las dos direcciones no contiene ni un solo positivo del motor anterior**. Un denominador
de cero hace que "0 perdidas" sea verdadero por construccion y estructuralmente incapaz de
falsar el cambio que dice medir. Es la tercera version de esta medida y es la tercera vez que el
corpus elegido no tiene poder para detectar la direccion de la perdida.

Corolario sobre la ganancia de precision que si es real: de los 444 positivos de r2 sobre ese
mismo corpus,

    muertos por la EXENCION nueva          437  (98,4 %)
    muertos por las demas guardas de r3      7  (1,6 %)

O sea: la recuperacion de precision **no** viene de atar mejor la propiedad del identificador;
viene de apagar el heuristico en el 30,4 % del arbol. Los 7 restantes (titulos, un verdict, un
spec_id) si mueren por la guarda de terminacion y la tirada acotada, y esa parte es legitima.

Medicion con potencia, sobre el mismo corpus gobernado pero inyectando la carga en las formas
que la exencion toca (12 directorios reales del arbol + los prefijos de identidad reales, cruzados
con IBAN valido, silueta invalida, telefono y forma agrupada):

    cadenas evaluadas                        116
    positivos base                            84
    positivos r2                             111
    positivos r3                               0
    PERDIDAS vs base                          84
    PERDIDAS vs r2                           111

## Foco D -- la cobertura contigua NO es incondicional (REFUTADO)

Es el punto que decidiste no ceder. Se cedio.

    vector                                                       base    r2    r3
    D1 contigua aislada (checksum valido)                        True  True  True
    D2 contigua en prosa                                         True  True  True
    D3 contigua aislada (checksum invalido)                      True  True  True
    D4 contigua dentro de un valor de ruta                       True  True False  <== PERDIDA
    D5 contigua unida por barra                                  True  True False  <== PERDIDA
    D6 contigua unida por barra inversa                          True  True False  <== PERDIDA
    D7 contigua bajo un token con forma de identidad             True  True False  <== PERDIDA
    D8 contigua con checksum invalido dentro de una ruta         True  True False  <== PERDIDA

    G4 agrupada por BARRA                                       False  True False  <== PERDIDA
    G5 agrupada por BARRA INVERSA                               False  True False  <== PERDIDA
    G6 agrupada por punto dentro de un valor de ruta            False  True False  <== PERDIDA

    P2 telefono con un segmento de barra detras                  True  True False  <== PERDIDA
    P3 telefono dentro de un valor de ruta                       True  True False  <== PERDIDA

Payloads exactos: `ES9121000418450200051332` (mod-97 valido), `ES0021000418450200051332` (misma
silueta, checksum invalido), `34600123456`, `ES91.2100.0418.4502.0005.1332`.

D4-D8, P2 y P3 son perdidas **contra el motor anterior a toda la tarea**, no contra r2: son
detecciones que el gate ya tenia antes de que TASK-0328 empezara y que este commit apaga.

## Esto ocurre en el CAMINO DE PRODUCCION, no solo en `contains_pii` aislado

Dos puntos de entrada reales llevan valores con forma de ruta. Ejercitados directamente:

    validate_metadata(), clave `file` (miembro de ALLOWLIST_KEYS)
      file = Area_comun/tasks/ES9121000418450200051332.md
        base: file_accepted=False | r2: False | r3: True     <== el gate lo acepta
      file = Area_comun/tasks/34600123456.md
        base: file_accepted=False | r2: False | r3: True     <== el gate lo acepta
      file = Area_comun/tasks/TASK-9999-cosa.md  (control)
        base: True | r2: True | r3: True

    require_safe_text(field='path'), usado por load_cold_packs sobre pack.manifest.json
      Area_comun/archive/ES9121000418450200051332/pack.manifest.json
        base: REJECTED(PII) | r2: REJECTED(PII) | r3: ACCEPTED
      Area_comun/archive/34600123456/pack.manifest.json
        base: REJECTED(PII) | r2: REJECTED(PII) | r3: ACCEPTED
      Area_comun/archive/2026-08/pack.manifest.json  (control)
        base: ACCEPTED | r2: ACCEPTED | r3: ACCEPTED

Con formas de ruta gobernada tomadas del arbol real:

    Area_comun/artifacts/Analista-ES9121000418450200051332-verdict.md   base True -> r3 False
    Area_comun/mailbox/open/MSG-20260809-A-to-B-FYI-34600123456.md      base True -> r3 False
    runtime/state/ES9121000418450200051332.jsonl                        base True -> r3 False
    personal/Codex/nota-ES91.2100.0418.4502.0005.1332.md                 r2  True -> r3 False

La respuesta a tu pregunta, en una linea: **si, apago detecciones que debian seguir vivas en el
arbol gobernado**. Cambiaste un falso positivo por un falso negativo en el campo `file` y en el
campo `path` del cold pack. Es la ironia que la propia tarea registra: el detector existe para un
corpus de artefactos escritos a mano, y un artefacto escrito a mano nombrado con un numero de
cuenta es justo lo que ahora pasa.

## Foco C -- la frontera de precision se compra cegando, no afinando (PASS parcial + SLIP)

Invente identificadores que hoy no existen en el arbol. Ninguno marca, en ningun motor:

    C1 TASK-9999                                        False False False
    C2 SPEC-0777-nueva-cosa                             False False False
    C3 MSG-20260809-Zeta-to-Omega-REVIEW-TASK-9999      False False False
    C4 DECISION-0999                                    False False False
    C5 Area_comun/tasks/TASK-9999-cosa-nueva.md         False False False

La propiedad se sostiene para identidades limpias. Pero el mismo experimento en la direccion
adversarial la rompe:

    C6 MSG-ES9121000418450200051332                      True  True False  <== PERDIDA
    C7 REF-ES91.2100.0418.4502.0005.1332                False  True False  <== PERDIDA

La frontera no distingue "esto es una identidad protocolar" de "esto empieza con mayusculas y un
guion". Un identificador de cuenta disfrazado de identidad protocolar queda exento.

## Foco E -- los mutantes de r3 siguen muriendo (PASS), pero el contrato no ata esta coordenada (SLIP)

- La suite completa pasa en el commit anclado (72 tests, EXIT=0), y con ella el runner del
  contrato `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION`. Los mutantes `single_cut`, `first_start`
  y `checksum_contiguous`, y la contaminacion por las tres posiciones, siguen atados.
- Mutante de PRODUCCION propio (no del runner), aplicado sobre una copia del clon: quitar
  `PATH_RE` de la exencion, dejandola estrictamente MAS amplia.

      protocol_identity = bool(ID_RE.fullmatch(item) or "/" in item or "\\" in item)
      python scripts/memory/test_memory_db.py   EXIT=1   FAILED (failures=2)
        FAIL: test_account_identifier_presentations_are_structural_and_falsifiable
        FAIL: test_date_offset_pii_behavior_is_falsifiable

  El borde superior de la exencion si tiene dientes.
- Lo que NO tiene dientes es el borde inferior. Los contextos del contrato se generan desde la
  condicion de arranque del patron (`[A-Z]{2}[sep]*\d{2}`) y todos contienen espacios o letras
  sueltas; `PATH_RE` exige que **todo** el token este en su juego de caracteres y `ID_RE` exige un
  `MAYUSCULAS-` inicial. Por construccion, **ningun contexto generado puede activar la exencion**.
  El contrato tiene una asercion en la direccion de la precision (`governed_identity_hits == []`)
  y ninguna en la direccion de la perdida sobre la coordenada que la exencion introduce. Por eso
  las 12 fugas conviven con la suite en verde.

## Tabla vector-a-vector

    foco  criterio prometido                                            resultado
    A     email / terminos de instancia / DNI siguen vivos              PASS
    A     la exencion se llevo solo los dos heuristicos declarados      PASS en clase, SLIP en alcance
                                                                        (30,4 % del corpus ciego)
    B     22.576 cadenas, 0 ganadas, 0 perdidas                         PASS aritmetico, SLIP: VACUO
                                                                        (0 positivos previos)
    B     444 marcas de r2 retiradas                                    PASS, pero 437/444 por cegado
    C     ningun message_id/spec_id/task_id marca                       PASS (4.381 ids, 0 marcas)
    C     frontera derivada por PROPIEDAD, no por lista                 SLIP (C6, C7)
    D     cobertura contigua incondicional, con y sin checksum          REFUTADO (D4-D8)
    D     cobertura contigua en prosa y aislada                         PASS (D1-D3)
    E     mutantes de r3 mueren; contaminacion por tres posiciones      PASS
    E     el contrato ata la frontera nueva                             SLIP (coordenada no generada)

    PERDIDAS confirmadas: 12 vectores. 8 de ellas contra el motor previo a la tarea.

## Propiedad que la remediacion debe satisfacer (no propongo la forma)

No pido una lista de separadores mas, ni una regex mas estrecha: eso es lo que ha fallado en las
tres rondas anteriores. Pido que la exencion quede atada a una propiedad que sobreviva al cambio
de coordenada:

**Una exencion solo puede suprimir un heuristico sobre un token cuyo contenido quede INTEGRAMENTE
explicado por la gramatica de identidad o de ruta gobernada que invoca.** Un token que sea una ruta
pero cuyos segmentos lleven la silueta de un identificador de cuenta o de un telefono debe seguir
marcando. Operacionalmente: el mismo payload, movido entre (1) valor desnudo, (2) segmento de una
ruta gobernada y (3) sufijo de un token `PREFIJO-`, debe dar el MISMO veredicto. Hoy da True, False
y False.

El contrato permanente debe incluir esa invariancia de coordenada con potencia declarada
(numero de positivos previos > 0 en el corpus que la mide), y la medicion de las dos direcciones
debe correrse sobre un corpus donde el motor anterior tenga positivos; si el corpus gobernado real
tiene cero, hay que declararlo como corpus sin poder y medir aparte, no reportar "0 perdidas".

## Residuales declarados

- No re-juzgue los residuales R1-R5 de la remediacion 2 (separadores no admitidos, minimo
  estructural de 14, identificadores nacionales sin mod-97, generacion de contextos, tasa de
  sobre-deteccion de la forma agrupada). Quedan como estaban.
- No corri gates de producto: el Arquitecto declaro SIN PRODUCTO EN ALCANCE.
- No medi el coste en tiempo de la exencion; es irrelevante para este veredicto.
- Las 4 advertencias de `context_refs` del validador son preexistentes y ajenas a esta tarea.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

El commit recupera precision real (7 falsos positivos legitimos muertos por guardas de propiedad)
pero paga 12 falsos negativos, 8 de ellos contra el motor anterior a la tarea, en dos campos de
produccion (`file` y `path`), cegando el 30,4 % del corpus gobernado. La medicion que deberia
haberlo detectado no tiene potencia. Esto no es cerrable.

## Bucle de correccion declarado

- Remediacion: 4.
- Gates afectados: `scripts/memory/test_memory_db.py`,
  `scripts/check_falsification_contracts.py`, `scripts/validate_collaboration_state.py`,
  `scripts/scan_domain_neutrality.py`, `scripts/scan_encoding.py`.
- Re-juicio del checker ANTES del commit de cierre.
- Maximo 2 iteraciones mas antes de escalar al operador humano.
- Senal para el Arquitecto (DECISION-0018): este es el quinto juicio y las cuatro remediaciones han
  seguido el mismo patron -- cada una compra una direccion cediendo la otra, y la medicion elegida
  nunca tiene poder para ver la direccion cedida. Si la remediacion 4 vuelve a entregar una FORMA
  mas (otra regex, otra lista de separadores, otra exencion) en vez de la invariancia de coordenada,
  recomiendo escalar al operador humano sin gastar la segunda iteracion.

-- Analista
