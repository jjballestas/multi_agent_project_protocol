---
task_id: TASK-0213
title: "Ceremonia de instanciacion atestada: keygen por firmante + roster (firmantes/workers + binding LLM) en new_instance.py (DECISION-0069, SPEC-0108)"
type: protocol
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
maker: Codex
checker: Arquitecto
linked_decisions: [DECISION-0069]
spec: SPEC-0108
file: Area_comun/tasks/TASK-0213-codex-instancing-attestation-ceremony.md
---

# TASK-0213 -- Ceremonia de instanciacion atestada (DECISION-0069 / SPEC-0108)

## Objetivo
Que instanciar pueda producir una instancia plenamente capaz (runtime + atestacion + roster), con keygen por
firmante, workers keyless, binding LLM por agente, y verificacion portable por terceros. DOMAIN-NEUTRAL,
off-by-default. Spec autocontenido en `Area_comun/specs/SPEC-0108-instancing-attestation-ceremony.md`;
rationale en `Area_comun/decisions/DECISION-0069-instancing-attestation-ceremony.md`.

## Alcance (SOLO archivos NUEVOS + new_instance.py; NO tocar pineados del hub)
1. `scripts/keygen_agent.py` (NUEVO): keygen Ed25519 + HMAC por firmante (privadas->protocol-secrets gitignored,
   publica portable); idempotente; sin imprimir secretos.
2. `new_instance.py`: tier/paso `attested` + roster `{id, role, tier: signer|worker, llm_preset}`. Signers ->
   claves+override+`signatures.public_keys`. Workers -> keyless en registry. Todos -> `personal/<id>/` + llm_preset.
   Copia runtime/scripts, corre genesis, deja enforce OFF (enable explicito posterior).
3. Documentar la convencion de provenance (`author_agent`+`model` en metadata del evento) -- via payload de
   submit_intent en instancias nuevas; NO modificar eventlog.py del hub.
4. Golden tests del keygen y de la ceremonia (instancia desechable en RUTA CORTA, MAX_PATH Windows).

## Criterios de aceptacion
AC1-AC6 de SPEC-0108. Los CRITICOS:
- **AC3:** clon de la instancia nueva SIN secretos verifica el ledger via publicas commiteadas (validate exit 0).
- **AC4:** worker keyless NO puede escribir el ledger bajo enforce (prueba negativa).
- **AC5 (GUARDRAIL TFM, DURO):** keygen + ceremonia hacen CERO cambios en los pineados del hub (eventlog.py,
  validador, protocol.config.json, override, pre-registro): mismo sha256 antes/despues. Incluye el check.

## DoD
AC1-AC6 verdes en clon limpio (ruta corta C:/t/...). Handoff `in_review` con comandos exactos + sha256 de pineados
del hub ANTES/DESPUES (identicos) + prueba de verificacion por tercero. Commit como Arquitecto + Co-Authored-By
Codex. Checker=Arquitecto (clon limpio + verifico el guardrail). Si algun subcaso exigiera tocar un pineado del
hub -> `blocked` + pregunta (se APARCA hasta cerrar la ventana de 500, DECISION-0069 #6).
