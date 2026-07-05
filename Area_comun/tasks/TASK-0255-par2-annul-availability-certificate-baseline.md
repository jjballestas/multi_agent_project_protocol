---
task_id: TASK-0255
title: "[VISION-NOVA] PAR-2 Annul_Availability_Certificate (miembro baseline, superficie C# sobre hardening)"
type: feature
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-05
reviewer: Analista
checker: adversarial-informal-subagent
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, DECISION-0091, DECISION-0078]
linked_decisions: [DECISION-0091, DECISION-0078]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
intake:
  type: feature
  goal: Implementar la superficie C#/API/UI sobre el proc de hardening Budget.Annul_Availability_Certificate (anulacion de CDP), siguiendo SPEC-NOVA-P4-005. Miembro BASELINE de PAR-2 (sorteo del sello s.23, 2026-07-05, empate resuelto por orden alfabetico del nombre real del proc SQL). Contraparte gobernada: Annul_Commitment (SPEC-NOVA-P4-006, Sprint 1). AISLAMIENTO CRITICO -- no leer nada de la implementacion del hermano. El proc SQL ya existe (hardening del DBA, 10/10 pruebas verificadas); esta tarea NUNCA construye ni modifica el proc, solo consume el contrato.
  acceptance:
    - Los 8 criterios Given/When/Then de SPEC-NOVA-P4-005 s.7 pasan contra el sandbox sellado (DbsFinanciero_SANDBOX, rol budget_sandbox_verifier).
    - F-NOVA-01 cumplida - el maker RE-VERIFICA el set COMPLETO de THROW del proc desplegado via OBJECT_DEFINITION (conocidos por el DBA: 50293 guarda bloqueante RP-activo, y un THROW de SESSION_CONTEXT faltante familia 50100 a re-confirmar) -- NO asumir que esos 2 son el set completo.
    - Guarda bloqueante RN-08 (THROW 50293 si hay RP activo) verificada contra el proc real, NUNCA reimplementada en C#.
    - Idempotencia verificada contra el proc real (anular dos veces no doble-restaura).
    - Saldo leido de la vista correspondiente, NUNCA recalculado en C#.
    - AISLAMIENTO PAR-2 verificable en el diff -- ningun archivo de esta unidad referencia Annul_Commitment ni tipos de compromiso (test de arquitectura mecanico, mismo patron que TASK-0254).
    - Evidencia F-NOVA-01 versionada con clase SQL real (gateada por env vars, NA limpio sin credenciales) -- guard de procedencia, NINGUN mock/Recording* in-memory sustituye la evidencia.
    - Tramo contable documentado como NO-OP para CDP (confirmado por el DBA, no reimplementar un posteo que el proc no hace).
    - Disciplina de captura de medicion - fila OPEN al inicio + CLOSE al done via personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_ledger.py --corpus personal/Arquitecto/TFM-medicion/corpus/medicion (explicito).
  verification_cmd:
    - dotnet test NOVA.sln
  scope_routes:
    - (repo producto Nova-Budget, fuera del hub)
  out_of_scope:
    - Anulacion de compromiso (Annul_Commitment, P4-006) - FUERA (aislamiento PAR-2).
    - Crear/aprobar/ajustar el CDP (P3.2, P4.2 ya cerrada) - FUERA.
    - Construir o modificar el proc de hardening (ya existe) - FUERA.
    - Contabilidad real (NO-OP confirmado para CDP/RP) - FUERA.
  risk: medium
  estimate: M
---

# TASK-0255 - PAR-2 Annul_Availability_Certificate (miembro baseline)

Owner: Codex (implementa) + checker adversarial informal en sesion separada (Agent subagent, checker_formal=0).

## Contexto (sorteo PAR-2, sello s.23, 2026-07-05)
PAR-2 = {Annul_Availability_Certificate, Annul_Commitment} (par CONFIRMADO, s.13). Sorteo (nombre real del
proc SQL, empate desempatado por orden alfabetico, transparencia completa en s.23) asigno:
**Annul_Availability_Certificate = BASELINE** (esta unidad) / **Annul_Commitment = GOBERNADO** (Sprint 1).

## SPEC completa
Ver `Area_comun/specs/nova/SPEC-NOVA-P4-005-annul-availability-certificate.md`.

## PRECONDICION -- preflight de permisos AMPLIADO pendiente
Se pidio al DBA (via Operador) `GRANT VIEW DEFINITION` sobre el proc + tablas de reverso, y `GRANT SELECT`
sobre las tablas BASE que el proc consulte internamente (leccion de TASK-0254: SQL 229 por SELECT
denegado sobre una tabla no anticipada). Codex puede AVANZAR con Application/API/UI mientras se resuelve;
F-NOVA-01 en vivo espera la confirmacion del preflight.

## AISLAMIENTO CRITICO (PAR-2)
NO leer la implementacion del hermano Annul_Commitment (SPEC-NOVA-P4-006, Sprint 1). Esta SPEC se redacta
SOLO de docs de proceso compartidos + el patron congelado de P4.1/P4.2.

## Gate final (checker_formal=0, baseline)
Adversarial informal de 12 puntos en SESION SEPARADA. Debe incluir guard de procedencia + test de
aislamiento PAR-2, mismo patron que TASK-0254.

## DoD (testable)
Ver bloque intake (acceptance) + SPEC s.7/s.8. Disciplina de captura de medicion OPEN/CLOSE obligatoria.
