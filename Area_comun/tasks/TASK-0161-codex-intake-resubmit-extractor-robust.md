---
task_id: TASK-0161
title: "Proyecto-front (RF-14): re-subir archivo ya ingerido no rompe (auto-push idempotente=no-op) + extractor reporta causa especifica + robusto ante latencia local (precarga + timeout no clavado) (AC66-AC68, SPEC-0086)"
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
file: Area_comun/tasks/TASK-0161-codex-intake-resubmit-extractor-robust.md
---

# TASK-0161 - Re-submit idempotente + extractor robusto (AC66-AC68)

> Feedback de uso del operador (carga por archivo, re-prueba). maker=Codex / checker=Arquitecto + PASADA DEL
> ANALISTA. OFF-by-default; #4 byte-identica; ASCII-only; behavior-tests por AC. El operador aprobo la pieza robusta.

## Contexto (reportado por el operador)
1. Re-subir el MISMO archivo da: "auto commit push has no staged submit_intent output changes" -> bloquea el flujo.
2. El primer intento dio "extractor failed" (generico) -> resulto ser el timeout de 10s (AbortError tragado). El
   timeout ya se subio a 30s en la runtime config, pero el error generico no lo decia.
3. La latencia del modelo local (carga en frio ~10s + generacion ~10s = ~21s) hace fragil cualquier timeout fijo bajo.

## Diagnostico del Arquitecto (head-start)
- AC66 (BLOQUEANTE): `commitAndPushSubmitIntentOutputs` (src/server.js ~1964) hace `git add` + `git diff --cached
  --quiet`; si limpio (re-submit idempotente, la TASK-EXTRACT ya existe) lanza 409. Debe ser NO-OP exitoso que
  devuelve el taskId existente para que el front proceda a /intake-extractions/run.
- AC67: catch generico `reason: "extractor failed"` (src/server.js ~1615) traga la causa; `callLocalVlm` (~1681)
  usa AbortController -> al exceder timeoutMs el fetch lanza AbortError (no-ClientError) -> "extractor failed". Hay
  que distinguir timeout vs HTTP !ok vs parseo vs firma.
- AC68: `sanitizeLocalVlmConfig` (~1150) recorta timeoutMs a Math.min(30000,...); el modelo local necesita mas
  margen. Precargar el modelo (keep_alive en la peticion de callLocalVlm y/o warm-up al boot) + subir/quitar el tope.

## Alcance (AC66-AC68)
- **AC66** auto-push: diff limpio (sin cambios staged) = NO-OP exitoso (no 409), devuelve el taskId de la
  TASK-EXTRACT existente; re-subir un archivo ya ingerido re-ejecuta la extraccion (el front procede a la corrida).
- **AC67** el `reason` del estado fallido y el mensaje rojo del front distinguen la causa: timeout (con los ms),
  error HTTP del endpoint, JSON no parseable, firma/clave -- no mas "extractor failed" generico.
- **AC68** precarga del modelo (keep_alive en la peticion local-vlm y/o warm-up al arrancar el server) + timeout
  configurable GENEROSO (subir/quitar el clamp de 30s; permitir minutos) y/o por-segmento. Off-by-default + loopback
  (AC52) intactos.

## DoD
- AC66-AC68 verdes con behavior-tests deterministas: (66) re-submit mismo archivo -> sin 409, taskId devuelto,
  extraccion procede (git mockeado: diff limpio -> no-op). (67) abort -> reason timeout con ms; HTTP !ok -> reason
  endpoint; basura -> reason parseo. (68) timeout > 30s en config se respeta (clamp ya no recorta); la peticion
  incluye keep_alive.
- Carry AC16/AC17/AC43/AC51-AC65 (no-bypass, gate PII, candidatas no-ledger, loopback, autoria, auto-push, UX).
- node --test / CI verde EN CLON LIMPIO; validate con/sin secretos exit 0; drift 0; neutralidad + encoding 0.
- #4 byte-identica (protocol.config.json sin tocar). OFF-by-default intacto.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA.
- REPRO: server vivo (runtime override + Ollama) + subir `historias_panel_operar_agentes.md` -> extrae y salen
  tarjetas; re-subir el mismo archivo -> NO da 409 y re-extrae; si el modelo excede el timeout, el error dice "timeout".

## Notas
- AC66: cuida que el no-op NO sea un bypass -- solo significa "el submit_intent ya estaba aplicado (idempotente)";
  el output gobernado ya existe en el canonico; no se crea un segundo escritor (carry AC17).
- AC68: el warm-up al boot no debe bloquear el arranque del server si Ollama no esta (best-effort, log).
- NUNCA pilotar contra el log vivo: PROTOCOL_REPO_PATH a un clon desechable para el repro del write gobernado.
