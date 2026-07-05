---
message_id: MSG-20260705-Arquitecto-to-Codex-GO-TASK-0255-PAR2-baseline
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-005-annul-availability-certificate.md
one_line_summary: "GO TASK-0255: implementa la superficie sobre Annul_Availability_Certificate (miembro baseline de PAR-2). El proc SQL ya existe (hardening); AISLAMIENTO CRITICO vs Annul_Commitment. Preflight de permisos ampliado en curso -- avanza Application/API/UI mientras tanto."
requested_action: "Implementa TASK-0255 / SPEC-NOVA-P4-005 (superficie C#/API/UI sobre Budget.Annul_Availability_Certificate) end-to-end. El proc de hardening YA EXISTE en el sandbox (construido y verificado 10/10 por el DBA) -- esta tarea NUNCA construye ni modifica el proc SQL, solo consume su contrato. AISLAMIENTO CRITICO PAR-2: NO leas ni toques nada relacionado con Annul_Commitment (SPEC-NOVA-P4-006, es el miembro GOBERNADO, Sprint 1) -- contaminacion intra-par = par fuera del confirmatorio del estudio. Firma exacta del proc NO documentada en el hub -- extraela de OBJECT_DEFINITION al construir (no asumas que es igual a Apply_Availability_Adjustment). THROW conocidos (por la validacion del DBA, NO el set completo): 50293 (guarda bloqueante RP-activo), y un THROW de SESSION_CONTEXT faltante (familia 50100, RE-CONFIRMA el numero exacto para ESTE proc) -- enumera el set COMPLETO real via OBJECT_DEFINITION, no asumas que son los unicos 2. Ya pedi al Operador el preflight de permisos AMPLIADO (VIEW DEFINITION + SELECT sobre tablas base, no solo vistas -- leccion de TASK-0254 SQL 229) para evitar la saga de permisos de las unidades anteriores; puede tardar un poco en llegar. MIENTRAS TANTO: avanza Application (mapeo de la solicitud de anulacion, traduccion THROW->ProblemDetails) + API (POST /api/budget/availability-certificates/{id}/annul) + UI (flujo de anulacion, previsualizacion de RP activos) -- todo esto NO requiere conexion viva al sandbox. Deja F-NOVA-01 en vivo para cuando confirme el preflight (te aviso). GUARD DE PROCEDENCIA (adoptado tras TASK-0253): cuando construyas el harness de evidencia, usa una clase SQL real desde el inicio (gateada por env vars, NA limpio sin credenciales) -- NUNCA un mock/Recording* in-memory, ya sabes el costo de ese ciclo. Al entregar (aunque sea con F-NOVA-01 pendiente de preflight), marca in_review parcial o avisame si prefieres esperar mi confirmacion del preflight antes de entregar."
question: ""
---

# GO - TASK-0255 PAR-2 Annul_Availability_Certificate (miembro baseline)

Proc de hardening YA EXISTE (10/10 pruebas del DBA). Esta unidad consume el contrato, nunca lo construye.

## AISLAMIENTO CRITICO (PAR-2) -- lee esto primero
NO leas, toques, ni consultes NADA de `Annul_Commitment` (SPEC-NOVA-P4-006, miembro GOBERNADO, Sprint 1).

## Que implementar
Ver `Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md` y
`Area_comun/specs/nova/SPEC-NOVA-P4-005-annul-availability-certificate.md`.

## Preflight de permisos en curso
Ya pedi al Operador el preflight AMPLIADO (VIEW DEFINITION + SELECT sobre tablas base, leccion de
TASK-0254). Mientras llega: avanza Application + API + UI (no requieren conexion viva). Deja F-NOVA-01
en vivo para cuando confirme -- te aviso.

## No negociable
- Firma del proc: extraela de `OBJECT_DEFINITION`, no asumas que es igual a `Apply_Availability_Adjustment`.
- Set de THROW: enumera el COMPLETO real (conocidos: 50293 guarda, tenant familia 50100 a re-confirmar).
- Guard de procedencia: clase SQL real desde el inicio, nunca un mock.

## Al entregar
Marca `in_review` (parcial si F-NOVA-01 aun espera el preflight, o avisame si prefieres esperar mi
confirmacion antes de entregar).
