---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0275-y-GO-0285
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS. (A) task_status TASK-0275 review_approved -> done: el checker dio GO/OK-CLOSABLE (log ROLLBACK_QUARANTINED en exito, retencion 30d manual, negativo killeado por mutacion en 2 capas) y ya lo ratifique; el residual de retencion documental-no-maquinal queda declarado, no bloqueante. (B) GO a TASK-0285, la ULTIMA de higiene: el runner de instanciacion completa nace ROJO por dos causas ajenas a cualquier unidad, confirmadas preexistentes por el checker en el padre 6197e10. Arreglar: (1) el export born-operational arrastra ledger_head (modulo/entrypoint) a la instancia generada, de modo que el prune_state generado lo encuentre y el runner pueda invocarlo; (2) la asercion de coordination-default del runner distingue el tier de la instancia -- no da rojo cuando la instancia es runtime-tier legitima. El runner de instanciacion completa pasa a VERDE sobre una instancia recien exportada, para que un rojo futuro sea senal real. Negativo permanente con mutacion demostrada: quitar ledger_head del export vuelve a poner el runner rojo; tier mal declarado tambien. Espejo born-operational. Entregar in_review + handoff bien formado + release. NO redesplegar el harness vivo."
question: "ETA de 0285, y confirmas que el runner de instanciacion completa pasa a verde sobre una instancia recien exportada, con ledger_head arrastrado y la asercion de tier corregida?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0285-instanciacion-runner-ledger-head.md
  - Area_comun/artifacts/Analista-TASK-0275-cuarentena-residual-verdict.md
one_line_summary: "0275 cerrada (cuarentena recuperable). GO a 0285, la ultima de higiene: el runner de instanciacion deja de nacer rojo (ledger_head exportado + asercion de tier)."
---

# ACTION - done-flip de 0275 y GO a 0285, la ultima de higiene

Hora local: 2026-07-22 17:55.

## (A) TASK-0275 cerrada

GO del checker: el rollback loguea `ROLLBACK_QUARANTINED path=<orig> quarantine_path=<stored>`
en exito, por fichero, recuperable sin arqueologia; retencion de 30 dias con limpieza manual;
y el negativo permanente muere por mutacion en dos capas. Residual declarado: la retencion es
documental, no automatica -- no bloqueante. Quinta de higiene. Aplica el flip.

## (B) GO a TASK-0285, y cierra la maquinaria

El runner de instanciacion completa -- el humo que prueba que una instancia recien nacida
arranca sana -- nace ROJO por dos causas que el checker confirmo preexistentes (fallan igual
en el padre 6197e10, sin codigo de otra unidad):

1. **El export no arrastra `ledger_head`.** El `prune_state` generado en la instancia lo usa
   pero no lo encuentra, y el runner falla al invocarlo. Haz que el export born-operational lo
   arrastre.
2. **La asercion de tier asume coordination.** El runner da falso rojo cuando la instancia es
   runtime-tier legitima. Que distinga el tier declarado.

El objetivo es simple: **el runner pasa a verde sobre una instancia recien exportada**, para
que un rojo futuro sea senal real y no ruido que nadie puede distinguir de un fallo.

Negativo permanente con mutacion demostrada: quitar `ledger_head` del export vuelve a poner el
runner rojo; un tier mal declarado tambien.

## Guardas

Es la ultima de higiene. Cuando cierre, la maquinaria queda completa y abrimos el nucleo 0103
-- las ocho unidades que el Operador firmo. Handoff bien formado. No redesplegar el harness
vivo. Trailers en bloque final sin linea en blanco.
