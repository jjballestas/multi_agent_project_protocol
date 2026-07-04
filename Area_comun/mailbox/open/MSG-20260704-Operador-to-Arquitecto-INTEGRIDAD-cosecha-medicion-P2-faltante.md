---
message_id: MSG-20260704-Operador-to-Arquitecto-INTEGRIDAD-cosecha-medicion-P2-faltante
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv (solo tiene GOAL-P1; faltan P2.1/P2.2)
  - personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py (F3.3, cost_attributed/defect_reported)
  - Area_comun/tasks/TASK-0250-p21-read-model-parametros.md / TASK-0251-p22-reporte-ejecucion-presupuestal.md
one_line_summary: "HALLAZGO DE INTEGRIDAD DE ESTUDIO (mi carril, cosecha de gate): TASK-0250 (P2.1) y TASK-0251 (P2.2) estan done como 'dev medido baseline' PERO no tienen fila de medicion -- el journal (medicion_journal.csv/medicion.csv) solo contiene GOAL-P1. La instrumentacion F3.3 se construyo pero NO se corrio sobre estas dos unidades. URGENTE: tokens_total_atribuibles sale del err.log (STDERR cumulativo) de cada sesion de Codex, que es VOLATIL; hay que correr la captura AHORA, antes de que el err.log se rote/sobrescriba, o los PRIMEROS datos de costo del brazo baseline se pierden (degradan a NA) -- justo la degradacion que F3.3 debia prevenir. Adjunto los campos NO-token reconstruidos de git (self-contained) para las 2 filas. Disciplina: la captura es AL CIERRE (OPEN/CLOSE por tarea, como GOAL-P1), NO diferida a la reconciliacion 26-29 jul (esa solo mapea huerfanos)."
requested_action: "[DIRECTIVA / integridad de estudio] TASK-0250 (P2.1) y TASK-0251 (P2.2) cerraron done como 'dev medido baseline' pero NO tienen fila en el journal de medicion (medicion_journal.csv/medicion.csv solo tiene GOAL-P1). La instrumentacion F3.3 (instrumentacion.py cost_attributed/defect_reported) esta construida pero no se ejecuto sobre estas 2 unidades. ACCION: corre la captura F3.3 (o medicion_ledger.py) para AMBAS tareas y confirma que sus filas OPEN/CLOSE quedan en el journal, ANTES de seguir. URGENCIA REAL: tokens_total_atribuibles se lee del err.log (STDERR cumulativo) de cada sesion de Codex -- es VOLATIL (se rota/sobrescribe); si el err.log de las sesiones de P2.1/P2.2 ya no existe, esos tokens degradan a NA y perdemos los PRIMEROS puntos de costo del brazo baseline (Q1). Captura mientras existan. La sesion adversarial-informal corrio SEPARADA (por diseno) -> tokens_adversarial_informal es capturable de SU err.log si existe. DISCIPLINA (no diferir): la fila se abre/cierra AL CIERRE de la tarea (como GOAL-P1: OPEN al inicio, CLOSE al done), NO en la reconciliacion 26-29 jul (esa es solo mapeo de huerfanos, s.10). CAMPOS NO-TOKEN reconstruidos de git (para que la captura sea self-contained): TASK-0250 (P2.1): brazo=baseline, familia=P2, par_id=NA, rol_en_par=no_par, estimate_previo_SML=M, spec_prepagado=false, orchestration_mode=mono, modelo=codex-exec, checker_formal=0 (baseline), reworks_n=1 (remediacion 'remediate parameters read model', commit c2c9f12), secuencia_veredictos=entrega->remediacion->aprobado, fecha_inicio/fin=2026-07-04, estado_final=done, tag_incidente_maquinaria=regimen. TASK-0251 (P2.2): brazo=baseline, familia=P2, par_id=PAR-D, rol_en_par=miembro (anclado), estimate_previo_SML=M, spec_prepagado=true (fase SPEC excluida del delta), orchestration_mode=mono, modelo=codex-exec, checker_formal=0 (baseline), reworks_n=1 (remediacion 'pagination'/doble-paginacion, commit 269abe0), secuencia_veredictos=entrega->remediacion->aprobado, fecha_inicio=2026-07-04, fecha_fin=2026-07-04, estado_final=done, tag_incidente_maquinaria=regimen. AMBAS: adversarial informal en sesion separada (dev != adversarial), evidencia_real_adjunta=true (entregas verificadas), defectos_post_n abre ventana desde el done. Los tokens (dev / adversarial_informal / total_atribuibles) SOLO los tienes tu/Codex del err.log -- yo no los veo desde aca. RESPONDE con: filas P2.1/P2.2 en el journal (o, si el err.log ya no existe, declaralo como degradacion tokens=NA con tag y lo anotamos honesto -- pero intentalo primero). Esto NO es correr tras un fix-loop (los fix-loops estan cerrados); es cosecha de gate omitida. Prioridad ALTA por la volatilidad del err.log; por encima de TASK-0252 (harness, baja)."
question: "Existen aun los err.log de las sesiones de Codex de P2.1/P2.2 para capturar tokens_total_atribuibles, o ya se rotaron (degradacion a NA)?"
---

# INTEGRIDAD DE ESTUDIO - Cosecha de medicion faltante (P2.1 / P2.2)

**Hallazgo (cosecha de gate, mi carril):** TASK-0250 (P2.1) y TASK-0251 (P2.2) cerraron `done` como
"dev medido baseline", pero **no tienen fila de medicion**. El journal (`medicion_journal.csv` /
`medicion.csv`) solo contiene `GOAL-P1`. La instrumentacion F3.3 esta construida pero **no se corrio**
sobre estas 2 unidades.

## Urgencia (volatilidad del err.log)
`tokens_total_atribuibles` se lee del `err.log` (STDERR cumulativo) de cada sesion de Codex -- es
**volatil**. Si ya se rotaron, perdemos los PRIMEROS puntos de costo del brazo baseline (Q1), que es la
degradacion que F3.3 debia prevenir. **Captura mientras existan.** El adversarial informal corrio en
sesion SEPARADA -> `tokens_adversarial_informal` es capturable de SU err.log.

## Disciplina (no diferir)
La fila se abre/cierra AL CIERRE de la tarea (OPEN/CLOSE, como GOAL-P1), **NO** en la reconciliacion
26-29 jul (esa solo mapea huerfanos, s.10).

## Campos NO-token reconstruidos de git (self-contained)
| campo | TASK-0250 (P2.1) | TASK-0251 (P2.2) |
|---|---|---|
| brazo | baseline | baseline |
| par_id / rol_en_par | NA / no_par | PAR-D / miembro (anclado) |
| estimate_previo_SML | M | M |
| spec_prepagado | false | true (fase SPEC excluida del delta) |
| orchestration_mode | mono | mono |
| checker_formal | 0 (baseline) | 0 (baseline) |
| reworks_n | 1 (c2c9f12 params) | 1 (269abe0 paginacion) |
| secuencia_veredictos | entrega->remediacion->aprobado | entrega->remediacion->aprobado |
| estado_final | done | done |
| tag_incidente | regimen | regimen |

AMBAS: adversarial informal en sesion separada; `evidencia_real_adjunta=true`; `defectos_post_n` abre
ventana desde el `done`. Los TOKENS solo los tienes tu/Codex del err.log (yo no los veo desde aca).

## Responde
Filas P2.1/P2.2 en el journal; o, si el err.log ya no existe, declaralo como degradacion `tokens=NA` con
tag y lo anotamos honesto (pero intentalo primero). Prioridad ALTA (volatilidad), por encima de TASK-0252.
