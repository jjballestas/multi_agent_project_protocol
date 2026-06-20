---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-ratifica-TASK-0132
task_id: TASK-0132
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: Arquitecto
one_line_summary: "GO de ratificacion: apruebo OPCION A (routing banked como TASK-0131 cerrado + TASK-0132 para el RESTO de la conformidad de diseno; NO reabrir routing). G4 = capa-entidad (a), aprobado. Promueve TASK-0132 por submit_intent, maker=Codex/checker=Arquitecto. Condicion de cierre: AC12 (routing-comportamiento) + AC13 (conformidad-diseno) quedan PERMANENTES en SPEC-0086. Etapa 5 roster sigue DEFERIDA."
requested_action: "Promueve TASK-0132 por submit_intent y arranca con Codex (maker). Alcance ratificado = el RESTO de la conformidad (NO rehacer el routing verde de TASK-0131): Backlog = kanban (design 4.3: columnas por estado + claims + filtro por agente); proyecto = capa-ENTIDAD `{id,name,kind,source,state}` alimentada por los repos bajo Zeus pero consumida por la UI como entidad, no como ruta de disco (design 4.8, honra DECISION-0050); confirmar redaccion PII en la vista del ledger (design 4.5 / AC11); adoptar tokens del design-system (tipografia/espaciado/radius que styles.css omite); fidelidad por pantalla contra los previews de design/interface/components. CONDICION DE CIERRE: agrega a SPEC-0086 AC12 (AC-ROUTING, test de comportamiento permanente: clic en X -> solo panel X visible, demas ocultos, topbar/integrity-band presentes; ya satisfecho por TASK-0131, se vuelve permanente) y AC13 (AC-CONFORMIDAD-DISENO permanente: las 7 vistas existen, navegables, cada una = su pantalla del design brief, Backlog=kanban). Gates: validate con/sin secretos exit 0, drift 0, #4 epoca 1.14.0 intacta, neutralidad, node --test/CI verde; al cerrar npm start ejecutable y las 7 vistas navegan. maker=Codex / checker=Arquitecto, reproduccion desde clon limpio. Reporta el cierre en canonico."
question: none
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-TASK-0132-front-etapa6.1.md
  - Area_comun/tasks/TASK-0131-arquitecto-front-view-routing.md
  - Area_comun/mailbox/open/MSG-20260620-Arquitecto-to-Operador-etapa6.1-draft.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - personal/operador/18_Asistente_gap-diseno-vs-front-etapa6.md
deadline_or_blocking_level: normal
---

# GO - ratifico TASK-0132 (opcion A) + G4 = capa-entidad

Ratifico tu recomendacion: **OPCION A** -- routing ya cerrado y verificado (TASK-0131, Codex 17/17), y
**TASK-0132 cubre solo el RESTO** de la conformidad de diseno. **No reabrir routing.** Promueve TASK-0132 por
`submit_intent`; maker=Codex / checker=Arquitecto.

- **G4 aprobado = capa-entidad (a):** la UI consume la entidad-proyecto, no el path; honra design 4.8 sin
  romper DECISION-0050. Buena decision.
- **Condicion de cierre (innegociable):** AC12 (routing-comportamiento, ya satisfecho por TASK-0131) y AC13
  (conformidad-diseno) quedan **PERMANENTES en SPEC-0086**. Sin eso, un refactor futuro puede volver a apilar
  las vistas y CI seguiria verde -- es justo el hueco que abrio esta etapa.
- **Alcance:** Backlog kanban (4.3), proyecto-entidad (4.8), confirmar PII en el ledger (4.5), tokens del
  design-system, fidelidad por pantalla. Etapa 5 roster (RF-9) sigue DEFERIDA.

Verifico tu cierre en canonico. Canal ASCII.
