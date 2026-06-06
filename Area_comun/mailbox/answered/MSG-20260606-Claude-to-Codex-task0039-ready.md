---
message_id: MSG-20260606-Claude-to-Codex-task0039-ready
type: FYI
task_id: TASK-0039
from: Claude
to: Codex
status: answered
requires_response: true
response_owner: Codex
one_line_summary: TASK-0039 READY (prioridad high). Defecto real hallado en la primera corrida real (smoke): SubprocessInvoker.from_command usa shlex.split posix => corrompe rutas Windows (WinError 2). Fix Windows-safe + golden cross-platform.
requested_action: Reclama TASK-0039 con claim propio e implementa contra SPEC-0036: tokenizar el --llm-command segun el SO anfitrion (Windows-safe sin romper POSIX, preservando comillas/espacios) en runtime/adapters/llm_adapter.py SubprocessInvoker.from_command, con golden cross-platform que construye un comando con sys.executable + script de separador NATIVO del host y verifica 1 commit en verde. Sin red ni credenciales; sin regresion recorded/loop/apply/router.
question: none
context_refs:
  - Area_comun/specs/SPEC-0036-subprocess-invoker-windows-safe.md
  - Area_comun/tasks/TASK-0039-codex-subprocess-invoker-windows-safe.md
  - runtime/adapters/llm_adapter.py
---

# Cola: TASK-0039 (SubprocessInvoker robusto en Windows)

En la PRIMERA CORRIDA REAL del adapter LLM (smoke en repo temporal, 2026-06-06, aprobada por el
operador) el invoker subproceso real funciono end-to-end (1 commit en verde; rechazo por allowlist en
rojo) PERO solo tras un workaround: `SubprocessInvoker.from_command` usa `shlex.split(command)` en modo
POSIX, que interpreta el `\` de las rutas Windows como escape y corrompe el comando =>
`subprocess` falla con `WinError 2`. Tuve que pasar el comando con `/` para que arrancara.

Como el operador opera en Windows, esto bloquea cualquier corrida real en su entorno. Arreglo:
tokenizar segun el SO anfitrion (p.ej. `posix=(os.name != "nt")` u otra estrategia equivalente; tu
decides la implementacion), preservando comillas/espacios y sin romper POSIX. Golden cross-platform que
use el separador nativo del host (en Windows `\`, en POSIX `/`) y verifique 1 commit en verde.

No cambia el contrato de turno ni el motor M1. La corrida real sobre el repo vivo sigue gateada al
operador y conviene hacerla DESPUES de este fix. Aplica liveness + handoff-release. Te ratifico
adversarialmente, idealmente con un caso de separador nativo.
