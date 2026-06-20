# DRAFT - Extension 5 de SPEC-0086: higiene de mailbox con 1 click (mailbox-archive gobernado) [RF-14]

> DRAFT en personal/Arquitecto; NO promovido. Triage del REQ-B65E7802 (semilla del operador, intake).
> TOCA EL RELAY -> bajo DECISION-0053 (extiende 0052). maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol
> + runtime core (nuevo intent kind `mailbox_archive`).

## Origen (REQ-B65E7802, author=Operador)
"Como operador, quiero ver en el front mis mensajes ya leidos y procesados y archivarlos (higienizar) con un
click, sin bajar a la terminal." Intencion: vista Mailbox con estado (open/answered/archived); boton "archivar"
por mensaje -> emite open->archived + status del frontmatter via submit_intent (relay ACOTADO, builder
server-side), NUNCA edita el mailbox directo; misma disciplina anti-impersonacion que el intake; atestado e
idempotente; vista read-only salvo el archive gobernado.

## AC24 (NUEVO) - Mailbox-archive gobernado de 1 click, atestado e idempotente [comportamiento PERMANENTE; DECISION-0053]
- La vista **Mailbox** muestra los mensajes con su **estado** (open/answered/archived) y marca los consumidos.
- Un **boton "archivar"** por mensaje en `open/` dispara la accion de relay gobernada `mailbox-archive`:
  builder SERVER-SIDE construye el intent `mailbox_archive` desde un `message_id` VALIDADO -> `submit_intent`
  emite un evento ATESTADO (author=Operador, relayed_by=Arquitecto, endorsement=none) y el runtime mueve
  `open/<msg>.md` -> `archived/<msg>.md` con `status: archived` (ASCII).
- **NUNCA edita el mailbox directo**: no hay ruta de escritura del front al filesystem; todo pasa por el runtime
  (escritor unico; extiende la prueba negativa de no-bypass AC17).
- **Idempotente:** re-archivar (mismo idempotency_key / mensaje ya archivado) es no-op, no falla ni duplica.
- **Honestidad (hereda AC11):** el archive y el cambio de estado en la UI SOLO se reflejan si el runtime
  REALMENTE aplico (evento con seq); si falla -> error real visible, el mensaje sigue en open/, NO se pinta como
  archivado.
- Conforme al design-system (hereda AC13: dark-first, tokens; mailbox view existe y navega).

## AC25 (NUEVO) - ANTI-IMPERSONACION de mailbox-archive (prueba negativa PERMANENTE) [CRITICO; DECISION-0053]
El servidor NUNCA confia en datos crudos del cliente para esta accion. Test permanente (no reabrir el 403):
- forjar `payload.actorId` / `payload.intents` / llaves extra -> RECHAZADO (assertAllowedKeys; hereda AC19).
- archivar un `message_id` inexistente o una ruta FUERA de `Area_comun/mailbox/open/` (path-traversal) -> RECHAZADO.
- usar `mailbox-archive` para emitir CUALQUIER otro intent que no sea el `mailbox_archive` de forma exacta ->
  RECHAZADO. El hard-gate admite EXACTAMENTE {`requirement-intake`, `mailbox-archive`}; toda otra forma 403.
- El evento relayado NO se cuenta/renderiza como AUTORADO ni avalado por el Arquitecto (hereda AC20).

## AC4-byte (refuerzo #4)
El nuevo intent kind `mailbox_archive` y la accion de relay NO tocan `protocol.config.json` (signer set),
genesis, keys ni `protocol_version`: se aserta BYTE-IDENTIDAD de config/manifest/keys antes/despues (drift 0 es
necesario, no suficiente). Los eventos del nuevo kind se encadenan normalmente.

## test_plan (anadido)
- **Core (runtime, golden):** `mailbox_archive` valida existencia/ruta del mensaje, emite evento atestado,
  mueve open->archived + flip status, idempotente; rechaza message_id inexistente / ruta fuera de mailbox /
  path-traversal. (Casos golden negativos PERMANENTES.)
- **Server (Zeus):** `mailbox-archive` builder server-side (sin trust de payload.actorId/intents); hard-gate
  admite solo {requirement-intake, mailbox-archive}; camino feliz = archive REAL (write real, no mock) con actor
  relay=Arquitecto; prueba negativa de impersonacion (AC25).
- **Front (Zeus):** Mailbox muestra estado + boton archivar; tras archive OK el mensaje pasa a archived en la UI
  (derivado de la respuesta real); fallo -> error, sigue en open; no-bypass (sin ruta directa al filesystem).
- **Validador protocolo:** un mailbox-archive real deja el canonico VERDE (validate exit 0; el mensaje movido
  casa carpeta/status); regresion-proof (espiritu AC22).
- **Conformidad de diseno (AC13)** contra el design-system de la vista Mailbox.

## Carry permanentes
AC11 / AC13 / AC17 / AC19 / AC20 verdes. #4 epoca 1.14.0 byte-identica. Gates: validate exit 0 con/sin secretos,
drift 0, npm test verde, neutralidad/encoding 0. El core sigue DOMAIN-NEUTRAL (mailbox = maquinaria generica).
