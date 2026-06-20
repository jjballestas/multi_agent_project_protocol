---
id: TASK-0129
title: Proyecto-front - endurecimiento badge-honesto - test de COMPORTAMIENTO (regresion-proof honestidad de estado), producto Zeus-protocol (SPEC-0086 AC11)
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049]
created_at: 2026-06-20
---

# TASK-0129 - Endurecimiento badge-honesto: test de comportamiento

## Objective

Pieza chica previa a la etapa 5 (GO operador, secuencia confirmada; origen: recomendacion del Analista
sobre TASK-0128). Hacer **regresion-proof** la honestidad de estado del front: hoy el test que la cubre
(`staticContract.test.js`) es **string-match** (prueba PRESENCIA de los validadores en el codigo, NO el
COMPORTAMIENTO del badge). Un refactor que conserve los strings pero repinte verde una verificacion fallida
**pasaria el test igual** = falso verde sobre la propiedad-tesis. maker=Codex, checker=Arquitecto.

En `D:\Agentes\Zeus\Zeus-protocol`. Read-only intacto; sin tocar #4 (epoca 1.14.0 pinned).

## Alcance (producto Zeus-protocol)

Agregar un **test de COMPORTAMIENTO** (node --test) que inyecte una verificacion-runtime controlada y
asevere el render real del badge (no la presencia de strings):

- `chain.valid=false` -> badge cadena NO-verde (warn/danger); `attested` = false.
- un item de `event_auth` invalido -> badge event-auth NO-verde; `attested` = false.
- `anchor` invalido / `drift.has_drift=true` / validator no-ok -> `attested` = false (NO verde).
- `source.state != "canonical"` (working_tree) -> chip canonico NO-verde (warn) aunque todo lo demas verifique.
- TODO valido (chain/sig/anchor/event_auth ok + drift false + validator ok + source canonical) -> atestado VERDE.
- runtime no verificable (sin secretos / sin entries) -> badge "indeterminate" (warn), NUNCA verde.
- PII: payload con texto -> preview SIEMPRE "[redacted - PII de tercero]" (caso positivo y negativo).

Las funciones ya son inyectables (`loadRuntimeVerification` acepta runner; la derivacion de `app.js`
-- `attested`, `sourceClean`, `variant` -- es testeable con un modelo fake). Permitido extraer la logica de
derivacion del badge a una **funcion pura** testeable, **sin cambiar el comportamiento observable** (el render
canonico vivo debe quedar identico).

## DoD

- Test de comportamiento agregado que cubre los casos de arriba; **falla** si se repinta verde una
  verificacion fallida o si el payload con texto no queda redactado.
- `node --test` verde (>= los 11 actuales + nuevos), gateado por EXIT REAL.
- Comportamiento observable del badge SIN cambios en el caso canonico (mismo render que hoy).
- Read-only intacto: ninguna ruta de escritura nueva.
- Gates del protocolo: `validate_collaboration_state.py --root .` CON y SIN secretos exit 0; drift 0;
  `scan_encoding` / `scan_domain_neutrality` exit 0. Epoca 1.14.0 pinned, #4 ON intacto.
- maker=Codex / checker=Arquitecto; reproduccion del checker desde clon limpio. Reporta a in_review con
  claim file-scoped + submit_intent. Codigo en Zeus-protocol; cita/gobernanza en Area_comun (dataset).

## Verification

- CI del producto verde (node --test) incluyendo los casos de comportamiento (falla->no-verde; valido->verde;
  indeterminado->warn; PII siempre redactado).
- Gates del protocolo exit 0 (con y sin secretos), drift 0, gateado por EXIT REAL del validador.
