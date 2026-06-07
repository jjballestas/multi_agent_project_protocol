---
decision_id: DECISION-0024
title: Politica de activacion de autonomia supervisada (loop multi-turno acotado, off-by-default, gateado)
status: draft
date: 2026-06-07
ratified_at: ""
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0009, DECISION-0021, DECISION-0019, DECISION-0015, DECISION-0013, DECISION-0022]
phase: P2
---

# DECISION-0024 - Activacion de autonomia supervisada (DRAFT)

> DRAFT en personal/Claude/ (adelanto autorizado por el operador 2026-06-07: "trabaja en area personal").
> NO promover al ledger ni encender flags sin GO explicito + aprobacion humana (cambio de boundary,
> AGENTS.md sec.4). ID DECISION-0024 tentativo (0023 ya promovida; nada mas en cola de decision).

## Contexto

El runtime N-agente ya ejecuta turnos bajo gate. DECISION-0021 activo el **wrapper LLM real** pero con un
limite duro explicito (sec.7): "habilita invocar UN agente real por turno bajo gate; el loop autonomo
multi-turno sin humano sigue GATEADO/post-v1.0 (autonomia supervisada)". Ese limite se **enforce en codigo**:
`runtime/orchestrator.py` rechaza el invoker real multi-turno —

```
if adapter_name == "llm" and llm_invoker == "subprocess" and not once:
    return {"ok": False, "reason": "subprocess llm invoker requires --once"}
```

`autonomia supervisada` = permitir que el orquestador encadene **N>1 turnos con agente(s) real(es) sin humano
entre turnos**, pero dentro de un **sobre de supervision dura** con topes y paradas verificables. Es un cambio
de boundary: tiene efecto real acumulado => requiere DECISION + aprobacion humana, igual que DECISION-0009
(activo el runtime) y DECISION-0021 (activo el invoker real).

## Lo que YA existe (no se reconstruye; se compone)

El loop (`run_loop`) ya para de forma dura ante: pre-gate no verde; ruta sin unidad o escalada a humano
(`select_next` -> escalate); deadline por tarea; budget soft/hard y `max_cost_tokens`; turno invalido (schema);
`outcome` humano (`decision_required`/`human_required`); cambios de worktree no declarados; post-gate no verde
(revierte). Hay **1 commit/turno** (auditable), run-log + summary (observabilidad 6.1), tool-policy
deny-by-default (5.2), guardrails anti-inyeccion (5.1), firma de envelope (5.3), budget/deadline A10 (6.2).
La autonomia supervisada **reusa todo esto**; solo agrega el sobre que falta y levanta el cerrojo `--once`
de forma controlada.

## Decision (propuesta)

**La autonomia supervisada se distribuye OFF y su activacion es opt-in, gateada, acotada y registrada por
instancia (con su propia aprobacion humana).** Nunca se activa automaticamente.

1. **Off por defecto.** Nuevo bloque de config `runtime.supervised_autonomy` con
   `{enabled:false, activation_decision:"", approved_by:"", approved_at:"", caps:{...}}`. Sin registro valido,
   el cerrojo `--once` del invoker real **sigue vigente** (comportamiento DECISION-0021 intacto).
2. **Activacion explicita y registrada.** Encender exige: `runtime.enabled=true` + `real_invoker` ya activado
   (DECISION-0021) + `supervised_autonomy.enabled=true` con `activation_decision/approved_by/approved_at`
   poblados + un flag CLI explicito (p.ej. `--allow-supervised-autonomy`). El orquestador rechaza el modo si
   falta cualquiera (analogo a `real_invoker_activation_error`).
3. **Sobre de supervision dura (topes obligatorios, todos verificables).** Al activar son **obligatorios**:
   - `max_turns` por corrida (entero pequeno, p.ej. <= 5) — tope duro de turnos encadenados.
   - `budget_tokens` (techo) + `deadline` por tarea — ya existen; obligatorios aqui.
   - **kill-switch / pausa**: el loop comprueba un centinela (p.ej. `runtime/state/PAUSE`) **antes de cada
     turno**; si existe, para con `outcome=paused` sin tocar estado.
   - **deadline de reloj de pared** por corrida (tope de tiempo total), ademas del deadline por tarea.
   - **checkpoint humano forzado**: tras `K` turnos o ante repeticion de fix-cycles (quality_policy), el loop
     para y exige re-confirmacion humana para continuar (no auto-resume).
   - Toda parada existente (gate rojo, escalada, human_required, schema, dirty no declarado) **sigue siendo
     parada dura**. Falla cerrada: ante duda, para.
4. **Auditabilidad.** 1 commit/turno se mantiene; cada corrida deja run-log + summary + un **reporte de
   corrida** legible (turnos, paradas, costo, commits). Resumir y revisar es parte del cierre de la corrida.
5. **Shadow-first (sin agentes reales primero).** El modo multi-turno acotado se prueba con `RecordedInvoker`
   (replay) para demostrar que el sobre acota y observa, ANTES de habilitarlo con el invoker real. Golden
   deterministas (sin red ni credenciales) cubren cada tope (para por max_turns, por pausa, por checkpoint,
   por budget, por reloj).
6. **Vendor-neutral, sin secretos.** Reusa el SubprocessInvoker generico (DECISION-0021); credenciales del
   entorno del adoptante, nunca commiteadas; CI con RecordedInvoker.
7. **Reversibilidad.** Apagar = `supervised_autonomy.enabled=false` (o quitar el registro): el cerrojo
   `--once` vuelve a regir. Sin migracion retroactiva; byte-equivalente cuando esta off.

## Versionado y neutralidad (DECISION-0001)

- Aditivo, off-by-default, opt-in, reversible => **MINOR**. Neutral de dominio (sobre generico de supervision).
  Mantiene boundaries "no secretos" y "aprobacion humana para cambios de boundary".

## Alternativas descartadas (preliminar)

- **Autonomia sin tope de turnos / sin kill-switch:** RECHAZADA (riesgo de loop sin freno; viola supervision
  dura).
- **Auto-resume tras checkpoint:** RECHAZADA (el checkpoint debe exigir re-confirmacion humana).
- **Encender con el invoker real directo (sin shadow):** RECHAZADA (primero probar el sobre en replay).

## Aprobacion humana

Requerida por ser cambio de boundary (AGENTS.md sec.4). PENDIENTE. Este draft solo prepara la politica para
revision del operador; no habilita nada.

## Pendiente

- [ ] Revision del operador a la politica (caps por defecto, valor de `max_turns`, `K`, reloj de pared).
- [ ] Decompose tecnico (ver DRAFT-SPEC-autonomia-supervisada): SA.1..SA.5.
- [ ] Promover a Area_comun/decisions/ + PROJECT_STATE#decisions SOLO con GO (ventana segura, DECISION-0020).
