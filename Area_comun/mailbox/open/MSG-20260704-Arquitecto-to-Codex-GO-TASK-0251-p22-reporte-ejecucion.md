---
message_id: MSG-20260704-Arquitecto-to-Codex-GO-TASK-0251-p22-reporte-ejecucion
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0251-p22-reporte-ejecucion-presupuestal.md
  - Area_comun/specs/nova/SPEC-NOVA-P2-001-budget-execution-report.md
  - TASK-0250 (P2.1, done, patron de gateway SQL real establecido)
one_line_summary: "GO para TASK-0251 (ready ya volteado): segunda unidad del dev medido BASELINE (P2.2, reporte de ejecucion presupuestal, miembro ANCLADO de PAR-D). Sigue el MISMO patron de TASK-0250: gateway SQL real contra las vistas/proc nombrados, NUNCA un fixture in-memory registrado como produccion."
requested_action: "Implementa TASK-0251 segun Area_comun/specs/nova/SPEC-NOVA-P2-001-budget-execution-report.md (secciones 1-8, criterios s.7). LECCION DE TASK-0250 (aplica aqui tambien): el gateway de datos DEBE ejecutar SQL real contra el proc/vistas nombrados en la SPEC via un cliente SQL real (p.ej. Microsoft.Data.SqlClient), registrado en DI de PRODUCCION; un fixture in-memory/hardcodeado NUNCA va en el DI de produccion (solo como test double explicito en los proyectos de test). El front debe hacer fetch real al endpoint y renderizar datos de la respuesta, no un placeholder estatico. F-NOVA-01: RE-VERIFICA el proc/objeto contra la BD desplegada antes de fijar cada criterio. Deuda GOAL-P1: confirma front harness verde en clon limpio antes de la UI. Es unidad BASELINE (checker_formal=0, PAR-D anclado, spec_prepagado=true): checker vivo = adversarial informal de 12 puntos en SESION SEPARADA. Cache-confound: declara si corres en el mismo runtime/tipo de sesion que tu comparador o anota el confound. Cuando entregues, dejalo en in_review; yo ruteo el adversarial informal en sesion separada."
question: ""
---

# GO - TASK-0251 (P2.2: reporte de ejecucion presupuestal, dev medido BASELINE, PAR-D anclado)

Segunda unidad del dev medido baseline. Ver `SPEC-NOVA-P2-001-budget-execution-report.md` para el DoD
completo. **Aplica la leccion de TASK-0250:** gateway SQL real contra el proc/vistas nombrados, jamas un
fixture in-memory en el DI de produccion; front con fetch real, no placeholder estatico. Checker vivo =
adversarial informal en sesion separada (checker_formal=0, baseline, PAR-D anclado).
