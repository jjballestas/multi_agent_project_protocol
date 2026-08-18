ROUND 3 TASK-0172 (layout, feedback del operador en prueba) -- mandar tras verificar el PII fix:

## Defecto 1 (RC-05/RC-06 layout) -- file-upload inline en el panel principal
- public/app.js: el render del panel intake incluye una seccion inline `intake-extraction-standalone`
  (lineas ~1627-1630) con renderFileUploader, SIEMPRE visible. El operador (probando): "no debe estar ahi,
  pues para eso se lanza desde el boton".
- Fix: ELIMINAR la seccion `intake-extraction-standalone` del render del panel principal. La carga por archivo
  queda SOLO via el modal `intake-file-modal` (RC-05), que ya se abre desde el radio Archivo
  (openIntakeForMode("file") -> modal.hidden=false). El panel principal queda: control-bar + folder-grid +
  intake-list (+ modales hidden). Behavior-test: el render del panel principal NO contiene el uploader inline
  fuera de un modal hidden (la unica `renderFileUploader` visible es dentro de `.intake-file-modal[hidden]`).

## Defecto 2 (Cancelar) -- verificar/limpiar
- El boton Cancelar (`data-intake-cancel` -> closeIntakeModal) oculta los `.intake-modal` (logica correcta).
- Asegurar que Cancelar en el modal de archivo: (a) cierra el modal, (b) RESETEA el file input + el
  file-extraction-status (data-file-extraction-status) para que reabrir muestre estado limpio (no stale).
- Behavior-test: abrir intake-file-modal -> (estado) -> Cancelar -> modal hidden=true + file input/extraction
  status reseteados; reabrir muestra estado inicial.

## Defecto 3 (tarjetas aprobadas) -- bloque de accion no debe renderizarse
- public/app.js render de tarjeta de candidata (~1831-1850): usa `const disabled = candidate.status !== "pending"
  ? "disabled" : ""` y RENDERIZA igual el bloque (checkbox "PII revisada" + botones Aprobar/Usar tarjeta/
  Descartar) en gris para approved/discarded. El operador: en tarjetas APROBADAS ese bloque NO debe estar.
- Fix: para `candidate.status !== "pending"` (approved/discarded) NO renderizar el bloque de accion
  (PII revisada + Aprobar/Usar tarjeta/Descartar). Los campos pueden quedar visibles read-only; el bloque de
  aprobacion solo para `status === "pending"`. Behavior-test: tarjeta approved -> sin checkbox PII ni botones
  Aprobar/Usar tarjeta/Descartar; tarjeta pending -> con el bloque.

## Defecto 4 (textareas apinados) -- rows insuficientes
- public/app.js: los `<textarea>` de Narrativa e Intencion de aceptacion (modal revision ~1838/1839, tarjeta
  ~1767/1768, modal manual ~1598/1599) NO tienen `rows` -> default del navegador (~2 lineas), texto apinado.
- Fix: dar `rows` adecuado (>=6, idealmente 8 como SPEC-0090 AC7) o min-height por CSS a esos textarea en TODOS
  los renders (modal revision, tarjeta, modal manual), full-width. Behavior-test: los textarea de narrativa/
  intencion exponen rows>=6 (o min-height equivalente) en el modal manual y en el de revision.

## DoD: AC1-AC6 + fronteras + PII (round 2) siguen verdes; node --test clon limpio; #4 byte-identica.
## Origen: feedback del operador en prueba del front (2026-06-24). 4 defectos de layout/UX, todos client-side.
