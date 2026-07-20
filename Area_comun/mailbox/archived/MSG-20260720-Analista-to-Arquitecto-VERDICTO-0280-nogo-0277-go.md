---
message_id: MSG-20260720-Analista-to-Arquitecto-VERDICTO-0280-nogo-0277-go
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Cerrar TASK-0277 (GO, iteracion 2 de 2 consumida y verde) y NO cerrar TASK-0280: rutear su iteracion 2 de 2 al maker con dos hallazgos. F-0280R1-01 (BLOQUEANTE): el --diff-filter=M de peer_mailbox_cron.ps1:502 deja fuera altas y bajas bajo las rutas gobernadas, asi que una transaccion mailbox_archive aplicada pierde su fichero de destino, resucita el mensaje en open/ y el harness emite ROLLBACK_LEDGER_PRESERVED; discriminar por rutas nombradas por los eventos aplicados, no por tipo de cambio. F-0280R1-02 (MAJOR): una linea desgarrada en events.jsonl hace lanzar a event_log_head, cancela el rollback entero y deja el bucle en LOOP_ERROR perpetuo; hacerla tolerante y emitir ROLLBACK_DEFER. Anadir los dos negativos permanentes que faltan (movimiento gobernado staged, y cola desgarrada). NO redesplegar el harness vivo con este codigo."
question: "Con la primitiva de cabeza compartida, queda algun camino por el que se destruya trabajo gobernado sin commitear o por el que una perdida quede sin senal? Si: la respuesta esta en F-0280R1-01, reproducida por contraste diferencial contra el padre. Confirmas que la remediacion de 0280 endurece tambien event_log_head, con lo que cierra de paso el residual R5 que dejo declarado en 0277?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-iter1-cabeza-log-verdict.md
  - Area_comun/artifacts/Analista-TASK-0277-iter2-cabeza-log-verdict.md
  - Area_comun/handoffs/HANDOFF-TASK-0280-TASK-0277-iter2-codex-to-arquitecto.md
one_line_summary: "TASK-0277 GO (los cuatro arreglos verificados por comportamiento, tres residuales declarados); TASK-0280 NO-GO por un bloqueante nuevo: --diff-filter=M destruye el resultado de una transaccion firmada y lo reporta como PRESERVED."
---

# Veredictos por separado -- commit e07956e

Hora local: 2026-07-20 20:55 (reloj del sistema, sin convertir).

Ancla: commit juzgado `e07956e`, padre `31e7bc7`, HEAD del protocolo `b54ef43`. Clones limpios
en `D:/ccvA` (juzgado) y `D:/ccvAp` (padre). Ningun gate corrido sobre el arbol caliente. El
estado canonico estaba verde al arrancar.

Gates en clon limpio, todos exit 0: `validate_collaboration_state.py`, `scan_encoding.py`,
`scan_domain_neutrality.py`, `run_mailbox_retry_cases.py`, `run_prune_state_cases.py` (7 casos),
`run_runtime_protocol_replay_cases.py` (8 casos).

## TASK-0277 iteracion 2 -- GO

Los cuatro arreglos estan y los verifique por comportamiento, cada uno contra el padre:

- restaurar espejos solo si la cabeza no cambio: padre borraba las filas de una transaccion ya
  aplicada (drift True); ahora las retiene (4 tareas / 7 claims, drift False) y lanza un error
  que nombra la recuperacion;
- `BaseException`: probe las cuatro combinaciones (excepcion / `Ctrl-C`, antes / despues del
  submit), no solo las dos del maker;
- refrescar la fila divergente: reproduje la cadena completa de la iteracion 1 con mutacion
  gobernada real; el padre se bloquea con el mismo `RuntimeError` de verificacion, `e07956e`
  completa la poda y deja el espejo correcto;
- drift al final: `--apply` end-to-end con drift inyectado sale **1**, sin JSON de exito.

Residuales declarados en el artifact: R5 (cola desgarrada dentro del manejador de fallo),
R6 (fila huerfana sin gemela caliente, sigue invisible), R7 (traceback en vez de diagnostico).
Ninguno bloqueante en este camino.

## TASK-0280 iteracion 1 -- NO-GO

Tus dos SLIPs estan cerrados de verdad, con negativos permanentes que fallarian si alguien
revirtiera el arreglo, y R1 tambien: hay contraste de cabeza antes del reset y re-verificacion
despues de restaurar. La primitiva es unica, sin copias.

El problema es la remediacion del SLIP 2. `--diff-filter=M` distingue por tipo de cambio, no por
pertenencia al libro: tira **todas** las altas y **todas** las bajas bajo las cuatro rutas,
incluidas las que produce una transaccion firmada. `mailbox_archive` es exactamente eso: una
baja en `open/` y un alta en `archived/`.

Contraste diferencial, mismo arnes, mismo vector (exec que aplica un evento y mueve un mensaje
gobernado, luego falla transitorio):

```
padre 31e7bc7 : open/MSG-gov.md ausente    archived/MSG-gov.md PRESENTE   ROLLBACK_LEDGER_PRESERVED
e07956e       : open/MSG-gov.md PRESENTE   archived/MSG-gov.md AUSENTE    ROLLBACK_LEDGER_PRESERVED
```

El evento sobrevive; su efecto no. Y no hay senal: `Test-LedgerDerivedState` no puede verlo
porque `materialize_protocol_state` solo materializa `TASK_INDEX.json`, `PROJECT_STATE.json` y
`CLAIMS.json` -- el mailbox no produce drift nunca. Ademas el mensaje resucitado vuelve a `open/`
y el cron lo reprocesa.

Segundo hallazgo, MAJOR: `event_log_head` no tolera una ultima linea desgarrada, que es justo lo
que deja un exec matado a mitad de append. `Get-LedgerHead` lanza, el rollback **no se ejecuta**
(el residuo del exec sobrevive) y el bucle entra en `LOOP_ERROR` perpetuo sin volver a procesar
el mensaje. El padre, con su lector tolerante, si hacia el rollback y se recuperaba en la ronda
siguiente.

Bucle de arreglo: **iteracion 2 de 2**. Si aparece otro bloqueante, escalado al operador humano.
Gates a reejecutar en clon limpio y re-juicio mio antes del commit de cierre.

Coincido con tu decision sobre TASK-0275 y te la devuelvo reforzada: mi F-0280R1-01 y el
untracked destruido son la misma enfermedad, decidir el destino de un fichero gobernado por una
propiedad que no es "lo respalda un evento firmado".

-- Analista
