---
task_id: TASK-0220
title: "Segunda ronda adversarial Engram (v3 honesta): atacar la HONESTIDAD y COMPLETITUD de las etiquetas de la matriz de estado (no re-litigar lo aceptado ABIERTO/DISCIPLINARIO)"
type: review
status: cancelled
owner: Analista
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
author_under_review: Arquitecto
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0020, DECISION-0040]
linked_tasks: [TASK-0219]
file: Area_comun/tasks/TASK-0220-analista-adversarial-review-engram-v3-honesty.md
---

# TASK-0220 -- Segunda ronda adversarial Engram (v3 honesta)

## Encargo

Tu ronda 1 (TASK-0219) cerro NO-GO con 6 bloqueantes. El Arquitecto respondio NO con "cerrado", sino
con una **MATRIZ DE ESTADO HONESTA** (v3). Tu trabajo AHORA es distinto: **NO re-litigar lo ya aceptado
como ABIERTO/DISCIPLINARIO; ATACAR que las ETIQUETAS de la matriz sean HONESTAS y COMPLETAS.** Postura
por defecto sigue siendo adversarial. author_under_review = Arquitecto.

## Artefactos a revisar (v3, sufijo -v2; v1 sin sufijo = audit trail de tu ronda 1, INTACTO)

- personal/Arquitecto/DRAFT-DECISION-engram-memory-backend-v2.md  (matriz de estado honesta v3)
- personal/Arquitecto/PATCH-engram-observation-intent-v2.md       (SPEC; NO implementado)

Etiquetas de la matriz (conjunto declarado): ESTRUCTURAL | ESTRUCTURAL-PENDIENTE-IMPL+TESTS |
ESTRUCTURAL-SI-PRECONDICION(<cual>) | DISCIPLINARIO | ABIERTO-DIFERIDO.

## Verificaciones (una por una, evidencia archivo/linea + grep)

1. **Sobre-afirmacion residual.** Alguna fila de la matriz AUN sobre-afirma? Busca "estructural" SIN
   precondicion declarada, o cualquier "cerrado/probado" aplicado a algo que (a) no tiene codigo merged,
   (b) tiene precondiciones no declaradas, o (c) aun admite prosa libre.
2. **B-PII: el fix real es hermetico?** Intenta meter prosa/PII por CUALQUIER campo que llegue a
   `events.jsonl`: `scope`, `task_id`, `supersedes`, `topic_key`, `memory_project` (y cualquier otro).
   Construye un payload falsable. Si entra prosa libre por algun campo, B **NO** es estructural -> la
   etiqueta miente.
3. **Precondiciones completas (patron 0040).** Las precondiciones declaradas (A: adoption_tier=runtime +
   chain_enabled; E: actor_auth_enforce atestado; el tier para el dataset_seal) -> estan TODAS las que el
   CODIGO REAL exige, o falta alguna NO declarada? (el patron 0040: lo disciplinario disfrazado de
   estructural por una precondicion silenciosa). Verifica contra runtime/ real.
4. **El PATCH inventa config/API inexistente?** El PATCH v3 cita allowlist de `eventlog.py` (243-277),
   `protocol.config.json -> event_state.engram`, guard `event_state_config_error`, `dataset_seal`,
   `adoption_tier`, etc. Verifica contra la FUENTE (runtime/eventlog.py, submit_intent.py,
   protocol_replay.py): existe cada forma de config/API citada, o el parche inventa alguna?

## Entregable (veredicto ESTRUCTURADO)

- Por CADA etiqueta de la matriz: **HONESTA | AUN-SOBRE-AFIRMA | PRECONDICION-FALTANTE**, con evidencia
  archivo/linea + el grep usado.
- Veredicto final: **GO-PROMOVER-OFF** (la DECISION es promovible OFF con la matriz honesta) **/ NO-GO**
  (lista de correcciones minimas).

## Reglas

- Narracion minima (DECISION-0038); un solo informe final firmado.
- Corre gates en CLON LIMPIO (validate/scan_encoding/neutralidad; drift; protocol.config.json
  byte-identico = guardrail TFM).
- No toques rutas bajo claim ajeno (los drafts son del Arquitecto: refutalos, no los edites).
- Si necesitas algo del Arquitecto, una pregunta concreta y espera.

## Definition of Done

Artefacto `Area_comun/artifacts/ANALISTA-TASK-0220-veredicto.md` + MSG REVIEW al Arquitecto; reclamado y
liberado via submit_intent firmado; commit como autor Analista. NO tocar task_status (lo lleva el Arquitecto).
