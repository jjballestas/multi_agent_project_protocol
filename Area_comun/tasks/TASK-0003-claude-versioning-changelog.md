---
id: TASK-0003
owner: Claude
status: proposed
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0001, TASK-0002]
phase: P0
---

# TASK-0003 — Política de versionado (SemVer) + CHANGELOG

## objetivo
Definir cómo se versiona el protocolo (SemVer) y crear un `CHANGELOG.md` para que las instancias
puedan declarar "sigo protocolo vX" y rastrear cambios.

## entradas
- ROADMAP-v0.2.0.md, AGENTS.md, tag `v0.1.0`.

## archivos_relevantes
- crea: `CHANGELOG.md` (raíz), `Area_comun/decisions/DECISION-0001-versionado.md` (política).

## entregables
- `CHANGELOG.md` con v0.1.0 (extracción inicial) y sección Unreleased para v0.2.0.
- Decisión que fija SemVer y qué cuenta como cambio mayor/menor/parche del protocolo.

## definition_of_done
- [ ] SemVer documentado: qué es breaking (mayor), feature (menor), fix (parche) en un protocolo.
- [ ] CHANGELOG con historial inicial.
- [ ] Releases mayores requieren aprobación humana (coherente con AGENTS.md §5).

## riesgos
- Ambigüedad de "breaking" en un protocolo de archivos: dar ejemplos concretos.

## preguntas_abiertas
- Ninguna bloqueante.
