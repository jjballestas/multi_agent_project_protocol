---
message_id: MSG-20260720-Operador-to-Arquitecto-DIRECTIVA-deadlock-poda-reparto
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Registrar una unidad nueva con intake DoR completo para resolver el deadlock poda-vs-claim con el reparto decidido: (1) el gate de poda AVISA y no bloquea en local, (2) la poda se ejecuta COORDINADA en el checkpoint de higiene del Arquitecto, (3) el CI la exige antes de integrar. Medir y reportar ademas el tiempo real de prune_state --apply, que hoy no tenemos. No arrancar sin GO."
question: "Puedes registrar la unidad con ese reparto y darme el numero de prune_state --apply antes de su GO?"
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-COORD-residuo-staged-realimenta-abortos.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "DECISION del Operador sobre el deadlock poda-vs-claim: mismo reparto que E6-A. El gate de poda pasa a AVISO en local (deja de secuestrar al equipo), la poda se hace COORDINADA en el checkpoint de higiene (arbol quieto, claims liberados, sin pisar nadie) y el CI la exige antes de integrar. Se pide ademas medir prune_state --apply, numero que hoy no existe."
---

# DIRECTIVA - resolver el deadlock poda-vs-claim

## El problema, en una linea

Para commitear hay que podar; podar escribe en `Area_comun/state` y
`Area_comun/mailbox`; esas rutas estan bajo un claim vivo y legitimo. **Nadie commitea.**

Los dos mecanismos son correctos por separado -- higiene obligatoria y claim-como-lock --
y juntos se bloquean. Y las dos condiciones coinciden de forma natural: la poda vence
porque el ledger crece, y hay claims vivos porque hay trabajo en vuelo. Es decir, el
deadlock aparece **justo en los periodos de mas actividad**, cuando bloquear cuesta mas.

Hoy la salida ha sido el bypass declarado con verificacion manual. Bien hecho y bien
documentado -- pero un bypass excepcional es sano y uno rutinario vacia el harness que
acabamos de construir.

## Decision: el mismo reparto que E6-A

**1. El gate de poda AVISA, no bloquea (en local).**

Que la poda este vencida **no es una violacion de correccion**: no hay estado invalido,
no hay drift, no hay nada roto. Es un umbral de higiene. Bloquear todos los commits del
equipo por mantenimiento es desproporcionado, y es literalmente lo que genero el bucle:

```
poda vencida -> alguien poda -> cambios en state sin commitear
  -> el exec siguiente ve "cambio ajeno" y ABORTA (correctamente)
  -> el aborto deja SU residuo staged
  -> el exec siguiente aborta por ese residuo
  -> nadie commitea -> la poda vuelve a vencer
```

**2. La poda se ejecuta COORDINADA, en el checkpoint de higiene del Arquitecto.**

No una barrera ad-hoc cada vez que salta el umbral, sino atada a un momento de quietud
que **ya existe**: en el checkpoint el arbol esta limpio y los claims liberados por
construccion. Menos mensajes, menos oportunidades de que se quemen.

Si hiciera falta una barrera explicita (avisar a los peers de que no arranquen otro exec
hasta que corra la poda), tienes autoridad para ello -- pero teniendola como excepcion,
no como rutina.

**3. El CI la exige antes de integrar.**

Si la coordinacion falla, se detecta donde el committer no alcanza. Mismo reparto que ya
decidimos con E6-A: **hook = primera linea rapida, CI = enforcement duro.**

## Por que esta combinacion y no una sola de las piezas

- Solo el aviso (1): la poda podria no hacerse nunca en local. Esta madrugada
  `cold_start_tokens` subio de 20726 a 21050 mientras todos trabajaban.
- Solo la coordinacion (2): la barrera viaja por el mismo canal que quemo cuatro mensajes
  hoy. Si el aviso se quema, un peer arranca y la poda colisiona igual. Y su fiabilidad
  dependeria de TASK-0272, que aun no existe.
- Con las tres: **si el mensaje de barrera se quema, la consecuencia es que la poda se
  retrasa, no que el equipo se pare.** El fallo pasa de bloqueante a degradado, que es lo
  que quiero de cualquier mecanismo de higiene.

## Lo que pido medir (no lo tenemos)

`prune_state --apply`: **cuanto tarda de verdad.** Lo unico medido es `--check` = 0.612 s.
El numero cambia el diseno: si `--apply` es sub-segundo, la coordinacion es casi gratis;
si esta en decenas de segundos, hay que pensarla mejor. **Quiero el dato antes del GO**,
no despues.

## Alcance y limites

- **No es enmienda a TASK-0272.** 0272 arregla que un mensaje se queme cuando un exec
  aborta; esto arregla **que los abortos se produzcan** por el deadlock. Arreglar solo uno
  deja el bucle medio abierto.
- **No relaja ninguna otra guarda**: claim-como-lock intacto, validate intacto, drift
  intacto. Solo cambia quien bloquea por una tarea de mantenimiento.
- Espejo born-operational y entrada al conjunto adoptable: aplica la leccion de
  `.githooks` -- si no viaja, no es del protocolo.

## Guardas

Reservadas N=6 intactas, fondo intocable (2E35F26E / epoch 1.14.0 / N=500), sin encender
supervised_autonomy ni real_invoker. Nada arranca sin mi GO.

-- Operador
