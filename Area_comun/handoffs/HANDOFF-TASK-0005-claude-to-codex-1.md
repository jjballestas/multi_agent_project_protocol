---
handoff_id: HANDOFF-TASK-0005-claude-to-codex-1
task_id: TASK-0005
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: yes
response_owner: Codex
requested_action: Construir profiles/dotnet_enterprise/ (TASK-0006) conforme al contrato profile.manifest, y anadir adopted_profiles + soporte de validador de forma aditiva (TASK-0007), manteniendo la neutralidad del core y la paridad .py/.ps1.
---

# Handoff: arquitectura de perfiles lista → desbloquea TASK-0006 y TASK-0007

## 1. Minimal Context
Cerré **TASK-0005**: ya existe la capa de perfiles del protocolo (DECISION-0002 materializada).
Esto **desbloquea** tus tareas TASK-0006 (perfil `dotnet_enterprise`) y TASK-0007 (`adopted_profiles`
+ soporte en validador), que dependían de TASK-0005.

## 2. What Was Done
- `profiles/README.md`: qué es un perfil, qué puede/no puede hacer, **contrato `profile.manifest`**,
  cómo instancia un proyecto (core o core+perfiles) y cómo se **registra la adopción**.
- `profiles/PROFILE_TEMPLATE/`: master **neutral** de un perfil →
  `profile.manifest.template.json` (solo placeholders), `README.md` y carpetas `docs/`,
  `templates/`, `prompts/`.
- `Area_comun/artifacts/ARQUITECTURA-core-profiles.md`: diagrama de 3 capas (core/profiles/examples),
  reglas de composición, mapa de directorios objetivo y decisión abierta sobre `adopted_profiles`.

## 3. What Was Not Done
- No creé `profiles/dotnet_enterprise/` (es TASK-0006, tuya).
- No toqué el validador ni `PROJECT_STATE.template.json` (es TASK-0007, tuya).
- No edité `README_INSTANCIACION.md` (estaba en tu claim activo de TASK-0004); la instanciación con
  perfiles quedó documentada en `profiles/README.md` §4-§5.

## 4. How To Verify
- `python scripts/validate_collaboration_state.py` → OK (raíz).
- Revisar `profiles/README.md` §3 (tabla de campos del manifiesto) y
  `profiles/PROFILE_TEMPLATE/profile.manifest.template.json`.
- Barrido de neutralidad: el `profile.manifest.template.json` y `profiles/README.md` no contienen
  términos de stack (solo placeholders / texto genérico).

## 5. Requested Action
1. **TASK-0006 — `profiles/dotnet_enterprise/`:** copia `PROFILE_TEMPLATE/`, rellena
   `profile.manifest.json` (con `requires_protocol_version`, p.ej. `">=0.2.0 <1.0.0"`), y empaqueta
   desde `D:\Agentes\entorno_open_cloude`: ADRs, branching, seguridad/secretos, pipelines (Azure
   DevOps), versionado de plantillas, onboarding, Dev Containers, SQL Server. **Sin secretos**
   (`.env` solo como `.example`). Todo dentro del perfil; **nada** al core.
2. **TASK-0007 — estado + validador:** añade `adopted_profiles` (opcional) a
   `PROJECT_STATE.template.json` y soporte en `validate_collaboration_state.{py,ps1}` de forma
   **aditiva** (instancias sin perfiles validan igual). Verifica el `requires_protocol_version`
   contra el `protocol_version` de la instancia. Mantén paridad `.py` ↔ `.ps1` con golden tests.
3. Crea una instancia de prueba que adopte core + `dotnet_enterprise` y valídala en verde.
4. Handoff de cierre a Claude para revisión de frontera (que nada del perfil se filtró al core).

## 6. Risks and Assumptions
- Riesgo principal: **fuga de dominio al core**. Lo reviso yo en tu handoff de cierre.
- Asumo `requires_protocol_version` compatible con la futura v0.2.0; ajústalo si v0.2.0 cambia algo.
- Convertir un chequeo de perfiles en obligatorio sería MAJOR: aplica solo si hay `adopted_profiles`.

## 7. Open Questions / BLOCKED
- No bloqueante: `adopted_profiles` ¿campo, decisión o ambos? Recomendación: ambos la primera vez.
  Decídelo al implementar TASK-0007 y déjalo en tu handoff.

## 8. Pointers
- `profiles/README.md`, `profiles/PROFILE_TEMPLATE/`
- `Area_comun/artifacts/ARQUITECTURA-core-profiles.md`
- `Area_comun/decisions/DECISION-0002-core-perfiles-profesionales.md`, `DECISION-0001-versionado.md`
- Tareas: `Area_comun/tasks/TASK-0006-*`, `TASK-0007-*`
- Insumo: `D:\Agentes\entorno_open_cloude` (docs/, templates/, prompts/, ONBOARDING.md)
