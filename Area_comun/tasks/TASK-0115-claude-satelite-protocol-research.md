---
id: TASK-0115
title: Satelite protocol_research (read-only, unidireccional) - estructura + scaffolding (DECISION-0035)
type: documentation
status: done
owner: Claude
phase: P2
priority: medium
spec_id: none
linked_decisions: [DECISION-0035]
created_at: 2026-06-14
---

# TASK-0115 - Satelite protocol_research (estructura + scaffolding)

## Objective

Autorizar y montar el satelite de investigacion `protocol_research/` acotado a ESTRUCTURA + SCAFFOLDING
(no corre nada, no publica), por el metodo de DECISION-0035 (aditiva, neutral, MINOR 1.8.0). maker !=
checker: analista hizo la pasada (RATIFICABLE; concurrio con la reconciliacion de gates al brief 07);
operador ratifico + GO.

## Expected output

- DECISION-0035 en el Core (autorizacion + acoplamiento unidireccional + gates GATE-DATASET/GATE-INST/
  PRE-REG + alcance #1), registrada por escritor unico.
- Repo SEPARADO read-only en `d:\Agentes\protocol_research` (hermano del Core): README (coupling + gates),
  gates/GATES.md, datasets/mast_over_history (README+schema, sin datos), stubs OFF y NO ejecutables de
  exporter #2 (GATE-DATASET), feed #3 (GATE-DATASET) y harness ablacion/TFM (GATE-INST + PRE-REG).
- CHANGELOG [1.8.0]; protocol_version 1.7.0 -> 1.8.0.

## Question to resolve

Como dar continente separado y read-only a #1/#2/#3/TFM con acoplamiento unidireccional explicito y
hard-stops nombrados, sin romper la neutralidad ni la independencia del Core, y sin correr/publicar nada.

## Closure criterion

Acceptance estructural de personal/Claude/drafts-research/ACCEPTANCE-and-CHANGELOG.md verde (estructura
presente; #1 sin datos; stubs OFF inertes; gates bien asignados; neutralidad sobre base real; satelite NO
estacionado en el Core); validador/encoding/neutralidad verdes; MINOR 1.8.0 + CHANGELOG; DECISION-0035
registrada por escritor unico; drift 0; repo satelite creado read-only. Nada corre ni se publica;
#3/#4/SA.4 intactos.
