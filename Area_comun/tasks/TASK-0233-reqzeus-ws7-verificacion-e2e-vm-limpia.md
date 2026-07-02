---
task_id: TASK-0233
title: "[VISION-NOVA][F2.2] Verificacion e2e distribuida: un clon limpio opera 1 tarea completa solo via Git [re-alcance: pivote Vision Nova, DECISION-0083]"
type: verify
status: proposed
owner: Analista
phase: P2
priority: high
created_at: 2026-07-02
reviewer: Arquitecto
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0075, DECISION-0076, DECISION-0077, DECISION-0083]
linked_reqs: [REQ-ZEUS-001]
depends_on: [TASK-0226, TASK-0229, TASK-0230, TASK-0231, TASK-0232]
file: Area_comun/tasks/TASK-0233-reqzeus-ws7-verificacion-e2e-vm-limpia.md
---

# TASK-0233 - [VISION-NOVA][F2.2] Verificacion e2e distribuida (re-alcance DECISION-0083)

- **Owner (maker):** Analista - **Review:** Arquitecto - **Checker:** Arquitecto. maker != checker.
- **Precondicion:** el alta del Analista como participante (TASK-0228, WS5) YA se cumplio. Deps de workstream:
  WS1-WS6 (branding/bootstrapper/backend/instalador/runbooks) deben estar done antes de PROMOVER esta tarea.
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. Verificacion end-to-end en **VM/entorno LIMPIO** (sin residual
  de dev), como lo veria un empleado que instala Zeus-Aegis por primera vez.

## Alcance (checklist de aceptacion e2e)
1. **Instalacion limpia:** el producto se instala y arranca en una VM/entorno limpio siguiendo solo el runbook de
   empleado (WS10), sin pasos manuales ocultos ni dependencias de dev.
2. **Checklist de licencias MIT:** todo componente vendorizado (hermes-2.3.0 y demas) conserva su `NOTICE`/licencia
   MIT; no hay violacion de licencia; el inventario de licencias es correcto y verificable.
3. **Cero "hermes" visible al usuario:** ninguna cadena/branding/URL/env visible al empleado expone "hermes" ni el
   origen upstream (UI, i18n, pantallas de onboarding, mensajes de error). Los alias `ZEUS_*` funcionan; el shim de
   compat `HERMES_*` sigue operando pero NO es visible.
4. **Cero PII:** ningun dato personal identificable queda embebido en el paquete/artefactos/logs por defecto
   (nombres, correos, tokens, rutas de usuario, telemetria no consentida).
5. **Read-only del panel de gobernanza intacto** (no regresion de F1 / TASK-0227): el panel sigue sin write-paths.

## DoD
- e2e ejecutado en entorno limpio con evidencia reproducible (capturas/logs/inventario de licencias) adjunta en un
  artefacto `Area_comun/artifacts/ANALISTA-TASK-0233-*`.
- Los 5 puntos del checklist pasan; cualquier fallo se reporta como hallazgo falsable.
- Sin tocar el core del protocolo ni los pineados. Sin secretos. Neutralidad: `scope` producto (Zeus-Aegis).

## Handoff
Autocontenida. maker (Analista) != checker (Arquitecto). Ambiguedad -> blocked + 1 pregunta concreta.
NO promover hasta que WS1-WS6 esten done (esta tarea queda `proposed` a proposito).
