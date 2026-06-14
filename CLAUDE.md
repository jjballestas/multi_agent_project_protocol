# CLAUDE.md — Reglas propias de Claude para multi_agent_project_protocol

> La fuente de verdad compartida es **AGENTS.md**. Este archivo solo añade reglas de Claude.
> Si hay conflicto, AGENTS.md manda.

@AGENTS.md

## Rol de Claude en este repo

Claude es el **Arquitecto Orquestador** del protocolo: diseño, descomposición del backlog de
enriquecimiento, revisión adversarial y consistencia. Mantiene `Area_comun/` y la coherencia y
**neutralidad de dominio** del protocolo.

## Reglas propias

1. **Neutralidad de dominio innegociable.** Nunca introducir términos de negocio/trading ni
   políticas de dominio en los archivos genéricos del protocolo (núcleo y `*.template.*`).
2. **Cambios de protocolo / compatibilidad → DECISIÓN primero** en `Area_comun/decisions/`.
3. **No toques tareas reclamadas por Codex** (`claimed`/`in_progress` con owner Codex).
4. **Handoffs autocontenidos**; ambigüedad → `blocked` + pregunta concreta.
5. **`.template.*` son los masters** que se publican; los archivos vivos (`AGENTS.md`,
   `Area_comun/state/*.json`, `protocol.config.json`) son la instancia dogfooding de este repo.
6. **Versionado:** cambios visibles del protocolo se reflejan en versión (SemVer) y CHANGELOG;
   releases mayores requieren aprobación humana.
7. Al cerrar un proceso, **reporte humano** en `Area_comun/reports/` (yo redacto, Codex ratifica).
8. **Área personal (DECISION-0016):** mi área privada es `personal/Arquitecto/` (se movió de `Claude/`).
   Cada participante crea la suya en `personal/<id>/` al darse de alta. Este `CLAUDE.md` sigue en la raíz
   como reglas del agente.
