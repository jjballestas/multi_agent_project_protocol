# DRAFT v2 (REMEDIACION DE SEGURIDAD) - Extension 2 de SPEC-0086: intake relay acotado + anti-impersonacion + camino feliz (RF-14)

> DRAFT v2 en personal/Arquitecto; NO promovido. Gated por DECISION-0052 v2 (ratificacion pendiente).
> Cierra (1) la FALLA DE VERIFICACION de TASK-0133 (happy path nunca probado) Y (2) el DEFECTO DE SEGURIDAD
> CRITICO ya mergeado (impersonacion via payload.actorId/intents). Insumo: veredicto adversarial del Analista
> (Area_comun/artifacts/ANALISTA-intake-relay-veredicto-adversarial.md).

## RF-14 (actualizado): modelo de escritura del intake (relay ACOTADO)
- El servidor construye el intent del intake **server-side** (builder estricto desde campos de datos);
  NUNCA usa `payload.actorId` ni `payload.intents` crudos.
- Actor del evento = `Arquitecto` (firmante pinned RELAY), determinado server-side, SOLO para la forma
  exacta `requirement-intake`. Payload: `author:Operador`, `origin:front-intake`, `relayed_by:Arquitecto`,
  `endorsement:none`.

## AC15 (REVISADO) - EXECUTE: negativo **y** CAMINO FELIZ con write REAL
- **Negativo (existente):** execute sin `confirm:SUBMIT_INTENT` -> 409, sin escritura.
- **CAMINO FELIZ (write REAL, no mock):** test de comportamiento PERMANENTE en CI que demuestra
  `execute+confirm` -> escritura REAL por submit_intent: el requirement aterriza en TASK_INDEX/PROJECT_STATE
  (proposed, author=Operador, relayed_by=Arquitecto), runtime ok con seq, drift 0 despues. NO basta dry_run.

## AC19 (NUEVO, CRITICO) - ANTI-IMPERSONACION (prueba negativa PERMANENTE)
El front NO confia en el cliente para autoria ni forma. Test de comportamiento permanente: un POST al
endpoint EXECUTE que intente (a) un `payload.actorId` distinto, o (b) `payload.intents` arbitrarios
(decision/claim/task_status/cualquier forma != requirement-intake) para firmarse como Arquitecto -> es
**RECHAZADO** (no construye, no firma, no escribe). Solo la forma exacta del requirement-intake se relaya.
Falla si un cliente local puede forjar un evento atestado firmado como Arquitecto. (Remedia la anomalia
DECISION-0018 ya mergeada en Zeus 42e7931.)

## AC18 (atribucion honesta - RENDER) + AC20 (accountability)
- **AC18:** test de RENDER -- la UI muestra firmante=Arquitecto y `author:Operador`; NINGUN verde/elemento
  afirma "Operador firmo".
- **AC20 (NUEVO):** firma del relay = origen+transporte, NO aval (`endorsement:none`); test de que un evento
  relayado NO se cuenta/renderiza como AUTORADO/avalado por el Arquitecto. El aval es la SPEC posterior.

## AC4/#4 (reforzado) - byte-identico
Aserto: `protocol.config.json` (signer set), genesis, keys y `protocol_version` **BYTE-IDENTICOS**
antes/despues del intake (no solo drift 0). El relay no toca el config/epoca.

## AC16 (PII) - sin sobre-afirmar
Redaccion estructural real por PATRONES (NIT/razon social/SQL + ASCII) best-effort; **NO se afirma
"PII-free" garantizado** (un nombre/email/telefono podria pasar). DEF-PII (TASK-0118) sigue siendo el gate
antes de captura viva de PII real.

## Carry permanentes
AC11/AC12/AC13 + AC14/AC17 verdes.

## test_plan (anadido)
- Anti-impersonacion (AC19): forjar actorId/intents -> RECHAZADO (permanente, CI).
- Camino feliz (AC15): write REAL + seq + drift 0 + atribucion, desde clon limpio.
- Render (AC18) + accountability (AC20) + byte-identico (#4). validate exit 0 con/sin secretos (DECISION-0046).

## UX (Claude Design; NO bloqueante)
project-first (selector de proyecto primero; demas campos habilitados tras elegir) + tipografia del selector
destacada.
