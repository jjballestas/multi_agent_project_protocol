---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0172-changes3
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Corregir el ANCHO de los textarea/campos de la tarjeta de candidata (feedback operador en prueba): la regla width:100% esta scopeada a `.intake-wizard textarea/select` (modales); la tarjeta `.candidate-card` NO esta cubierta, asi que sus textarea (rows=8 tras round 3) quedan al ancho default del navegador -> altos pero ESTRECHOS, desperdiciando el ancho. Fix en public/styles.css: `.candidate-card label { display:grid; gap }`, `.candidate-card textarea, .candidate-card input, .candidate-card select { width:100%; box-sizing:border-box }`, `.candidate-card textarea { min-height:~180px; resize:vertical }` (y lo mismo para review cards si aplica) para que titulo/narrativa/intencion/proyecto ocupen el ancho COMPLETO de la tarjeta. Behavior-test/contrato del CSS. Reentregar a in_review."
question: "Confirmas el fix de ancho (full-width real en .candidate-card: textarea/input/select width:100% + label grid), sin romper las demas fixes (PII/round3) ni fronteras?"
one_line_summary: "TASK-0172 round 4 (ancho): los textarea de .candidate-card quedan estrechos (width:100% solo en .intake-wizard); cubrir la tarjeta."
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# TASK-0172 round 4 -- ancho de los campos de la tarjeta de candidata

Round 3 (95af6ed) quedo bien: standalone inline removido, sin bloque de accion en aprobadas, rows=8, Cancelar.
El operador, probando, reporta que los textarea de Narrativa/Intencion siguen ESTRECHOS (altos pero angostos),
desperdiciando el ancho a la derecha.

## Causa (diagnosticada por el Arquitecto)
public/styles.css: la regla `width:100%` esta en `.intake-wizard textarea, .intake-wizard select` (~1286-1304).
La tarjeta `.candidate-card` (vista de lista/aprobadas) NO esta cubierta por esa regla, asi que sus `<textarea>`
con rows=8 quedan al ancho default del navegador (~20 cols).

## Fix (CSS, full-width real en la tarjeta)
- `.candidate-card label { display: grid; gap: var(--sp-1) }` (label arriba, campo abajo) -- o block.
- `.candidate-card textarea, .candidate-card input, .candidate-card select { width: 100%; box-sizing: border-box }`.
- `.candidate-card textarea { min-height: ~180px; resize: vertical }`.
- Si aplica, lo mismo para `.candidate-review` cards. Los campos ocupan el ANCHO COMPLETO de la tarjeta.

## DoD: AC1-AC6 + fronteras + PII + round 3 siguen verdes; behavior-test/contrato del CSS de la tarjeta;
node --test clon limpio exit 0; #4 byte-identica. Reentregar a in_review; luego checker Arquitecto + Analista
(pasada final PII+fronteras) -> cierro. rr=true.
