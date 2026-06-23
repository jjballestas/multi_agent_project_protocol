---
task_id: TASK-0163
title: "Proyecto-front (RF-14): colision de ledger (canal ocupado) -> mensaje AMABLE 'Canal ocupado, intente mas tarde', nunca el comando crudo ni el traceback (AC72, SPEC-0086)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
created_at: 2026-06-23
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
depends_on: TASK-0162
file: Area_comun/tasks/TASK-0163-codex-ledger-busy-friendly-message.md
---

# TASK-0163 - Mensaje amable cuando el canal/ledger esta ocupado (AC72)

> Feedback del operador: al aprobar una candidata mientras un agente tenia un claim activo, el front mostro el
> comando crudo + traceback de Python ("Command failed: python runtime/submit_intent.py ... ERROR: claim acquire
> overlaps active claim CLAIM-...-Codex-TASK-0162"). Eso no debe verse. maker=Codex / checker=Arquitecto + Analista.
> OFF-by-default; #4 byte-id; ASCII-only. Se ejecuta DESPUES de TASK-0162.

## Contexto (reportado por el operador)
- El front y los agentes son ambos escritores del ledger y reclaman CLAIMS.json -> cuando un agente trabaja, la
  escritura del operador colisiona (DECISION-0020). El error que vio el operador fue el dump crudo del submit_intent.
- Pedido: que el front muestre algo tipo "Canal ocupado, intente mas tarde", no el error tecnico.

## Diagnostico del Arquitecto (head-start)
- src/server.js runSubmitIntent / runFileExtractionAgent surface el error del CLI submit_intent verbatim (incluye el
  argv completo + "ERROR: claim acquire overlaps active claim ..."). El catch debe detectar el error de CONTENCION
  (claim overlap / ledger busy) y devolver un error LIMPIO y tipado (sin argv ni stacktrace).
- public/app.js (submitCandidateApproval ~1516, submitFileExtraction, kickoff) muestra result.error tal cual -> debe
  mapear el error de contencion a un mensaje amable.

## Alcance (AC72)
- **Server**: detecta el error de contencion del submit_intent (claim acquire overlaps active claim, u otro de
  contencion) y responde un error LIMPIO y tipado (p.ej. 409 con code "ledger-busy" / "retry-later") SIN exponer el
  comando/argv ni el traceback. Otros errores tecnicos tampoco deben filtrar el argv crudo al cliente.
- **Front**: mapea ese error tipado a un mensaje amable visible ("Canal ocupado, intente mas tarde", rojo/aviso),
  idealmente con opcion de reintentar. Aplica a todas las escrituras gobernadas (aprobar candidata, requirement-intake,
  kickoff).

## DoD
- AC72 verde con behavior-tests: respuesta de submit_intent con claim-overlap -> el server responde error tipado de
  contencion (sin comando/traceback en el body) y el front muestra el mensaje amable (no el dump). Otros errores no
  filtran el argv crudo.
- Carry AC16/AC17/AC43/AC51-AC71 (no-bypass, gate PII, candidatas no-ledger, UX previa).
- node --test / CI verde EN CLON LIMPIO (EXIT explicito); validate con/sin secretos exit 0; drift 0; neutralidad +
  encoding 0. #4 byte-identica (protocol.config.json sin tocar). OFF-by-default intacto.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA.
- REPRO: aprobar/escribir mientras hay un claim activo de otro escritor -> el front dice "Canal ocupado, intente mas
  tarde", no el comando crudo.

## Notas
- NO cambiar la semantica de gobierno (la escritura sigue serializada por DECISION-0020); solo se mejora el MENSAJE.
- El fix de RAIZ de la colision (claim de grano fino para que escrituras a entradas distintas no colisionen) es una
  pieza/decision SEPARADA; aqui solo se trata el mensaje amable.
- NUNCA pilotar contra el log vivo: PROTOCOL_REPO_PATH a un clon desechable para el repro del write gobernado.
