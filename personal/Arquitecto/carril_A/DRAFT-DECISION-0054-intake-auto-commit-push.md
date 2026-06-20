# DRAFT - DECISION-0054: superficie de TRANSPORTE gobernada - auto commit+push acotado de los outputs de submit_intent

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion del operador.
> Origen: REQ-444E0DE5 (intake del operador). EL MAS SENSIBLE de la cola: nueva superficie de TRANSPORTE
> (git write + push + credenciales). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (transporte) antes de cerrar.

## status
proposed

## Contexto
REQ-444E0DE5: tras un EXECUTE exitoso del intake, el operador no quiere bajar a la terminal a hacer
git add/commit/push; quiere que la app ATERRICE el cambio gobernado en canonico. Hoy el server Zeus solo usa
`execFile git` para LECTURAS (canonical short, dirty, validate). Esto agrega operaciones git de ESCRITURA
(add/commit) + EGRESS de red con CREDENCIALES (push al remote). Es una SUPERFICIE NUEVA que no existe hoy.

## Por que DECISION propia (regla 2 + boundary)
Un commit al repo + push a un remote con credenciales es una superficie de transporte/egress que no existe
gobernada. Aunque cuelga de un submit_intent ya gobernado, el git write + la salida de red son nuevos. Regla 2
(cambio de superficie -> DECISION) y la frontera "no secrets / egress" exigen rastro auditable. Por eso DECISION
propia (no prosa en 0052/0053).

## Decision
1. **Commit ACOTADO a los outputs de submit_intent.** El server commitea EXACTAMENTE el conjunto de rutas que
   la transaccion submit_intent reporto como escritas (`task_files_updated` + ledger/state: `events.jsonl`,
   `snapshot.json`, `CLAIMS.json`, `PROJECT_STATE.json`, `TASK_INDEX.json` + sus `.slim`, el seed/requirement
   file). Se hace `git add <rutas-exactas>`, NUNCA `git add -A`/`.`/working-tree arbitrario. El mensaje de commit
   es TEMPLADO server-side (no texto libre del cliente; ASCII; deriva del actionId + id + seq).
2. **Prueba negativa anti-commit-arbitrario (PERMANENTE):** un archivo SUCIO AJENO en el working tree (no escrito
   por esta transaccion) NO entra al commit. El cliente NO puede inyectar rutas ni mensaje. Test permanente.
3. **Push al remote PRE-CONFIGURADO, sin force.** Push SOLO a la rama/remote configurados; `--force`/`--force-
   with-lease` PROHIBIDOS. Si el remote avanzo (non-fast-forward) -> NO se fuerza; se reporta error "remote
   advanced, retry" (el operador reintenta; la app puede fetch+reintentar de forma segura, nunca sobrescribir).
4. **Honestidad (AC11): push fallido = error, NO verde.** Si el push falla (red, auth, non-fast-forward) la UI
   muestra el error REAL y el resultado NO se pinta verde; el commit local puede existir, pero el resultado se
   reporta como NO-aterrizado. Solo con push OK se reporta "enviado + aterrizado en canonico (HEAD, seq)".
5. **Resultado atomico y honesto.** El resultado deriva del estado REAL: HEAD (sha) y seq tras el push exitoso.
6. **Credenciales: el front NO las recibe ni almacena.** El push usa el credential helper/ambiente ya presente
   en la maquina; el server invoca `git push` y git resuelve credenciales. El front nunca ve el token.
7. **OFF BY DEFAULT, config FUERA del config pinned.** La capacidad nace deshabilitada; su flag + remote/branch
   viven en un registro FUERA de `protocol.config.json` (pinned bajo #4, epoca 1.14.0), estilo
   `connectors.config.json` (DECISION-0047/versioning-por-epoca). Activar el push VIVO contra el remote real
   exige GO POSTERIOR del operador (mirror del connector s9): la DECISION ship la capacidad OFF.
8. **No toca el escritor unico ni #4.** El commit+push NO emite eventos ni muta el ledger (solo PERSISTE en git
   lo que submit_intent ya escribio); no toca config/genesis/keys; #4 byte-identica. Commitea un SNAPSHOT
   CONSISTENTE (exactamente los outputs) -> el clon limpio valida desde git HEAD.

## Alcance / limites
- Solo tras un EXECUTE gobernado EXITOSO (requirement-intake / mailbox-archive); no es una accion git arbitraria.
- NO `git add -A`, NO commit de working-tree ajeno, NO force-push, NO texto libre del cliente en el mensaje.
- NO maneja merges/conflictos automaticamente mas alla de "non-fast-forward -> error seguro".

## Threat model (resumen)
- Inyeccion de rutas/mensaje por el cliente -> rechazado (server-side, rutas derivadas de submit_intent).
- Sucio ajeno arrastrado al commit -> prueba negativa permanente.
- Force-push / sobrescritura del remote -> prohibido por construccion.
- Egress de credenciales al front -> imposible (git las resuelve, el front no las ve).
- Push "fantasma" pintado verde sin aterrizar -> AC11 (solo push OK = verde; HEAD/seq reales).
- Uso vivo sin querer -> off-by-default + GO del operador para el remote real.

## Consecuencias
Nueva capacidad de producto (Zeus) off-by-default; registro fuera del config pinned. El core no cambia. Cierra
el ciclo del intake en la app. Activacion viva = GO posterior del operador.

## Condiciones de cierre (innegociables)
(a) commit acotado EXACTO a outputs de submit_intent (add explicito, nunca -A); (b) prueba negativa sucio-ajeno-
no-entra + cliente-no-inyecta-rutas/mensaje (permanente); (c) push fallido -> error NO verde (AC11); resultado =
HEAD+seq reales solo con push OK; (d) sin force-push; non-fast-forward -> error seguro; (e) off-by-default,
registro fuera del config pinned, push vivo gateado por GO del operador; (f) #4 byte-identica, validate con/sin
secretos exit 0, drift 0, npm test verde, neutralidad/encoding 0; (g) PASADA DEL ANALISTA (bounding del
transporte + egress) ANTES de cerrar.
