---
decision_id: DECISION-0017
title: Alcance del event log como writer vivo del estado - A->B incremental
status: accepted
date: 2026-06-06
ratified_at: 2026-06-06
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0015, DECISION-0009, DECISION-0014, DECISION-0011, DECISION-0001]
phase: P2
spec_id: Area_comun/specs/SPEC-0039-event-log-writer-vivo.md
---

# DECISION-0017 - Alcance del event log como writer vivo (A->B incremental)

> Estado: ACCEPTED (2026-06-06, aprobada por el operador). Cierra la pregunta de alcance del item A.1
> del inventario de cierre del nucleo N-agente. Cambio que afecta el mecanismo de escritura del estado
> => requiere DECISION + aprobacion humana (CLAUDE.md regla 2, AGENTS.md sec.4).

## Contexto

El event log (Fase 2, TASK-0044) es hoy aditivo/observacional: `apply.py` escribe el estado del protocolo
directo a `Area_comun/state/*.json`, `replay_events` solo reconstruye el control-plane de concurrencia, y
`assert_snapshot_matches` no esta cableado a apply ni al validador global. Ademas, las transiciones del
estado de protocolo hoy las hacen los agentes editando JSON a mano, no el runtime. "Writer vivo" implica
decidir QUE captura el log y QUIEN escribe el estado, lo que afecta el modo de trabajo. Ver
SPEC-0039 secciones 1-3 para el detalle y las opciones evaluadas (A / A->B / B / C).

## Decision

Adoptar el alcance **A -> B incremental**:

1. **Fase A (ahora, TASK-0048) - control-plane gate.** En los turnos del runtime, apply/orchestrator
   emiten `acquire_claim`/`apply_intent` al `EventWriter`; `assert_snapshot_matches` se vuelve hard-gate
   en apply (pre-commit del runtime) y en el validador global py/ps1 cuando `runtime/state/` existe y no
   esta vacio. Aditivo, reversible; fallback intacto cuando no hay `runtime/state/` (el repo vivo sigue
   con edicion manual del estado de protocolo sin cambios). Cierra el FOLLOW-UP rastreado desde Fase 2.

2. **Fase B (especificada, GATEADA) - estado de protocolo en el log.** Extender el replay al estado de
   protocolo, materializar los `*.json` desde el snapshot (log = fuente de verdad), genesis-snapshot del
   estado actual, ventana de transicion (drift como warning -> hard-fail) y migracion/prohibicion de la
   edicion manual de esos archivos. Se activa por decision posterior del operador, cuando el runtime sea
   el escritor habitual.

Opciones descartadas: "solo A" sin camino a B (no cumpliria 11/I5-I6 sobre el estado de protocolo);
"B directa" (alto impacto inmediato sobre el modo de trabajo); "C dual-track con reconciliacion"
(complejidad y riesgo de drift silencioso).

## Versionado y neutralidad (DECISION-0001)

- Fase A: **MINOR** (aditivo, runtime-gated, fallback intacto).
- Fase B: **MINOR-con-migracion** o **MAJOR** si rompe el flujo de edicion manual; se evalua al activarla.
- Neutral de dominio: es infraestructura de runtime/auditoria; sin terminos de negocio.

## Consecuencias

- Habilita auditoria/replay reales del control-plane ya (Fase A) y del estado completo cuando se active B.
- No altera el flujo de trabajo actual hasta que se active B (Fase A no aplica gate si no hay runtime/state).
- TASK-0048 implementa la Fase A. La Fase B sera una tarea/SPEC posterior gateada.
