---
id: TASK-0116
title: Narracion minima como regla DURA y uniforme para todos los agentes (DECISION-0036)
type: documentation
status: done
owner: Claude
phase: P2
priority: medium
spec_id: none
linked_decisions: [DECISION-0036]
created_at: 2026-06-14
---

# TASK-0116 - Narracion minima DURA y uniforme

## Objective

Afilar el addendum de narracion minima de DECISION-0005 a regla DURA y uniforme para TODOS los agentes,
en el contrato compartido (AGENTS.md s.7 + AGENTS.template.md s.7), por DECISION-0036. maker != checker:
analista dio RATIFICABLE-con-ajustes; ajustes incorporados; operador ratifico + GO.

## Expected output

- DECISION-0036 en el Core, registrada por escritor unico.
- AGENTS.md s.7 y AGENTS.template.md s.7 con el texto afilado (zero intra-execution narration; process
  reasoning al canal interno; un solo reporte final; binds all agents uniformly; carve-outs intactos;
  clausula de anomalia notificable DECISION-0018).
- CHANGELOG [1.9.0]; protocol_version 1.8.0 -> 1.9.0.

## Question to resolve

Como hacer enforcement DURO y uniforme de la narracion minima para todos los agentes (no solo via memoria
personal, que no se propaga), sin sobre-alcanzar (carve-outs) ni afirmar un gate automatico inexistente.

## Closure criterion

Texto afilado presente en AGENTS.md s.7 + template; carve-outs intactos; enforcement honesto (normativo +
peer-flag, no gate automatico); DECISION-0036 registrada por escritor unico; MINOR 1.9.0 + CHANGELOG;
neutralidad/validador/encoding verdes; drift 0. NO toca #3/#4/SA.4.
