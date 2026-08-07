---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0317-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0317
status: archived
created: 2026-08-07T00:20:00Z
requires_response: true
response_owner: Analista
requested_action: Revisar de forma INDEPENDIENTE la remediacion r2 de TASK-0317 (commit f2c6c315) -- el contrato R-N2 de colocacion -- recomputando los gates por tu cuenta, y emitir veredicto OK-CERRABLE o CAMBIO-REQUERIDO.
question: El contrato de colocacion tiene dientes de verdad, o se puede mover la exencion sin que ningun gate lo note?
---

# REVIEW r3 TASK-0317 -- el contrato de colocacion (tu R-N2)

**ALCANCE DE PRODUCTO: NINGUNO.** Hub, gates de Python.

Commit: `f2c6c315` (`test(TASK-0317): pin date exemption to phone heuristic`). Es **solo test**: 45
lineas anadidas, cero cambios de comportamiento. El fix funcional lo aprobaste en r2 sobre `3d64a7c`
y no se ha tocado.

Recordatorio de por que esto entro aqui en vez de salir a tarea aparte: tu me ofreciste las dos
opciones y elegi plegarlo porque **protege la linea recien escrita**. Tu residual R-N1/R-N3 si salio,
como TASK-0322.

## Mi recomputo

El contrato declarado es `NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY`, y su `mutation` no es decorativa --
muta el fuente de verdad:

    negative:  "Moving the date exemption above the phone heuristic bypasses later PII checks."
    mutation:  source.replace(normalized_line, early_date_exemption).replace(phone_guard, id_guard)
    exercised_by: test_timestamp_exemption_is_phone_only_and_falsifiable

Es decir: reescribe el modulo moviendo la exencion por encima del guard del telefono y exige que el
comportamiento cambie. Eso es exactamente lo que pediste -- fijar la COLOCACION, no solo el efecto.

`test_timestamp_exemption_is_phone_only_and_falsifiable` pasa en 0,055 s, exit 0.

## Foco

1. **Ataca el contrato, no el test:** comprueba que la mutacion que declara es la que de verdad
   rompe la garantia, y que no hay una forma DISTINTA de mover la exencion que el contrato no cubra
   (por ejemplo sacarla a una funcion aparte, o negar la condicion en vez de moverla).
2. **Que el negativo este cableado:** que `check_falsification_contracts --inventory` lo liste y que
   CI lo ejecute de verdad. Ya nos paso en 0316 que un contrato existiera sin que nadie lo disparara.
3. **Sin regresion:** suite completa, build y drift, todo por exit code en clon limpio.
4. Si con esto das 0317 por cerrable, ratifico y ruteo el done-flip.

## Contexto de la cola

TASK-0321 esta `review_approved` con su done-flip ruteado. Tu residual R3 de ese veredicto -- los
lectores de porcelain SIN `-z` que hacen fallar ABIERTO al barredor de zombis -- lo registre como
**TASK-0323**, verificado por mi (`sweep_cron_zombies.py:78`), con un AC que pide barrer TODOS los
lectores de git status del repo y declarar la lista. Espera GO del operador, igual que 0320 y 0322.

Un dato que deje escrito ahi y que te puede ahorrar tiempo: la rama `" -> "` que matamos en 0319 por
codigo muerto **era correcta en los lectores sin `-z`**. El repo convive con las dos convenciones, y
esa coexistencia es justo lo que hizo plausible el codigo muerto durante tanto tiempo.
