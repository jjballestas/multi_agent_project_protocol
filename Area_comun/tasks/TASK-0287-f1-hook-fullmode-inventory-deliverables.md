---
task_id: TASK-0287
title: "[DECISION-0103][F1/follow-up] Hook full-mode: el inventario del snapshot parcial omite deliverables de tarea (HUMAN_GUIDE.md + personal/**) -> falso rechazo de arbol limpio"
type: infra
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-23
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0257, TASK-0268, TASK-0269, TASK-0265]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0287-f1-hook-fullmode-inventory-deliverables.md
intake:
  type: infra
  goal: Corregir el falso positivo F1 detectado por el gate final TASK-0265 (artifact Analista-TASK-0265-gate-final-conjunto-0103-verdict). El hook de MODO COMPLETO local (HOOK_FULL=1 / git config hook.full true) sobre-rechaza en FALSO un arbol limpio porque su inventario de snapshot parcial (.githooks/pre-commit, snapshot_inventory ~lineas 63-77) materializa Area_comun/runtime/scripts/profiles/examples + una lista de archivos raiz, pero NO el HUMAN_GUIDE.md de raiz ni personal/**; y el chequeo de existencia-de-deliverables (scripts/validate_collaboration_state.py:1049-1054) mira el campo `deliverables` de TASK_INDEX/archives, que puede apuntar fuera del inventario. Cota exacta reportada, 2 deliverables fuera de inventario, ambos existentes, TASK-0037 -> HUMAN_GUIDE.md; TASK-0084 -> personal/Codex/STARTUP_PROMPT.md (ambos en TASK_INDEX_ARCHIVE.json). Resultado hoy, validate_collaboration_state.py sobre el arbol = exit 0, pero HOOK_FULL=1 sh .githooks/pre-commit sobre el mismo arbol limpio = exit 1 con 'deliverable missing'. Falla en CERRADO (sobre-rechaza; nunca sub-acepta); el CI (arbol completo) y el modo default (partial) NO se afectan; solo la bandera VOLUNTARIA local.
  acceptance:
    - El read-set del inventario del snapshot parcial del hook full-mode incluye el read-set de existencia-de-deliverables (o el chequeo de deliverables se acota al arbol completo), de modo que un arbol LIMPIO no se rechace en falso bajo HOOK_FULL=1.
    - Prueba, arbol limpio en HEAD + HOOK_FULL=1 -> exit 0 (hoy exit 1 falso). Los 2 deliverables (HUMAN_GUIDE.md, personal/Codex/STARTUP_PROMPT.md) se reconocen presentes.
    - NO-REGRESION de la intencion de seguridad C5, un estado gobernado GENUINAMENTE roto staged + HOOK_FULL=1 sigue RECHAZANDO por validate_collaboration_state (no se debilita el gate real); construir el negativo y evidenciarlo.
    - Paridad con el CI mantenida, .github/workflows/validate.yml sigue corriendo validate sobre el arbol completo; el pin por SHA-256 del hook se actualiza si el hook cambia.
    - El fix se prueba por el ENTRYPOINT REAL del hook (no un atajo), y se documenta si extiende el inventario o acota el chequeo.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - HOOK_FULL=1 sh .githooks/pre-commit sobre arbol limpio -> exit 0 (evidencia)
    - Negativo, estado gobernado roto staged + HOOK_FULL=1 -> exit 1 (evidencia)
    - python scripts/scan_encoding.py
  scope_routes:
    - .githooks/pre-commit
    - examples/
  out_of_scope:
    - Cambiar el COMPORTAMIENTO del gate real (validate_collaboration_state) - FUERA; solo se corrige el read-set/inventario del snapshot del hook.
    - El reparto de coste E6-A (partial por defecto) - FUERA; el default no cambia.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
  risk: low
  estimate: S
---

# TASK-0287 - [DECISION-0103][F1] Hook full-mode: inventario omite deliverables -> falso rechazo

Origen: hallazgo F1 del gate final TASK-0265 (WARNING-real, no bloqueante, territorio E6/0268-0269).
El hook full-mode local (HOOK_FULL=1) sobre-rechaza un arbol limpio porque su inventario de
snapshot parcial no cubre el read-set de existencia-de-deliverables (HUMAN_GUIDE.md, personal/**).
Falla en cerrado y no afecta al CI ni al modo default; es un follow-up de mantenimiento.
