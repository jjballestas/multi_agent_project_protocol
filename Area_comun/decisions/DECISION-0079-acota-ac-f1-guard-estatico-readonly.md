---
decision_id: DECISION-0079
title: "Acota el AC F1: el guard estatico read-only cubre firmas enumerables; la garantia dura es el endpoint backend"
status: accepted
date: 2026-07-01
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0072, DECISION-0074, TASK-0227]
scope: product
phase: P2
---

# DECISION-0079 - Frontera del guard estatico F1 (panel de gobernanza read-only)

## Contexto

TASK-0227 (REQ-ZEUS-001) pide un guard que verifique que el front del panel de gobernanza es **read-only**: que
no exista ningun write-path del cliente hacia `/api/governance/*`. El guard implementado es un analisis
**estatico** del codigo del front.

Tras cuatro rondas de revision adversarial del Analista (rem-1..rem-3 NO-GO), el patron es claro: cada ronda el
Analista construye una firma de write-path mas indirecta que el guard estatico no atrapa
(`fetch(url, opts)` con `opts` armado en runtime, `fetch(new Request(...))`, `axios.request(url, cfg)`
posicional, y las variantes shorthand/computed ya cubiertas). Esto es esperado: **decidir estaticamente si un
codigo arbitrario ejecuta un write es indecidible** (un `opts` construido en runtime, o un `method` leido de una
variable no rastreable, no es decidible por un lint sin analisis de flujo completo). Un guard estatico nunca
sera una prueba total de ausencia de writes.

La garantia **dura** de read-only ya existe y es estructural: el **endpoint backend** de gobernanza rechaza
cualquier metodo que no sea de lectura (`governance-readonly.test.ts`, verde). El guard del front es
**defensa en profundidad / alerta temprana** para el caso comun y accidental, no la barrera de seguridad.

## Decision

Se **acota formalmente el AC F1** de TASK-0227 asi:

1. **En alcance del guard estatico (DEBE atrapar, negativos permanentes):** las firmas de write-path
   **estaticamente decidibles y enumerables** hacia rutas de gobernanza:
   - `fetch(url, { method: 'POST'|... })` literal, incluyendo shorthand `{ method }` y computed `{ ['method']: ... }`.
   - `axios({ url, method })`, `axios.<verbo>()`, `axios.request({ url, method })` y `axios.request(url, { method })` con config literal.
   - objeto de opciones **local** con `method` literal pasado a un `fetch` de gobernanza; `new Request(url, { method })` literal.
2. **Fuera de alcance del guard estatico (indecidible):** write-paths construidos puramente en runtime
   (objeto de opciones armado dinamicamente, `method` desde variable no rastreable, indireccion via helpers
   opacos). Estos **no** se persiguen en el lint.
3. **Garantia read-only residual:** queda cubierta por (a) el **endpoint backend read-only** (rechazo estructural
   de metodos de escritura, ya testeado verde) y (b) code review de PRs que toquen el panel.
4. **Cierre:** TASK-0227 se cierra contra este AC acotado una vez rem-4 anada los negativos del punto 1 que aun
   faltan (las 3 firmas del veredicto rem-3). No hay mas rondas de guard mas alla de rem-4.

## Consecuencias

- Corta el arms-race lint (ROI negativo) y evita bloquear el pipeline REQ-ZEUS en una tarea de front.
- Documenta la frontera para futuras instancias: el read-only del panel es una **propiedad del backend**, no del
  lint del front; el lint es complemento.
- Neutralidad de dominio intacta: esta decision es `scope: product` (Zeus-Aegis), no toca el nucleo del protocolo.

## Amendment 2026-07-01 (operador GO tras 6 rondas) - FRONTERA FINAL, familia CERRADA

Tras seis rondas de revision adversarial (rem-1..rem-5), cada una hallando una nueva forma sintactica de la
misma clase (inline, shorthand, computed, typed const, y ahora claves string-literal `"method"`/`"url"`), se
**cierra formalmente y de forma DEFINITIVA** el alcance del guard estatico F1:

- **EN alcance (el guard DEBE atrapar): claves literales `method`/`url` en TODA su forma literal** -- identificador
  sin comillas (`method:`), string literal con comillas (`"method":`, `'method':`) y clave computada literal
  (`['method']`) -- dentro de un objeto de opciones inline, `const` local (tipado o no), `new Request(...)`,
  `axios(...)`, `axios.<verbo>()` y `axios.request(url, cfg)`. rem-6 debe cerrar la clase de claves con comillas.
- **FUERA de alcance, DEFINITIVO (no habra mas rondas de guard):** cualquier construccion que requiera analisis
  de flujo de datos o resolucion dinamica -- `method`/`url` desde variable no rastreable, alias multinivel
  (`const b = opts; fetch(url, b)`), claves template/computadas dinamicas, helpers opacos. Estas quedan cubiertas
  por el **endpoint backend read-only** (rechazo estructural, test verde) + code review.

Racional: el riesgo residual es NULO (el backend rechaza toda escritura con independencia del lint); las formas de
clave literal son un conjunto finito y decidible que rem-6 completa; lo dinamico es indecidible y su persecucion es
ROI negativo. **Con el GO de rem-6, TASK-0227 se cierra contra este AC final y NO hay rem-7.**
