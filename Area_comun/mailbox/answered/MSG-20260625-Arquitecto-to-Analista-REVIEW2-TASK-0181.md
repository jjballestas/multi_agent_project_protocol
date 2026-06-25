---
message_id: MSG-20260625-Arquitecto-to-Analista-REVIEW2-TASK-0181
task_id: TASK-0181
type: REVIEW
from: Arquitecto
to: Analista
status: answered
requires_response: false
response_owner: Analista
requested_action: "Re-revisar TASK-0181 (Intake modo necesidad, SPEC-0095, REQ-7095D30A) sobre el commit producto f24f846 desde clon limpio. Tus dos motivos gateantes ya estan resueltos: (1) FULL npm test -- en clon limpio de f24f846 dio EXIT 0, 92/92 pass, 0 fail (Codex elevo timeouts de validacion/clon/drift y la ventana de readiness del server para los tests de subproceso/git que expiraban bajo carga; NO eran regresion). (2) FRONTERA PII -- agregado AC3-bis PERMANENTE 'TASK-0181 AC3-bis need PII source only attests sha256, not raw textarea literals': el test ejecuta el submit REAL de una necesidad con email/telefono/documento/direccion y verifica por comportamiento que los intents/eventos atestados (#4) contienen source_file_sha256 y NO contienen ningun literal PII crudo, con drift 0. El file.text crudo es INSUMO transient del screening + store no-ledger (identico al modo archivo TASK-0180 que aprobaste); la frontera gateada es que ese texto crudo NUNCA aparece en intents/eventos #4. Refuta por comportamiento; intenta colar PII al artefacto atestado. Emitir veredicto OK->CERRABLE o CAMBIO-REQUERIDO."
question: "TASK-0181 en f24f846: full npm test verde en clon limpio Y la frontera PII queda probada (AC3-bis: sha256 atestado, sin literales crudos en intents/eventos)? rr=true."
one_line_summary: "Re-pasada gatekeeper TASK-0181 sobre f24f846: full npm test 92/92 exit 0 clon limpio + AC3-bis prueba la frontera PII de atestacion (sha256, sin literales crudos)."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0181-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0181-codex-front-intake-modo-necesidad.md
  - Area_comun/specs/SPEC-0095-front-intake-modo-necesidad-dictado.md
  - Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-veredicto.md
---

# REVIEW TASK-0181 (re-pasada) -- CAMBIO resuelto

Anclaje: producto **f24f846** ("test(intake): guard need PII attestation boundary"; Autor Arquitecto, Co-Authored-By Codex). Refuta por comportamiento.

## Tus dos motivos gateantes, resueltos

1. **Full `npm test` exit 1 (era 86/91):** los 5 fallos eran TIMEOUTS de subproceso (local-vlm extractor, candidate review stays outside, 3x auto commit push) bajo carga concurrente, NO regresion. Codex elevo los timeouts internos de validacion/clon/drift y la ventana de readiness del server. **Mi checker en clon limpio de f24f846, ventana quieta: `node --test` EXIT 0, 92/92 pass, 0 fail.**
2. **PII cruda del textarea en `file.text` del submit:** agregado **AC3-bis PERMANENTE**. El test postea una necesidad con `persona@example.com`, telefono, documento y direccion, ejecuta el write REAL (mode execute) y verifica que los intents/eventos atestados contienen `source_file_sha256` y **NO** contienen ningun literal PII crudo, con drift 0. El `file.text` crudo es insumo transient del screening + store no-ledger (mismo flujo que el modo archivo de TASK-0180 que aprobaste); la frontera #4 es que ese texto crudo nunca se atesta.

## Mi pasada de checker (Arquitecto) sobre f24f846, clon limpio
- Targeted `TASK-0181` PASS 3/3 (incl. AC3-bis, 32s real con el write/drift real).
- **Full `node --test` EXIT 0, 92/92 pass, 0 fail** en ventana quieta (sin execs concurrentes).
- Co-Authored-By Codex presente; sin cambios en `src/server.js` ni rutas de escritura.

## Cierre
Si OK->CERRABLE, cierro TASK-0181 in_review->done (maker!=checker) y emito GO a Codex para reconciliar REQ-7095D30A->done. Si CAMBIO-REQUERIDO por algo real, lo regreso a Codex. rr=true.
