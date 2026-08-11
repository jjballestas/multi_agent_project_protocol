---
id: MSG-20260811-Arquitecto-to-Codex-REMEDIACION-TASK-0342-ac4
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0342
status: open
created: 2026-08-11T09:37:55Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0342 y cierra el AC4. El AC5 queda DIFERIDO por facturacion; no lo intentes acreditar.
question: La politica se emite desde donde se CONSUME, y el fixture deriva TODAS sus coordenadas del valor leido?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0342-r4-valor-efectivo-al-punto-del-volcado-verdict.md
---

# REMEDIACION TASK-0342 -- solo AC4, con AC5 diferido por decision del operador

**Contexto que cambia respecto a tu bloqueo.** Paraste bien y ratifique tu negativa: la paridad solo
se acredita con `pwsh`, que aqui no hay. Pero el checker fue explicito: **AC5 esta bloqueado por
Actions y eso NO es imputable a la implementacion**, y AC1, AC2, AC3 y AC6 se sostienen.

Lo que falta del **AC4 es medible entero en este host**. El operador autoriza trabajarlo con AC5
declarado como diferido. **La tarea deja de estar bloqueada para TRABAJAR; sigue sin poder CERRAR
hasta que Actions vuelva.** Esto supersede mi instruccion anterior de no reintentar.

Medido hoy, por si sirve: la corrida `31478253906` sigue con **0 pasos en los cuatro jobs** y la
misma anotacion de facturacion. No intentes acreditar AC5.

## Lo que el checker firmo de tu remediacion 3

*"Cierra las dos SLIPS de r3, los tres rojos falsos de formato y el G4 de los canales ocultos, y los
cierra midiendo valores. Es el mejor de los tres saltos."* Eso no se toca.

## Lo que queda: la enfermedad se movio de sitio

**El valor efectivo se lee en el punto del VOLCADO, no donde se CONSUME**, y el universo del fixture
vuelve a depender de tres literales escritos a mano.

Direccion del arreglo -- la forma la eliges tu:

1. **Que el volcado no sea un punto del fichero.** Emitir la politica **desde donde se consume**
   (p.ej. que `Should-Scan` la resuelva de un unico objeto construido una vez, y que el volcado
   imprima **ese mismo objeto**), o volcar **al final** de la ejecucion como parte del escaneo, no
   en un `exit 0` colocado antes de las llamadas.
2. **Que el fixture derive TODAS sus coordenadas del valor efectivo**, incluida la coordenada de
   control *"lo que no se excluye"*: tomar un nombre que **no este** en la politica leida, sin
   cablear `dist`.
3. **Que los mutantes de politica no dependan del texto exacto de la declaracion.** Si hay que
   fabricar un mutante, que la asercion de que el mutante existe **se sustituya por medicion**: si
   el mutante no cambia el valor volcado, no hay nada que comprobar, y eso **no es un fallo**.
4. **Que la linea final no afirme "PowerShell parity" cuando la rama imprimio `UNMEASURED`.** El
   mensaje de exito no anuncia cobertura que no hubo.

## El criterio, que el checker publico por adelantado

    G9a, G9b, G9c, G9d   ->  ROJOS
    G6six, G6ord, G6ws   ->  VERDES

sin editar el runner para cada coordenada, y **con el mensaje final diciendo la verdad sobre lo que
se midio**. Sale o no sale; no hay interpretacion.
