---
id: MSG-20260814-Arquitecto-to-Operador-PLAN-gate-colaboracion
from: Arquitecto
to: Operador
type: DECISION
task_id: none
status: open
requires_response: false
one_line_summary: Recibida la DECISION del gate de colaboracion -- descompuesta en cuatro tareas gobernadas (0378-0381), Puntos 1 y 3 en ready para publicar ya, Puntos 2 y 4 registrados y coordinados con F2/F3; confirmado por medicion propia que el gate no existe.
context_refs:
  - Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
  - Area_comun/tasks/TASK-0379-el-prompt-no-declara-quien-construye-cada-pendiente.md
  - Area_comun/tasks/TASK-0380-liveness-de-maker-y-checker-como-paso-cero.md
  - Area_comun/tasks/TASK-0381-el-estado-no-distingue-pendiente-de-capacidad-caida.md
---

# PLAN -- DECISION del gate de colaboracion

Recibida. Antes de descomponer, verifique el diagnostico contra el nucleo del hub en vez de heredarlo
del reporte:

    scripts/check_commit_trailers.py    96 lineas   menciones de "claim": 0   lee TASK_INDEX: si
    .githooks/pre-commit               193 lineas   menciones de claim/owner/maker: 0

Confirmado al pie: el gate autoritativo comprueba que el `Task-Id` EXISTE y no comprueba quien puede
trabajar esa tarea. **No es un gate roto: es un gate que no existe**, y la distincion importa porque
un gate roto se arregla y uno inexistente se construye con su prueba de rechazo desde el primer dia.

## Descomposicion

    TASK-0378   Punto 1   claim obligatorio para commitear producto      READY
    TASK-0379   Punto 3   el prompt declara maker por pendiente          READY
    TASK-0380   Punto 2   liveness como paso 0, no watchdog              proposed, coordinado F2/F3
    TASK-0381   Punto 4   capacidad caida != tarea pendiente             proposed, coordinado F2/F3

Los cuatro llevan el criterio 2f dentro del AC, no como nota: **cada control entrega la prueba de que
RECHAZA**. En 0378 va por partida doble -- un AC para el gate autoritativo y otro para el gancho
local, cada uno con sus cuatro casos y su propio exit code --, tal y como pediste que viviera en los
dos ganchos.

El AC4 de 0378 exige que ambos NAZCAN con la derivacion de prefijo de instancia, con los dos casos
acreditados: prefijo vacio (el hub, sin cambio de comportamiento) y prefijo no vacio (modelo 2.A). Si
naciera comparando rutas a pelo repetiria el defecto 1 el dia que alguien instancie.

## La limitacion, escrita donde no se pueda perder

Tu nota obligatoria para la version esta **dentro del `out_of_scope` de TASK-0378**, no en un
recordatorio aparte: el Punto 1 para el incidente reportado, que tenia cero claims, pero por si solo
deja MEDIO ABIERTA la familia maker==checker porque un actor puede auto-clamarse y commitear. Cerrarla
es el Punto 2. Y TASK-0380 lo recoge por el otro lado con un AC dedicado (AC5) que exige acreditar el
caso CONJUNTO -- auto-clamado mas sin checker vivo -- en vez de suponer que dos controles parciales
suman uno completo.

Asi el aviso viaja con las dos tareas y no depende de que alguien lo recuerde al redactar la nota.

## Secuencia, y una constriccion real que declaro

Comparto tu analisis de por que 1 y 3 salen ya: se apoyan en el esquema ACTUAL, los dominios son
disjuntos -- 0378 vigila commits sobre tareas con claim activo, la memoria hibrida enfria tareas
`done` -- y ninguno toca el estado del otro.

Lo que declaro es la cola: **Codex es el unico maker y ahora mismo esta en la tercera vuelta de
TASK-0368**, que es la puerta de F3 y donde el checker acaba de encontrar cinco bloqueantes, uno de
ellos una puerta de CI en rojo introducida por la propia remediacion. Meterle 0378 encima de eso
compraria retraso en las dos, no adelanto en una. Mi plan: **ruteo 0378 en cuanto 0368 salga de su
vuelta actual**, y 0379 detras por ser lint de plantilla y barato.

Si prefieres 0378 por delante de 0368 aunque cueste una vuelta mas en la puerta de F3, dilo y lo
reordeno: es una decision tuya, no mia.

## Entregable

Cambio de nucleo mas nota de version adoptable por `upgrade_instance.py`, con la limitacion del
parrafo anterior declarada explicita. La nota se redacta **cuando el gate este acreditado**, no
antes: escribir la nota de un control que aun no ha dicho que no seria el mismo defecto que el
hallazgo denuncia.

Reportare el cierre en canonico.

-- Arquitecto, 2026-08-14 02:45 local (UTC+2)
