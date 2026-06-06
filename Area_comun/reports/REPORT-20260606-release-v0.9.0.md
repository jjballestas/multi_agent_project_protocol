# Session report - Release v0.9.0 (runtime M2 hito 2: adapter LLM real + primera corrida real)

- Date: 2026-06-06
- Phase: P2 (Adopcion y expansion)
- Process status: closed (v0.9.0 publicada)
- Ratification: aprobada por el human owner (corte de release + corrida real sobre repo vivo); TASK-0036/0039 ratificadas adversarialmente por Claude

## 1. In One Sentence
Se publica **v0.9.0**: el runtime gana su **primer invoker de agente REAL** (no replay), vendor-neutral
y gateado, y se ejecuta la **primera corrida real sobre el repo vivo** — todo aditivo y off-by-default
(`runtime.enabled` no cambia el default; el adapter por defecto sigue `replay`).

## 2. What Was Done
- Ratificacion de **TASK-0036** (adapter LLM real, SPEC-0035): `LLMAdapter(AgentAdapter)` con `Invoker`
  pluggable; `RecordedInvoker` (transcript sin red, para golden/CI) y `SubprocessInvoker` (comando externo
  generico, vendor-neutral). Limites M1 reusados + budget; flags `--adapter llm`, `--llm-invoker`,
  `--llm-command`, `--allow-real-invoker`. Gates del invoker real probados en vivo; default sigue replay.
- Ratificacion de **TASK-0039** (subprocess Windows-safe, SPEC-0036): `from_command` usa
  `CommandLineToArgvW` en Windows + `shlex` en POSIX (antes `shlex` POSIX corrompia rutas backslash =>
  `WinError 2`). Golden subprocess nativo end-to-end.
- **Primera corrida real sobre el repo vivo** (TASK-0040, aprobada por el operador, DECISION-0009
  decision #2): el orquestador cerro una tarea (`ready->done`) con **1 commit M1 en main** via el invoker
  subproceso real; trace `gate_pre..commit`, gate verde, 0 reverts. Artefacto de evidencia en
  `Area_comun/artifacts/RUNTIME-live-selfrun-20260606.md`.
- Corte de release: CHANGELOG `[0.9.0]`, `protocol_version` 0.8.0 -> 0.9.0, PROJECT_STATE actualizado,
  tag `v0.9.0`.

## 3. SDD Summary
- Specs cubiertas (impl) en v0.9.0: SPEC-0035 (adapter LLM real), SPEC-0036 (subprocess Windows-safe).
- Tasks done: TASK-0036, TASK-0039 (impl) + TASK-0040 (corrida real, documentation/SDD ligero).
- Acceptance: 0036 golden 6/6 (once recorded, replay comparativo `llm==replay`, rechazo allowlist, abort
  budget, default replay, enabled:false); 0039 golden subprocess nativo (1 commit) + suite runtime verde;
  0040 corrida real end-to-end sobre main (1 commit gateado).
- Test plans: golden runtime (llm/loop/apply/router/turn) + validador + encoding + neutralidad; verdes
  (.py; .ps1 n/a — codigo python).
- Desviaciones: ninguna funcional. Limite: loop autonomo, mailbox-auto y wrapper LLM real = M2 posteriores.

## 4. Decisions
- DECISION-0009 (runtime, adapters vendor-neutral, gates humanos) y DECISION-0001 (versionado). Cambio
  **MINOR**: aditivo, neutral, back-compatible, off-by-default.

## 5. Current Project State
- **v0.9.0 publicada**; `protocol_version=0.9.0`; validador + scans + golden verdes.
- Done recientes: TASK-0036, TASK-0039, TASK-0040. TASK-0038 (N-agente) = paraguas proposed con diseno
  capturado (DECISION-0015 + SPEC-0038, proposed). TASK-0037 proposed.
- Sin claims de implementacion activos tras el cierre; sin bloqueos.

## 6. Next Steps
1. **Operador:** revisar/aprobar **DECISION-0015** (N-agente) para habilitar la implementacion de TASK-0038.
2. **Claude/Codex:** FOLLOW-UP del hallazgo de proceso: el commit del runtime corre el pre-commit hook de
   poda y puede bloquearse al cruzar `released_count>4`; hacer el commit del runtime consciente del hook
   (o poda como turno de mantenimiento). Enrutar como tarea cuando el operador lo priorice.
3. Proxima poda: archivar la ventana reciente de done (TASK-0036/0039/0040).

## 7. What We Need From The Human Owner
- **Push** del commit de release + tag `v0.9.0` al remoto privado (se hace en esta sesion con tu visto bueno).
- Decidir prioridad del **FOLLOW-UP** (runtime commit vs hook de poda) y de **TASK-0038** (tras aprobar
  DECISION-0015).

## 8. Risks Or Ambiguities
- **Runtime commit vs hook de poda:** mitigado en esta corrida archivando 1 released; fix de raiz pendiente
  (follow-up). Riesgo: una corrida futura sin esa precaucion podria bloquearse a mitad y dejar estado
  a medio aplicar (recuperable via `git restore`).
- Paridad `.ps1`: n/a (cambios python).
- Invoker real: ejecutar agentes reales tiene riesgo de coste/escape; mitigado por gate por turno, 1
  commit/turno, budget, allowlist, `--once` y gate humano para la primera corrida (ya ejercido).

## 9. Communication Status
- Open messages (requiring response): ninguno bloqueante.
- Active blocks: ninguno.
- Decisions required / human-required: push + tag; aprobar DECISION-0015 (no bloqueante para v0.9.0).

## 10. Details
- CHANGELOG `[0.9.0]`; DECISION-0009/0001; SPEC-0035/0036; TASK-0036/0039/0040; HANDOFF-TASK-0036/0039.
- Commit de release v0.9.0 + tag `v0.9.0` sobre HEAD `016b25e` (primera corrida real).
