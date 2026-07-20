---
message_id: MSG-20260720-Arquitecto-to-Operador-ACK-tres-decisiones
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
requested_action: "Ninguna. Registro por el canal gobernado tus tres decisiones del 2026-07-20 sobre el reporte de estado de la tanda 0103 y lo que ya se ejecuto de cada una."
question: "Sin pregunta abierta."
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
  - Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
one_line_summary: "Registradas tus tres decisiones: crons relanzados con el harness de 0272 ya desplegado, GO a TASK-0277, y ventana N=6 CONGELADA (con la propagacion de 0266 hacia NOVA parada por la misma razon)."
---

# FYI - registro de las tres decisiones del Operador

Hora local: 2026-07-20 16:50. Registro por el canal gobernado lo que decidiste sobre el
reporte de estado, y el estado de ejecucion de cada punto.

## 1. Crons parados y relanzados -- HECHO

Ambos loops corrian codigo cargado en memoria desde antes del fix, el de Codex desde el
19-jul a las 19:49. Espere a que cerrara el exec que tenia en vuelo (no se mata trabajo
vivo), hice teardown de los dos, limpie lock y lease huerfanos y relance una sola
instancia de cada uno a las 16:43:26. Codex pid 60260, Analista pid 62440.

**Evidencia de que el harness nuevo esta en vigor:** el primer exec bajo el codigo nuevo
cerro con `code=0 outcome=definitive`, un contrato de salida explicito que el codigo viejo
no emitia. TASK-0272 quedo ademas en `done` (evento seq 5353) justo antes del relanzamiento.

## 2. GO a TASK-0277 -- RUTEADA

Promovida a `ready` y ruteada a Codex. Ademas de recomponer la fila de TASK-0267 desde el
event log, la unidad cierra los dos huecos de clase: el validador pasa a cruzar los
ficheros de tareas contra las filas de indice, y el chequeo de deriva pasa a cubrir los
archivos de poda. Sin eso, otra unidad puede evaporarse con todos los gates en verde.

Restriccion que le puse por escrito: la reparacion RECONSTRUYE la fila derivada, no toca
ni re-firma eventos. El ledger esta intacto y es la fuente.

## 3. Ventana N=6 -- CONGELADA

Anotado, el build-open no arranca. Consecuencia que aplico sin pedirtela: **la propagacion
de TASK-0266 hacia NOVA queda igualmente parada**, por el mismo motivo por el que la
senale al pedirte el GO, no se cambia el entorno sellado a mitad de ventana preregistrada.
La unidad 0266 sigue en `ready` dentro del hub; lo congelado es su exportacion.

## Estado tras estas tres

Nueve unidades en `done` (0257, 0258, 0267, 0268, 0269, 0270, 0271, 0272, 0273). En cola,
0259 a 0264 mas 0266, el gate final 0265, y las cuatro nacidas de los juicios (0274, 0275,
0276 y la ya ruteada 0277). La cola del nucleo 0103 sigue parada por decision mia mientras
se cierran las unidades de harness, que son las que hacen fiable todo lo demas.
