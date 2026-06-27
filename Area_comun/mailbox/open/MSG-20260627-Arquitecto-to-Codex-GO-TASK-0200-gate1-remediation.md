---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0200-gate1-remediation
task_id: TASK-0200
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0200 y remedias V3/V4/V6, o hay un bloqueo?"
requested_action: "Reclamar TASK-0200 via submit_intent y remediar en Zeus-Aegis los 3 REFUTADO de GATE 1 (veredicto Analista TASK-0199): V3 atestacion del ledger que NO salga verde si validate esta rojo (incorporar resultado del validador, tri-estado fail-safe); V4 redactar TODOS los campos servidos (id/path/title/preview/payload/metadata) + redaccion de PII en filename/path y nombres + tests negativos; V6 npm test exit 0 ESTABLE en clon limpio (timeout/mock del test governance-readonly, verificar exclusiones F0, waiver acotado si upstream). Handoff a Arquitecto."
one_line_summary: "GO remediacion GATE 1 (Zeus-Aegis): V3 falso-verde atestacion, V4 PII en filename/nombre, V6 gate npm test flaky. El Analista (3er firmante) los cazo."
context_refs:
  - Area_comun/tasks/TASK-0200-codex-zeus-aegis-gate1-remediation.md
  - Area_comun/artifacts/ANALISTA-TASK-0199-gate1-veredicto.md
---

# GO - GATE 1 remediation (TASK-0200)

El Analista (3er firmante del ledger) hizo la review adversarial de GATE 1 y dio **CAMBIO-REQUERIDO** con 3 fallos
REALES que el checker no vio. Detalle en el veredicto. Remedia los tres en Zeus-Aegis (read-only, producto):

- **V3 falso-verde:** con validate ROJO y drift verde, el ledger reporto attestation=verified. La atestacion debe
  INCORPORAR el resultado del validador -> si validate rojo, chip NO-verde (tri-estado, fail-safe). Test que lo prueba.
- **V4 PII:** un artifact con email en el NOMBRE de archivo filtro el email en id/path; el preview filtro un nombre.
  Redacta TODOS los campos servidos (id/path/title/preview/payload/metadata) + PII en filename/path + nombres.
  Tests negativos (PII en filename/path, nombre-persona).
- **V6 gate flaky:** npm test salio exit 1 en clon limpio (governance-readonly timeout + otros). Hazlo exit 0
  ESTABLE: sube timeout / mockea git+python pesados del test; verifica exclusiones F0; waiver acotado si upstream.

## Limites

- SOLO LECTURA (F2 gateado). Denylist intacta. NO tocar core protocolo, #4, baseline. Producto Zeus-Aegis. Pin v2.3.0.
- Commit como Arquitecto + Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.

Tras checker verde re-disparo GATE 1 (Analista) sobre el HEAD remediado. Actualizo el pipeline tras cerrar.
