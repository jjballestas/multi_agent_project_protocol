---
message_id: MSG-20260702-Operador-to-Arquitecto-ACTION-orden-F1-registro-backlog
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-02
context_refs:
  - personal/operador/vision-nova/F0/BACKLOG-F1-descompuesto.md
  - personal/operador/vision-nova/F0/SPEC-F1-gate-intake.md
  - personal/operador/vision-nova/F0/SPEC-F1-exception-trailers.md
  - personal/operador/vision-nova/F0/DIRECTIVA-OPERADOR-F0.1-20260702.md
  - Area_comun/decisions/DECISION-0083 (commit 0569f7b)
one_line_summary: "Orden F1: registra el backlog F1-A..G en el ledger (rama vision-nova), relanza los crons de peers y promueve F1-A tras la higiene de Codex."
requested_action: "Sobre la rama vision-nova: (1) registra el backlog F1 completo (7 tareas F1-A..G segun BACKLOG-F1-descompuesto.md, DoD tal cual; las 2 SPECs son la referencia de alcance de F1-A/B/C) como TASK-02xx con prefijo [VISION-NOVA][F1.x] + relates_to GOAL-VISION-NOVA-001, status proposed, owners segun el documento; (2) relanza los crons de Codex y Analista (GO del Operador incluido en esta orden); (3) el primer ciclo de Codex procesa su ACTION de higiene pendiente; recibido su FYI de higiene, promueve F1-A a ready + GO a Codex; (4) promocion DE A UNA segun la secuencia del documento: F1-A -> F1-B -> F1-C en la cadena de Codex; F1-D y la parte doctrinal de F1-E avanzan en paralelo sin bloquear esa cadena; F1-F y F1-G cierran la fase; (5) cada cierre con commit de paths explicitos + 3 gates por exit-code antes de pedir review; (6) actualiza el tablero (F1.x en_curso/hecho solo con evidencia + sello de hora); (7) FYI al Operador con ids de tareas registradas + commits."
question: "Confirmas registro del backlog + relanzamiento de crons + promocion de F1-A con un FYI que cite ids y commits?"
---

# ACTION - Orden F1: registro del backlog del nucleo doctrinal (v1.18.0)

Contexto: F0 esta CERRADA (directiva F0.1 emitida commit ee2963c; DECISION-0083 commit
0569f7b con re-alcances aplicados; tablero F0 = hecho). Arranca F1 = nucleo doctrinal
v1.18.0, ventana sem 1-2 (objetivo ~18-jul), dentro del gate duro Sprint 1 = 30-jul
(se recorta alcance, nunca la fecha).

Reglas de la fase:
- Todo ledger-op de F1 va sobre la rama vision-nova (igual que F0.2).
- Preflight skill arquitecto-ledger-ops en cada operacion; ASCII puro en mensajes.
- F1.6 (aprendizajes-externos, timebox 2d) SOLO si hay holgura; nunca camino critico.
- F1-G (release v1.18.0 + CHANGELOG + tag) es el cierre de fase: ese tag lo consume
  F2.1 (new_instance nova-budget).
- La cosecha gentle-ai nivel B (configs commiteadas, dry-run/write-atomico, prohibir
  gentle-ai install) NO va en F1: queda anotada en el backlog rumbo a la orden F2.

Acuse: el FYI de cierre de F0.2 (MSG-20260702-Arquitecto-to-Operador-FYI-F0.2-
DECISION-0083) queda ACUSADO por esta orden; puedes archivarlo como consumido en tu
proxima higiene de mailbox.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
