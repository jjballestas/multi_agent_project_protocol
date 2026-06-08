---
spec_id: SPEC-0067-guard-authoritative-requiere-enforce
task_id: TASK-0086
type: design
status: ready
created_at: 2026-06-08
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0006]
relates_to: [TASK-0085, SPEC-0066]
---

> PROMOVIDA por Claude (2026-06-08) bajo enforce+authoritative. Cierra el "false-secure" detectado al flipear
> authoritative: hoy `authoritative=true` con `enforce=false` NO da error, solo se degrada en silencio
> (authoritative_enabled=False). Un config asi PARECE autoritativo pero no esta enforced. Este guard lo RECHAZA.

# Diseno - Guard: authoritative=true REQUIERE enforce=true (acople duro de flags)

## 1. Objetivo

Que un `event_state` con `authoritative:true` y `enforce:false` (o el resto de la cadena rota) sea **rechazado
con error claro** por la maquinaria existente, en vez de degradarse en silencio. Mata el riesgo de un config
"false-secure" (parece escritor-unico pero la edicion manual no hard-failea).

## 2. Estado actual (punto de partida)

- `protocol_state_enforcement_enabled(cfg)` = `enabled && enforce && tier==runtime`.
- `protocol_authoritative_enabled(cfg)` = `enforcement_enabled && materialize && authoritative`.
- Consecuencia: `authoritative:true` con `enforce:false` => `authoritative_enabled` devuelve **False sin avisar**.
  No hay ningun punto que **rechace** el config inconsistente. Eso es el false-secure.

## 3. Alcance

1. **Invariante de config** (funcion nueva en `runtime/protocol_replay.py`, p.ej.
   `event_state_config_error(config) -> str | None`): devuelve un error si la cadena de flags es incoherente.
   Regla minima exigida: `authoritative:true` REQUIERE `enforce:true`. Recomendado cubrir toda la cadena
   monotonica: `authoritative` => `enforce` => `materialize` => `enabled` (cada nivel exige el anterior); y
   `enforce`/`authoritative` solo validos en `tier==runtime`. Mensaje accionable (que flag falta).
2. **Cableado por la maquinaria existente** (que MUERDA, no que degrade):
   - `scripts/validate_collaboration_state.py`: si `event_state_config_error` != None => `validation.fail`
     (HARD-FAIL, igual que el drift bajo enforce). Asi CI y el validador local rechazan el config incoherente.
   - `runtime/submit_intent.py` y `runtime/apply.py`: rechazar la operacion (raise) si el config es incoherente,
     ANTES de aplicar intents / commitear turno. (Reusar el mismo `event_state_config_error`.)
3. **Golden** (`examples/` nuevo o extension de enforce/replay cases):
   - `authoritative:true + enforce:false` => `event_state_config_error` != None; validador FALLA; submit_intent
     RECHAZA. 
   - cadena coherente (todos true, o todos false, o enabled+materialize+enforce sin authoritative) => sin error.
   - off/coordination-tier => sin error (no aplica).
4. **Paridad** `.ps1` del validador donde aplique + CI.

## 4. Invariantes
1. Config coherente actual (enabled+materialize+enforce+authoritative todos true) => sin cambio de comportamiento.
2. Off/sin enforce coherente => byte-equivalente; template intacto (no cambia defaults del master).
3. Determinista, neutral, ASCII, sin secretos. Aditivo.

## 5. Cierre (DoD)
- `event_state_config_error` implementado + cableado en validador (hard-fail) + submit_intent/apply (raise).
- Golden que demuestra: authoritative-sin-enforce RECHAZADO (validador falla + submit_intent raise); cadenas
  coherentes pasan. Regresiones verdes. Paridad .ps1/CI. Template intacto.
- Verificacion EN VIVO no requerida (el config vivo ya es coherente: todos true); basta golden + que el config
  vivo siga pasando el validador.

## 6. Fuera de alcance
- Decidir/implementar teeth propias de authoritative (defense-in-depth): es el follow-up TASK-0087
  (bloqueante para ADOPCION, no para SA.4).
- SA.4 y Capa C (ventanas separadas).
