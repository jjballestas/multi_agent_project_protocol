---
task_id: TASK-0281
title: "[HARNESS] El bucle no puede quedarse bloqueado ni ciego: lock huerfano por fallo de arranque, defer sin tope ni escalado, linea base por seq, y residuo sucio que nadie mira"
type: fix
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-21
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0276, TASK-0278, TASK-0280, DECISION-0020, DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0281-bucle-no-ciego-ni-bloqueado.md
intake:
  type: fix
  goal: "Cuatro defectos del bucle del harness encontrados por una revision adversarial independiente encargada por el Arquitecto tras cuatro iteraciones de TASK-0280. Ninguno esta cubierto por 0280 y los cuatro comparten familia: el bucle puede quedarse bloqueado, o esperando para siempre, o creyendo que trabajo antiguo es suyo, o ciego a un residuo que el mismo dejo. (1) LOCK HUERFANO, jam permanente: el lock se escribe antes de un tramo que corre FUERA del try cuyo finally lo borra; si el helper de cabeza no puede lanzarse, la excepcion escapa, el lock queda sin lease, Clear-StaleCronLockIfSafe no lo auto-sana precisamente porque no hay lease, y el cron entra en LOCKED skip indefinido. (2) DEFER SIN TOPE NI SENAL: el camino ledger_unreadable_before_exec no toca el estado de reintentos, asi que una causa permanente difiere la cola entera para siempre sin RETRY_EXHAUSTED ni senal de watchdog, violando el acceptance CERO QUIETUD SILENCIOSA de TASK-0272. (3) LINEA BASE FRAGIL: event_log_head devuelve el seq de la ULTIMA LINEA, no el maximo; con una cola desordenada (el clobber bajo doble escritor ya observado) la linea base cae por debajo de un evento propio anterior y la evidencia propia acepta trabajo historico. (4) RESIDUO SUCIO INVISIBLE: Get-StagedResidueState mira SOLO el indice, asi que un exec matado a mitad de escritura deja ficheros modificados no stageados que ningun pre-gate ve; hoy lo tapa el reset --hard, que es justo lo que hay que poder retirar."
  acceptance:
    - "Ningun fallo entre la escritura del lock y el arranque del proceso puede dejar el lock sin borrar: todo ese tramo queda cubierto por el mismo camino de limpieza que el resto, y una excepcion ahi deja el bucle en estado reintentable, no bloqueado."
    - "Un lock sin lease y sin proceso vivo se considera huerfano y se limpia solo, en vez de bloquear la cola indefinidamente."
    - "Todo camino de defer (cabeza ilegible, snapshot fallido, residuo vivo) tiene tope y escalado: al agotarlo emite senal equivalente a RETRY_EXHAUSTED para que el watchdog la vea. Ningun defer puede ser silencioso e infinito."
    - "La linea base de la evidencia propia deja de ser un seq: se toma del tamano en bytes o del numero de lineas del log pre-exec, de modo que una cola desordenada o reescrita no pueda hacer pasar un evento historico como propio de la ventana."
    - "Get-StagedResidueState pasa a mirar indice Y worktree (git status --porcelain): un exec matado que dejo ficheros modificados sin stagear produce defer con senal, no un arranque a ciegas contra un arbol roto."
    - "Negativos permanentes por el bucle real para los cuatro: helper de cabeza que no arranca (lock limpio y cola viva), defer repetido hasta el tope (senal emitida), log con cola desordenada (evidencia propia falsa NO se acepta), y residuo modificado-no-stageado (defer con senal)."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde con los cuatro negativos nuevos"
    - "Prueba de bucle real con el helper de cabeza inutilizable: el lock no sobrevive y la cola sigue viva"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Retirar la rama destructiva del rollback (reset --hard y re-apply del parche de worktree) - FUERA de esta unidad: esa retirada necesita enmienda firmada del Operador porque toca la mitad 'revert' del acceptance de TASK-0272, y ademas depende de que el punto 4 de esta unidad este cerrado."
    - "Reabrir el acceptance de TASK-0280 - FUERA."
    - "Cambiar la frontera de outcome (token, exit, evidencia, texto libre) - FUERA."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: medium
  estimate: M
---

# TASK-0281 - El bucle no puede quedarse bloqueado ni ciego

Origen: revision adversarial independiente encargada por el Arquitecto tras cuatro
iteraciones de TASK-0280, con el encargo explicito de romper la propuesta del propio
Arquitecto. Encontro estos cuatro y de paso refuto el vector que el checker habia declarado
bloqueante en la iteracion 3 (ver la consulta de reconciliacion ruteada al checker).

Los cuatro comparten una forma: **el bucle se queda sin salida o sin vista**.

1. **Se queda bloqueado.** Un fallo al lanzar el helper de cabeza deja el lock huerfano, sin
   lease, y la auto-sanacion no actua justamente porque no hay lease. El cron hace
   `LOCKED skip` de toda la cola para siempre.
2. **Se queda esperando.** El defer por cabeza ilegible no toca el estado de reintentos: si
   la causa es permanente, la cola entera espera indefinidamente sin ninguna senal. Es la
   quietud silenciosa que TASK-0272 declaro inaceptable, por otra puerta.
3. **Se cree dueno de trabajo ajeno en el tiempo.** La linea base por `seq` de la ultima
   linea es fragil ante una cola desordenada, que ya hemos sufrido bajo doble escritor. Por
   bytes o lineas, el problema desaparece sin depender de que el log este bien ordenado.
4. **No ve lo que el mismo rompio.** El pre-gate solo mira el indice. Un exec matado a mitad
   de escritura deja ficheros sucios que nadie detecta; hoy eso lo tapa el `reset --hard`,
   que es precisamente la operacion que queremos poder retirar por destructiva. Sin el punto
   4, retirarla convierte una destruccion visible en una parada silenciosa.

Por eso el punto 4 es **precondicion** de la retirada de la rama destructiva, y por eso esa
retirada vive fuera de esta unidad y con firma del Operador.
