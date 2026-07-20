---
task_id: TASK-0280
title: "[HARNESS][CRITICO] El rollback del exec revierte el LEDGER: transacciones ya aplicadas desaparecen y el agente reporta trabajo que no existe"
type: fix
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0277, TASK-0278, DECISION-0022, DECISION-0103]
linked_decisions: [DECISION-0022, DECISION-0103]
file: Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
intake:
  type: fix
  goal: "Observado en campo el 2026-07-20 a las 18:33. Un exec aplico correctamente el done-flip de TASK-0278 por el runtime (eventos 5402 a 5404 segun su propio reporte), despues aborto por una condicion no relacionada, y el rollback de TASK-0272 restauro el worktree pre-exec, borrando de paso runtime/state/events.jsonl. Resultado: el agente entrego un informe afirmando que la unidad quedaba cerrada mientras el ledger vivo sigue en 5401 y TASK-0278 sigue en review_approved. El ledger es append-only y es la fuente de verdad; un rollback de worktree no puede tratarlo como un fichero mas. La consecuencia no es solo perder trabajo: es producir un reporte ATESTADO que afirma algo que el ledger no respalda, que es exactamente la clase de fallo que esta metodologia existe para impedir."
  acceptance:
    - "El rollback del exec NO restaura runtime/state/events.jsonl ni el resto del estado del ledger a su version pre-exec; el log firmado es append-only y queda fuera del alcance de la restauracion."
    - "Si el exec aplico eventos y despues aborta, el harness lo DECLARA en su senal (los eventos aplicados quedan y se reportan), en vez de dejar al agente afirmando trabajo que ya no existe."
    - "Ningun camino del rollback puede dejar el ledger y el estado derivado en desacuerdo: si tras el rollback el estado derivado ya no corresponde al log, el harness lo detecta y lo senala en vez de continuar en silencio."
    - "Negativo permanente: exec que aplica una transaccion de ledger y despues aborta por precondicion; el evento sobrevive, el reporte lo refleja y el mensaje sigue siendo reintentable sin duplicar el trabajo ya aplicado."
    - "Negativo permanente del caso inverso: un exec que NO aplico nada mantiene el rollback completo del worktree tal y como lo dejo TASK-0272."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde con los negativos nuevos"
    - "Sandbox E2E: transaccion aplicada mas aborto posterior, el evento permanece en el log"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Reescribir o re-firmar eventos existentes - PROHIBIDO."
    - "Cambiar el modelo de transacciones del runtime (submit_intent ya es atomico con rollback propio) - FUERA, el defecto es del rollback de worktree del harness."
    - "Re-genesis o cualquier toque al config pineado - PROHIBIDO (epoch 1.14.0, genesis 2E35F26E, dataset N=500)."
    - "Unidades RESERVADAS del preregistro N=6 - FUERA."
  risk: high
  estimate: S
---

# TASK-0280 - Un rollback no puede borrar el libro

Secuencia real del 2026-07-20:

1. 18:33, el exec de Codex aplica el done-flip ratificado de TASK-0278 por la via
   gobernada. Sus eventos existen mientras el exec vive.
2. El mismo exec intenta despues reproducir el `prune_state --apply` que le pedi, choca
   con el fallo de TASK-0277 y decide abortar.
3. El rollback de TASK-0272 restaura el worktree al estado pre-exec. `events.jsonl` es un
   fichero del worktree, asi que vuelve atras con todo lo demas.
4. Su informe dice, de buena fe, que TASK-0278 quedo cerrada citando los seq 5402 a 5404.
   El ledger vivo termina en 5401 y la unidad sigue en `review_approved`.

Nadie mintio y sin embargo el reporte era falso. Esa es la gravedad: no es perdida de
trabajo, es **atestacion sin respaldo**, producida por el propio mecanismo de seguridad.

Remediacion iteracion 1: una unica primitiva compartida captura `seq` y SHA-256 de la
cabeza del event log. El rollback solo excluye rutas gobernadas cuando esa cabeza avanzo,
preserva cambios trackeados sin resucitar altas staged, y contrasta otra vez la cabeza
antes del reset y despues de restaurar.

Remediacion iteracion 2: las rutas preservadas se derivan de los eventos aplicados en la
ventana, no del tipo de cambio que informa git. Esto conserva tambien movimientos
firmados de mailbox (baja en `open/` y alta en `archived/`). La primitiva de cabeza tolera
una ultima linea desgarrada y el harness emite `ROLLBACK_DEFER reason=ledger_torn_tail`
sin mutar la cola. Ambos casos tienen negativos permanentes en el sandbox de reintentos.

Relacion con lo demas: el rollback de TASK-0272 sigue siendo correcto para lo que se
diseno, deshacer el residuo staged de un exec abortado. El error es de alcance, no de
concepto. El ledger firmado no es residuo: es la unica cosa del arbol que no se puede
deshacer restaurando un fichero.
