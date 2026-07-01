---
decision_id: DECISION-0074
title: "REQ-ZEUS D3 - Backend de modelos hibrido: frontera multi-proveedor (firmantes) + peones locales keyless fuera del ledger; cero-egress de PII; piloto de peones en sandbox aparte"
status: accepted
ratified_at: 2026-06-30
date: 2026-06-30
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0050, DECISION-0072]
scope: product
phase: P2
---

# DECISION-0074 (REQ-ZEUS D3) - Backend de modelos hibrido + guia de peones

> ACCEPTED (operador endoso OPS-115242Z + registro en hub, 2026-06-30). Canonicaliza la D3 de NOVA
> (`.../NOVA/Area_comun/decisions/DECISION-0003-D3-backend-modelos-hibrido.md`) e incorpora la guia de modelos-peon
> (`TEMP_Guia_Modelos_Peones_y_Medicion.md`) como requisito del operador para WS4.

## Decision
Backend **hibrido**:
- **Frontera (firmantes/"jefes"):** router OpenAI-compatible multi-proveedor (tipo LiteLLM) que expone los modelos
  frontera del operador: **Codex, Claude Code, GLM 5.2, Gemini 3.1 Pro**. Punto unico de claves, costo y politica PII.
- **Peones (drafters baratos):** **Ollama local** con Qwen2.5-Coder-7B-Instruct (Q4 ~4.7GB) y DeepSeek-Coder-6.7B
  (contraste); `qwen2.5-coder:3b` para CRUD trivial. Opcional Gemini Flash-Lite como critico asesor (Brazo C), NO firmante.

## Frontera de firma (no negociable en modo atestado)
Solo los firmantes frontera tienen clave Ed25519 y firman; los **peones son drafters keyless FUERA del ledger y NUNCA
firman** ("delego pero respondo"). Un prompt de peon filtrado no puede forjar una firma (no tiene clave).

## Guia de peones (requisito del operador, aplica a WS4)
- **Codegen antes que LLM:** si la salida es funcion mecanica de la entrada (CRUD, DTOs, mappers, cliente OpenAPI) ->
  scaffolding/plantillas/Roslyn, cero tokens. El peon solo para la variacion con criterio; decide el firmante.
- **Patron:** peon = maker barato (borradores fuera del ledger, nunca `submit_intent`); firmante distinto (Codex)
  integra, prueba y FIRMA. maker!=checker. El peon nunca toca reglas de negocio ni el repo del protocolo.
- **Gate determinista:** build + test (unit+golden) + arch-tests + lint/format + scan encoding + guard "sin logica de
  negocio / sin deps nuevas". Verde -> el firmante ojea el diff y firma.
- **Medicion 3 brazos** (A control / B peon->gate->firmante / C peon->gate->critico->firmante) sobre 10-20 tareas
  homogeneas reales-sin-PII; **metrica que decide = tokens del firmante**. Reglas pre-comprometidas de adopcion.

## Reglas
- Claves NUNCA en el repo (config local / vault). **PII / datos reales NUNCA salen a modelos externos** (cero-egress).
- El instalador apunta al router de empresa por defecto; Ollama local solo donde haya GPU.

## Consecuencias
- El piloto de peones (experimento A/B/C) corre en **repo SANDBOX aparte `D:/Agentes/Zeus/piloto-peones/`**, cero
  escritura al repo medido. El dataset ya esta sellado en N=500, asi que la "regla de oro" (peones post-N=500) se cumple.
