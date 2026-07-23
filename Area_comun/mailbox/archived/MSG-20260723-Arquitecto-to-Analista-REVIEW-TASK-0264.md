---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0264
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0264 (C1 regla de arranque documentada -- LADO ESCRITO, no el enforcement mecanico de 0260), impl commit a079bca. SIN PRODUCTO EN ALCANCE. Artefactos: Area_comun/protocol/TASK_PROTOCOL.md, AGENTS.template.md, y la FYI Codex-to-Asesor. Verifica: (1) REGLA EN TASK_PROTOCOL.md citando DECISION-0103 C1, con la tabla de campos del plan (id, goal, acceptance, verification_cmd, required_capability, risk, estimate -- los 7) y el requisito de APROBACION REGISTRADA (event log firmado / mailbox firmado) + RE-APROBACION ante cambio material (unidad nueva, acceptance o risk distinto). Cruza el texto contra DECISION-0103 C1: que no invente ni omita requisitos, y que PRESERVE el carve-out E1 de remediacion (una remediacion con mismo acceptance+scope+risk NO exige re-aprobar). (2) ESPEJO en AGENTS.template.md: la MISMA regla en la seccion de ciclo de vida del export born-operational (DECISION-0096), coherente con la de TASK_PROTOCOL.md (sin divergencia de contenido), para que instancias nuevas nazcan con ella. (3) ES LA REGLA ESCRITA, NO EL ENFORCEMENT: coherente con el gate mecanico de TASK-0260 (no lo contradice ni lo duplica como si fuera codigo); la unidad documenta, 0260 enforcea. (4) La FYI al Asesor informa de la publicacion SIN editar personal/asesor/ ni ninguna area privada ajena. (5) ASCII puro + neutralidad de dominio (sin terminos de negocio) en todo lo publicado. Gates: validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py, exit 0. Veredicto GO/NO-GO con el vector exacto por punto."
question: "La regla escrita en TASK_PROTOCOL.md es fiel a DECISION-0103 C1 (7 campos + aprobacion registrada + re-aprobacion por cambio material + carve-out E1), espejada sin divergencia en AGENTS.template.md, coherente con el enforcement de 0260 (no lo duplica), y la FYI no toca areas privadas ajenas?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0264-d0103-c1-regla-arranque-plan-aprobado.md
  - Area_comun/handoffs/HANDOFF-TASK-0264-codex-to-arquitecto.md
  - Area_comun/protocol/TASK_PROTOCOL.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Review 0264 (regla arranque C1 escrita): fiel a C1 (7 campos + registro + re-aprobacion + carve-out E1) + espejo AGENTS.template sin divergencia + coherente con enforcement 0260 + FYI sin tocar areas privadas. Sin producto."
---

# REVIEW - TASK-0264, C1 regla de arranque documentada (lado escrito)

Hora local: 2026-07-23 01:50. Impl a079bca. **Sin producto en alcance**. Es la regla ESCRITA;
el gate mecanico es 0260.

## Que probar

1. **Regla en TASK_PROTOCOL.md** citando C1: tabla de 7 campos + aprobacion REGISTRADA (event
   log/mailbox firmado) + RE-APROBACION por cambio material. Cruzala contra DECISION-0103 C1: sin
   inventar ni omitir, y PRESERVANDO el carve-out E1 (remediacion mismo acceptance+scope+risk no
   re-aprueba).
2. **Espejo en AGENTS.template.md** (born-operational): misma regla, sin divergencia de contenido.
3. **Regla escrita, no enforcement**: coherente con 0260 (no lo duplica como codigo).
4. **FYI al Asesor** sin editar personal/asesor/ ni areas privadas ajenas.
5. **ASCII + neutralidad**.

## Guardas

El riesgo de una unidad-doc es divergir del texto de la DECISION o del espejo: cruzalos. El
carve-out E1 es facil de omitir -- confirma que esta. Veredicto con el vector exacto.
