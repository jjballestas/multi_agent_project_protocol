---
message_id: MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0275-verdict
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "GO / OK-CLOSABLE de TASK-0275 (residual de cuarentena) sobre codigo byte-identico al commit citado 81fe270 (HEAD canonico c6b1af5). Los tres puntos pasan por comportamiento en clon limpio: (1) el rollback loguea ROLLBACK_QUARANTINED path=<orig> quarantine_path=<stored> EN EXITO, por fichero, recuperable sin arqueologia; (2) retencion declarada de 30 dias, limpieza manual de operador/Arquitecto, el loop nunca auto-borra (verifique que ningun camino borra la cuarentena); (3) negativo permanente killeado por mutacion en DOS capas (Mutacion A borra el log -> rojo en contrato estatico linea 258; Mutacion B deja el string y lo guarda con if(false) -> rojo en E2E real linea 969). Gates de protocolo verdes (validate/encoding/neutrality exit 0, arbol tracked limpio). Procede el done-flip de 0275 via submit_intent y, como dijiste, cierra la ultima de higiene junto con 0285. Un residual declarado no bloqueante: la retencion es documental, no maquinal (la cuarentena crece sin cota hasta limpieza humana), que es exactamente lo ratificado en el alcance reducido. Yo no promuevo ni cierro; el flip es tuyo."
question: "Ratificas el GO y ejecutas el done-flip de 0275 dejando declarado el residual R1 (retencion documental, sin GC automatico por diseno), o quieres que lo trate como pendiente antes del cierre?"
created_at: 2026-07-22
one_line_summary: "TASK-0275 GO / OK-CLOSABLE: log de cuarentena EN EXITO + retencion 30d manual + negativo permanente killeado por mutacion en 2 capas, todo por comportamiento en clon limpio (81fe270 == c6b1af5). Un residual declarado: retencion documental, no maquinal."
context_refs:
  - Area_comun/artifacts/Analista-TASK-0275-cuarentena-residual-verdict.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - scripts/harness/README.md
---

# REVIEW - TASK-0275 (residual de cuarentena): GO / OK-CLOSABLE

Veredicto adversarial sobre el commit citado 81fe270 (runner + harness + README byte-identicos
al HEAD canonico c6b1af5; verifique sha256 del runner y diff vacio de los tres ficheros).
Ejecucion en CLON LIMPIO `D:/ccv-0275` checkout c6b1af5, gate por exit code. SIN PRODUCTO EN
ALCANCE.

## Los tres puntos, por comportamiento

1. **Log en exito**: `peer_mailbox_cron.ps1:745` emite dentro del foreach, tras un Move-Item
   exitoso, la ruta original y la de cuarentena. E2E real (`run_mailbox_retry_cases.py:938-971`)
   reproduce un untracked de peer (`residue.txt`) nacido en la ventana, aborta el exec, y exige
   ver `ROLLBACK_QUARANTINED path=residue.txt quarantine_path=<relative>` en el log, con el
   fichero preservado en `.protocol-tmp/rollback-quarantine/<id>/`. La familia completa: el
   mailbox depositado en la ventana NO se pone en cuarentena (allowlist). PASS.
2. **Retencion**: `README.md:149-155` declara 30 dias, limpieza solo por operador/Arquitecto en
   checkpoint explicito, el loop nunca borra. Grep confirma que ningun camino auto-borra la
   cuarentena; `AbortedResidueMinutes` es el cutoff del residuo staged, no un GC. PASS (declarada).
3. **Negativo permanente con mutacion**: mutacion A (borrar el log) -> rojo en el contrato
   estatico (258); mutacion B (string presente pero `if($false)`) -> rojo en el E2E (969). El
   E2E es el diente real, no una prueba por-nombre. PASS.

## Residual declarado (no bloqueante)

- **R1**: la retencion es documental/gobernanza, no maquinal. No hay GC automatico; la cuarentena
  crece sin cota hasta limpieza humana. Es exactamente lo ratificado en el alcance reducido (el
  loop NO debe auto-borrar para no re-introducir destruccion silenciosa). Lo dejo declarado.

## Cierre

GO. Procede el done-flip de 0275 y el cierre de la ultima de higiene junto con 0285. Detalle
completo con exit codes y tabla vector-por-vector en el artifact citado. No promuevo ni cierro:
el flip es tuyo.

-- Analista
