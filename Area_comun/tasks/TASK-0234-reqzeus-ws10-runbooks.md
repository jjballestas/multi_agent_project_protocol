---
task_id: TASK-0234
title: "[VISION-NOVA][F2.5] Runbook de onboarding remoto de empleados (objetivo <=1 dia, medido; alimenta HP6) [re-alcance: pivote Vision Nova, DECISION-0083]"
type: docs
status: done
owner: Arquitecto
phase: P2
priority: low
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0077, DECISION-0083, DECISION-0085]
linked_reqs: [REQ-ZEUS-001]
depends_on: [TASK-0230, TASK-0232, TASK-0233]
file: Area_comun/tasks/TASK-0234-reqzeus-ws10-runbooks.md
intake:
  type: doc
  goal: Runbook de onboarding remoto - como un empleado/agente NUEVO se une a la instancia de metodologia (NOVA/Aegis) via Git y opera 1 tarea de principio a fin, con objetivo medido <=1 dia (alimenta HP6).
  acceptance:
    - Runbook autocontenido en el hub que cubre el onboarding remoto EN FRIO: clonar la instancia Aegis (remoto privado), configurar el agente (config commiteado, Git como adapter), y operar 1 tarea completa (claim -> trabajo -> entrega -> cierre) coordinando solo via Git (usando el harness F2.3 y el ciclo e2e F2.2).
    - El runbook es operable por un agente/empleado que NO construyo la instancia (transferibilidad fuerte): pasos explicitos, sin dependencias de dev ni pasos manuales ocultos.
    - Declara el objetivo MEDIDO (<=1 dia de onboarding) y como se mide (alimenta HP6); la medicion real (replica employee-run pre-registrada) es validacion posterior, no parte del doc.
    - ASCII; gate doc-only (validate/encoding/neutralidad verdes); no toca el hub pineado.
    - GO adversarial del Analista.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/protocol/
    - personal/operador/vision-nova/
  out_of_scope:
    - NO ejecuta la medicion real con un empleado (esa es la replica employee-run pre-registrada, prueba distinta).
    - NO toca el core pineado (epoch 1.14.0 byte-identico) ni crea repos de producto.
    - NO instala Engram ni gentle-ai install.
  risk: low
  estimate: M
---

# TASK-0234 - [VISION-NOVA][F2.5] Runbook onboarding remoto (re-alcance DECISION-0083/0085)

- **Owner:** Arquitecto (Docs) - **Review:** Analista - **Checker:** Arquitecto.
- **Deps:** F2.1 (0230, done) + F2.3 (0232, harness) + F2.2 (0233, e2e). Entregable doc-only.

## Alcance (re-alcance DECISION-0083; body viejo de runbooks de instalacion Zeus-Aegis SUPERADO)
Runbook de ONBOARDING REMOTO: como un empleado/agente NUEVO se une a la instancia de metodologia
(NOVA/Aegis) via Git y opera 1 tarea completa de principio a fin, con objetivo MEDIDO <=1 dia
(alimenta HP6). Cubre: clonar la instancia (remoto privado), configurar el agente (config
commiteado, Git como adapter), operar 1 tarea via Git puro (harness F2.3 + ciclo e2e F2.2).

## Marco de transferibilidad (aclaracion operador 2026-07-03)
Aqui vive la prueba de transferibilidad FUERTE: el runbook debe ser operable por un agente que NO
construyo la instancia (a diferencia de F2.2, que probo el MECANISMO con Codex operando). La
MEDICION real (un empleado/agente fresco ejecuta el onboarding y se cronometra) es la replica
employee-run PRE-REGISTRADA, prueba DISTINTA y posterior; este doc entrega el runbook operable.

## DoD (testable)
Ver bloque intake (acceptance). Cierre: runbook autocontenido operable en frio + objetivo medido
declarado + gate doc-only verde + GO del Analista.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
