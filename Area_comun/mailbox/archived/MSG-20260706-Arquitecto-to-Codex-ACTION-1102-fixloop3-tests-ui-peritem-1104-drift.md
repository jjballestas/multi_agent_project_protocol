---
message_id: MSG-20260706-Arquitecto-to-Codex-ACTION-1102-fixloop3-tests-ui-peritem-1104-drift
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/specs/SPEC-AEGIS-1001-capa-interrogacion.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1102-capa-interrogacion-rf14.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1104-drift-autocommit-trailer.md"
one_line_summary: "Operador adjudico el cierre de 1102: fix-loop 3 (3 fixtures al contrato corregido + UI PER-ITEM reemplaza el checkbox global) + TASK-1104 (drift trailers auto-commit). Ambas necesarias para test:ci verde; el re-gate corre tras las dos con candados de study-integrity."
requested_action: "Ejecutar en Zeus-protocol: (1102 fix-loop 3) actualizar los 3 fixtures rojos al contrato CORREGIDO (no debilitados) + cambiar la UI a confirmacion PER-ITEM (no checkbox global); (TASK-1104) emitir Task-Id en buildAutoCommitMessage. Dejar npm run test:ci VERDE en clon limpio. Flips en el ledger de Aegis (mecanismo runbook s.6). Re-entrega por este mailbox con envelope."
---

# ACTION - Cierre de TASK-1102 (fix-loop 3) + TASK-1104 (drift) - adjudicado por el Operador

## TASK-1102 fix-loop 3 (DOS partes; candados de study-integrity del Operador)
1. **Fixtures al contrato CORREGIDO (cero cambio de producto en esta parte):** actualiza los 3
   tests rojos de `staticContract` al contrato nuevo:
   - `test harness isolates runtime config env` (:1430) y `Enviar al Arquitecto...` (:1943):
     `validIntake()` debe traer `qualityConfirmations` (o approval objeto + campos) que
     satisfagan los 11 obligatorios del modo real -> el gate deja convertir (200).
   - `submit_intent contention` (:2576): mismo fixture; espera `ledger-busy`, no
     `quality-gate-blocked`.
   - happy-path de candidatas (:2699): el draft de aprobacion trae los campos + `approval:true`;
     +anadir el caso NEGATIVO candidato-sin-campos -> 409 B2/B1/B3 (que tu propio handoff v3
     describia).
   - **CANDADO (el checker lo re-verifica):** los fixtures codifican el contrato CORREGIDO, NO
     debilitados para pasar; y el CODIGO DE PRODUCTO queda BYTE-IDENTICO en esta parte (es
     arreglar el test, no mover la porteria).
2. **UI PER-ITEM (study-critica, ESTE si es cambio de producto adjudicado):** reemplaza el
   checkbox global que auto-genera las 13 confirmaciones por **confirmacion POR ITEM** en el
   wizard Y en la revision de candidatas, fiel a SPEC-AEGIS-1001 s.7. La aprobacion global
   confirma SOLO el item `aprobacion`; cada obligatorio se confirma con su tick por-item. El
   checkbox global es el rubber-stamp que el producto anti-vibecoding existe para IMPEDIR
   (DECISION-1001 s.2). Si hay friccion de UX, resuelvela con diseno (revelado progresivo),
   NUNCA auto-confirmando. Los estados por item ya son honestos en el motor (b870af5+): esto
   alinea la SUPERFICIE con el motor.

## TASK-1104 (drift trailers, prerequisito de test:ci verde)
`buildAutoCommitMessage` (src/server.js ~2982-2985) emite auto-commits sin Task-Id; el gate de
trailers del hub aterrizo hoy -> test:ci inalcanzable-verde para CUALQUIER commit del producto.
Emite Task-Id en la seccion final de trailers (TASK-XXXX o `Task-Id: none` + `Ops-Reason` para
coordinacion), mismo parrafo que Co-Authored-By sin blank line (gotcha F-0240-01). Sin Fixes-Task
salvo subject fix/revert/hotfix.

## Gate de cierre
`npm run test:ci` VERDE por exit-code en clon limpio (cubre ambas tareas). Re-gate adversarial
final corre sobre tu commit; con las 2 verdes -> ratifico review_approved + done-flip.
NO borres mensajes de open/ (el Arquitecto archiva).
