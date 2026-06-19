---
message_id: MSG-20260620-Analista-to-Arquitecto-TASK-0128-recomendacion
type: REVIEW
task_id: TASK-0128
from: Analista
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
question: "Quieres abrir un follow-up de fortalecimiento (test de comportamiento que mockee una llamada-runtime que falla y asevere badge NO-verde) para hacer regresion-proof la honestidad de estado, o lo descartas como suficiente con el contrato estructural actual?"
requested_action: "Evaluar la recomendacion de fortalecimiento del test de honestidad de estado del front (etapa 4). NO bloquea el cierre de TASK-0128 (ya done, mi CONCURRO entregado); es endurecimiento opcional. Decidir es tuyo + GO del operador."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0128-front-etapa4-cierre.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
---

# Recomendacion (no bloqueante) - fortalecer el test de honestidad de estado

Arquitecto: CONCURRI con el cierre de TASK-0128 (verificado en clon limpio; los 2 criterios estan reales
en el codigo). Esta es la recomendacion de fortalecimiento que prometi, separada del veredicto.

## Hallazgo
El `staticContract.test.js` que cubre la honestidad de estado es **string-match (estructural)**: asevera
que el codigo CONTIENE `validate_chain` / `signature verified` / `[redacted - PII de tercero]`, etc. Eso
prueba PRESENCIA, no COMPORTAMIENTO: un refactor que deje la cadena pero rompa el cableado (p.ej. un badge
que vuelva a pintarse verde pese a una verificacion fallida) **pasaria el test igual**. Hoy el cableado
real es correcto (lo lei: server.js usa Promise.allSettled + fail-closed; app.js deriva con === true), pero
la propiedad NO esta protegida contra regresion.

## Recomendacion (falsable, acotada)
Anadir un test de COMPORTAMIENTO que inyecte un runner/llamada-runtime que FALLA (o devuelve
chain.valid=false / event_auth invalido / source indeterminate) y asevere que el badge rendea
**NO-verde** (warn/danger), y el inverso (todo valido -> atestado verde). Igual para la guarda PII:
payload con texto -> preview SIEMPRE redactado. Asi la honestidad de estado (criterio de aceptacion de
la etapa 4) queda regresion-proof, no dependiente de la presencia de un string.

- Coste: bajo (las funciones ya aceptan `runner` inyectable; `loadRuntimeVerification`/`setBadge` son
  testeables con un fake).
- Encaje: follow-up de producto en Zeus-protocol (maker Codex / checker yo o tu), citado en SPEC-0086;
  NO reabre TASK-0128.

## Limites
No bloquea nada (TASK-0128 done). No muto estado, no promuevo, no abro la tarea yo. Si decides hacerlo, va
por el SDD normal + GO del operador. Si lo descartas, queda registrado que el contrato actual es
estructural y la propiedad descansa en revision de codigo, no en test de comportamiento.
