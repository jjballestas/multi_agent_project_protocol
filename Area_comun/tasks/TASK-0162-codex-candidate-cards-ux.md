---
task_id: TASK-0162
title: "Proyecto-front (RF-14): UX de tarjetas candidatas -- Aprobar muestra el bloqueo de PII visible, Usar tarjeta sincroniza el selector de modo, y al enviar la candidata cambia de estado + refresca (AC69-AC71, SPEC-0086)"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
created_at: 2026-06-23
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
depends_on: TASK-0161
file: Area_comun/tasks/TASK-0162-codex-candidate-cards-ux.md
---

# TASK-0162 - UX de tarjetas candidatas (AC69-AC71)

> Feedback de uso del operador: la extraccion YA genera tarjetas, pero la UX de aprobar/usar/estado es mala.
> maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA. OFF-by-default; #4 byte-id; ASCII-only; behavior-tests.
> Se ejecuta DESPUES de TASK-0161 (mismo flujo de Intake).

## Contexto (reportado por el operador)
1. Hay un boton "Aprobar" que no hace nada.
2. "Usar tarjeta" carga la opcion de requerimiento manual, pero hay que cambiar el selector a manual a mano o pone
   problemas.
3. Al enviar una tarjeta, sigue en el listado de tarjetas extraidas y no cambia de estado.

## Diagnostico del Arquitecto (head-start)
- AC69: `submitCandidateApproval` (public/app.js ~1516) exige `candidateDraft.piiReviewed`; si falta, escribe el
  error SOLO en #intake-preview (JSON, no visible) y vuelve -> "Aprobar no hace nada". El error debe ser VISIBLE en
  la tarjeta.
- AC70: `selectCandidateDraft` (~1501) llama `applyIntakeInputMode("typed")` (cambia la seccion) pero NO sincroniza
  el radio `intake-input-mode` -> estado inconsistente, el operador debe cambiar el selector a mano.
- AC71: `submitCandidateApproval` NO refresca el panel tras un envio exitoso -> la tarjeta sigue "pending". Falta
  (a) que el servidor marque la candidata approved/discarded en el store no-ledger, y (b) que el front refresque.

## Alcance (AC69-AC71)
- **AC69** El bloqueo de "Aprobar" por PII-no-revisada (o validacion) se muestra VISIBLE en/junto a la tarjeta (rojo),
  no solo en el preview JSON; el operador ve que debe marcar "PII revisada". Sigue gobernado (submit_intent + AC43).
- **AC70** "Usar tarjeta" sincroniza el radio/selector de modo a typed/manual (consistente con la seccion mostrada),
  sin pasos manuales.
- **AC71** Tras aprobar/descartar una candidata con exito: el servidor marca su estado (approved/discarded) en el
  store no-ledger de forma idempotente Y el front refresca -> la tarjeta refleja el nuevo estado o sale de pendientes.

## DoD
- AC69-AC71 verdes con behavior-tests: (69) aprobar sin PII-revisada -> error visible en la tarjeta (no solo
  preview); con PII -> procede. (70) usar tarjeta -> radio de modo en typed + seccion typed, consistente. (71)
  aprobar -> status approved y ya no pending; descartar -> discarded; panel refrescado.
- Carry AC16/AC17/AC43/AC51-AC68 (no-bypass, gate PII humano, candidatas no-ledger, loopback, auto-push, UX previa).
- node --test / CI verde EN CLON LIMPIO (captura EXIT explicito); validate con/sin secretos exit 0; drift 0;
  neutralidad + encoding 0. #4 byte-identica (protocol.config.json sin tocar). OFF-by-default intacto.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA.
- REPRO: server vivo + Ollama + subir un .md -> tarjetas; "Usar tarjeta" cambia a modo manual solo; "Aprobar" sin
  PII muestra el error en la tarjeta; con PII -> aprueba, la candidata cambia de estado y sale de pendientes.

## Notas
- AC71: marcar el estado de la candidata NO la mete al ledger (sigue en el store no-ledger); el requisito gobernado
  se crea por submit_intent (AC17) -- no crear un segundo escritor.
- NUNCA pilotar contra el log vivo: PROTOCOL_REPO_PATH a un clon desechable para el repro del write gobernado.
