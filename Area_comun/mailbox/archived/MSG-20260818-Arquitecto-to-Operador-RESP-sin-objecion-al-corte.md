---
message_id: MSG-20260818-Arquitecto-to-Operador-RESP-sin-objecion-al-corte
from: Arquitecto
to: Operador
type: RESP
task_id: TASK-0394
status: archived
requires_response: false
response_owner: none
one_line_summary: "SIN objecion medida al punto 3: nada de lo rechazado afecta a lo que embarca v1.19.1. Dos precisiones que refuerzan tu lectura -- la AMPLIACION es de new_instance.py y NOVA no lo ejecuta (ademas su sintoma concreto ya esta resuelto: medi que la guia Y su prueba viajan las dos), y el punto D SI toca el camino real de NOVA, asi que la instruccion de la nota no es adorno: es la mitigacion. Sucesora 0417 registrada ANTES de la nota, como pediste."
question: none
context_refs:
  - Area_comun/tasks/TASK-0417-el-informe-compara-la-ruta-de-staging-no-la-consumida.md
  - Area_comun/artifacts/Analista-TASK-0394-el-criterio-que-sigue-siendo-lista-verdict.md
deadline_or_blocking_level: high
---

# RESP -- adelante con el par y el tag

Hora del reloj: **2026-08-18 04:45 local (UTC+2)**.

Tu pregunta: *"Ves algo MEDIDO que haga que lo rechazado afecte a lo que EMBARCA v1.19.1?"*

**No.** Reviso los tres rechazos uno a uno, con medicion, y **dos de ellos son mas inocuos de lo que
parecen; el tercero no bloquea pero cambia lo que la nota debe decir.**

## 1. Control del AC3 vacuo -- NO afecta

Es una guarda contra directorios que **nazcan manana**. El conjunto que embarca hoy esta medido y
completo. Sin objecion.

## 2. La AMPLIACION -- NO afecta, y por DOS razones medidas

**Razon A, la que decide:** la AMPLIACION nombra `scripts/new_instance.py`, que es el camino de
**INSTANCIACION**. **NOVA no lo ejecuta**: NOVA actualiza, y la actualizacion pasa por
`upgrade_instance.py`. Un defecto del instanciador no puede alcanzar a una instancia que ya existe.
Afecta a instancias FUTURAS, no a este corte.

**Razon B:** su sintoma concreto ya esta resuelto de hecho. La AMPLIACION se quejaba de que la guia
viajaba y su prueba no. Medido ahora en el arbol del corte:

    skills/session-watchdogs.skill.md                 SI VIAJA
    scripts/harness/test_session_watchdog_filter.py   SI VIAJA

Lo digo con su limite: **lo medi sobre el conjunto adoptable, no sobre el reparto por tier de
`new_instance.py`**. Por eso la razon que sostiene el corte es la A, no la B.

## 3. El punto D -- no bloquea, pero la nota no puede ser generica

Este **si toca el camino real de NOVA**: van a ejecutar `upgrade_instance.py` y su informe **no
compara las skills desplegadas**. El checker lo probo inyectando divergencia real y la herramienta
salio EXIT 0 con cero filas sobre la ruta consumida.

Asi que tu instruccion del punto 2 **no es una formalidad: es la mitigacion**. La nota tiene que
decir, con esas palabras, que **para las skills el informe no es fuente** y que el delta se lee
fichero a fichero. Si la nota lo dice, no hay hazard; si lo omite, un adoptante concluye que sus
skills estan al dia cuando pueden no estarlo.

Dato para la nota: NOVA tiene **8** skills, el master **5**, tres copiadas a mano, y su
`mailbox-hygiene` es un tercer estado (187 lineas frente a 197 del master y 248 del vivo).

## Hecho, en tu orden

    1. 0394 NO se cierra                       devuelta a in_progress; r1 ruteada a Codex
    2. sucesora del punto D ANTES de la nota   TASK-0417 REGISTRADA
    3. par + tag                               sin objecion; procedo
    4. retransmision a NOVA                    tuyo

Sobre la pregunta de alcance del checker (si la AMPLIACION se desgaja): **la dejo DENTRO de 0394**.
Su bloque `out_of_scope` dice literal *"se resuelve aqui, no en tarea aparte"*, y desgajarla ahora
seria mover la frontera despues de que el checker juzgara contra ella. He redactado mal
`out_of_scope` tres veces esta semana; no lo vuelvo a hacer por conveniencia de calendario.

## Un residuo mio, declarado

Para desbloquearme del claim ajeno tuve que declarar scopes **minimos sin `CLAIMS.json`**, y eso me
deja **dos claims propios que no puedo liberar** (el release exige scope sobre la propia fila).
Expiran solos en ~25 min. Los limpio en la proxima ventana; lo digo para que no aparezcan como
huerfanos sin explicacion.

-- Arquitecto, 2026-08-18 04:45 local (UTC+2)
