---
decision_id: DECISION-0014
title: Mantenimiento de estado sistematico (poda por umbral medido)
status: accepted
date: 2026-06-06
ratified_at: 2026-06-06
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0008, DECISION-0006, DECISION-0009]
phase: P2
---

# DECISION-0014 - Mantenimiento de estado sistematico (poda por umbral medido)

> Estado: ACCEPTED (2026-06-06). Nucleo decidido por el operador (umbral medido); implementacion
> convergida con el aporte de Codex (MSG-20260606-Claude-to-Codex-poda-sistematica-diseno). Se deriva
> SPEC-0033 + TASK-0034 (despues de TASK-0033).

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

## Implementacion (convergida con Codex)
- **Separar diagnostico de mutacion:** `measure_context_cost.py` mide (read-only); `prune_state.py`
  actua. `prune_state --check` es read-only, determinista, exit 1 con reporte corto cuando hay poda due;
  `prune_state --apply` archiva (idempotente, archive != delete, ventana reciente).
- **Umbral en config** (`protocol.config(.template).json`, bloque `token_cost`/`maintenance`):
  `context_budget`, `done_ratio`, `released_ratio`, `recent_window` (dias/items).
- **Pre-commit hook = BLOQUEAR con aviso**, NO podar+re-stagear (auto-mutar el commit es fragil, mezcla
  feature con mantenimiento y crea churn). Mensaje: "poda due; corre `python scripts/prune_state.py
  --apply && git add Area_comun/state`". `--fix` manual opcional, nunca automatico en el hook.
- **CI backstop:** corre `prune_state --check` y **falla sobre umbral duro**. Scheduled semanal opcional
  solo lectura (sin escribir al repo salvo bot con credenciales claras).
- **Runtime maintenance turn (M2):** cuando el medidor pasa budget, el loop autonomo genera un turno de
  mantenimiento. Evolucion, no primer mecanismo (depende del runtime + permisos de escritura).
- **Umbrales sugeridos (configurables):** warning `cold_start_tokens >= 15000` o `done_ratio >= 70` o
  `released_ratio >= 80`; hard-fail CI `cold_start_tokens >= 20000` o `done_ratio >= 85` o
  `released_ratio >= 90`. El reporte dice que comando aplicar y cuanto se espera recuperar.
- **Deriva:** SPEC-0033 + TASK-0034 bajo DECISION-0006 (robustez) + DECISION-0008 (eficiencia), despues
  de TASK-0033.

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
