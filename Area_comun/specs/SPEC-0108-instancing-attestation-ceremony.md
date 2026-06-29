---
spec_id: SPEC-0108
title: Ceremonia de instanciacion atestada -- keygen por firmante + roster por instancia (firmantes/workers + binding LLM) en new_instance.py
status: ready
owner: Codex
decision: DECISION-0069
relates_to: [DECISION-0069, DECISION-0068, DECISION-0067, DECISION-0050, DECISION-0016, DECISION-0045]
date: 2026-06-29
file: Area_comun/specs/SPEC-0108-instancing-attestation-ceremony.md
---

# SPEC-0108 -- Ceremonia de instanciacion atestada

Implementa la capacidad decidida en DECISION-0069: que instanciar pueda producir una instancia PLENAMENTE
CAPAZ (runtime + atestacion + roster), con keygen por firmante, workers keyless, binding LLM por agente, y
verificacion portable por terceros. **DOMAIN-NEUTRAL.** Off-by-default (enforce no se auto-activa).

## Componentes

1. **Script de keygen por firmante** (p.ej. `scripts/keygen_agent.py`, NUEVO): dado `agent_id` + `keyid`,
   genera keypair Ed25519 (A2) + secreto HMAC (A1). Escribe la PRIVADA PEM y el secreto HMAC en
   `protocol-secrets/` (gitignored) de la instancia; la PUBLICA en formato portable. Idempotente (no
   sobreescribe sin `--force`); NUNCA imprime secretos a stdout; usa `cryptography` (ya requerido por eventlog).

2. **Tier/paso `attested` en `new_instance.py`** (extension, scaffolding NO pineado): acepta un ROSTER
   parametrizable; por agente `{id, role, tier: signer|worker, llm_preset}`:
   - **signer:** invoca keygen -> referencia la privada en el override `actor_auth_config.private_key_files` +
     `event_auth.keys`; escribe la PUBLICA en `signatures.public_keys` del `protocol.config.json` de la INSTANCIA
     (commiteable, portable).
   - **worker:** registra KEYLESS en `agent_registry`/`agent_roles` (sin keypair).
   - todos: crea `personal/<id>/` (DECISION-0016) y fija su `llm_preset` (slot neutral por-agente; el modelo
     concreto es config de instancia, el picker lo pondra Hermes en el panel).
   - copia `runtime/`+`scripts/` (tier runtime), corre genesis (`regenesis.py`) para anclar la cadena de la
     instancia; deja `event_state.enforce`/`actor_auth_enforce` OFF (enable explicito posterior, DECISION-0045).

3. **Provenance (convencion):** documentar el campo de metadata del evento (`author_agent` real + `model`) que un
   firmante incluye al atestar trabajo de un worker. Se ejercita en instancias NUEVAS via payload de
   `submit_intent` (que ya admite metadata); NO se modifica el `eventlog.py` del hub.

## Criterios de aceptacion

- **AC1 (keygen):** produce PRIVADA Ed25519 PEM (ruta gitignored) + PUBLICA portable + secreto HMAC; idempotente;
  no imprime secretos; rechaza sobreescritura sin `--force`.
- **AC2 (ceremonia):** `new_instance.py --tier attested` con un roster {signer Arquitecto, signer Codex, signer
  Analista, worker <peon>} produce: 3 firmantes con claves + override + `signatures.public_keys`; worker KEYLESS en
  el registry; `personal/<id>/` para los 4; genesis anclado; **validate exit 0 en la instancia nueva**.
- **AC3 (verificacion portable por tercero):** un CLON de la instancia nueva SIN `protocol-secrets/` corre
  `validate_collaboration_state.py` y **verifica el ledger via las publicas commiteadas** -> exit 0, actor_auth
  verificado (no requiere secretos para verificar).
- **AC4 (frontera):** un worker KEYLESS NO puede escribir el ledger bajo `enforce` (`submit_intent` lo rechaza por
  clave ausente) -- prueba negativa.
- **AC5 (GUARDRAIL TFM -- DURO):** correr keygen + la ceremonia hace **CERO cambios** en los archivos PINEADOS del
  HUB (`runtime/eventlog.py`, `scripts/validate_collaboration_state.py`, `protocol.config.json`, override
  `event-state.runtime.json`, pre-registro v2.0): permanecen byte-identicos (mismo sha256). Un check lo asegura.
  La ceremonia opera SOLO sobre instancias nuevas + scripts nuevos.
- **AC6:** `scan_domain_neutrality.py` limpio; golden tests del keygen y de la ceremonia (sobre instancia
  desechable en ruta corta por MAX_PATH Windows); off-by-default (enforce no auto-activado).

## DoD

AC1-AC6 verdes en clon limpio (ruta corta). Handoff `in_review` con: comandos exactos, sha256 de los pineados del
hub ANTES/DESPUES (identicos), y la prueba de verificacion por tercero (clon sin secretos). maker=Codex/
checker=Arquitecto. Tras cerrar: **fase de aplicabilidad con Zeus-Aegis** (verificar que las opciones se pueden
aplicar end-to-end; la accion "instanciar proyecto" del panel = trabajo de producto, SDD aparte).
