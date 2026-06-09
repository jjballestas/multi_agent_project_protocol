---
id: TASK-0092
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-09
updated_at: 2026-06-09
depends_on: [TASK-0090]
relates_to: [TASK-0088, TASK-0089, TASK-0091, SPEC-0064]
phase: P2
spec_id: Area_comun/specs/SPEC-0069-codex-implementer-invoker-turno-completo.md
linked_decisions: [DECISION-0027, DECISION-0021, DECISION-0024]
objective: (OFF-PILOT, no multiplicador) Integrar el CLI codex como invoker real implementer (codex exec no interactivo) y endurecer build_prompt para que el turno real produzca un TURNO COMPLETO valido (claim -> edicion real del/los archivo(s) -> turn-report schema-valido con agent ruteado + changed_paths + commit_message + transitions). NO re-armar SA.4 ni correr el piloto.
expected_output: (1) preset runtime.llm_cli_presets.codex.command -> wrapper vendor-neutral con backend "codex exec -s workspace-write --output-schema runtime/turn_schema.json -c approval_policy=\"never\" --skip-git-repo-check" (flags exactos confirmados por smoke; prompt por stdin; el wrapper resuelve via shutil.which); si la salida de codex no llega como turn-report a stdout, adaptar wrapper/preset (p.ej. -o <tmpfile> leido por el wrapper) minimo + golden; (2) build_prompt (runtime/adapters/llm_adapter.py) endurecido para conducir claim+edicion+report con agent=owner ruteado, changed_paths, commit_message y transitions (claim + task_status p.ej. in_progress->in_review); (3) golden determinista recorded (turno completo aceptado / incompleto -sin changed_paths/sin claim- rechazado) + regresiones verdes + paridad/CI; vendor-neutral, sin secretos, template intacto. NO re-armar SA.4 (enabled=false) NI correr piloto.
question_to_resolve: confirmar por smoke (1) donde deja codex exec el turn-report (stdout vs -o file) y (2) que -s workspace-write + approval_policy=never editan sin colgar ni pedir aprobacion. Si codex no soporta un turno agentico multi-accion headless -> blocked + nota (es el riesgo que el smoke debe despejar). Si submit_intent rechaza, NO editar *.json a mano.
closure_criterion: preset codex->wrapper->codex exec produce turn-report schema-valido consumible + build_prompt conduce turno completo (claim+edit+report) + golden determinista (completo aceptado / incompleto rechazado) verde + regresiones/validador/neutralidad/encoding verdes; vendor-neutral; sin secretos; template intacto; SA.4 sigue DE-ARMADO; todo por submit_intent; handoff con evidencia (incluye una traza de turno completo recorded). El SMOKE REAL de turno completo lo hace Claude al ratificar (gate del piloto).
sdd_required: true
---

# TASK-0092 - Codex como invoker implementer real + contrato de turno completo (off-pilot)

> READY (encolada por Claude 2026-06-09 VIA submit_intent bajo enforce+authoritative). OFF-PILOT. Resuelve el
> hallazgo del 1er piloto: el turno de trabajo (editar+entregar) exige `implementer`; el unico implementer es
> Codex, cuyo CLI esta disponible (`codex exec`). Ver SPEC-0069. SA.4 DE-ARMADO; NO re-armar ni piloto.

## Contexto

1er piloto (preset claude) RECHAZADO por el gate (falla cerrada): #1 agent Claude lacks implementer; #2
local_write sin changed_paths; #3 no active claim. Usar codex (agent=Codex, implementer) casa la capability (#1)
y el claim (#3, agent==owner). Falta que el turno REALMENTE edite + reporte changed_paths (#2) -> contrato del
turno + flags de codex exec. `codex doctor`: codex presente+autenticado (gpt-5.5); `codex exec` soporta stdin,
`-s workspace-write`, `--output-schema`, `-o`, `--json`, `approval_policy` via `-c`.

## Alcance (SPEC-0069)

1. **Invoker codex exec** via el wrapper (preset codex). Backend no interactivo con `-s workspace-write`
   `--output-schema runtime/turn_schema.json` `-c approval_policy="never"` `--skip-git-repo-check` (ajustar por
   smoke). Confirmar salida->turn-report en stdout; si no, adaptar wrapper/preset (p.ej. `-o <tmpfile>`) + golden.
2. **build_prompt** endurecido: claim -> edicion real -> turn-report con agent ruteado + changed_paths +
   commit_message + transitions.
3. **Golden determinista recorded** (completo aceptado / incompleto rechazado) + regresiones verdes + paridad/CI.

## Restricciones (duras)

- OFF-PILOT: SA.4 sigue de-armado; NO re-armar NI correr piloto. enforce+authoritative ON: todo por submit_intent.
- Vendor-neutral, ASCII, **sin secretos** (auth del entorno, nunca commiteada). Determinista en CI (golden
  recorded, sin red). Template intacto. 1 commit/turno. NO cambiar el capability-gate (B descartada).

## Cierre

Claude ratifica adversarialmente (golden + lectura del contrato) y cierra por submit_intent. DESPUES (Claude):
SMOKE REAL de turno COMPLETO por codex (claim+edit+report) -> si limpio, reporto al operador -> go a re-armar
(preset codex) + re-disparar piloto (caps 2/1/180000, checkpoint tras turno 1).
