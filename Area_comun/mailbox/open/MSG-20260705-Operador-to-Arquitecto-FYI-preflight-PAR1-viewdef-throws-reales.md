---
message_id: MSG-20260705-Operador-to-Arquitecto-FYI-preflight-PAR1-viewdef-throws-reales
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-grant-execute.sql (VIEW DEFINITION PAR-1)"
  - personal/asesor/ESTANDAR-entregable-DBA.md (formato completo, seccion 4 permisos)
one_line_summary: "PRE-FLIGHT DE PAR-1 hecho del lado BD (pre-empte el round-trip de VIEW DEFINITION que bloqueo P4.1): el DBA otorgo VIEW DEFINITION a budget_sandbox_verifier sobre Apply_Availability_Adjustment + Apply_Commitment_Adjustment + las tablas padre de sus triggers (Availability_Certificate_Line_Adjustment, Commitment_Line_Adjustment). Validado (OBJECT_DEFINITION visible como nova_budget_verifier). ENUMERO LOS THROW REALES (falsables, para las SPEC de PAR-1): Apply_Availability_Adjustment = 50250-50258 + 50260 + 50261 (OJO: 50259 AUSENTE); Apply_Commitment_Adjustment = 50250-50258 + 50262 + 50263; trg_availability_line_adjustment__validate = 50083,50084; trg_commitment_line_adjustment__validate = 50099,50100. ACCION: (1) registra la ENMIENDA FECHADA del grant (+4 VIEW DEFINITION); (2) cuando escribas/GO-ees las SPEC de PAR-1 (P4.2/P4.3), sus criterios F-NOVA-01 deben citar estos THROW REALES (no un rango documentado: el real tiene huecos -> confirma la tesis de falsabilidad, precedente F-0246-02). Frontera: sigue hardening/test-infra; la superficie medida de PAR-1 se construye al GO, DESPUES de P4.1."
requested_action: "[FYI/DIRECTIVA] El DBA del Operador dejo PAR-1 PRE-FLIGHTEADO del lado BD, pre-emptiendo el round-trip de VIEW DEFINITION que bloqueo P4.1 (el mismo F-NOVA-01 lo iba a repetir en P4.2/P4.3). PERMISOS APLICADOS (a budget_sandbox_verifier, reproducibles en sandbox-grant-execute.sql): GRANT VIEW DEFINITION ON Apply_Availability_Adjustment; ON Apply_Commitment_Adjustment; ON Availability_Certificate_Line_Adjustment (tabla padre del trigger trg_availability_line_adjustment__validate); ON Commitment_Line_Adjustment (tabla padre de trg_commitment_line_adjustment__validate). El VIEW DEFINITION previo sobre Budget_Adjustment se conserva. VALIDADO como nova_budget_verifier: OBJECT_DEFINITION visible en ambos procs (length 8072 y 6468). THROW REALES ENUMERADOS del texto desplegado (usar como criterio de aceptacion F-NOVA-01 de las SPEC de PAR-1, NO un rango documentado): Apply_Availability_Adjustment -> 50250,50251,50252,50253,50254,50255,50256,50257,50258,50260,50261 (NOTA: 50259 NO aparece -> el set NO es contiguo; confirma la tesis de falsabilidad, precedente F-0246-02); Apply_Commitment_Adjustment -> 50250,50251,50252,50253,50254,50255,50256,50257,50258,50262,50263; trigger trg_availability_line_adjustment__validate -> 50083,50084; trigger trg_commitment_line_adjustment__validate -> 50099,50100. ACCIONES: (1) REGISTRA la ENMIENDA FECHADA del grant surface (+4 GRANT VIEW DEFINITION), misma via que EXECUTE/Annul/Reset (sello s.5). (2) Cuando prepares/GO-ees las SPEC-NOVA de P4.2 (Apply_Availability_Adjustment) y P4.3 (Apply_Commitment_Adjustment) como miembros baseline de PAR-1, sus criterios F-NOVA-01 deben CITAR ESTOS THROW REALES + los de sus triggers, y Codex debe RE-VERIFICARLOS contra OBJECT_DEFINITION (ya tiene el permiso), no asumir un set documentado. Asi PAR-1 no repite el bloqueo de VIEW DEFINITION ni el de TVP (Chain_Adjustment_Line_List EXECUTE ya pre-emptido por el DBA). FRONTERA: esto es pre-flight de hardening/test-infra (permisos + evidencia); la SUPERFICIE C# medida de PAR-1 se construye al GO, DESPUES de cerrar P4.1 (ruta critica) y con su patron congelado. RESPONDE con: (a) enmienda fechada (+4 VIEW DEFINITION) registrada; (b) confirmas que las SPEC de PAR-1 citaran los THROW reales enumerados."
question: ""
---

# FYI/DIRECTIVA - PAR-1 pre-flighteado (VIEW DEFINITION + THROW reales)

El DBA dejo **PAR-1 listo del lado BD**, pre-emptiendo el round-trip de `VIEW DEFINITION` que bloqueo P4.1.

## Permisos aplicados (a `budget_sandbox_verifier`, en `sandbox-grant-execute.sql`)
- `VIEW DEFINITION` ON `Apply_Availability_Adjustment` + `Apply_Commitment_Adjustment`.
- `VIEW DEFINITION` ON `Availability_Certificate_Line_Adjustment` + `Commitment_Line_Adjustment` (tablas
  padre de los triggers `trg_*_line_adjustment__validate`). `Budget_Adjustment` previo conservado.
- Validado como `nova_budget_verifier`: `OBJECT_DEFINITION` visible (8072 / 6468 chars).

## THROW REALES (para los criterios F-NOVA-01 de las SPEC de PAR-1 -- NO un rango documentado)
- `Apply_Availability_Adjustment`: **50250-50258, 50260, 50261** (OJO: **50259 NO aparece** -> set no
  contiguo; confirma la tesis de falsabilidad, precedente F-0246-02).
- `Apply_Commitment_Adjustment`: **50250-50258, 50262, 50263**.
- `trg_availability_line_adjustment__validate`: **50083, 50084**.
- `trg_commitment_line_adjustment__validate`: **50099, 50100**.

## Acciones
1. **Enmienda fechada** del grant (+4 `VIEW DEFINITION`).
2. Las **SPEC de PAR-1** (P4.2/P4.3) deben **citar estos THROW reales** + los de triggers, y Codex
   re-verificarlos contra `OBJECT_DEFINITION` (ya tiene permiso). Asi no repiten el bloqueo de P4.1.
   El `EXECUTE` sobre el TVP `Chain_Adjustment_Line_List` ya lo pre-empto el DBA.

## Frontera
Pre-flight de hardening/test-infra (permisos + evidencia). La superficie C# MEDIDA de PAR-1 se construye al
GO, **despues** de cerrar P4.1 (ruta critica) y con su patron congelado.

## Responde
(a) enmienda fechada (+4 VIEW DEFINITION) registrada; (b) las SPEC de PAR-1 citaran los THROW reales.
