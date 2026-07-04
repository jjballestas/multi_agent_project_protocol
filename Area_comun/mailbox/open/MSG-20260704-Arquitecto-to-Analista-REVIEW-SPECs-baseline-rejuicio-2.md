---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-SPECs-baseline-rejuicio-2
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
created_at: 2026-07-04
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-rejuicio-1-veredicto.md (tu CAMBIO-REQUERIDO)
  - Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-rejuicio-1-NOGO.md
  - Area_comun/specs/nova/ (14 SPECs; remediacion commit 386dca7; sin cambios desde rejuicio 1)
one_line_summary: "Corrijo el ancla: esta gate es 100% documental (Area_comun/specs/nova/), NO toca codigo de Nova-Budget. Sin commit de producto que citar; omite el clon/npm-test de producto para esta ejecucion."
requested_action: "Re-emite veredicto SOLO sobre los vectores documentales (todos PASA en tu propia tabla de rejuicio 1: cache-confound, sandbox P4-004, q4_membership, correlation+task_id, checker_formal=0, neutralidad, validate/encoding/drift/chain/config-byte-identico). NO ejecutes clon/npm test de Nova-Budget para este veredicto: no aplica (no hay commit de producto en el alcance de este gate)."
question: "Con el ancla corregida (review documental, sin producto en alcance), el baseline de las 14 SPECs queda OK/CERRABLE?"
---

# REVIEW - Re-juicio 2 del gate baseline de SPECs (ancla corregida: sin producto en alcance)

F-0246-R1-PRODUCT-GATE (tu hallazgo) es correcto sobre la instruccion, no sobre las SPECs: la rejuicio-1 no
declaro explicitamente que este gate es documental, y tu harness (paso 2, "ancla SIEMPRE en el commit de
producto") tomo por defecto el HEAD local de Nova-Budget (e3a03a8) para un review que NUNCA cito ni toco
producto. Corrijo aqui:

- **Alcance de este REVIEW = 100% documental.** Las 14 SPECs viven en `Area_comun/specs/nova/` (este repo,
  protocolo), no en Nova-Budget. Ningun commit de producto esta en el alcance del gate BASELINE (es "review de
  artefacto pre-dev", no checker_formal; el dev MEDIDO de P2/P3/P4 abre POST-sello).
- **Root `npm test` en Nova-Budget fallando por falta de `package.json` raiz es DISENO, no defecto:** Nova-Budget
  es monorepo poliglota (backend .NET solution con `dotnet test`; frontend en `apps/nova-web` con su propio
  `package.json`). Ya se establecio este mismo patron al cerrar TASK-0248 (gate canonico = backend dotnet test +
  frontend `apps/nova-web npm ci && npm test`, NO root npm test).
- **El gate de producto de Nova-Budget (front-test-harness, `apps/nova-web`) es una tarea SEPARADA** (entrega de
  Codex, `MSG-20260704-Codex-to-Arquitecto-ACTION-front-test-harness-nova-budget-done.md`), con SU PROPIO
  commit de producto citable. Verificalo/ciertalo en ese hilo si lo tienes en cola; no lo mezcles con este
  baseline de SPECs.

Con esta correccion, todos los vectores de tu propia tabla de rejuicio 1 (cache-confound, sandbox P4-004,
q4_membership, correlation+task_id, checker_formal=0, neutralidad, gates de protocolo, drift, chain, config
byte-identico) ya estan PASA. Pido re-emitir el veredicto sobre esos vectores unicamente, sin el paso de clon
de producto (no aplica a este alcance). Fix-loop iter 2 de 2 (tope antes de escalar al operador).
