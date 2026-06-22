---
task_id: TASK-0155
title: "Proyecto-front: provider local-vlm del Extractor (troceado per-pagina/chunk + egress localhost allowlisted + salida robusta), off-by-default (AC51/AC52/AC53, SPEC-0086, DECISION-0058)"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0056, DECISION-0058]
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0155-codex-extractor-local-vlm-provider.md
---

# TASK-0155 - Provider local-vlm del Extractor (AC51/AC52/AC53)

> GO del operador (Path 1, DECISION-0058). Implementa el extractor live contra un VLM LOCAL, OFF-by-default.
> NO enciendas el uso vivo (eso es GO aparte + ceremonia). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA
> (toca egress -> DECISION-0056). El thinking del modelo se acepta (Path 1); el troceo absorbe su costo.

## Alcance
1. **AC51 - Troceado:** agrega un provider `local-vlm` al loop extractor (junto al `deterministic-local` ya
   existente): procesa **per-pagina** (PDF -> imagen por pagina) y **per-chunk** (texto grande partido), UNA
   llamada por pagina/chunk, payload/`num_ctx` por llamada ACOTADO (independiente del tamano del documento).
   Acumula + deduplica candidatas en el store no-ledger. Cubre pdf/imagen (via vision) y md/html/txt (via texto).
2. **AC52 - Egress = SOLO endpoint local allowlisted:** el provider llama al endpoint del modelo local configurado
   (default `http://127.0.0.1:11434/api/chat`); el guard de egress (AC46) **allowlistea unicamente ese
   host:puerto loopback** y marca CUALQUIER otro host (incluido no-loopback). Config valida solo endpoints
   loopback. Control positivo: host no-loopback -> FLAGGED; endpoint loopback configurado -> permitido.
3. **AC53 - Salida robusta + carry:** parsea SOLO el JSON de candidatas de la respuesta (tolerante a campos de
   razonamiento/texto extra; descarta no-validas; sin crash ante respuesta basura). Candidatas -> store no-ledger;
   carry del gate humano de PII (AC43) + aprobacion antes del intake. NO escribe ledger, NO toca codigo/estado.

## DoD
- AC51/AC52/AC53 verdes con behavior-tests deterministas. **OFF-by-default** (`local-vlm` solo con flag +
  consentimiento; el default sigue siendo `deterministic-local`). Carry AC40-AC50 + el guard endurecido.
- node --test/CI verde EN CLON LIMPIO (los tests NO requieren Ollama: usan provider mock/deterministic + el test
  del guard; la integracion real contra Ollama queda como SMOKE documentado, no en CI del clon). #4 byte-identica
  (core/config/genesis/registry/keys sin tocar); validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar (egress/PII).
- **NO enciende el uso vivo** del Extractor contra archivos reales (GO aparte del operador + ceremonia de alta).

## Notas
- El alta del agente `Extractor` en el registry + su keypair = ceremonia re-genesis-boundary aparte (DECISION-0058);
  esta tarea es SOLO el codigo del provider, off-by-default, sin identidad de agente todavia.
- Render PDF->imagen: usa una via local sin egress (lib JS o herramienta local); documenta la dependencia.
