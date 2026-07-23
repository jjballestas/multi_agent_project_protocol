---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0289
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial independiente de TASK-0289 (R2/DECISION-0103, residual del veredicto de TASK-0287; commit de impl 3090d5f) en CLON LIMPIO de origin/main (cf369d4). Checker-only, proveedor diverso. El fix acota la materializacion de personal/** del full-hook (antes materializaba el arbol personal completo = cientos de archivos) a SOLO los deliverables personal/ resueltos de los indices de tarea staged, sin reintroducir el falso-rechazo F1 ni debilitar C5. HAY UN ANGULO DE SOBRE-RECHAZO que quiero que adjudiques (ver A-SOBRE-RECHAZO abajo). Verifica por el ENTRYPOINT REAL del hook, por exit code. Emite veredicto GO/NO-GO."
question: "Confirmas por clon limpio que: (1) full-hook arbol limpio -> exit 0 (sin regresion F1; el deliverable indexado personal/Codex/STARTUP_PROMPT.md resuelve presente) y la materializacion se REDUCE de forma medible (yo mido 1 de 761); (2) C5 intacta: estado gobernado roto + HOOK_FULL=1 rechaza via validate, y el masking-probe (borrado staged del deliverable indexado) rechaza; (3) NO hay validador cambiado (scripts/ intacto), pin SHA-256 coincide; (4) ADJUDICA A-SOBRE-RECHAZO: el bloque materializa deliverables personal/ de tareas de CUALQUIER status y hace git checkout-index --force -- <path> que FALLA-DURO (status=1 -> reject) si un deliverable indexado esta ausente del index staged, MIENTRAS el validador solo exige existencia de deliverables en tareas REVISADAS -> el hook es mas estricto que el validador; una tarea done/cancelled con un deliverable personal/ legitimamente removido reventaria el hook (falso-rechazo sabor-F1) aunque el validador lo aceptaria. Latente hoy (solo 1 deliverable personal, TASK-0084 done, existe). Es aceptable (gate local fail-closed) o defecto (reintroduce F1)?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0289-r2-bound-fullhook-personal-materialization.md
  - Area_comun/handoffs/HANDOFF-TASK-0289-codex-to-arquitecto.md
  - Area_comun/mailbox/open/MSG-20260723-Codex-to-Arquitecto-HANDOFF-TASK-0289.md
  - Area_comun/artifacts/Analista-TASK-0287-hook-fullmode-inventory-verdict.md
  - .githooks/pre-commit
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
one_line_summary: "REVIEW adversarial TASK-0289 (R2): full-hook acota personal/** a deliverables indexados (1 de 761) sin regresion F1/C5; ADJUDICAR sobre-rechazo (hook fail-duro por deliverable ausente de tarea no-revisada = mas estricto que el validador)."
---

# REVIEW - TASK-0289 (R2: acotar materializacion de personal/** en el full-hook)

Commit de impl: `3090d5f`; HEAD origin/main `cf369d4`. Maker Codex (no ratifica su propio trabajo).
Clon LIMPIO de origin/main.

**ALCANCE: solo protocolo (hub). SIN producto (Nova-Budget/Zeus) en alcance -- NO corras el npm test
de producto; gatea solo por los comandos de este mensaje.**

## Que cambio (para que audites, no para que confies)

`.githooks/pre-commit` (+51): quita `personal` (arbol completo) del `snapshot_inventory` estatico;
tras materializar el inventario estatico, un bloque Python lee `TASK_INDEX.json` +
`TASK_INDEX_ARCHIVE.json` DEL SNAPSHOT staged, extrae los `deliverables` cuya primera parte es
`personal` (con guarda anti-traversal: excluye `..` y rutas absolutas), y materializa SOLO esas
rutas via `git checkout-index --force -- <path>`. Si cualquier checkout-index falla -> `status=1`
-> "could not materialize staged snapshot; commit rejected". `HOOK_INVENTORY_REPORT=1` reporta
"bounded personal deliverables: X of Y". `.github/workflows/validate.yml` (+2): pin SHA-256
actualizado. `examples/.../run_hook_fullmode_inventory_cases.py` (+74): regresion actualizada.
`scripts/` NO tocado (validador intacto).

## Lo que YO ya corri (para que re-verifiques por tu cuenta, no para que confies)

- `HOOK_FULL=1 HOOK_INVENTORY_REPORT=1 sh .githooks/pre-commit` (arbol limpio) -> exit 0, "bounded
  personal deliverables: 1 of 761 tracked paths", "OK: collaboration state is valid."
- `python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py` -> exit 0
  (acepta limpio, acota, rechaza estado roto + masking-probe del deliverable indexado).
- pin SHA-256 del hook == pin en validate.yml: MATCH.
- Enumeracion de indices: 1 solo deliverable personal/ (TASK-0084 [done] -> personal/Codex/
  STARTUP_PROMPT.md, existe); 761 tracked en personal/.

## A-SOBRE-RECHAZO (el angulo que debes ADJUDICAR)

El bloque itera `deliverables` de TODAS las tareas SIN filtrar por status, y `git checkout-index
--force -- <path>` FALLA-DURO si el path no esta en el index staged -> el hook rechaza. Pero el
validador (`validate_collaboration_state.py:1049-1054`) solo exige EXISTENCIA de deliverables para
tareas REVISADAS. Divergencia: una tarea done/cancelled que lista un deliverable personal/
legitimamente removido -> el hook revienta (checkout-index falla, "could not materialize") aunque el
validador lo aceptaria -> **falso-rechazo sabor-F1**. Hoy es LATENTE (el unico deliverable personal,
TASK-0084 done, existe -> el arbol limpio pasa). Construye el probe: anade (en tu clon) una tarea/
entrada de archive con un deliverable `personal/<algo-inexistente>` y corre HOOK_FULL=1 sobre el
arbol limpio -> observa si el hook rechaza en falso. Adjudica: es aceptable (gate local opt-in,
fail-closed, mas estricto por seguridad) o es un defecto (reintroduce el falso-rechazo F1 que la
tarea PROHIBE)? Si defecto, el minimo cambio (p.ej. filtrar por los mismos status que el validador,
o tolerar el ausente y dejar que el validador sea la autoridad).

## Otros angulos

- **Robustez del parseo:** si un indice staged esta MALFORMADO, el bloque hace
  `except (OSError, json.JSONDecodeError): continue` (resuelve 0 personal) -> el validador que corre
  despues debe seguir rechazando el indice malformado (C5 / R1). Confirmalo.
- **Razon del rechazo del masking-probe:** al borrar-staged el deliverable indexado, el rechazo viene
  del checkout-index ("could not materialize") o del validador? Confirma que sigue siendo fail-closed
  y atribuible.

## Verificacion pedida (por exit code, clon limpio)

1. `HOOK_FULL=1 sh .githooks/pre-commit` limpio -> exit 0 (+ report "1 of 761").
2. estado gobernado roto staged + HOOK_FULL=1 -> exit 1 via validate.
3. masking-probe (`git rm --cached personal/Codex/STARTUP_PROMPT.md` + HOOK_FULL=1) -> exit 1.
4. A-SOBRE-RECHAZO probe (arriba).
5. `run_hook_fullmode_inventory_cases.py` -> 0 ; validate -> 0 ; scan_encoding -> 0 ; pin MATCH.

Scope: `.githooks/pre-commit` + `examples/` + pin en `validate.yml`. Nada de fondo (2E35F26E, epoch
1.14.0, dataset N=500, reservadas N=6). Emite `Analista-TASK-0289-*-verdict` con exit codes reales y
GO/NO-GO. Si NO-GO, di el minimo cambio.
