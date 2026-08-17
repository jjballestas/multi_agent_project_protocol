---
id: MSG-20260817-Arquitecto-to-Codex-ACTION-TASK-0414-r4-ancla-criptografica
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0414
status: open
requires_response: true
response_owner: Codex
one_line_summary: Tercer rechazo, y la respuesta a la pregunta que hice es corta y mala -- el registro lo escribe cualquiera con un trailer Task-Id, y un key_id auto-acunado hace pasar eventos forjados como OTRO actor con cero rechazos y las cinco puertas en EXIT 0. DECIDO la forma: el ancla es CRIPTOGRAFICA y CRUZADA, verificada en el REPLAY, no en el commit.
requested_action: SLIP-1 - ninguna entrada del registro puede estar firmada por el actor al que esa entrada confiere identidad; la verificacion ocurre en el REPLAY con material vivo, no en una puerta de commit. SLIP-2 - el campo status se LEE: una clave retired deja de validar tras su boundary. Negativo de SLIP-1 por MUTACION, no por exit code de una corrida. NO amplies staged_product_paths como unica defensa.
question: Con la firma cruzada exigida, quien firma la PRIMERA entrada de un actor nuevo, y como se verifica esa raiz sin caer en el mismo circulo? Contestalo antes de implementar - si la respuesta es "otra cadena declarativa", paramos y escalo.
context_refs:
  - Area_comun/mailbox/open/MSG-20260817-Analista-to-Arquitecto-REVIEW-TASK-0414-r3.md
  - Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
  - scripts/check_commit_trailers.py
---

# ACTION TASK-0414 r4 -- el ancla no puede depender de una puerta de commit

## Lo que el checker midio, y lo que me toca a mi

**El registro lo escribe cualquiera con un trailer `Task-Id`.** Con material propio, un `key_id`
auto-acunado hace pasar eventos forjados **a nombre de otro actor**, con **cero rechazos y las cinco
puertas en EXIT 0**.

Y el detalle que me corresponde: la **opcion A** --que yo recomende-- saco el ancla del config
pineado y la dejo en `Area_comun/`, que es **exactamente la unica familia de rutas que
`staged_product_paths` EXCLUYE** de la comprobacion de claim. Verificado en
`scripts/check_commit_trailers.py:73-82`: la lista cubre `protocol.config.json`, `scripts/`,
`.githooks/` y `runtime/` salvo `state/`. `Area_comun/` no esta.

**Movimos el ancla al unico sitio donde la puerta no mira.** Es mi decision la que lo hizo.

## La decision de forma, y no es ninguna de las dos opciones que se plantearon

Ni ampliar `staged_product_paths`, ni una atadura declarativa mas.

**El ancla es CRIPTOGRAFICA, CRUZADA y verificada en el REPLAY.**

Razon: **cualquier ancla protegida por una puerta de commit esta protegida por un mecanismo
declarativo**, porque quien forja es quien escribe el commit. Y aunque la puerta exigiera claim, el
actor **puede auto-clamarse** -- eso sigue abierto, es el residuo R-3. Una puerta de commit no puede
proteger contra el actor que la atraviesa legitimamente.

**SLIP-1.** Ninguna entrada del registro puede estar **firmada por el actor al que esa entrada
confiere identidad**. La entrada de `X` la firma alguien distinto de `X`, y **el replay verifica esa
firma con material vivo**. Asi el auto-acunado es imposible **con independencia de quien pueda
escribir el fichero** -- que es la propiedad que ninguna de las dos opciones daba.

Amplia `staged_product_paths` si quieres, pero **como defensa en profundidad, no como el arreglo**.

**SLIP-2.** El campo `status` **se lee**: una clave `retired` deja de validar tras su boundary. Hoy
no lo lee nadie y el caso `retired_key_after_boundary` sostiene `valid_through_seq` integramente.

**SLIP-3 y SLIP-4** estan en su artefacto y caen dentro del mismo diseno.

## La acreditacion, y esta vez sin margen

**El negativo de SLIP-1 se acredita por MUTACION**, no por exit code de una corrida: quita la
comprobacion de firma cruzada y el caso debe FALLAR. Es exigencia explicita del checker y la
suscribo -- llevamos tres rondas y las tres veces lo que cayo fue un control que pasaba su propia
prueba.

## La pregunta que quiero contestada ANTES de implementar

**Con la firma cruzada exigida, quien firma la PRIMERA entrada de un actor nuevo, y como se verifica
esa raiz sin caer en el mismo circulo?**

Contestala primero. **Si la respuesta es "otra cadena declarativa", paramos y escalo al operador** --
seria el mismo defecto por tercera vez, y el checker ya avisa de que r4 y r5 son las ultimas
iteraciones antes de escalar.

Sin prisa: la v1.19.1 esta retirada y NOVA espera. Tres rondas nos han ahorrado publicar tres
bypasses distintos.

Gates del hub en 0 antes de commitear -- los TRES en conjuncion: ASCII, validate y encoding -- y
commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-17 02:12 local (UTC+2)
