---
message_id: MSG-20260629-Arquitecto-to-Analista-GO-TASK-0215
task_id: TASK-0215
type: GO
from: Arquitecto
to: Analista
status: open
requires_response: true
response_owner: Analista
question: "Tras tu pasada adversarial V1-V6 sobre TASK-0213 (ceremonia atestada): CERRABLE o CAMBIO-REQUERIDO?"
requested_action: "Reclamar TASK-0215 via submit_intent (claim ACQUIRE firmado Ed25519). Revisar adversarialmente en clon limpio el commit d2d19e2 (scripts/keygen_agent.py + new_instance.py --tier attested + test_attested_instancing.py): V1 secretos no se imprimen/commitean/filtran, V2 worker keyless no escribe el ledger bajo enforce (forja/atribucion-cruzada fail-closed), V3 clon SIN secretos verifica via publicas y no puede firmar, V4 guardrail (pineados del hub byte-identicos), V5 genesis sano/enforce-off, V6 neutralidad. Entregar artefacto Area_comun/artifacts/ANALISTA-TASK-0215-veredicto.md + MSG REVIEW al Arquitecto, commit como autor Analista, y RELEASE del claim. NO toques task_status."
one_line_summary: "Review adversarial de la ceremonia de instanciacion atestada (keygen/firma/secretos/guardrail). Busca el secreto filtrado, la forja del worker y el falso-verde."
context_refs:
  - Area_comun/tasks/TASK-0215-analista-review-0213-attested-ceremony.md
  - Area_comun/tasks/TASK-0213-codex-instancing-attestation-ceremony.md
  - Area_comun/decisions/DECISION-0069-instancing-attestation-ceremony.md
---

# GO - Review adversarial de TASK-0213 (ceremonia atestada)

Codex entrego TASK-0213 (commit `d2d19e2`): keygen por firmante + `new_instance.py --tier attested --roster` +
golden. Implementa DECISION-0069. Checker (Arquitecto) ya verifico pineados del hub byte-identicos (guardrail OK) y
golden PASS. Por ser sensible a seguridad, el operador pidio tu pasada adversarial.

## Eres el 3er firmante -- entrega via LEDGER
Reclama TASK-0215 con submit_intent (claim ACQUIRE Ed25519 -> tu firma entra al corpus). Veredicto como artefacto +
MSG, commit como autor Analista, libera el claim. NO toques task_status.

## Vectores calientes (intenta REFUTAR)
- **V1:** que un SECRETO (privada PEM/HMAC) se imprima, se commitee o se filtre fuera de `protocol-secrets/`.
- **V2:** que un WORKER keyless ESCRIBA el ledger bajo enforce (forja/atribucion cruzada) -> debe fail-closed.
- **V3:** clon SIN secretos: verifica via publicas (exit 0) pero NO puede firmar; busca un falso-verde.
- **V4:** que algun camino TOQUE los pineados del hub (eventlog.py/validador/config/override).

Detalle V1-V6 en la tarea. ASCII-only (corre scan_encoding antes de commitear). Minimal narration.
