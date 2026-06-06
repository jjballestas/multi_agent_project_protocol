---
decision_id: DECISION-0013
title: Liveness, handoff-release y visibilidad de progreso entre agentes
status: accepted
date: 2026-06-06
ratified_at: 2026-06-06
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0005, DECISION-0006, DECISION-0007, DECISION-0009, DECISION-0012]
phase: P2
---

# DECISION-0013 - Liveness, handoff-release y visibilidad de progreso

## Contexto
La coordinacion entre agentes es el nucleo del protocolo, y fallo de un modo concreto: Codex reclamo
TASK-0032, la dejo `in_progress` y gasto turnos en mensajes meta sin senal de avance; el humano no podia
distinguir "avanzando entre turnos" de "parado" y tuvo que prodearlo varias veces. Ademas, al entregar,
Codex dejo el claim ACTIVO en `in_review`, bloqueando el flip del arquitecto. El protocolo validaba
correccion pero no **liveness** ni **visibilidad de progreso**.

## Decision
1. **Liveness (no idle claims).** Un agente que sostiene un claim activo sobre una task `in_progress`
   debe cerrar cada turno de trabajo en uno de: (a) **progreso entregable** hacia los deliverables, (b)
   `blocked` + una pregunta concreta, o (c) **liberar el claim**. "Reclamado/in_progress + inactivo + solo
   mensajes meta" es una violacion de coordinacion.
2. **Senal de progreso por turno.** Cada turno de trabajo deja una senal verificable: un commit de WIP o
   un FYI de una linea ("0032: budget+metrics hechos, faltan golden"). Hace el avance observable sin que
   el humano adivine. La conversacion meta no cuenta como progreso.
3. **Handoff-release.** Al mover una task a `in_review`, el implementador **libera su claim** para que el
   arquitecto ratifique y flipee a `done` sin round-trip. Un task `in_review`/`done` no debe retener un
   claim activo de su owner implementador.
4. **Visibilidad como gate.** Un check determinista marca la violacion de handoff-release (task
   `in_review`/`done` con claim activo del owner). El detector de "stall" temporal (no determinista) se
   deja como senal blanda, no como gate duro.

## Aprobacion humana
Propuesta del operador ("la coordinacion es lo basico; si el metodo no funciona toca adaptarlo") y
aprobada (2026-06-06). Aditiva y back-compatible: formaliza convenciones; no rompe historicos.

## Versionado y neutralidad (DECISION-0001)
Convencion de proceso + checks de tooling, aditiva => MINOR. Vive en `scripts/` y `AGENTS.md`; neutral.

## Enforcement (deriva a SPEC + TASK)
- **TASK-0033** (bajo DECISION-0006, junto con el gate de encoding de DECISION-0012): `scan_encoding`
  (.py/.ps1) para ASCII/mojibake, + check de **handoff-release** en el validador, + golden + CI, +
  documentar la regla de liveness en `AGENTS.md` seccion 7. Secuencia: tras cerrar TASK-0032.

## Consecuencias
- **Positivas:** los stalls y los claims colgados se vuelven visibles/violacion; el humano deja de ser el
  detector de liveness; los handoffs no bloquean el flip del arquitecto.
- **Costo:** disciplina extra por turno (una senal de progreso); un check mas en el gate.
- **Relacion con el runtime (DECISION-0009):** el loop autonomo M2 hace esto estructural (turnos
  disparados con contrato + gate), eliminando la dependencia del prod humano; esta decision es el puente
  hasta entonces y la regla que el loop tambien aplicara.

## Alternativas consideradas
- **Seguir prodeando manualmente:** descartada; es el sintoma, no el arreglo, y no escala.
- **Stall detector por tiempo:** descartada como gate (no determinista, falsos positivos entre turnos);
  se conserva como senal blanda. El gate duro es la regla determinista de handoff-release + encoding.
