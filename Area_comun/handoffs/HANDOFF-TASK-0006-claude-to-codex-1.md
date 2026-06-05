---
handoff_id: HANDOFF-TASK-0006-claude-to-codex-1
task_id: TASK-0006
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: yes
response_owner: Codex
requested_action: Implementar TASK-0007 contra la especificacion del borrador DECISION-0003 (campo adopted_profiles + chequeos aditivos del validador con paridad .py/.ps1); si algo de la spec no encaja, responder a este handoff o al borrador antes de implementar.
---

# Handoff: TASK-0006 aceptada → input para TASK-0007 (DECISION-0003 draft)

## 1. Minimal Context
Revisé tu entrega de **TASK-0006** (`profiles/dotnet_enterprise/` + `examples/dotnet_enterprise_instance/`).
**Aceptada y cerrada (`done`).** Para TASK-0007 dejé un **borrador de especificación**:
`Area_comun/decisions/DECISION-0003-adopted-profiles-contract.md`.

## 2. Resultado de la revisión (TASK-0006)
- **Frontera de neutralidad: OK.** Barrido sobre el core (`AGENTS.template.md`,
  `protocol.config.template.json`, `Area_comun/README.template.md`, `Area_comun/protocol/`,
  `scripts/`, `README*.md`) sin términos de stack. Lo .NET/SQL Server/Azure DevOps/Docker vive
  solo en `profiles/dotnet_enterprise/`. (Las menciones a `dotnet_enterprise` en archivos de
  estado son nombres de tarea/perfil, no política en el contrato — aceptable.)
- **Contrato:** `profile.manifest.json` conforme a TASK-0005 (`requires_protocol_version`,
  `stack`, `provides`, `adds_*`, `neutrality_note`). `provides` apunta a archivos existentes.
- **Secretos:** OK. Solo placeholders (`<CAMBIAR_POR_PASSWORD_LOCAL_SEGURA>`) y referencias a
  `$SA_PASSWORD`/`${localEnv:...}`; `.env.example` saneado; no se copió `.git/` ni `Analisis/`.
  `SOURCE_MAP.md` traza el origen.
- **Ejemplo:** `examples/dotnet_enterprise_instance/` valida en verde, con `adopted_profiles` y una
  decisión de adopción de instancia.

## 3. Qué NO hice
- No implementé TASK-0007 (es tuya). No toqué el validador ni `PROJECT_STATE.template.json`.
- DECISION-0003 está en **borrador** (pendiente de ratificación humana); no la marqué `accepted`.

## 4. How To Verify
- `python scripts/validate_collaboration_state.py --root examples/dotnet_enterprise_instance` → OK.
- Revisar `DECISION-0003-adopted-profiles-contract.md` §3 (spec del validador) y §1 (esquema del
  campo) — está alineado con la forma que ya usaste en el ejemplo.

## 5. Requested Action (TASK-0007)
1. Implementar el campo `adopted_profiles` (opcional) en `Area_comun/state/PROJECT_STATE.template.json`.
2. Añadir los chequeos **aditivos** del validador (`.py` y `.ps1`) según DECISION-0003 §3-§4:
   sin `adopted_profiles` → comportamiento idéntico al actual; con él → validar esquema, coherencia
   id/versión contra el manifiesto, `requires_protocol_version` vs `protocol_version`, dependencias
   y duplicados. Mantener **paridad `.py` ↔ `.ps1`** con golden tests (positivos y negativos).
3. Si algún punto de la spec no encaja con la implementación real, **respóndelo** (en este handoff
   o como comentario al borrador) y lo ajusto antes de ratificar DECISION-0003.
4. Handoff de cierre a Claude.

## 6. Risks and Assumptions
- No convertir chequeos en obligatorios para instancias solo-core (sería MAJOR): aplican solo si
  hay `adopted_profiles`.
- Subconjunto SemVer de `requires_protocol_version`: exacto y rangos con límites; rango no
  parseable → warning, no error (ver §3.3).

## 7. Open Questions / BLOCKED
- DECISION-0003 cierra (propone) la pregunta de "campo y/o decisión" → **ambos**. Confírmalo al
  implementar; si discrepas, dilo antes de que se ratifique.

## 8. Pointers
- `Area_comun/decisions/DECISION-0003-adopted-profiles-contract.md` (borrador, spec de TASK-0007)
- `profiles/dotnet_enterprise/`, `profiles/dotnet_enterprise/docs/SOURCE_MAP.md`
- `examples/dotnet_enterprise_instance/` (PROJECT_STATE.json con `adopted_profiles` + decisión)
- `Area_comun/tasks/TASK-0007-codex-profiles-state-validator.md`
- DECISION-0001 (versionado), DECISION-0002 (core/profiles/examples)
