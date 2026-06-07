# runtime/ - Plano de control de orquestacion (opt-in, off by default)

> **Proprietary - All Rights Reserved** (ver `/LICENSE`, DECISION-0010).
> Capa de tooling neutral que orquesta el protocolo file-based. Adoptada por
> [DECISION-0009](../Area_comun/decisions/DECISION-0009-runtime-orquestacion.md); diseno en
> [DISENO-runtime-orquestacion-automatizada.md](../Area_comun/artifacts/DISENO-runtime-orquestacion-automatizada.md).
> **`enabled:false` por defecto:** una instancia sin el bloque `runtime` en `protocol.config` se
> comporta exactamente como hoy (coordinacion manual).

## Estado: M2 parcial (adapter LLM real gateado)
Esta carpeta contiene el contrato de turno, router determinista, loop M1 con apply+gate+commit,
observabilidad, y el hito M2 de adapter LLM real gateado. El adapter por defecto sigue siendo
`replay`; `llm` debe seleccionarse de forma explicita y la corrida real por subproceso exige un
flag adicional.

- `turn_schema.json` - esquema estricto del turn report que un agente devuelve por turno
  (contrato SPEC-0026).
- `context.py` - carga de estado compartida para runtime.
- `router.py` - `select_next(state)` puro y determinista (SPEC-0027).
- `turn_validate.py` - validacion de esquema + write-allowlist + anti-carrera (SPEC-0026).
- `orchestrator.py` - `--plan` dry-run y `--run` opt-in con `--adapter replay|llm`.
- `adapters/replay.py` - adapter determinista para fixtures y dogfooding.
- `adapters/llm_adapter.py` - `LLMAdapter` con `RecordedInvoker` (CI, sin red) y
  `SubprocessInvoker` (real, solo con `--allow-real-invoker` + `--llm-command`).

## Adapter LLM
Uso determinista en CI:

```text
python runtime/orchestrator.py --run --adapter llm --llm-invoker recorded --once --replay-report <transcript-or-dir>
```

El transcript recorded usa JSON local:

```json
{
  "format": "recorded_invoker.v1",
  "expected_prompt_contains": ["TASK-9000"],
  "report": { "turn_id": "...", "task_id": "TASK-9000", "...": "..." }
}
```

Uso real gateado:

```text
python runtime/orchestrator.py --run --adapter llm --llm-invoker subprocess --once --allow-real-invoker --llm-command "<command>"
```

La primera corrida real sobre el repo vivo queda pendiente de aprobacion puntual del operador. El
subproceso recibe el prompt por stdin y debe devolver por stdout un JSON de turn report, o
`{"report": <turn report>}`. El orquestador rechaza cambios de worktree no declarados en
`changed_paths`, valida la allowlist del claim y aplica el budget antes de mutar estado.

## Principios (no negociables, DECISION-0009)
Ficheros = fuente de verdad. 1 turno = 1 commit. Gate por turno + rollback. Gates humanos como
paradas duras. Adapters vendor-neutral. Determinismo en router/transiciones. Claim como lock.

## Neutralidad
`runtime/**` es tooling: se anade a `scan_globs` de neutralidad (no puede introducir terminos de
dominio). El dominio del piloto vive en la instancia, no aqui.
