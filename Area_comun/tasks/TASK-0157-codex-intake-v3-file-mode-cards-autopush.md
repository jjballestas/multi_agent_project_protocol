---
task_id: TASK-0157
title: "Proyecto-front (RF-14): Intake v3 -- modo carga-por-archivo en seccion dedicada (sin scroll, sin campos previos) + boton Extraer requisito -> candidatas como tarjetas -> click puebla campos; auto-commit-push ergonomico (override runtime) (AC55-AC58, SPEC-0086)"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0058]
created_at: 2026-06-23
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
spawned_from: TASK-EXTRACT-DC0E283672
file: Area_comun/tasks/TASK-0157-codex-intake-v3-file-mode-cards-autopush.md
---

# TASK-0157 - Intake v3: flujo carga-por-archivo + tarjetas candidatas + auto-push ergonomico

> GO del operador (feedback de uso real, capturado via Intake gobernado en TASK-EXTRACT-DC0E283672).
> maker=Codex / checker=Arquitecto (clon limpio) + PASADA DEL ANALISTA. OFF-by-default; #4 byte-identica
> (no toca el core ni protocol.config.json). ASCII-only. Behavior-tests deterministas por cada AC.

## Contexto (problema reportado)

1. En el Intake actual, la opcion de "cargar archivo" queda abajo y hay que hacer **scroll** para llegar.
2. La carga por archivo deberia **abrir una seccion nueva** con el selector + un boton **"Extraer requisito"**.
3. Ese boton manda el archivo al **agente Extractor** (ruta gobernada ya existente) y genera requisitos
   **candidatos** pendientes de aprobacion/envio humano.
4. Los candidatos se muestran como **tarjetas**; al hacer **click** en una tarjeta se **pueblan** las
   secciones [Titulo, Narrativa, Intencion de aceptacion] con sus valores.
5. Esos campos **NO** se deben pedir **antes** de cargar el archivo (vienen en el archivo o los pone el LLM).
6. Al colocar un requisito **no queda gateado**: el operador tuvo que hacer `push` manual para que el
   Arquitecto lo viera. Debe ser **automatico** al presionar "Execute submit_intent".

## Alcance (AC55-AC58)

- **AC55** - Modo "carga por archivo" abre seccion dedicada; selector + boton "Extraer requisito" como primer
  elemento visible (sin scroll). NO pedir Titulo/Narrativa/Intencion antes de la carga.
- **AC56** - "Extraer requisito" -> ruta gobernada del Extractor (off-by-default, loopback, carry AC51-AC54) ->
  candidatas renderizadas como **tarjetas** (una por candidata).
- **AC57** - Click en tarjeta -> puebla [Titulo, Narrativa, Intencion de aceptacion]; pendiente de aprobacion
  humana + submit_intent (no entra al ledger antes).
- **AC58** - Resolucion de config prefiere el override runtime gitignored (`*.runtime.json`) cuando existe (cae al
  versionado off-by-default si no). Override activo -> "Execute submit_intent" hace commit+push del output
  gobernado a origin (visible al checker sin push manual). Config versionado sigue `enabled:false`. El push solo
  propaga el output de submit_intent (carry AC17 no-bypass; no es segundo escritor).

## DoD

- AC55-AC58 verdes con behavior-tests deterministas (DOM/render para AC55-57; git mockeado para AC58). Carry
  AC16/AC17/AC43/AC51-AC54 (no-bypass, gate PII humano, candidatas no-ledger, loopback, autoria del Extractor).
- `node --test` / CI verde EN CLON LIMPIO; `validate` con/sin secretos exit 0; drift 0; neutralidad + encoding 0.
- #4 byte-identica (protocol.config.json pinned 1.14.0 sin tocar). OFF-by-default: sin override runtime, el
  comportamiento vivo queda apagado.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
- **NO enciende nada vivo** por su cuenta: la activacion la hace el operador colocando/teniendo el override
  runtime; este task solo cablea que el override SE LEA y que la UX/flujo funcionen.

## Notas

- Insumo de diseno: `Zeus-protocol/design/interface/components/intake/` (lista, wizard-1-capturar,
  wizard-2-preview, cards). Respeta tokens del design-system.
- Reutiliza lo ya construido: rutas `/api/protocol/intake-extractions/run`,
  `/api/protocol/intake-candidates`, `buildFileRequirementPayload`, `buildCandidateApprovalPayload`,
  `commitAndPushSubmitIntentOutputs`, `commit-push.runtime.json` (ya `enabled:true`).
- El cambio de AC58 es de **resolucion de path de config** (preferir `.runtime.json` si existe) + behavior-test;
  no cambiar el default versionado. Mantener el host loopback estricto (`isLoopbackHost`) intacto.
