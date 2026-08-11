---
id: MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0359-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0359
status: open
created: 2026-08-11T21:52:28Z
requires_response: true
response_owner: Analista
one_line_summary: Vuelta 2 de 2 de TASK-0359 -- el negativo deberia morir ya con el mutante que deja el muestreo de produccion INALCANZABLE, aseverando el desenlace del bucle real, y la clave del mapa de CPU deberia distinguir un PID reciclado.
requested_action: Revisa la implementacion exacta ec0b93ce contra los tres puntos que quedaban. Sin producto en alcance (no gatees npm test). Clona con historia completa.
question: El negativo distingue el arbol sano del mutante de :1565, o sigue devolviendo lo mismo en los dos casos?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0359-r2-liveness-monotona-verdict.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/test_exec_lease_harness.py
---

# REVIEW TASK-0359 r3 -- vuelta 2 de 2

Implementacion exacta `ec0b93ce`. **Sin producto en alcance.** El arnes de TASK-0361 ya esta
verde y ratificado, asi que esta vez puedes acreditar dentro de el.

## Lo que ya firmaste y no hay que volver a medir

Monotonia **PASS**, techo **PASS**, colgado por su clase **PASS** (6 de 6, tres clases). El delta
minimo y la captura del instante antes del muestreo se quedan como estan.

## Los tres puntos de esta vuelta

1. **AC5 -- el mutante correcto.** El negativo debe morir con el que deja el bloque de muestreo de
   produccion **INALCANZABLE** (`:1565`, `if ($false)`, una linea). En r2 el negativo devolvia
   `progressing=True` **identico** sobre el arbol sano y sobre el mutante, 2 de 2: no media la
   propiedad, pasaba.
2. **La asercion sobre el desenlace.** Debe ser *muere / no muere* del bucle real, no el booleano
   `progressing` del helper. Va ligado al punto 1: si el negativo ejecuta el bucle, el desenlace es
   observable.
3. **R6 -- PID reciclado.** La clave del mapa `pid -> maximo` debe distinguir un PID reutilizado
   (`pid + process_start_time_utc`, como ya hace el resto del harness). Tu mecanismo probado:
   sembrando una entrada inflada, dos ventanas seguidas declaran "no progresa" sobre un proceso que
   quema CPU al 100%.

## El liston que tu misma pusiste en 0361

**Un verde que el codigo anterior tambien produce no acredita nada.** Alli corriste el PRE-FIX bajo
el mismo arnes -- tambien pasaba -- y solo firmaste cuando pusiste ambas versiones bajo el mismo
instrumento encarecido. Aqui el control equivalente es directo: **el negativo de antes y el de ahora,
los dos contra el mutante de `:1565`**. Si el nuevo tampoco lo distingue, da igual cuantos casos
pasen.

## Presupuesto

**Vuelta 2 de 2.** Si sigue abierta, escalo al operador -- no pido una tercera.

## Lo que declara el maker (verificalo, no lo aceptes)

- El mutante exacto **muere por desenlace**: el arbol sano ejecuta el bucle real de supervision con un
  hijo que quema CPU en silencio, emite `EXEC_PROGRESSING` y **no llama a la ruta de kill** en el
  primer deadline; sustituyendo el guard de muestreo por `if ($false)` bajo el mismo instrumento
  medido, no emite progreso, llega a `EXEC_HUNG reason=no_progress` y llama a la ruta de kill una vez.
  Dice que las aserciones observan *sobrevive / muere*, no el booleano del helper.
- **R6 cerrado** clavando la clave a `pid|process_start_time_utc`, con negativo permanente que siembra
  maximos inflados para el PID numerico reutilizado y una identidad vieja.
- Worktree limpio con historia completa: arnes **31/31**, contratos **74/74**, retry cases PASS,
  validador, encoding y las dos neutralidades en EXIT=0.

El inventario de contratos paso de 73 a 74: hay un negativo nuevo. Mira que sea el que dice ser.
