---
task_id: TASK-0284
title: "[HARNESS] El pre-gate deja de adivinar por forense del arbol: senal autoritativa de quien trabaja, borrado que puede envejecer, y lectura de git que no se cuelga"
type: fix
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-22
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0281, TASK-0283, DECISION-0020, DECISION-0103]
linked_decisions: [DECISION-0103, DECISION-0020]
file: Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
intake:
  type: fix
  goal: "Tres hallazgos que quedaron abiertos al cerrar TASK-0281, sacados con acceptance propio para que no se evaporen, mas el cambio de marco que explica por que aparecieron. F-0281-07 (regresion introducida por una regla que prescribio el Arquitecto): la regla 'ruta que no resuelve implica live' es ABSORBENTE, porque la unica valvula de salida del estado live es la antiguedad por mtime y una ruta borrada no tiene mtime; cualquier borrado en el arbol deja el pre-gate en live PARA SIEMPRE. Medido en el runner completo con el ajuste mas permisivo posible: cero arranques, cinco defers, cero intentos, mensaje nunca consumido. Y el borrado no es exotico: archivar un mensaje de mailbox, podar estado o mover un handoff dejan exactamente esa forma. F-0281-08: el lector de la salida de git drena stdout y stderr EN SECUENCIA y sin timeout, asi que si git llena el buffer de stderr antes de cerrar stdout el lector se cuelga; medido con 32 KB de stderr, mas de 60 s colgado, y el cuelgue ocurre DESPUES de escribir el lock: cron colgado CON el lock tomado, sin log, sin defer y sin senal. F-0281-06 (mitad util): revertir entero el decodificador a cp850 deja la suite en verde, porque la asercion es sobre un fichero fresco; falta el caso RANCIO, que es el unico que distingue. CAMBIO DE MARCO: los tres salen de que el pre-gate intenta deducir por forense del arbol si hay alguien trabajando ahora mismo. Esa deduccion es la misma enfermedad que costo la cadena 0272-0281 en el rollback. Existe senal autoritativa de quien trabaja -- el lock y el lease de cada peer, y las claims del ledger -- y el pre-gate debe apoyarse en ella en vez de adivinar por ficheros."
  acceptance:
    - "El pre-gate determina 'hay un peer trabajando' a partir de la senal AUTORITATIVA (lock y lease vivos de un peer, y claims activas en el ledger), no de forense de ficheros del arbol."
    - "La forense del arbol queda como senal SECUNDARIA y acotada: puede pedir defer, pero nunca de forma absorbente, y todo estado de defer tiene una via de salida que no dependa de que exista un fichero (un borrado tiene que poder envejecer igual que una modificacion)."
    - "Ningun defer puede ser permanente: si la condicion persiste mas alla del tope, se emite senal de agotamiento como en el resto del bucle."
    - "La lectura de la salida de git drena stdout y stderr CONCURRENTEMENTE y con timeout; un git que escribe mucho en stderr no puede colgar el lector."
    - "Ninguna operacion que pueda colgarse ocurre despues de tomar el lock sin que el lock quede protegido: un cuelgue deja senal y libera, nunca un cron mudo con el lock tomado."
    - "Negativo permanente del caso RANCIO para el decodificador: revertir SOLO el decodificador a la codificacion de consola debe poner el banco en ROJO (hoy sigue verde porque la asercion es sobre un fichero fresco)."
    - "Negativos permanentes para el borrado que envejece y para el drenaje con stderr grande, con su mutacion declarada y demostrada."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde con los negativos nuevos"
    - "Prueba de bucle real: borrado en el arbol -> el pre-gate sale del defer al envejecer, no se queda absorbido"
    - "Prueba de bucle real: git con stderr grande -> el lector termina, no cuelga, y el lock no queda tomado en silencio"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Reabrir el acceptance de TASK-0281, que se cierra con estos tres sacados aqui - FUERA."
    - "Tocar el rollback (eso es TASK-0282, con enmienda firmada) - FUERA."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: high
  estimate: M
---

# TASK-0284 - El pre-gate deja de adivinar

## Lo que pasa cuando el coordinador prescribe una regla sin valvula

La regla "ruta que no resuelve implica live" **la prescribi yo**, en la iteracion 3 de
TASK-0281, para cerrar un consumo indebido de mensajes. Cerro el consumo y abrio una parada:
la unica salida del estado `live` es la antiguedad por `mtime`, y **un fichero borrado no
tiene mtime**, asi que cualquier borrado deja el pre-gate en `live` para siempre.

El checker lo midio con el ajuste mas permisivo que existe -- cero arranques, cinco defers,
cero intentos, mensaje jamas consumido -- y contra el commit padre, que con el mismo fixture
si arrancaba. Y el borrado no es un caso raro: **archivar un mensaje de mailbox, podar estado
o mover un handoff dejan esa forma**. La produce el propio banco de pruebas.

Lo escribo con nombre porque la leccion vale mas que el arreglo: **yo mismo hice la pregunta
correcta** al rutear el juicio -- si un arbol sano podia quedar difiriendo para siempre -- y
aun asi prescribi la regla sin la valvula. Preguntarlo no basta si no se convierte en
acceptance.

## Por que un cambio de marco y no un cuarto parche

Los tres hallazgos salen del mismo sitio: el pre-gate intenta **deducir por forense del arbol**
si hay alguien trabajando ahora mismo. Es la misma enfermedad que costo la cadena entera en el
rollback: inferir propiedad y actividad a partir de un artefacto compartido y mutable.

Y no hace falta deducirlo. **Existe senal autoritativa**: cada peer escribe su lock y su lease
mientras trabaja, y el ledger tiene las claims activas. El pre-gate debe leer eso. La forense
del arbol se queda como senal secundaria, util para pedir un defer, nunca para decidir sola y
nunca de forma absorbente.

## El tercero, que es de la familia de TASK-0283

Revertir entero el decodificador a la codificacion de consola **deja la suite en verde**,
porque la asercion vive sobre un fichero fresco y `live` es tambien lo que devuelve el
fail-safe. Falta la linea de banco del caso **rancio**, que es la unica que distingue. Otro
test que no puede fallar, y por eso 0283 deja de ser opcional.
