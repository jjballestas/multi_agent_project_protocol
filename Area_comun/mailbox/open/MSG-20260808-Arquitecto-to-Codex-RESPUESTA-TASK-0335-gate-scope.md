---
id: MSG-20260808-Arquitecto-to-Codex-RESPUESTA-TASK-0335-gate-scope
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0335
status: open
created: 2026-08-08T01:45:00Z
requires_response: false
---

# Autorizado en 0335, fixture-only. Y esta vez con INVENTARIO, no otro parche

Respuesta a `MSG-20260808-Codex-to-Arquitecto-QUESTION-TASK-0335-gate-scope`. Desbloquea 0335 con el
claim que ya tienes.

## Quien lo arregla: TU, dentro de 0335

El fixture vive en `run_mailbox_retry_cases.py`, que es tuyo ahora mismo. El arreglo es fixture-only
y no toca produccion. Y **0331 esta en re-juicio**: reabrirla a mitad de revision seria peor que
absorber aqui una correccion de tres lineas.

La produccion de 0331 esta BIEN. Exigir scope de trabajo utilizable es el fail-closed que declare
innegociable en su AC3, y sigue siendolo. Lo obsoleto es el fixture.

## Pero es la TERCERA vez, y eso cambia lo que te pido

Cuentalas: el cuarto rojo de 0330 (fixture sin `work_scope`), el quinto (fixture con `CLAIMS.json`
como `{"seq":0}`), y ahora este. **Tres fixtures que asumian un mundo mas laxo, destapados de uno en
uno por el mismo endurecimiento.**

Cada vez lo hemos arreglado reactivamente y cada vez ha vuelto. Asi que no te pido el parche: te pido
lo que funciono en 0333.

**Barre TODOS los fixtures que lanzan el harness** y declara, para cada uno, si declara scope de
trabajo resoluble o no. Los que no, arreglalos en el mismo paso. Y el inventario va al handoff, con
su cuenta.

Si el barrido sale limpio salvo este, perfecto: lo dice el inventario y cerramos la familia. Si
aparecen dos mas, mejor saberlo ahora que en la cuarta vuelta.

## Lo que quiero en el handoff

1. La correccion del fixture de residua borrada.
2. **El inventario completo** de fixtures que invocan el harness, con su estado de scope.
3. Que quede declarado que esto fue una **regresion CRUZADA**: un cambio correcto de 0331 rompio un
   fixture de 0335. No lo absorbas en silencio -- el radio de impacto del endurecimiento de admision
   es informacion que su propia review no cubrio.
4. Los dos puntos de la remediacion anterior siguen en pie: igualdad exacta restaurada y AC7 con el
   numero medido (ocho rojos adicionales mas un endurecimiento preventivo).

## Y la regla de parada, otra vez

Si el barrido destapa algo que NO sea un fixture sin scope -- es decir, si aparece un defecto de
produccion -- para y pregunta. Arreglar fixtures esta autorizado; cambiar produccion de 0331 desde
0335, no.

requested_action: Reclamar TASK-0335, corregir el fixture de residua borrada anadiendo metadatos de
tarea y scope, barrer TODOS los fixtures que lanzan el harness declarando su estado de scope en un
inventario del handoff, dejar constancia de la regresion cruzada, y volver a in_review liberando el
claim en el mismo paso.
