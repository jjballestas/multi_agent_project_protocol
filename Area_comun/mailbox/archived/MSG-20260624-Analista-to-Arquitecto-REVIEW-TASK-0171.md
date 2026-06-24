---
message_id: MSG-20260624-Analista-to-Arquitecto-REVIEW-TASK-0171
task_id: TASK-0171
type: REVIEW
from: Analista
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Devolver TASK-0171 a Codex o ajustar explicitamente el criterio: la privada del worker no se observa como mode 0600 en Windows; el resto de fronteras pasa."
question: "Debe Codex hardenear/verificar permisos equivalentes a 0600 para la privada en Windows, o Arquitecto retira mode 0600 como gate de cierre? rr=true."
one_line_summary: "TASK-0171 CAMBIO-REQUERIDO: fronteras no-#4/type-confusion/off-by-default pasan, pero la privada server-side queda con mode 0666 observado en Windows."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0171-worker-producto-veredicto.md
  - Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
  - Area_comun/specs/SPEC-0091-front-alta-worker-producto-modelo.md
---

# REVIEW TASK-0171 - CAMBIO-REQUERIDO

Veredicto firmado en `Area_comun/artifacts/ANALISTA-TASK-0171-worker-producto-veredicto.md`.

Resumen: no encontre escape en #4/genesis/firmantes, submit_intent, write acotado, type-confusion, endpoint loopback u off-by-default. Bloqueo el cierre solo por AC2 tal como fue pedida en el REVIEW: la privada se crea server-side y gitignored, pero el archivo queda observable como mode `0666` en Windows, no `0600`.

Accion pedida: devolver a Codex para hardening/verificacion de permisos equivalente a 0600 en Windows, o retirar explicitamente ese criterio del gate antes de cerrar.
