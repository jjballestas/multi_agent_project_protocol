---
spec_id: SPEC-0068-llm-turn-wrapper-vendor-neutral
task_id: TASK-0089
type: design
status: ready
created_at: 2026-06-08
author: Claude (arquitecto)
linked_decisions: [DECISION-0027, DECISION-0021, DECISION-0024]
relates_to: [TASK-0088, SPEC-0064]
---

> PROMOVIDA por Claude (2026-06-08) bajo enforce+authoritative. Off-pilot (NO multiplicador): endurece el preset
> del invoker real para que emita un turn-report JSON limpio y schema-valido, antes del piloto SA.4. SA.4
> de-armado mientras tanto (real_invoker/supervised_autonomy enabled=false; DECISION-0027 vigente).

# Diseno - Wrapper fino vendor-neutral para el invoker real (turn-report limpio)

## 1. Objetivo

El `SubprocessInvoker` (runtime/adapters/llm_adapter.py) pipea el prompt a stdin del comando del preset y hace
`json.loads(stdout)` con timeout 120s. El preset `claude` bare corre interactivo (cuelga) y aun `claude -p`
emite texto/JSON con posibles fences/prosa que `json.loads` crudo no parsea. Este wrapper interpone una capa
fina, **vendor-neutral**, que invoca el CLI subyacente de forma no interactiva, extrae y VALIDA el turn-report
JSON, y emite SOLO el JSON limpio (o falla limpio, nunca cuelga). Asi el invoker recibe un turn-report parseable.

## 2. Alcance

`runtime/llm_turn_wrapper.py` (vendor-neutral; el backend es configurable, no baked-in):
1. **Entrada:** lee el prompt de **stdin**.
2. **Backend configurable:** invoca el CLI subyacente en modo NO interactivo (p.ej. `claude -p`), pasado por
   arg/env (no hardcodear el vendor). El preset `claude` apuntara a este wrapper + backend `claude -p`.
3. **Timeout propio < 120s** (p.ej. 100s): si el backend excede, el wrapper termina el subprocess y **falla
   limpio** (exit!=0 + stderr), NUNCA cuelga (el invoker tiene 120s; el wrapper corta antes).
4. **Extraccion tolerante:** del stdout del backend, extrae el turn-report JSON tolerando ```json/``` fences y
   prosa alrededor (localiza el objeto JSON; si viene `{report:{...}}` lo acepta tambien).
5. **Validacion contra `runtime/turn_schema.json`:** campos requeridos al menos `turn_id`, `task_id`, `agent`,
   `outcome`, `summary`, `changed_paths`, `commit_message` (alinear con el schema real). Invalido => fallo limpio.
6. **Salida:** exito => emite SOLO el JSON limpio (objeto, o `{report:{...}}` segun lo que espera el invoker) a
   **stdout** + exit 0. Fallo (timeout / no-JSON / schema-invalido / backend exit!=0) => exit!=0 + diagnostico a
   **stderr**, stdout limpio.
7. **Preset:** `runtime.llm_cli_presets.claude.command` apunta al wrapper con su backend (p.ej.
   `python runtime/llm_turn_wrapper.py --backend "claude -p"` o equivalente determinista). Vendor-neutral: otro
   vendor = otro `--backend`. (codex CLI ausente hoy; no se exige.)

## 3. Golden determinista (sin red, sin LLM real)

`examples/llm_turn_wrapper_cases/` con backend **fake** (un comando local que emite stdout grabado):
- caso JSON limpio valido => wrapper emite el JSON, exit 0.
- caso JSON con ```json fences + prosa alrededor => extrae y valida, exit 0.
- caso `{report:{...}}` => aceptado.
- caso JSON invalido / falta campo requerido => exit!=0 + stderr.
- caso backend exit!=0 => exit!=0 + stderr.
- caso timeout (backend que duerme) => wrapper corta < su timeout, exit!=0, no cuelga.
Determinista; sin red; sin LLM real. Paridad .ps1 si aplica + CI.

## 4. Invariantes
1. Vendor-neutral (backend por arg/env; nada baked-in). Neutral de dominio, ASCII, sin secretos (credenciales del
   entorno, nunca commiteadas).
2. NUNCA cuelga: timeout propio < 120s, fallo limpio.
3. Off-pilot: este wrapper NO re-arma SA.4 ni corre el piloto; SA.4 sigue de-armado (enabled=false).
4. Determinista en CI (golden con backend fake). Template intacto.

## 5. Cierre (DoD)
- `runtime/llm_turn_wrapper.py` (stdin->backend->extrae->valida->emite limpio / falla limpio, timeout<120s) +
  golden determinista (limpio/fences/{report}/invalido/backend-fail/timeout) + preset `claude` apunta al wrapper +
  regresiones verdes + paridad/CI; vendor-neutral; sin secretos; template intacto. Todo por submit_intent.
- Despues (Claude, no en esta tarea): SMOKE REAL = UNA invocacion `claude -p` via wrapper -> confirmar turn-report
  schema-valido parseable; iterar wrapper/prompt si trae fences/prosa (sigue off-pilot). Recien con smoke limpio:
  re-armar registro + disparar piloto con checkpoint tras turno 1.

## 6. Fuera de alcance
- Re-armar SA.4 / correr el piloto (pasos posteriores, tras smoke limpio).
- Cambiar el invoker mas alla de apuntar el preset al wrapper (el wrapper absorbe la fragilidad).
- codex backend (CLI ausente; el diseno lo soporta por ser vendor-neutral, pero no se exige).
