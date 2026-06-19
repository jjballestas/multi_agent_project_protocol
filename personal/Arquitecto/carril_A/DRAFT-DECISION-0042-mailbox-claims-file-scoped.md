---
decision_id: DECISION-0042 (DRAFT - id final al promover)
title: Claims sobre el mailbox deben ser file-scoped - prohibicion de locks dir-level del canal compartido + guard de enforcement
status: draft (pendiente GO operador)
date: 2026-06-19
deciders: [operador humano (pendiente), Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0020, DECISION-0018, DECISION-0007, DECISION-0012]
phase: P2
---

# DECISION-0042 (DRAFT) - Mailbox claims file-scoped (anti-deadlock del canal)

> DRAFT del Arquitecto. Medida pedida por el operador ("eso no puede pasar") tras un incidente real
> (2026-06-19): un claim de coordinacion con scope dir-level sobre `Area_comun/mailbox/` bloqueo la
> respuesta de Codex en el canal. Addendum a DECISION-0020 (anti-colision). Aditivo. La parte de
> enforcement (guard) es implementacion de Codex.

## Contexto

El mailbox es el **canal compartido multi-escritor** de coordinacion. DECISION-0007 exige un claim activo
antes de crear/editar archivos en rutas compartidas. El problema: si ese claim usa scope a nivel de
**directorio** (`Area_comun/mailbox/`, o `.../open/`, `.../answered/`, `.../archived/`), el solapamiento
de scope (`scopes_overlap`) bloquea que el peer adquiera su propio claim para **responder** -> deadlock
auto-infligido contra el peer.

**Incidente (2026-06-19):** el Arquitecto adquirio `CLAIM-...-promo-coord` con scope
`["Area_comun/mailbox/open/","answered/","archived/"]`. Codex reporto: "el Arquitecto dejo activo un claim
que cubre todo Area_comun/mailbox/, justo donde tendria que responderle; espero ventana segura". El
Arquitecto libero el claim. El bug NO debe poder repetirse.

## Decision

1. **Regla (vinculante para todos los agentes).** El `scope` de un claim que toque el mailbox debe listar
   **archivos `MSG-*.md` concretos**, nunca un **directorio** del mailbox. La higiene que mueve varios
   mensajes lista cada archivo explicitamente. Los archivos de estado (`Area_comun/state/*.json`) y otros
   no-canal pueden ir en scope como siempre (no bloquean el canal).

2. **Enforcement (guard - teeth).** El validador (`scripts/validate_collaboration_state.py`) y/o
   `runtime/submit_intent.py` **RECHAZAN** un `claim acquire` cuyo `scope` contenga una **ruta de
   directorio del mailbox** (una entrada bajo `Area_comun/mailbox/` que no termine en un `MSG-*.md`
   concreto). Mensaje de error claro ("mailbox claim must be file-scoped: <entry>"). Asi el bug es
   imposible, no solo desaconsejado. Implementacion = Codex (dueno del validador/runtime); golden:
   un claim dir-level de mailbox es rechazado; uno file-scoped pasa.

3. **Alcance del guard.** Solo el mailbox (canal). NO aplica a `Area_comun/state/*.json` ni a otras rutas
   (esas pueden ser claim a nivel de archivo completo). Aditivo; no rompe claims historicos (el guard
   actua en `acquire`, no re-valida claims ya released del archivo).

## Alcance / No-alcance

- **En alcance:** la regla (addendum DECISION-0020) + el guard en validador/submit_intent + golden.
- **Fuera de alcance:** cambiar el modelo de claims fuera del mailbox; tocar #4 ni Carril A.

## Consecuencias

- El canal de coordinacion no puede quedar bloqueado por un claim de un agente: el peer siempre puede
  responder sobre archivos distintos.
- Refuerza DECISION-0020 (anti-colision) con un control automatico, no solo disciplinario.

## Tarea de implementacion

- **TASK-0119 (Codex):** implementar el guard (validador + submit_intent) + golden (dir-level rechazado,
  file-scoped aceptado); paridad py/ps si aplica; aditivo, SemVer MINOR + CHANGELOG. `type: security`.

## Alternativas consideradas

- **Solo regla documental (sin guard).** Descartada: el operador pidio que "no pueda pasar"; lo
  disciplinario ya fallo una vez. Se necesita enforcement.
- **Prohibir claims sobre mailbox del todo.** Descartada: DECISION-0007 exige claim para escribir rutas
  compartidas; la solucion es granularidad (file-scoped), no quitar el claim.
