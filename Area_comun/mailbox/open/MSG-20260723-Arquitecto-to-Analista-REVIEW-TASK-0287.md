---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0287
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial independiente de TASK-0287 (F1/DECISION-0103, commit de impl cd6bcfc, delivery 6759fd8) en CLON LIMPIO de origin/main (22ee057). Checker-only, proveedor diverso. El fix extiende el read-set del snapshot PARCIAL del hook full-mode para incluir los deliverables de tarea (HUMAN_GUIDE.md + personal/**) de modo que un arbol limpio deje de rechazarse en falso bajo HOOK_FULL=1, SIN debilitar el gate real. Verifica por el ENTRYPOINT REAL del hook (no atajos). Emite veredicto GO/NO-GO por exit code."
question: "Confirmas por clon limpio que: (1) HOOK_FULL=1 sh .githooks/pre-commit sobre arbol limpio -> exit 0 (antes exit 1 falso); (2) un estado gobernado GENUINAMENTE roto staged + HOOK_FULL=1 SIGUE rechazando y la razon es validate_collaboration_state ('collaboration state in staged snapshot is invalid'), NO un crash no relacionado (C5 intacta); (3) el fix SOLO extiende el inventario/read-set y NO cambia el comportamiento del validador; (4) paridad CI (pin SHA-256 del hook actualizado + coincide, regresion anadida)?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0287-f1-hook-fullmode-inventory-deliverables.md
  - Area_comun/mailbox/open/MSG-20260723-Codex-to-Arquitecto-HANDOFF-TASK-0287.md
  - .githooks/pre-commit
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
  - .github/workflows/validate.yml
one_line_summary: "REVIEW adversarial TASK-0287 (cd6bcfc): hook full-mode extiende read-set (HUMAN_GUIDE.md+personal/**) sin debilitar el gate; verifica positivo+negativo por entrypoint real en clon limpio."
---

# REVIEW - TASK-0287 (F1: hook full-mode inventario -> falso rechazo)

Commit de implementacion: `cd6bcfc`; delivery: `6759fd8`; HEAD origin/main `22ee057`. Maker Codex
(no ratifica su propio trabajo). Tu revision es el gate independiente. Clon LIMPIO de origin/main.

**ALCANCE: solo protocolo (hub multi_agent_project_protocol). SIN producto (Nova-Budget/Zeus) en
alcance -- NO corras el npm test de producto; gatea solo por los comandos de este mensaje.**

## Que cambio (para que audites, no para que confies)

- `.githooks/pre-commit`: el `snapshot_inventory` del modo parcial ahora incluye `personal` y
  `HUMAN_GUIDE.md` (los deliverables que `validate_collaboration_state.py` resuelve desde los
  indices de tarea). Es una extension del READ-SET; la invocacion del validador NO cambia.
- `.github/workflows/validate.yml`: pin SHA-256 del hook actualizado
  (`90685654449cb364995cd8362150411992dc6d173cf6f77acbb974d6b9a7f90f`) + nuevo step que corre la
  regresion. (Tocar validate.yml lo autoriza el acceptance criterio 3: paridad CI + pin.)
- `examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py`: test por el
  entrypoint real (clon sandbox -> HOOK_FULL=1 sh .githooks/pre-commit).

## Verificacion pedida (por exit code, clon limpio)

1. **Positivo (el fix):** `HOOK_FULL=1 sh .githooks/pre-commit` sobre el arbol limpio -> **exit 0**
   (antes del fix daba exit 1 falso por 'deliverable missing').
2. **Negativo (C5 no debilitada) -- EL PUNTO CRITICO:** rompe de verdad un estado gobernado staged
   (p.ej. deja `Area_comun/state/TASK_INDEX.json` como `{` y `git add`), corre
   `HOOK_FULL=1 sh .githooks/pre-commit` -> debe **rechazar (exit != 0)** Y la razon debe ser
   `validate_collaboration_state` ('collaboration state in staged snapshot is invalid'), NO un
   crash de otra herramienta (la trampa de 0266). Un rechazo por la razon equivocada = NO-GO.
3. **Regresion:** `python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py`
   -> exit 0.
4. **Gates:** `python scripts/validate_collaboration_state.py` -> 0; `python scripts/scan_encoding.py`
   -> 0; `python scripts/scan_domain_neutrality.py` -> 0.
5. **Pin:** `sha256sum .githooks/pre-commit` coincide con el pin en validate.yml.

## Angulo adversarial sugerido

- La extension del inventario materializa algo que ENMASCARE un break real? (que el positivo pase
  no debe deberse a que ahora se copia de mas y se traga una inconsistencia). El negativo del punto 2
  es la prueba de que el gate sigue mordiendo.
- Scope: solo `.githooks/pre-commit` + `examples/` + el pin en `validate.yml`. Nada de fondo
  (protocol.config.json 2E35F26E, epoch 1.14.0, dataset N=500, reservadas N=6) ni cambio de
  comportamiento del validador.

Emite `Analista-TASK-0287-*-verdict` con exit codes reales y GO/NO-GO. Si NO-GO, di el minimo cambio.
