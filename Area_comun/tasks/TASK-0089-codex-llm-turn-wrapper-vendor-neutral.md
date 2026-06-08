---
id: TASK-0089
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0088]
relates_to: [TASK-0021, SPEC-0064]
phase: P2
spec_id: Area_comun/specs/SPEC-0068-llm-turn-wrapper-vendor-neutral.md
linked_decisions: [DECISION-0027, DECISION-0021, DECISION-0024]
objective: Endurecer el preset del invoker real (off-pilot, NO multiplicador) con un wrapper fino vendor-neutral que invoque el CLI subyacente NO interactivo, extraiga y VALIDE el turn-report JSON (tolerante a fences/prosa) contra runtime/turn_schema.json, y emita SOLO el JSON limpio o falle limpio (nunca cuelga). Asi el SubprocessInvoker recibe un turn-report parseable. NO re-armar SA.4 ni correr el piloto.
expected_output: runtime/llm_turn_wrapper.py (lee prompt de stdin; invoca backend NO interactivo configurable por arg/env, p.ej. "claude -p"; timeout propio < 120s -> falla limpio si excede, nunca cuelga; extrae turn-report JSON tolerante a ```json/``` fences y prosa, acepta objeto o {report:{...}}; valida campos requeridos turn_id/task_id/agent/outcome/summary/changed_paths/commit_message contra runtime/turn_schema.json; exito => SOLO JSON limpio a stdout + exit 0; fallo => exit!=0 + stderr) + golden determinista examples/llm_turn_wrapper_cases/ con backend FAKE grabado (limpio/fences/{report}/invalido/backend-fail/timeout) + preset runtime.llm_cli_presets.claude.command apuntando al wrapper + paridad .ps1/CI; vendor-neutral, sin secretos, template intacto.
question_to_resolve: ninguna (alcance fijado por SPEC-0068). Si el turn_schema real exige otros campos, alinear y notar. Si submit_intent rechaza, NO editar *.json a mano.
closure_criterion: wrapper implementado (stdin->backend->extrae->valida->emite limpio / falla limpio, timeout<120s, nunca cuelga) + golden determinista (backend fake: limpio, fences+prosa, {report}, invalido, backend-fail, timeout) verde + preset claude apunta al wrapper + regresiones verdes + paridad/CI; vendor-neutral; sin secretos; template intacto; SA.4 sigue de-armado (enabled=false, NO re-armar); todo por submit_intent; handoff autocontenido con evidencia de los golden.
sdd_required: true
---

# TASK-0089 - Wrapper fino vendor-neutral para el invoker real (turn-report limpio)

> READY (encolada por Claude 2026-06-08 VIA submit_intent bajo enforce+authoritative). OFF-PILOT (NO
> multiplicador): endurece el preset antes del piloto SA.4. SA.4 DE-ARMADO (real_invoker/supervised_autonomy
> enabled=false; DECISION-0027 vigente). NO re-armar ni correr piloto. Ver SPEC-0068.

## Contexto (hallazgo)

El `SubprocessInvoker` pipea el prompt a stdin y hace `json.loads(stdout)` (timeout 120s). El preset `claude`
bare corre interactivo (cuelga); aun `claude -p` emite texto/JSON con fences/prosa que el `json.loads` crudo no
parsea. `codex` CLI esta ausente (solo `claude` v2.1.160). Este wrapper absorbe la fragilidad.

## Alcance (SPEC-0068)

1. `runtime/llm_turn_wrapper.py`: stdin(prompt) -> backend NO interactivo configurable (arg/env, p.ej. `claude -p`;
   NO hardcodear vendor) -> capturar stdout.
2. Timeout propio < 120s; si excede, termina el subprocess y **falla limpio** (exit!=0 + stderr), NUNCA cuelga.
3. Extrae el turn-report JSON tolerante a ```json/``` fences y prosa; acepta objeto o `{report:{...}}`.
4. Valida contra `runtime/turn_schema.json` (al menos turn_id/task_id/agent/outcome/summary/changed_paths/
   commit_message); invalido => fallo limpio.
5. Exito => emite SOLO el JSON limpio a stdout + exit 0. Fallo (timeout/no-JSON/schema-invalido/backend exit!=0)
   => exit!=0 + diagnostico a stderr.
6. Preset `runtime.llm_cli_presets.claude.command` apunta al wrapper + su backend. Vendor-neutral.
7. Golden determinista `examples/llm_turn_wrapper_cases/` con backend FAKE grabado (limpio/fences+prosa/{report}/
   invalido/backend-fail/timeout). Paridad .ps1/CI. Regresiones verdes.

## Restricciones (duras)

- **OFF-PILOT:** NO re-armar SA.4 (real_invoker/supervised_autonomy siguen enabled=false) NI correr el piloto.
- enforce+authoritative ON: CERO edicion manual de `state/*.json`, todo por submit_intent; si rechaza, blocked +
  error + transaccion.
- Vendor-neutral (backend por arg/env), ASCII, **sin secretos** (credenciales del entorno, nunca commiteadas).
  Determinista en CI (golden backend fake, sin red). Template intacto. 1 commit/turno; release/handoff 0018/0020.

## Cierre

Claude ratifica adversarialmente (golden determinista verde; preset apunta al wrapper; nunca cuelga; falla limpio;
vendor-neutral; sin secretos) y cierra por submit_intent. DESPUES (Claude, no en esta tarea): SMOKE REAL (1
invocacion `claude -p` via wrapper -> turn-report schema-valido), luego re-armar registro + piloto con checkpoint
tras turno 1. Su ciclo de vida cuenta para la ventana de observacion authoritative.
