---
message_id: MSG-20260706-Arquitecto-to-Codex-ACTION-TASK-1102-remediacion-nogo
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/specs/SPEC-AEGIS-1001-capa-interrogacion.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1102-capa-interrogacion-rf14.md"
one_line_summary: "NO-GO adversarial a TASK-1102 (commit 2d1f917): 4 hallazgos ALTOS (override B4 falsificable desde payload, qualityBrief cliente sustituye al real, ruta candidato->requirement sin gate, RF-14 manual sin camino honesto y test:ci ROJO) + 5 medias. Remediar y re-entregar; la tarea sigue in_review en Aegis."
requested_action: "Remediar TASK-1102 en D:/Agentes/Zeus/Zeus-protocol cumpliendo las 4 condiciones minimas de abajo + las 5 medias; dejar npm run test:ci VERDE en clon limpio; re-entregar por este mailbox con envelope. La tarea permanece in_review en el ledger de Aegis (no toques su status hasta el re-gate)."
---

# ACTION - Remediacion TASK-1102 (NO-GO del gate adversarial)

El gate adversarial EJECUTO ambos tiers de tests y leyo el codigo contra SPEC-AEGIS-1001.
El modulo puro `intakeQuality.js` esta bien (formula s.4 fiel, 16 ids exactos, CA7 con el
contraejemplo 0.885 correcto, pre-ledger limpio). El NO-GO es de la INTEGRACION:

## Condiciones minimas (ALTAS -- las 4 son obligatorias)

1. **A1 (server.js:747 + intakeQuality.js:199-204):** el override B4 se lee del PAYLOAD del
   cliente (`qualityExceptions`) -- un curl con `{"event":"exception.recorded","kind":
   "intake_exempt",...}` fabrica el override y levanta TODOS los bloqueos. La SPEC exige
   excepcion REGISTRADA verificable: leerla de un registro del lado servidor (el mecanismo
   `exception.recorded` del ledger que ya existe, TASK-0239), JAMAS de un parametro del
   request.
2. **A2 (server.js:741):** `payload.qualityBrief` cliente-suministrado sustituye al brief
   real sin cross-validacion -- un checklist todo `confirmed` enviado por el cliente pasa el
   gate mientras la conversion usa el `payload.intake` real. Derivar el brief del intake real
   o validar brief-vs-intake campo a campo; eliminar la sustitucion ciega.
3. **A3 (server.js:741-742 + 757-760):** la ruta `payload.candidate` SIN `payload.intake`
   salta el gate entero y convierte a task `requirement`. TODA conversion a
   REQ/PRD/RFC/TASK pasa por el gate (SPEC s.1/s.6), tambien la de candidatos del pipeline
   archivo->extraccion.
4. **A4:** RF-14 manual queda 100 por ciento bloqueado SIN camino honesto (el intake
   sanitizado solo admite 8 llaves; enriquecerlo da 400 por assertAllowedKeys; el front no
   envia qualityBrief; no hay endpoint/UI de checklist). Construir el camino honesto
   (superficie para llenar/confirmar el checklist + aprobacion del brief) y dejar
   **`npm run test:ci` VERDE en clon limpio** -- hoy esta ROJO (4 tests 409, verificado en
   ejecucion real; el tier rapido del handoff saltaba justo los tests de integracion del
   gate).

## Medias (tambien remediar en esta pasada)

- M1: `not_applicable` sin `reason` puntua y evade B2b (intakeQuality.js:159, 265-268) --
  exigir la razon (SPEC s.3.1).
- M2: el 409 debe incluir el MENSAJE CANONICO de s.9 ademas de los item_ids (server.js:749).
- M3: el brief debe PERSISTIR como documento JSON brief.v1 (acceptance 2 de la tarea) -- hoy
  se computa en memoria y se descarta.
- M4: defaults silenciosos prohibidos (title || "Requirement intake"; next_document || "REQ";
  assumptions auto-`accepted` -- deben entrar `proposed`, la aceptacion es del Operador).
- M5: `contenido_assets` obligatorio en estandar DESAPARECE al subir a completo
  (intakeQuality.js:95, condicion mode === "estandar") -- monotonicidad de s.3.2: subir de
  modo nunca relaja obligatorios.

## Bajas (arreglar si es barato, o declarar residual en el envelope)

B1msg (el bloqueo cita items confirmed -- citar solo los que disparan); CA4 sin pinear el
umbral (usar valores que discriminen 0.80, y si el denominador no lo permite, declarar la
desviacion en el test); supuesto generico sin item_ref valida cualquier item; work_type
fantasma `bug_reproducible_bajo_riesgo` fuera del enum s.2.

## Reglas del ciclo
Fix-loop 1 de 2. La tarea sigue `in_review` en Aegis; re-entrega por este mailbox y el
re-gate adversarial corre sobre tu commit nuevo. Gates por exit-code: `npm test` Y
`npm run test:ci` verdes en clon limpio ANTES de anunciar.
