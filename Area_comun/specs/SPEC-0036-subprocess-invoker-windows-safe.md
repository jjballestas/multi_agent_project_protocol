---
spec_id: SPEC-0036-subprocess-invoker-windows-safe
task_id: TASK-0039
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0006, DECISION-0001]
created_at: 2026-06-06
author: Claude
---

# SPEC-0036 - SubprocessInvoker robusto en Windows (fix shlex.split posix)

> Estado: READY. Defecto real detectado durante la PRIMERA CORRIDA REAL (smoke en repo temporal,
> 2026-06-06) del adapter LLM (TASK-0036). Aditivo/correctivo; no cambia el contrato de turno ni el
> motor M1.

## Contexto
`runtime/adapters/llm_adapter.py` `SubprocessInvoker.from_command(command)` tokeniza el comando con
`shlex.split(command)`, que corre en **modo POSIX por defecto**. En Windows el separador de rutas es `\`
y shlex POSIX lo interpreta como caracter de escape, por lo que un comando con rutas nativas
(p.ej. `C:\Python\python.exe C:\tools\agent.py`) se corrompe y `subprocess` falla con `WinError 2`
(archivo no encontrado). Resultado: el invoker REAL es inusable en Windows con rutas nativas; en el smoke
hubo que reescribir el comando con `/` para que arrancara. El operador opera en Windows, por lo que esto
bloquea cualquier corrida real sobre la instancia viva en su entorno.

## Alcance
- Hacer que `SubprocessInvoker` acepte y ejecute correctamente un `--llm-command` con rutas NATIVAS del
  SO anfitrion (backslashes en Windows; comportamiento POSIX intacto en Linux/macOS). La tokenizacion debe
  ser correcta en el SO anfitrion (p.ej. `shlex.split(command, posix=(os.name != "nt"))` u otra estrategia
  equivalente; Codex decide la implementacion, pero el resultado debe preservar tokens con comillas y no
  romper rutas con separador nativo).
- Mantener el contrato actual: el subproceso recibe el prompt por stdin y devuelve por stdout un turn
  report JSON (o `{"report": <turn report>}`). El timeout y el manejo de returncode/stderr no cambian.

## No-alcance
- NO cambia el motor M1 (apply/gate/vcs), el router, el contrato de turno ni el RecordedInvoker.
- NO dispara ninguna corrida real sobre el repo vivo (sigue gateada al operador, DECISION-0009).
- NO introduce dependencias nuevas ni dominio.

## execution_pipeline
1. Ajustar `SubprocessInvoker.from_command` para tokenizar segun el SO anfitrion (Windows-safe) sin romper
   POSIX, preservando comillas/espacios.
2. Golden cross-platform en `examples/llm_adapter_cases/` (o nuevo dir) que construye un comando con
   `sys.executable` + ruta de script reales (con separador NATIVO del host) y verifica que el invoker
   ejecuta y el loop M1 produce 1 commit en verde. Determinista, sin red.
3. Regresion: el comando con `/` y el camino recorded siguen verdes.

## acceptance_criteria
- En Windows, `--llm-invoker subprocess --llm-command "<python.exe nativo> <script.py nativo>"` (rutas con
  `\`) ejecuta el subproceso y el loop M1 aplica el turno (1 commit en verde) sin `WinError 2`.
- En POSIX el comportamiento no cambia (rutas con `/`, comillas y espacios respetados).
- Golden cross-platform verde en el host de CI/desarrollo; sin red ni credenciales.
- Sin regresion en recorded ni en el resto de golden del runtime.

## linked_decisions
- `DECISION-0009` (runtime, adapters vendor-neutral). `DECISION-0006` (robustez operacional / portabilidad
  cross-platform). `DECISION-0001` (correctivo aditivo => PATCH/MINOR; sin cambio incompatible).

## test_plan
- Golden que tokeniza y ejecuta un comando con separador nativo del host (en Windows `\`, en POSIX `/`),
  verificando 1 commit en verde; caso recorded intacto; sin API en vivo. Paridad .ps1 n/a (python).

## closure_criteria
- `SubprocessInvoker` Windows-safe; golden cross-platform verde; sin regresion recorded/loop/apply/router;
  revision del arquitecto OK; claim liberado al pasar a in_review (handoff-release).

## Risks
- **Tokenizacion incorrecta entre SO** (comillas/espacios). Mitigacion: golden que cubre el host real;
  preservar semantica POSIX existente.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Comando con rutas nativas Windows ejecuta | TASK-0039 | golden cross-platform | 1 commit en verde sin WinError 2 |
| POSIX sin regresion | TASK-0039 | golden + recorded | rutas `/`/comillas intactas |
| Sin red ni credenciales | TASK-0039 | golden | deterministas sin API |
