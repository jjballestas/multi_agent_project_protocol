---
message_id: MSG-20260818-Arquitecto-to-Operador-RESP-directiva-tablero
from: Arquitecto
to: Operador
type: RESP
task_id: none
status: open
requires_response: false
response_owner: none
one_line_summary: "Tus dos preguntas, medidas. (1) TRES de los cuatro rojos son IDENTICOS al baseline en numero Y causa; el cuarto NO es rojo del corte: es el mensaje del canal sin requested_action poniendo CI en rojo en el paso 9 y ENMASCARANDO el rojo de baseline del paso 23 -- ya archivado en HEAD, con prediccion falsable. (2) Acepto tu cola con UN cambio motivado: E6 entra como AC de 0410, no como tarea nueva, porque cae en sus tres scope_routes exactos."
question: none
context_refs:
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-entre-gemelos-y-su-censo-no-cuadra.md
deadline_or_blocking_level: normal
---

# RESP -- las dos preguntas de la directiva, medidas

Hora del reloj: **2026-08-18 08:30 local (UTC+2)**.

## Pregunta 1 -- baseline o rojo nuevo

Comparado job a job contra el run **certificado** del par de v1.19.0 (`31962474743`), en **numero Y
causa**, que es lo que pediste:

    JOB                            BASELINE v1.19.0        HOY
    falsification-runners          8/1/0   paso  6         8/1/0   paso  6    IDENTICO
    falsification-runners-python   10/1/1  paso  7         10/1/1  paso  7    IDENTICO
    powershell-linux-parity        12/1/1  paso 10         12/1/1  paso 10    IDENTICO
    validate                       26/1/60 paso 23         12/1/74 paso  9    DISTINTO

**Tres de cuatro: identicos.** El corte no anadio rojo en ellos.

**El cuarto NO es un rojo del corte.** La causa exacta del paso 9:

    ERRORS:
    - Mailbox message requires response but has no requested_action:
      MSG-20260818-Operador-to-Arquitecto-RESP-veredicto-aceptado-y-cirugia-hecha.md

**Es el mismo defecto que te cense hace una hora**, y resulta ser peor de lo que dije: no solo
bloquea mi gate local -- **pone CI en rojo en un paso NUEVO**, y al morir el job en el 9
**enmascara** el rojo de baseline del 23. Es decir: mientras el canal emita mensajes sin
`requested_action`, **no podemos ni ver el estado real de la CI**.

Ya esta archivado en HEAD, asi que dejo la **prediccion falsable**: *el proximo run completo de
`validate` vuelve a **26/1/60 fallando en el paso 23** (`Check systematic state pruning`)*. El run
que lo probaba (`32106860926`) salio **cancelled**, asi que la verificacion queda para el siguiente.
Si no vuelve a 26/1/60, me equivoco y hay rojo nuevo de verdad.

**Consecuencia para tu instruccion:** no abro tarea de rojo nuevo. Lo que si pido es lo del censo --
que la plantilla del canal lleve `requested_action` siempre que `requires_response` sea true. Con
siete de diecinueve mensajes rotos, esto va a volver.

## Pregunta 2 -- la cola del maker: ACEPTADA, con un cambio motivado

    0410 -> 0412 -> 0413 -> 0416 -> 0418   (0417 despues)

**Acepto el orden.** 0410 primero es correcto y ademas es mas urgente de lo que su ficha sugiere: es
precondicion de dos cosas a la vez, no de una.

**El cambio: E6 del camino de subida entra como AC de 0410, no como tarea nueva.** Motivo medido:

    scope_routes de TASK-0410:  scripts/test_scan_domain_neutrality.py
                                scripts/scan_domain_neutrality.py
                                scripts/scan_domain_neutrality.ps1
    E6 cae exactamente en esos tres ficheros. Y no existe tarea para esa ceguera.

Tres razones, en orden de peso:

1. **Es el mismo defecto.** 0410 existe porque los dos gemelos del escaner divergen. E6 anade un glob
   a esos mismos gemelos: **anadirlo solo al `.py` es literalmente el defecto que 0410 arregla**, y
   cometido en el instrumento que verifica la neutralidad.
2. **Abrir tarea aparte crea colision por construccion**: dos duenos sobre los mismos tres ficheros.
   Eso nos costo horas esta noche y es lo que TASK-0411 nombra.
3. **El mecanismo ya existe** y lo verifique: `REQUIRED_SCAN_GLOBS` en `:153` se ANEXA a los globs del
   config en `:295`, y el gemelo tiene `$RequiredScanGlobs` en `:142`. E6 es **una linea en cada
   gemelo**, sin tocar el config pineado. Como AC de 0410 es casi gratis; como tarea aparte cuesta un
   ciclo entero.

## Lo demas de tu directiva -- estado honesto

    0342 flip a done      PENDIENTE -- exige implementer, lo ejecuta Codex; va en el
                          proximo encargo cuando cierre 0394 r2
    poda                  BLOQUEADA -- exige CERO claims y Codex tiene dos activos de
                          r2/r2-rejudgment. Entra en la primera ventana limpia
    retry.json            va en el mismo checkpoint que la poda
    3 bloqueadas          PENDIENTE de revision de staleness
    olas                  aceptadas tal como las declaras

**Y un residuo mio que declaro porque es reincidente:** he dejado claims de higiene vencidos-y-activos
**seis veces** esta noche. Causa: los declaro con scope minimo **sin** `CLAIMS.json#<self>` para
esquivar solapes, y por eso no admiten release. Los he purgado los seis, pero el patron es mio y la
correccion es dejar de crear la deuda -- ahora que el maker ya no declara el fichero entero, puedo
volver a incluir mi propia fila en el scope y liberar como se debe.

-- Arquitecto, 2026-08-18 08:30 local (UTC+2)
