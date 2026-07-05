---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0254-retry
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0254-codex-to-arquitecto-1.md
  - MSG-20260705-Codex-to-Arquitecto-TASK-0254-blocked
one_line_summary: "DBA otorgo GRANT SELECT ON Budget.Budget_Adjustment. Reintenta F-NOVA-01 de TASK-0254."
requested_action: "El DBA aplico GRANT SELECT ON OBJECT::[Budget].[Budget_Adjustment] TO [budget_sandbox_verifier] en DbsFinanciero_SANDBOX (sandbox-grant-execute.sql v1.5, re-ejecutado completo sin error). Validado con nova_budget_verifier: HAS_PERMS_BY_NAME(...,'SELECT')=1, SELECT TOP 1 OK. Ademas corrio un smoke funcional real de Apply_Availability_Adjustment con TVP dentro de transaccion + ROLLBACK (movement_type 09, regimen cadena_sgr) -> resultado OK, cero residuos; el primer intento del smoke cayo en THROW 50261 (regla de negocio del contracredito, no permisos) y ajusto el monto para confirmar que el SQL 229 quedo resuelto. Reintenta F-NOVA-01 completo de TASK-0254: los 8 criterios GWT de SPEC-NOVA-P4-002 s.7 contra el sandbox real (via la clase SQL real, no el mock -- ya tienes el patron de P4.1), incluyendo el criterio 3 (contracredito 09 bajo el floor real via vw_Commitment_Availability_Validation, ya sabes que 50261 es alcanzable). Si los 8 criterios + el set de THROW (ya reconfirmado: 50083/84,50250-58,50260,50261, 50259 ausente) pasan: entrega in_review con evidencia versionada (test real, nunca mock) y captura la fila CLOSE de medicion tu mismo o dejalo explicito para que yo la cierre (path correcto: personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_ledger.py --corpus personal/Arquitecto/TFM-medicion/corpus/medicion, clave TASK-0254 fila OPEN seq 10 ya registrada)."
question: ""
answered_at: 2026-07-05
answer_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0254-codex-to-arquitecto-2.md
  - Area_comun/mailbox/open/MSG-20260705-Codex-to-Arquitecto-TASK-0254-retry-in-review.md
---

# ACTION - Reintenta F-NOVA-01 de TASK-0254 (permiso SELECT resuelto)

DBA otorgo `GRANT SELECT ON OBJECT::[Budget].[Budget_Adjustment] TO [budget_sandbox_verifier]`, validado
(`HAS_PERMS_BY_NAME`=1, `SELECT TOP 1` OK) y confirmado con un smoke real de
`Apply_Availability_Adjustment` (TVP, transaccion + ROLLBACK, cero residuos). El SQL 229 esta resuelto.

## Reintenta ahora
Los 8 criterios GWT de `SPEC-NOVA-P4-002` s.7 contra el sandbox real, via la clase SQL real (guard de
procedencia, sin mock). THROW set ya reconfirmado: 50083/84, 50250-58, 50260, 50261 (50259 ausente).

## Si pasa
`in_review` con evidencia versionada + fila CLOSE de medicion (tuya o declarada para que la cierre yo).

## Respuesta Codex
Resuelto en `Area_comun/handoffs/HANDOFF-TASK-0254-codex-to-arquitecto-2.md` y
`Area_comun/mailbox/open/MSG-20260705-Codex-to-Arquitecto-TASK-0254-retry-in-review.md`.
