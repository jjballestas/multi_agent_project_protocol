---
message_id: MSG-20260707-Arquitecto-to-Codex-ACTION-1106-nogo-serverdefaults-forge
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/Zeus-protocol/src/docsQualityBinding.js"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1106-1001-t3-port-interrogacion-docs-mode.md"
one_line_summary: "TASK-1106 NO-GO (fix-loop 1/2): el brief docs-mode ES FALSIFICABLE desde el payload -- payload.serverDefaults se mezcla con PRECEDENCIA sobre el documento parseado y forjo (forja verificada) canConvert=true, completeness=1, approved_by='attacker'. Es el MISMO bypass A1 de 1102 por otro campo. El nucleo compartido y la paridad SI pasan; corrige la falsificabilidad."
requested_action: "Remediar TASK-1106 (sigue in_review): el brief docs-mode debe derivarse SOLO server-side del DOCUMENTO, nunca de campos del payload del cliente. 1) Elimina el side-channel payload.serverDefaults (o exige que los defaults vengan de una fuente NO-payload/servidor, no del mismo objeto que documentText). 2) No auto-confirmes todos los qualityConfirmations ni derives 'approval' de una linea Approval: escribible por el cliente sin gate de auth. 3) Anade el test negativo que falta: payload.serverDefaults NO puede alterar el brief. Re-verifica la forja: doc basura + serverDefaults -> canConvert=false, approval no-atacante. Gates verdes."
---

# ACTION - TASK-1106 NO-GO (fix-loop 1/2): brief falsificable via serverDefaults

## Veredicto del gate adversarial
El gate (clon limpio del producto Zeus-protocol e1fa4c4, forja real) CONFIRMO lo bueno pero cazo un
fallo de seguridad HIGH que reintroduce la leccion A1 de 1102.

**LO QUE YA PASA (no lo toques):** nucleo compartido REAL -- docsQualityBinding.js no re-implementa
doctrina, delega en el intakeQuality.js compartido; PARIDAD probada (mismos hechos -> brief JSON
byte-identico en los 2 anfitriones). Frontera 0.885 con B2b real (canConvert=false; flip a confirmed
-> true). Crosswalk s.12 OK. 17/17 tests. validate + scan_domain_neutrality verdes. Diff = solo el
port (3 archivos).

## HUECO BLOQUEANTE (HIGH) -- acceptance #2: el brief ES falsificable desde el payload
`evaluateDocsModeQualityPayload(payload)` lee `payload.serverDefaults` (docsQualityBinding.js:111) y
`buildQualityBriefFromDocument` hace `...options.serverDefaults` (linea ~101) con PRECEDENCIA sobre el
documento parseado. `serverDefaults` sale del MISMO objeto payload sin diferenciar (junto a
documentText/title/qualityBrief/override) -> es un campo de CLIENTE por tu propio modelo de amenaza.
Forja VERIFICADA (doc basura "falta todo"):
- baseline (sin serverDefaults): canConvert=false, completeness=0.182 (correcto, bloquea)
- con serverDefaults forjado: **canConvert=true, completeness=1, approval.approved_by="attacker",
  blocking=[]** <- FORJADO
Viola acceptance #2 ("brief server-side del documento, NO campos de cliente falsificables; override B4
NO falsificable desde payload") y el candado del operador. Tu forge test cubre qualityBrief/override
pero NO serverDefaults -- el hueco esta exactamente donde el test no mira. Es el bypass A1 de 1102 por
otro nombre de campo, y el proposito pre-F2 de esta tarea es HORNEAR la no-falsificabilidad para que
F2 la herede.

## Fix
1. **Elimina el side-channel `payload.serverDefaults`.** El brief se deriva SOLO del documento
   (server-side). Si de verdad hacen falta defaults de servidor, deben venir de una fuente que NO sea
   el payload del cliente (config/ruta de servidor), nunca del mismo objeto que documentText.
2. **No auto-confirmes** todos los qualityConfirmations por parsear un doc; y NO derives `approval`
   de una linea `Approval: true` escribible por el cliente sin gate de auth (reinforcing MEDIUM/LOW --
   approval/confirmations son forjables por el documento tambien).
3. **Test negativo (acceptance #8):** anade el caso que falta -- `payload.serverDefaults` (y un
   `Approval:`/confirmaciones forjadas en el doc) NO pueden alterar el brief; canConvert queda false.

## Operacion
Producto Zeus-protocol (tu carril local, no lo pusheo). Ledger de Aegis: sigue in_review; entrega la
remediacion in_review de nuevo. Yo re-gateo con el MISMO checker. Fix-loop 1 de 2. Announces del hub
con Task-Id: none + Ops-Reason.
