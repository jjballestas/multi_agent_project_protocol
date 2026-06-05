# MEMORY.md — Memoria privada de Claude (Arquitecto del protocolo)

> Para mi yo de la próxima sesión. NO es contrato (eso es `AGENTS.md`) ni estado canónico (eso es
> `Area_comun/state/`). Referencia los canónicos; no los duplico.
> Última actualización: 2026-06-05.

## 1. Qué es este repo
`multi_agent_project_protocol`: el **protocolo multiagente genérico reutilizable**, extraído del
proyecto de trading (`bot_spot_ai_strategy_pack`) por DECISION-0005/0006. Versión publicada
**v0.1.0** (tag). Este repo **se gestiona a sí mismo** con su propio protocolo (dogfooding).

## 2. Quién soy aquí
Arquitecto Orquestador. Diseño/descompongo el backlog de enriquecimiento, reviso de forma
adversarial, mantengo `Area_comun/` y la **neutralidad de dominio**. Codex implementa (validador,
CI, scripts, tests). El operador aprueba releases y cambios incompatibles.

## 3. Para retomar (en orden)
1. `AGENTS.md`; 2. `Area_comun/state/PROJECT_STATE.json` (fase P0, next_actions);
3. `TASK_INDEX.json`; 4. `CLAIMS.json`; 5. `mailbox/open/`; 6. `Area_comun/reports/`.

## 4. Estado al cierre de la sesión (2026-06-05)
- Instancié el `Area_comun/` del repo (dogfooding) + áreas privadas `Claude/`, `Codex/`,
  `.claude/`, `CLAUDE.md`. Tag `v0.1.0`. Todo commiteado y pusheado a `main`.
- Fase **P0 = enriquecimiento**. **TASK-0001** (roadmap, `done` → `ROADMAP-v0.2.0.md`) y
  **TASK-0002** (Codex: validador Python + CI, **revisado OK por mí → `done`**).
- **Backlog priorizado dejado para la próxima sesión:** TASK-0003 (Claude, SemVer+CHANGELOG) y
  TASK-0004 (Codex, scaffolding). Ambas `proposed`, paralelizables.
- Cold-start de la nueva sesión: `RESUME.md` (raíz). Mensaje de buzón a Codex → `answered`.
- **Codex colabora bien aquí:** creó su `Codex/` y entregó TASK-0002 en paralelo sin colisión.

## 5. Reglas que no olvido
- Núcleo **neutral de dominio** (sin trading/negocio/secretos). Cambios de protocolo →
  `decisions/`. `.template.*` = masters publicados; vivos = instancia dogfooding.
- Codex puede correr en paralelo: revisar `TASK_INDEX/CLAIMS/mailbox` antes de crear/editar.
- El otro repo (trading) NO recibe mejoras del protocolo automáticamente: se adoptan por DECISIÓN.

## 6. Lecciones del proyecto madre (trading)
Codex corre EN PARALELO sobre los mismos archivos; respetar claims; comunicación barata en
tokens (ID + deltas + ACK/OK/CHANGES/BLOCKED); JSON de estado pueden quedar con BOM (leer en
Python con `utf-8-sig`); el validador corre sin `-ExecutionPolicy Bypass`.
