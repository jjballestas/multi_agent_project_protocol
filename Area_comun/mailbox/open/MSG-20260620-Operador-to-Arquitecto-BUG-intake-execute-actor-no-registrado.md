---
message_id: MSG-20260620-Operador-to-Arquitecto-BUG-intake-execute-actor-no-registrado
task_id: TASK-0133
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "HALLAZGO (dogfooding del intake): el camino feliz del intake RF-14 esta ROTO. EXECUTE confirm -> submit_intent falla con 'ERROR: actor not registered/enabled: Operador'. El front ofrece el boton pero el runtime rechaza al Operador como escritor. El checker de TASK-0133 solo probo dry_run + 409 (sin confirm), NUNCA la escritura real -> se fue verde roto. Tension de gobierno: bajo #4 enforce un escritor necesita registro Y firma; proveer al Operador como firmante tocaria la epoca PINNED, lo que contradice el 'no toca #4' de DECISION-0051. Decide tu el mecanismo."
requested_action: "Resuelve el camino feliz del intake (RF-14) por el metodo. (1) CAUSA: submit_intent rechaza el intent con actorId='Operador' -> 'actor not registered/enabled: Operador'. El Operador no esta como agente habilitado en el registry; DECISION-0051 autorizo la SUPERFICIE execute en la UI pero TASK-0133 no dejo al Operador como escritor aceptado por el runtime. (2) DECISION DE GOBIERNO (nucleo): como se vuelve el Operador un escritor aceptado para el intake bajo #4 enforce? Habilitarlo en el registry puede no bastar porque enforce tambien valida FIRMA de agente; proveer una clave de firma al Operador = cambia el conjunto de firmantes = tocaria la epoca 1.14.0 PINNED (re-genesis) -> contradice el 'no toca #4' que afirmo DECISION-0051. Opciones a evaluar: (a) registrar/habilitar al Operador con la capacidad minima para el task_upsert de requirement-intake SIN firma propia (si el modelo admite un actor no-firmante gateado); (b) que el intent del Operador lo CO-FIRME/relaye un agente firmante existente (ej. el Arquitecto) preservando la cadena #4; (c) provisionar al Operador como firmante via la ceremonia de re-genesis-boundary (lo mas pesado; conecta con RF-9 roster, hoy diferido). Reexamina la factibilidad de DECISION-0051 a la luz de esto y elige; si cambia el modelo de escritura -> DECISION (enmienda 0051 o nueva). (3) FALLA DE VERIFICACION: agrega a AC15 (y al test_plan) el CAMINO FELIZ: un test que demuestre execute+confirm -> escritura real exitosa por submit_intent (hoy solo se probo el 409 negativo). Misma filosofia que AC11: probar el comportamiento real, no solo la prueba negativa. maker=Codex/checker=Arquitecto, SDD, reproduccion desde clon limpio. Drafts para mi ratificacion."
question: "Como hacemos al Operador un escritor aceptado para el intake bajo #4 sin romper la epoca pinned (registro no-firmante / co-firma de un agente / re-genesis), y reabres TASK-0133/DECISION-0051 para cerrar el camino feliz + su test? Reporta drafts."
context_refs:
  - Area_comun/decisions/DECISION-0051-operator-execute-write-surface-front.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0133-codex-front-intake-historias.md
  - runtime/submit_intent.py
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: blocking
---

# HALLAZGO (dogfooding) - el intake RF-14 no escribe: "actor not registered/enabled: Operador"

Probe el intake usando el propio front (montar un requisito real para desarrollar el front). El dry_run y la
prueba negativa (sin confirm -> 409) funcionan, pero **EXECUTE con confirm FALLA**:

```
Command failed: python runtime/submit_intent.py --root . --actor-id Operador ... 
ERROR: actor not registered/enabled: Operador
```

## Que significa
El front ofrece el boton EXECUTE, pero el runtime (escritor unico) **rechaza al Operador**: no esta
registrado/habilitado como agente. DECISION-0051 autorizo la SUPERFICIE de escritura en la UI, pero el
Operador no quedo como escritor ACEPTADO por el runtime. El camino feliz nunca se demostro: el checker de
TASK-0133 solo probo dry_run + el 409 (sin confirm).

## La tension de gobierno (tu decision)
Bajo #4 enforce, escribir exige registro Y firma de agente. Proveer al Operador como firmante cambia el
conjunto de firmantes = **tocaria la epoca 1.14.0 PINNED** (re-genesis), lo que contradice el "no toca #4"
de DECISION-0051. Opciones a evaluar: (a) actor no-firmante gateado; (b) co-firma/relay por un agente
firmante existente; (c) re-genesis (lo mas pesado; conecta con RF-9 roster diferido). Reexamina 0051 y elige;
si cambia el modelo de escritura, va por DECISION.

## Ademas
- **Falla de verificacion:** AC15 solo cubrio el 409 negativo. Agrega el test del CAMINO FELIZ (execute+confirm
  -> escritura real exitosa), filosofia AC11.

maker=Codex / checker=Arquitecto. Drafts para mi ratificacion. Verifico tu respuesta en canonico. Canal ASCII.
