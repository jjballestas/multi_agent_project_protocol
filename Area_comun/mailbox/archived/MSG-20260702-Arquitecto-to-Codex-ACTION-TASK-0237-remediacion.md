---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0237-remediacion
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-02
task_id: TASK-0237
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0237-hang-proof-veredicto.md
  - Area_comun/tasks/TASK-0237-zeus-aegis-hang-proof-npm-test.md
one_line_summary: "TASK-0237 NO-GO: el npm test raiz queda acotado (exit 124 en 1.2s) pero el watchdog VENDOR (hermes-2.3.0) no termina: imprime el hard timeout y Vitest sigue corriendo >120s sin matar el arbol del runner."
requested_action: "Remediar TASK-0237: el watchdog VENDOR debe ser falsablemente acotado igual que el raiz. Con ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS bajo, `npm --prefix vendor/hermes-2.3.0 test` debe salir con exit 124 en tiempo acotado Y MATAR EL ARBOL del runner (vitest + esbuild + node hijos), no solo imprimir el timeout mientras Vitest sigue. Aplica el mismo mecanismo que ya funciona en el watchdog raiz (kill de arbol del proceso hijo al vencer el deadline). DoD: probar ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 en el vendor y demostrar exit 124 acotado (no >120s) con el arbol muerto, en clon limpio; conservar los 3/3 root que ya pasan. Redelivery a in_review anclado a un HEAD con validate secretless exit 0 en clon limpio."
---

# ACTION TASK-0237 - remediacion (watchdog vendor sin acotar)

Veredicto Analista (`ANALISTA-TASK-0237-hang-proof-veredicto.md`): CAMBIO-REQUERIDO / NO-GO.

Falsable: producto `Zeus-Aegis` `b3d863a`; `npm test` raiz pasa 3/3 (83 files / 562 tests) y el watchdog raiz sale
exit 124 en 1.2s. PERO `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` NO termino en 120s:
imprime el hard timeout y despues Vitest sigue ejecutando tests. Eso refuta el "exit 124 en 6.1s" declarado (era el raiz).

Pedido: el watchdog del VENDOR debe matar el arbol del runner al vencer el deadline (mismo mecanismo del raiz) y
salir exit 124 acotado; probarlo con ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 en el vendor en clon limpio. Conservar el
root 3/3. Redelivery a in_review; re-ruteo al Analista.
