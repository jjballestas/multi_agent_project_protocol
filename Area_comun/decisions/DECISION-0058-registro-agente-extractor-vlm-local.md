---
decision_id: DECISION-0058
title: "Registro del agente Extractor (VLM local) para la extraccion documental de la carga por archivo v2"
status: accepted
date: 2026-06-22
deciders: [operador humano, Arquitecto]
supersedes: []
related: [DECISION-0040, DECISION-0044, DECISION-0049, DECISION-0050, DECISION-0056, DECISION-0057]
---

# DECISION-0058 - Registro del agente Extractor (VLM local)

## Contexto

DECISION-0056 (carga por archivo v2) define un "agente extractor" que lee el archivo del upload-store y propone
candidatas de requisitos al store NO-ledger; la Fase C (TASK-0152) entrego un provider `deterministic-local`
(cero egress) para CI. Para el USO VIVO, el operador decidio un **LLM LOCAL** (no de frontera): asi el contenido
del archivo -- con posible PII de terceros -- **nunca sale de la maquina**. Se valido empiricamente
**Qwen3-VL-4b via Ollama en localhost** (extraccion estructurada de historias+criterios de calidad; ~83 tok/s en
la RTX 5060 8 GB). Limitacion observada: el modo "thinking" de Qwen3-VL no se desactiva en Ollama 0.30.9
(`think:false` / `/nothink` ignorados); se acepta como costo (el razonamiento va en campo aparte; el contenido
sale limpio) y se mitiga con el diseno troceado de abajo. Su eliminacion es una optimizacion futura (investigacion
en curso), NO un bloqueo.

## Decision

Se registra en la metodologia un nuevo agente **`Extractor`** (rol: extraccion documental), con estas
propiedades vinculantes:

1. **Backend = VLM LOCAL.** Qwen3-VL-4b servido por Ollama en `http://localhost:11434`. **Cero egress externo**:
   el contenido del archivo no sale de la maquina.
2. **Diseno TROCEADO (robusto al tamano).** Procesa **per-pagina** (PDF -> imagen por pagina) y **per-chunk**
   (texto grande partido), **una llamada al modelo por pagina/chunk** -> el `num_ctx` por llamada es **acotado y
   fijo**, NO depende del tamano del documento. Las candidatas de todas las paginas/chunks se **acumulan y
   deduplican** en el store no-ledger. Un documento mas grande escala el NUMERO de llamadas, no el contexto por
   llamada (nunca desborda).
3. **Frontera de egress = SOLO el endpoint Ollama localhost**, allowlisted en el guard de egress (AC46 deny-all);
   cualquier otra salida de red la marca el guard. Sin internet.
4. **tool_policy MINIMO:** lee el upload-store + escribe candidatas al store no-ledger. **NADA de ledger, codigo,
   ni estado.** No corre `submit_intent` (no es escritor del ledger).
5. **Candidatas -> store NO-ledger.** El **GATE HUMANO DURO de PII (AC43)** + la aprobacion humana antes del
   intake se mantienen sin cambio. PII de terceros **nunca** al log atestado (DECISION-0040).
6. **Autoria honesta.** El Extractor **firma sus candidatas con su propio keypair** -> atribuible en el dataset #4
   (se ve que las propuso el Extractor, no un humano ni otro agente). maker != checker intacto: el Extractor
   PROPONE; el humano aprueba; Arquitecto/Analista no se contaminan.
7. **OFF-by-default.** El uso vivo (encender el Extractor contra archivos reales) = **GO aparte del operador**,
   con **pasada del Analista** al cierre (es la ventana de modelo real).
8. **Alta del agente = CEREMONIA de re-genesis-boundary gobernada** (DECISION-0057 es gestion de runtime, NO de
   identidad): el alta en `agent_registry` (pinned/atestado bajo #4) + la provision del keypair del Extractor se
   hacen en una ceremonia con el **operador presente**, en copia limpia, con rollback ensayado. La registracion
   en el registry NO ocurre fuera de esa ceremonia.

## Consecuencias / boundaries

- **Neutralidad:** el Extractor, su provider y su perfil de extraccion viven en la capa de producto/instancia
  (mirror DECISION-0049/0050), NO en el core neutral. El core no aprende del dominio.
- **Versionado:** la capacidad se documenta en CHANGELOG; el alta del agente toca `agent_registry`, por eso es un
  **re-genesis-boundary** (cambio de epoca coordinado, DECISION-0047), no un toggle.
- **Sin fine-tuning** de inicio (decision del operador): prompt estructurado + few-shot + gate humano; el
  fine-tuning (QLoRA-4b) queda como optimizacion posterior si la calidad lo exige.

## Pendiente (gateado, NO en esta decision)

- SPEC con los AC del Extractor (troceado, contexto acotado por llamada, tool_policy minimo, egress=localhost
  allowlisted, candidatas no-ledger, manejo de los 5 formatos, acumula+dedup).
- Tarea de implementacion (maker=Codex / checker=Arquitecto + Analista), off-by-default.
- La ceremonia de re-genesis-boundary (alta en registry + keypair).

## Addendum 2026-06-22 - Modelo resuelto: Qwen3-VL-4B-Instruct (no-thinking)

La investigacion del operador confirmo que el thinking del tag `qwen3-vl:4b` (variante Thinking) NO se desactiva
de forma fiable en Ollama. **Resolucion: el Extractor usa `qwen3-vl:4b-instruct`** (variante Instruct, NO-thinking,
tag DIRECTO en la libreria de Ollama; sin import manual de GGUF+mmproj). Validado empiricamente: thinking len = 0,
`content` = JSON limpio, `done="stop"` (sin sobre-generar), `format: json` funciona. El provider (TASK-0155) es
agnostico al modelo -> este cambio es de CONFIG (que tag apunta el Extractor), no de codigo; no rehace TASK-0155.
