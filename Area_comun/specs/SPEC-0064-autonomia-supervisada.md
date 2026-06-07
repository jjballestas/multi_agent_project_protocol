---
spec_id: SPEC-0064-autonomia-supervisada
task_id: TASK-0078
type: design
status: ready
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0024, DECISION-0021, DECISION-0009, DECISION-0019, DECISION-0013]
relates_to: [TASK-0038, SPEC-0048, SPEC-0035]
---

> PROMOVIDA por Claude (2026-06-08). Diseno tecnico de la autonomia supervisada (DECISION-0024 APROBADA).
> SA.1 = TASK-0078 (primera rebanada, shadow). SA.2..SA.5 se encolan de a una. La ACTIVACION real (invoker
> multi-turno, SA.4) sigue gateada por su sobre + GO del operador + rollback ensayado.

# Diseno - Autonomia supervisada (loop multi-turno acotado)

## 1. Objetivo

Permitir que `runtime/orchestrator.py` encadene **N>1 turnos con agente(s) real(es) sin humano entre turnos**,
dentro de un **sobre de supervision dura** verificable, reversible y off-by-default. Conforme a DECISION-0024.

## 2. Estado actual (punto de partida real, ya en el repo)

`run_loop` ya es multi-turno para replay/recorded (`--max-iter`, bucle `for index in reports[:limit]`) y ya
para de forma dura ante: pre-gate rojo, ruta escalada a humano, deadline por tarea, budget soft/hard/max_cost,
schema invalido, `outcome` humano, worktree sucio no declarado, post-gate rojo (revierte). Hay 1 commit/turno,
run-log + summary, tool-policy, guardrails, firma de envelope, budget/deadline A10.

**Unico cerrojo a levantar (controladamente):** el invoker real esta limitado a un turno:
```
if adapter_name == "llm" and llm_invoker == "subprocess" and not once:
    return {"ok": False, "reason": "subprocess llm invoker requires --once"}
```
Todo lo demas del sobre es ADITIVO alrededor de este loop.

## 3. Componentes nuevos (sobre de supervision)

| # | Componente | Donde | Comportamiento |
|---|-----------|-------|----------------|
| C1 | Registro de activacion | `protocol.config.json` `runtime.supervised_autonomy{enabled,activation_decision,approved_by,approved_at,caps}` + `--allow-supervised-autonomy` | Sin registro valido => cerrojo `--once` intacto. Funcion `supervised_autonomy_activation_error(config)` analoga a `real_invoker_activation_error`. |
| C2 | Tope de turnos | `caps.max_turns` (entero pequeno) | El loop nunca encadena mas de `max_turns` turnos reales; al alcanzarlo para con `outcome=max_turns_reached`. |
| C3 | Kill-switch / pausa | centinela `runtime/state/PAUSE` chequeado ANTES de cada turno | Si existe => para con `outcome=paused`, sin mutar estado. Reanudar exige quitar el centinela + re-invocar. |
| C4 | Reloj de pared | `caps.wall_clock_ms` (determinista via `--clock-fixed` en tests) | Suma de duraciones; al exceder, para con `outcome=wallclock_exhausted`. |
| C5 | Checkpoint humano forzado | `caps.human_checkpoint_every_k` + senal de fix-cycles (quality_policy) | Tras `K` turnos o repeticion de fix-cycles, para con `human_required=True`; NO auto-resume. |
| C6 | Reporte de corrida | extension del summary + `*.runreport.md` legible | Turnos, paradas, costo, commits, motivo de cierre. Cierre = revisar el reporte. |

Falla cerrada: cualquier ambiguedad o tope alcanzado => parada con outcome explicito y commit/estado consistente.

## 4. Decompose por rebanadas (aditivo, gateado, shadow-first)

- **SA.1 - Sobre en SHADOW (sin agentes reales).** C1 (registro+flag) + C2 (max_turns) + C6 (reporte), pero el
  modo multi-turno se ejercita con `RecordedInvoker`/replay. Levanta `--once` SOLO si el registro es valido y
  los caps obligatorios estan; si no, comportamiento DECISION-0021 intacto. Golden: para por max_turns; off =>
  byte-equivalente. **Demuestra que el sobre acota y observa sin tocar el invoker real.**
- **SA.2 - Kill-switch + reloj.** C3 (centinela PAUSE) + C4 (wall_clock). Golden deterministas: para por pausa;
  para por reloj (clock-fixed). Sin auto-resume.
- **SA.3 - Checkpoint humano + escalacion.** C5 wired a quality_policy (max_*_cycles, escalate_to_architect_
  before_human) y al router (escalada existente). Golden: para y exige humano tras K / tras fix-cycles repetidos.
- **SA.4 - Invoker real bajo el sobre.** Levanta `--once` para `subprocess` SOLO con `supervised_autonomy`
  activo + todos los caps. Replay-comparativo donde aplique; CI con RecordedInvoker (sin red/credenciales).
  Requiere GO del operador + registro (analogo a DECISION-0021). **Este es el unico paso con efecto real nuevo.**
- **SA.5 - Docs + operacion + promocion.** Guia de operacion (como activar, caps recomendados, como pausar,
  como leer el reporte, como apagar), README_INSTANCIACION/N_AGENT_RUNTIME, promover DECISION-0024 + SPEC/TASK.

## 5. Invariantes de seguridad (no negociables)

1. Off => byte-equivalente; cerrojo `--once` vigente (DECISION-0021 intacto).
2. Sin registro valido + caps obligatorios => no hay multi-turno real.
3. Toda parada dura existente sigue siendo parada dura.
4. 1 commit/turno; cada turno autonomo es un commit auditable; rojo => revertido.
5. Kill-switch efectivo entre turnos; checkpoint humano sin auto-resume.
6. Sin secretos; vendor-neutral; CI sin red ni credenciales.
7. Reversible: apagar restaura el comportamiento previo sin migracion.

## 6. Tests (golden determinista, sin red)

Para por: max_turns, pausa (centinela), reloj (clock-fixed), checkpoint humano (K), fix-cycles repetidos,
gate rojo, escalada, schema invalido. Off => byte-equivalente. Activacion sin registro => rechazo. Paridad
.py/.ps1 donde aplique. Replay-comparativo en SA.4.

## 7. SemVer y neutralidad

MINOR (aditivo, off-by-default, opt-in, reversible). Neutral de dominio (sobre generico). DECISION-0024.

## 8. Secuencia y dependencias

Despues de Fase 7 (no compite por turnos de Codex ahora). Depende de DECISION-0024 aprobada. SA.1->SA.2->SA.3
en shadow (sin riesgo), luego SA.4 (unico con efecto real, GO aparte), luego SA.5. Encolar de a una
(DECISION-0020), GO por mailbox, ETA por turno.

## 9. Preguntas abiertas para el operador

1. Valores por defecto de los caps: `max_turns` (sugiero <=5), `human_checkpoint_every_k`, `wall_clock_ms`.
2. Ubicacion/forma del kill-switch (centinela de archivo `runtime/state/PAUSE` vs flag de config).
3. Quien puede activar la autonomia: solo el operador, o tambien el arquitecto bajo politica.
4. Alcance del primer piloto real (SA.4): tareas de bajo riesgo unicamente? una sola tarea acotada?
