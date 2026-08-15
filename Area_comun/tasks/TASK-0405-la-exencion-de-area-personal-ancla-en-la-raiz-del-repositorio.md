---
id: TASK-0405
title: La exencion de area personal del guardian de residuo ancla en la raiz del repositorio, asi que en toda instancia con el gobierno anidado esta MUERTA
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0405-la-exencion-de-area-personal-ancla-en-la-raiz-del-repositorio.md
created: 2026-08-16
reviewer: Analista
intake:
  type: fix
  goal: >
    Defecto D-1 del reporte de campo de la instancia NOVA, primera adopcion real de la metodologia.
    Lo diagnostico su Arquitecto y el Arquitecto del hub lo verifico en el codigo el 2026-08-16.

    `Get-StagedResidueState` (`scripts/harness/peer_mailbox_cron.ps1:918`) exime del calculo de residuo
    el area personal de los OTROS peones:

        $candidateIsRelevant = ($candidate -notmatch '^personal/([^/]+)(?:/|$)' -or $Matches[1] -ieq $PeerId)

    La expresion ancla en `^personal/`. En el hub la raiz del repositorio git ES la raiz de gobierno,
    asi que `git status --porcelain` emite `personal/Codex/...` y la exencion FUNCIONA. En una
    instancia con el gobierno ANIDADO -- modelo 2.A, el que usa NOVA, con `Aegis/` dentro del repo de
    producto -- la misma orden emite `Aegis/personal/Codex/MEMORY.md`. **El ancla no casa jamas y la
    exencion esta muerta.** Comprobado por ellos empiricamente con un fichero de sonda, leyendo la
    salida real y no razonando sobre ella.

    Consecuencia medida en su instancia: el area personal de CUALQUIER peon cuenta como residuo para
    TODOS, asi que el residuo de uno paraliza al otro. En 15 minutos de log: el checker aplazo tres
    veces la verificacion de un defecto vivo en produccion, y el maker aplazo cuatro mensajes.
    Repetido cuatro veces en un solo dia de operacion.

    Lo que hace este defecto especialmente caro es DONDE esta: el remedio ya estaba escrito, con la
    intencion correcta, y llevaba desactivado desde que existe la posibilidad de instanciar anidado.
    Nadie lo vio porque en el hub -- donde se desarrolla y se prueba -- funciona por coincidencia de
    topologia.
  acceptance:
    - "AC1 (reproducir en las DOS topologias antes de tocar nada): montar el caso con el gobierno en
      la raiz y con el gobierno anidado, y capturar la salida real de `git status --porcelain` en cada
      una mas el veredicto del guardian. Sin el par no esta demostrado que el defecto sea de anclaje y
      no de otra cosa."
    - "AC2 (la exencion funciona en las dos): el prefijo se DERIVA de la ruta de gobierno respecto a
      la raiz del repositorio y se descuenta antes de comparar. NO vale relajar la expresion a
      `(?:^|/)personal/`: eso casaria tambien `cualquier/cosa/personal/x` y cambia un defecto por
      otro. Lo dice el propio reporte de NOVA y estoy de acuerdo."
    - "AC3 (el negativo sigue vivo): un fichero sin commitear en una ruta COMPARTIDA -- `Area_comun/`,
      `runtime/state/` -- sigue contando como residuo y sigue difiriendo. Se acredita ejecutando: si
      el arreglo exime de mas, deja de proteger lo que debe."
    - "AC4 (el mismo error de anclaje, en otros sitios): buscar si hay mas comparaciones de ruta en el
      arnes que asuman que la raiz del repositorio es la raiz de gobierno, y reportarlas. NOVA ya
      comprobo `Test-ScopeIntersection` y ahi NO ocurre -- los dos lados vienen de `scope_routes` del
      ledger y son consistentes entre si. El censo se DERIVA de una busqueda, no de esta nota."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/
  out_of_scope: >
    NO cierra el interbloqueo circular del peon consigo mismo: la exencion cubre el area de los OTROS
    peones, y que la memoria del propio peon lo bloquee es TASK-0406. Arreglar el ancla es condicion
    necesaria y no suficiente; conviene decirlo para que nadie de por resuelto D-1 entero. NO se toca
    la interseccion de alcances (TASK-0337, TASK-0387).
  risk: high
  estimate: M
---

# TASK-0405 -- una exencion correcta, desactivada por un ancla

## Procedencia

Defecto **D-1** del reporte de campo de NOVA (2026-08-15). Su Arquitecto encontro la causa raiz; el
Arquitecto del hub la verifico en `peer_mailbox_cron.ps1:918` el 2026-08-16.

## Por que el hub no lo vio

    hub    raiz del repo == raiz de gobierno   ->  "personal/Codex/x"        -> CASA, exencion viva
    NOVA   gobierno anidado en Aegis/          ->  "Aegis/personal/Codex/x"  -> NO casa, exencion muerta

Se desarrolla y se prueba donde funciona por coincidencia de topologia. Es la forma mas cara de punto
ciego: el codigo correcto, la intencion correcta, y el efecto nulo en la mitad de las instancias.

-- Arquitecto, 2026-08-16
