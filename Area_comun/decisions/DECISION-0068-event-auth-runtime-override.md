---
decision_id: DECISION-0068
title: event_auth.keys (HMAC por actor) legibles desde un RUNTIME OVERRIDE fuera del config pinned (anadir un firmante sin re-genesis) -- espejo de DECISION-0067 para la capa A1
status: accepted
ratified_at: 2026-06-27
date: 2026-06-27
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0067, DECISION-0047, DECISION-0045, DECISION-0022, DECISION-0066]
phase: P2
---

# DECISION-0068 - event_auth keys en runtime override (espejo de DECISION-0067)

> ACCEPTED (operador GO "camino B" 2026-06-27). **Mismo patron que DECISION-0067**, ahora para la capa A1
> (event_auth HMAC). El mapeo `event_auth.keys` (actor -> key_id + secret_file) vive HOY en `protocol.config.json`
> (PINNED): Arquitecto/Codex/runtime. Anadir un firmante nuevo (Analista) exigiria editar ese config -> cambia
> `canonical_hash(config)` -> rompe `chain.genesis` ("genesis mismatch"), EXACTAMENTE el muro que DECISION-0067
> resolvio para actor_auth. El override actual (`event-state.runtime.json`) solo admite `actor_auth_*`.

## Contexto

El operador quiere que el **Analista firme el mismo** sus turnos (no relay): 3er firmante cruzado real del dataset
(refuerza H1/H3 del pre-registro; >=2 ya se cumple, pero un 3er firmante fortalece la evidencia). El Ed25519 (A2)
del Analista ya esta provisto (private_key_files + analista-ed25519-private.pem + keyid analista:v1). Falta la capa
**event_auth HMAC (A1)**: no hay `event_auth.keys.Analista` y `agent_registry.agents[].auth.secret_file` es null,
asi que `signing_secret(config, "Analista")` devuelve None -> "event auth signing key missing for actor: Analista".
La clave `secrets/eventauth-analista.key` ya existe (generada), pero NADA la mapea.

## Decision

1. **`event_auth.keys` (y campos `event_auth` por actor) se MERGEAN desde el runtime override gitignored** (espejo
   exacto de DECISION-0067 para actor_auth). Se extiende el conjunto de claves permitidas del override
   (`event-state.runtime.json`) para incluir `event_auth` (al menos `keys`), y el lector `agent_auth_config` /
   `signing_secret` mergea override sobre config (override gana) **sin** leer ese mapeo del config pinned cuando el
   override lo provee.
2. **`protocol.config.json` NO se edita.** Anadir/quitar un firmante (Analista) se hace en el override -> NO cambia
   `canonical_hash(config)` -> `chain.genesis` INTACTO, sin re-genesis, cadena CONTINUA. Rollback = quitar la
   entrada del override.
3. **El algoritmo de firma/verificacion NO cambia** (HMAC-SHA256 sobre el evento canonico; DECISION-0066 intacta).
   Solo cambia DE DONDE se lee el mapeo actor->secret_file de event_auth. Mismo principio que DECISION-0067.
4. **Off-by-default / sin secretos al repo.** El override es gitignored; las claves HMAC viven en `secrets/`
   (gitignored). Sin la entrada en el override, el actor no firma (comportamiento actual byte-identico).
5. **Re-baseline:** como esto toca el core (`eventlog.py`), tras implementarlo se RE-ATESTA el measurement baseline
   (DECISION-0066) con los hashes nuevos. Legitimo: cero resultados mirados (pre-medicion). El baseline previo
   (commit 8943756) se supersede limpio; la cadena no se rompe.
6. **Capability del reviewer (aclaracion, sin cambio de config):** `claim` ya admite `reviewer` (submit_intent
   acepta {implementer, orchestrator, reviewer}); el Analista reclama su review por si mismo. `task_status` (que
   exige implementer/orchestrator) lo lleva el Arquitecto: el Analista entrega claim + artefacto + MSG, el
   Arquitecto mueve el estado de la tarea. NO se tocan capabilities en el registro pinned.
7. **SDD:** SPEC-0106 + TASK-0195, maker=Codex / checker=Arquitecto. AC clave: anadir Analista por override ->
   `submit_intent` del Analista firma event_auth + actor_auth -> `validate` exit 0 (sin "genesis mismatch"), drift
   0, chain intacta; sin override el comportamiento es byte-identico (Analista no firma).

## Alcance / No-alcance

- **En alcance:** mergear `event_auth.keys` desde el override; permitir la clave `event_auth` en el override;
  off-by-default; provisionar Analista por override; re-baseline; tests (incl. AC chain-intacta-tras-anadir-firmante).
- **Fuera de alcance:** cambiar el algoritmo HMAC/verificacion; tocar el config pinned o el agent_registry; cambiar
  capabilities; re-genesis; medir el TFM.

## Consecuencias

- Anadir/quitar un firmante event_auth pasa a ser un cambio de RUNTIME (override), sin romper la cadena -- igual que
  el flip A2 quedo limpio con DECISION-0067. El Analista puede firmar (A1+A2) y entrar como 3er firmante cruzado.
- El measurement baseline se re-ata una vez (pre-resultados); cadena continua, dataset sin discontinuidad.

## Alternativas consideradas

- **Re-genesis (camino A):** editar event_auth.keys en el config pinned + re-anclar cadena nueva. Pesado, rompe
  continuidad, resetea baseline por cadena nueva. Descartado.
- **Relay (Arquitecto firma el veredicto del Analista):** no es auto-firma; el operador pidio que el Analista firme
  el mismo. Descartado para este objetivo.
