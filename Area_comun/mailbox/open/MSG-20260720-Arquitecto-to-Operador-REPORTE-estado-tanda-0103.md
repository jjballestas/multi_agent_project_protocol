---
message_id: MSG-20260720-Arquitecto-to-Operador-REPORTE-estado-tanda-0103
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: true
response_owner: Operador
requested_action: "Leer el estado de la tanda DECISION-0103 a media tarde del 2026-07-20: lo logrado, los tres problemas abiertos (uno de ellos nuevo, un agujero de trazabilidad en el indice) y lo que falta. Decidir sobre el unico punto que sigue en tu mesa, el GO del build-open del N=6, y sobre la reparacion de TASK-0267 que propongo al final."
question: "Autorizas la reparacion del agujero de trazabilidad de TASK-0267 por la via gobernada (re-alta de la fila en el archivo desde el propio event log), y mantienes retenido el GO del build-open N=6 o lo das?"
created_at: 2026-07-20
context_refs:
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter1-veredicto.md
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
  - Area_comun/tasks/TASK-0275-rollback-cuarentena-untracked.md
one_line_summary: "Tanda 0103 a 16:20 del 20-jul: 8 unidades done, 1 en juicio final, 10 en cola; tres problemas abiertos (0272 en su ultima iteracion, gate de drift vacuo, y un agujero de trazabilidad NUEVO, TASK-0267 desaparecio del indice y del archivo)."
---

# REPORTE - estado de la tanda DECISION-0103

Hora local: 2026-07-20 16:20. HEAD 6ebf591. Fondo intocable intacto (config
2E35F26E...354, epoch 1.14.0, dataset N=500, reservadas N=6 sin tocar).

## 1. LO LOGRADO

**Ocho unidades cerradas (done)** de las diecinueve que hoy componen la tanda:

- **TASK-0257** el harness armado (core.hooksPath -> .githooks, pre-commit invocando el
  validador). Es la clausula C5 y la razon de que el resto de esta lista sea verificable.
- **TASK-0258** el bloque `obstacles[]` en el esquema de turno. Es la clausula C3, el
  vocabulario con el que un agente cuenta contra que se peleo.
- **TASK-0267** el hook v2 con materializacion del indice, que cerro el falso verde del
  juicio sobre arbol sucio.
- **TASK-0268 y TASK-0269** el reparto de coste del hook (E6). Acotado local por defecto,
  completo bajo flag, CI como frontera dura, mas la materializacion parcial.
- **TASK-0270** endurecimiento del ledger, verificacion post-write y coherencia de
  idempotencia contra estado. Nacio de una perdida de evento real y ya cazo en produccion
  una transaccion parcial.
- **TASK-0271** migracion del checker a proveedor diverso (Anthropic), que es lo que
  sostiene la diversidad maker/checker de la DECISION-0101.
- **TASK-0273** el deadlock poda-contra-claim. Ademas del desbloqueo, la poda no-op bajo
  de 87 segundos a 0.29.

**La enmienda E6 quedo resuelta por el criterio ex-ante que sellaste antes de conocer la
cifra.** La medicion dio 70.7 s en caliente con piso de 43 s, muy por encima del umbral de
15 s, asi que E6-A queda permanente y el hibrido no se autoriza. Dato que merece quedar:
materializar costaba solo 1.9 s, el coste nunca estuvo donde lo suponiamos.

**El gate hizo su trabajo tres veces**, y esa es la evidencia mas valiosa del dia:

1. En 0257 el checker rompio la primera version y forzo tres iteraciones.
2. En 0272 le pedi que intentara romper la cura por dos vias, lo consiguio por las dos y
   encontro tres mas, todas con una sola causa raiz.
3. En la iteracion 1 de 0272 encontro el fallo que ningun test del maker podia ver, la
   evidencia de autoria propia se apoyaba en el autor de git y este arbol commitea todo
   bajo dos autores. Su sandbox usaba autores distintos, el despliegue real no.

**Codex se nego a commitear una vez, correctamente**, porque hacerlo habria absorbido
rutas ajenas mias sin commitear. La negativa era la conducta debida; el error era mio.

## 2. LO QUE TIENE PROBLEMAS

**(a) TASK-0272 esta en su ULTIMA iteracion permitida.** El seen-burn silencioso es el
peor modo de fallo que vimos en la tanda, un mensaje se quema sin que nadie reintente y la
quietud resultante es indistinguible de una pausa normal. La iteracion 2 acaba de
entregarse (commit 02cee08) moviendo la atribucion al canal firmado del ledger. Esta en
juicio del checker ahora mismo. Si encuentra fallo nuevo, el tope obliga a subirtelo en
vez de dar una tercera vuelta.

Residual declarado y consciente, no defecto: la combinacion {token ausente + exit 0} cae
al reconocimiento por texto libre. Es la frontera que decidi y esta dimensionada.

**(b) El gate de drift que citabamos los tres era VACUO.** `runtime/protocol_replay.py
--check-drift` no tiene entrypoint CLI, importa el modulo y sale 0 con cualquier
argumento; verificado con `--bogus-flag`. Aparecia como evidencia en handoffs, veredictos
y cuerpos de commit. El fondo esta bien, la deriva real es cero, pero la forma era una
falsa garantia. Lo levanto el checker retractandose de su propio veredicto anterior, que
citaba el mismo comando. Registrado como **TASK-0274**. Mientras no cierre, la deriva se
afirma corriendo la funcion y citando el `up_to_seq`.

**(c) NUEVO, detectado al preparar este reporte, agujero de trazabilidad: TASK-0267
desaparecio del indice Y del archivo.** Fue podada del indice caliente el 20-jul a las
03:13 (evento seq 5093) pero su fila NO esta en `TASK_INDEX_ARCHIVE.json`, mientras que
las podas posteriores (0270/0271 en 5152, 0257/0268 en 5214) si aterrizaron. Hoy la unidad
existe como fichero en `Area_comun/tasks/`, tiene claims en el archivo de claims y toda su
historia intacta en el event log, pero no tiene fila en ningun indice. Es recuperable, no
hay perdida de informacion en el ledger, pero es exactamente la clase de hueco que esta
tanda existe para eliminar.

Dos cosas que este hallazgo revela y que valen mas que el caso concreto: **el chequeo de
deriva no cubre los archivos de poda**, y **el validador no cruza los ficheros de
`Area_comun/tasks/` contra las filas del indice**, asi que una unidad puede evaporarse del
indice con todos los gates en verde. La causa mas probable es la misma que me costo la
manana, el `TASK_INDEX_ARCHIVE.json` quedandose sin commitear y siendo revertido por una
operacion posterior sobre el arbol compartido.

**(d) Friccion operativa, ya cerrada pero con coste.** Seis abortos de peers en un dia,
todos con negativa correcta del peer, causados por mis propias escrituras en el arbol
compartido mientras ellos sondeaban. Lo corte con silencio de escritura tras rutear, con
staging por lista explicita y con higiene solo en checkpoint coordinado. Hoy volvio a
morderme una vez, en el bloqueo de Codex que cito arriba.

## 3. LO QUE FALTA

**Diez unidades en cola**, ninguna arrancada:

- **0259** validacion condicional de `obstacles` en el validador de turno.
- **0260** vista de plan del conjunto, que es la clausula C1, poder ver el plan ANTES de
  que arranque.
- **0261** el validador de mailbox exigiendo `obstacles` mas contador de friccion.
- **0262** plantillas de mailbox con el REPORTE de entrega y el bloque de obstaculos.
- **0263** mecanismo de oferta de mejora (C3-bis), que ofrece y nunca crea.
- **0264** la regla de arranque documentada, ningun conjunto arranca sin plan aprobado.
- **0266** propagacion del harness a instancias nuevas (E4/E5).
- **0265** el gate final, revision adversarial del conjunto 0257..0264 por el checker.
- **0274 y 0275**, las dos nacidas del ultimo juicio, retenidas hasta que 0272 cierre.

**Lo que esta en tu mesa (unico):** el **GO del build-open del N=6**. Te respondi que es
adelantable con evidencia verificada en el arbol de NOVA, corpus E2 entregado el 14-jul
(commit 35a1b4e, 35 unidades) y BR-C4 en done (TASK-9392 con GO del checker). No hay
previos vivos. El riesgo que te senale sigue vigente, si lo das, hay que **congelar la
propagacion de TASK-0266 hacia NOVA hasta despues de la medicion**, para no cambiar el
entorno sellado a mitad de ventana preregistrada.

**Lo que propongo hacer yo a continuacion, salvo que digas lo contrario:** registrar la
reparacion del agujero de 0267 como unidad propia (re-alta de la fila en el archivo
reconstruida desde el event log, mas el cruce ficheros-contra-indice en el validador para
que la clase no se repita), y mantener la cola parada hasta que el checker cierre 0272.

## 4. LINEA PARALELA

El diseno del grafo sobre memoria hibrida sigue en pausa por dependencia, no por fallo. El
checker fijo N=78 y exige el manifiesto de consultas con SHA-256, y eso depende de
reconstruir el store, que espera al cierre de esta tanda.
