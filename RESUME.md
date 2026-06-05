# RESUME.md - Como retomar este proyecto

> Cold start para `multi_agent_project_protocol`. Fuente de verdad: `AGENTS.md` y
> `Area_comun/state/`. Este repo se gestiona a si mismo con su propio protocolo.

## 1. Foto Actual

- Fecha de esta memoria: 2026-06-05.
- Rama: `main`.
- Version publicada: `v0.5.0`.
- Ultimo commit observado: `a74639b release(v0.5.0): comunicacion compacta token-efficient entre agentes`.
- Tag publicado: `v0.5.0`.
- Estado del arbol al actualizar esta memoria: limpio antes de editar `RESUME.md`.
- Claims activas: ninguna.
- Mailbox abierto: solo `.gitkeep`.
- Tareas: `TASK-0001..TASK-0015` estan `done`.
- Decisiones aceptadas/publicadas: `DECISION-0001..DECISION-0005`.

## 2. Validar Al Entrar

```powershell
cd d:\Agentes\multi_agent_project_protocol
git checkout main
git pull
git status --short --branch
python scripts\validate_collaboration_state.py --root .
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
```

Validaciones de regresion recomendadas:

```powershell
python scripts\validate_collaboration_state.py --root examples\minimal_instance
python scripts\validate_collaboration_state.py --root examples\generated_minimal_instance
python scripts\validate_collaboration_state.py --root examples\dotnet_enterprise_instance
python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance
python scripts\validate_collaboration_state.py --root examples\compact_communication_case
powershell -NoProfile -ExecutionPolicy Bypass -File examples\sdd_validation_cases\run_sdd_cases.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File examples\compact_comms_validation_cases\run_compact_comms_cases.ps1
```

## 3. Leer En Este Orden

1. `AGENTS.md`.
2. `Area_comun/README.md`.
3. `Area_comun/protocol/TASK_PROTOCOL.md`.
4. `Area_comun/protocol/COMMUNICATION_PROTOCOL.md`.
5. `Area_comun/state/PROJECT_STATE.json` (`next_actions` manda).
6. `Area_comun/state/TASK_INDEX.json`.
7. `Area_comun/state/CLAIMS.json`.
8. `Area_comun/mailbox/open/`.
9. La tarea concreta en `Area_comun/tasks/`.

## 4. Releases Cerrados

- `v0.1.0`: extraccion/bootstrap inicial del protocolo.
- `v0.2.0`: versionado, CHANGELOG, validador Python, CI, scaffolding.
- `v0.3.0`: arquitectura core/profiles/examples, perfil `dotnet_enterprise`, `adopted_profiles`.
- `v0.4.0`: SDD config-gated (DECISION-0004), specs, validadores SDD, `minimal_sdd_instance`.
- `v0.5.0`: comunicacion compacta token-efficient (DECISION-0005), soft-checks de mailbox,
  `MAILBOX_MESSAGE_TEMPLATE`, golden cases compactos y `compact_communication_case`.

## 5. Estado Funcional

- Fase activa: `P2 = adopcion y expansion`.
- Subfase `P2.SDD`: cerrada con `v0.4.0`.
- Capa de comunicacion compacta: publicada con `v0.5.0`.
- No hay tareas activas ni bloqueos registrados.
- Backlog abierto conceptual: adopcion en instancias reales, mas perfiles/ejemplos/docs.

## 6. Reglas Vigentes

- Core neutral de dominio: no meter negocio/trading/secretos en el nucleo.
- Cambios incompatibles requieren decision en `Area_comun/decisions/` y aprobacion humana.
- Tareas implementables nuevas siguen SDD: `spec_id`, `execution_pipeline`,
  `acceptance_criteria`, `linked_decisions`, `test_plan`, `closure_criteria`.
- Comunicacion compacta: usar `MAILBOX_MESSAGE_TEMPLATE.md`, una intencion por mensaje y una sola
  `question` si `requires_response:true`.
- Antes de editar: leer `TASK_INDEX.json`, `CLAIMS.json`, `mailbox/open/` y reclamar scope.
- No hacer commits parciales de release si Claude/orquestador tiene claim de release activa.

## 7. Proximos Pasos Probables

- Ratificacion humana pendiente de `v0.5.0` y, si aplica, releases/decisiones previas.
- Definir el siguiente backlog P2 con SDD:
  - adopcion del protocolo en `bot_spot_ai_strategy_pack`;
  - mas perfiles profesionales;
  - mas ejemplos de referencia;
  - documentacion de adopcion y migracion de instancias.

## 8. Archivos Clave Recientes

- `Area_comun/reports/REPORT-20260605-release-v0.5.0.md`
- `Area_comun/decisions/DECISION-0005-comunicacion-compacta-token-efficient.md`
- `Area_comun/protocol/MAILBOX_MESSAGE_TEMPLATE.md`
- `examples/compact_communication_case/`
- `examples/compact_comms_validation_cases/`
- `examples/minimal_sdd_instance/`
- `examples/sdd_validation_cases/`
