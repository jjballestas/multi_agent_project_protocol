---
id: TASK-0004
owner: Codex
status: proposed
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0001]
phase: P0
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
- [ ] Generar una instancia de prueba + correr el validador → OK.
- [ ] Sustituye todos los `{{...}}`; no deja placeholders sin resolver.
- [ ] Multiplataforma; sin dependencias pesadas; sin secretos.
- [ ] Reclamar en CLAIMS.json (scope `scripts/`) antes de editar; handoff autocontenido.

## riesgos
- Desincronización si cambian los placeholders: el script debe detectar placeholders no resueltos.

## preguntas_abiertas
- ¿Python, PowerShell o ambos? Proponer en el handoff (recomendado: Python por portabilidad).
