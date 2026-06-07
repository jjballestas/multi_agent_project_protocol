---
handoff_id: HANDOFF-TASK-0071-codex-to-claude-1
task_id: TASK-0071
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# TASK-0071 - F7.1 SBOM determinista

## Resumen

Implementada la primera rebanada de Fase 7: generador de SBOM canonico del paquete con inventario
determinista de archivos fuente, hashes sha256, tamanos, cuatro ejes de version, commit y timestamp provistos.

## Cambios principales

- `scripts/generate_sbom.py`
  - CLI determinista: `--root`, `--commit`, `--timestamp`, `--output`.
  - Salida JSON canonica (`ensure_ascii`, claves ordenadas, LF estable, UTF-8 sin BOM).
  - Inventario por ruta posix + sha256 + tamano.
  - Version axes: `protocol`, `runtime`, `schema.turn_schema`, perfiles (`profile_id`, `profile_version`).
  - Globs por defecto para fuente del paquete y exclusiones de estado/efimeros.
- `scripts/generate_sbom.ps1`
  - Wrapper delegado a Python para paridad.
- `examples/sbom_cases/run_sbom_cases.py`
  - Golden de arbol fijo, determinismo byte-identico, salida a archivo, cambio de hash y paridad ps1 si hay shell.
- `.github/workflows/validate.yml`
  - Agregada suite `Run SBOM generation cases`.

## Verificacion ejecutada

- `python examples\sbom_cases\run_sbom_cases.py`
- `python scripts\generate_sbom.py --root . --commit TEST --timestamp 2026-06-07T00:00:00Z | python -m json.tool`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\generate_sbom.ps1 -Root . -Commit TEST -Timestamp 2026-06-07T00:00:00Z | python -m json.tool`
- `python -m compileall scripts\generate_sbom.py examples\sbom_cases`
- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance`
- `python scripts\scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .`
- `python scripts\scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples\neutrality_scan_cases\run_neutrality_scan_cases.ps1`
- `python scripts\prune_state.py --root . --apply` (mantenimiento post-release: `claims_archived=1`,
  `next_actions_condensed=3`, `recovered_tokens=747`)
- `python scripts\prune_state.py --root . --check` => OK, prune not due (`cold_start_tokens=12603`)
- `git diff --check` (solo avisos CRLF de Windows, sin whitespace errors)

## Evidencia adicional

Sobre el repo vivo, el SBOM reporta `file_count=690`, protocol `1.0.0`, runtime `0.10.0`, turn schema `1.2.0`
y perfil `dotnet_enterprise 0.1.0`. Confirmado que no lista `runtime/state/`, `runtime/runs/`, `.git/` ni
`__pycache__`.

## Fuera de alcance respetado

- No firma.
- No provenance.
- No verificacion de release publicado.
- No secretos ni contenido de archivos en el SBOM.
- No cambio al turn schema ni al flujo de coordinacion.

## Nota de modo sombra

Los validadores del repo vivo emiten warning de drift de estado de protocolo porque el writer-vivo esta en modo
sombra (`event_state.enabled+materialize=true`, `enforce+authoritative=false`). El warning es esperado y no es
hard-fail.
