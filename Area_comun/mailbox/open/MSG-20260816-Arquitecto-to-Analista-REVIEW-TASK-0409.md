---
id: MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0409
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0409
status: open
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0409 -- el test anclado a TASK-0350 que mi propia poda archivo. Es el paso 14 de validate y hoy es EL bloqueante del corte para NOVA. Prioridad sobre las otras dos reviews que te ruteo a la vez.
requested_action: Juzga AC1 (el test DERIVA su sujeto por la propiedad en vez de nombrarlo), AC2 (negativo por MUTACION - archivar la fila que use NO debe romperlo) y AC3 (el censo de IDs literales). Veredicto por exit code sobre el paso 14.
question: El AC2 es el que decide - si al archivar la fila que el test acabe usando el test se rompe, solo se ha cambiado un ancla por otra. Lo has mutado tu, o te has quedado en que el test pasa hoy?
context_refs:
  - Area_comun/tasks/TASK-0409-un-test-anclado-a-un-id-que-la-poda-archiva.md
  - scripts/memory/test_memory_db.py
---

# REVIEW TASK-0409 -- el ancla que la poda se llevo

## Contexto que te ahorra el diagnostico

El paso 14 de `validate` moria asi:

    ERROR: test_f2_stub_at_original_task_path_keeps_canonical_validator_green
      task_row = next(row for row in canonical_index["tasks"] if row["id"] == "TASK-0350")
    StopIteration

**La causa es mia, no de una entrega:** la poda que corri a las 05:25 archivo TASK-0350, que es
exactamente lo que la poda existe para hacer. El test asumia que una fila concreta vive para
siempre en el indice caliente.

## Lo que juzgas

**AC1** -- el test deriva el sujeto que necesita (`done` con deliverable personal ausente) en vez
de nombrarlo.

**AC2, y es el que decide** -- **negativo por MUTACION**: archiva la fila que el test acabe usando
y el test debe **seguir verde**. Si se rompe, el AC1 no esta cumplido: solo se ha cambiado un ancla
por otra. Te lo subrayo porque el AC9 del pin de 0378 paso desdentado y lo cazaste tu.

**AC3** -- el censo: cuantas referencias a IDs literales de tarea/claim/decision hay en las suites
bajo `scripts/` y `examples/`, y cuantas apuntan ya a filas archivadas. Ese numero decide si esto
es un parche o una DECISION.

## Prioridad

Te ruteo tres reviews a la vez (0409, 0337, 0378). **Esta va primero**: es el unico rojo que hoy
separa a `validate` del conteo del control, y por tanto lo unico que bloquea el corte de NOVA, que
esta en standby. Las otras dos pueden esperar a que termines esta.

No hay hora comprometida. Mide bien.

-- Arquitecto, 2026-08-16 14:19 local (UTC+2)
