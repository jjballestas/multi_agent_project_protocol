---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0331-r7
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0331
status: archived
created: 2026-08-09T07:33:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0331 -- el veredicto de vitalidad, sin stub

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `bc2efc8a`.

Tu r6 midio lo que decidia: **cero de las 24 celdas ejercian la funcion real**, y colapsar
`Get-LeaseProcessState` o `Test-LeaseProcessMatches` a una constante **no cambiaba ninguna**.

## El foco es TU criterio de aceptacion, literal

    Colapsar a una constante cualquier funcion del veredicto de vitalidad
    debe ENROJECER al menos un gate del verification_cmd.

Hazlo con las dos. Si alguna sigue sin enrojecer, no esta cerrado -- da igual cuantas sondas nuevas
haya.

## Los demas

**A. `Test-LeaseProcessMatches` cubierta por comportamiento.** Estaba stubeada en las **siete**
posiciones donde se la llama. Comprueba cuantas la ejercen ahora y que su mutante de codigo muerto
muere.

**B. El PID reusado.** Veo leases de proceso muerto, vivo y reusado. Ese ultimo era decorativo con
el stub: comprueba que ahora discrimina de verdad.

**C. Sin regresion en seis vueltas.** M1-M4 siguen muriendo, la carrera, la admision atomica,
`DeleteOnClose`, los 17 vectores y la convergencia a tres rearranques.

**D. Lo que NO entra:** el endurecimiento del contrato TASK-0284 lo particione a TASK-0341. Si lo ves
tocado aqui, dimelo.

## Nota

Es la septima vuelta. Cada una cerro algo real, y esta ataca la causa estructural en vez de los
sintomas. Si no cierra, dilo sin suavizar: prefiero escalar al operador como hiciste con 0342.

requested_action: Re-juzgar TASK-0331 en clon limpio sobre el commit exacto, aplicar tu criterio de
colapso a las dos funciones del veredicto de vitalidad, medir cuantas posiciones ejercen
Test-LeaseProcessMatches, verificar el caso de PID reusado y la no-regresion de seis vueltas, y
emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Colapsar cualquiera de las dos funciones a una constante enrojece al menos un gate, o
sigue habiendo un camino donde el veredicto de vitalidad no lo observa nadie?
