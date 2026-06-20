# DECISION-0052 (DRAFT) - Mecanismo de firma del intake del operador: RELAY/co-firma por un firmante pinned (sin tocar la epoca #4)

- status: proposed (DRAFT en personal/Arquitecto; NO promovido; espera ratificacion del operador)
- type: protocol-surface / governance
- amends: DECISION-0051 (refina el MECANISMO de escritura; el resto de 0051 sigue vigente)
- relates: DECISION-0040 (PII), DECISION-0045/0046 (#4), RF-9 roster (re-genesis, diferido)
- proposed_by: Arquitecto · ratifies: Operador

## Causa (dogfooding, MSG-BUG-intake-execute-actor-no-registrado)
DECISION-0051 fijo `actorId:"Operador"` para el intake. Bajo #4 enforce el runtime EXIGE que el actor de
cada evento este registrado Y tenga secreto de firma. `Operador` no esta en `agent_registry` ni en
`protocol.config.json:event_auth.keys` -> submit_intent lo rechaza ("actor not registered/enabled: Operador").
**Probado:** actor=Operador -> REJECTED; actor=Arquitecto -> pasa el registro (solo requiere claim, que la
transaccion provee). El conjunto de firmantes vive en `protocol.config.json`, cuyo hash es el `prev_hash` del
`chain.genesis` -> **agregar al Operador como firmante = editar el config = re-genesis = toca la epoca 1.14.0
PINNED.** Por eso `actorId:"Operador"` era inviable bajo el "no toca #4" que afirmo 0051.

## Decision (mecanismo elegido: opcion (b) RELAY)
El intake del operador se escribe **RELAYADO/co-firmado por un agente firmante ya existente en el conjunto
pinned** (el **Arquitecto**, agente responsable del runtime). Concretamente:
- El front emite el EXECUTE con `actorId:"Arquitecto"` (firmante pinned; firma con su clave ya anclada al
  genesis -> **cadena #4 intacta, sin re-genesis, epoca 1.14.0 PINNED**).
- El payload del `task_upsert` requirement lleva la **autoria honesta del originador**: `author:"Operador"`,
  `origin:"front-intake"`, `relayed_by:"Arquitecto"`. El dataset NO afirma que el Operador firmo
  criptograficamente; afirma que el Arquitecto (firmante responsable) RELAYO un requisito ORIGINADO por el
  operador via el intake gobernado del front.
- El Operador NO se agrega al registry de firmantes ni al config. No hay clave nueva. No hay re-genesis.

## Por que NO las otras opciones (ahora)
- (a) Actor no-firmante gateado: el modelo firma POR el actor del evento (`sign_event` usa `event.actor`);
  un actor sin secreto -> "signing key missing". No hay actor no-firmante sin tocar el modelo de firma del
  runtime (cambio de mecanismo mas profundo, no justificado).
- (c) Re-genesis para volver al Operador firmante: lo mas pesado; cambia el conjunto pinned; pertenece a la
  ceremonia RF-9 roster (DIFERIDA). Queda como camino FUTURO si el operador quiere su propia firma
  criptografica; hoy se rechaza por costo/alcance.

## Honestidad (lente Analista)
La UI debe declarar el modelo: "tu historia se registra como evento gobernado, FIRMADO por el Arquitecto
(agente del runtime) EN NOMBRE del Operador; tu autoria queda como `author:Operador`". Nada sugiere que el
Operador firma. Coherente con AC11 (no verde falso) y con la atestacion honesta del #4.

## Boundaries
No toca INTENT_TYPES, ni el config, ni la epoca. Mantiene `directLedgerWrites:false` y un solo writer
(submit_intent). Neutralidad intacta.

## Rollback
Deshabilitar la accion de intake en el front (como 0051). Sin cambios de runtime que revertir.
