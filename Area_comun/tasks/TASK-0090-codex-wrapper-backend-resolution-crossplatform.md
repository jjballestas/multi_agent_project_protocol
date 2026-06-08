---
id: TASK-0090
owner: Codex
status: in_review
type: implementation
priority: high
created_at: 2026-06-09
updated_at: 2026-06-09
depends_on: [TASK-0089]
relates_to: [DECISION-0006, SPEC-0068]
phase: P2
spec_id: Area_comun/specs/SPEC-0068-llm-turn-wrapper-vendor-neutral.md
linked_decisions: [DECISION-0027, DECISION-0006]
objective: Fix cross-platform del wrapper del invoker (off-pilot): runtime/llm_turn_wrapper.py debe resolver el ejecutable del backend (command[0]) via shutil.which antes de subprocess.run, para soportar shims (p.ej. npm claude.CMD en Windows) que subprocess no resuelve por PATHEXT. Sin esto, el preset backend "claude -p" falla con WinError 2 y el piloto no puede invocar el backend. NO re-armar SA.4 ni correr piloto.
expected_output: en runtime/llm_turn_wrapper.py run_backend (o split/resolve), resolver command[0] con shutil.which (si lo encuentra, usar la ruta resuelta; si no, dejar command[0] tal cual y que el fallo sea limpio como hoy); preservar timeout<120s/fail-limpio/extraccion/validacion; golden determinista nuevo que cubra "comando resoluble solo via PATHEXT/shutil.which" (p.ej. un shim fake .cmd/.bat en un dir temporal agregado al PATH, o mock de shutil.which) -> el wrapper lo invoca OK; y "comando inexistente" -> fallo limpio exit!=0. Paridad .ps1/CI. Vendor-neutral, sin secretos, template intacto.
question_to_resolve: ninguna (fix puntual caracterizado: claude.CMD se ejecuta OK via ruta resuelta -devuelve PONG/JSON-, pero subprocess.run(['claude',...]) da WinError 2). Si submit_intent rechaza, NO editar *.json a mano.
closure_criterion: wrapper resuelve backend via shutil.which (shim Windows npm funciona; comando inexistente falla limpio) + golden determinista (resoluble-via-PATHEXT OK, inexistente fail) + regresiones verdes (llm_turn_wrapper_cases sigue) + validador/neutralidad/encoding verdes; vendor-neutral; template intacto; SA.4 sigue DE-ARMADO; todo por submit_intent; handoff con evidencia.
sdd_required: true
---

# TASK-0090 - Wrapper: resolucion cross-platform del backend (off-pilot)

> READY (encolada por Claude 2026-06-09 VIA submit_intent bajo enforce+authoritative). OFF-PILOT. Fix puntual
> del wrapper de TASK-0089 para que el piloto SA.4 pueda invocar el backend en Windows. SA.4 DE-ARMADO; NO
> re-armar ni correr piloto. Ver SPEC-0068.

## Contexto (smoke real, caracterizado)

El smoke real confirmo que el wrapper + `claude -p` producen un turn-report schema-valido (con la ruta resuelta:
`shutil.which('claude')` -> `claude.CMD`, devuelve PONG y el JSON del turno). PERO el wrapper hace
`subprocess.run(["claude","-p"], ...)` que en Windows NO resuelve el shim npm `claude.CMD` por PATHEXT -> WinError 2
("backend could not be started"). El preset backend `"claude -p"` falla asi, y el piloto (orquestador -> preset ->
wrapper -> backend) no podria invocar el backend. El wrapper en lo demas esta OK (logica, timeout, validacion).

## Alcance

1. En `runtime/llm_turn_wrapper.py` (`run_backend`/resolucion): resolver `command[0]` via `shutil.which`; si lo
   encuentra, usar la ruta resuelta para `subprocess.run`; si no, dejar `command[0]` y que el fallo sea limpio
   (exit!=0 + stderr) como hoy. Mantener timeout<120s, nunca-cuelga, extraccion tolerante y validacion.
2. **Golden determinista** (sin red, sin LLM real): caso "backend resoluble solo via PATHEXT/shutil.which"
   (shim fake .cmd/.bat en dir temporal en PATH, o mock de shutil.which) -> wrapper lo invoca OK; caso "comando
   inexistente" -> fallo limpio exit!=0. Las regresiones `llm_turn_wrapper_cases` siguen verdes.
3. Paridad `.ps1`/CI.

## Restricciones (duras)

- OFF-PILOT: SA.4 sigue de-armado (real_invoker/supervised_autonomy enabled=false); NO re-armar NI correr piloto.
- enforce+authoritative ON: CERO edicion manual de `state/*.json`, todo por submit_intent.
- Vendor-neutral (no hardcodear claude ni rutas absolutas), ASCII, sin secretos, template intacto. 1 commit/turno.

## Cierre

Claude ratifica adversarialmente (golden + re-smoke end-to-end via orquestador->preset->wrapper->claude con la ruta
resuelta) y cierra por submit_intent. DESPUES (Claude): si el re-smoke end-to-end es limpio, re-armar registro +
piloto con checkpoint tras turno 1.
