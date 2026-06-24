---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0172-changes2
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Corregir 4 defectos de layout/UX del rediseno Intake (feedback del operador en prueba), todos en public/app.js (+ CSS): (1) ELIMINAR la seccion inline intake-extraction-standalone del panel principal -- la carga por archivo queda SOLO via el modal intake-file-modal (ya se abre desde el radio Archivo); (2) el boton Cancelar del modal de archivo ademas de cerrar debe RESETEAR el file input + el file-extraction-status; (3) en tarjetas de candidata con status != pending (approved/discarded) NO renderizar el bloque de accion (checkbox PII revisada + botones Aprobar/Usar tarjeta/Descartar) -- solo en status pending; (4) los textarea de Narrativa e Intencion de aceptacion (modal revision, tarjeta y modal manual) deben tener rows>=6 (idealmente 8, SPEC-0090 AC7) o min-height, full-width (estaban sin rows -> apinados). Behavior-test por cada uno. El fix de PII (round 2) y las AC1-AC6/fronteras siguen verdes. Reentregar a in_review."
question: "Confirmas las 4 correcciones de layout (quitar uploader inline / reset al cancelar / sin bloque-accion en aprobadas / textareas rows>=6) con behavior-test, sin romper PII fix ni fronteras?"
one_line_summary: "TASK-0172 round 3 (layout, feedback prueba operador): quitar uploader inline, reset Cancelar, sin bloque-accion en aprobadas, textareas rows>=6."
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# TASK-0172 round 3 -- 4 correcciones de layout (feedback del operador en prueba)

El fix de PII (round 2, commit 9f1f772) quedo verde (default redactado fail-safe + test negativo). El operador,
probando el front, reporto 4 defectos de layout/UX (todos client-side):

## Defecto 1 -- file-upload inline en el panel principal
public/app.js: el render del panel intake incluye una seccion inline `intake-extraction-standalone` (~1627-1630)
con renderFileUploader, SIEMPRE visible. Debe ELIMINARSE: la carga por archivo va SOLO por el modal
`intake-file-modal` (RC-05), que ya se abre desde el radio Archivo (openIntakeForMode("file")). El panel principal
queda: control-bar + folder-grid + intake-list (+ modales hidden).

## Defecto 2 -- Cancelar del modal de archivo no resetea
El boton Cancelar (`data-intake-cancel` -> closeIntakeModal) cierra el modal (OK), pero debe ademas RESETEAR el
file input y el `file-extraction-status` para que reabrir muestre estado limpio (no stale).

## Defecto 3 -- tarjetas aprobadas muestran el bloque de accion
Render de tarjeta (~1831-1850): con `status != pending` deja el bloque (checkbox PII revisada + Aprobar/Usar
tarjeta/Descartar) en gris. Debe NO renderizarse para approved/discarded; solo en `status === pending`.

## Defecto 4 -- textareas apinados
Los `<textarea>` de Narrativa e Intencion de aceptacion (modal revision ~1838/1839, tarjeta ~1767/1768, modal
manual ~1598/1599) no tienen `rows` -> default ~2 lineas. Darles rows>=6 (idealmente 8) o min-height, full-width,
en TODOS los renders.

## DoD: AC1-AC6 + fronteras + PII (round 2) verdes; behavior-test por defecto; node --test clon limpio exit 0;
#4 byte-identica; sin nueva ruta de escritura. Reentregar a in_review; luego checker Arquitecto + Analista. rr=true.
