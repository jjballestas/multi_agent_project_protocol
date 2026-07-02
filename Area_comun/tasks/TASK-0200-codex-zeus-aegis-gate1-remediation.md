---
task_id: TASK-0200
title: "Zeus-Aegis GATE 1 remediation: V3 atestacion honesta (no falso-verde), V4 PII en todos los campos servidos, V6 gate npm test fiable en clon limpio (SPEC-0107)"
type: integration
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0107
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0040, DECISION-0022]
file: Area_comun/tasks/TASK-0200-codex-zeus-aegis-gate1-remediation.md
---

# TASK-0200 - GATE 1 remediation (veredicto Analista TASK-0199)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Remedia los 3 REFUTADO del veredicto de GATE 1 del
> Analista. SOLO LECTURA (F2 sigue gateado). NO tocar core protocolo, #4, baseline. Ver
> Area_comun/artifacts/ANALISTA-TASK-0199-gate1-veredicto.md.

## Hallazgos a remediar

- **V3 (REFUTADO) - falso verde en atestacion del ledger.** Con el validador en ROJO y drift verde,
  `getGovernanceLedger` reporto attestation=verified en cada evento. El chip de atestacion puede salir verde
  mientras `validate_collaboration_state.py` esta rojo.
  - FIX: la atestacion servida debe INCORPORAR el resultado del validador (y validacion de firma/auth); si validate
    sale rojo, render NO-verde (tri-estado, fail-safe). El verde de atestacion exige validate verde.
- **V4 (REFUTADO) - PII en campos no redactados.** Un artifact con email en el NOMBRE de archivo filtro el email en
  `id`/`path`; el preview filtro un nombre de persona (Juan Perez). `redactFreeText` cubre email/phone/id en el
  cuerpo, pero NO los identificadores de display, paths ni nombres.
  - FIX: redactar TODOS los campos servidos: id, path, title/subject, preview, payload, metadata. Anadir redaccion
    de PII en filename/path y de nombres-de-persona. Tests negativos para PII en filename/path y nombre.
- **V6 (REFUTADO) - gate F0 no fiable en clon limpio.** `npm test` salio exit 1 (governance-readonly timeout, files
  timeout, mcp presets timeout/seed). El gate es FLAKY.
  - FIX: hacer `npm test` fiable exit 0 en CLON LIMPIO: subir el timeout / mockear las llamadas git+python pesadas
    del test de governance-readonly para que no expire; confirmar que las exclusiones del gate F0 (los 11 upstream,
    incl. mcp-presets) realmente aplican; si algun fallo es upstream no-F1, waiver acotado escrito que NO cubra
    fallos de F1.

## DoD

- AC1 (V3) atestacion del ledger NO sale verde si validate esta rojo; test que lo prueba (validate rojo -> chip no-verde).
- AC2 (V4) todos los campos servidos (id/path/title/preview/payload/metadata) redactados; tests negativos de PII en
  filename/path y nombre-persona pasan.
- AC3 (V6) `npm test` exit 0 ESTABLE en clon limpio (repetible); exclusiones F0 verificadas; waiver acotado si aplica.
- AC4 sigue read-only (denylist intacta); core protocolo intacto; handoff a Arquitecto (checker).

## Nota

- Tras checker verde, re-disparo GATE 1 (review del Analista) sobre el HEAD remediado antes de cerrar F1.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- POLITICA: el Arquitecto actualiza Zeus-Aegis/pipeline.html tras cerrar este caso.
