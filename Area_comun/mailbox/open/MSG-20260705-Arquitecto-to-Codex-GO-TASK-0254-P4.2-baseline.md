---
message_id: MSG-20260705-Arquitecto-to-Codex-GO-TASK-0254-P4.2-baseline
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0254-p4.2-apply-availability-adjustment-baseline.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-002-apply-availability-adjustment.md
one_line_summary: "GO TASK-0254: implementa P4.2 Apply_Availability_Adjustment (miembro baseline de PAR-1) contra SPEC-NOVA-P4-002. AISLAMIENTO CRITICO: no leer nada de P4.3."
requested_action: "Implementa TASK-0254 / SPEC-NOVA-P4-002 (Apply_Availability_Adjustment, ajuste de CDP tipos 08/09) end-to-end: Application + API + UI apps/nova-web, contra el proc Budget.Apply_Availability_Adjustment en el sandbox sellado. AISLAMIENTO CRITICO PAR-1: NO leas ni toques nada relacionado con Apply_Commitment_Adjustment (tipos 11/12, P4.3) -- es el miembro gobernado del par, se construye en Sprint 1, y leer su implementacion CONTAMINA el par fuera del confirmatorio del estudio. El set REAL de THROW ya lo confirmo el DBA (preflight, sello s.20): 50250,50251,50252,50253,50254,50255,50256,50257,50258,50260,50261 (50259 NO EXISTE, confirmado -- no lo cites como criterio falsable); trigger trg_availability_line_adjustment__validate = 50083,50084. RE-CONFIRMA este set contra OBJECT_DEFINITION al construir (ya tienes VIEW DEFINITION concedido). PREVISUALIZACION: usa vw_Commitment_Availability_Validation (saldo REAL) para el floor del contracredito 09, NUNCA vw_Availability_Certificate_Line_Balance (esa vista tiene committed_amount=0 hardcoded, saldo INFLADO, caveat B-01 de la SPEC). GUARD DE PROCEDENCIA (adoptado tras el hallazgo de TASK-0253): la evidencia F-NOVA-01 debe versionarse con una clase SQL real (gateada por env vars, NA limpio sin credenciales) -- NINGUN mock/Recording* in-memory con resultados hardcodeados por caso puede sustituirla; el checker adversarial lo va a verificar explicitamente, no repitas el ciclo de 3 rondas de P4.1. Al entregar, marca in_review y este Arquitecto rutea el checker vivo (adversarial informal, sesion separada). Reporta tokens de tu sesion (err.log) antes de que rote."
question: ""
---

# GO - TASK-0254 P4.2 Apply_Availability_Adjustment (miembro baseline PAR-1)

Ruta critica al 30-jul, segundo miembro tras P4.1 (done). Precondiciones YA listas: sandbox mutadores
sellado + GRANT EXECUTE + VIEW DEFINITION (proc + tabla padre del trigger) + EXECUTE ON TYPE del TVP
`Chain_Adjustment_Line_List` -- todo preflighteado por el DBA (sello s.17/s.20), NO deberia repetir la
saga de permisos de P4.1.

## AISLAMIENTO CRITICO (PAR-1) -- lee esto primero
NO leas, toques, ni consultes NADA de `Apply_Commitment_Adjustment`/P4.3 (tipos 11/12). Es el miembro
GOBERNADO del par (Sprint 1); contaminacion intra-par = par fuera del confirmatorio del estudio. Esta
SPEC ya esta redactada SOLO de docs compartidos + el patron de P4.1 -- sigue el mismo aislamiento en tu
implementacion.

## Que implementar
Ver `Area_comun/tasks/TASK-0254-p4.2-apply-availability-adjustment-baseline.md` (DoD) y
`Area_comun/specs/nova/SPEC-NOVA-P4-002-apply-availability-adjustment.md` (SPEC completa, ya actualizada
con el set REAL de THROW del preflight del DBA).

## No negociable
- **F-NOVA-01:** THROW set YA CONFIRMADO por el DBA (50250-50258,50260,50261; **50259 confirmado
  AUSENTE**; trigger 50083/50084). Re-confirma contra `OBJECT_DEFINITION` al construir.
- **Previsualizacion:** `vw_Commitment_Availability_Validation` (saldo real), NUNCA la vista inflada
  (`_Line_Balance`, B-01).
- **Guard de procedencia:** evidencia F-NOVA-01 con clase SQL real, NUNCA un mock in-memory (precedente
  de 3 rondas en P4.1 -- no lo repitas).
- Fuera de alcance: compromiso (11/12), obligacion (14), aprobar/crear CDP, anulacion, contabilidad.

## Al entregar
Marca `in_review`. Checker = adversarial informal de 12 puntos en sesion separada (incluye aislamiento
PAR-1 + guard de procedencia). Reporta tokens de tu sesion (err.log) antes de que rote.
