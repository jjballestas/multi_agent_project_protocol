---
task_id: TASK-0335
file: Area_comun/tasks/TASK-0335-asercion-acoplada-al-formato-del-log.md
title: "Sexto rojo de la suite revivida: la asercion busca una subcadena exacta del log y TASK-0321 metio campos nuevos en medio -- el estado terminal esta, el emparejamiento textual no"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0330
  - TASK-0321
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    Sexto rojo declarado en la particion de TASK-0330, con diagnostico completo del maker y sin
    aplicar por orden mia. `run_unreadable_head_case` en
    `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` busca una subcadena EXACTA que coloca
    `signal=watchdog` inmediatamente detras de `attempts=0`. Produccion emite hoy `elapsed_seconds`
    y `timeout_seconds` entre esos dos campos, cambio introducido por TASK-0321.
    **El estado terminal SI aparece en el log**; lo que falla es el emparejamiento textual. No hay
    defecto de produccion.
    Urge porque TASK-0330 dejo los tres runners cableados en CI -- que es su valor -- y esta unica
    asercion mantiene el paso en rojo, y con el la integracion.
    Es la quinta aparicion en un dia de la misma familia: una asercion atada a una FORMA (posicion
    de una subcadena) en vez de a la PROPIEDAD (se alcanzo el estado terminal). Como en 0324, 0325,
    el tercer rojo de 0330 y el cuarto.
  acceptance:
    - "AC1 (falsacion previa): se reproduce que el estado terminal SI se alcanza y aparece en el log, y que lo unico que falla es el emparejamiento de subcadena. Evidencia por comportamiento con la linea real."
    - "AC2 (afirmar la PROPIEDAD, no la forma): la asercion pasa a comprobar que se alcanzo el estado terminal por la causa esperada, con independencia de que campos intermedios emita el log y en que orden. Un cambio futuro de formato que conserve la semantica NO debe romperla."
    - "AC3 (sigue siendo falsable): la asercion debe SEGUIR cayendo si el estado terminal no se alcanza o se alcanza por otra causa. Verificado por mutacion en las dos direcciones -- no basta con que deje de fallar."
    - "AC4 (sin relajar): no se marca el caso como skip, no se debilita ninguna otra asercion del fixture y no se toca produccion."
    - "AC5 (CI verde): tras el arreglo, run_mailbox_retry_cases.py exit 0 y el paso de CI que TASK-0330 cableo pasa a verde. Se declara el recuento final de contratos ejecutados."
    - "AC6 (sin regresion): suites del harness, inventario de contratos y gates del repo exit 0 en clon limpio."
    - "AC7 (AMPLIADO 2026-08-07, punto 4 del veredicto de 0330): el inventario de rojos del runner de retry estaba INCOMPLETO. Se exploran y declaran TODOS los rojos restantes -- el 7o, 8o y 9o quedaron sin declarar y la cola posterior a la linea 1390 sin explorar. Esta tarea NO cierra sobre la premisa de que el sexto era el ultimo."
    - "AC8 (AMPLIADO 2026-08-07, punto 5 del veredicto de 0330): `retry-ledger-head-defer-order` NO se ejecuta hoy -- la linea 785 revienta antes de llegar a la 802 -- y su mitad mutante es VACUA porque `terminal_line` es una subcadena que ningun log de produccion satisface, de modo que `expect_terminal=False` pasaria hiciera lo que hiciera produccion. Al reparar la asercion del sexto rojo, ese negativo debe quedar ALCANZABLE y verificado por mutacion en las dos direcciones, dentro de este alcance y no despues."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  out_of_scope: >
    No se toca produccion: el formato de log actual es correcto y es el que TASK-0321 dejo. No se
    tocan los otros fixtures ya reparados en TASK-0330. No se reabre TASK-0330, que cerro su nucleo
    correctamente.
  risk: low
  estimate: S
---

# TASK-0335 -- la asercion mira la forma del log, no lo que el log dice

## De donde sale

Particion explicita de TASK-0330 al sexto rojo, ejecutada por el maker segun la regla que fije: si
aparece un sexto, entregar el nucleo, inventariar lo pendiente y **no silenciar nada**. Lo hizo, y
este es el pendiente, con el diagnostico ya completo.

## Por que es urgente pese a ser una asercion

TASK-0330 dejo los tres runners dormidos cableados en CI -- 47 negativos permanentes que pasan de
declarados a EJECUTADOS. Ese es su valor y esta entregado. Pero esta unica asercion obsoleta
mantiene ese paso en rojo, asi que hoy la integracion esta bloqueada por un emparejamiento textual,
no por un defecto.

Dejar el rojo visible fue la decision correcta -- esconderlo habria reproducido el problema que 0330
existe para erradicar. Arreglarlo rapido es la consecuencia de esa decision, no una excepcion a ella.

## Quinta aparicion de la misma familia en un dia

    0324   el contrato ataba el HELPER, no el efecto
    0325   el detector nombraba `continue`, no la propiedad "salida temprana"
    0330#3 el checker exigia el literal `$expires -gt $now`
    0330#4 el fixture asumia un mundo sin `work_scope` obligatorio
    0335   la asercion exige una POSICION de subcadena en el log

Y el patron secundario tambien se repite: **quien rompio esta asercion fue TASK-0321**, otra tarea
nuestra, con un cambio correcto. Tres de los seis rojos de la suite revivida los causamos nosotros.

Por eso el AC2 no pide actualizar la subcadena: pide que la asercion compruebe **que se alcanzo el
estado terminal por la causa esperada**, para que el siguiente cambio de formato no la vuelva a
romper. Y el AC3 exige que siga cayendo cuando debe -- una asercion que deja de fallar no esta
arreglada, esta apagada.

## Ampliacion 2026-08-07 tras el veredicto de TASK-0330

Esta tarea se contrato sobre el inventario del maker dando por hecho que el sexto rojo era el
ultimo. **No lo era**: el checker encontro un septimo, octavo y noveno sin declarar, y la cola del
runner posterior a la linea 1390 sin explorar. El error de encuadre es del Arquitecto -- tomo un
inventario ajeno sin verificar que estuviera cerrado, que es la misma clase de fallo que este hilo
lleva todo el dia corrigiendo: aceptar una afirmacion util sin falsarla.

Entra ademas el residual del foco E: el negativo que protege el arreglo de ORDEN de produccion
autorizado en 0330 es hoy **codigo muerto con una mitad vacua**. Repararlo pertenece aqui porque
depende de la misma subcadena obsoleta; dejarlo para despues seria cerrar 0330 con su unica
ampliacion de produccion sin guardian real.
