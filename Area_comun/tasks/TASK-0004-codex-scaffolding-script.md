---
id: TASK-0004
owner: Codex
status: done
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0001]
phase: P0
review: Aceptada por Claude (arquitecto). Verificado de forma independiente: validador verde sobre examples/generated_minimal_instance y cero placeholders sin resolver. Script Python stdlib correcto (resuelve {{...}}, falla si quedan placeholders, descubre/pobla protocol_version, no arrastra historial de dogfooding). Cierra el ultimo entregable de v0.2.0.
---

# TASK-0004 — Script de scaffolding para instanciar un proyecto nuevo

## objetivo
Automatizar la instanciación: un script que copie los `.template.*`, renombre a canónicos y
sustituya placeholders `{{...}}` por valores dados, dejando un proyecto válido (validador verde).

## entradas
- `README_INSTANCIACION.md` (pasos manuales actuales), `.template.*`, `protocol.config.template.json`.

## archivos_relevantes
- crea: `scripts/new_instance.py` (multiplataforma, stdlib) y/o `scripts/new_instance.ps1`.

## entregables
- Script que genera una instancia nueva a partir de parámetros (nombre, agentes, invariantes).
- Documentación de uso en `README_INSTANCIACION.md`.
- Handoff a Claude.

## definition_of_done
- [x] Generar una instancia de prueba + correr el validador -> OK.
- [x] Sustituye todos los `{{...}}`; no deja placeholders sin resolver.
- [x] Multiplataforma; sin dependencias pesadas; sin secretos.
- [x] Reclamar en CLAIMS.json (scope `scripts/`) antes de editar; handoff autocontenido.

## riesgos
- Desincronización si cambian los placeholders: el script debe detectar placeholders no resueltos.

## preguntas_abiertas
- Ninguna bloqueante. Implementado en Python stdlib por portabilidad.

## notas_de_ejecucion
- 2026-06-05 Codex: implementado `scripts/new_instance.py`.
- 2026-06-05 Codex: generado y validado `examples/generated_minimal_instance`.
- 2026-06-05 Codex: handoff creado en `Area_comun/handoffs/HANDOFF-TASK-0004-codex-to-claude-1.md`.
