---
id: TASK-0379
title: El prompt de arranque no declara QUIEN construye cada pendiente, y por defecto lo construye quien lo lee
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0379-el-prompt-no-declara-quien-construye-cada-pendiente.md
created: 2026-08-14
reviewer: Analista
intake:
  type: doc
  goal: >
    Punto 3 de la DECISION del Operador del 2026-08-14, publicable YA junto con el Punto 1 por ser
    ortogonal a la memoria hibrida. La plantilla del prompt de arranque declara el ROL de quien la
    lee, pero no declara, por cada pendiente, QUIEN lo construye. El efecto medido en campo: una
    sesion que se declara coordinadora acaba construyendo producto, porque la lista de pendientes no
    nombra maker y el camino de menor resistencia es hacerlo uno mismo. No es un fallo de disciplina
    del que lee: es que el punto de entrada no lo dice. Si el maker de un pendiente ha de ser el
    propio Arquitecto, eso deja de ser el defecto por defecto y pasa a ser una EXCEPCION escrita, con
    checker designado por nombre.
  acceptance:
    - "AC1 (la plantilla lo exige por pendiente): la plantilla del prompt de arranque tiene, para cada
      pendiente listado, un campo que nombra al maker. Un pendiente sin maker declarado es un defecto
      de la plantilla, no una omision tolerable."
    - "AC2 (la excepcion se escribe, no se asume): si el maker declarado es el propio Arquitecto, la
      plantilla exige ademas un checker designado por nombre y una linea de por que. Sin las dos, no
      es excepcion: es el camino por defecto disfrazado."
    - "AC3 (lint que DETECTA la contradiccion, con prueba de rechazo): existe una revision ejecutable
      que falla ante un prompt que declara un rol coordinador y a la vez ordena construir producto
      sin declarar maker ni excepcion. Se acredita con el PAR: un prompt contradictorio muere, uno
      correcto pasa. Es el criterio 2f -- la prueba es el rechazo."
    - "AC4 (medido contra los prompts REALES): el lint se corre sobre los prompts de arranque que
      existen hoy en `personal/`, y se reporta cuantos declaran maker y cuantos no. Si el prompt
      vigente del Arquitecto falla, se declara y se corrige; un lint que solo pasa sobre su propio
      ejemplo no acredita."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - Area_comun/protocol/
    - scripts/
  out_of_scope:
    - "El claim obligatorio para commitear producto: es TASK-0378, el Punto 1."
    - "La liveness de maker y checker en el cold-start: es TASK-0380, Punto 2, coordinado con F2/F3."
    - "Reescribir los prompts personales de cada agente mas alla de lo que el lint exija: la plantilla
      es el nucleo; los prompts vivos los adapta su duenio."
  risk: low
  estimate: S
---

# TASK-0379 -- el punto de entrada calla quien construye

## El mecanismo, no la culpa

La plantilla dice que la sesion coordina. La lista de pendientes dice que hay cosas por hacer. No
dice quien las hace. Cuando esas dos frases conviven, el camino de menor resistencia es que las haga
quien lee -- y eso ocurre sin que nadie decida hacerlo.

El arreglo no es pedir mas disciplina: es que el punto de entrada nombre al maker de cada pendiente,
y que el caso "lo construyo yo" tenga que escribirse con checker al lado.

## Lo que lo hace verificable

El AC3 pide un lint con prueba de RECHAZO, y el AC4 lo corre contra los prompts que ya existen. Si el
prompt vigente del Arquitecto falla el lint, eso es el hallazgo -- no un inconveniente del lint.
