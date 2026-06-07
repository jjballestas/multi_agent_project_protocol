---
decision_id: DECISION-0021
title: Politica de activacion del wrapper LLM real (opt-in, gateada, off-by-default, supervisada)
status: accepted
date: 2026-06-07
ratified_at: 2026-06-07
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0009, DECISION-0015, DECISION-0019, SPEC-0035, SPEC-0036]
phase: P2
---

# DECISION-0021 - Activacion del wrapper LLM real

> Estado: ACCEPTED (2026-06-07, aprobada por el operador: "apruebo activacion 0021"). Cambio de boundary
> (AGENTS.md sec.4): habilita operar el runtime con agentes reales (CLI), off-by-default y opt-in por
> instancia. Analoga a DECISION-0009 (que activo el runtime en este repo). SemVer MINOR. Neutral.

## Contexto

El alcance v1.0 (operador) incluye el WRAPPER LLM REAL: que un proyecto adoptante opere el runtime N-agente
con agentes reales (claude/codex CLI), no solo replay. El motor seguro ya existe: invoker generico real
(TASK-0036/SPEC-0035, vendor-neutral, gateado por flags), Windows-safe (TASK-0039/SPEC-0036), guardrails
(Fase 5: anti-inyeccion 5.1, tool-policy deny-by-default 5.2, firma del envelope 5.3), budget/deadline A10
(Fase 6.2) y observabilidad (6.1). Falta un adapter CLI concreto + una politica de activacion. Activar
agentes reales tiene efecto real => cambio de boundary => DECISION + aprobacion humana.

## Decision

**El wrapper LLM real se distribuye OFF y su activacion es opt-in, gateada y supervisada por instancia.**

1. **Off por defecto:** el adapter CLI concreto se entrega (tier runtime) como configuracion, pero
   `runtime.enabled=false` y sin invoker real activo. Una instancia que no lo activa sigue en replay.
2. **Activacion explicita por instancia (con su propia aprobacion humana):** exige `runtime.enabled=true`
   + los flags ya existentes (`--allow-real-invoker` + `--llm-command` + `--once`) + registrar la activacion
   (analogo a DECISION-0009). El protocolo NO activa agentes reales automaticamente en ninguna instancia.
3. **Limites obligatorios al activar (ya construidos):** budget/deadline A10, tool-policy deny-by-default,
   guardrails anti-inyeccion, 1 commit/turno + gate por turno (M1), paradas humanas duras. Sin estos
   activos, no se habilita el invoker real.
4. **Vendor-neutral:** el wrapper es CONFIGURACION (`llm-command`) sobre el SubprocessInvoker generico; NO
   se hardcodea claude. Adapters concretos (claude/codex) como ejemplos/perfiles.
5. **Sin secretos:** credenciales del CLI las provee el entorno del adoptante; nunca se commitean. CI sigue
   con RecordedInvoker (sin red ni credenciales).
6. **Replay-comparativo:** el adapter real pasa el golden comparativo (llm==replay) donde aplique, para no
   romper el determinismo de las suites.
7. **Autonomia NO incluida:** habilita invocar UN agente real por turno bajo gate; el loop autonomo
   multi-turno sin humano sigue GATEADO/post-v1.0 (autonomia supervisada).

## Consecuencias

Desbloquea SPEC-0048 (adapter CLI concreto + golden + docs de operacion real) y TASK-0062. La doc de
operacion real entra en D2.3. El wrapper es el ultimo bloque funcional de v1.0 antes de docs/SemVer/release.

## Alternativas descartadas

- Dejar el wrapper para v1.1: descartada por el operador (lo subio a v1.0).
- Activar agentes reales por defecto: RECHAZADA (riesgo; viola off-by-default y el patron DECISION-0009).

## Aprobacion humana

Requerida por ser cambio de boundary (AGENTS.md sec.4). Otorgada por el operador el 2026-06-07.
