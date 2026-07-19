# GUIA - Probar tu runtime (paso a paso, de riesgo cero a un turno real)

> Escrita por el Asesor (2026-07-19) tras el probe de memoria. El runtime es TU equivalente
> ATESTADO de codex-plugin-cc: orquesta turnos (invoca claude/codex) con router determinista +
> gate por turno + 1-turno=1-commit al ledger. Nunca lo encendiste en real. Esta guia te lleva
> de "verlo sin tocar nada" a "un turno real invocando a Codex", subiendo el riesgo un escalon
> por vez. Correr TODO desde la raiz del hub: D:/Agentes/multi_agent_project_protocol.

## AVISO DE VERSION (leccion del 19-jul, verificada en codigo)
Hay DOS versiones del runtime en circulacion y **se comportan distinto en el escalon 3**:
- **HUB** (`D:/Agentes/multi_agent_project_protocol/runtime/`, la NUEVA y mas ESTRICTA): exige
  `--allow-real-invoker` **Y** el bloque de config `runtime.real_invoker.enabled: true` CON los
  tres campos `activation_decision` + `approved_by` + `approved_at` (si falta uno, falla).
  Soporta `--llm-preset` (resuelve contra `runtime.llm_cli_presets`).
- **examples/full_runtime_instance** (mas VIEJA; lo que se copia a instancias scratch): NO lee
  `real_invoker.enabled` (el gate real es solo el flag `--allow-real-invoker`) y **NO tiene
  `--llm-preset`** (solo `--llm-command "<comando>"`).
**REGLA: verifica SIEMPRE contra el codigo de TU instancia antes de correr el escalon 3**
(`grep -n "llm-preset\|real_invoker" runtime/orchestrator.py`). No te fies del doc.

## Antes de empezar (verificado)
- Python 3.12 OK. `runtime.enabled: true` en protocol.config.json. `real_invoker.enabled: FALSE`
  (el invoker real esta gateado; hace falta flip + DECISION para el escalon 3).
- Grounded: `python runtime/orchestrator.py --plan` YA corre y devuelve `{"dry_run":true,"next":null}`
  = funciona, y ahora mismo NO hay turno que enrutar (estado idle del hub).

## ESCALON 0 - `--plan` (READ-ONLY, riesgo CERO)
```
python runtime/orchestrator.py --plan
```
- No muta nada, no llama a ningun LLM. Imprime el proximo turno que el router elegiria.
- `"next": null` = no hay tarea enrutable. Para ver que ELEGIRIA, primero tiene que existir un
  turno enrutable (ver "Crear un turno de prueba" abajo).
- Uselo SIEMPRE antes de cualquier `--run`: es tu vista previa segura.

## ESCALON 1 - `--run --adapter replay` (loop real, SIN LLM real, determinista)
```
python runtime/orchestrator.py --run --adapter replay --replay-report <fixture-o-dir> --once
```
- Ejecuta el loop completo (router -> apply -> gate -> commit) pero con un turno GRABADO (fixture),
  no un LLM real. Mira `runtime/runs/` y `runtime/adapters/replay.py` para fixtures existentes.
- Sirve para SENTIR la mecanica (1 turno = 1 commit, gate por turno) sin gastar tokens ni red.
- `--once` = exactamente un turno (recomendado siempre al principio).

## ESCALON 2 - LLM grabado (recorded; CI, sin red)
```
python runtime/orchestrator.py --run --adapter llm --llm-invoker recorded --once --replay-report <transcript>
```
- Igual que arriba pero por el path del adapter LLM, con un transcript JSON local
  (`format: recorded_invoker.v1`). Prueba el cableado del adapter LLM sin invocar nada real.

## ESCALON 3 - TURNO REAL invocando a Codex (el "true" que nunca usaste)
Requiere, A LA VEZ (diseno anti-accidente):
1. En protocol.config.json (rompe el pin -> exige DECISION firmada):
   ```json
   "runtime": { "real_invoker": {
     "enabled": true,
     "activation_decision": "DECISION-XXXX",
     "approved_by": "operador humano (Jball)",
     "approved_at": "2026-..." } }
   ```
2. El comando con TODOS los flags:
   ```
   python runtime/orchestrator.py --run --adapter llm --llm-invoker subprocess \
     --once --allow-real-invoker --llm-preset codex --run-id <id-unico>
   ```
   (`--llm-preset codex` usa el preset ya definido en tu config; o `--llm-preset claude`.)
- Que hace: arma el prompt, lo pasa por STDIN al CLI de Codex, espera un turn-report JSON por
  STDOUT, valida schema + allowlist del claim + guardrails + budget, corre el gate, y si pasa
  COMMITEA el turno (1 turno = 1 commit atestado). Rechaza cambios de worktree no declarados.
- La autonomia multi-turno NO se enciende aqui (eso es `supervised_autonomy`, otro gate).
- Empieza con `--once` (UN turno), un `--run-id` de prueba, y un turno de scratch (no algo real).

### RECETA REAL -- la que FUNCIONO (validada 19-jul en instancia scratch, turno b486141)
Lecciones del primer turno real con Codex; aplicalas o el escalon 3 falla:
1. **`codex exec` NO emite JSON puro por stdout** -> hace falta un WRAPPER que traduzca:
   prompt por stdin -> codex (sandbox read-only, sesion efimera) -> **JSON puro** por stdout.
   El wrapper reutilizable quedo en la instancia scratch: `scripts/codex_turn_invoker.py`.
   Comando final: `--llm-command "python scripts/codex_turn_invoker.py"`.
2. **ENSAYA SIEMPRE FUERA DEL RUNTIME PRIMERO** (build_prompt -> wrapper -> validate_turn):
   confirma plomeria + auth + formato ANTES de arriesgar el turno. Este paso salvo la corrida.
3. **Pre-requisitos del turno enrutable**: tarea con frontmatter `status:` == indice; entrada en
   TASK_INDEX con `required_capability: implementer`; **claim ACTIVO** cuyo scope cubra los
   `changed_paths` Y los ledgers row-scoped. `spec_id` inyecta el spec al prompt (canal oficial).
4. **Si el turno deja la tarea `done`, DEBE liberar el claim en la MISMA transaccion**
   (regla handoff-release: el gate falla si el owner retiene claim de tarea terminada).
5. **Timeout duro**: `SubprocessInvoker` corta a 120s (el wrapper usa 100s internos). Turnos
   largos hay que trocearlos.

## Crear un turno de prueba enrutable (para que `--plan`/`--run` tengan algo que hacer)
El router (`select_next`) elige de tareas en el ledger en estado enrutable (ready, asignada a un
agente). Para un primer contacto seguro: registrar una tarea trivial de scratch en estado ready,
correr `--plan` (ver que la elige), luego `--replay`/`--once`. Mejor hacerlo GUIADO la 1a vez.

## Guardarrailes (los principios del runtime, DECISION-0009)
Ficheros = fuente de verdad. 1 turno = 1 commit. Gate por turno + rollback. Gates humanos = paradas
duras. Claim como lock. Determinismo en router. Credenciales del CLI = entorno local, no se commitean.

## Recomendacion de arranque
Escalon 0 (ya visto) -> Escalon 1 (replay, un turno) -> Escalon 3 solo cuando quieras, con el
flip de config + DECISION. NO saltes al real sin haber visto replay. El Asesor puede correr los
escalones 0-2 EN VIVO contigo (riesgo cero); el escalon 3 exige tu decision de flip (soberana).
