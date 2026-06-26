---
spec_id: SPEC-0102
task_id: TASK-0189
type: security
status: accepted
linked_decisions:
  - DECISION-0062
  - DECISION-0063
  - DECISION-0040
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0102 - Remediacion consola del Arquitecto: audit timestamp + cleanup del launcher

## Context

El SMOKE VIVO del Arquitecto (consola DECISION-0062/0063, piezas ya cerradas) destapo 2 defectos que los tests no
vieron (usaban stdin.end limpio + cwd=Zeus). Esta tarea los corrige. maker=Codex / checker=Arquitecto. Repo =
Zeus-protocol.

## Defectos a corregir

1. **Audit timestamp CORRUPTO (de TASK-0187/pieza 3):** el redactor PII se aplica a campos ESTRUCTURALES del audit
   y se come la FECHA -> `"timestamp":"[PHONE-REDACTED]T20:37:..Z"` (la fecha `2026-06-26` matchea la familia
   telefono). Evidencia: `.runtime/architect-bridge/sessions/<id>.jsonl` del smoke.
2. **Cleanup NO ROBUSTO del launcher (de TASK-0188/pieza 4):** tras `stop` del puente o muerte del parent, el
   **lock del launcher persiste** y quedan procesos **huerfanos** (el cleanup solo corre en cierre por stdin, no en
   SIGTERM ni cuando el puente mata el hijo). Riesgo: lock stale -> el proximo `open` no puede spawnear el launcher.

## Scope

- **Audit (server.js):** redactar SOLO los campos de TEXTO LIBRE del registro (p.ej. `text`/contenido del mensaje
  y de la salida); NUNCA los campos estructurales (`timestamp`, `sessionId`, `kind`, `stream`). El mismo principio
  para el streaming si aplicara (el stream ya conserva el timestamp; verificar).
- **Cleanup launcher (scripts/architect-runtime-launcher.mjs) + stop del puente (server.js):** el launcher remueve
  su lock y termina el inner ante **SIGTERM** y cierre de stdin (no solo stdin); el `stop` del puente termina al
  launcher de forma que dispare su cleanup (SIGTERM/graceful, con kill duro solo como ultimo recurso tras timeout) y
  garantiza que no queden inner huerfano ni lock stale.

## Acceptance Criteria

- **AC1 (audit estructural intacto, regresion-proof PERMANENTE):** tras enviar un mensaje con PII, el registro de
  audit conserva `timestamp` ISO valido (matchea `^\d{4}-\d{2}-\d{2}T...Z`), `sessionId`/`kind`/`stream` intactos, y
  el TEXTO sigue redactado por familias (sin literales PII). Behavior-test que asserta el timestamp NO redactado.
- **AC2 (cleanup del launcher robusto):** lanzar el launcher (stub inner) y enviarle **SIGTERM** -> remueve el lock
  y termina el inner (sin huerfanos); idem cierre por stdin (no regresion). Behavior-test.
- **AC3 (stop del puente sin huerfano ni lock stale):** open -> stop -> (a) no queda inner/launcher vivo, (b) el
  lock fue removido, (c) un `open` POSTERIOR vuelve a arrancar correctamente (no lo bloquea un lock stale).
  Behavior-test.
- **AC4 (sin regresion de invariantes):** no-bypass (no escribe ledger; no importa escritores), identidad existente,
  off-by-default, instancia unica, redaccion PII del contenido -> todo se mantiene verde.
- **AC5 (gates):** `npm test` (rapido) verde + casos en el tier CI (`npm run test:ci` en VENTANA QUIETA, 100% pass);
  protocolo validate exit 0 (con/sin secretos), drift 0, encoding/neutrality exit 0; `protocol.config.json`/genesis
  intactos; Co-Authored-By Codex.

## Out of scope

- Nuevas funciones de la consola; activacion viva real (paso del operador). Solo los 2 fixes + sus guardas.

## Notes

- Origen: hallazgos del smoke vivo (Arquitecto). El (2) es el mas serio para uso repetido (lock stale bloquea el
  proximo open). Repo Zeus; clon en Windows: `git -c core.longpaths=true`. Checker corre test:ci en ventana quieta.
