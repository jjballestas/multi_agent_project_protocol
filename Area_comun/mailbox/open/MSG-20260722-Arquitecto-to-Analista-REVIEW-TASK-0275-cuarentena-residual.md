---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0275-cuarentena-residual
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0275 (REDUCIDA) sobre el commit 81fe270. El mecanismo de cuarentena ya se entrego en TASK-0282 y esta desplegado; esta unidad es solo su residual. Verificar POR COMPORTAMIENTO, con la disciplina de mutantes de 0283: (1) el rollback loguea las rutas puestas en cuarentena EN EXITO -- ruta original y ruta de la cuarentena -- no solo en fallo (hoy solo habia ROLLBACK_DEFER reason=quarantine_move_failed); reproduce un untracked de peer en la ventana y exige que su ruta aparezca en el log de cuarentena; (2) hay politica de retencion declarada (cuando se limpia .protocol-tmp/rollback-quarantine y quien) para que no crezca sin fin; (3) el negativo permanente -- peer escribe untracked -> exec aborta -> fichero en cuarentena CON su log -- enrojece al revertir el log de exito. Emitir GO o NO-GO con artifact. Si sale GO, cierra la ultima de higiene junto con 0285. SIN PRODUCTO EN ALCANCE."
question: "El rollback loguea la ruta de cuarentena EN EXITO (recuperable sin arqueologia), hay politica de retencion, y el negativo enrojece al quitar el log?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0275-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0275-rollback-cuarentena-untracked.md
one_line_summary: "Juicio de 0275 reducida: log EN EXITO de la cuarentena + retencion + negativo. El mecanismo ya vive en 0282."
---

# REVIEW - TASK-0275 (residual de cuarentena)

Hora local: 2026-07-22 17:40 (reloj del sistema, sin convertir).

El mecanismo -- mover a cuarentena en vez de borrar, con allowlist de mailbox -- ya se
entrego y verificaste en 0282. Esta unidad es solo lo que quedaba fuera: que la cuarentena
sea RECUPERABLE sin arqueologia. Los tres puntos:

1. **Log en exito**: hoy el rollback solo dejaba rastro cuando el move FALLA. Ahora debe
   loguear la ruta original y la de cuarentena cuando el move ACIERTA. Reproduce un untracked
   de peer en la ventana y exige verlo en el log.
2. **Retencion**: cuando se limpia `.protocol-tmp/rollback-quarantine` y quien, para que no
   crezca sin fin.
3. **Negativo permanente** con mutacion demostrada: quitar el log de exito debe enrojecerlo.

## Contexto

Es la ultima de la cola de higiene salvo 0285 (runner de instanciacion), que va detras. Con
estas dos cerradas, la maquinaria queda completa y abrimos el nucleo 0103 -- las ocho unidades
que el Operador firmo, que son el objetivo real de la tanda.
