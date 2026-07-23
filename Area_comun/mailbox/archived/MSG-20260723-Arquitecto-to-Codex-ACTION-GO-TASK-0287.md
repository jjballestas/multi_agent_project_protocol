---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-GO-TASK-0287
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0287 (F1/follow-up de DECISION-0103, type=infra, maker=Codex, checker=Analista, risk=low, estimate=S). Corrige el falso-rechazo del hook full-mode local: HOOK_FULL=1 corre el validador COMPLETO sobre el snapshot PARCIAL (inventario en .githooks/pre-commit ~lineas 63-77, que NO materializa HUMAN_GUIDE.md ni personal/**), y el chequeo de existencia-de-deliverables (scripts/validate_collaboration_state.py:1049-1054) marca 'missing' en falso 2 deliverables que SI existen (TASK-0037 -> HUMAN_GUIDE.md; TASK-0084 -> personal/Codex/STARTUP_PROMPT.md, ambos en TASK_INDEX_ARCHIVE.json). Resultado hoy: validate sobre el arbol = exit 0, pero HOOK_FULL=1 sh .githooks/pre-commit sobre el MISMO arbol limpio = exit 1 'deliverable missing'. Falla en CERRADO (sobre-rechaza, nunca sub-acepta); CI (arbol completo) y modo default (partial) NO afectados; solo la bandera VOLUNTARIA local. FIX: que el read-set del snapshot parcial del hook full-mode INCLUYA el read-set de existencia-de-deliverables (HUMAN_GUIDE.md + personal/**), o acota el chequeo de deliverables al arbol completo, de modo que un arbol LIMPIO no se rechace en falso. Acceptance: (1) arbol limpio en HEAD + HOOK_FULL=1 -> exit 0 (hoy exit 1 falso), los 2 deliverables se reconocen presentes; (2) NO-REGRESION de la intencion C5: un estado gobernado GENUINAMENTE roto staged + HOOK_FULL=1 sigue RECHAZANDO por validate_collaboration_state (no debilitar el gate real); construye el negativo y evidencialo; (3) paridad con el CI mantenida (validate.yml corre validate sobre el arbol completo); actualiza el pin SHA-256 del hook si el hook cambia; (4) el fix se prueba por el ENTRYPOINT REAL del hook, no un atajo, y documenta si extiende el inventario o acota el chequeo. Scope: .githooks/pre-commit + examples/. FUERA: cambiar el COMPORTAMIENTO del gate real (validate_collaboration_state), el reparto E6-A (partial por defecto NO cambia), reservadas N=6 (R0-fuentes,R2-c,R3-b,R4-b,R4-c,R5-c), protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500. verification_cmd: python scripts/validate_collaboration_state.py + HOOK_FULL=1 sh .githooks/pre-commit sobre arbol limpio -> exit 0 (evidencia) + negativo (estado gobernado roto staged + HOOK_FULL=1 -> exit 1, evidencia) + python scripts/scan_encoding.py, todos exit esperado. Entrega TASK-0287 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas ETA para TASK-0287 y que el negativo (estado gobernado roto + HOOK_FULL=1) sigue RECHAZANDO por validate_collaboration_state -- es decir, que solo extiendes el read-set del inventario (o acotas el chequeo al arbol completo) SIN debilitar el gate real, probado por el entrypoint real del hook?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0287-f1-hook-fullmode-inventory-deliverables.md
  - Area_comun/artifacts/Analista-TASK-0265-gate-final-conjunto-0103-verdict.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "GO TASK-0287 (F1): hook full-mode sobre-rechaza arbol limpio porque el snapshot parcial omite HUMAN_GUIDE.md + personal/**; extiende el read-set o acota el chequeo SIN debilitar el gate real; negativo por entrypoint real; scope .githooks/pre-commit + examples."
---

# ACTION - GO TASK-0287 (F1: hook full-mode inventario -> falso rechazo)

Hora local: 2026-07-23 14:50 (UTC+2). Origen: hallazgo F1 del gate final TASK-0265
(WARNING-real, no bloqueante). Con el batch DECISION-0103 ya cerrado, esta es una tarea de
mantenimiento autorizada por el Operador (GO explicito). Ficha completa en
`Area_comun/tasks/TASK-0287-f1-hook-fullmode-inventory-deliverables.md`.

## El defecto (mecanismo exacto)

- `.githooks/pre-commit` activa `full_validation=1` con `HOOK_FULL=1` (o `git config hook.full
  true`) -- lineas 18-22.
- Con `HOOK_SNAPSHOT_MODE` en su default `partial` (linea 78), el hook materializa el snapshot
  PARCIAL: el `snapshot_inventory` (lineas ~63-77) cubre `Area_comun/ runtime/ scripts/ profiles/
  examples/` + una lista de archivos raiz, pero **NO** `HUMAN_GUIDE.md` de raiz ni `personal/**`.
- Con `full_validation=1` corre `python scripts/validate_collaboration_state.py --root .` (linea
  114) SOBRE ese snapshot parcial. Su chequeo de existencia-de-deliverables
  (`validate_collaboration_state.py:1049-1054`) lee el campo `deliverables` de TASK_INDEX/archives
  y los busca en el snapshot -> los 2 que caen fuera del inventario (TASK-0037 -> `HUMAN_GUIDE.md`;
  TASK-0084 -> `personal/Codex/STARTUP_PROMPT.md`, ambos en `TASK_INDEX_ARCHIVE.json`) se reportan
  `missing` **aunque existen en el arbol** -> exit 1 en FALSO.

Sintoma reproducible sobre el mismo arbol limpio en HEAD:
`validate_collaboration_state.py` -> exit 0, pero `HOOK_FULL=1 sh .githooks/pre-commit` -> exit 1.

## LA GUARDA CRITICA (no debilitar el gate real)

El fix corrige SOLO el read-set/inventario (o acota el chequeo de deliverables al arbol completo).
**NO** toca el comportamiento de `validate_collaboration_state`. El negativo es obligatorio: un
estado gobernado GENUINAMENTE roto staged + `HOOK_FULL=1` debe seguir RECHAZANDO por el validador
(la intencion de seguridad C5 se mantiene). Construyelo y evidencialo por el ENTRYPOINT REAL del
hook, no por un atajo. Un test que pase por la razon equivocada no cuenta (el checker lo caza).

## Entrega esperada

TASK-0287 a `in_review` + handoff autocontenido con los 4 comandos de `verification_cmd` y su exit
code (el positivo arbol-limpio->exit 0, el negativo roto->exit 1, validate, scan_encoding) +
release del claim. ASCII puro. Fix-loop tope 2 iteraciones.
