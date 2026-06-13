# Codex Startup Prompt

Copy-paste para arrancar otra sesion:

```text
Lee AGENTS.md y personal/Codex/STARTUP_PROMPT.md.
```

Con eso deberia saber continuar. Despues de leer este archivo, hacer el arranque operativo de abajo.

## Arranque Operativo

1. Leer `AGENTS.md`.
2. Leer `personal/Codex/Memory.md`.
3. Revisar estado vivo:
   - `Area_comun/state/PROJECT_STATE.slim.json`
   - `Area_comun/state/TASK_INDEX.slim.json`
   - `Area_comun/state/CLAIMS.slim.json`
   - `Area_comun/mailbox/open/`
4. Ejecutar:

```powershell
Write-Output SANDBOX_OK
git status --short
git log -5 --oneline
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\validate_collaboration_state.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
```

## Estado Esperado Al Escribir Este Prompt

- Fecha de refresco: 2026-06-14 Europe/Madrid.
- HEAD observado: `237f04d chore(state): commitea CLAIMS.slim.json (baja del claim TASK-0109 liberado en Part 2)`.
- Commits recientes importantes:
  - `e5c13a0 release(v1.4.0): activacion MEDIDA de compaction en la instancia viva (SPEC-0078/TASK-0106)`.
  - `d74caae release(v1.5.0): architect cierra sus analysis-tasks (DECISION-0032) + cierra TASK-0109`.
  - `04c236b chore(encoding): limpia bytes non-ASCII del canal mailbox (DECISION-0012)`.
  - `93dbb2b chore(state): reconcilia PROJECT_STATE.version a 1.5.0 via flujo de estado`.
  - `237f04d chore(state): commitea CLAIMS.slim.json (baja del claim TASK-0109 liberado en Part 2)`.
- `mailbox/open` esperado: solo `.gitkeep`.
- Claims activos esperados: ninguno.
- Drift esperado: `has_drift=false`, `up_to_seq=422`.
- Validador esperado: OK.
- `event_state.enabled/materialize/enforce/authoritative` estan activos; no editar `Area_comun/state/*.json` a mano.
- Runtime real invoker / SA.4 / Capa C siguen sin re-armarse salvo GO explicito.

## Tareas Calientes

Segun `TASK_INDEX.slim.json`, solo quedan propuestas para Codex:

- `TASK-0095`: commits de turno self-consistentes.
- `TASK-0096`: `run_id` unico por corrida del orquestador.
- `TASK-0100`: `.gitattributes eol=lf` para releases reproducibles cross-platform.

No reclamar ninguna sin revisar mailbox, claims y GO vigente del operador/Claude.

## Reglas Que Importan

- Usar `submit_intent.py` / `ledger_ops.py --submit` para estado compartido.
- Crear claim antes de editar rutas compartidas, incluido mailbox.
- Liberar claim al cerrar entrega o higiene.
- Despues de cada commit de Codex, actualizar `personal/Codex/Memory.md`.
- No tocar `personal/Claude/` ni `personal/operador/` salvo instruccion explicita.
- No revertir cambios ajenos ni limpiar `personal/operador/` solo porque aparezca untracked.

## Caveats

- Si un test con `tempfile` falla sandboxed con `WinError 5` / `PermissionError`, puede ser el caso conocido de ACL temporal en Windows sandbox. Reintentar solo lo necesario con elevacion y registrar la evidencia.
- Si `scan_encoding.py` vuelve a fallar, verificar primero si es deuda historica o una ruta tocada por Codex.
