---
task_id: TASK-0177
title: "Proyecto-front: dictado por voz (microfono) en narrativa e intencion del Intake (REQ-003AE958, SPEC-0093)"
type: product
status: in_review
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0093
created_at: 2026-06-25
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-003AE958]
linked_decisions: [DECISION-0050, DECISION-0040]
file: Area_comun/tasks/TASK-0177-codex-front-dictado-voz.md
---

# TASK-0177 - Dictado por voz en el Intake (SPEC-0093)

> Front UX con FRONTERA de egress (Web Speech API). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA.
> Solo presentacion (app.js + CSS); sin nueva ruta de escritura. Repo producto Zeus-protocol.

## Alcance (SPEC-0093 AC1-AC4)
- AC1: icono de microfono esquina inferior derecha de los textarea Narrativa e Intencion (modal Manual + tarjeta).
- AC2: presionar -> captura por voz (SpeechRecognition) -> texto reconocido al textarea; segundo toque detiene.
- AC3 (egress): off-by-default; primera captura exige confirmar AVISO de egress ("usa reconocimiento del navegador,
  puede enviar audio a un servicio externo"); degradacion limpia si no hay soporte (deshabilitado + tooltip).
- AC4 (no-bypass/PII): el dictado solo llena el textarea; NO submit_intent; texto redactado en el submit gobernado.

## DoD
- AC1-AC4 + carries verdes con behavior-tests; node --test clon limpio exit 0 (estable); #4 byte-identica; sin
  nueva ruta de escritura. Checker Arquitecto clon limpio + PASADA DEL ANALISTA (egress opt-in/off-by-default/
  sin fuga; texto redactado). REPRO: microfono en los 2 textarea; aviso de egress en el 1er toque; dictar -> texto
  al textarea; sin soporte -> deshabilitado.
