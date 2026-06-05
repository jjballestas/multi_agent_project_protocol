---
id: TASK-0007
owner: Codex
status: done
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0005]
relates_to: [TASK-0006]
phase: P1
review: Aceptada por Claude (arquitecto). Paridad .py/.ps1 verificada por lectura (mismo patron profile_id, misma logica SemVer exacta/rango, mismos mensajes, misma politica warning-vs-fail). Golden cases ejecutados con .py - 6/6 con exit code esperado (valid=0, duplicate/version_mismatch/protocol_incompatible/missing_dependency=1, remote_reference_warning=0+warn). Compatibilidad hacia atras OK (instancias sin adopted_profiles validan igual). Conforme a DECISION-0003. Codex detecto correctamente el wording de profile_id (kebab_case -> patron real); enmendado en DECISION-0003. Ultimo entregable de v0.3.0.
---

# TASK-0007 — Soporte de perfiles en estado y validador

## objetivo
Hacer que el estado y el validador reconozcan los perfiles adoptados por una instancia, de forma
**aditiva y compatible** (cambio MINOR), manteniendo paridad `.py` ↔ `.ps1`.

## entradas
- TASK-0005 (contrato `profile.manifest`, decisión sobre `adopted_profiles`) — **bloqueante**.
- DECISION-0001 (aditivo = MINOR, no romper instancias sin perfiles) y DECISION-0002.

## archivos_relevantes
- edita: `Area_comun/state/PROJECT_STATE.template.json` (campo opcional `adopted_profiles`).
- edita: `scripts/validate_collaboration_state.py` y `scripts/validate_collaboration_state.ps1`.

## entregables
- Campo opcional `adopted_profiles` documentado en la plantilla de estado.
- Validador que, si una instancia declara `adopted_profiles`, verifica que cada perfil existe y
  que su `profile.manifest` es coherente (incluida compatibilidad `requires_protocol_version`
  contra el `protocol_version` de la instancia). Si no hay perfiles, comportamiento idéntico al
  actual (cero impacto en instancias existentes).
- Handoff a Claude.

## definition_of_done
- [x] Compatibilidad hacia atrás: instancias sin perfiles validan exactamente igual que hoy.
- [x] Paridad `.py` ↔ `.ps1` verificada (mismos resultados en los casos de prueba).
- [x] `examples/minimal_instance/` sigue verde; añadir caso de prueba con un perfil adoptado.
- [x] Sin dependencias pesadas; multiplataforma; sin secretos.
- [x] Handoff autocontenido a Claude.

## riesgos
- Romper paridad de validadores: añadir golden tests del nuevo chequeo en ambos.
- Convertir un chequeo en obligatorio por error (sería MAJOR): los nuevos chequeos de perfiles
  solo aplican cuando la instancia declara `adopted_profiles`.

## preguntas_abiertas
- Ninguna bloqueante una vez cerrada TASK-0005.

## notas_de_ejecucion
- 2026-06-05 Codex: añadido `adopted_profiles` opcional a `PROJECT_STATE.template.json`.
- 2026-06-05 Codex: implementado soporte aditivo en validadores Python y PowerShell.
- 2026-06-05 Codex: creados fixtures `examples/profile_validation_cases/` y verificada paridad.
- 2026-06-05 Codex: handoff creado en `Area_comun/handoffs/HANDOFF-TASK-0007-codex-to-claude-1.md`.
