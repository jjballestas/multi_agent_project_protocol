---
spec_id: SPEC-0069-codex-implementer-invoker-turno-completo
task_id: TASK-0092
type: design
status: ready
created_at: 2026-06-09
author: Claude (arquitecto)
linked_decisions: [DECISION-0027, DECISION-0021, DECISION-0024]
relates_to: [TASK-0088, TASK-0089, TASK-0090, TASK-0091, SPEC-0064, SPEC-0068]
---

> PROMOVIDA por Claude (2026-06-09) bajo enforce+authoritative. OFF-PILOT (NO multiplicador). Integra el CLI
> `codex` como invoker real `implementer` y endurece el contrato del turno real para que produzca un TURNO
> COMPLETO valido (claim -> edicion real -> turn-report). SA.4 sigue DE-ARMADO hasta smoke de turno completo limpio.

# Diseno - Codex como invoker implementer real + contrato de turno completo

## 1. Contexto (hallazgo del 1er piloto)

El 1er piloto (preset claude) fue RECHAZADO por el gate (falla cerrada, cero footprint), por 3 errores:
(1) agent Claude lacks implementer; (2) gate.diff_required: local_write sin changed_paths; (3) no active claim.
Raiz: el gate deriva la capability del CONTENIDO del turno (`required_capability_for_report`,
runtime/turn_validate.py): editar archivos (`changed_paths`) o entregar (->in_review/done) exige `implementer`;
Claude (architect) no lo tiene. El unico agente `implementer` es **Codex**, cuyo CLI ESTA disponible y autenticado
(`codex exec`, gpt-5.5, ChatGPT auth). Usar codex casa la capability y resuelve #1 y #3 (agent=Codex == owner).
Falta #2: el turno real debe REALMENTE editar + reportar `changed_paths` (contrato del turno).

## 2. Alcance

### 2.1 Integrar el invoker `codex exec`
- Preset `runtime.llm_cli_presets.codex.command` apunta al wrapper vendor-neutral (SPEC-0068) con backend
  `codex exec` NO interactivo, p.ej.:
  `python runtime/llm_turn_wrapper.py --backend "codex exec -s workspace-write --output-schema runtime/turn_schema.json -c approval_policy=\"never\" --skip-git-repo-check"`
  (el wrapper ya resuelve el ejecutable via shutil.which, TASK-0090). Determinar/ajustar los flags exactos por
  smoke. Prompt por stdin (codex exec lo lee de stdin).
- **Salida -> turn-report:** confirmar que `--output-schema runtime/turn_schema.json` produce el turn-report donde
  el wrapper lo lee (stdout). Si codex escribe el final solo a `-o <file>` o mezcla eventos, adaptar wrapper/preset
  (p.ej. usar `-o <tmpfile>` y que el wrapper lea ese archivo) -- minimo, vendor-neutral, con su golden.
- **No interactivo / sandbox:** `-s workspace-write` (puede editar) + `approval_policy=never` (sin prompts);
  verificar que NO cuelga ni pide confirmacion (el wrapper igual corta por timeout<120s).
- **Commit:** codex SOLO edita (+ reporta); el commit lo hace el orquestador (apply_gate_and_commit). Verificar
  que codex no commitea por su cuenta (o que el flujo del orquestador lo absorbe sin doble-commit).

### 2.2 Endurecer `build_prompt` (runtime/adapters/llm_adapter.py)
- El prompt debe conducir al agente RUTEADO (owner del unit) a: (a) RECLAMAR la tarea (transicion claim acquire),
  (b) hacer la EDICION real del/los archivo(s) del alcance, (c) devolver un turn-report schema-valido con
  `agent`=owner ruteado, `changed_paths` (los archivos editados), `commit_message`, y las `transitions`
  (claim + task_status apropiado, p.ej. in_progress->in_review para entrega implementer). Sin prosa/fences.
- Mantener determinismo y neutralidad; no filtrar secretos.

### 2.3 Golden + SMOKE REAL (el gate)
- **Golden determinista (recorded, sin red):** el contrato endurecido produce/parsea un turn-report COMPLETO
  (claim + changed_paths + commit_message + transitions + agent) y el orquestador lo aplica; casos de turno
  incompleto (sin changed_paths / sin claim) siguen RECHAZADOS (falla cerrada).
- **SMOKE REAL (lo ejecuta Claude al ratificar, off-pilot, sin re-armar):** UNA corrida real de un turno completo
  por `codex exec` via wrapper sobre una tarea de prueba de bajo riesgo (la nota de TASK-0091 o un fixture) ->
  demuestra claim + edicion real + turn-report schema-valido que el gate ACEPTA. Si codex no edita / no reporta /
  cuelga / pide aprobacion -> iterar flags/prompt (sigue off-pilot). El smoke COMPLETO limpio es el gate del piloto.

## 3. Invariantes
1. OFF-PILOT: SA.4 sigue de-armado (real_invoker/supervised_autonomy enabled=false); NO re-armar NI correr el piloto.
2. Vendor-neutral (backend por arg/env; el wrapper no hardcodea vendor), ASCII, **sin secretos** (auth del entorno,
   nunca commiteada). Determinista en CI (golden recorded). Template intacto.
3. NO cambiar el capability-gate (codex=implementer ya cubre; se descarto la opcion B).
4. enforce+authoritative ON: toda transicion de ledger por submit_intent.

## 4. Cierre (DoD)
- Preset codex -> wrapper -> `codex exec` (flags correctos) produce un turn-report schema-valido consumible;
  build_prompt endurecido conduce claim+edit+report; golden determinista (completo aceptado / incompleto
  rechazado) verde; regresiones (llm_turn_wrapper_cases, supervised_autonomy_cases, real_adapter) verdes;
  validador/neutralidad/encoding verdes; vendor-neutral; sin secretos; template intacto; SA.4 sigue de-armado.
- DESPUES (Claude): SMOKE REAL de turno COMPLETO limpio por codex -> reporto al operador -> go a re-armar
  (preset codex) + re-disparar piloto (caps 2/1/180000, checkpoint tras turno 1).

## 5. Fuera de alcance
- Re-armar SA.4 / correr el piloto (tras smoke completo limpio + go del operador).
- Cambiar el capability-gate (B descartada).
- claude como invoker de turnos implementer (no tiene la capability; queda para turnos reviewer/orchestrator a futuro).
