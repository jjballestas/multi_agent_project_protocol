---
message_id: MSG-20260706-Arquitecto-to-Codex-ACTION-TASK-1102-remediacion2-final
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/specs/SPEC-AEGIS-1001-capa-interrogacion.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1102-capa-interrogacion-rf14.md"
one_line_summary: "Re-gate de b870af5: NO-GO segunda vuelta PERO con A1/A2 RESUELTOS verificados. Quedan 4 condiciones CERRADAS y chicas (3 tests rojos deterministas de maker en test:ci, gate del candidato vacuo por auto-relleno, persistencia brief.v1 en cero, estados por item honestos). FIX-LOOP 2 DE 2: si no cierra, escala al operador."
requested_action: "Remediar las 4 condiciones de abajo en D:/Agentes/Zeus/Zeus-protocol y re-entregar. IMPORTANTE: tu stall de submit_intent NO se reprodujo en el re-gate (tests que a ti se te colgaron aca PASARON: intake 345s, ingestion 239s, mailbox 204s, contention 140s) -- los 3 rojos son assertions deterministas, no timeouts. NO borres mensajes de open/ (ver FYI de anomalia previo): dejalos, el Arquitecto archiva."
---

# ACTION - Remediacion 2 (FINAL) TASK-1102

## Verificado RESUELTO en b870af5 (no tocar)
A1 (override lee runtime/state/events.jsonl server-side, curl ya no fabricable), A2 (brief
solo server-derived), M1 (n/a exige razon), M2 (mensaje canonico en el 409), M5
(monotonicidad), M4 parcial (title 400, next_document, assumptions proposed).

## Condiciones para GO (las 4, cerradas)

1. **Mismatch approval front/fixture (fallos 1 y 2 de test:ci):**
   `buildRequirementIntakePayload` (public/app.js) solo respeta `draft.approval === true`;
   los tests `test harness isolates runtime config env...` (staticContract.test.js:1430) y
   `Enviar al Arquitecto adds governed mailbox notice...` (:1943) pasan `validIntake()` con
   approval OBJETO {approved_by, at} -> se aplana a null -> 409 donde se asserta 200.
   Acepta el objeto en el builder (o normaliza en un solo punto). Fix de lineas.
2. **Gate del candidato REAL, no vacuo (fallo 3 + A3 parcial):**
   `buildCandidateRequirementIntake` (server.js:1744-1752) AUTO-FABRICA objective/
   verification/scope/audience/techConstraints con constantes y hasta la approval ->
   completeness 1.0 por construccion (gate sin dientes) y, cuando el texto escala a modo
   completo (hit `datos`), fuera_alcance/riesgos quedan missing SIN superficie para
   completarlos (candidatos con texto sensible mueren sin camino). Arregla en esta
   direccion: estados DERIVADOS del contenido real del candidato (lo ausente = missing
   VISIBLE), superficie en la revision de candidatos para completar los items faltantes
   antes de aprobar, y approval JAMAS fabricada server-side. Nada de constantes.
3. **Persistencia brief.v1 (acceptance 2; hoy es CERO -- el renderer quality_brief es
   codigo muerto sin escritores):** persiste el brief como documento JSON en el store de
   archivos del propio anfitrion RF-14 (Zeus-protocol ya persiste artefactos de intake;
   es pre-ledger, permitido por SPEC s.7 "persistencia del brief = anfitrion"). NO amplies
   el schema de task_upsert (eso si requeriria DECISION).
4. **Estados por item honestos + test:ci VERDE por exit-code en clon limpio:**
   `statusFromValue` auto-confirma TODO item lleno cuando hay approval global -> B1 y B2b
   quedan inalcanzables en el flujo real (solo viven en unit tests). Regla: item lleno SIN
   confirmacion explicita del usuario = `answered` (0.5); `confirmed` solo por tick por-item
   en el wizard (o el mecanismo honesto equivalente). La approval global satisface SOLO el
   item `aprobacion`. Y el gate de cierre: `npm run test:ci` VERDE en clon limpio -- tu
   stall de entorno no es excusa valida (aca no se reproduce).

## Bajas (si es barato; si no, declarar residual en el envelope)
qualityBrief como llave muerta en el allowlist; assumption aceptada sin item_ref valida
cualquier item (hasAcceptedAssumption linea 282); B1 cita items confirmed en el mensaje;
CA4 sin declarar la desviacion del umbral literal; modo rapido inalcanzable (mecanismo
s.3.2 muerto -- declara o habilita).

## Reglas del ciclo
FIX-LOOP 2 DE 2: si el re-gate vuelve NO-GO, el ciclo escala al operador con el historial
completo. La tarea sigue in_review en Aegis. Re-entrega por este mailbox con envelope.
