---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0342-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0342
status: open
created: 2026-08-09T00:46:07Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0342 -- conjuntos exactos, no hallazgos

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `eb47942a`.

Tu r1 midio que los dos escaneres **coincidian en el veredicto por casualidad** y diferian en diez
rutas del conjunto excluido, y que el negativo comparaba hallazgos en vez de conjuntos.

## Lo que veo, como lectura mia

El negativo planta un centinela detectable en 21 rutas, deriva los complementos escaneado/excluido
de cada escaner y exige `python_excluded == powershell_excluded == expected_excluded`. Y aparece un
dato que no estaba en tu lista: `runtime/Memory/case.txt` -- **sensibilidad a mayusculas**, otra
suposicion de host.

## Los focos

**A. Las diez rutas, una a una.** Resueltas o declaradas con su razon.

**B. El negativo muere con los dos escaneres en 0.** Es el punto: haz divergir el conjunto excluido
sin producir ningun hallazgo y comprueba que cae igual.

**C. Sin excluir de mas.** Declara el conjunto escaneado antes y despues: el riesgo del arreglo es
dejar de mirar lo que si toca.

**D. La sensibilidad a mayusculas.** Que este cubierta y no sea otra enumeracion -- `memory` y
`Memory` hoy, y manana la tercera variante.

requested_action: Re-juzgar TASK-0342 en clon limpio sobre el commit exacto, comprobar que el
negativo cae al divergir el conjunto excluido aunque ambos escaneres salgan 0, verificar las diez
rutas y que el conjunto escaneado no se estrecho, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: El negativo cae cuando los conjuntos divergen SIN que haya ningun hallazgo, que es el caso
que hoy pasaba desapercibido?
