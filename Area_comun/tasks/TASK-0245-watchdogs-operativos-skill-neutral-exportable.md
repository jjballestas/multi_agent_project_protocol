---
task_id: TASK-0245
title: "[VISION-NOVA][infra] Portar los watchdogs operativos a la capa neutral skills/ (exportable via new_instance)"
type: feature
status: proposed
owner: Codex
phase: P2
priority: medium
created_at: 2026-07-03
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, DECISION-0061]
linked_decisions: [DECISION-0061, DECISION-0085]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0245-watchdogs-operativos-skill-neutral-exportable.md
intake:
  type: feature
  goal: Crear una skill DOMINIO-NEUTRAL en la capa exportable skills/ que arme los 3 monitores operativos (entregas + demora-tarea + acumulacion-mailbox) al iniciar sesion, para que new_instance la lleve a toda instancia.
  acceptance:
    - Nueva skill neutral en skills/ (p.ej. skills/session-watchdogs.skill.md) con el procedimiento de armado de los 3 watchdogs, SIN terminos de dominio/negocio (scan_domain_neutrality verde sobre skills/).
    - Registrada en skills/skills.config.json (off-by-default, como el resto de la capa).
    - Los patrones son genericos y parametrizados (rutas de mailbox/estado/cron por config del template), NO hardcodean rutas del hub ni nombres de peers especificos del dogfooding.
    - new_instance lleva la skill a la instancia: verificar que una instancia recien generada desde el tag la contiene en su skills/ y el loader READ-ONLY la resuelve.
    - Caso de prueba en examples/ (o el suite de skills) que valida que la skill carga y es neutral.
    - Gates verdes en clon limpio; el epoch pineado y protocol.config.json intactos.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - skills/
    - examples/
  out_of_scope:
    - NO toca protocol.config.json ni el epoch pineado (1.14.0 byte-identico).
    - NO mueve las skills session-local de .claude/skills (esas siguen siendo del harness Claude Code; esta tarea crea el equivalente NEUTRAL exportable en skills/).
    - NO cablea hooks del harness (fuera de alcance; la skill es doc + loader read-only, DECISION-0061).
  risk: low
  estimate: M
---

# TASK-0245 - [VISION-NOVA] Watchdogs operativos como skill neutral exportable

Owner: Codex (implementa) + Arquitecto (checker de neutralidad) + Analista (review adversarial).

## Contexto (directiva operador 2026-07-03)
Los 3 monitores operativos del coordinador (entregas + demora-tarea 15-min + acumulacion-mailbox) son
el ENFORCER MECANICO de las reglas de coordinacion (una regla de disciplina se cae bajo carga; miss real
durante F2). Hoy viven en `.claude/skills/` (session-local de Claude Code) que NO se exporta con
new_instance. El operador pide que se puedan EXPORTAR al instanciar la metodologia: una instancia
(Aegis, y futuras) debe armar los mismos watchdogs en el arranque de sus agentes.

## Alcance
Portar el comportamiento de armado de watchdogs a la capa NEUTRAL `skills/` (DECISION-0061, exportable
via new_instance): una skill doc dominio-neutral + registro en skills.config.json (off-by-default) +
verificacion de que new_instance la lleva y el loader read-only la resuelve. Recetas fuente (a
neutralizar/parametrizar): watchdog v3.1 (demora 15-min / hung-exec / cron-dead) y watchdog de higiene
(acumulacion mailbox), documentados en la skill arquitecto-monitor-coordina (s.1b/1c/1d).

## DoD (testable)
Ver bloque intake (acceptance). Cierre: GO adversarial del Analista + neutralidad verde + una instancia
generada desde el tag contiene la skill y la carga.
