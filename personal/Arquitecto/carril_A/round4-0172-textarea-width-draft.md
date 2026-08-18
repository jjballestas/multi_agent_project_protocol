ROUND 4 TASK-0172 (ancho de textareas, feedback operador) -- mandar tras verificar round 3:

## Defecto -- textareas de la tarjeta de candidata altos pero ESTRECHOS (desperdician ancho)
- public/styles.css: la regla `width: 100%` de textarea/select esta scopeada a `.intake-wizard textarea,
  .intake-wizard select` (~1286-1304). La TARJETA `.candidate-card` (vista de lista/aprobadas) NO esta cubierta,
  asi que sus `<textarea>` (con rows=8 tras round 3) quedan al ancho default del navegador (~20 cols) -> altos
  pero estrechos; se desperdicia el espacio a la derecha. (El operador lo confirma en imagen sobre una tarjeta
  approved.)
- Fix CSS (full-width real en la tarjeta y en cualquier card de candidata):
  - `.candidate-card label { display: grid; gap: var(--sp-1) }` (label text arriba, campo abajo) -- o block.
  - `.candidate-card textarea, .candidate-card input, .candidate-card select { width: 100%; box-sizing: border-box }`.
  - `.candidate-card textarea { min-height: ~180px; resize: vertical }` (consistente con .intake-wizard textarea).
  - Si aplica, lo mismo para `.candidate-review` cards. La idea: los campos (titulo/narrativa/intencion/proyecto)
    ocupan el ANCHO COMPLETO de la tarjeta, no una columna estrecha a la izquierda.
- Behavior-test/contrato: el CSS de la tarjeta de candidata aplica width:100% a sus textarea/input (no quedan al
  ancho default). (Si el test es de DOM/CSS-string, asertar la regla; si es de estructura, asertar la clase.)

## DoD: AC1-AC6 + fronteras + PII + las 4 de round 3 siguen verdes; node --test clon limpio exit 0; #4 byte-id.
## Origen: feedback del operador en prueba (2026-06-24): "los textarea siguen apinados... se desperdicia el
## espacio a la derecha". Es ANCHO (width), no alto (rows ya quedo en 8).
