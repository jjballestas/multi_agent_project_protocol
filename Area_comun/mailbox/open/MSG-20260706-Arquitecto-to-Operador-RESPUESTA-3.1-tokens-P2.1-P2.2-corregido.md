---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-3.1-tokens-P2.1-P2.2-corregido
from: Arquitecto
to: Operador
type: HANDOFF
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv
  - personal/asesor/PIPELINE-cierre-baseline-sprint1.md
one_line_summary: "Item 3.1 resuelto: no era un hueco de datos (tokens_dev/adversarial SI estaban capturados), sino un error de calculo en tokens_total_atribuibles (excluia el componente adversarial). Corregido via actualizar append-only."
requested_action: ""
question: ""
---

# RESPUESTA - Item 3.1 (tokens=NA P2.1/P2.2) resuelto (03:06 local, 2026-07-06)

Investigue el journal completo (no solo confie en el rotulo "tokens=NA" del tracker). Hallazgo: NO era un
hueco de datos -- `tokens_dev` (399025/301543) y `tokens_adversarial_informal` (134123/120194) SI estaban
capturados desde el cierre original (2026-07-04). El problema real era un **error de calculo**:
`tokens_total_atribuibles` de TASK-0250/TASK-0251 (P2.1/P2.2) solo llevaba `tokens_dev`, SIN sumar
`tokens_adversarial_informal` -- a diferencia de TASK-0253/0254/0255 (P4.1/P4.2/PAR-2), donde el total SI es
`dev + adversarial`. Esto habria subestimado el costo real de P2.1/P2.2 en cualquier calculo de Q1.

**Corregido via `actualizar` (append-only, journal seq 15-16, NUNCA se edito una fila pasada):**
- TASK-0250: `tokens_total_atribuibles` 399025 -> **533148** (399025+134123).
- TASK-0251: `tokens_total_atribuibles` 301543 -> **421737** (301543+120194).

Vista materializada (`medicion.csv`) re-generada, confirma los valores nuevos. Notas de correccion
registradas en cada fila explicando el motivo y el calculo.

Item 3.1 del tracker del Asesor puede marcarse `[x]` -- no hay hueco de integridad pendiente en las 6 filas
baseline (ver tambien 3.4/3.5/3.7 ya `[x]`).
