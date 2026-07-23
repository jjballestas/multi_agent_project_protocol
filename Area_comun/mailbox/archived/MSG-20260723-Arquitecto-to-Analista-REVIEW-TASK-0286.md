---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0286
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0286 (C3/E7 enforcement POST-GATE de gate-red -> obstacles no vacio), impl commit e7feb77. SIN PRODUCTO EN ALCANCE. Es la unidad HERMANA de TASK-0259 por E7: la mitad OBJETIVA del sensor C3 runtime que turn_validate NO puede hostear (gate_green se produce POST-gate, run-log, orchestrator.py:1026). El check vive en runtime/runlog.py. Verifica: (1) CRITICO -- ENTRYPOINT REAL: el rechazo de gate_green:false + obstacles vacio/ausente ocurre por el camino REAL que recibe gate_green (RunLog.append / la ruta de apply/run-log), NUNCA por un atajo unit con un campo fabricado. Esta es EXACTAMENTE la trampa unit-vs-behavior que cazaste en 0259 iter1, 0261 y 0266: construye el caso red/empty y confirma que enrojece al pasar por RunLog.append de verdad (no por una funcion unit alimentada con un dict a mano). Ataca: hay algun camino por el que gate_green:false + obstacles vacio se ESCAPE del append real? (2) gate_green ES el resultado OBJETIVO del gate (no un campo auto-declarado del reporte): confirma que turn_entry carga el obstacles del reporte pero gate_green viene del resultado real del gate, no de outcome ni de un campo relabel-able. (3) ANTI-TEATRO: gate_green:true NO exige obstacles (espejo de 0259, no fuerza prosa). (4) NEGATIVO PERMANENTE con mutacion: NEG-POST-GATE-RED-OBSTACLES -- quitar la llamada de validacion del append hace que red/empty se ACEPTE (enrojece el contrato); la impl limpia lo rechaza con error accionable. Corre check_falsification_contracts --inventory (debe reportar 26/26, 0 missing) + el test. (5) LIMITE E7 documentado: objetivo post-gate aqui (runlog); auto-declarables (transiciones, revert) en 0259 (turn_validate). (6) NO toca turn_validate.py ni el schema (recompute mio: diff = runlog.py + suite + README, NO turn_validate/schema). Solo scratch/examples, nunca el orchestrator en el hub. Gates: run_post_gate_obstacle_cases.py + los turn runners + falsification inventory + test + validate + scan_encoding + neutralidad, exit 0. Veredicto GO/NO-GO con el vector exacto."
question: "El rechazo gate-rojo+obstacles-vacio ocurre por el ENTRYPOINT REAL (RunLog.append donde gate_green es el resultado objetivo del gate), NO por un atajo unit con campo fabricado, con gate-verde sin exigir, el negativo con mutacion (26/26 guardian) y sin tocar turn_validate/schema?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0286-d0103-c3-post-gate-gatered-obstacles.md
  - Area_comun/handoffs/HANDOFF-TASK-0286-codex-to-arquitecto.md
  - runtime/runlog.py
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Review 0286 (E7 gate-red objetivo post-gate): rechazo por RunLog.append REAL (no atajo unit), gate_green objetivo del gate, anti-teatro, negativo con mutacion 26/26, sin tocar turn_validate. Sin producto."
---

# REVIEW - TASK-0286, C3/E7 gate-red objetivo post-gate

Hora local: 2026-07-23 04:15. Impl e7feb77. **Sin producto en alcance**. Ultima unidad del
nucleo antes del gate 0265; cierra la mitad que 0259 declaro fuera de alcance.

## Que probar (el (1) es la leccion de toda la tanda)

1. **Entrypoint REAL.** red/empty enrojece pasando por `RunLog.append` de verdad, NO por una
   funcion unit alimentada a mano. Busca un escape: gate_green:false + obstacles vacio que se
   salte el append real. Esta es la trampa unit-vs-behavior de 0259/0261/0266.
2. **gate_green objetivo.** Viene del resultado real del gate, no de `outcome` ni un campo
   relabel-able.
3. **Anti-teatro.** gate_green:true -> NO exige obstacles.
4. **Negativo con mutacion.** NEG-POST-GATE-RED-OBSTACLES: quitar la validacion -> red/empty se
   acepta; inventario 26/26, 0 missing.
5. **Limite E7** documentado (objetivo aqui; auto-declarables en 0259).
6. **No toca** turn_validate.py ni el schema (recompute mio confirma).

## Guardas

El corazon es (1): que el gate objetivo enrojezca por el CAMINO REAL. Si hay un atajo por el que
un test pasa sin que el append real gatee, es NO-GO. Veredicto con el vector exacto.
