---
handoff_id: HANDOFF-TASK-0070-codex-to-claude-1
task_id: TASK-0070
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# TASK-0070 - Neutralidad exime runtime/state

## Resumen

Implementada SPEC-0056: `runtime/state/**` queda exento del scan de neutralidad en la config viva y
en el template, porque es estado generado de instancia. La fuente bajo `runtime/**` sigue escaneada.

## Cambios principales

- `protocol.config.json` y `protocol.config.template.json`
  - Agregado `runtime/state/**` a `domain_neutrality.exempt_globs`.
- `examples/neutrality_scan_cases/`
  - Nuevo caso `runtime_state_exempt`: un termino denylist bajo `runtime/state/**` pasa.
  - Nuevo caso `runtime_source_still_scanned`: el mismo tipo de termino en `runtime/source.py` falla.
  - El harness valida paridad Python/PowerShell en ambos casos.
- `scripts/scan_domain_neutrality.ps1`
  - Corregida la lectura de archivos de una sola linea para preservar paridad con Python.
- Docs
  - `Area_comun/protocol/N_AGENT_RUNTIME.md` y `README_INSTANCIACION.md` documentan que
    `runtime/state/` no se gitignora de forma general: en modo autoritativo contiene event log y
    snapshots fuente de verdad de la instancia y debe poder commitearse.

## Verificacion ejecutada

- `powershell -NoProfile -ExecutionPolicy Bypass -File examples\neutrality_scan_cases\run_neutrality_scan_cases.ps1`
- `python scripts\scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .`
- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance`
- `python scripts\scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .`
- `python scripts\prune_state.py --root . --apply` (mantenimiento post-release: `claims_archived=1`,
  `next_actions_condensed=3`, `recovered_tokens=825`)
- `python scripts\prune_state.py --root . --check` => OK, prune not due (`cold_start_tokens=13034`)
- `git diff --check` (solo avisos CRLF de Windows, sin whitespace errors)
- `git check-ignore -v runtime/state/snapshots/example.json` => no ignorado.

## Fuera de alcance respetado

- No se cambio el denylist.
- No se cambio el contrato del turn schema.
- No se activo `event_state.enabled`, `materialize`, `enforce` ni `authoritative`.
- No se gitignoro `runtime/state/`.

## Nota para revision

El fix deja desbloqueado el reintento de activacion sombra indicado en el GO de TASK-0070. La activacion
misma sigue fuera de esta tarea y queda para Claude tras ratificacion.
