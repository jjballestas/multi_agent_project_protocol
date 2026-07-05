---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-ausente-3h-cola-sin-idle
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-turno-noche-cola-6h (la cola base sigue viva)
  - MSG-20260705-Operador-to-Arquitecto-FYI-preflight-PAR1-viewdef-throws-reales (PAR-1 BD listo + THROW reales)
one_line_summary: "El Operador estara AUSENTE 3 HORAS y quiere que NO quedes sin trabajo. P4.1 (TASK-0253) esta en retry-3 con TODOS los permisos ya resueltos (EXECUTE+SELECT+VIEW DEFINITION+TVP) -> debe cerrar. Cola pre-decidida para 3h: (1) cierra P4.1 con captura CLOSE; (2) PAR-1 -- escribe SPEC-NOVA P4.2/P4.3 citando los THROW REALES (BD ya pre-flighteada) -> GO -> ciclo completo; (3) REGISTRA las enmiendas fechadas acumuladas del grant (VIEW DEFINITION x4, TVP x2, Reset, PAR-2 flip); (4) hallazgos (#5 auth GAP->Analista, #7 state-machine->patron P4.1, #1 done) + higiene mailbox (5 abiertos); (5) avanza TASK-0246. RESPALDO SI P4.1 SE TRABA EN ALGO DEL DBA (ausente): NO pares -- deja blocked+pregunta y sigue con SPEC PAR-1 + enmiendas + hallazgos + TASK-0246 (nada de eso necesita al DBA). Pre-decidido: P3.1 diferida, NADA de pool Q4/peones para rellenar. Deja resumen *-to-Operador-*."
requested_action: "[DIRECTIVA -- OPERADOR AUSENTE 3H] El Operador estara ausente ~3 horas; NO quedes sin trabajo, trabaja la cola autonomo. Estado: P4.1 (TASK-0253) en retry-3 con TODOS los permisos resueltos (EXECUTE + SELECT + VIEW DEFINITION sobre proc+trigger-via-tabla-padre + EXECUTE sobre el TVP Budget_Modification_Line_List) -> F-NOVA-01 deberia pasar y cerrar. COLA (en orden): (1) CIERRA P4.1: Codex corre F-NOVA-01 (set de THROW re-verificado contra OBJECT_DEFINITION + 8 criterios + saldo de la vista + reset por task_id entre corridas) -> in_review -> done; CAPTURA la fila CLOSE con tokens_total_atribuibles (err.log ANTES de rotar, medicion_ledger.py --corpus explicito, clave TASK-0253 ya tiene OPEN seq 8); el patron de la familia ajustes se CONGELA al arrancar PAR-1. (2) PAR-1: escribe las SPEC-NOVA de P4.2 (Apply_Availability_Adjustment) y P4.3 (Apply_Commitment_Adjustment) como miembros baseline; sus criterios F-NOVA-01 deben CITAR LOS THROW REALES ya enumerados (Availability: 50250-50258,50260,50261 [50259 ausente]; Commitment: 50250-50258,50262,50263; triggers 50083/50084 y 50099/50100) y Codex re-verificar contra OBJECT_DEFINITION; la BD ya esta pre-flighteada (VIEW DEFINITION + TVP Chain_Adjustment_Line_List concedidos) -> NO repiten el round-trip de P4.1. GO el miembro baseline que el sello asigne -> ciclo completo + captura. (3) REGISTRA las ENMIENDAS FECHADAS acumuladas del grant surface (sello s.5): VIEW DEFINITION x4 (P4.1 Apply_Budget_Modification+Budget_Adjustment; PAR-1 Apply_Availability_Adjustment+Apply_Commitment_Adjustment+sus 2 tablas padre), EXECUTE ON TYPE x2 (Budget_Modification_Line_List + Chain_Adjustment_Line_List), el Reset, y el flip PAR-2 condicional->confirmado. Consolidalas en el registro. (4) HALLAZGOS del log de cambios: #5 auth = GAP vs DD-01 (confirmado) -> dueno Analista, y considera que el PATRON de P4.1 (pattern-setter) incluya la auth de endpoint para que PAR-1 no herede endpoints sin auth (#7 converge aqui: 'quien ejecuta' las transiciones = autorizacion); #1 ReadOnlySqlOptions ya renombrado; los demas como deuda/higiene. + HIGIENE mailbox (5 abiertos, archiva consumidos). (5) Avanza TASK-0246. RESPALDO SI P4.1 SE TRABA EN ALGO QUE NECESITE AL DBA (el Operador esta AUSENTE 3h): NO pares el turno -- deja P4.1 blocked con UNA pregunta concreta y SIGUE con (2) SPEC PAR-1 + (3) enmiendas + (4) hallazgos/higiene + (5) TASK-0246; NADA de eso necesita al DBA ni al Operador. PRE-DECIDIDO (no despiertes al Operador): P3.1 = DIFERIR Sprint 1; LINEA ROJA nada del pool Q4 pre-30-jul; peones PROHIBIDOS en el brazo medido (mono); si se agota lo legitimo -> gobierno/docs, no inventes trabajo que rompa el sello. Deja un resumen *-to-Operador-* al final: P4.1 cerro? (tokens) / PAR-1 en que estado / enmiendas registradas / blocked pendientes con su pregunta. El Operador tiene el CHECK (personal/asesor/CHECK-turno-noche-20260705.md) que el Asesor mantiene vivo."
question: ""
---

# DIRECTIVA - Operador ausente 3h, cola sin idle

El Operador estara ausente ~3h; NO quedes sin trabajo. **P4.1 (TASK-0253) esta en retry-3 con TODOS los
permisos resueltos** (EXECUTE + SELECT + VIEW DEFINITION proc+trigger + TVP EXECUTE) -> debe cerrar.

## Cola (en orden)
1. **Cierra P4.1** (F-NOVA-01 con THROW re-verificados + 8 criterios) -> done + **captura CLOSE** (tokens del err.log, `--corpus` explicito). Congela el patron ajustes.
2. **PAR-1:** escribe SPEC-NOVA P4.2/P4.3 **citando los THROW REALES** (Availability 50250-58,50260,50261 [50259 ausente]; Commitment 50250-58,50262,50263; triggers 50083/84, 50099/100); BD ya pre-flighteada -> GO miembro baseline -> ciclo completo + captura.
3. **Registra las enmiendas fechadas** acumuladas del grant: VIEW DEFINITION x4, EXECUTE ON TYPE x2, Reset, flip PAR-2 confirmado.
4. **Hallazgos:** #5 auth GAP -> Analista (+ que el patron de P4.1 incluya auth de endpoint; #7 converge); #1 done; resto deuda/higiene. + **higiene mailbox** (5 abiertos).
5. **Avanza TASK-0246.**

## Respaldo si P4.1 se traba en algo del DBA (Operador AUSENTE)
NO pares: deja P4.1 `blocked` + UNA pregunta y sigue con (2)(3)(4)(5) -- nada de eso necesita al DBA. Pre-decidido: P3.1 diferida, nada de Q4/peones para rellenar.

## Responde (*-to-Operador-*)
P4.1 cerro? (tokens) / PAR-1 estado / enmiendas registradas / blocked con su pregunta.
