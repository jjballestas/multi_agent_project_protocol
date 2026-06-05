---
id: TASK-0003
owner: Claude
status: done
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0001, TASK-0002]
phase: P0
review: Done por Claude (arquitecto). CHANGELOG.md + DECISION-0001 (SemVer con ejemplos, mecanismo protocol_version, procedimiento de release y aprobacion humana de MAJOR). Campo protocol_version anadido a template/live/ejemplo. Handoff a Codex por impacto en TASK-0004.
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
- [x] SemVer documentado: qué es breaking (mayor), feature (menor), fix (parche) en un protocolo
      (DECISION-0001, tabla con ejemplos concretos + regla de desempate "ante la duda, MAJOR").
- [x] CHANGELOG con historial inicial (v0.1.0 + sección Unreleased hacia v0.2.0).
- [x] Releases mayores requieren aprobación humana (DECISION-0001 §4, coherente con AGENTS.md §5).
- [x] Mecanismo `protocol_version` definido y aplicado (template + live + ejemplo + README).

## riesgos
- Ambigüedad de "breaking" en un protocolo de archivos: dar ejemplos concretos.

## preguntas_abiertas
- Ninguna bloqueante.
