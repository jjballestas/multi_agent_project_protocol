# RESUME.md — Cómo retomar este proyecto (multi_agent_project_protocol)

> Para abrir una sesión nueva en frío y seguir enriqueciendo el protocolo. Fuente de verdad del
> estado: `Area_comun/state/`. Este repo **se gestiona a sí mismo** (dogfooding).

## 1. Posicionarse y validar
```
cd d:\Agentes\multi_agent_project_protocol
git checkout main && git pull
python scripts/validate_collaboration_state.py --root .              # debe dar OK
python scripts/validate_collaboration_state.py --root examples/minimal_instance
```
(También existe el validador PowerShell equivalente: `scripts/validate_collaboration_state.ps1`.)

## 2. Leer en este orden (cold start, AGENTS.md §0)
1. `AGENTS.md` (+ `CLAUDE.md` para reglas de Claude).
2. `Area_comun/README.md`.
3. `Area_comun/protocol/TASK_PROTOCOL.md` y `COMMUNICATION_PROTOCOL.md`.
4. `Area_comun/state/PROJECT_STATE.json` → **`next_actions`**.
5. `Area_comun/state/TASK_INDEX.json` y `CLAIMS.json`.
6. `Area_comun/mailbox/open/` (mensajes pendientes).
7. La tarea concreta en `Area_comun/tasks/`.

Atajo: `Claude/MEMORY.md` (mío) y `Codex/Memory.md` (de Codex) tienen el contexto condensado.

## 3. Dónde quedó (a 2026-06-05)
- Versión publicada: **v0.1.0** (tag). Fase **P0 = enriquecimiento** hacia v0.2.0.
- **Hecho:** dogfooding del repo (Área común viva, áreas privadas, `.claude/`), y **TASK-0002**
  (validador Python multiplataforma + CI) **done**. **TASK-0001** (roadmap) **done** →
  `Area_comun/artifacts/ROADMAP-v0.2.0.md`.
- **Backlog priorizado listo para trabajar (próximo):**
  1. **TASK-0003** (Claude) — Política SemVer + `CHANGELOG.md`.
  2. **TASK-0004** (Codex) — Script de scaffolding `new_instance`.
  - Candidatos futuros en el ROADMAP: más ejemplos, README principal, golden tests de paridad,
    plantillas PR/issue, guía de adopción upstream→instancia.

## 4. Reglas que no cambian
- **Núcleo neutral de dominio** (sin trading/negocio/secretos). Cambios de protocolo o
  compatibilidad → `Area_comun/decisions/` + (releases mayores) aprobación humana.
- `.template.*` = masters publicados; los canónicos vivos son la instancia dogfooding de ESTE repo.
- Codex corre en paralelo: revisa `TASK_INDEX/CLAIMS/mailbox` antes de crear/editar; respeta claims.

## 5. Relación con el otro repo
La instancia piloto de trading vive en `bot_spot_ai_strategy_pack` (repo aparte, en pausa). El
protocolo **no se propaga** a las instancias automáticamente: cada una lo adopta por decisión.

## 6. Para arrancar la nueva sesión
Sugerencia: reclama **TASK-0003** (Claude) y/o pásale **TASK-0004** a Codex (paralelizables,
tocan archivos distintos). O define con el operador el orden del ROADMAP v0.2.0.
