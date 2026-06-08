---
id: TASK-0086
owner: Codex
status: ready
type: security
priority: high
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0085]
relates_to: [TASK-0069, SPEC-0066]
phase: P2
spec_id: Area_comun/specs/SPEC-0067-guard-authoritative-requiere-enforce.md
linked_decisions: [DECISION-0022, DECISION-0006]
objective: Cerrar el false-secure detectado al flipear authoritative - que event_state.authoritative=true con enforce=false (o cadena de flags rota) sea RECHAZADO con error claro por la maquinaria existente, no degradado en silencio. Acopla los flags duro.
expected_output: funcion event_state_config_error(config) en runtime/protocol_replay.py (authoritative=>enforce=>materialize=>enabled; enforce/authoritative solo en tier runtime; mensaje accionable) cableada para que MUERDA: validate_collaboration_state.py hard-fail si incoherente; submit_intent.py + apply.py raise antes de aplicar; golden que demuestra authoritative-sin-enforce RECHAZADO (validador falla + submit_intent raise) y cadenas coherentes pasan; paridad .ps1/CI; template intacto.
question_to_resolve: ninguna (alcance fijado por SPEC-0067). Si una transicion submit_intent rechaza, NO editar *.json a mano -> blocked + error + transaccion.
closure_criterion: event_state_config_error implementado + cableado (validador hard-fail + submit_intent/apply raise) + golden (authoritative-sin-enforce rechazado; coherentes pasan) + regresiones verdes + paridad .ps1/CI; config vivo (todos true) sigue pasando el validador; template intacto; todo emitido por submit_intent (enforce+authoritative ON); handoff autocontenido.
sdd_required: true
---

# TASK-0086 - Guard: authoritative=true requiere enforce=true (mata el false-secure)

> READY (encolada por Claude 2026-06-08 VIA submit_intent bajo enforce+authoritative). Ver SPEC-0067.
> Cierra el hallazgo del flip authoritative: hoy authoritative=true con enforce=false se degrada en SILENCIO
> (authoritative_enabled=False) sin rechazar el config -> false-secure. enforce+authoritative ON: TODO por
> submit_intent.

## Contexto

Al flipear authoritative=true verifique que `authoritative` NO tiene callers de comportamiento: la garantia
escritor-unico la provee `enforce`. Riesgo: un config con `authoritative:true` + `enforce:false` parece
autoritativo pero NO hard-failea la edicion manual, y hoy nada lo rechaza (solo se degrada en silencio). Este
guard acopla los flags y lo rechaza con error claro.

## Alcance (SPEC-0067)

1. `event_state_config_error(config)` en `runtime/protocol_replay.py`: error si `authoritative` sin `enforce`
   (recomendado toda la cadena: authoritative=>enforce=>materialize=>enabled; enforce/authoritative solo en
   tier runtime). Mensaje accionable.
2. Cablear para que MUERDA: `validate_collaboration_state.py` -> `validation.fail` si incoherente;
   `submit_intent.py` + `apply.py` -> raise antes de aplicar. (Reusar la misma funcion.)
3. Golden: authoritative-sin-enforce RECHAZADO (validador falla + submit_intent raise); cadenas coherentes
   (todos true / enabled+materialize+enforce / off) pasan; coordination-tier no aplica.
4. Paridad `.ps1` del validador + CI.

## Restricciones (duras)

- enforce+authoritative ON: CERO edicion manual de `state/*.json` -> todo por `submit_intent`/`ledger_ops`.
- **Template intacto** (no cambia defaults del master). Config vivo (todos true) DEBE seguir pasando el validador.
- Neutral, ASCII, sin secretos. Aditivo, determinista. Release/handoff DECISION-0018/0020.

## Cierre

Claude ratifica adversarialmente (golden authoritative-sin-enforce rechazado en vivo; config vivo coherente
pasa; regresiones verdes) y cierra por submit_intent. Su ciclo de vida cuenta para estabilizar la ventana de
observacion de authoritative.
