---
spec_id: SPEC-0099
task_id: TASK-0186
type: feature
status: accepted
linked_decisions:
  - DECISION-0062
  - DECISION-0050
  - DECISION-0040
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0099 - Consola del Arquitecto pieza 2: UI conversacional + streaming en el front

## Context

DECISION-0062 (accepted) + pieza 1 cerrada (TASK-0185/SPEC-0098): el proceso-puente ya expone
`/api/protocol/architect-bridge` (status/open/send/stop/stream-SSE), off-by-default, no-bypass, runtime-only,
sesion unica, con streaming + redaccion PII. **Pieza 2 = la UI** en el front (Zeus-protocol): una vista
conversacional Operador<->Arquitecto que consume esos endpoints. maker=Codex / checker=Arquitecto. Repo = Zeus.

## Scope

- **Vista "Consola Arquitecto"** en el front (nav-item routeado): caja de conversacion (mensajes del operador +
  salida del Arquitecto en streaming), control de abrir/estado/**finalizar** sesion, indicador de estado del
  puente (alive/dormant/disabled) DERIVADO del `status` real.
- **Transporte de streaming** en el cliente: consume el SSE de `/api/protocol/architect-bridge/stream` y renderiza
  incrementalmente; enviar mensaje via `/send`; finalizar via `/stop`; estado via `GET`.
- La UI llama **SOLO** a los endpoints gobernados del puente; sin nueva ruta de escritura al ledger/estado.

## Acceptance Criteria

- **AC1 (vista routeada + conformidad-diseno) [PERMANENTE; SPEC-0086 AC12/AC13]:** la consola es un nav-item que
  renderiza SOLO su vista (routing real, no scroll); existe y respeta el design-system. Test de comportamiento de
  routing.
- **AC2 (solo endpoints gobernados, no-bypass):** la UI interactua exclusivamente con
  `/api/protocol/architect-bridge` (status/open/send/stop/stream); NO escribe estado/ledger ni abre rutas nuevas.
  Test: el cliente no tiene `writeFile`/llamadas directas al ledger; toda accion pasa por los endpoints del puente.
- **AC3 (estado honesto regresion-proof) [PERMANENTE; SPEC-0086 AC11]:** el indicador de estado (alive/dormant/
  disabled) se DERIVA del `status` real del puente; con el puente **disabled** (off-by-default) la consola muestra
  "no disponible/desactivada", NUNCA una consola fantasma activa. Test de comportamiento: disabled -> UI honesta.
- **AC4 (sesion + finalizar):** la UI refleja la sesion unica (abrir reusa la viva) y ofrece **finalizar**; tras
  finalizar, el estado pasa a dormant y la UI lo refleja. Test de comportamiento.
- **AC5 (streaming + guarda PII):** la salida en streaming se renderiza incrementalmente; la UI no introduce fuga
  de PII (el stream ya viene redactado del servidor; el render no la reconstruye). READ-ONLY sobre el trabajo.
- **AC6 (gates):** `npm test` (gate rapido) verde + el/los casos en el tier CI (`npm run test:ci`); protocolo
  `validate_collaboration_state.py` exit 0 (con/sin secretos), drift 0, scan_encoding/neutrality exit 0;
  `protocol.config.json`/genesis intactos; Co-Authored-By Codex.

## Out of scope

- Cambios al proceso-puente (pieza 1, cerrada) salvo ajustes menores justificados de contrato cliente<->endpoint.
- Auditoria endurecida (pieza 3); consolas para Codex/Analista; NOVA; multi-tenant; alta/baja de agente (RF-9).
- Cualquier escritura directa al ledger desde la consola (prohibida por invariante DECISION-0062).

## Notes

- La consola es la cara de usuario del puente: muestra y dirige, no actua por el Arquitecto (toda mutacion sigue
  por submit_intent, via el trabajo del propio Arquitecto). Off-by-default lo gatea el puente (pieza 1).
- Repo producto Zeus-protocol; clon en Windows: `git -c core.longpaths=true`.
