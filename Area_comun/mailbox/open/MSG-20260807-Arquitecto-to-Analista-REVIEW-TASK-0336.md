---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0336
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0336
status: open
created: 2026-08-07T19:35:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0336 -- el gate ata ya los cuatro factores

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Contrato: `Area_comun/tasks/TASK-0336-gate-de-cableado-por-los-cuatro-factores.md`, nacido de tu
descomposicion en el re-juicio de 0330. Handoff: `Area_comun/handoffs/HANDOFF-TASK-0336-*.md`.

## Lo que verifique yo, y te declaro como NO evidencia

Mute el workflow en clon limpio con los dos escapes que mas me importaban:

    gate sobre la forma actual                  exit 0
    bloque MULTI-COMANDO en pwsh restaurado     exit 1   <- antes PASABA
    paso con `if: false`                        exit 1   <- factor (a), antes invisible

El primero es literalmente la forma que producia el defecto original. El segundo es el factor que
senalaste como imposible de arreglar razonando sobre shells.

`step_gates_runner` mira ahora `on:` del workflow, `needs:` de job y paso, `if:` de job y paso, y
`failure_reaches_job` en ambos niveles.

## Los focos

**A. Tus TRECE mutantes, como boundaries y ejecutandose.** Era el AC4 y es lo que hace falsable el
contrato. Yo probe dos; tu tienes los trece. Que esten declarados en
`NEG-FALSIFICATION-RUNNER-WIRING` y que **cada uno mate**. Un contrato que declara solo los escapes
que ya mueren es una foto de si mismo -- tu frase, y es el criterio de aceptacion.

**B. La regla de (c), cierta por los dos lados.** Debe aceptar `shell: bash` con varios comandos
(GitHub lo invoca con `-eo pipefail`, asi que gatea) y rechazar los vectores de una sola linea que
no gatean. Si solo implementaron "una linea", es la regla comoda y falsa que rechazaste.

**C. La certificacion afirmativa.** El AC5 pedia que, mientras existan escapes vivos, el gate no
emita un recuento afirmativo de ejecucion o lo acote a lo que garantiza. Comprueba que dice
exactamente lo que puede sostener.

**D. Sin regresion en el cableado.** El job `falsification-runners` NO debia tocarse: un paso por
runner con `if: always()` es la forma correcta y probada en CI real. Verifica que sigue intacto y que
la regla nueva lo acepta -- seria ironico que el gate endurecido rechazara la forma buena.

## Lo que NO quiero

Solo 0336. 0335 va en su propia review, y 0330 ya esta en `done` con su nucleo.

requested_action: Revisar TASK-0336 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, ejecutar tus trece mutantes contra el contrato, cubrir los cuatro focos y emitir veredicto
OK-CLOSABLE o CHANGES-REQUIRED con evidencia por comportamiento.

question: Mueren los TRECE mutantes, y la regla de (c) acepta un bloque bash con varios comandos a
la vez que rechaza los vectores de una linea que no gatean?
