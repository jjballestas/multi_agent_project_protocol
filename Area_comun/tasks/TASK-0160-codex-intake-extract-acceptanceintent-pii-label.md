---
task_id: TASK-0160
title: "Proyecto-front (RF-14): la subida-para-EXTRAER no debe exigir acceptanceIntent (desbloquea extraccion, alinea AC55) + alinear/limpiar la confirmacion de PII (AC64-AC65, SPEC-0086)"
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
file: Area_comun/tasks/TASK-0160-codex-intake-extract-acceptanceintent-pii-label.md
---

# TASK-0160 - Fix extraccion bloqueada por acceptanceIntent + PII label alineado (AC64-AC65)

> Feedback de uso del operador (carga por archivo). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA.
> OFF-by-default; #4 byte-identica; ASCII-only; behavior-tests por AC.

## Contexto (reportado por el operador)
1. Al intentar EXTRAER los requisitos sale el error "requirement-intake acceptanceIntent is required" -> la
   extraccion queda BLOQUEADA.
2. La confirmacion de PII ("Confirmo que revise PII y que esta accion escribe via runtime/submit_intent.py como
   relay acotado.") se ve mal / mal alineada.

## Diagnostico del Arquitecto (head-start)
- BUG1 (bloqueante): `src/server.js` `sanitizeFileExtractionUpload` (~linea 864) llama
  `validateHonestRequirementField("acceptanceIntent", acceptanceIntent)` -> exige acceptanceIntent en la
  subida-para-EXTRAER. Pero en modo archivo NO se pide ese campo (AC55: los campos vienen del archivo/modelo). La
  extraccion solo necesita archivo + proyecto (+ ack PII). El acceptanceIntent pertenece a la APROBACION por
  candidata (`sanitizeCandidate`, ~linea 993), no a la peticion de extraccion.
- BUG2 (UX): `public/app.js` (~linea 1215) `<div class="confirm-box"><label><input id="intake-pii-ack" ...> Confirmo
  que revise PII y que esta accion escribe via runtime/submit_intent.py como relay acotado.</label></div>` -- frase
  larga con jerga, mal alineada.

## Alcance (AC64-AC65)
- **AC64** La subida-para-EXTRAER NO exige acceptanceIntent: quita la validacion de acceptanceIntent (y de cualquier
  otro campo de requisito) de `sanitizeFileExtractionUpload`; acceptanceIntent OPCIONAL ahi (puede ir vacio). Manten
  REQUERIDO acceptanceIntent en `sanitizeCandidate` (aprobacion de candidata). Sigue exigiendo proyecto + ack PII
  para extraer. Carry AC43 gate PII + candidatas no-ledger.
- **AC65** Alinea y limpia la confirmacion de PII: checkbox alineado al inicio del texto, texto que envuelve limpio
  (CSS), y redaccion en lenguaje llano (simplifica "escribe via runtime/submit_intent.py como relay acotado" -> p.ej.
  "esta accion se ejecuta de forma gobernada"), sin perder el sentido. Label asociado al input.

## DoD
- AC64-AC65 verdes con behavior-tests deterministas: (64) extraccion con acceptanceIntent vacio -> 200 OK (no 400);
  aprobar candidata sin acceptanceIntent -> sigue 400. (65) checkbox+label asociados y contenedor con la alineacion.
- Carry AC16/AC17/AC43/AC51-AC63 (no-bypass, gate PII humano, candidatas no-ledger, loopback, auto-push, UX previa).
- node --test / CI verde EN CLON LIMPIO; validate con/sin secretos exit 0; drift 0; neutralidad + encoding 0.
- #4 byte-identica (protocol.config.json sin tocar). OFF-by-default intacto.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
- REPRO: con server vivo (runtime override + Ollama) subir `historias_panel_operar_agentes.md` -> la extraccion ya
  NO pide acceptanceIntent y salen las tarjetas; el check de PII se ve alineado.

## Notas
- NO cambiar la semantica de gobierno: el ack de PII sigue siendo obligatorio para extraer/aprobar (AC43); solo se
  simplifica el TEXTO y la alineacion, no la condicion.
- NUNCA pilotar contra el log vivo: si el repro necesita el write gobernado, PROTOCOL_REPO_PATH a un clon desechable.
