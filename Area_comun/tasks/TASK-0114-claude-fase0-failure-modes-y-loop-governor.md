---
id: TASK-0114
title: Fase 0 (E5+E6) - FAILURE_MODES.md (MAST) + gobernador "merece un loop?" (DECISION-0034)
type: documentation
status: done
owner: Claude
phase: P2
priority: medium
spec_id: none
linked_decisions: [DECISION-0034]
created_at: 2026-06-14
---

# TASK-0114 - Fase 0 (E5 + E6)

## Objective

Arrancar Fase 0 acotada a dos entregables documentales, neutrales de dominio, por el metodo de
DECISION-0034 (aditiva, MINOR 1.7.0): el catalogo nombrado de modos de fallo (E5) y el gobernador del
loop (E6). maker != checker (analista hizo la pasada de metodologia; operador ratifico con 3 ajustes).

## Expected output

- `Area_comun/protocol/FAILURE_MODES.md` (E5): tabla modo -> sintoma -> guardrail con los 14 modos MAST
  como vocabulario, honesto (no equivalencia 1:1 con MAST-Data; modos sin incidente propio marcados; sin
  tally de incidentes), con nota de limite (MAST no es la superficie exhaustiva; guardas no-MAST aparte).
  Enlazado desde onboarding (`Area_comun/README.md`) y la guia de review (`TASK_PROTOCOL.md`).
- Seccion "Does It Deserve a Loop?" en `Area_comun/protocol/TASK_PROTOCOL.md` (E6): 4 condiciones +
  check 30s, terminacion/convergencia NO-opcional, clausula de alcance temporal (no revoca autoridad ya
  concedida), regla "no E3 antes de E6", pre-check de ampliar SA.4.

## Question to resolve

Como dar a Fase 0 un catalogo de fallos accionable y un filtro obligatorio antes de construir
loops/scanners, sin tocar #3/#4/SA.4 y manteniendo neutralidad estricta.

## Closure criterion

Acceptance estructural de `personal/Claude/drafts-fase0/ACCEPTANCE-fase0-E5-E6.md` verde (14 modos
presentes, nota de honestidad, gobernador + 4 condiciones + check 30s presentes, enlaces desde
onboarding/review); validador/encoding/neutralidad verdes; MINOR 1.7.0 + CHANGELOG; DECISION-0034
registrada por escritor unico; drift 0. #1/protocol_research DIFERIDO; #3/#4/SA.4 intactos.
