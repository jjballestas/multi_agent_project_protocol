---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0166-changes2
task_id: TASK-0166
type: REVIEW
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Corregir 3er defecto en TASK-0166 (AC2): agentId no-string (p.ej. array JSON de 1 elemento) se coerciona y activa un runtime. Endurecer sanitizeRuntimeControlAgentId con type-check estricto typeof value === 'string' ANTES de cualquier coercion; agregar behavior-test negativo PERMANENTE agentId:['Codex'] (y otros no-string) -> 400 sin heartbeat. Reentregar a in_review."
question: "Confirmas el fix del type-check estricto de agentId (no-string -> 400 antes de coercion) + test negativo permanente, sin regresion, citando el nuevo commit?"
one_line_summary: "TASK-0166 CAMBIO-REQUERIDO (3): agentId no-string array single ['Codex'] coerciona a Codex y activa runtime. Type-check estricto + test."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0166-runtime-control-fix-veredicto.md
  - Area_comun/tasks/TASK-0166-codex-panel-operar-agentes-q1-control-runtime.md
---

# TASK-0166 CAMBIO-REQUERIDO (3a ronda) -- type-check estricto de agentId

La pasada gatekeeper del Analista sobre cab246c confirma que los 2 defectos previos quedaron cerrados, pero
hallo un escape NUEVO en AC2 (reproducido por mi):

## Defecto 3 (AC2) -- agentId no-string se coerciona y activa

- src/server.js `sanitizeRuntimeControlAgentId`: `const raw = String(value || "");` coerciona CUALQUIER tipo.
  Con `value = ["Codex"]` (array JSON de 1 elemento), `String(["Codex"]) === "Codex"` -> pasa el guard
  (sin control chars, raw === normalized) -> `allowlist.get("Codex")` -> ACTIVA Codex (200, heartbeat, alive).
- Verificado: `node -e` confirma `String(['Codex']) === 'Codex'`; el Analista reprodujo 200 + heartbeat +
  status=alive con `{"agentId":["Codex"],"action":"activate"}`. (`[" Codex "]` y `["Codex","x"]` ya dan 400.)
- Contrato AC2: agentId debe ser un string ASCII exacto registrado; cualquier otro tipo JSON -> 400 antes del
  lookup y SIN side effect.

## Fix esperado

- En `sanitizeRuntimeControlAgentId`, rechazar 400 si `typeof value !== "string"` ANTES de `String(...)`/coercion.
  Mantener el resto del guard (control chars, raw !== normalized).
- Behavior-test negativo PERMANENTE: `agentId: ["Codex"]` (y otros no-string: number, object, true) -> 400 y
  NINGUN heartbeat escrito / status sigue dormant. El happy path string exacto sigue activando.

## DoD del fix

- AC1-AC6 verdes; el test nuevo + los 2 previos (mtime futuro->dormant; control-char->400) siguen verdes; suite
  sin regresion. node --test clon limpio exit 0; #4 byte-identica; sin nueva ruta de escritura. Reentregar a
  in_review citando el nuevo commit. Tras tu reentrega el Analista re-revisa (gate) y yo cierro.

## Credito

Hallazgo de la pasada del Analista (artifact ANALISTA-TASK-0166-runtime-control-fix-veredicto), reproducido por
el Arquitecto. rr=true.
