---
decision_id: DECISION-0027
title: Activacion de SA.4 (invoker real multi-turno) - primer piloto acotado
status: accepted
date: 2026-06-08
ratified_at: 2026-06-08
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0024, DECISION-0021, DECISION-0022, DECISION-0026]
phase: P2
---

# DECISION-0027 - Activacion de SA.4 (invoker real multi-turno), primer piloto acotado

> ACEPTADA por el operador (micro-GO 2026-06-08) tras: lock-lift de SA.4 ratificado y OFF-BY-DEFAULT
> (TASK-0088, commit 4e2323a) + ensayo de rollback verde. Activa el invoker real multi-turno bajo el sobre
> de DECISION-0024, para UN piloto acotado. SemVer **MINOR** + CHANGELOG.

## Contexto

DECISION-0024 (politica de autonomia supervisada) y DECISION-0021 (activacion del wrapper LLM real, limitado a
`--once`) dejaron SA.4 (loop multi-turno con invoker real bajo el sobre) **gateado**. TASK-0088 implemento el
lock-lift OFF-BY-DEFAULT: `orchestrator.subprocess_multiturn_allowed` exige
`--allow-real-invoker` AND `--allow-supervised-autonomy` AND `supervised_autonomy_activation_error is None` AND
`real_invoker_activation_error is None`; con el registro vacio el cerrojo `--once` queda intacto
(byte-equivalente). Verificado en vivo + ensayo de rollback verde.

## Decision

Se **activa SA.4** en la instancia viva poblando el registro (`runtime.real_invoker` + `runtime.supervised_autonomy`)
para correr **UN primer piloto acotado** con el invoker real, dentro del sobre de DECISION-0024.

1. **Alcance del piloto:** una sola tarea de **bajo riesgo, acotada, fuera de nucleo y `*.template.*`**: una
   nota de prosa (1-2 frases) en `examples/neutrality_scan_cases/README.md`. Sin tocar fixtures/configs/codigo/
   goldens. Reversible.
2. **Sobre de supervision (caps del piloto, mas estrictos que el estandar 5/2/300000):** `caps.max_turns=2`,
   `caps.human_checkpoint_every_k=1` (checkpoint humano OBLIGATORIO tras el turno 1, sin auto-resume),
   `caps.wall_clock_ms=180000`; `budget_tokens` + `deadline` por tarea obligatorios. Kill-switch `runtime/state/PAUSE`
   chequeado antes de cada turno. Toda parada dura preexistente sigue dura (gate rojo, escalada, `human_required`,
   schema, dirty no declarado). **Falla cerrada.**
3. **Invocacion:** subprocess real (`claude`/`codex`), credenciales del entorno, **nunca commiteadas**. Determinista
   en CI con RecordedInvoker (el piloto en vivo usa el invoker real).
4. **Reversibilidad:** despoblar el registro (`enabled=false` o quitar el registro) restaura el cerrojo `--once`,
   byte-equivalente (ensayado). Rollback armado en todo momento.
5. **Registro de activacion:** `activation_decision="DECISION-0027"`, `approved_by="operador humano"`,
   `approved_at="2026-06-08"` en ambos bloques.

## Regla de oro (DECISION-0026) - innegociable

SA.4 va **sola** en su ventana. **Capa C del bridge queda OFF.** `enforce`/`authoritative` NO se tocan (es el
estado de partida, no un flip nuevo). Un solo multiplicador de riesgo por ventana. Ampliar caps/alcance = otra
ventana, con su propia evaluacion.

## Versionado y neutralidad (DECISION-0001)

- Aditivo (capacidad ya off-by-default en codigo; esta decision la activa para un piloto acotado, reversible) =>
  **MINOR** (`protocol_version` 1.0.0 -> 1.1.0) + entrada en CHANGELOG. Neutral de dominio; sin secretos.

## Cierre de la ventana SA.4

Piloto dentro del sobre, todas las paradas comportandose, `drift 0` sostenido, `replay==hot`, cero hard-fails
falsos, reporte de corrida + reporte humano en `Area_comun/reports/` (Claude redacta, operador ratifica). Recien
entonces se considera ampliar caps/alcance, en otra ventana.

## Alternativas descartadas

- Activar sin lock-lift ratificado / sin rollback ensayado: RECHAZADA (se hizo primero, TASK-0088).
- Piloto sobre tarea de nucleo/template/ledger-critico/release: RECHAZADA (debe ser bajo riesgo).
- SA.4 + Capa C en la misma ventana: RECHAZADA (DECISION-0026, un solo multiplicador).
- Caps estandar (5/2/300000): mas laxos; el piloto usa 2/1/180000 (mas estrictos).
