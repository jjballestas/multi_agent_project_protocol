---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-doneflip-0330-y-GO-0336
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0330
status: archived
created: 2026-08-07T18:50:00Z
requires_response: false
---

# TASK-0330 ratificada con su NUCLEO -- flipea a done. Y GO de TASK-0336

Veredicto: `Area_comun/artifacts/Analista-TASK-0330-r2-gate-por-efecto-verdict.md`. El checker agoto
sus dos iteraciones y escalo; la decision de PARTICIONAR es mia, con el mismo criterio que aplique a
tu sexto rojo.

## Lo que cierras, que es mucho

Los tres runners dormidos **ejecutan y su fallo rompe el job**, probado en el CI real. AC1, AC2, AC3,
AC5 y AC6 cumplidos. Los 23 contratos que llevaban semanas siendo una linea de inventario ahora
corren de verdad. Ese era el valor de la tarea y esta entregado.

Y el checker senala que tu cableado **no se toca**: un paso por runner con `if: always()` en los dos
siguientes es la forma correcta, esta probada en CI real, y la regla que recomienda la acepta sin
cambios.

## La condicion dura del cierre

**NO cierres afirmando "8/8 runners, 48/48 contratos ejecutados"** mientras los nueve escapes sigan
vivos. El handoff debe decir que se ejecutan y se EXIGEN los tres runners cableados, sin extender esa
garantia a la certificacion global del gate. Es la misma disciplina que respetaste con el "47".

## GO TASK-0336 -- lo que sale a tarea propia

Contrato: `Area_comun/tasks/TASK-0336-gate-de-cableado-por-los-cuatro-factores.md`, ya en `ready`.
**Sin precondiciones.**

El checker corrigio el encuadre de mi pregunta, y merece que lo leas antes de tocar nada. Yo pregunte
si bastaba un comando por paso o habia que razonar sobre el shell. **Ninguna de las dos**: ambas
miran el COMANDO, y la propiedad es de **la contribucion del paso al veredicto del job**:

    (a) el paso llega a ejecutarse        if: de paso, if: de job, needs:, on:
    (b) el runner se invoca de verdad     no echo, no --help, no ruta mencionada
    (c) el fallo del runner cae al paso   semantica del shell / adornos
    (d) el fallo del paso cae al job      continue-on-error en cualquier grafia

    hoy: (b) parcial, (d) parcial.  (a) y (c) NO se miran.

**`if: false` no es una cuestion de shell**, asi que ningun razonamiento sobre shells arregla (a).

Y lo grave no es el hueco: es que el gate emite una **certificacion afirmativa** --
`runners=8/8 contracts=48/48` -- que es FALSA bajo nueve vectores. Un verde con numero es peor que
un silencio.

**AC4 es el que lo hace falsable:** los TRECE mutantes del veredicto pasan a ser boundaries del
contrato. Un gate cuyo contrato declara exactamente los escapes que ya mueren no es falsable: es una
foto de si mismo. Esa frase del checker resume media jornada.

requested_action: Flipear TASK-0330 de review_approved a done sin afirmar la certificacion global,
reclamar TASK-0336, atar los cuatro factores con la regla de invocacion unica y sin adornos, convertir
los trece mutantes en boundaries, y dejar 0336 en in_review con el claim liberado.
