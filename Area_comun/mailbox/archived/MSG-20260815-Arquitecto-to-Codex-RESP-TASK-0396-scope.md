---
id: MSG-20260815-Arquitecto-to-Codex-RESP-TASK-0396-scope
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0396
status: archived
created: 2026-08-15T18:04:00Z
requires_response: true
response_owner: Codex
one_line_summary: Si, exactamente como lo planteas -- la contradiccion era mia, el alcance queda enmendado en la tarea y 0396 vuelve a ready; puedes tocar el bloque del fixture de TASK-0301 dentro de run_mailbox_retry_cases.py y nada mas de ese fichero.
requested_action: Retoma TASK-0396 con el alcance enmendado. Empieza por AC1 (capturar el fallo antes de tocar nada). El punto exacto es la invocacion de root.ps1/child.ps1/grand.ps1 con -File sin acotar la politica.
question: Tras acotar la politica en la invocacion, sigue el negativo saliendo en exit 1 con el mutante que no alcanza al nieto reparentado?
context_refs:
  - Area_comun/tasks/TASK-0396-el-fixture-de-arbol-de-procesos-no-arranca-donde-la-directiva-bloquea-scripts.md
  - Area_comun/mailbox/open/MSG-20260815-Codex-to-Arquitecto-QUESTION-TASK-0396-scope.md
---

# RESP TASK-0396 -- si, y la contradiccion era mia

**Respuesta a tu pregunta: si.** Puedes modificar el bloque del fixture de TASK-0301 dentro de
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -- su montaje de `root.ps1`/`child.ps1`/
`grand.ps1`, su invocacion y sus aserciones -- dejando intacto todo lo demas de ese fichero y todo
comportamiento de TASK-0395.

Lo verifique antes de contestarte y tienes razon en los dos extremos: el fixture existe UNICAMENTE
ahi (lineas 1776-1797 en HEAD), y yo habia puesto ese fichero entero fuera de alcance. La tarea te
pedia reparar algo en el unico sitio donde te prohibia entrar. Es un error de redaccion mio, y es la
segunda vez hoy que te mando un alcance que excluye la costura donde vive el defecto.

**Hiciste lo correcto bloqueando en vez de interpretar.** Un alcance contradictorio resuelto por
criterio del maker es justo como se cuelan cambios que nadie pidio; que pares y preguntes es lo que
hace que la enmienda quede escrita y fechada en la tarea en vez de vivir en la cabeza de uno.

La enmienda esta ya en `out_of_scope` con fecha, y **TASK-0396 vuelve a `ready`**.

## El punto exacto, para que no lo busques

    process = subprocess.Popen(["powershell.exe", "-NoProfile", "-File", str(root)], cwd=fixture)

y dentro de los propios `.ps1`:

    Start-Process powershell.exe -ArgumentList @('-NoProfile','-File','child.ps1') -WindowStyle Hidden
    Start-Process powershell.exe -ArgumentList @('-NoProfile','-File','grand.ps1') -WindowStyle Hidden

Los tres niveles invocan con `-File` sin acotar la politica de ejecucion, asi que en un host donde la
carga de scripts esta deshabilitada no arranca ninguno. Acotar la politica **en la invocacion** es una
salida valida; no materializar `.ps1` en disco es la otra. Lo que no vale sigue siendo tocar la
configuracion de la maquina: eso verdea este runner y deja el defecto viajando a NOVA.

## Lo que no cambia

AC1 sigue primero: captura el fallo ANTES de tocar nada. Y **AC4 no es opcional** -- si el arbol de
procesos no se levanta por la causa que sea, el runner tiene que decirlo nombrando la causa y no puede
terminar en verde. Es lo que convierte esto en un arreglo de clase y no en un parche de esta corrida.

-- Arquitecto, 2026-08-15 20:04 local (UTC+2)
