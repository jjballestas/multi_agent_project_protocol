---
id: TASK-0361
title: El gate declarado del harness esta rojo porque su constante es menor que el coste del instrumento que invoca
status: ready
owner: Codex
file: Area_comun/tasks/TASK-0361-el-gate-del-harness-esta-rojo-por-una-constante-menor-que-su-instrumento.md
type: fix
intake:
  type: fix
  goal: "Poner en verde `scripts/test_exec_lease_harness.py` en clon limpio atacando la causa medida, no la cifra. La sonda del negativo mide dos veces con `Get-CimInstance Win32_Process`, que cuesta ~2,2 s por muestra en esta maquina, y el workload de la prueba vive 8 s: el segundo recorrido aterriza cuando el hijo ya ha muerto, el mapa acarreado se devuelve intacto y el delta sale cero. El gate es el instrumento de verificacion declarado por DOCE tareas y por el workflow de CI, asi que su rojo se propaga a toda la familia del harness."
  acceptance:
    - "AC1 (falsacion previa): se reproduce el rojo en clon limpio y se acredita la causa por MEDICION, no por inferencia: coste real por muestra del recorrido CIM en la maquina que corre, y el instante de muerte del hijo comparado con el instante de la segunda muestra. Con la unica variable de la vida del workload cambiada, el test pasa."
    - "AC2 (la vida se DERIVA del coste observado, no se sube hasta que cuadre): la duracion del workload de la sonda se calcula a partir del coste medido del instrumento en tiempo de ejecucion, con margen declarado. Subir la constante 8 -> 30 hasta que pase NO satisface este AC: eso ata la prueba a la velocidad de una maquina concreta y volvera a romperse en otra."
    - "AC3 (se acredita que se midio lo que se dice medir): la sonda afirma explicitamente que el hijo seguia VIVO en el momento de la segunda muestra. Si no lo estaba, el caso falla con un diagnostico que lo diga, en vez de devolver un delta cero indistinguible de -no progresa-."
    - "AC4 (el runner no oculta el resto): hoy el runner aborta en la primera asercion fallida (`healthy_busy` :1247) y los tests posteriores ni se ejecutan. Tras el cambio, un fallo de un caso no impide ejecutar y reportar los demas, o se declara por escrito por que no puede ser asi."
    - "AC5 (verde estable, no verde por suerte): `python scripts/test_exec_lease_harness.py` sale EXIT=0 en clon limpio en TRES corridas consecutivas, y se reporta el numero de casos ejecutados en cada una. Un verde de una sola corrida no acredita un fallo que se manifestaba 2 de 2 y 5 de 5."
    - "AC6 (sin regresion de cobertura): los casos que hoy SI pasan siguen pasando, y ninguno queda desactivado o relajado para conseguir el verde."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/test_exec_lease_harness.py
  out_of_scope:
    - "AC5 de TASK-0359 (el negativo permanente debe morir con el mutante que deja el muestreo inalcanzable): es una propiedad del CONTRATO, no del arnes, y se queda en la vuelta 2 de 0359."
    - "El residual R6 de 0359 (la clave del mapa de CPU debe ser pid + process_start_time_utc): tambien vuelta 2 de 0359."
    - "Acreditar nada en un run REAL de Actions: la facturacion sigue bloqueada y es decision del operador."
  risk: medium
  estimate: S
---

# TASK-0361 -- el gate esta rojo por una constante menor que su instrumento

Sale del veredicto r2 de TASK-0359. El checker lo midio en clon limpio, **dos corridas completas, dos
rojos**, en aserciones distintas del mismo test (`healthy_busy` :1247 y `retiring_child` :1250), con
la sonda devolviendo `delta_ticks = 0` exacto **5 de 5**.

## La causa, medida y no inferida

    Get-CimInstance Win32_Process   ~2,2 s por muestra en esta maquina
    la sonda la paga               2 veces
    vida del workload de la prueba  8 s
    -> el Get-Process del segundo recorrido aterriza DESPUES de que el hijo ha muerto
    -> se devuelve el mapa acarreado intacto -> delta cero -> "no progresa"

Cambiando **la unica variable** vida del workload 8 s -> 30 s, pasa 2 de 2.

## Por que no basta con subir el 8 a 30

Porque el 30 tambien es un numero. Ata la prueba a la velocidad de esta maquina y volvera a romperse
en la primera que sea mas lenta, o cuando el arbol de procesos crezca y el recorrido CIM cueste mas.
**La vida del workload tiene que derivarse del coste observado del instrumento**, que es justo lo que
la prueba puede medir antes de usarlo.

Es la tercera vez en la misma jornada que el defecto es una cifra donde deberia haber un criterio:
el AC2 de 0359 prometia 70 minutos donde el techo real eran 75, y el contrato de 0354 comparaba
contra un literal 73. Aqui la cifra esta dentro del arnes de pruebas, que es el sitio donde menos se
mira.

## Por que es urgente y va aparte

`scripts/test_exec_lease_harness.py` es el comando de verificacion declarado por **doce** tareas de la
familia del harness -- varias de ellas ya cerradas -- y esta en `.github/workflows/validate.yml`.
Mientras este rojo, ninguna de ellas puede acreditarse en limpio, y la vuelta 2 de TASK-0359 tampoco:
no se puede juzgar un negativo dentro de un arnes roto.
