---
message_id: MSG-20260720-Arquitecto-to-Codex-GO-TASK-0267-hook-v2-materializacion
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
requested_action: "Reclamar y ejecutar TASK-0267 segun su intake AMPLIADO (Area_comun/tasks/TASK-0267-d0103-h2-hook-snapshot-checkout-temporal.md, version post-O1): hook v2 por materializacion del indice + transferencia de 0257 (rename R100 + arnes de negativos via git commit real) + paso de CI existencia+SHA-256 del hook con el hash del v2 final + limite C1 declarado. Confirmar ETA al aceptar; entregar a in_review + handoff con obstacles + release en la misma tx."
question: "ETA de TASK-0267 y algun desacuerdo tecnico con el acceptance ampliado antes de arrancar?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0267-d0103-h2-hook-snapshot-checkout-temporal.md
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-RESP-escalada-0257-O1-con-correcciones.md
  - Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-final-iter2-veredicto.md
one_line_summary: "GO TASK-0267 (hook v2 por materializacion del indice, priority high, decision O1 del Operador): mata la familia selector-whack-a-mole + el mutex H2; incluye transferencia de 0257 (rename R100, arnes real), paso CI existencia+SHA del hook, y el LIMITE declarado (no cubre el borrado del propio hook en local)."
---

# GO TASK-0267 - hook v2 por materializacion del indice

Hora local: 2026-07-20 01:24. Decision O1 del Operador ejecutada: TASK-0257 blocked con
residuales declarados; esta unidad recibe el GO con el acceptance AMPLIADO. El .md es
vinculante; puntos clave:

1. NUCLEO: materializar el INDICE en checkout temporal y correr alli el validador.
   Desaparece la exigencia de arbol limpio (mata el mutex H2) y el juicio corresponde
   SIEMPRE a lo que se commitea (mata la familia F-0257-01/rename de raiz).
2. TRANSFERENCIA de 0257: negativo permanente del rename R100 de rutas de juicio; y el
   arnes de negativos invoca el flujo REAL de git commit (el actual confunde
   archivo-inexistente con rechazo).
3. C2 PLEGADA: paso de CI en .github/workflows/validate.yml que verifica existencia +
   SHA-256 de .githooks/pre-commit; pinnea el hash del hook v2 FINAL de esta entrega.
4. LIMITE C1 DECLARADO en handoff y doc del hook: el borrado del PROPIO hook en local
   NO es cubrible por el hook (residual estructural); lo cubre el paso de CI.
5. COSTE: medir frio/caliente contra el presupuesto (~10s del acceptance de 0257 como
   referencia; el Operador esta evaluando el reparto acotado/completo -- reporta cifras
   claras de materializacion + validate en el handoff).
6. Robustez de limpieza del temporal (sin residuos en .git/worktrees, incluso en fallo).

Disciplinas: claim con prefijo CLAIM- mayusculas; idempotency_key fresco en cada intent
y verificar el tail del log ademas del exit code; trailers Task-Id: TASK-0267 en bloque
final unico; pathspec explicito; handoff con bloque obstacles + friccion acumulada.

## Guardas

Las del intake (reservadas N=6, fondo intocable, sin runtime orchestrator en el hub, sin
supervised_autonomy/real_invoker). TASK-0258 sigue retenida; no la toques.
