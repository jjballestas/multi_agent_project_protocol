---
decision_id: DECISION-0014
title: Mantenimiento de estado sistematico (poda por umbral medido)
status: proposed
date: 2026-06-06
ratified_at: null
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0008, DECISION-0006, DECISION-0009]
phase: P2
---

# DECISION-0014 - Mantenimiento de estado sistematico (poda por umbral medido)

> Estado: PROPOSED. Nucleo decidido por el operador (umbral medido); la seccion de implementacion se
> finaliza con el aporte de Codex (MSG-20260606-Claude-to-Codex-poda-sistematica-diseno) y entonces pasa
> a accepted + se deriva la TASK.

## Contexto
La poda (archivar done/released + barrer mailbox viejo, DECISION-0008/TASK-0024) baja el cold-start pero
es periodica y hoy depende de que el humano la pida. Medicion 2026-06-06: cold-start re-acumulo a ~19.5k
tokens (suelo post-poda v0.7.0 ~9.2k; baseline original ~37k); el medidor reporta 88.9% de tareas `done`
y 95.5% de claims `released` en estado caliente. El operador pide que el mantenimiento sea SISTEMATICO,
no a peticion.

## Decision (nucleo)
El disparo del mantenimiento se determina por un **umbral medido**, no por evento de commit:

- **Senal:** reusar `scripts/measure_context_cost` (ya calcula dead_weight done%/released% y cold_start vs
  budget). Umbral de referencia: `done% >= 70` o `cold_start_tokens > budget`. Cuando se cruza, el
  gate/validador emite "poda due" (visible en cada validacion).
- **Ejecucion:** un script `prune_state` **idempotente** que archiva done/released fuera de una ventana
  reciente y barre mailbox answered/archived viejo. Archive != delete (el validador lee hot+archive).
- **Disparadores (cinturon + tirantes para cubrir el hueco "sin commit"):** pre-commit hook que avisa o
  bloquea sobre umbral (no que pode en silencio) + CI/scheduled como backstop independiente del commit +
  a futuro un **turno de mantenimiento del runtime** cuando el medidor pasa budget (DECISION-0009).

Descartado como UNICO disparador: "podar antes de cada commit" (sin commit no hay poda; se salta con
--no-verify; churnea archives; re-stagea dentro del commit). Se conserva el hook como un disparador mas,
no como el nucleo.

## Pendiente (input de Codex, luego accepted)
Factibilidad del hook que poda+re-stagea vs el que solo bloquea; donde cablear el umbral (medidor,
validador, o `prune --check`); backstop CI vs scheduled vs esperar runtime. Con eso: status -> accepted +
SPEC + TASK (bajo DECISION-0006 robustez + DECISION-0008 eficiencia).

## Versionado y neutralidad (DECISION-0001)
Tooling + proceso, aditivo => MINOR. Vive en `scripts/`/CI/hooks; neutral.

## Consecuencias
- **Positivas:** el cold-start se mantiene cerca del suelo sin intervencion humana; el peso muerto deja
  de crecer en silencio; trazabilidad intacta (archive != delete).
- **Costo:** un script + hook/CI a mantener; definir ventana reciente y umbral con histeresis para no
  churnear.

## Alternativas consideradas
- **Solo pre-commit:** descartada como nucleo (hueco sin-commit + bypass + churn).
- **Solo manual (hoy):** descartada; es el problema que el operador pide resolver.
- **Solo runtime-turn:** ideal a futuro pero depende de que el loop autonomo (M2) avance; se adopta como
  backstop/destino, no como unico mecanismo inicial.
