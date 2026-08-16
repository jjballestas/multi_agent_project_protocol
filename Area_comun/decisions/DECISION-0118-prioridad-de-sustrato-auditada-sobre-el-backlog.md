---
decision_id: DECISION-0118
title: Los fixes del sustrato de coordinacion tienen prioridad de ruteo, y la etiqueta se audita sobre el BACKLOG, no sobre lo ruteado
status: accepted
date: 2026-08-16
author: Arquitecto
approved_by: operador humano
supersedes: []
superseded_by: []
related:
  - TASK-0337
  - TASK-0407
  - TASK-0408
  - TASK-0411
  - personal/Analista/drafts/PROPUESTA-20260816-eficiencia-coordinacion-v3-FINAL.md
---

# DECISION-0118 -- el sustrato salta la cola, y su etiqueta se audita donde puede esconderse

## Que se decide

**1.** Una tarea cuyo objeto es el **sustrato de coordinacion** --guards, retry, watchdogs,
timeouts, locks, scope de claims, arnes de crons-- tiene **prioridad de ruteo** sobre tareas de
producto de igual urgencia.

**2. La etiqueta `sustrato` la audita el checker sobre el BACKLOG (`proposed` + `ready`), NO sobre lo
ruteado.** Esta es la parte que hace la regla falsable, y sale de un ataque de gaming a la version
previa: si solo se audita lo ruteado, **una tarea de sustrato que nunca se rutea nunca se impugna**
-- y el punto ciego es exactamente la poblacion que la regla pretende proteger.

## Por que: un bug de sustrato grava TODAS las tareas posteriores

Medido el 2026-08-16, en una sola jornada del hub:

- El guard de residuo ciego al scope **bloqueo en bucle el propio mensaje que lo cerraria**, tres
  veces, y una de ellas **agoto un encargo entero** (`RETRY_EXHAUSTED attempts=3`), dejando el
  trabajo del maker varado sin commitear.
- El scope grueso de claims me bloqueo **TRES escrituras legitimas** -- dos podas y el alta de una
  tarea. El alta solo entro **retirando** una ruta de mi scope, es decir esquivando el conflicto.
- La instancia NOVA midio **137 aplazamientos `worktree_residue_live` en un solo dia** entre su
  maker y su checker, con su coordinador haciendo de desatascador manual.

Ninguna de esas perdidas aparece imputada a la tarea que las sufrio. Por eso el sustrato no compite
con el producto en igualdad: **lo grava**.

## AC de la propia DECISION

Durante el proximo mes, **ninguna tarea etiquetada como sustrato espera mas de 72 h en
`proposed`/`ready`** mientras se rutean tareas de producto no urgentes. Se mide sobre el backlog.

Y el control cruzado, para que la regla no se convierta en una etiqueta comoda: **el checker puede
impugnar la etiqueta**, y una impugnacion aceptada cuenta como anomalia DECISION-0018 contra quien
la puso -- que soy yo, porque la asigno el Arquitecto en el intake.

## Lo que NO se decide aqui

Que sea el sustrato quien decida el orden entre sus propias tareas: eso sigue siendo criterio de
coordinacion caso a caso. Y no se altera la regla de promocion de una en una (DECISION-0020 #7) ni
el cap de 3-4 encargos por peer.
