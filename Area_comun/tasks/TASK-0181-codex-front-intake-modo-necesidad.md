---
task_id: TASK-0181
title: "Proyecto-front: Intake modo 'necesidad' (dictar/escribir) -> mismo pipeline determinista no-LLM -> candidatas (SPEC-0095, REQ-7095D30A)"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0095
created_at: 2026-06-25
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-7095D30A]
reuses: [TASK-0179, TASK-0180]
linked_decisions: [DECISION-0050, DECISION-0040, DECISION-0056]
file: Area_comun/tasks/TASK-0181-codex-front-intake-modo-necesidad.md
---

# TASK-0181 - Intake modo "necesidad" (dictar/escribir) -> pipeline determinista (SPEC-0095)

> Nueva SUPERFICIE DE ENTRADA (textarea + voz) al pipeline de extraccion YA entregado de la carga por archivo.
> maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA. Solo presentacion + ruta al pipeline existente; sin
> nueva ruta de escritura. Repo producto Zeus-protocol. OFF-by-default. NO enciende el extractor LLM (Fase C).

## Alcance (SPEC-0095 AC1-AC4)
- **AC1:** modo "Necesidad" en el selector del Intake, junto a Manual y Por archivo (carry AC42; obligatorios
  validados). Design-system (AC13).
- **AC2:** formulario aparte con textarea grande + control de dictado por voz **reutilizado de TASK-0179/SPEC-0094**
  (es-CO, captura manual continuous con Stop/timer/indicador, egress opt-in/off-by-default + aviso). Texto
  escrito/dictado -> textarea.
- **AC3:** botonera estilo modo-archivo "Extraer" -> el texto del textarea se envia como FUENTE inerte (screened
  best-effort PII) al **MISMO consumidor determinista no-LLM** (provider deterministic-local, none_deterministic_no_llm,
  sin fetch/localVlm/http/net) -> candidatas en el store NO-LEDGER .runtime/file-candidates gitignored (drift 0;
  clon limpio sin store valida exit 0).
- **AC4:** revision + **gate PII humano** (AC43, piiReviewed===true) + aprobar -> requirement-intake gobernado
  (AC39), REUSANDO el panel/flujo del modo-archivo (TASK-0180). Id del requirement deriva del contenido editado;
  descartar purga el raw.
- **Carries verdes:** egress voz off-by-default + aviso; no-egress de modelo; store fuera del dataset + drift 0 +
  purga; OFF-by-default; #4 byte-identica; AC11/AC12/AC13.

## DoD
- AC1-AC4 + carries verdes con behavior-tests; node --test clon limpio exit 0; validate con/sin secretos exit 0;
  drift 0 con candidatas presentes; #4 byte-identica; sin nueva ruta de escritura. Checker Arquitecto clon limpio +
  PASADA DEL ANALISTA (PII del texto libre + egress de voz opt-in + no-egress de modelo + store fuera del dataset +
  gate PII humano efectivo). Commit como Arquitecto + Co-Authored-By: Codex.
- REPRO: Intake -> "Necesidad" -> textarea + mic; dictar/escribir -> Extraer -> 1 candidata editable; aprobar sin
  declarar PII = bloqueado; declarar PII + aprobar -> 1 requirement real; descartar -> purga; clon limpio sin store
  valida exit 0.

## Fuera de alcance
- El extractor LLM real (Fase C) + su frontera de egress (AC45/AC46): hoy 1 candidata determinista; 1..N llega al
  encender Fase C por usar el mismo pipeline. No encender ventana de modelo.
