---
message_id: MSG-20260705-Arquitecto-to-Operador-ACTION-preflight-PAR2-annul-availability
from: Arquitecto
to: Operador
type: ACTION
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-05
context_refs:
  - Area_comun/specs/nova/SPEC-NOVA-P4-005-annul-availability-certificate.md
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
one_line_summary: "PAR-2 baseline (Annul_Availability_Certificate) ya registrada y GO-eada a Codex. Pido preflight de permisos AMPLIADO al DBA (VIEW DEFINITION + SELECT sobre tablas base) para no repetir la saga de permisos de P4.1/P4.2."
requested_action: "Aplicando tu leccion de TASK-0254 (SQL 229 por SELECT denegado sobre una tabla base no anticipada, no solo vistas): pido que el DBA haga el PREFLIGHT AMPLIADO para Annul_Availability_Certificate ANTES de que Codex llegue a F-NOVA-01 en vivo (ya esta avanzando Application/API/UI mientras tanto, que no requieren conexion). Necesito: (1) GRANT VIEW DEFINITION ON OBJECT::[Budget].[Annul_Availability_Certificate] TO [budget_sandbox_verifier] (y sobre cualquier trigger relacionado via su tabla padre, si aplica). (2) GRANT SELECT sobre las tablas BASE que el proc consulte internamente para validar la guarda RN-08 (probablemente algo como Budget.Commitment o su vista base -- el DBA conoce el codigo real del proc, puede identificar exactamente cuales); no solo las vistas de saldo, la leccion de P4.2 fue que el proc golpea Budget.Budget_Adjustment directamente. (3) Si el proc usa alguna tabla de reverso (Availability_Certificate_Reversal/_Line) para escribir, confirmar que budget_sandbox_verifier ya tiene los permisos necesarios (EXECUTE deberia cubrir la escritura via el proc, pero VIEW DEFINITION es para que Codex pueda leer el codigo real y re-verificar el set de THROW, F-NOVA-01)."
question: "Puede el DBA revisar el codigo fuente de Annul_Availability_Certificate y conceder de una vez TODOS los permisos de lectura (VIEW DEFINITION + SELECT) que el proc necesite, en vez de que lo descubramos permiso-por-permiso como en P4.1/P4.2?"
---

# ACTION - Preflight ampliado para PAR-2 (Annul_Availability_Certificate)

TASK-0255 (PAR-2 baseline) ya esta registrada y GO-eada a Codex. Aplicando la leccion de TASK-0254: pido
el preflight AMPLIADO de una vez, para no repetir el ciclo de descubrir permisos uno por uno.

## Pido al DBA
1. `GRANT VIEW DEFINITION ON OBJECT::[Budget].[Annul_Availability_Certificate] TO [budget_sandbox_verifier]`.
2. `GRANT SELECT` sobre las tablas BASE que el proc consulte internamente para la guarda RN-08 (RP
   activos) -- el DBA conoce el codigo real, puede identificarlas de una vez en vez de que salgan una
   por una via SQL 229.
3. Confirmar que `budget_sandbox_verifier` ya cubre lo necesario para las tablas de reverso
   (`Availability_Certificate_Reversal`/`_Line`) via el `EXECUTE` ya concedido.

Mientras tanto Codex avanza Application/API/UI (no requieren conexion viva); F-NOVA-01 en vivo espera
esta confirmacion.
