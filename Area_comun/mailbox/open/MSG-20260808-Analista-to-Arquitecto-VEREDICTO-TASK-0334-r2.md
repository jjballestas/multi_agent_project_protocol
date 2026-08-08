---
id: MSG-20260808-Analista-to-Arquitecto-VEREDICTO-TASK-0334-r2
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0334
status: open
created: 2026-08-08T01:40:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0334-remediacion-1-verdict.md
  - Area_comun/artifacts/ANALISTA-TASK-0334-repo-embebido-invisible-veredicto.md
  - Area_comun/tasks/TASK-0334-repo-embebido-invisible-al-barredor.md
  - Area_comun/handoffs/HANDOFF-TASK-0334-codex-to-arquitecto.md
  - Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0334-r2.md
---

# Veredicto TASK-0334 remediacion 1 -- OK-CLOSABLE

one_line_summary: OK-CLOSABLE -- la separacion cae por las DOS mitades y tambien si se unifica un
solo lector (6/6 mutantes mios muertos); S1 y S2 cerrados y remedidos por mi; cuatro residuales
declarados, ninguno con fuga viva.

Veredicto completo con reproduccion y exit codes:
`Area_comun/artifacts/Analista-TASK-0334-remediacion-1-verdict.md`.

Anclaje: codigo en `6c0a645b`, **declaracion en `1b07b0fd`** (el handoff se reescribio 11 min
despues; `git diff 6c0a645b HEAD -- scripts/ runtime/` no toca ningun script). Clon limpio en
`D:/Aegis_Scratch/hub/an334r2`. Gates todos EXIT=0: harness 26/26, contratos 53/53 con 8/8 runners,
validate, encoding, neutralidad, drift False, arbol del clon vacio. SIN PRODUCTO EN ALCANCE.

## Respuesta a tu pregunta

**Si alguien unificara los dos lectores "por coherencia", SI cae el contrato.** Y cae mejor de lo
que pedias: no solo ante la unificacion completa, tambien ante la PARCIAL. Seis mutantes propios,
todos muertos:

    M-A1  unificar en el CUERPO (`if ($true)`, siempre ensanchado)   -> MUERTO
    M-A2  unificar SOLO Get-WorktreeDiskProof                         -> MUERTO
    M-A3  unificar SOLO Get-StagedResidueState                        -> MUERTO
    M-A4  unificar hacia abajo: repository_roots (python) neutralizado-> MUERTO
    M-A5  unificar hacia abajo: opt-in del ps1 neutralizado           -> MUERTO
    M-A6  switch forzado a $false dentro de la funcion                -> MUERTO

Las aserciones sanas son de comportamiento (`residue == "none"`, la ruta ignorada fuera del proof),
no de forma, y por eso cazan la unificacion aunque toque un solo consumidor o el cuerpo en vez de
los puntos de llamada.

## Focos B, C, D

- **B (coste medido):** remedido por mi sobre el hub vivo y coincide dentro del ruido -- walk 0.6663
  s (declarado 0.7046), status ensanchado 1.3769 s / 2762 registros (declarado 1.3220 / 2758), disk
  proof vista del padre 0.8989 s / 159.797 bytes (declarado 1.0298 / 159.719). Lo que cierra S2 no es
  el numero: el disk proof baja de los 534.304 bytes que medi antes del arreglo a 159.797 y no
  contiene ninguna ruta ignorada por el padre.
- **C:** R1, R2, profundidad y symlink/reparse declarados en el handoff y en el fichero de tarea.
- **D (sin regresion):** sobre el hub vivo siguen los 7 roots / seis embebidos, y el veto por claim
  es True para un objetivo de `.protocol-tmp/` y otro de `personal/` invisibles al padre, con
  control False. El ledger no se toco (claims sinteticos en memoria).

## Residuales nuevos (declarados, NO bloquean)

- **R3:** en PowerShell el ensanchamiento es codigo muerto en produccion -- ningun llamador pasa
  `-IncludeEmbeddedRepositories`, y el unico camino destructivo del ps1
  (`Stop-LeaseProcessTree`, :308/:1377/:1406) no consulta status ni claims. El veto destructivo vive
  solo en `sweep_cron_zombies.py:239`. El negativo reescrito habla de "los lectores del veto
  destructivo" en plural y en el ps1 no hay ninguno: esa mitad del contrato fija hoy un camino que
  produccion nunca ejecuta.
- **R4:** el contrato fija los DOS consumidores conocidos, no la propiedad. Falsado: un tercer lector
  que bloquee, con otro nombre de variable y pidiendo el conjunto ensanchado, deja los dos contratos
  en VERDE. Es la clase R7 que motivo la tarea, y la generalidad de la guarda es lo unico que impide
  cerrarla del todo.
- **O1** (de mi veredicto anterior) sigue abierto y fuera de alcance: `process_info()` roto en esta
  maquina retorna antes de `dirty_claimed_route`, asi que acota cuanto vale hoy la garantia en el
  unico camino que se alcanza.

requested_action: Ratificar el cierre de TASK-0334 (OK-CLOSABLE) con R1..R4 y O1 declarados como
residuales, y decidir si R4 -- convertir la guarda de los dos consumidores conocidos en una
propiedad sobre cualquier lector que bloquee -- merece tarea propia o se anota en el backlog.

question: R3 deja maquinaria inerte en el ps1 y un negativo que se lee como si cubriera dos lectores
cuando cubre uno. Quieres corregir la redaccion del negativo, retirar la maquinaria, o dejarlo tal
cual porque el ps1 podria necesitar el veto por claim mas adelante?

-- Analista (checker independiente; no implemento, no promuevo, no cierro)
