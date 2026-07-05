---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-preflight-PAR2-hecho-THROW-completo
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Arquitecto-to-Operador-ACTION-preflight-PAR2-annul-availability (tu pedido)
  - Area_comun/specs/nova/SPEC-NOVA-P4-005-annul-availability-certificate.md
one_line_summary: "PRE-FLIGHT DE PAR-2 HECHO Y COMPLETO por el DBA (adelantado, ambos miembros): VIEW DEFINITION sobre los 2 Annul + 4 tablas de reverso; SELECT sobre 13 tablas base (reviso el codigo del proc, concedio todo de una); sin TVP (no EXECUTE ON TYPE); sin triggers en reverso; smoke real OK (CDP 30 / RP 87, rollback, 0 residuos, activo/G -> procedencia verificada). CORRECCION IMPORTANTE: el OBJECT_DEFINITION revela que el set de THROW REAL es mas rico que el del smoke (y que mi encargo previo): Annul_Availability_Certificate (baseline) = 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287 (9 codigos, no 3). La SPEC-NOVA-P4-005 debe citar el SET COMPLETO, no el subconjunto del smoke; Codex re-verifica los 9 contra OBJECT_DEFINITION. F-NOVA-01 puede proceder sin la saga. Registra la enmienda del grant (VIEW DEFINITION x6 + SELECT x13, ambos miembros)."
requested_action: "[DIRECTIVA] El DBA del Operador HIZO el pre-flight ampliado de PAR-2, COMPLETO y adelantado (ambos miembros del par). RESUMEN + REVISION DEL ASESOR (PASA): (a) VIEW DEFINITION sobre budget_sandbox_verifier: Annul_Availability_Certificate + Annul_Commitment + las 4 tablas de reverso (Availability_Certificate_Reversal/_Line, Commitment_Reversal/_Line). (b) SELECT sobre 13 tablas base que los procs leen (Availability_Certificate + _Line + _Line_Adjustment + 2 reverso; Commitment + _Line + _Line_Adjustment + 2 reverso; Obligation; Core.Fiscal_Year; Core.Internal_Catalog; Security.[User]) -- el DBA reviso el codigo real y concedio TODO de una, no permiso-por-permiso (leccion P4.1/P4.2 aplicada). Vistas de saldo/validacion ya estaban, revalidadas. (c) SIN TVP -> no se requiere EXECUTE ON TYPE. (d) SIN triggers en las tablas de reverso -> no hay grant-via-tabla-padre pendiente. (e) SMOKE REAL como nova_budget_verifier con ROLLBACK: Annul_Availability_Certificate sobre CDP 30 OK, Annul_Commitment sobre RP 87 OK, cero errores de permiso, 0 residuos, CDP/RP quedaron activo/G -> procedencia verificada en el sandbox real. CORRECCION CRITICA (falsabilidad -- 2a vez que el OBJECT_DEFINITION revela mas THROW que el subconjunto documentado/smoke, refuerza el guard): el set de THROW REAL leido del texto desplegado es MAS RICO que el que puse en mi encargo previo (yo cite 50283/50281/50100, del smoke -- INCOMPLETO). Sets reales completos: **Annul_Availability_Certificate (PAR-2 BASELINE) = 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287** (9 codigos). Annul_Commitment (gobernado, Sprint 1) = 50100, 50290, 50291, 50292, 50293, 50294, 50295, 50296, 50297. ACCION: (1) la SPEC-NOVA-P4-005 (Annul_Availability_Certificate baseline) debe citar el SET COMPLETO de 9 THROW (50100 + 50280-50287) en sus criterios F-NOVA-01, NO el subconjunto de mi encargo; Codex re-verifica los 9 contra OBJECT_DEFINITION (ya tiene VIEW DEFINITION). Si ya escribiste la SPEC con mi subconjunto, corrigela al set completo. (2) F-NOVA-01 de TASK-0255 puede PROCEDER: todos los permisos de lectura estan (VIEW DEFINITION + SELECT tablas base + vistas), sin round-trips pendientes. (3) REGISTRA la ENMIENDA FECHADA del grant surface (VIEW DEFINITION x6 + SELECT x13; ambos miembros pre-flighteados, el gobernado adelantado para Sprint 1). RESPONDE con: (a) SPEC-NOVA-P4-005 cita los 9 THROW reales (no el subconjunto); (b) enmienda del grant registrada; (c) F-NOVA-01 de TASK-0255 desbloqueada para correr."
question: ""
---

# DIRECTIVA - Pre-flight PAR-2 hecho + set de THROW COMPLETO (correccion)

El DBA hizo el pre-flight de PAR-2 **completo y adelantado (ambos miembros)**. Revision del Asesor: **PASA**.

## Pre-flight (resumen)
- VIEW DEFINITION: 2 Annul + 4 tablas de reverso. SELECT: 13 tablas base (reviso el codigo, todo de una).
- Sin TVP, sin triggers en reverso. Smoke real OK (CDP 30 / RP 87, rollback, 0 residuos) -> procedencia verificada.

## CORRECCION (falsabilidad -- 2a vez)
El `OBJECT_DEFINITION` revela un set de THROW mas RICO que el smoke/mi encargo (cite 50283/50281/50100 --
incompleto). **Set real de `Annul_Availability_Certificate` (baseline) = `50100, 50280, 50281, 50282, 50283,
50284, 50285, 50286, 50287`** (9). (`Annul_Commitment` gobernado = 50100, 50290-50297.)

## Acciones
1. **SPEC-NOVA-P4-005 cita los 9 THROW reales** (50100 + 50280-50287), NO mi subconjunto; Codex re-verifica los 9. Si ya la escribiste con el subconjunto, corrigela.
2. **F-NOVA-01 de TASK-0255 puede proceder** (todos los permisos de lectura estan, sin round-trips).
3. **Registra la enmienda fechada** del grant (VIEW DEFINITION x6 + SELECT x13, ambos miembros).

## Responde
(a) SPEC cita los 9 THROW; (b) enmienda registrada; (c) F-NOVA-01 desbloqueada.
