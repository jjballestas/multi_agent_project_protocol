---
decision_id: DECISION-0067
title: Correccion a DECISION-0065 - el flag actor_auth_enforce (+ actor_auth_config) vive en un RUNTIME OVERRIDE fuera del config pinned (no rompe chain.genesis)
status: accepted
ratified_at: 2026-06-27
date: 2026-06-27
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0065, DECISION-0047, DECISION-0045, DECISION-0022]
phase: P2
---

# DECISION-0067 - actor_auth_enforce en runtime override (corrige DECISION-0065)

> ACCEPTED (operador GO 2026-06-27). **Corrige un error de diseno de DECISION-0065/SPEC-0103/TASK-0190**: el flag
> `actor_auth_enforce` quedo dentro de `protocol.config.json`. El ENSAYO del flip (en copia desechable,
> DECISION-0045) demostro que encenderlo alli **rompe la cadena #4** ("genesis mismatch"), porque
> `chain.genesis` (seq 0) se ancla a `canonical_hash(protocol.config.json)` y NO hay tool que re-ancle la cadena
> sin arrancar una nueva. Contradice DECISION-0047 (lo flippeable va FUERA del config pinned).

## Contexto

DECISION-0065/TASK-0190 entregaron el mecanismo A2 (`submit_intent` firma `actor_auth` Ed25519) con el flag en
`event_state.actor_auth_enforce` dentro de `protocol.config.json`. El mecanismo firma+verifica bien (ensayo:
`actor_auth:{keyid:arquitecto:v1,method:ed25519}`), PERO el flip exige editar el config -> cambia
`canonical_hash(config)` -> el `chain.genesis` existente deja de casar -> `validate` falla "genesis mismatch".
`regenesis.py` solo re-ancla el genesis de ESTADO (drift), no la cadena. Re-anclar la cadena = arrancar una
cadena nueva (boundary T0 bespoke), inaceptable para un simple flip.

## Decision

1. **`actor_auth_enforce` + `actor_auth_config` se LEEN de un runtime override gitignored FUERA de
   `protocol.config.json`** (p.ej. `event-state.runtime.json` o `actor-auth.runtime.json`), espejo de
   `file-ingestion.runtime.json` / `connectors.config.json` (DECISION-0047). Los lectores
   `actor_auth_enforce_enabled()` / `actor_auth_config()` mergean el override (override gana) **sin** leer el flag
   del config pinned.
2. **`protocol.config.json` NO contiene el flag** (queda OFF/ausente). Asi encender/apagar A2 **no cambia el
   `canonical_hash(config)` -> `chain.genesis` INTACTO -> sin re-genesis, cadena CONTINUA**. El path de firma
   (TASK-0190) no cambia; solo cambia DE DONDE se lee el enable + la config de llaves.
3. **El flip pasa a ser un cambio de RUNTIME** (poner el override `enabled:true` + `actor_auth_config`): sin tocar
   el config, sin re-genesis, cadena continua, el dataset abarca el flip sin discontinuidad. Rollback = quitar/false
   el override.
4. **Off-by-default; sin secretos al repo.** Override ausente -> `not_enforced_phase2` (byte-identico al actual).
   El override es gitignored; las privadas siguen en `protocol-secrets`.
5. **Template:** documentar el override (no el flag en config). Quitar el flag del `protocol.config.template.json`
   donde TASK-0190 lo metio (o marcarlo como override-only).
6. **SDD:** SPEC-0105 + TASK-0192, maker=Codex / checker=Arquitecto. AC clave: encender via override + un
   `submit_intent` real -> `validate` exit 0 (NO "genesis mismatch"), drift 0, chain intacta -- justo lo que el
   ensayo demostro roto con el flag-en-config.

## Alcance / No-alcance

- **En alcance:** mover el enable+config de A2 al runtime override; lectura mergeada; off-by-default; quitar el flag
  del config/template; tests (incl. el AC de chain-intacta-tras-flip).
- **Fuera de alcance:** cambiar el path de firma/verificacion (TASK-0190 esta bien); la ACTIVACION viva (flip) que
  sigue siendo ventana del operador; generar/medir el dataset.

## Consecuencias

- El flip A2 deja de ser un re-genesis-boundary que rompe la cadena y pasa a ser un flip de runtime limpio
  (cadena continua, dataset sin discontinuidad). El runbook del flip se simplifica (sin regenesis de cadena).
- El ensayo (DECISION-0045) probo su valor: caza el fallo antes del vivo.

## Alternativas consideradas

- **Aceptar el flip como cadena nueva (boundary T0):** mas pesado, sin tooling listo, descarta continuidad de
  cadena. Descartado.
- **Dejar el flag en config + bespoke re-chain:** fragil y contradice DECISION-0047. Descartado.
