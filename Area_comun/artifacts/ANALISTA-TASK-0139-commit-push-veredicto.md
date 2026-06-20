# ANALISTA - VOZ EXTERNA ADVERSARIAL - commit-push acotado (TASK-0139 / DECISION-0054 / AC27-AC28)

> Voz: Analista (escepticismo externo). Firma: Analista. Fecha: 2026-06-20. Lente: transporte / egress /
> honestidad / seguridad. ANCLADO EN CANONICO: protocolo HEAD==origin `a1e9b94`; codigo front en clon
> limpio Zeus-protocol `9d0a586` (arbol limpio). Verifique leyendo el CODIGO y corriendo la suite YO MISMO.
> NO promuevo, NO autoro SPEC, NO muto estado. El push VIVO al remote real sigue OFF (GO separado del operador).

## VEREDICTO: OK -> CERRABLE.
Transporte, egress y honestidad RESISTEN. Lo critico (no-drag y non-fast-forward) esta probado por
COMPORTAMIENTO contra un bare remote local, no por string-match.

## Reproduccion (gate por exit code)
- Zeus clon @ 9d0a586: `npm test` -> **29/29 PASS**.
- Protocolo: drift `has_drift=False`; `validate` exit 0 (con secretos). El test clona el HEAD PUSHEADO (bare
  remote, sin secretos) y corre `validate` -> "OK: collaboration state is valid" (sin-secretos verificado ahi).

## TRANSPORTE -> PASA (behavior-tested)
- **Paths derivados SERVER-SIDE:** `collectSubmitIntentOutputPaths` arma la lista del OUTPUT del
  submit_intent (`materialization.paths` + `runtime/state/events.jsonl|snapshot.json` + `task_files_updated`
  + `seedFilesWritten`), NO del cliente. `normalizeSubmitIntentOutputPath` rechaza absolutos (`/`, `C:`) y
  cualquier segmento `..` (sin traversal).
- **`git add -- <paths>` + `git commit -m <msg> --only -- <paths>`:** el `--only -- <paths>` commitea
  EXACTAMENTE esas rutas, ignorando cualquier staged/dirty ajeno.
- **PRUEBA DE COMPORTAMIENTO (test "lands only exact submit_intent outputs on a test remote"):** el test crea
  `STAGED_UNRELATED.txt` (staged) + `UNRELATED_DIRTY.txt` (dirty), dispara un execute real, y asserta que el
  commit (`git show --name-only`) **NO** incluye ninguno de los dos (si incluye events/snapshot/TASK_INDEX/
  seed), y que tras el commit siguen `A STAGED_UNRELATED` / `?? UNRELATED_DIRTY` intactos. No-drag PROBADO.
- **Mensaje templado server-side:** `buildAutoCommitMessage` = `ascii(stripControl("front <actionId>
  <primaryId> seq <seq>"))`. No es texto libre del cliente.
- **Sin force:** `git push <remote> HEAD:refs/heads/<branch>` plano; `grep '--force|force-with-lease'` en el
  server = 0. **Non-fast-forward -> 409 SIN sobrescribir**, probado por comportamiento (test "reports
  non-fast-forward without overwriting": avanza el remote desde un clon, el push da **409** `remote advanced`
  y `ls-remote` muestra que el remote sigue en el head avanzado, no sobrescrito).

## EGRESS -> PASA
- **Registro FUERA del config pinned:** `commit-push.config.json` (separado de `protocol.config.json`);
  default `enabled:false` -> **OFF by default** (loader devuelve `{enabled:false}` en ENOENT o enabled false).
- **assertAllowedKeys cierra el payload:** top-level admite solo `{actionId, mode, confirm, intake, mailbox}`
  -> un `paths`/`commitMessage`/`intents` del cliente = 400 (y `payload.actorId`/`payload.intents` ya
  rechazados explicitamente). El cliente NO inyecta rutas, mensaje ni intents.
- **Sin secretos en el payload/commit:** las rutas son output de runtime; `secrets/` es gitignored y no esta
  en el set derivado. `remote`/`branch` salen del config server-side, sanitizados (`sanitizeGitRemote`
  rechaza CRLF y valores que empiezan con `-` = sin flag-injection; `sanitizeGitBranch` regex estricta,
  rechaza `..`, `@{`, `:`, `\`, trailing `/`). `git` via `execFileAsync` (sin shell). `scrubGitOutput`
  redacta el remote en mensajes de error -> sin fuga del remote/credencial en diagnosticos.

## HONESTIDAD (AC11) -> PASA (behavior-tested)
- `landed:true` SOLO cuando `remoteHead` confirma via `ls-remote` que el HEAD sha EXACTO esta en
  `refs/heads/<branch>`; si no aterriza -> 502 (no landed). El test asserta `landed:true` + `head` (40 hex)
  + `seq == runtime_snapshot.up_to_seq` Y verifica con un `ls-remote` independiente que el head pusheado esta
  en el remote; ademas clona ese head y valida exit 0. Push OK == aterrizaje real, no optimista.

## Observacion (no bloqueante)
El push VIVO contra el remote REAL no se ejecuto (gateado, requiere GO separado del operador). NO es un gap
de verificacion: el mecanismo (add/commit --only/push/ls-remote/landed) esta ejercitado por comportamiento
contra un bare remote LOCAL que recorre el MISMO code path; lo unico no ejercitado es la red + credenciales
reales, que es exactamente lo que el gate del operador cubre. Correcto que siga OFF hasta el GO.

## RECOMENDACION: OK, CERRABLE.
Con mi OK el Arquitecto puede cerrar TASK-0139 -> done. El push vivo permanece OFF hasta GO separado.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre la tarea, no ejecute push vivo. Ancle en canonico
  (a1e9b94 / 9d0a586). Suite/clones corrieron en temporales; no toque el ledger vivo. Scratch limpiado.
