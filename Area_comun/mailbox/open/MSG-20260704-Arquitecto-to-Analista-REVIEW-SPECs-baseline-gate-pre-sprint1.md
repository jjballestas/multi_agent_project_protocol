---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-SPECs-baseline-gate-pre-sprint1
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/specs/nova/ (14 SPECs de la familia gobernada NOVA-DEV)
  - Area_comun/artifacts/ANALISTA-TASK-0248-... (precedente de omision F-0246-01: q4_membership)
one_line_summary: "GATE BASELINE de ARTEFACTO (pre-dev, NO cuenta como checker_formal) sobre la familia de 14 SPECs de Area_comun/specs/nova/: deja un baseline de SPECs ATESTADO antes de Sprint 1. Verifica COMPLETITUD/CITAS/q4_membership (caza las omisiones tipo F-0246-01 AHORA, no durante el dev). Es review de artefacto de arq+docs, no gate de codigo."
requested_action: "Gatea en clon limpio la familia de 14 SPECs de Area_comun/specs/nova/ como REVIEW DE ARTEFACTO (pre-dev). NO es checker_formal de ninguna tarea medida (es un gate de artefacto de arq+docs; no cuenta en la moneda de tokens). FOCO (caza omisiones tipo F-0246-01 ANTES del dev): (1) **q4_membership DECLARADO** explicitamente en el preambulo DoR de CADA SPEC (F-0246-01 bloqueo P3 por omitirla): P2-001/002 FUERA (baseline), P2-003/004 segun su unidad, P3-001..005 segun DEC, P4-001 FUERA (pattern-setter), P4-002/003 DENTRO (par PAR-1), P4-004 DENTRO, P6-003. (2) **COMPLETITUD del formato** NOVA-SPEC-T-001 (preambulo DoR + 10 campos) en cada una. (3) **CITAS BD PLAUSIBLES**: cada objeto (proc/vista/tabla) citado con nombre exacto; NO ejecutes contra la BD (readonly sin EXECUTE; ademas es pre-dev), pero SI marca cualquier objeto citado que sea claramente inexistente/mal-nombrado o cualquier THROW citado como falsable SIN la clausula F-NOVA-01 de re-verificacion. (4) **AISLAMIENTO declarado** donde aplica (PAR-1: P4-002/003 leyo_codigo_hermano=NO; PAR-D: P2-004 vs P2-001; P4-001 pattern-setter). (5) **HORNEADOS del operador presentes**: adversarial-separado (sesion limpia), checker_formal=0 en baseline, cache-confound, deuda front, correlation+task_id, sandbox<=14-jul en los mutadores P4.x. (6) NEUTRALIDAD: specs/nova/ es instancia namespaced (scan_domain_neutrality NO debe flaggear). Emite un veredicto CONSOLIDADO por SPEC (OK / hallazgos concretos) para dejar el baseline atestado. NO gatees codigo (no hay dev aun); es completitud/citas/estructura. Lista de las 14: P2-001, P2-002, P2-003, P2-004, P3-001..005, P4-001, P4-002, P4-003, P4-004, P6-003."
question: "La familia de 14 SPECs queda como baseline ATESTADO (completitud + q4_membership + citas + horneados), o hay SPECs con omisiones concretas (tipo F-0246-01) a remediar antes de Sprint 1?"
---

# REVIEW - Gate BASELINE de la familia de SPECs (pre-Sprint 1, review de artefacto)

Antes del dev del Sprint 1, gatea la familia de **14 SPECs** de `Area_comun/specs/nova/` como REVIEW DE
ARTEFACTO (arq+docs; NO cuenta como checker_formal, no hay codigo aun). Objetivo: dejar el baseline de SPECs
ATESTADO y cazar omisiones tipo F-0246-01 (q4_membership faltante) AHORA, no durante el dev.

## Foco
1. **q4_membership declarado** en cada preambulo DoR (la omision que bloqueo P3 en 0246).
2. **Completitud** del formato NOVA-SPEC-T-001 (DoR + 10 campos).
3. **Citas BD** con nombre exacto + THROW con la clausula F-NOVA-01 de re-verificacion (no ejecutar: readonly
   sin EXECUTE + pre-dev).
4. **Aislamiento** declarado (PAR-1 P4-002/003 leyo_codigo_hermano=NO; PAR-D P2-004; P4-001 pattern-setter).
5. **Horneados del operador**: adversarial-separado, checker_formal=0 baseline, cache-confound, deuda front,
   sandbox<=14-jul en P4.x.
6. **Neutralidad** (specs/nova/ namespaced, no debe flaggear).

Veredicto CONSOLIDADO por SPEC. Detalle en requested_action. PAR-2 (Annul_*) NO va en este lote: es condicional
a hardening <=15-jul (procs inexistentes; no autorable falsable aun).
