---
id: TASK-0007
owner: Codex
status: ready
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0005]
relates_to: [TASK-0006]
phase: P1
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
- [ ] Compatibilidad hacia atrás: instancias sin perfiles validan exactamente igual que hoy.
- [ ] Paridad `.py` ↔ `.ps1` verificada (mismos resultados en los casos de prueba).
- [ ] `examples/minimal_instance/` sigue verde; añadir caso de prueba con un perfil adoptado.
- [ ] Sin dependencias pesadas; multiplataforma; sin secretos.
- [ ] Handoff autocontenido a Claude.

## riesgos
- Romper paridad de validadores: añadir golden tests del nuevo chequeo en ambos.
- Convertir un chequeo en obligatorio por error (sería MAJOR): los nuevos chequeos de perfiles
  solo aplican cuando la instancia declara `adopted_profiles`.

## preguntas_abiertas
- Ninguna bloqueante una vez cerrada TASK-0005.
