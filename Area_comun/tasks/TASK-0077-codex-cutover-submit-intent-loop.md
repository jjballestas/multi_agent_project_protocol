---
id: TASK-0077
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0076]
relates_to: [TASK-0072, TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0063-cutover-submit-intent-codex-loop.md
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0020]
execution_pipeline: [mapear cada transicion del lazo autonomo de Codex (auto-claim = claim acquire + task_status ready->in_progress; handoff-release = task_status in_progress->in_review + claim release [+ task_upsert]) a una transaccion submit_intent --intents (atomica, TASK-0076); helper/receta runtime/ledger_ops.py para construir los sobres de intents comunes; golden examples/cutover_loop_cases que aplica una secuencia tipica (acquire -> in_progress -> in_review + release) via submit_intent --intents sobre fixture con drift 0 (clean base) -> ledger esperado, drift 0, idempotente; paridad .ps1 + CI]
acceptance_criteria: [el lazo de Codex tiene una ruta probada para emitir auto-claim y handoff-release via submit_intent --intents (transaccional); golden cutover_loop_cases sobre fixture drift-0 materializa el ledger esperado con drift 0 e idempotente; helper/receta para construir intents comunes; NO se encienden enforce/authoritative ni se re-genesisa el repo vivo; determinista sin reloj/red; sin secretos; neutral; paridad/delegacion .ps1; golden + gates py/ps verdes]
expected_output: runtime/ledger_ops.py (o receta documentada) + golden examples/cutover_loop_cases + CI; el lazo de Codex emite sus transiciones via submit_intent --intents (shadow); enforce/authoritative OFF.
test_plan: [golden cutover_loop: secuencia auto-claim+in_progress y handoff-release (in_review+release) via submit_intent --intents sobre fixture drift-0 -> ledger esperado + drift 0 + idempotente; off/shadow byte-equivalente; determinismo + paridad py/ps]
question_to_resolve: ninguna (alcance acotado en SPEC-0063). Si exige cambiar el formato del event log de forma incompatible o tocar el repo vivo => blocked + pregunta.
closure_criterion: ruta probada (golden drift-0) para auto-claim y handoff-release via submit_intent --intents + helper/receta + golden cutover_loop_cases + paridad .ps1; SIN flip ni re-genesis del vivo; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [auto-claim y handoff-release del lazo de Codex expresables como transaccion submit_intent --intents; helper runtime/ledger_ops.py o receta documentada; golden examples/cutover_loop_cases (drift0, ledger esperado, idempotente) sobre fixture clean-base; enforce/authoritative OFF + repo vivo NO re-genesisado; determinista sin reloj/red; sin secretos; neutral; paridad/delegacion .ps1 + CI; gates verdes; handoff autocontenido; release atomico DECISION-0018; staging por paths DECISION-0020]
---

# TASK-0077 - Cutover: el lazo de Codex adopta submit_intent --intents (prerrequisito del flip)

> READY (encolada por Claude 2026-06-08 tras cerrar TASK-0076). Cutover de la migracion al escritor-unico:
> que tu lazo autonomo deje de editar los `*.json` a mano y emita TODAS sus transiciones via submit_intent
> --intents. SHADOW: enforce/authoritative OFF (sin flip; sin re-genesis del vivo). Ver SPEC-0063.

## Contexto

TASK-0076 entrego submit_intent transaccional (`--intents`) + re-genesis. Ahora el cutover: tu lazo construye
y emite sus transiciones (auto-claim, handoff-release) via submit_intent --intents, no por edicion directa.
Es el prerrequisito para encender enforce: si siguieras editando a mano, tras el flip tu proxima edicion
hard-failearia y romperia el lazo.

## Alcance (ver SPEC-0063 sec.2)

1. Mapear auto-claim (claim acquire + task_status ready->in_progress) y handoff-release (task_status
   in_progress->in_review + claim release [+ task_upsert]) a transacciones submit_intent --intents.
2. Helper/receta `runtime/ledger_ops.py` para construir los sobres de intents comunes.
3. Golden `examples/cutover_loop_cases` sobre fixture **drift 0** (clean base): secuencia tipica -> ledger
   esperado, drift 0, idempotente. + paridad `.ps1` + CI.

## Restricciones

- **NO encender enforce/authoritative; NO re-genesisar el repo vivo** (eso es la ACTIVACION posterior, la hace
  el arquitecto tras verificar ambos lados + GO + rollback ensayado). Off/shadow => byte-equivalente.
- submit_intent exige drift 0 -> el golden parte de un fixture clean-base, NO del repo vivo.
- Determinista (timestamp/commit provistos); sin secretos; neutral. Cambios al event log aditivos.
- Handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020).

## Nota

Yo (arquitecto) hago el lado de Claude en paralelo: mandato en AGENTS.md/TASK_PROTOCOL (submit_intent = unico
write-path bajo enforce) + adopcion de mis propios cierres. Tras ambos lados: ACTIVACION = re-genesis vivo +
flip enforce+authoritative + ensayo de rollback (autorizaciones del operador 2026-06-08 ya otorgadas).
