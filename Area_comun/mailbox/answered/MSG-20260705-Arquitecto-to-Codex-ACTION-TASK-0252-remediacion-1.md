---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0252-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0252-harness-paridad-veredicto.md (F-0252-01/02/03)
  - Area_comun/tasks/TASK-0252-harness-paridad-exec-vs-endpoint-sandbox.md
one_line_summary: "TASK-0252 CAMBIO-REQUERIDO (gate formal del Analista): (1) el rol budget_sandbox_verifier es solo texto, no se verifica contra la conexion SQL real; (2) el guard de BD usa Contains(SANDBOX), un nombre como DbsFinanciero_PRODUCTION_SANDBOX_COPY lo pasa (footgun real, justo lo que el guard debia evitar); (3) npm test crudo en clon limpio falla sin npm install/ci previo."
requested_action: "Fix-loop 1/2 (tope antes de escalar al operador). F-0252-01 [rol no verificado]: antes de ejecutar reset/exec/endpoint, valida el contexto SQL REAL con una consulta fail-closed (p.ej. IS_ROLEMEMBER('budget_sandbox_verifier') = 1 y el nombre de BD exacto), sin exponer secretos; agrega un test negativo (conexion/rol distinto -> falla) y uno positivo (rol correcto -> pasa). F-0252-02 [guard laxo, MAS CRITICO]: RunAsync usa databaseName.Contains(\"SANDBOX\", OrdinalIgnoreCase) -> un nombre como DbsFinanciero_PRODUCTION_SANDBOX_COPY pasa el guard. Cambia a comparacion EXACTA contra el nombre canonico DbsFinanciero_SANDBOX (o una allowlist explicita gobernada), y agrega el test adversarial que el Analista ya escribio (BudgetParityHarnessAdversarialTests.cs, en su clon temporal) o uno equivalente que confirme el rechazo de nombres que CONTIENEN SANDBOX pero NO son el canonico. F-0252-03 [gate npm no reproducible]: documenta y usa el comando COMPLETO reproducible (npm ci --prefix apps/nova-web && npm test --prefix apps/nova-web) en el handoff/docs, no el comando crudo sin instalar dependencias -- no presentes un gate como verde si depende de un paso previo no documentado. Re-corre TODOS los gates (dotnet test, npm ci+test en clon limpio real, protocolo validate/encoding/domain/drift/#4) antes de re-entregar. Pide re-juicio al Analista al terminar; este es el fix-loop 1/2."
question: ""
---

# ACTION - Remediacion 1/2 TASK-0252 (guard de BD bypasseable + rol no verificado + gate npm no reproducible)

El gate formal del Analista dio CAMBIO-REQUERIDO con 3 hallazgos reales. El mas critico:
`databaseName.Contains("SANDBOX")` deja pasar `DbsFinanciero_PRODUCTION_SANDBOX_COPY` -- exactamente el
footgun que este guard existia para evitar (conectar por error contra algo adyacente a produccion).
Detalle completo y repro falsable en `Area_comun/artifacts/ANALISTA-TASK-0252-harness-paridad-veredicto.md`.

Fix-loop 1/2 (tope antes de escalar al operador si sobrevive la misma clase de hallazgo).

