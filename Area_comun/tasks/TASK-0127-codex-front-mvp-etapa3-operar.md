---
id: TASK-0127
title: Proyecto-front MVP etapa 3 - Operar gobernado (RF-5..RF-8 SOLO via submit_intent, sin bypass) (DECISION-0049 / SPEC-0086)
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0029, DECISION-0022, DECISION-0047]
created_at: 2026-06-20
---

# TASK-0127 - Proyecto-front MVP etapa 3 (Operar gobernado)

## Objective

Etapa 3 del MVP (SPEC-0086), sobre etapa 1-2 (done). En `D:\Agentes\Zeus\Zeus-protocol`, **acciones
gobernadas** que el front emite **EXCLUSIVAMENTE via `runtime/submit_intent.py`** (escritor unico; sin
bypass de gates/#4/drift): RF-5 acciones SDD (crear DECISION/SPEC/task, abrir handoff, enviar mailbox), RF-6
GO del operador / responder requires_response, RF-7 disparar turno/run de agente, RF-8 disparar validacion
(validate/gates -> drift/cadena/firmas/anclas/scans). maker=Codex, checker=Arquitecto. Es la pieza de MAS
cuidado: ninguna ruta del front puede escribir el estado/ledger sin submit_intent.

## Alcance (SPEC-0086 etapa 3, RF-5..RF-8)

- TODA escritura al protocolo va por `submit_intent` (transaccion atomica, idempotente, actor/timestamp);
  el front NO toca events.jsonl / state/*.json / mailbox directo. Lectura por patron read-only (etapa 2).
- Disparos (run de agente, validacion) por las vias gobernadas; sin saltar gates ni #4.
- Codigo SOLO en Zeus-protocol; CI del producto verde; canal ASCII para lo que escribe al protocolo.
- Disciplina de canonico/clon limpio para escrituras (RNF-2): el front opera sobre el canonico, no el
  working tree volatil.

## DoD

SPEC-0086 **AC2 (escritura SOLO via submit_intent, con PRUEBA NEGATIVA: intento de escritura directa al
ledger -> ausente/rechazado por diseno)** + AC4 (sin bypass; no secretos; PII nunca al event log) + AC9
(cada accion = evento gobernado atestado) + AC1/AC5/AC6/AC7/AC10. maker=Codex/checker=Arquitecto; sin tocar
#4/config (epoca 1.14.0). Reporta a in_review con claim file-scoped + submit_intent.

## Verification

- CI del producto verde (node --test) + test que demuestra que toda accion de escritura pasa por
  submit_intent (mock/dry-run) y que NO existe ruta de escritura directa al ledger (prueba negativa).
- `validate_collaboration_state.py --root .` (con y sin secretos) + scans del protocolo exit 0; drift 0.
