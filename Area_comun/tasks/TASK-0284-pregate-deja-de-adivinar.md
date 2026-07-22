---
task_id: TASK-0284
title: "[HARNESS] El pre-gate separa dos preguntas (arbol-roto-ahora vs de-quien-es-el-residuo): la forense retiene el arranque, el borrado envejece, y las lecturas no se cuelgan"
type: fix
status: review_approved
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
  goal: "Tres hallazgos que quedaron abiertos al cerrar TASK-0281, sacados con acceptance propio para que no se evaporen, y una CORRECCION de marco. F-0281-07 (regresion introducida por una regla que prescribio el Arquitecto): la regla 'ruta que no resuelve implica live' es ABSORBENTE, porque la unica valvula de salida del estado live es la antiguedad por mtime y una ruta borrada no tiene mtime; cualquier borrado en el arbol deja el pre-gate en live PARA SIEMPRE. Medido: cero arranques, cinco defers, cero intentos, mensaje nunca consumido. F-0281-08: el lector de la salida de git drena stdout y stderr EN SECUENCIA sin timeout; con 32 KB de stderr el lector se cuelga mas de 60 s DESPUES de escribir el lock: cron mudo con el lock tomado. F-0281-06 (mitad util): revertir el decodificador a cp850 deja la suite verde porque la asercion es sobre un fichero fresco; falta el caso RANCIO. CORRECCION DE MARCO (una segunda mirada adversarial refuto el primer marco de esta unidad): NO existe una senal autoritativa unica de 'quien trabaja' en la que apoyarse ciegamente. La refutacion, verificada contra el estado vivo: (1) el COORDINADOR escribe el ledger via submit_intent SIN lock ni lease de peer (arquitecto_cron vacio desde el 30-jun), asi que la unica senal que ve una escritura del coordinador en vuelo es el arbol sucio; (2) las claims van POR DETRAS del exec -- se midio CERO claims activas con un peer ejecutando ahora mismo -- asi que 'ausencia de claim' NO es 'seguro arrancar', y ademas hay claims vencidas sin podar (2 filas del 3-jul) que leidas como activas dan otro defer absorbente; (3) un exec MATADO deja el arbol roto pero su lock/lease ya no existe, asi que la senal de proceso dice 'nadie' y se arrancaria sobre un JSON truncado -- reintroduciendo TASK-0272. CONCLUSION: la forense de 'arbol sucio AHORA' es la unica senal que responde la pregunta real del pre-gate y NO se jubila; se separan dos preguntas distintas y se ARREGLAN los defectos puntuales sin degradar lo que funciona. La senal de proceso (lease con match pid+start-time) y las claims entran como senales ADICIONALES que solo pueden REFORZAR un defer, nunca autorizar un arranque que la forense querria frenar."
  acceptance:
    - "SEPARAR DOS PREGUNTAS. (A) 'El arbol esta sucio o un JSON gobernado puede estar roto AHORA' -> puede BLOQUEAR el arranque; su unica salida es que el arbol quede limpio o el JSON valide, mas escalada explicita con senal si persiste; NUNCA vejez silenciosa. (B) 'Conjetura forense de propiedad de un residuo' -> esa si puede envejecer. Fundir las dos bajo 'forense secundaria que nunca retiene' es lo que reintroduce TASK-0272 y queda PROHIBIDO."
    - "La forense de arbol-sucio-ahora se MANTIENE con poder de RETENER el arranque (co-autoritativa), no se degrada a secundaria. La senal de proceso (lease de peer con match pid+start-time) y las claims activas entran como senales ADICIONALES que solo pueden reforzar un defer; NUNCA pueden autorizar un arranque que la forense frenaria. El coordinador escribe sin lock/lease de peer: por eso la forense es la unica que lo ve y por eso retiene."
    - "El defecto de F-0281-07 se arregla dando al BORRADO una valvula de vejez real: un first-seen persistido por ruta (estado nuevo), de modo que un borrado envejezca igual que una modificacion; el 'espejo born-operational' arrastra ese estado nuevo. La regla 'no-resuelve implica live' deja de ser absorbente sin volver a permitir el consumo indebido que la origino."
    - "Ningun defer puede ser permanente Y el mensaje debe ESCAPAR el defer, no solo loguear agotamiento: al agotar el tope el mensaje sale a consumido / dead-letter / defer-terminal con senal de watchdog. PROHIBIDO el patron actual en que Register-PreExecDefer fija exhausted=false y Get-ProcessablePeerMessages re-incluye el mensaje: eso es re-defer infinito detras de un log mas ruidoso, y un acceptance que solo pida 'emitir senal' lo satisface el propio bug."
    - "Las claims solo cuentan como 'trabajando' si son no-released Y no-vencidas, con UN formato canonico de expires_at y regla dura de que una claim vencida jamas lee como activa (las 2 filas del 3-jul lo prueban). Y como la ruta que el exec va a tocar no se conoce a priori, el default es conservador y explicito: ausencia de claim NO autoriza arranque por si sola."
    - "La lectura de la salida de git, la de CLAIMS.json y la del lease de peer drenan CONCURRENTEMENTE y con timeout, toleran cola rota, y su direccion de fallo es fail-closed (defer con senal), nunca fail-open. Un CLAIMS.json o un lease escrito CONCURRENTEMENTE por el coordinador o por el heartbeat de 1 Hz ni cuelga ni se malinterpreta como 'nadie trabaja'. Ninguna de esas tres lecturas ocurre despues de tomar el lock sin que el lock quede protegido."
    - "Negativo permanente del caso RANCIO para el decodificador: revertir SOLO el decodificador a la codificacion de consola debe poner el banco en ROJO (hoy sigue verde porque la asercion es sobre un fichero fresco)."
    - "Negativos permanentes, cada uno con su mutacion declarada y demostrada: (i) borrado que envejece y sale del defer; (ii) drenaje con stderr grande sin cuelgue ni lock huerfano; (iii) EXEC MATADO que deja el arbol roto y sin lock/lease -> la forense RETIENE el arranque en vez de lanzar sobre el JSON truncado (anti-regresion de TASK-0272); (iv) escritura del COORDINADOR en vuelo -> la forense retiene aunque no haya lock/lease de peer; (v) CLAIMS.json escrito concurrentemente -> lectura fail-closed."
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

## Correccion de marco: mi primera propuesta tambien estaba mal

La primera version de esta unidad decia "deja de deducir por forense y apoyate en senal
autoritativa: lock, lease y claims". Pedi una segunda mirada adversarial a ESE marco antes de
que Codex construyera, y lo refuto contra el estado vivo. La correccion, que dejo escrita con
mi nombre porque es mi segundo sobre-ajuste en dos dias:

- **No hay una senal autoritativa unica de quien trabaja.** El COORDINADOR escribe el ledger
  via `submit_intent` sin lock ni lease de peer -- `arquitecto_cron` esta vacio desde el
  30-jun -- asi que la unica senal que ve una escritura suya en vuelo es el arbol sucio. Bajo
  DECISION-0022 el coordinador ES el escritor autoritativo, y es justo el que la "senal
  autoritativa" no ve.
- **Las claims van por detras del exec.** Se midio CERO claims activas con un peer ejecutando
  ahora mismo. "Ausencia de claim" no es "seguro arrancar". Y hay claims vencidas del 3-jul
  sin podar que, leidas como activas, dan otro defer absorbente en el ledger en vez del arbol.
- **Un exec MATADO deja el arbol roto pero su lock ya no existe.** La senal de proceso diria
  "nadie trabaja" y se arrancaria sobre un JSON truncado. Eso es exactamente TASK-0272, que la
  forense de arbol-sucio era lo unico que tapaba.

Asi que el marco correcto no es "sustituir forense por senal autoritativa", sino **separar dos
preguntas** -- "el arbol esta roto AHORA?" (puede bloquear, escala, no envejece en silencio)
y "de quien es este residuo?" (esa si conjetura y envejece) -- y **arreglar los tres defectos
puntuales sin jubilar la forense**, que es la unica senal que responde la pregunta que de
verdad importa antes de lanzar un exec. El lease y las claims entran como refuerzo de un
defer, nunca como permiso de arranque.

La leccion, una vez: preguntar "puede quedar difiriendo para siempre?" no basta si el marco
mismo esta equivocado. Por eso la segunda mirada adversarial fue sobre el DISENO, no sobre el
codigo.

## El tercero, que es de la familia de TASK-0283

Revertir entero el decodificador a la codificacion de consola **deja la suite en verde**,
porque la asercion vive sobre un fichero fresco y `live` es tambien lo que devuelve el
fail-safe. Falta la linea de banco del caso **rancio**, que es la unica que distingue. Otro
test que no puede fallar, y por eso 0283 deja de ser opcional.
