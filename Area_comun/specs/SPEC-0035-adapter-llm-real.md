---
spec_id: SPEC-0035-adapter-llm-real
task_id: TASK-0036
type: implementation
status: proposed
linked_decisions: [DECISION-0009, DECISION-0001]
created_at: 2026-06-06
author: Claude
---

# SPEC-0035 - Adapter LLM real (un turno real, con limites, replay comparativo, SIN autonomia)

> Estado: PROPOSED. Es M2 hito 2. Implica invocar un agente LLM REAL que escribe/commitea en el repo
> via el motor M1 -> tiene implicaciones de seguridad y necesita confirmacion del operador (mecanismo de
> invocacion + gate de primera corrida real, DECISION-0009). No pasa a ready hasta esa confirmacion.

## Contexto
Runtime M2 (DECISION-0009). M1 cerro el loop de forma determinista con un replay adapter. Hito 2:
sustituir el replay por un adapter que invoca un agente REAL (Claude via Agent SDK/API, Codex via CLI)
detras de la MISMA interfaz `AgentAdapter` (SPEC-0030), produciendo un turn report conforme a
`turn_schema.json`. El loop M1 (apply+gate+commit/revert) NO cambia. Encuadre del operador: limites
claros + replay comparativo + **SIN activar autonomia** (un turno, gateado por humano; nada de loop
autonomo multi-turno todavia).

## Alcance
- `runtime/adapters/llm_adapter.py`: `LLMAdapter(AgentAdapter)` que construye el prompt desde el
  `ContextPack` (contrato de turno `turn_schema` + tarea + specs/decisions enlazadas) e invoca al agente a
  traves de un **invoker pluggable** (interfaz `Invoker.run(prompt) -> (changed_files, report)`), y
  devuelve un turn report. Vendor-neutral: el invoker concreto (Claude SDK / Codex CLI / otro) es
  intercambiable; el replay sigue como invoker de respaldo.
- **Invoker grabable/mock para CI:** un `RecordedInvoker` reproduce un transcript pre-grabado (sin red),
  de modo que los golden son deterministas y NO dependen de API en vivo. El invoker real (SDK/CLI) se usa
  solo en corridas explicitas fuera de CI.
- **Limites claros (reusan M1 + budget):** (a) sandbox de escritura a `root`; (b) write-allowlist + 
  denylist de M1 (no `.git/`, `Area_comun/decisions/`, `AGENTS.md`, `protocol.config*`); (c) el report
  declara `changed_paths` y el orquestador RECHAZA si exceden el claim/allowlist (ya en M1 gate); (d)
  budget de coste/tokens por turno (reusa `runtime/budget.py`): excederlo aborta el turno.
- **Replay comparativo:** un harness que corre el `LLMAdapter` con `RecordedInvoker` sobre un fixture y
  verifica que el loop (validate->apply->gate->commit) produce el MISMO resultado que el replay adapter
  (mismo turn report aplicado, mismo commit/transicion). Prueba que el adapter real es un drop-in
  conforme: cambiar replay->real NO cambia el loop ni los gates.
- **SIN autonomia:** solo `--adapter llm --once` (un turno). NO hay loop autonomo multi-turno aqui. El
  adapter por defecto sigue siendo `replay`. Correr el invoker REAL sobre el repo vivo exige
  `runtime.enabled:true` (ya activo) + seleccion explicita del invoker real + **gate humano**
  (DECISION-0009: primera corrida real = aprobacion del operador).

## No-alcance
- NO el loop autonomo Claude<->Codex multi-turno (hito posterior). NO mailbox automation (hito
  posterior). NO cambia el motor M1 (apply/gate/vcs), el router, ni el contrato de turno. NO mete
  credenciales en el repo (el invoker real las toma del entorno; nunca commiteadas).

## execution_pipeline
1. `LLMAdapter.run_turn` construye el prompt desde el ContextPack y delega en el invoker.
2. `RecordedInvoker` (CI/golden) reproduce transcript; el invoker real (SDK/CLI) queda detras de la misma
   interfaz, seleccionable por flag/config, gateado.
3. El report pasa por `validate_turn` + gates M1; `changed_paths` fuera de allowlist/claim => rechazo;
   budget excedido => abort.
4. `--adapter llm --once`: un turno; sin autonomia. Default `replay` intacto.
5. Replay comparativo: golden que corre llm(RecordedInvoker) y replay sobre el mismo fixture y compara.

## acceptance_criteria
- `LLMAdapter` implementa `AgentAdapter`; `--adapter llm --once` con `RecordedInvoker` produce un turn
  report que el loop M1 aplica (1 commit en verde), determinista.
- Replay comparativo: llm(RecordedInvoker) == replay sobre el mismo fixture (mismo commit/transicion).
- Limites: report con `changed_paths` fuera del claim/allowlist => rechazado (reusa gate M1); budget
  excedido => abort con outcome claro.
- Sin autonomia: solo un turno; correr el invoker real sobre el repo vivo requiere enabled + flag
  explicito + gate humano (no se dispara solo). Default replay sin regresion.
- Sin credenciales en el repo; CI no depende de API en vivo.

## linked_decisions
- `DECISION-0009` (runtime, adapters vendor-neutral, gates humanos); `DECISION-0001` (aditivo,
  off-by-default ⇒ MINOR). La PRIMERA corrida real sobre el repo vivo es decision del operador.

## test_plan
- Golden `examples/llm_adapter_cases/` con `RecordedInvoker`: un turno => 1 commit; replay comparativo
  (llm==replay); rechazo por changed_paths fuera de allowlist; abort por budget; default replay intacto;
  enabled:false aborta. Sin red. Paridad .ps1 n/a (python).

## closure_criteria
- `LLMAdapter` + invoker pluggable + RecordedInvoker + limites (sandbox/allowlist/budget) + replay
  comparativo + `--adapter llm --once`; golden deterministas verdes; default replay sin regresion; sin
  credenciales; revision del arquitecto OK; claim liberado al pasar a in_review (handoff-release).

## Risks
- **Agente real produce trabajo incorrecto y lo commitea.** Mitigacion: gate por turno + 1 commit/turno +
  git revert (M1) + un solo turno (sin autonomia) + gate humano para la primera corrida real.
- **Fuga de sandbox / toca politica.** Mitigacion: sandbox a root + write-allowlist M1 + report
  changed_paths validado contra el claim.
- **Dependencia de API en vivo en CI.** Mitigacion: RecordedInvoker (transcript), sin red en golden.
- **Credenciales.** Mitigacion: del entorno, nunca commiteadas; scan de secretos se mantiene.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Adapter real drop-in de replay | TASK-0036 | golden replay comparativo | llm==replay |
| Limites (sandbox/allowlist/budget) | TASK-0036 | golden rechazo/abort | fuera de allowlist => rechazo |
| Un turno, sin autonomia | TASK-0036 | golden once | 1 commit; sin loop |
| Sin red / sin credenciales en CI | TASK-0036 | golden RecordedInvoker | deterministas sin API |
