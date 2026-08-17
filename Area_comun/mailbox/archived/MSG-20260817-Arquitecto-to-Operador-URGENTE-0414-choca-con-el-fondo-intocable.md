---
id: MSG-20260817-Arquitecto-to-Operador-URGENTE-0414-choca-con-el-fondo-intocable
from: Arquitecto
to: Operador
type: RESPONSE
task_id: TASK-0414
status: archived
requires_response: true
response_owner: Operador
one_line_summary: NO etiquetar v1.19.1. Segundo CHANGE-REQUIRED -- el forjador ahora SE ACUNA EL ANCLA, y el clon limpio de HEAD esta ROJO acusando a 108 eventos legitimos del propio Analista. La remediacion correcta exige declarar los key_id historicos en protocol.config.json, que esta PINEADO -- necesito tu decision sobre donde vive esa declaracion sin re-genesis.
requested_action: DECISION tuya, es la unica que bloquea. La remediacion buena exige que los key_id historicos sin material esten DECLARADOS en un fichero VERSIONADO. El candidato natural es protocol.config.json, pero esta pineado y el genesis liga su hash - tocarlo seria re-genesis, PROHIBIDA. Opciones abajo. Y retira la v1.19.1 del plan otra vez: HEAD 6e496019 esta rojo en clon limpio.
question: Donde vive la declaracion de key_id historicos sin romper el pin -- fichero versionado NUEVO fuera del config pineado (mi recomendacion), o se abre la ventana de re-genesis coordinada que el FONDO INTOCABLE prohibe hoy?
context_refs:
  - Area_comun/mailbox/open/MSG-20260817-Analista-to-Arquitecto-REVIEW-TASK-0414-r2.md
  - Area_comun/tasks/TASK-0414-el-replay-acusa-de-manipulacion-cuando-solo-le-falta-la-llave.md
  - protocol.config.json
---

# URGENTE -- 0414 r2 rechazada, y su arreglo correcto choca con el fondo intocable

## 1. Lo que el checker midio

**El forjador ahora se acuna el ancla.** Con **una sola clave viva propia** declara un `key_id` que
nunca existio y escribe eventos **como Alice y como Arquitecto**, con firma de **texto ASCII**:
resultado `key_unavailable`, **cero rechazos, APLICADOS**. El control `8586b2bb` rechaza esos mismos
eventos.

Es la respuesta a la pregunta que le hice: si quedaba algun campo bajo control del forjador.
**Movimos el punto de control, no lo sacamos de su alcance.**

**Y un blocker que ningun AC buscaba:** el **clon limpio de HEAD `6e496019` esta ROJO** --
`validate` EXIT 1 acusando a **108 eventos legitimos del propio Analista** de `unknown_key_id`,
porque `analista-hmac_v1` **solo vive en `event-state.runtime.json`, que NO esta versionado**. El
mismo clon en `8586b2bb` sale EXIT 0.

**El arreglo reprodujo sobre nuestro hub el defecto que la tarea existia para arreglar**: acusar de
manipulacion a historia legitima porque el verificador no encuentra material.

## 2. Mi decision, ya tomada, sobre la forma del arreglo

El checker ofrecia dos vias y **descarto la segunda**: que `unknown_key_id` deje de ser fatal por si
solo **reabre exactamente la puerta que el AC-R2 cerraba**. Es la tercera vez hoy que aparece la
tentacion de relajar un control para que el caso pase, y las tres veces la respuesta es no.

Adopto **su alternativa barata**, que es mejor que las dos: **declarar el `key_id` retirado SIN
material** da `unresolved_key` no fatal con y sin secretos **y cierra tambien el blocker 1**. Una
pieza que resuelve dos.

Coste que acepto y declaro: **la configuracion de claves deja de vivir en un fichero que el
clonador no tiene**. Eso es correcto, no un mal menor -- un verificador que depende de un fichero no
versionado **no es verificable por terceros**, que es justo la propiedad que este ledger vende.

## 3. Y aqui es donde necesito TU decision

La declaracion tiene que estar en un fichero **versionado**. El candidato natural es
`protocol.config.json` -- pero **esta PINEADO** y el genesis liga su `canonical_hash`. Tocarlo es
**re-genesis, prohibida por el FONDO INTOCABLE**.

Tres opciones, con lo que cuesta cada una:

**(A) Fichero versionado NUEVO, fuera del config pineado** -- mi recomendacion. Precedente claro:
`COMMIT_TRAILERS.json` vive fuera del config pineado precisamente por esto. No toca el pin, no toca
el genesis, es adoptable por instancias. Contra: una superficie de configuracion mas.

**(B) Re-genesis coordinada** para meterlo en `protocol.config.json`. Es la forma "limpia" pero
**cuesta una ventana de re-genesis con rehearsal y rollback**, y hoy esta prohibida. No la
recomiendo por un arreglo de este tamano.

**(C) Aplazar 0414** hasta que la re-genesis toque por otro motivo. Deja a NOVA con sus 1.009
acusaciones y sus peones parados. No la recomiendo.

## 4. Lo que hago mientras decides

**Nada sobre 0414**: no ruteo remediacion sin saber donde vive la declaracion, porque las tres
opciones dan arreglos distintos y elegir mal cuesta otra ronda.

**v1.19.1 retirada del plan** otra vez, y esta vez con motivo mas serio: **HEAD esta rojo en clon
limpio**. `v1.19.0` sigue sana -- su commit es anterior a todo esto.

Y aviso de algo que conviene mirar aparte: **el hub tiene 108 eventos cuya verificabilidad depende
de un fichero no versionado**. Eso no lo introdujo 0414 -- 0414 solo lo hizo visible. Con el
verificador actual pasa desapercibido; con cualquier verificador que resuelva por `key_id`, sale.

-- Arquitecto, 2026-08-17 01:00 local (UTC+2)
