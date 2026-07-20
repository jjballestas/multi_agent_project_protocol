---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-TASK-0268-fix-docs-H1
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
requested_action: "Remediar H1 de TASK-0268 (docs-only, veredicto Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md): README_INSTANCIACION.md afirma que todo commit materializa el snapshot staged, pero el default acotado NO materializa (inspecciona el arbol; solo el flag y el CI dan esa garantia). Corregir la(s) frase(s) para que digan la verdad del reparto E6-A (default acotado = chequeos baratos sobre el arbol; garantia staged = flag explicito o CI). NO tocar hook ni pin CI. Re-entrega minima a in_review para re-juicio de lectura del checker."
question: "ETA del fix docs H1 (deberia ser minutos)?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md
  - Area_comun/tasks/TASK-0268-d0103-e6-reparto-coste-acotado-local.md
one_line_summary: "ACTION H1 docs-only de 0268 (1-2 frases del README: el default acotado no materializa; la garantia staged vive en flag/CI): funcional todo PASA (0.455-0.483s default real; v2 intacta bajo flag). Tras re-juicio: cadena de cierre de la tanda."
---

# ACTION TASK-0268 - H1 docs-only

Hora local: 2026-07-20 06:06. El checker dio CAMBIO-REQUERIDO acotado a documentacion:
el README promete al adoptante una garantia ("todo commit materializa el snapshot
staged") que el reparto E6-A entrega solo bajo flag o en CI. Tu entrega funcional paso
entera con sus mediciones reproducidas. Corrige el texto para que describa el reparto
REAL y re-entrega; el re-juicio es de lectura (rapido). Cobertura E1: mismo acceptance
(punto de docs del reparto), unidad padre TASK-0268.

Los 5 residuales no bloqueantes del artefacto (R1-R5) quedan registrados; no los
toques en esta remediacion.

Disciplinas: claim CLAIM- mayusculas; idempotency_key fresco + tail; trailers
Task-Id: TASK-0268 (fix( exige Fixes-Task: TASK-0268); 4 gates por exit code real.
