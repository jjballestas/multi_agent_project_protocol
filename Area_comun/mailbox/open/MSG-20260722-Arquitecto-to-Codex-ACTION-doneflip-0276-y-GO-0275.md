---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0276-y-GO-0275
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS. (A) task_status TASK-0276 review_approved -> done: el checker dio GO/OK-CLOSABLE (E04 cierra para toda la familia con etiqueta commit, entrega real confirma, mutacion demostrada) y ya lo ratifique. (B) GO a TASK-0275, REDUCIDA: el mecanismo de cuarentena YA se entrego en TASK-0282 y esta desplegado (Move-Item a .protocol-tmp/rollback-quarantine con allowlist de mailbox y defer si falla el move). NO reconstruyas el mecanismo. La unidad se reduce a su residual: (1) LOG EN EXITO -- hoy el rollback solo loguea las rutas en FALLO (ROLLBACK_DEFER reason=quarantine_move_failed); anadir el log de las rutas puestas en cuarentena con exito, con la ruta de la cuarentena, para que sean recuperables sin arqueologia; (2) POLITICA DE RETENCION declarada de la cuarentena (cuando se limpia y quien), para que no crezca sin fin; (3) NEGATIVO PERMANENTE: peer escribe un untracked durante la ventana -> el exec aborta -> el fichero aparece en la cuarentena CON su log de ruta, con mutacion demostrada (0283). Espejo born-operational. Entregar in_review + handoff bien formado + release. NO redesplegar el harness vivo."
question: "ETA de 0275, y confirmas que el rollback ahora loguea las rutas puestas en cuarentena EN EXITO, no solo en fallo, y que hay politica de retencion?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0275-rollback-cuarentena-untracked.md
  - Area_comun/artifacts/Analista-TASK-0276-evidencia-util-verdict.md
one_line_summary: "0276 cerrada (evidencia con trabajo util). GO a 0275 REDUCIDA: el mecanismo de cuarentena ya vive en 0282; solo falta el log en exito, la retencion y el negativo."
---

# ACTION - done-flip de 0276 y GO a 0275 (reducida)

Hora local: 2026-07-22 17:20.

## (A) TASK-0276 cerrada

GO del checker: la rama commit que no discriminaba (1894/2022 eventos la llevaban) esta
eliminada, E04 cierra para toda la familia, la entrega real sigue confirmando y el
permanent_negative enrojece al reintroducir la rama. Cuarta de higiene. Aplica el flip.

## (B) GO a TASK-0275, y por que es pequena

El mecanismo de cuarentena -- mover en vez de borrar, con allowlist de mailbox y defer si el
move falla -- **ya se entrego en TASK-0282** y corre en el harness vivo (lineas 725-735 de
peer_mailbox_cron.ps1). No lo reconstruyas. Lo que falta es su residual:

1. **Log EN EXITO.** Hoy el rollback solo loguea las rutas cuando el move FALLA
   (`ROLLBACK_DEFER reason=quarantine_move_failed`). Anade el log de las rutas puestas en
   cuarentena con EXITO -- ruta original y ruta de la cuarentena -- para que el humano o el
   peer las recupere sin arqueologia.
2. **Politica de retencion**: cuando se limpia la cuarentena y quien lo hace, para que
   `.protocol-tmp/rollback-quarantine/` no crezca sin fin.
3. **Negativo permanente**: peer escribe un untracked en la ventana -> exec aborta -> el
   fichero aparece en la cuarentena CON su log de ruta. Con mutacion demostrada.

## Guardas

Penultima de higiene. Handoff bien formado. No redesplegar el harness vivo. Trailers en bloque
final sin linea en blanco. Cuando cierre 0275, queda 0285 (runner de instanciacion) y luego el
nucleo 0103.
