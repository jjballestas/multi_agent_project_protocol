---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0229-allowlist-decision0082
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-5-veredicto.md
  - Area_comun/decisions/DECISION-0082-branding-user-visible-scope-ws3.md
one_line_summary: "TASK-0229 a un paso de cerrar: los 3 hits estan corregidos y gates verdes, pero falta ENTREGAR la allowlist etiquetada de DECISION-0082; producela y reentrega para el gate final."
requested_action: "Entregar la ALLOWLIST ETIQUETADA que exige DECISION-0082 (punto 3) -- es el unico bloqueo del Analista (los 3 hits ya estan corregidos, npm test/gates verdes). Produce un artefacto (p.ej. Area_comun/artifacts o docs del producto, referenciado desde la tarea) que liste, a partir de `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` en el HEAD del producto, CADA hit restante con: path:linea + etiqueta {identificador|import|comentario|dev-log-no-surfaceado|test-fixture|licencia-provenance|env-shim} + una linea de prueba/justificacion de por que NO se renderiza al usuario (traza a que no llega a una superficie del punto 1 de DECISION-0082). Para cualquier hit que NO puedas probar como no-render, REBRANDEALO a Zeus (no lo dejes sin prueba). Regenera el bundle si tocaste src. La lista debe ser FALSABLE: el Analista debe poder verificar cada etiqueta. Sin regresion (shim, npm test verde por EXIT, no-rename, NOTICE MIT). Reentrega a in_review con la allowlist adjunta/enlazada."
---

# ACTION TASK-0229 - entregar la allowlist etiquetada (cierre)

El operador pidio cerrar 0229. El Analista confirma: los 3 hits estan corregidos y `npm test` clon limpio = 0,
gates verdes; el UNICO bloqueo es que **no entregaste la allowlist etiquetada por-hit** que DECISION-0082 (punto 3)
convierte en el AC. Sin lista falsable, el Analista no puede verificar que las etiquetas sean verdaderas -> NO-GO.

Entrega esa allowlist: por cada hit `hermes` que quede en `vendor/hermes-2.3.0/src/**` + `electron/server-bundle.cjs`,
da `path:linea` + etiqueta + prueba de no-render. Rebrandea a Zeus cualquier hit sin prueba. Es un entregable
documental (mas rebrand de lo no-probable), no otra ronda de whack-a-mole. Reentrega a in_review; el Analista hace el
gate final contra la allowlist. maker != checker. Con su GO ratifico y cierras a done.
