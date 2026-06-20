# DRAFT - Extension 2 de SPEC-0086: camino feliz del intake + relay-signer (RF-14)

> DRAFT en personal/Arquitecto; NO promovido. Gated por DECISION-0052 (ratificacion pendiente).
> Cierra la FALLA DE VERIFICACION de TASK-0133: AC15 solo probo el 409 negativo; NUNCA el write real.

## RF-14 (actualizado): modelo de escritura del intake
- El front emite EXECUTE con `actorId:"Arquitecto"` (firmante pinned RELAY; DECISION-0052), NO `Operador`.
- El payload requirement lleva `author:"Operador"`, `origin:"front-intake"`, `relayed_by:"Arquitecto"`.
- La transaccion envuelve `claim(acquire as Arquitecto) -> task_upsert(requirement) -> claim(release)`
  (enforce exige claim del actor que cubra el scope).

## AC15 (REVISADO) - EXECUTE: prueba NEGATIVA **y** CAMINO FELIZ
- **Negativo (ya existia):** `mode:execute` sin `confirm:SUBMIT_INTENT` -> 409, sin escritura, drift 0.
- **CAMINO FELIZ (NUEVO, obligatorio - filosofia AC11):** un test de COMPORTAMIENTO que demuestra
  `execute + confirm:SUBMIT_INTENT` -> **escritura REAL exitosa** por submit_intent: el requirement aterriza
  en TASK_INDEX/PROJECT_STATE (status proposed, author=Operador, relayed_by=Arquitecto), el runtime devuelve
  ok con seq, drift 0 despues. Falla si el front ofrece el boton pero el write real no ocurre (justo el bug
  de dogfooding). NO basta el dry_run ni el 409: hay que probar que el happy path ESCRIBE.

## AC18 (NUEVO) - Atribucion honesta del relay
La UI declara el modelo de firma (firmado por el Arquitecto en nombre del Operador; `author:Operador`); el
evento registrado muestra `author:Operador` + `relayed_by:Arquitecto`. Test: el payload/evento del intake
lleva ambos campos; ningun plano afirma que el Operador firmo criptograficamente.

## Carry permanentes
AC11/AC12/AC13 + AC14/AC16/AC17 siguen verdes.

## test_plan (anadido)
- **Camino feliz del intake (integration):** levantar el server (o invocar el builder + submit_intent con
  runtime real/fixture), enviar intake execute+confirm, asertar escritura real + seq + drift 0 + atribucion.
- Reproduccion desde clon limpio; validate exit 0 con y sin secretos (DECISION-0046); #4 epoca 1.14.0 intacta.

## UX (insumo de Claude Design; NO bloqueante, aplicar en el rework)
- **Project-first:** el selector de PROYECTO va PRIMERO; titulo/narrativa/intencion se habilitan SOLO tras
  elegir proyecto.
- **Tipografia del selector:** debe DESTACAR/distinguirse del resto del texto.
