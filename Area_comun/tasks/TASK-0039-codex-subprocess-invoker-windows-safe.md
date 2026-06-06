---
id: TASK-0039
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0036]
relates_to: [TASK-0018]
phase: P2
spec_id: Area_comun/specs/SPEC-0036-subprocess-invoker-windows-safe.md
linked_decisions: [DECISION-0009, DECISION-0006, DECISION-0001]
execution_pipeline: [ajustar SubprocessInvoker.from_command para tokenizar segun el SO anfitrion (Windows-safe sin romper POSIX) preservando comillas/espacios, golden cross-platform que ejecuta un comando con sys.executable + script con separador nativo del host (1 commit verde), regresion recorded/loop/apply/router]
acceptance_criteria: [en Windows --llm-invoker subprocess con --llm-command de rutas nativas (backslash) ejecuta y M1 commitea en verde sin WinError 2, en POSIX sin regresion (rutas / comillas espacios), golden cross-platform verde sin red ni credenciales, sin regresion recorded ni resto de golden del runtime]
test_plan: [golden que tokeniza/ejecuta un comando con separador nativo del host y verifica 1 commit en verde; caso recorded intacto; sin API en vivo]
closure_criteria: [SubprocessInvoker Windows-safe + golden cross-platform verde + sin regresion + handoff autocontenido + claim liberado al pasar a in_review]
---

# TASK-0039 - SubprocessInvoker robusto en Windows (fix shlex.split posix)

> `implementation` -> SDD; implementar contra [SPEC-0036](../specs/SPEC-0036-subprocess-invoker-windows-safe.md).
> **Defecto real** hallado en la PRIMERA CORRIDA REAL (smoke en repo temporal, 2026-06-06) del adapter LLM.

## Resumen
`SubprocessInvoker.from_command` usa `shlex.split(command)` en modo POSIX, que interpreta el `\` de las
rutas Windows como escape y corrompe el comando => `subprocess` falla con `WinError 2`. El invoker REAL
es inusable en Windows con rutas nativas (en el smoke hubo que pasar el comando con `/`). Como el operador
opera en Windows, esto bloquea cualquier corrida real en su entorno. Arreglar la tokenizacion para que sea
correcta en el SO anfitrion sin romper POSIX, con golden cross-platform.

## Evidencia (smoke 2026-06-06)
Comando `C:\...\python.exe "C:\...\agent.py"` => `FileNotFoundError [WinError 2]` en
`SubprocessInvoker.run` -> `subprocess.run`. Mismo comando con `/` => verde (loop M1 commitea 1 vez,
camino rojo por allowlist rechaza sin commit). El fix elimina la necesidad del workaround `/`.

## archivos objetivo (previstos)
- `runtime/adapters/llm_adapter.py` (`SubprocessInvoker.from_command`)
- `examples/llm_adapter_cases/` (golden cross-platform; o nuevo dir)

## Dogfood
Liveness por turno + handoff-release (commitea WIP y libera claim al pasar a in_review). ASCII-only en
mailbox/state (DECISION-0012). Te ratifico adversarialmente (idealmente con un caso que use el separador
nativo del host).
