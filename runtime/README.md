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
python runtime/orchestrator.py --run --adapter llm --llm-invoker subprocess --once --allow-real-invoker --llm-preset claude
```

El invoker real esta apagado aunque `runtime.enabled` sea `true`. Para arrancarlo se requiere, a
la vez: `--once`, `--allow-real-invoker`, `--llm-command` o un `--llm-preset` declarado en
`runtime.llm_cli_presets`, y un registro local en `protocol.config.json`:

```json
{
  "runtime": {
    "real_invoker": {
      "enabled": true,
      "activation_decision": "DECISION-XXXX",
      "approved_by": "operador humano",
      "approved_at": "YYYY-MM-DD"
    }
  }
}
```

El subproceso recibe el prompt por stdin y debe devolver por stdout un JSON de turn report, o
`{"report": <turn report>}`. El orquestador rechaza cambios de worktree no declarados en
`changed_paths`, valida la allowlist del claim, aplica guardrails/tool-policy y budget antes de
mutar estado, y mantiene 1 turno = 1 commit. Las credenciales del CLI pertenecen al entorno local
del adoptante; no se commitean. La autonomia multi-turno no queda habilitada por este wrapper.

## Runtime override para autenticacion de eventos
`event_state.actor_auth_enforce`, `event_state.actor_auth_config` y las altas locales de
`event_auth.keys` no pertenecen al `protocol.config.json` pinned. Para ensayar o activar esas
credenciales se usa el override gitignored `event-state.runtime.json`, o la ruta indicada por
`EVENT_STATE_RUNTIME_CONFIG_PATH`. El archivo admite solo:

```json
{
  "event_state": {
    "actor_auth_enforce": true,
    "actor_auth_config": {
      "secret_root": "D:/Agentes/protocol-secrets",
      "keyids": {},
      "private_key_files": {}
    },
    "event_auth": {
      "keys": {
        "Analista": {
          "key_id": "analista-hmac:v1",
          "secret_file": "secrets/eventauth-analista.key"
        }
      }
    }
  }
}
```

Sin override, `actor_auth` queda OFF (`not_enforced_phase2`) y `event_auth.keys` usa solo el
mapeo del config pinned. Las entradas `event_auth.keys` del override se mergean sobre el config y
ganan por actor; solo se admite esa subclave. Un override malformado falla cerrado. Las claves
privadas y HMAC siguen fuera del repo y `protocol.config.json` no se toca, preservando el genesis
de cadena.

## Principios (no negociables, DECISION-0009)
Ficheros = fuente de verdad. 1 turno = 1 commit. Gate por turno + rollback. Gates humanos como
paradas duras. Adapters vendor-neutral. Determinismo en router/transiciones. Claim como lock.

## Gate de deriva del ledger

Desde la raiz de una instancia runtime, el gate verificable es:

```text
python runtime/protocol_replay.py --check-drift
```

Imprime `verdict=CLEAN|DRIFT` y `up_to_seq=<n>`. Sale 0 exclusivamente con
`has_drift=false`; la deriva, un argumento desconocido o la ausencia de
`--check-drift` producen un exit distinto de cero. Las automatizaciones deben gatear
el exit code, no buscar texto en stdout.

## Neutralidad
`runtime/**` es tooling: se anade a `scan_globs` de neutralidad (no puede introducir terminos de
dominio). El dominio del piloto vive en la instancia, no aqui.
