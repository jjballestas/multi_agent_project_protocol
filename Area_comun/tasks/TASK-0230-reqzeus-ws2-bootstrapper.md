---
task_id: TASK-0230
title: "[VISION-NOVA][F2.1] new_instance de nova-budget desde tag v1.18.0 + perfil de instancia (arm/mode + taxonomia de riesgo) [re-alcance: pivote Vision Nova, DECISION-0083]"
type: build
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0074, DECISION-0075, DECISION-0077, DECISION-0083]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0230-reqzeus-ws2-bootstrapper.md
intake:
  type: infra
  goal: Instanciar nova-budget desde el tag v1.18.0 con new_instance + perfil de instancia (arm/mode + taxonomia de riesgo), cosecha gentle-ai nivel B (configs commiteadas, dry-run + write atomico).
  acceptance:
    - new_instance genera la instancia nova-budget desde el tag v1.18.0 (no desde HEAD) en su repo propio, con protocol.config.json y estado inicial coherentes.
    - Perfil de instancia declarado (arm/mode + taxonomia de riesgo) y el TASK_TEMPLATE de la instancia extiende el bloque intake con los campos v2/DoR (target_user/functional_scope/assets_inputs/tech_constraints/risks_list/priority) para type feature/product, con regla anti-vacio.
    - Configs de agente COMMITEADAS en el repo de la instancia (Git es el adapter; NO se construyen adapters multi-IDE); new_instance usa dry-run + write atomico temp+rename.
    - PROHIBIDO 'gentle-ai install' (inyecta Engram; reabriria DECISION-0081). Verificado ausente.
    - Gates verdes en clon limpio; timebox 1 dia (el tiempo real se registra como dato del estudio).
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - scripts/new_instance.ps1
    - examples/
  out_of_scope:
    - No toca el nucleo neutral del hub ni el epoch pineado (protocol.config.json 1.14.0).
    - No instala Engram ni corre 'gentle-ai install'.
    - El codigo de producto vive en el repo de la instancia (D:/Agentes/Zeus/), no en el hub.
  risk: medium
  estimate: L
---

# TASK-0230 - [VISION-NOVA][F2.1] new_instance nova-budget (re-alcance DECISION-0083)

## Extension intake v2 del template de instancia (DECISION-0084; directiva Operador dae40ac)

El TASK_TEMPLATE de la instancia nova-budget EXTIENDE el bloque intake del hub con los campos
v2 de la Definition of Ready (anexo A de DECISION-0084; detalle en
personal/operador/vision-nova/CHECKLIST-DEFINITION-OF-READY-V2.md s.3):
- `priority: P1|P2|P3` (todo tipo).
- Para `type: feature|product` (obligatorios): `target_user` (1 linea), `functional_scope`
  (1-3 lineas), `assets_inputs` (lista | "ninguno"), `tech_constraints` (lista | "ninguna"),
  `risks_list` (lista >=1 | "ninguno declarado").
- REGLA ANTI-VACIO: "ninguno"/"ninguna" EXPLICITO vale; campo AUSENTE no vale; placeholder
  (TBD) invalido (R2). El enforcement estructural vive en la INSTANCIA (o v1.19 futura); el
  validador del hub NO cambia en F1.

- **Owner build:** Codex - **Review:** Analista - **Checker:** Arquitecto
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. Dep: D3 (0074), D4 (0075). Reusa `autoStartGateway` existente.

## Alcance (modulo en Electron main; idempotente; con logs)
1. En 1er arranque: **detecta/instala el gateway** (hermes-agent, D4 vendorizado o desde fuente).
2. **Apunta/instala el backend** de modelos (D3: router empresa por defecto; Ollama local donde haya GPU).
3. Escribe **config resuelta** en `~/.zeus`.
4. Levanta el gateway en `:8642` con **health-check / reinicio / cierre limpio**.

## DoD
- Maquina limpia -> gateway `:8642` corriendo + backend conectado **sin intervencion**.
- **0 procesos huerfanos** al cerrar; re-abrir es idempotente. Logs de arranque legibles.
- Claves fuera del repo (D3). Sin PII saliente. Gate Analista: GO. maker!=checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
