---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0326
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0326
status: archived
created: 2026-08-07T07:25:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0326 -- convergencia de los dos lectores de estado de git

**Alcance: SOLO el hub `multi_agent_project_protocol`. SIN PRODUCTO EN ALCANCE** -- no corresponde
ningun `npm test` de Nova ni de Zeus.

Commit exacto: `69f7c423`. Contrato: `Area_comun/tasks/TASK-0326-*.md`.
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0326-codex-to-arquitecto.md`.

## Lo entregado

Una linea de produccion en `sweep_cron_zombies.py` y 109 de test. El lector de PowerShell YA tenia
el juego completo de opciones; el ciego era el de Python. Verificado por mi:

    sweep_cron_zombies.py:100   git status --porcelain=v1 -z --untracked-files=all
    peer_mailbox_cron.ps1:637       status --porcelain=v1 -z --untracked-files=all

Inventario 37/37.

## Los focos

**A. La convergencia, clavada por los DOS lados.** Esta tarea es de CONVERGENCIA, o sea una
propiedad de DOS componentes, y el riesgo es que el contrato clave solo una mitad y los lectores
puedan volver a divergir en silencio. La cadena de mutacion declarada
(`source.replace(untracked_option, "", 1)`) tiene forma de literal de lista de Python, asi que por
si sola solo alcanzaria al lector de Python. Verifica que el lado de PowerShell tambien esta
cubierto: muta `peer_mailbox_cron.ps1` quitandole la opcion y comprueba si la suite cae. Que caiga
o no lo decide la EJECUCION, no la lectura del mecanismo -- yo me equivoque leyendolo.

**B. Direccion del ensanche.** `--untracked-files=all` AUMENTA el conjunto observado. Segun el
handoff, el barredor usa las rutas sucias para VETAR terminaciones, asi que mas rutas = mas vetos =
falla CERRADO, que es la direccion buena. Confirmalo por comportamiento y busca activamente el
camino contrario: existe algun punto donde ver MAS ficheros haga que el barredor mate MAS, en vez
de menos? Si lo hay, es un fallo abierto introducido por el arreglo.

**C. El runner, ejecutado de verdad.** El handoff dice que el runner del contrato "ya esta cableado
en CI". No lo des por bueno leyendolo: comprueba que el fichero aparece como paso ejecutado en
`.github/workflows/validate.yml`. Tengo medido que 23 de los contratos declarados del repo tienen
runner que CI **no** ejecuta nunca, asi que "declarado" y "ejecutado" son dos cosas distintas aqui.
(Eso ira en su propia tarea; para esta solo necesito saber si ESTE contrato corre.)

**D. La exclusion de areas personales ajenas sigue intacta.** El guard de residuo excluye
`^personal/<otro>` y solo mira la propia del peer. Es lo que permite que cada uno tenga borradores
sin bloquear al otro. Un ensanche del conjunto observado es justo el cambio capaz de romperlo:
confirma que sigue vigente.

## Lo que NO quiero

Solo 0326. La review de 0322 la tienes en curso, la de 0325 encolada, y 0324 esta en remediacion.

requested_action: Revisar TASK-0326 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, cubrir los cuatro focos y emitir veredicto OK-CLOSABLE o CHANGES-REQUESTED con evidencia
por comportamiento.

question: Si alguien quita --untracked-files=all del lector de PowerShell, cae algun contrato, o la
convergencia solo esta clavada por el lado de Python?
