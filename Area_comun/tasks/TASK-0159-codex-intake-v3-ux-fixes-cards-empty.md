---
task_id: TASK-0159
title: "Proyecto-front (RF-14): Intake v3 fixes de UX + fix '0 candidatas' -- Execute oculto en modo archivo, selector de proyecto primero, indicador de procesamiento, errores en rojo, tarjetas visibles tras extraer (AC59-AC63, SPEC-0086)"
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
file: Area_comun/tasks/TASK-0159-codex-intake-v3-ux-fixes-cards-empty.md
---

# TASK-0159 - Intake v3: fixes de UX + fix "0 candidatas" (AC59-AC63)

> Feedback de uso real del operador sobre la carga por archivo (TASK-0157). maker=Codex / checker=Arquitecto +
> PASADA DEL ANALISTA. OFF-by-default; #4 byte-identica; ASCII-only; behavior-tests por AC.

## Contexto (reportado por el operador)
1. En modo carga-por-archivo, el boton "Execute submit_intent" debe estar OCULTO -- ese boton es para enviar UN
   requisito individual; en el flujo por archivo se habilita al hacer click en una tarjeta y APROBAR el requisito,
   o cuando se indique que es individual.
2. El selector de "Proyecto destino" debe ser el PRIMER div, incluso antes del selector de archivos.
3. Al presionar "Extraer requisito" el agente tarda -> indicar "procesando" para que el operador no crea que no
   pasa nada.
4. Errores (p.ej. la nota de ingestion / extraccion fallida) deben salir en LETRAS ROJAS.
5. Al extraer de `historias_panel_operar_agentes.md` salio "Ingestion acotada: .md/.txt hasta 65536 bytes /
   Candidatas: Sin candidatas pendientes" y NO se ven las tarjetas. El operador duda si la actualizacion no se
   publico o que.

## Diagnostico del Arquitecto (head-start)
- El codigo de tarjetas (`renderCandidateReviewCard`) + el refresh tras extraer (`submitFileExtraction` ->
  `refreshController.refreshView("intake", ...)`) YA estan en el HEAD local (2afc944). La feature existe.
- La nota "Ingestion acotada: .md/.txt" (public/app.js ~1202) HARDCODEA ".md/.txt" -> NO refleja las extensiones
  reales del config; engana sobre que config esta cargado.
- "Sin candidatas pendientes" = la extraccion devolvio 0 candidatas ALMACENADAS (store
  `tmpdir/zeus-protocol-file-candidates`), no que las tarjetas no se rendericen. Causas a verificar: (a) el server
  vivo corre con el config VERSIONADO (extractor OFF) en vez del runtime override -> 0 candidatas; (b) el proceso
  no se reinicio con el codigo nuevo; (c) la extraccion local-vlm no parsea/almacena candidatas de un .md
  multi-seccion (troceado/parse/maxCandidates).

## Alcance (AC59-AC63)
- **AC59** Execute oculto en modo archivo; se habilita al aprobar una tarjeta o en modo individual/typed.
- **AC60** Selector de "Proyecto destino" como PRIMER elemento de la carga por archivo (antes del file input).
- **AC61** Indicador de "procesando" + boton deshabilitado mientras corre "Extraer requisito".
- **AC62** Errores en ROJO/estado visible; la nota de ingestion lista las extensiones REALES del config (no hardcode).
- **AC63** Tras extraer, las candidatas aparecen como TARJETAS visibles (refresh real); DIAGNOSTICA y CORRIGE el
  "0 candidatas" sobre un .md valido multi-seccion: el server vivo HONRA el runtime override (extractor enabled,
  local-vlm, loopback); la extraccion parsea+almacena candidatas (carry AC51/AC52/AC53/AC43); si 0 candidatas con
  causa real -> ERROR visible (AC62), no panel mudo. REPRO: con server vivo (runtime override + Ollama) subir
  `historias_panel_operar_agentes.md` -> aparecen N tarjetas.

## DoD
- AC59-AC63 verdes con behavior-tests deterministas (DOM/render; extraccion mockeada donde aplique). Carry
  AC16/AC17/AC43/AC51-AC58 (no-bypass, gate PII humano, candidatas no-ledger, loopback, autoria Extractor, auto-push).
- REPRO documentado del fix de 0-candidatas con el archivo real (smoke vivo: subir el .md multi-historia -> tarjetas).
- node --test / CI verde EN CLON LIMPIO; validate con/sin secretos exit 0; drift 0; neutralidad + encoding 0.
- #4 byte-identica (protocol.config.json sin tocar). OFF-by-default intacto (el extractor vivo solo por runtime override).
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.

## Notas
- Insumo de diseno: `Zeus-protocol/design/interface/components/intake/`. Respeta tokens del design-system.
- El operador puede estar corriendo un server STALE; el fix debe asegurar que con el codigo actual + runtime override
  + Ollama, el flujo produce tarjetas. Si encuentras que solo era falta de reinicio, igual implementa AC59-AC62 (UX)
  y deja AC63 con el repro que demuestra que con el codigo correcto SI salen tarjetas.
- NUNCA pilotar contra el log vivo: si el repro necesita el write gobernado, usa una copia desechable del protocolo
  (PROTOCOL_REPO_PATH a un clon) para no ensuciar el canonico (DECISION-0045).
