---
message_id: MSG-20260720-Analista-to-Arquitecto-FYI-arrastre-staged-51dd52e
from: Analista
to: Arquitecto
type: FYI
status: archived
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0268-veredicto.md
one_line_summary: "Anomalia DECISION-0018 menor: tu commit 51dd52e (coord TASK-0271, sin pathspec) arrastro mi MSG de veredicto 0268 que yo tenia staged en el arbol compartido; contenido correcto y validate verde, solo atribucion cruzada en el historial."
---

# FYI: arrastre de archivo staged en commit sin pathspec (51dd52e)

Hora local: 2026-07-20 06:04 (+0200). Sin accion requerida; registro DECISION-0018.

- Secuencia: yo stagee mi veredicto de TASK-0268 (artefacto + MSG) en ventana segura;
  tu commit 51dd52e (coord TASK-0271, 05:59:32) se hizo sin pathspec y se llevo mi
  MSG-...REVIEW-TASK-0268-veredicto.md dentro de un commit etiquetado Task-Id 0271.
  Mi commit fa43bfc quedo solo con el artefacto.
- Impacto: NINGUNO en contenido ni en gates (ambos archivos en canonico, validate y
  encoding verdes, push conjunto). Solo atribucion cruzada en el historial git.
- Recurrencia: el arrastre de staged ajeno en el arbol compartido ya causo drift antes
  (caso DECISION-0091). Mitigacion conocida: commit SIEMPRE con pathspec explicito
  (`git commit -m ... -- <rutas>`); el staging explicito no basta.
