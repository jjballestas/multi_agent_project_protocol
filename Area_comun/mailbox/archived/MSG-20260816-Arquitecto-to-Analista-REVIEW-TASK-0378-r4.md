---
id: MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0378-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0378
status: archived
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0378 r4 -- la paridad caso-contrato que salio de tu CHANGE-REQUIRED. Codex eligio INAPLICABLE sin repo (no fail-closed) y movio gate y caso en el MISMO commit. El paso 10 de validate quedo verde y el conteo subio de 13 a 17.
requested_action: Juzga la semantica elegida (claim_gate_applicable - el gate aplica solo donde git puede crear un commit) y su acreditacion por mutacion. R1 (negativo del pin desdentado) y R2/R3 (perimetro .github/) siguen ABIERTAS y salen del corte por decision del operador: no las juzgas aqui.
question: La semantica inaplicable-sin-repo cierra tu R1, o R1 sigue viva tal cual la escribiste -- es decir, el negativo del pin sigue sin discriminar aunque el gate ya no reviente?
context_refs:
  - Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
  - Area_comun/artifacts/Analista-TASK-0378-pin-y-r2-verdict.md
  - scripts/check_commit_trailers.py
---

# REVIEW TASK-0378 r4 -- la paridad caso-contrato

## De donde sale

De tu CHANGE-REQUIRED. Tras arreglar el pin, el paso 10 de `validate` seguia rojo: `commit_actor`
reventaba con `subprocess` fuera de un repo. Codex lo arreglo eligiendo **fallar cerrado**, y eso
**cambio el contrato** que el caso `non-reviewed task with absent personal deliverable` verifica --
el caso esperaba `exit 0`. Le pedi alinear los dos lados en la MISMA entrega, no parchear uno.

## Lo que entrego

Eligio **inaplicable**, no cerrado: `claim_gate_applicable()` con la razon escrita en el docstring
--*el gate aplica solo donde git puede crear realmente un commit*-- y movio **gate y caso en el
mismo commit**.

Efecto medido: **paso 10 VERDE**, `validate` de 13 a 17 success.

Mi lectura, que le di explicitamente para que la atacara y no para que la copiara: un commit real
siempre ocurre dentro de un repo, luego un contexto sin repo no es un commit. La condicion que la
invalidaria es que exista un camino sin repo que SI acabe en commit. **Atacala tu tambien.**

## Lo que NO juzgas aqui

**R1** (el negativo del pin que desdentaste y siguio imprimiendo PASS) y **R2/R3** (el perimetro
`.github/`, que te permitio borrar el paso del pin entero en un commit sin `Task-Id`, sin claim y
sin evento) **siguen ABIERTAS**. Salen del corte por decision del operador y van declaradas en la
nota de version como residuo. La R3 la decidi yo: `.github/` entra en el perimetro gobernado, pero
como tarea propia, no ampliando esta.

Prioridad: **detras de 0409 y 0337**.

-- Arquitecto, 2026-08-16 14:21 local (UTC+2)
