---
id: TASK-0381
title: El estado no distingue una tarea pendiente de una capacidad caida, y las dos ocupan la misma linea del tablero
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0381-el-estado-no-distingue-pendiente-de-capacidad-caida.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Punto 4 de la DECISION del Operador del 2026-08-14. Cuando un maker o un checker no arrancan, eso
    aparece en el tablero como una linea mas junto a "archivar mensajes" o "promover la siguiente
    tarea". Son cosas de naturaleza distinta: una tarea pendiente espera a que alguien la haga; una
    capacidad caida RESTRINGE lo que la sesion entera puede hacer, y su prioridad no se negocia contra
    el resto de la lista. Mezclarlas hace que la caida compita por atencion con trabajo ordinario y
    pierda, que es exactamente lo que ocurre cuando la carga sube -- el momento en el que la caida
    importa mas.
  acceptance:
    - "AC1 (dos cosas distintas, representadas distinto): el estado distingue `tarea pendiente` de
      `capacidad caida` de forma estructural, no por convencion de redaccion. Un lector -- humano o
      agente -- puede responder `que capacidades estan caidas` sin leer la lista de pendientes."
    - "AC2 (la caida restringe, no solo informa): mientras una capacidad este caida, el estado declara
      QUE deja de poderse hacer. Se acredita con el par: con la capacidad caida lo restringido muere,
      y con ella viva pasa. Sin esa mitad es una etiqueta bonita."
    - "AC3 (derivado, no declarado a mano): el estado de capacidad sale de la misma senal de conducta
      que use TASK-0380, no de que alguien se acuerde de escribir una linea. Un tablero que hay que
      actualizar a mano miente el dia que nadie lo actualiza -- que es el dia en que la capacidad se
      cae."
    - "AC4 (medido sobre una caida REAL): se acredita provocando la caida de un peon y observando el
      tablero antes y despues. Esta instancia ha tenido caidas de sobra hoy mismo como para no
      necesitar inventarse una."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - Area_comun/state/
    - scripts/
  out_of_scope:
    - "La liveness como paso 0 del cold-start: es TASK-0380, y esta tarea consume su senal en vez de
      inventarse otra."
    - "El claim obligatorio para commitear producto: es TASK-0378."
  risk: low
  estimate: M
---

# TASK-0381 -- una caida no es un pendiente

## Por que importa el sitio donde se representa

Una lista de pendientes se prioriza. Una capacidad caida no compite: cambia lo que se puede hacer.
Cuando las dos comparten formato, la caida entra en la cola y pierde contra lo urgente -- y pierde
justo cuando la carga es alta, que es cuando caerse cuesta mas.

## La condicion que evita que sea cosmetico

El AC3. Si el estado de capacidad se escribe a mano, sera correcto mientras alguien se acuerde, y
dejara de serlo el dia que la capacidad se caiga de verdad y nadie este mirando. Por eso consume la
senal de conducta de TASK-0380 en vez de fabricar la suya.

## Por que se coordina con F2/F3

Como el Punto 2: no por el esquema, que esta congelado, sino porque toca la semantica de estado que
F2/F3 reescriben. Publicar antes obliga a tocarlo dos veces.
