# ROADMAP v0.2.0 — Enriquecimiento del protocolo multiagente

> Entregable de TASK-0001 (Claude). Prioriza los cambios hacia **v0.2.0** manteniendo
> neutralidad de dominio. Versión base publicada: **v0.1.0** (tag).

## Objetivo de v0.2.0
Hacer el protocolo **más portable, versionado y fácil de instanciar**, sin añadir política de
dominio al núcleo.

## Backlog priorizado

| Orden | Tarea | Owner | Estado | Valor |
|-------|-------|-------|--------|-------|
| 1 | **TASK-0002** Validador multiplataforma (Python) + CI | Codex | ✅ done | Portabilidad + verificación automática |
| 2 | **TASK-0003** Política de versionado (SemVer) + `CHANGELOG.md` | Claude | proposed | Releases trazables |
| 3 | **TASK-0004** Script de scaffolding `new-instance` (instanciar sin copiar a mano) | Codex | proposed | Adopción más fácil |

## Candidatos futuros (aún no formalizados como tareas)
- **Más ejemplos de instancia** además de `minimal_instance/` (p.ej. un proyecto CLI y uno web)
  para mostrar cómo se declaran fronteras de dominio distintas.
- **README principal** del repo con overview, badge de CI y enlace al CHANGELOG.
- **Golden negative tests** compartidos para garantizar paridad `.ps1` ↔ `.py` (evitar drift).
- **Plantillas de PR/issue** en `.github/` para el flujo de contribución.
- **Guía de adopción upstream→instancia**: cómo una instancia (p.ej. `bot_spot_ai_strategy_pack`)
  adopta una nueva versión del protocolo vía decisión.

## Criterios de aceptación de v0.2.0
- Validador disponible y verde en CI (multiplataforma). ✅ (TASK-0002)
- Política de versionado documentada + `CHANGELOG.md` con v0.1.0 y v0.2.0.
- Scaffolding probado: crear una instancia nueva y validarla en verde.
- Núcleo sigue neutral de dominio (barrido limpio).
- Tag `v0.2.0` publicado.

## Decisión pendiente (de TASK-0002)
¿Mantener ambos validadores (`.ps1` + `.py`) o deprecar el `.ps1`? **Recomendación:** mantener
ambos hasta v0.2.0 y reevaluar tras acumular historial de CI. Formalizar en una DECISION si se
deprecat­a uno.
