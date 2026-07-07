---
message_id: MSG-20260707-Arquitecto-to-Operador-RESPUESTA-pii-embeddings-formalizada
from: Arquitecto
to: Operador
type: RESPUESTA
status: open
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md"
one_line_summary: "Politica PII de embeddings FORMALIZADA como enmienda fechada 2026-07-07 de DECISION-1002 en el ledger de Aegis (commit 04a38ebf, llena el requisito s.6). Confirmado: F4 procede FTS-ONLY por default; embeddings OPT-IN solo bajo esta politica y necesidad concreta. No toca hub ni estudio medido."
requested_action: ""
---

# RESPUESTA - Politica PII de embeddings formalizada (enmienda DECISION-1002)

Confirmo la formalizacion. Los 6 puntos APROBADOS quedan como **Enmienda 2026-07-07 -- Politica PII de
embeddings (F4)** al final de `DECISION-1002` en el ledger de AEGIS (commit `04a38ebf`, pusheado,
validate + scan_encoding verdes). Llena el requisito ya nombrado en s.6 ("embeddings SOLO con politica
PII explicita"); es enmienda fechada, no reabre el resto de la decision.

Confirmado el regimen de F4:
- **FTS-only es el default de F4.** Los embeddings son **OPT-IN** y solo se activan bajo necesidad
  concreta, siempre sujetos a esta politica.
- Puntos duros que horneare como GATE de la tarea F4 que active embeddings: LOCAL-only (cero API
  externa), clasificar-antes-de-embeber (allowlist s.4b + content_sha256/redaction_state), texto libre
  **deny-by-default** (regex determinista fail-closed; pasar el regex NO auto-limpia; resumen
  estructurado o redaction cleared-por-humano como unicas vias), solo gobernanza/metodologia por ahora
  (producto con datos reales fuera hasta politica per-dominio + consentimiento legal), derivado/
  reconstruible/gitignored, y **golden test de PII plantada = 0 fugas** + test de no-embeber sin clear.

Nota de secuencia: F4 va DESPUES de 1001 t3-6 y de 1002 t5(pilot)/t6(runbook), segun tu rumbo
corregido. Cuando llegue F4, la SPEC de esa tarea citara esta enmienda como contrato de la parte de
embeddings. Nada de esto se activa antes; F4 arranca FTS-only.

No toca el hub ni el estudio medido; enmienda vive solo en el ledger de Aegis.
