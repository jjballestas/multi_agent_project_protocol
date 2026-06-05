---
handoff_id: HANDOFF-TASK-0002-claude-to-codex-1
task_id: TASK-0002
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: no
---

# Handoff: bootstrap del repo del protocolo hecho → TASK-0002 lista para ti

## 1. Contexto mínimo
`multi_agent_project_protocol` es el protocolo genérico (v0.1.0, tag publicado). Lo estamos
**enriqueciendo** y el repo **se gestiona a sí mismo** (dogfooding). Claude (arquitecto) hizo el
bootstrap del estado vivo; tú (Codex, implementador) tienes tu primera tarea de implementación.

## 2. Qué hizo Claude (el bootstrap que observaste)
- Instancia viva: `AGENTS.md`, `CLAUDE.md`, `protocol.config.json` (live; el master se renombró a
  `protocol.config.template.json`), `Area_comun/README.md` y estado vivo
  (`PROJECT_STATE.json`, `TASK_INDEX.json`, `CLAIMS.json`).
- Áreas privadas: `Claude/` (mía). **Respeté tu `Codex/`** (Memory.md + README.md que ya creaste);
  no lo toqué.
- `.claude/settings.json` (allowlist segura). Tag `v0.1.0`.
- Backlog P0 abierto: **TASK-0001** (Claude, roadmap v0.2.0) y **TASK-0002** (tuya, abajo).
- Docs (`README.md`, `README_INSTANCIACION.md`) actualizadas por el renombrado de la config-master
  y el dogfooding.

## 3. Tu tarea: TASK-0002 — Validador multiplataforma (Python) + CI
Ver `Area_comun/tasks/TASK-0002-codex-cross-platform-validator-ci.md`. Resumen:
- Crear `scripts/validate_collaboration_state.py` con **paridad funcional** del `.ps1` actual
  (mismos chequeos: `state_invariants`, task files, status match, deliverables de done/in_review,
  mailbox, claims, handoffs con `requires_response`).
- Crear `.github/workflows/validate.yml` que corra el validador (sobre `examples/minimal_instance`
  y la raíz) en cada push/PR.
- Handoff a Claude para revisión cruzada.

## 4. Cómo coordinar (importante)
- **Recláma TASK-0002 en `CLAIMS.json`** (scope `scripts/`, `.github/`) antes de editar, y ponla
  `claimed`/`in_progress` en el archivo de tarea **y** en `TASK_INDEX.json` (deben coincidir).
- **Es paralelizable con TASK-0001** (yo trabajo el roadmap; tú el validador): tocan archivos
  distintos. Si ambos editamos `TASK_INDEX.json`, coordinamos por claim/secciones.
- Mantén el núcleo **neutral de dominio**; sin secretos.

## 5. Verificación esperada
- `powershell -NoProfile -File scripts/validate_collaboration_state.ps1` → OK (estado actual).
- Tu `validate_collaboration_state.py` debe dar el mismo veredicto OK sobre
  `examples/minimal_instance` y la raíz.

## 6. Pregunta abierta (no bloqueante)
¿Mantener ambos validadores (.ps1 + .py) o deprecar el .ps1? Propón en tu handoff; lo decidimos.

## 7. Punteros
- Tarea: `Area_comun/tasks/TASK-0002-codex-cross-platform-validator-ci.md`
- Estado: `Area_comun/state/PROJECT_STATE.json`, `TASK_INDEX.json`
- Contrato: `AGENTS.md` · Validador de referencia: `scripts/validate_collaboration_state.ps1`
