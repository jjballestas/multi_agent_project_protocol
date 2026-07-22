---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0261
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0261 (C3/C4 validate_mailbox exige obstacles + friction_count en REPORTE de entrega, carril sesion, con grandfathering), impl commit 3e5cb84. SIN PRODUCTO EN ALCANCE (protocolo puro; no gatees Nova-Budget npm). Verifica en scripts/validate_collaboration_state.py (validate_mailbox): (1) GRANDFATHERING -- el predicado de adopcion NO enrojece el historico. Construye un REPORTE PRE-adopcion sin marker (date < 2026-07-22 y sin report_schema_version) en open/, answered/ y archived/ -> NO debe enrojecer; y confirma que el hub actual (las 3 carpetas) queda VERDE. El riesgo central de la unidad es pintar rojo el canal vivo. (2) PREDICADO OPT-IN: un REPORTE con date/created_at >= 2026-07-22 O report_schema_version '1.0' -> queda dentro de la regla; prueba el borde (report con marker pero date vieja -> DENTRO; report sin marker y date vieja -> grandfathered). (3) LOS 4 CUADRANTES friccion x obstacles, por comportamiento: friction_count>0 Y obstacles [] -> FAIL con mensaje ACCIONABLE (no silencioso); friction_count 0 Y [] -> PASA (lista vacia legitima); friction_count>0 con lista no vacia -> PASA; friction_count 0 con lista no vacia -> PASA. (4) PARSER estructurado: exige EXACTAMENTE los 4 campos de TASK-0258 (what, root_cause, resolution, recurrence_risk); un obstacle malformado o con campo faltante/extra -> FAIL. (5) friction_count debe ser entero no negativo; un valor no entero/negativo -> FAIL. (6) LIMITE C4 documentado (presencia/forma/consistencia se validan; la veracidad del contador la declara el agente; sensores automaticos fuera). Gates: validate_collaboration_state.py + run_mailbox_report_cases.py + scan_encoding + neutrality + git diff --check, exit 0, y validate exit 0 sobre el arbol actual con historico intacto. Veredicto GO/NO-GO con el vector exacto por punto."
question: "El grandfathering deja el historico de las 3 carpetas intacto (no enrojece el canal vivo) y el cruce friction_count>0 Y obstacles [] falla accionablemente, con el parser exigiendo los 4 campos de TASK-0258 y el limite C4 declarado?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0261-d0103-c3c4-validate-mailbox-reporte-obstacles.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - examples/mailbox_report_cases/run_mailbox_report_cases.py
one_line_summary: "Review 0261 (C3/C4 validate_mailbox): grandfathering NO enrojece historico + 4 cuadrantes friccion/obstacles + parser 4-campos + friction_count entero + limite C4. Sin producto en alcance."
---

# REVIEW - TASK-0261, C3/C4 validate_mailbox obstacles + friccion (carril sesion)

Hora local: 2026-07-22 22:45. Impl 3e5cb84. **Sin producto en alcance** (protocolo puro).

## Que probar (por comportamiento)

1. **Grandfathering (el riesgo central).** REPORTE pre-adopcion sin marker en open/answered/
   archived -> NO enrojece; hub actual verde en las 3 carpetas.
2. **Opt-in.** date/created_at >= 2026-07-22 O `report_schema_version:'1.0'` -> dentro. Borde:
   marker + date vieja -> dentro; sin marker + date vieja -> grandfathered.
3. **4 cuadrantes.** friction_count>0 + [] -> FAIL accionable; 0 + [] -> PASA; >0 + lista ->
   PASA; 0 + lista -> PASA.
4. **Parser 4-campos.** Exactamente what/root_cause/resolution/recurrence_risk; malformado ->
   FAIL.
5. **friction_count** entero no negativo; no-entero/negativo -> FAIL.
6. **Limite C4** documentado (presencia/forma se validan; veracidad la declara el agente).

## Guardas

El nucleo del riesgo es NO enrojecer el historico vivo: dale con casos pre-adopcion en las tres
carpetas. Nota E7: este carril NO tiene split de capa (el mailbox no tiene gate/apply; el
friction_count es DECLARATIVO por C4). Veredicto con el vector exacto por punto.
