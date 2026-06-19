---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-impl-TASK-0129
type: HANDOFF
task_id: TASK-0129
from: Arquitecto
to: Codex
requires_response: false
status: answered
one_line_summary: GO implementacion TASK-0129 (ready) - endurecimiento badge-honesto: test de COMPORTAMIENTO en Zeus-protocol (verificacion-runtime que FALLA -> badge NO-verde; todo-valido -> verde; PII siempre redactada). Pieza chica previa a etapa5 (GO operador). maker=Codex / checker=Arquitecto.
context_refs:
  - Area_comun/tasks/TASK-0129-codex-front-badge-behavior-test.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
deadline_or_blocking_level: normal
---

# GO: TASK-0129 - test de comportamiento del badge (regresion-proof)

Codex: GO a implementar TASK-0129 (ready). Es la pieza chica previa a la etapa 5 (secuencia confirmada por
el operador; origen: recomendacion del Analista sobre TASK-0128). Codigo en `D:\Agentes\Zeus\Zeus-protocol`.

## Problema
El `staticContract.test.js` que cubre la honestidad de estado es **string-match**: prueba que el codigo
MENCIONE los validadores, NO que el badge se ponga **no-verde** cuando la verificacion falla. Un refactor que
conserve los strings pero repinte verde una verificacion fallida pasaria igual = falso verde sobre la
propiedad-tesis.

## Que hacer (alcance en TASK-0129)
Test de **COMPORTAMIENTO** (node --test) que inyecte una verificacion-runtime controlada y asevere el render:
- `chain.valid=false` -> badge cadena NO-verde; `attested`=false.
- item de `event_auth` invalido -> badge event-auth NO-verde; `attested`=false.
- `anchor` invalido / `drift.has_drift=true` / validator no-ok -> `attested`=false (no verde).
- `source.state != "canonical"` -> chip canonico NO-verde (warn) aunque lo demas verifique.
- TODO valido -> atestado VERDE. No verificable (sin secretos/sin entries) -> "indeterminate" (warn), nunca verde.
- PII: payload con texto -> preview SIEMPRE "[redacted - PII de tercero]" (positivo y negativo).

Las funciones ya son inyectables (`loadRuntimeVerification` acepta runner; `attested`/`sourceClean`/`variant`
en app.js testeables con fake). Podes extraer la derivacion del badge a una **funcion pura** testeable SIN
cambiar el comportamiento observable (el render canonico vivo debe quedar identico).

## DoD / gates
- Test falla si se repinta verde una verificacion fallida o si el payload con texto no queda redactado.
- node --test verde (>= 11 + nuevos), gateado por EXIT REAL. Read-only intacto (sin ruta de escritura nueva).
- Gates protocolo: validate CON y SIN secretos exit 0; drift 0; scans exit 0. Epoca 1.14.0 pinned, #4 ON intacto.
- Reporta a in_review con claim file-scoped + submit_intent; reproduzco como checker desde clon limpio.

Cuando cierres esta, sigue **etapa 5 roster (RF-9)** -- te llega su SDD aparte (la autoro a continuacion).
Canal ASCII.
