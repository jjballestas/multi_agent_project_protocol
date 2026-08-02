---
decision_id: DECISION-0109
title: Roster de agentes desde el front, DOS NIVELES -- Nivel 1 (worker de producto no-firmante + enlace a LLM) habilitado por front-form off-by-default; Nivel 2 (agente de gobernanza #4) = ceremonia de re-genesis, NO front-toggle
status: accepted
ratified_at: 2026-08-02
date: 2026-08-02
deciders: [operador humano, Arquitecto]
relates_to: [DECISION-0058, DECISION-0069, DECISION-0107, DECISION-0106, DECISION-0050, REQ-ZEUS-001]
phase: P2
---

# DECISION-0109 - Roster de agentes desde el front (P4 de TASK-0178), DOS NIVELES

> ACCEPTED por el operador (2026-08-02, via META de sesion: completar C + P4; ratificado en sesion directa). Codigo SOLO en Zeus-protocol;
> core neutral. Separa explicitamente lo que SI es un front-form de lo que es ceremonia gobernada.

## Contexto
TASK-0178 P4. "Dar de alta un agente desde el front + enlazarlo a un LLM" tiene DOS niveles con fronteras de
seguridad MUY distintas (leccion del Extractor, DECISION-0058 Opcion 2; agent_registry PINNED bajo #4).

## Decision
### Nivel 1 -- Worker de PRODUCTO no-firmante + enlace a LLM (SI, front-form) -- ESTE es el alcance construible
1. El front puede DAR DE ALTA un WORKER DE PRODUCTO que **NO escribe el ledger** (como el Extractor): se registra
   FUERA del config #4, en un roster de workers (patron `extractors.config.json` / DECISION-0058), con su propio
   keypair, y se ENLAZA a un LLM (provider/endpoint/modelo: otro local-vlm, otro modelo de Ollama, etc.).
2. **Builder SERVER-SIDE, forma estricta (hereda 0051/0052):** el front compone la entrada del roster desde
   campos validados (id del worker, provider, endpoint, modelo, capacidades de PRODUCTO); el cliente no inyecta
   forma cruda. Off-by-default; el registro vive FUERA del config pinned.
3. **Frontera dura (keyless/no-firmante, DECISION-0069):** el worker es keyless -> NO firma ni cierra el ledger;
   su trabajo lo VERIFICA y FIRMA un jefe firmante (guard V2 de TASK-0213). Alta != autoridad de firma. NO toca
   agent_registry/#4/genesis (byte-identico).

### Nivel 2 -- Agente de GOBERNANZA que FIRMA el ledger (NO front-toggle) -- CEREMONIA
4. Dar de alta un agente que FIRMA el ledger cambia `event_state.signature_config.public_keys` + `agent_registry`
   = el config PINNED bajo #4 (epoca 1.14.0), cuyo genesis liga `canonical_hash(config)`. Eso EXIGE una
   **ceremonia de re-genesis-boundary GOBERNADA** con el operador PRESENTE (provisioning de keypair, vaciar el
   event log, re-genesis 1 sola vez con el config final). **NO es un boton del front.** El front puede INICIAR/
   PREPARAR la ceremonia (formulario de datos, checklist), pero el FLIP es la ceremonia, fuera de banda.
5. **FONDO INTOCABLE:** el Nivel 2 toca el config pineado / genesis (2E35F26E, 1.14.0) -> INVIOLABLE sin una
   DECISION nueva + aprobacion humana + re-genesis coordinado. Ningun agente lo ejecuta autonomamente. La
   ceremonia se documenta como RUNBOOK (P4b); su ejecucion es un evento con el operador, no parte de este build.

## Boundaries que esta DECISION NO mueve
- El Nivel 2 NO se automatiza ni se toggle-a desde el front. NO nuevo INTENT_TYPES. El core no cambia.
- Nivel 1: el worker es de PRODUCTO (Zeus), keyless, off-by-default; no gana capacidad de firma ni de riesgo.

## Implementacion
- **P4a (Nivel 1):** via SDD -- SPEC-0115 + tarea (maker Codex, checker Analista+Arquitecto), front-form de alta
  de worker de producto + enlace a LLM, off-by-default, keypair, roster fuera del config pinned. Construible ya.
- **P4b (Nivel 2):** RUNBOOK de la ceremonia de re-genesis-boundary (documento gobernado); ejecucion DIFERIDA a
  un evento con el operador presente (FONDO INTOCABLE). No se construye un toggle.
