---
message_id: MSG-20260630T110827Z-Operador-to-Arquitecto-DIRECTIVA-commit-instruccion-tfm
task_id: OPS-COMMIT-TFM-ARTIFACTS-20260630
type: DIRECTIVE
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
operator_directive: true
created_at: 2026-06-30T11:08:27Z
context_refs:
  - personal/operador/TFM/INSTRUCCION-ALIMENTAR-TFM-ESTUDIO.md
  - personal/operador/TFM/FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md
  - personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md
question: "Commiteados los artefactos TFM del operador con stage explicito y pusheados si verde? Confirmar con FYI (HEAD + hora UTC)."
requested_action: "Commitear los artefactos TFM del Operador con stage EXPLICITO por path (nunca git add -A): personal/operador/TFM/INSTRUCCION-ALIMENTAR-TFM-ESTUDIO.md (principal), y recomendado en el mismo commit personal/operador/TFM/FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md y personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md. EXCLUIR personal/operador/TFM/chat_tfm.txt (no es artefacto). Gates verdes por exit-code antes (validate_collaboration_state.py, scan_encoding.py, neutralidad, drift 0). Autor real Arquitecto. Push si verde; actualizar memoria (DECISION-0026)."
one_line_summary: "Operador ordena commitear los artefactos TFM del operador (instruccion + firma + plan), stage explicito, excluyendo chat_tfm.txt."
---

Directiva del Operador al Arquitecto.

CONTEXTO
- El Operador (via asistente) creo artefactos TFM en personal/operador/TFM/ (sin commitear). HEAD = 51d380e.
- La INSTRUCCION alimenta el caso TFM del agente Estudio (F5) con evidencia nueva del protocolo (runbook del
  operador, no toca ledger ni AGENTS.md).

ORDEN
1) Stage EXPLICITO por path (nunca git add -A: barre personal/):
   - personal/operador/TFM/INSTRUCCION-ALIMENTAR-TFM-ESTUDIO.md   (principal, lo pedido)
   - personal/operador/TFM/FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md   (recomendado; firma del freeze ya referenciada)
   - personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md           (recomendado; plan ya referenciado)
   EXCLUIR: personal/operador/TFM/chat_tfm.txt (transcripcion suelta, no artefacto).
2) Gates verdes por exit-code ANTES del commit: validate_collaboration_state.py, scan_encoding.py,
   scan de neutralidad, drift 0.
3) Commit con autor real Arquitecto (es contenido del operador, no se falsifica autoria de Codex/Analista).
   Mensaje sugerido: "docs(tfm): artefactos del operador (instruccion alimentar Estudio + firma freeze + plan medicion)".
4) Push si verde; actualizar memoria (DECISION-0026).

Reportar cierre con FYI: HEAD resultante + hora UTC.
