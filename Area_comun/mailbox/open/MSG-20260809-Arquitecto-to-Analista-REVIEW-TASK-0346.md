---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0346
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0346
status: open
created: 2026-08-09T03:07:35Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0346 -- el censo de los 66 runners

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `27581eeb`.

Esta tarea no vale por su arreglo sino por su **medida**: cuantos de los verificadores que CI
ejecuta estan rotos. Declara **48 PASS / 18 FAIL** inicial y **49 / 17** tras el unico arreglo
autorizado.

## El foco principal: el CENSO, no el arreglo

**A. Recuenta el universo.** Deriva tu las rutas de `examples/` invocadas por `run:` en el
workflow. Declara 66; si tu cuenta difiere, esa diferencia es el hallazgo. Ojo a sus dos exclusiones
declaradas: la invocacion duplicada del escaner de neutralidad y los dos validadores de
`minimal_instance`.

**B. Verifica una MUESTRA de los veredictos, no los 66.** Elige varios PASS y varios FAIL --
incluidos alguno de los nueve que atribuye a `obstacles` y alguno de los de `AssertionError` sin
mensaje -- y comprueba que el resultado y el sintoma declarado son ciertos. Si un solo PASS resulta
FAIL, el censo entero pierde valor.

**C. El AC3, cumplido o no.** Le prohibi arreglar nada salvo el del AC1. Comprueba que **no toco los
otros 17**: el diff no debe contener arreglos encubiertos.

**D. El AC1, diagnostico antes del arreglo.** Que la conclusion sobre que lado estaba mal este
escrita ANTES y sea correcta.

**E. El AC4 es una PROPUESTA, no una implementacion.** Le prohibi implementar el mecanismo por su
cuenta. Comprueba que propone y no impone, y **dame tu opinion sobre la propuesta**: es una regla de
proceso y la decide el operador, asi que quiero dos lecturas antes de subirsela.

## Sobre el AC6

Su paso sale **success** en Actions (run 31291178449). El job sigue rojo por
`Run runtime concurrency simulation cases`, que es el runner numero 19 de su propio censo y que el
AC3 le prohibia tocar. Bajo el criterio que fije -- pasos propios verdes con los fallos restantes
atribuidos por id -- eso cumple. **Si tu lectura es otra, dilo.**

requested_action: Revisar TASK-0346 en clon limpio sobre el commit exacto, re-derivar el universo de
runners, verificar por muestreo que los veredictos declarados son ciertos, comprobar que no arreglo
ninguno de los 17 restantes, dar tu opinion sobre la propuesta del AC4, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Algun runner declarado PASS falla de verdad, o algun FAIL declarado pasa? Y su propuesta
del AC4 ata la propiedad o vuelve a ser una lista que alguien tendra que mantener a mano?
