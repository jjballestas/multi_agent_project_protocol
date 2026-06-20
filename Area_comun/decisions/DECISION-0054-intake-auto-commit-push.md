---
decision_id: DECISION-0054
title: Superficie de TRANSPORTE gobernada - auto commit+push acotado de los outputs de submit_intent (cerrar el ciclo del intake en la app)
status: accepted
ratified_at: 2026-06-21
date: 2026-06-21
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amends: []
relates_to: [DECISION-0053, DECISION-0052, DECISION-0051, DECISION-0047, DECISION-0046, DECISION-0044]
phase: P2
---

# DECISION-0054 - Superficie de transporte gobernada: auto commit+push acotado del intake

> ACCEPTED por el operador (2026-06-21). Origen: REQ-444E0DE5 (intake del operador). EL MAS SENSIBLE de la cola:
> nueva superficie de TRANSPORTE (git write + push + credenciales/egress). OFF BY DEFAULT; push vivo = GO
> posterior del operador. NO toca config/genesis/keys (#4 epoca 1.14.0 PINNED, byte-identica). maker=Codex /
> checker=Arquitecto + PASADA DEL ANALISTA (transporte+egress) antes de cerrar.

## Contexto
REQ-444E0DE5: tras un EXECUTE exitoso del intake, el operador no quiere bajar a la terminal a git
add/commit/push; quiere que la app ATERRICE el cambio gobernado en canonico. Hoy el server Zeus solo usa
`execFile git` para LECTURAS (canonical short, dirty, validate). Esto agrega operaciones git de ESCRITURA
(add/commit) + EGRESS de red con CREDENCIALES (push al remote). Es una SUPERFICIE NUEVA que no existe hoy.

## Por que DECISION propia (regla 2 + boundary)
Un commit al repo + push a un remote con credenciales es una superficie de transporte/egress que no existe
gobernada. Aunque cuelga de un submit_intent ya gobernado, el git write + la salida de red son nuevos. Regla 2
(cambio de superficie -> DECISION) y la frontera "no secrets / egress" exigen rastro auditable.

## Decision
1. **Commit ACOTADO a los outputs de submit_intent.** El server commitea EXACTAMENTE las rutas que la
   transaccion submit_intent reporto como escritas (`task_files_updated` + ledger/state: `events.jsonl`,
   `snapshot.json`, `CLAIMS.json`, `PROJECT_STATE.json`, `TASK_INDEX.json` + `.slim`, el seed/requirement file).
   `git add <rutas-exactas>`, NUNCA `git add -A`/`.`/working-tree arbitrario. Mensaje de commit TEMPLADO
   server-side (no texto libre del cliente; ASCII; deriva de actionId+id+seq).
2. **Prueba negativa anti-commit-arbitrario (PERMANENTE):** un archivo SUCIO AJENO (no escrito por esta
   transaccion) NO entra al commit. El cliente NO puede inyectar rutas ni mensaje. Test permanente.
3. **Push al remote PRE-CONFIGURADO, sin force.** Push SOLO a la rama/remote configurados; `--force`/
   `--force-with-lease` PROHIBIDOS. Non-fast-forward -> NO se fuerza; error seguro "remote advanced, retry".
4. **Honestidad (AC11): push fallido = error, NO verde.** Si el push falla (red/auth/non-fast-forward) la UI
   muestra el error REAL y el resultado NO se pinta verde; el commit local puede existir, pero se reporta como
   NO-aterrizado. Solo con push OK se reporta "enviado + aterrizado en canonico (HEAD, seq)".
5. **Resultado atomico y honesto.** Deriva del estado REAL: HEAD (sha) y seq tras el push exitoso.
6. **Credenciales: el front NO las recibe ni almacena.** El push usa el credential helper/ambiente ya presente;
   el server invoca `git push` y git resuelve credenciales. El front nunca ve el token.
7. **OFF BY DEFAULT, config FUERA del config pinned.** La capacidad nace deshabilitada; su flag + remote/branch
   viven en un registro FUERA de `protocol.config.json` (pinned bajo #4, epoca 1.14.0), estilo
   `connectors.config.json` (DECISION-0047). Activar el push VIVO contra el remote real exige GO POSTERIOR del
   operador (mirror del connector s9): la DECISION ship la capacidad OFF.
8. **No toca el escritor unico ni #4.** El commit+push NO emite eventos ni muta el ledger (solo PERSISTE en git
   lo que submit_intent ya escribio); no toca config/genesis/keys; #4 byte-identica. Commitea un SNAPSHOT
   CONSISTENTE (exactamente los outputs) -> el clon limpio valida desde git HEAD.

## Alcance / limites
- Solo tras un EXECUTE gobernado EXITOSO (requirement-intake / mailbox-archive); no es accion git arbitraria.
- NO `git add -A`, NO commit de working-tree ajeno, NO force-push, NO texto libre del cliente en el mensaje.
- NO maneja merges/conflictos automaticamente mas alla de "non-fast-forward -> error seguro".

## Threat model (resumen)
Inyeccion de rutas/mensaje por el cliente -> rechazado (server-side). Sucio ajeno arrastrado -> prueba negativa
permanente. Force-push/sobrescritura -> prohibido por construccion. Egress de credenciales al front -> imposible
(git las resuelve). Push "fantasma" pintado verde sin aterrizar -> AC11 (solo push OK = verde; HEAD/seq reales).
Uso vivo sin querer -> off-by-default + GO del operador para el remote real.

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
