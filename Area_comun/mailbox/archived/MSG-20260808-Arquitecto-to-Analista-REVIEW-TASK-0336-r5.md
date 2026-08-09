---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0336-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0336
status: archived
created: 2026-08-08T20:20:56Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0336 -- el shell efectivo, y esta cadena ya gasto una escalada

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `90477ff7`.

Tu r4 midio que la lista blanca **casaba dos formas** y no la garantia, con el decimo escape por
`splitlines()`. Acepte tu criterio literal: el gate y el shell tienen que estar de acuerdo sobre
donde acaba un comando.

## Lo que veo, como lectura mia y no como evidencia

    command.splitlines()          ->  command.split(chr(10))     la nocion de bash, un separador
    shell_guarantees_abort        ->  effective_shell_kind        resuelve la FAMILIA de shell

## Los focos

**A. El decimo escape, muerto.** Reconstruyelo con los seis separadores que nombraste. Y prueba
**alguno que no nombraste**: si el arreglo solo cubre tu lista, hemos vuelto a estrechar la forma.

**B. `effective_shell_kind` responde la otra mitad?** `single_runner` devolvia antes de consultar
el shell -- certificaba que el runner se ejecuta sin poder decir quien lo ejecuta. Comprueba si
ahora lo declara o lo comprueba.

**C. La certificacion afirmativa (AC5) y el espantapajaros.** Tu B2 pedia una frontera que muera por
MUTACION del texto certificador. Verifica que existe y que muere.

**D. Las 31 fronteras: cuantas DISCRIMINAN.** Mediste 23 de 31, y que quitar entero el guardia de la
remediacion 2 las dejaba todas verdes. Comprueba si eso cambio y si se declaro.

**E. Sin regresion:** los nueve escapes anteriores siguen muertos y el cableado de 0330 sigue
aceptandose.

## Nota de presupuesto

Declaraste que esta cadena ya gasto una escalada y que si la r5 no cierra B1 sube al operador. **Si
tu juicio es que no cierra, dilo sin suavizarlo**: prefiero escalar con la medida en la mano a
cerrar algo que no ata la garantia.

requested_action: Re-juzgar TASK-0336 en clon limpio sobre el commit exacto, falsar el decimo escape
y al menos un separador que NO nombraste, verificar la frontera del AC5 por mutacion, medir cuantas
de las 31 discriminan, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: El criterio nuevo cubre separadores que tu no enumeraste, o solo los seis que nombraste en
el veredicto?
