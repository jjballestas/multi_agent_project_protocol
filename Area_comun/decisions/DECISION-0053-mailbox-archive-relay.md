---
decision_id: DECISION-0053
title: Accion de relay acotada "mailbox-archive" + nuevo intent kind core `mailbox_archive` (higiene de mailbox gobernada desde el front)
status: accepted
ratified_at: 2026-06-20
date: 2026-06-20
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amends: [DECISION-0052]
relates_to: [DECISION-0052, DECISION-0051, DECISION-0018, DECISION-0046]
phase: P2
---

# DECISION-0053 - Relay acotado "mailbox-archive" + intent kind core `mailbox_archive`

> ACCEPTED por el operador (2026-06-20, GO-ratifica-DECISION-0053-mailbox-archive). Amends DECISION-0052
> (relay acotado anti-impersonacion). Origen: REQ-B65E7802 (intake del operador). NO toca config/genesis/keys
> (#4 epoca 1.14.0 PINNED, byte-identica). maker=Codex / checker=Arquitecto; PASADA DEL ANALISTA validando el
> bounding + neutralidad ANTES de cerrar.

## Contexto
REQ-B65E7802: el operador quiere higienizar (archivar) mensajes ya leidos/procesados del mailbox con UN CLICK
desde el front, sin bajar a la terminal. Hoy la higiene de mailbox se hace con `git mv` manual del agente
(open->archived + status del frontmatter); NO existe ningun intent de runtime que mueva archivos de mailbox.

El front NO puede tener una ruta de escritura directa (AC17 no-bypass; el runtime es el ESCRITOR UNICO bajo #4
enforce). Para que el front archive un mensaje, la operacion DEBE pasar por el relay gobernado -> `submit_intent`
-> un evento ATESTADO, con la MISMA disciplina anti-impersonacion que el intake (DECISION-0052).

## Por que una DECISION propia (y no solo prosa en 0052)
DECISION-0052 acoto el relay a la forma exacta `requirement-intake` (un task_upsert existente). Archivar mailbox
requiere un **NUEVO intent kind en el runtime core** (`mailbox_archive`) que muta estado del mailbox y emite un
evento atestado nuevo. Agregar un intent kind al ESCRITOR UNICO es un cambio de SUPERFICIE DEL PROTOCOLO
(regla 2: cambio de protocolo -> DECISION primero), aunque sea ADITIVO y backward-compatible. Se registra como
DECISION para mantener el rastro de gobernanza auditable.

## Decision
1. **Nuevo intent kind core, neutral: `mailbox_archive`.** Aditivo a `INTENT_TYPES`. Payload estricto:
   `{ message_id }` (mensaje existente bajo `Area_comun/mailbox/open/`). El runtime:
   - VALIDA que el mensaje existe en `open/` y que su ruta esta dentro de `Area_comun/mailbox/` (rechaza ids
     forjados / rutas fuera del mailbox / path-traversal);
   - emite un evento ATESTADO (firmado por el actor del relay) que registra el archive
     (author=Operador, relayed_by=Arquitecto, endorsement=none);
   - aplica el side-effect (`apply_mailbox_side_effects`, analogo a `apply_task_file_side_effects`): mueve
     `open/<msg>.md` -> `archived/<msg>.md` y setea `status: archived` en el frontmatter (canal ASCII);
   - es IDEMPOTENTE: re-archivar un mensaje ya archivado (mismo idempotency_key) es no-op, no falla.
   El core sigue DOMAIN-NEUTRAL (mailbox es maquinaria generica del protocolo).
2. **Accion de relay acotada en el server (Zeus): `mailbox-archive`.** Builder SERVER-SIDE estricto: construye el
   intent `mailbox_archive` desde un `message_id` VALIDADO; NUNCA confia en `payload.actorId`/`payload.intents`
   crudos (hereda la defensa de 0052). actor del evento = Arquitecto (firmante pinned) EN NOMBRE del Operador.
   `assertAllowedKeys` cierra el payload del submission. El hard-gate 403 admite EXACTAMENTE dos acciones
   (`requirement-intake`, `mailbox-archive`); cualquier otra forma sigue 403.
3. **Anti-impersonacion permanente (PRUEBA NEGATIVA):** un cliente local NO puede (a) forjar `actorId`/`intents`,
   (b) archivar un mensaje inexistente o fuera de `open/`, (c) usar `mailbox-archive` para emitir cualquier OTRO
   intent. Se rechaza antes del backend. Test permanente en CI (no reabrir el 403; mismo espiritu que AC19).
4. **#4 epoca 1.14.0 BYTE-IDENTICA:** `mailbox_archive` NO toca `protocol.config.json` (signer set), genesis, keys
   ni `protocol_version`. Los eventos del nuevo kind se encadenan normalmente (el genesis ancla al hash del config,
   no al esquema de intents); se asierta byte-identidad de config/manifest/keys antes/despues.
5. **Accountability:** el archive relayado se atribuye author=Operador / relayed_by=Arquitecto / endorsement=none;
   no se cuenta como "autorado/avalado" por el Arquitecto (hereda AC20).

## Alcance / limites
- NO es un segundo escritor: el unico escritor del estado sigue siendo el runtime (`submit_intent`).
- Vista Mailbox READ-ONLY salvo el archive gobernado. Solo archive (open->archived); NO delete.
- La politica de QUE se puede archivar la decide el operador con el click; el runtime solo exige que el mensaje
  exista en `open/`. La UI puede advertir si `requires_response:true` y no esta answered, sin bloquear.

## Consecuencias
Se agrega un intent kind core (afecta `runtime/submit_intent.py`, el validador y la doc del protocolo) y una
accion de relay en el producto. Backward-compatible. El mailbox pasa a tener una mutacion gobernada y atestada
(antes solo git mv manual del agente, que sigue valido para los agentes en terminal).

## Condiciones de cierre (innegociables, del operador)
(a) hard-gate admite EXACTAMENTE {requirement-intake, mailbox-archive}, el resto 403 (test permanente);
(b) AC25 verde: id inexistente / fuera de open/ / path-traversal / otro-intent-via-mailbox-archive -> RECHAZADO;
(c) builder server-side, nunca confiar en payload.actorId/intents; (d) AC24: archive idempotente, atribucion
honesta (relayed_by=Arquitecto, nada de "Operador firmo"), auditable; (e) un archive real deja el canonico VERDE
(regresion-proof, como AC22); (f) #4 byte-identica, validate con/sin secretos exit 0, drift 0, npm test verde,
neutralidad/encoding 0; (g) PASADA DEL ANALISTA validando bounding + neutralidad ANTES de cerrar.
