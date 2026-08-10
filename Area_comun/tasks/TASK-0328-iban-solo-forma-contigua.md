---
task_id: TASK-0328
file: Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md
title: "El patron estructural de IBAN solo casa la forma contigua: la agrupacion en bloques de cuatro con que se escribe realmente escapa al patron Y a la banda del heuristico de telefono"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0314
  - TASK-0322
  - TASK-0327
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    `STRUCTURAL_PII_PATTERNS[1]` es `\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b`: exige la forma CONTIGUA.
    Un IBAN escrito como lo escriben las personas -- agrupado en bloques de cuatro, que es la
    presentacion estandar -- no casa. Y tampoco lo rescata el heuristico de telefono: ese captura
    la cadena de digitos y espacios pero luego exige entre 9 y 15 digitos, y un IBAN tiene entre
    15 y 34, asi que cae fuera de la banda por arriba.
    Medido: la forma contigua da True; la agrupada da False, tambien embebida en texto corriente.
    El residual se registro en el ledger del port de TASK-0314 como "R2 IBAN solo en forma
    contigua" y no llego a adjudicarse a ninguna tarea.
  acceptance:
    - "AC1 (falsacion previa): se demuestra sobre el motor real que la forma agrupada devuelve False y que no la rescata ninguna otra guarda, incluido el heuristico de telefono. Se declara por que la banda de 9-15 digitos no la alcanza."
    - "AC2 (deteccion de la forma real): el patron pasa a cubrir la agrupacion en bloques con separadores, manteniendo el rango de longitud valido del formato. La deteccion se mide sobre casos de las dos formas."
    - "AC3 (direccion del fallo, con presupuesto declarado): ensanchar un patron de PII sube el riesgo de falso positivo. Se mide la poblacion de cadenas del corpus que pasan a marcarse y se declara el numero; si aparece un falso positivo, se acota con una guarda que falle CERRADO, nunca relajando la deteccion."
    - "AC4 (interaccion con TASK-0322 declarada): 0322 estrecha las bandas del heuristico. Se verifica y se DECLARA si alguna cobertura de esta tarea dependia incidentalmente de ese heuristico, para que el estrechamiento no abra un hueco por la puerta de atras."
    - "AC5 (contrato): negativo permanente con las dos formas del identificador, declarado en el registro y cableado en CI, verificado por MUTACION que cae al revertir el patron."
    - "AC6 (sin regresion): test_memory_db.py, gates del repo y contratos de falsacion exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca el paso de terminos de dominio a los call sites (eso es TASK-0327), ni la exencion
    de fecha (0325), ni las bandas del heuristico de telefono (0322). El patron sigue siendo
    ESTRUCTURAL y neutral: cubre la forma de un identificador de cuenta, sin terminos de negocio.
  risk: medium
  estimate: S
---

# TASK-0328 -- el IBAN solo se detecta si esta escrito de corrido

## Evidencia medida (2026-08-07)

    contains_pii("ES9121000418450200051332")                        -> True
    contains_pii("ES91 2100 0418 4502 0005 1332")                   -> False
    contains_pii("cuenta: ES91 2100 0418 4502 0005 1332 del ...")   -> False

## Por que no lo rescata el heuristico de telefono

`PHONE_CANDIDATE_RE` si captura la cadena de digitos y espacios, pero el filtro posterior exige
`9 <= digitos <= 15`. Un IBAN tiene entre 15 y 34 digitos segun el pais; el del ejemplo tiene 22.
Se sale de la banda por arriba, asi que el candidato se descarta. La guarda existe, mira el valor
correcto y lo deja pasar.

## La ironia que conviene registrar

La forma que el patron SI detecta -- todo de corrido -- es la que produce una maquina. La que NO
detecta es la que produce una persona copiando de su banco, que es exactamente el caso por el que
existe un detector de PII en un corpus de artefactos escritos a mano.

## Riesgo declarado (medium)

Ensanchar un patron con separadores puede empezar a casar cadenas que no son cuentas
(referencias con prefijo de dos letras y bloques numericos). El AC3 obliga a medir la
poblacion afectada y a declarar el numero antes de dar la tarea por cerrada, en vez de
descubrirlo como ruido en produccion.

## Implementacion y medicion de Codex (2026-08-08)

- La deteccion ahora liga la propiedad estructural: prefijo ASCII de dos letras, dos
  digitos de control y cuerpo alfanumerico de 10 a 30 caracteres. Los separadores
  horizontales admitidos pueden aparecer con agrupaciones arbitrarias y mezclarse:
  espacio, tabulador, espacio no separable, espacio fino, espacio fino no separable,
  punto, guion, barra y barra inversa.
- La guarda de checksum sobre el identificador compactado evita aceptar referencias
  ordinarias que solo tienen la misma silueta. Ante un candidato estructural, solo un
  checksum valido abre la deteccion; la evaluacion no degrada silenciosamente a otra
  heuristica.
- AC3 medido sobre las 22,176 cadenas de metadata elegibles del corpus gobernado en
  HEAD: el patron ampliado produjo 10 candidatos nuevos brutos; la guarda rechazo los
  10; cadenas nuevas marcadas: 0; falsos positivos nuevos observados: 0.
- AC4 medido: ni la forma contigua ni la agrupada entra en la banda telefonica de
  9 a 15 digitos. Con el detector estructural desactivado, ambas devuelven False. La
  cobertura de esta tarea no depende del heuristico estrechado por TASK-0322.
- AC5 queda en `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION`. El mutante conserva el
  nuevo patron en una rama inalcanzable y restaura como rama viva el patron contiguo:
  la forma contigua sigue dando True y la agrupada cae a False.

## Remediacion 1: limite de avidez y delta bidireccional (2026-08-08)

- El candidato amplio ya no decide por su coincidencia completa. La guarda examina
  prefijos de longitud valida y solo acepta un prefijo con checksum correcto que
  termine ante un separador permitido o el final real de la cadena. Asi, el texto
  posterior puede estar dentro del candidato avido sin contaminar el identificador.
- La expresion conserva el maximo estructural de 34 caracteres compactados. Si el
  candidato termina porque alcanzo ese maximo, la guarda tambien mira el caracter
  siguiente del texto original y rechaza una continuacion alfanumerica sin separar.
- Comparacion bidireccional sobre el mismo corpus gobernado de metadata de HEAD,
  seleccionado con `iter_source_paths` y las claves de `ALLOWLIST_KEYS`: 22,342
  cadenas evaluadas por ambos motores; ganadas: 0; perdidas: 0.
- Corpus permanente de seis fronteras: ganadas frente al motor anterior: 2 (forma
  agrupada aislada y agrupada embebida); perdidas: 1. La unica perdida es una forma
  contigua extendida con `A` cuyo checksum es invalido; se conserva como rechazo
  deliberado. Todos los positivos validos del motor anterior permanecen detectados.
- El mutante permanente sustituye la validacion por prefijo por el checksum de la
  coincidencia completa: las formas aisladas siguen pasando, pero la forma contigua
  embebida vuelve a escapar. El contrato liga directamente la regresion observada.

## Remediacion 2: invariancia de contexto y cobertura monotona (2026-08-09)

- La silueta contigua vuelve a ser cobertura estructural incondicional. El checksum no
  puede quitar una deteccion que el motor anterior ya hacia: se usa solo para ensanchar
  la cobertura hacia presentaciones con separadores. Una silueta contigua se marca aunque
  su checksum sea invalido, porque puede ser un identificador real mal tecleado, truncado
  o parcialmente enmascarado y el gate de PII falla hacia marcar de mas.
- La deteccion agrupada ya no depende del primer candidato avido. El motor enumera cada
  posicion que satisface el arranque estructural y, desde cada una, evalua todos los
  prefijos de longitud admitida. Esto hace visible el identificador tanto con contaminacion
  a la izquierda como a la derecha, incluso si la prosa queda pegada sin separador.
- Medicion bidireccional con potencia: 10.800 cadenas, construidas con 300 identificadores
  de checksum valido y 300 siluetas de checksum invalido, cada uno en forma contigua y
  agrupada, cruzados con nueve contextos. Seis contextos se generan desde la propia
  condicion de arranque `[A-Z]{2}[sep]*\d{2}`. El motor anterior tiene 5.400 positivos;
  el reparado tiene 8.660. Ganadas: 3.260. Perdidas: 0. La cifra de perdidas ya no es
  vacua porque el denominador contiene 5.400 positivos anteriores.
- El contrato `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` mata tres regresiones por
  comportamiento: volver a un unico corte del candidato rompe la invariancia por la
  derecha; mirar solo el primer arranque la rompe al mover el identificador dentro de la
  frase; volver a exigir checksum a la silueta contigua pierde 2.140 positivos anteriores
  en la poblacion con potencia.
- AC4 corregido: en una muestra de diez identificadores multipais, GB33, NL91, BE68 y
  NO93 (4/10) caen incidentalmente dentro de la banda telefonica de 9 a 15 digitos, tanto
  contiguos como agrupados. Por tanto, la afirmacion anterior de dependencia cero era
  falsa. La cobertura de esta remediacion no depende de esa heuristica: las dos ramas
  estructurales se evaluan antes y de manera independiente.
- Laxitud declarada: al validar varios prefijos, la tasa medida por el checker sube de
  1,050 % con una forma contigua aislada a 3,140 % con una agrupada aislada y 4,990 % con
  una agrupada en prosa. Es la direccion fail-closed aceptada por AC3; el coste medido por
  el checker fue +3,9 % sobre el corpus gobernado y 14,3 ms en su peor carga de 20 kB.
- Residuales no bloqueantes ratificados como limites de esta tarea: R1, no se admiten los
  separadores U+2002, U+2003, U+2007, U+200A, U+200B, U+2010, U+2011, U+2013, U+00B7 ni
  salto de linea; R2, el minimo estructural sigue en 14 caracteres compactados; R3, los
  identificadores nacionales sin mod-97 solo quedan cubiertos si presentan la silueta
  contigua; R4, la medicion deja de ser una lista manual y genera contextos desde la
  condicion del patron; R5, la presentacion agrupada conserva la mayor tasa de
  sobre-deteccion ya cuantificada.

## Remediacion 3: terminacion, tirada acotada y frontera de precision (2026-08-09)

- La validacion de prefijos agrupados vuelve a exigir que el corte termine ante un
  separador admitido o al final real del candidato. El caracter siguiente al limite de
  34 caracteres compactados tambien participa, por lo que alcanzar el maximo no oculta
  una continuacion alfanumerica.
- La silueta contigua se evalua contra la tirada alfanumerica maximal que la contiene.
  Solo se acepta cuando esa tirada completa mide como maximo 34 caracteres. La cobertura
  contigua previa se conserva para valores completos de 14 a 34 caracteres, incluido un
  caracter adicional que aun queda dentro del maximo; una silueta interna en un objeto de
  40 o 64 caracteres no abre esta rama.
- Los tokens de identidad protocolar (`ID_RE`) y las rutas gobernadas validas se excluyen
  solo de las heuristicas de identificador de cuenta y telefono; email, terminos de
  instancia y sus validadores de forma siguen activos. Ademas, `git_ref` reconoce por
  propiedad los identificadores hexadecimales completos de 40 o 64 caracteres y no los
  somete al clasificador de PII; el resto de referencias conserva el gate.
- AC3 bidireccional contra el motor real anterior `f732292a`, con el selector productivo
  `iter_source_paths` y todas las claves de `ALLOWLIST_KEYS`: 22.576 cadenas gobernadas,
  marcas nuevas: 0, marcas perdidas: 0. El motor anterior y el actual marcaron 0 valores
  en esta medicion estructural sin terminos de instancia. Ninguno de los 4.385 valores
  `message_id`, `spec_id` o `task_id` del mismo arbol marco.
- El contrato permanente ata las dos direcciones. Quitar la guarda de terminacion produce
  nuevas marcas sobre el corpus gobernado; las identidades se derivan del arbol, no de un
  ejemplo; y los objetos git se derivan de `git rev-list --all`. Tambien conserva los tres
  mutantes de cobertura de la remediacion anterior.

## Remediacion 4: invariancia por coordenada y potencia de perdida (2026-08-09)

- La gramatica exenta ya no se infiere del juego de caracteres del valor. El llamador entrega
  la coordenada validada (`task_id`, relaciones, `file` o `path`) y el detector elimina solo la
  envoltura protocolar explicada por esa coordenada. El mismo payload conserva el veredicto al
  estar desnudo, en un segmento de ruta o como sufijo de una identidad.
- Las fechas y horas propias de identidades se neutralizan solo dentro de esas coordenadas; las
  detecciones estructurales incrustadas conservan fronteras alfanumericas. Los caminos reales
  `validate_metadata(file=...)` y `require_safe_text(field=path)` vuelven a rechazar identificadores
  de cuenta y telefonos incrustados, mientras rutas e identidades limpias siguen admitidas.
- Medicion bidireccional del corpus gobernado real contra el motor previo `f732292a`: 22.608
  cadenas, 0 positivos previos, 0 actuales, 0 ganancias y 0 perdidas. Se declara SIN PODER para
  la direccion de perdida porque el denominador previo es cero.
- Medicion separada con potencia sobre 16 valores que cruzan cuatro payloads con las coordenadas
  desnuda, `file`, `path` y `message_id`: 11 positivos previos, 16 actuales, 5 ganancias y 0
  perdidas. Un mutante que ciega por completo las coordenadas exentas pierde 12 detecciones.
- El contrato permanente deriva todas las identidades gobernadas y cubre las dos direcciones:
  ninguna identidad limpia marca, todos los payloads sensibles conservan su deteccion al cambiar
  de coordenada y el mutante de cegado debe perder positivos. Los mutantes anteriores permanecen.

## Remediacion 5: envoltura integral y corpus derivado (2026-08-09)

- La exencion ya no elimina un prefijo generico ni neutraliza fechas sobre el valor completo. Un
  parser acotado consume solo envolturas integrales de identidades, mensajes y rutas; el slug o
  segmento no explicado vuelve al detector sin atenuacion. Las fechas solo quedan fuera cuando
  forman parte completa de una identidad operacional reconocida.
- El salto por adyacencia deja de depender de la coordenada. Telefonos con letra a izquierda o
  derecha, cuentas agrupadas pegadas por la izquierda y cuentas con un bloque de ocho digitos que
  empieza por 19/20 conservan el mismo veredicto desnudas, en `file`, en `path` y como sufijo de
  identidad. Los caminos productivos `validate_metadata(file=...)` y
  `require_safe_text(field='path')` se ejercitan directamente sobre 85 payloads validos de ruta.
- El corpus permanente ya no enumera cuatro payloads. Deriva diez separadores desde la expresion
  productiva, 23 longitudes de bloque desde los limites productivos y ambas direcciones de
  adyacencia desde `isalnum`. La poblacion resultante contiene 260 payloads y 940 valores por
  coordenada: 244 positivos del motor anterior, 940 actuales, 696 ganancias y 0 perdidas.
- Tres mutantes independientes deben perder detecciones: cegado total de coordenada, restauracion
  del salto por adyacencia y restauracion conjunta de neutralizacion de fecha mas salto. El
  inventario declara ahora 18 fronteras para
  `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION`; los 70 contratos permanecen registrados.

## Remediacion 6: criterio previo a la exencion y envolturas derivadas (2026-08-10)

- La deteccion de candidatos con checksum valido ocurre sobre el valor integral antes de que la
  coordenada retire su envoltura. La exencion ya no puede borrar una cuenta contigua completa ni
  triturar una presentacion agrupada antes de que el detector la vea. El remanente no explicado
  se conserva como una unidad; solo un remanente vacio o una referencia protocolar integral queda
  exento.
- La guarda de contexto conserva cero hallazgos sobre las identidades gobernadas limpias. En una
  coordenada, una coincidencia que empieza dentro de otro token solo se admite si conserva el
  arranque estructural contiguo y al menos ocho digitos; esto mantiene las ganancias con
  adyacencia de datos densos sin restaurar los falsos positivos `SG-2026...` y `SK-02...` que
  motivaron la exencion.
- El corpus nuevo no enumera envolturas. Descubre las coordenadas reales del arbol gobernado para
  las que `pii_values_for_coordinate` consume una envoltura, selecciona ejemplos por tipo, deriva
  los puntos de insercion de sus separadores y cruza el payload antes, dentro y despues con las
  presentaciones contigua, agrupada y mixta derivadas de las expresiones productivas.
- Saldo emitido por el propio test: `population=231 previous_positive=64 current_positive=231
  gained=167 lost=0 coordinates=9 orders=3 formats=2`. Los dos caminos productivos siguen
  ejercitados: `validate_metadata(file=...)` rechaza los ficheros validos del corpus y
  `require_safe_text(field='path')` lanza el rechazo esperado.
- El mutante de produccion elimina la guarda previa a la exencion y pierde las 231 detecciones del
  corpus derivado. Los mutantes historicos de cegado de coordenada, adyacencia y fecha siguen
  muriendo sobre el corpus previo con positivos anteriores no nulos.

## Remediacion 7: silueta contigua integral y corpus no circular (2026-08-10)

- La guarda previa a la exencion evalua sobre el mismo valor integral tanto la silueta contigua
  incondicional como la presentacion agrupada con checksum. Una coordenada ya no puede consumir
  una silueta contigua con checksum invalido antes de que el detector estructural la vea.
- El corpus derivado deja de admitir casos mediante `account_identifier_grouped_is_detected`, que
  era la guarda bajo prueba. La admision ahora depende solo de que la presentacion construida no
  sobreviva en los remanentes del parser de coordenada; cruza 12 siluetas contiguas invalidas con
  las presentaciones validas, las nueve coordenadas descubiertas y los tres ordenes.
- Saldo emitido por el contrato: `population=1001 previous_positive=832 current_positive=1001
  gained=169 lost=0 coordinates=9 orders=3 formats=3`. Los formatos son contiguo valido,
  agrupado valido y contiguo con checksum invalido.
- El precio medido sobre las 22.990 cadenas gobernadas actuales es cero marcas nuevas. El mutante
  que retira solo la rama contigua de la guarda integral pierde detecciones del corpus derivado y
  conserva cero divergencias sobre el corpus gobernado real; el mutante historico que vuelve a
  exigir checksum a la rama contigua tambien muere.
