# SESSION START PROMPT -- Arquitecto (2026-08-12, cierre de tarde)

> REESCRITO el 2026-08-12 20:45 local (UTC+2). Supera a la version de las 14:35 del mismo dia (que
> describia una pausa por viaje ya consumida) y al SESSION_START_PROMPT_20260801.md. Estado REAL
> verificado por medicion, no por plan.
>
> **DIFERENCIA CLAVE CON EL CIERRE ANTERIOR: los crons quedaron VIVOS.** No hay marcador `.stop`.
> Los peones siguen trabajando su cola mientras no haya nadie mirando.

## ROL
Arquitecto / Orquestador de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Codex=maker/implementer, Analista=checker-only, operador(John)=aprueba. actor_id ledger="Arquitecto".
DECISION-0038 narracion minima. HORA local (UTC+2) **leida del reloj, jamas estimada**, en cada informe.

## COLD-START (ejecutar en orden; PASO 4 NO ES SALTABLE)
0. **Lease instancia-unica:** lee `personal/Arquitecto/.session-lease`; si hay lease FRESCO (<30min) de
   otro session_id -> NO coordinar, consultar al operador. Escribe/refresca el tuyo.
1. Lee `memory/MEMORY.md` + `memory/project-state-snapshot.md` (bloque TOPE + ACCION INMEDIATA).
2. Dispara la skill `arquitecto-ledger-ops` ANTES de cualquier escritura al ledger.
3. `git fetch` + `git merge --ff-only origin/main`. Verifica HEAD==origin.
4. **ARMA LOS 3 WATCHDOGS/MONITORES OBLIGATORIOS (skill `arquitecto-monitor-coordina`): (a) monitor de
   entregas HEAD-local con self-filter que ignora `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- LOS 3
   modelos -- + asesor; (b) watchdog exec-health; (c) watchdog higiene mailbox. SI NO LOS ARMAS, NO HAS
   COMPLETADO EL ARRANQUE.**
   - **El watchdog (b) usa el HEARTBEAT `EXEC_RUNNING` del log del cron, NO el mtime del `err.log`**:
     en text-mode el `err.log` queda a 0 bytes y su mtime congelado, y la version vieja falso-positiveaba
     en CADA review. Verificado hoy: disparo a los 511 s con el exec perfectamente vivo.
5. **Los crons quedaron VIVOS** (codex pid 2340, analista pid 25280 al cerrar). Verifica liveness real
   antes de asumir nada; si murieron, relanza con
   `powershell -NoProfile -File personal/<Peer>/<peer>_mailbox_cron.ps1` (run_in_background).
   **Al relanzar, LEE SU LOG EN LA PRIMERA RONDA**: un `RETRY_DEFER` con causa no transitoria es un
   mensaje muerto andando, no una espera.
6. **Verifica los runners propios** (DECISION-0112): `gh api repos/jjballestas/
   multi_agent_project_protocol/actions/runners` -> `protocol-win` y `protocol-linux` deben salir `online`.
   Si Linux no esta, la distro de WSL se cerro: relanza el ancla `wsl -d Ubuntu -- sleep infinity`.

## FONDO INTOCABLE (byte-identico, jamas tocar)
`protocol.config.json` sha8 = **2E35F26E** (verificado al cierre), epoch **1.14.0** PINEADO. Dataset
**N=500**. Re-genesis PROHIBIDO. Cambiar cualquiera = NUEVA DECISION.

## QUE ESTOY HACIENDO

**Prioridad declarada por el operador: TERMINAR LA MEMORIA HIBRIDA.** Todo lo demas cede.

**1. TASK-0367 en `ready` SIN RUTEAR -- es el primer GO.** El operador la aprobo expresamente y
aplazo su ejecucion por falta de tiempo. Cierra la SEGUNDA causa del paso 50 del job `validate`: el
nucleo neutral trae la identidad de esta instancia cableada (`runtime/context.py:15`
DEFAULT_AGENT_ROLES architect -> "Claude", `runtime/router.py:438` como ultimo recurso,
`scripts/prune_state.py:252` y `:442`, mas el arnes en el tier runtime). Toda instancia generada la
hereda: frontera de AGENTS.md s.4 medida por conducta.

**2. Memoria hibrida BLOQUEADA en dos frentes, registrados `proposed` y sin rutear.**
- **TASK-0368 (motor, Codex).** El motor deriva "decision vigente" del literal `status == "active"` y
  este corpus escribe `accepted`: 106 de 110 politicas salen `historical`/`hot_required=0`, incluidas
  DECISION-0026, 0020, 0038 y 0104. Fail-CLOSED para I4, **fail-OPEN para I7**. Sus AC matan
  explicitamente la salida facil ("anadir `accepted` a la lista" es la misma lista con un elemento
  mas) y exigen supervivencia a una tercera grafia con fallo RUIDOSO.
- **TASK-0369 (texto s.7, mia).** Tres divergencias entre la seccion normativa y el motor: `title`
  UTF-8 y tope 500 son transcripcion pendiente de P7; `applies_to` es una allowlist cuya lista
  publicada difiere de la efectiva -- y es la lista en la que I3 se apoya. P4 cierra ahi.
- **La SPEC NO sale de `draft-reviewed-informal` hasta que cierren LAS DOS.** Veredicto completo:
  `Area_comun/artifacts/Analista-TASK-0365-spec-memoria-hibrida-review-formal-verdict.md`.

**3. TASK-0364 (`in_progress`, Codex) -- vigilar si su GO murio.** `defer_started 18:06:54Z`,
`defers=4`, causa `worktree_residue_live`, ventana 7200 s -> **muerte dura hacia las 22:07 local del
12-ago**. La causa del residuo son los propios ficheros sin commitear de `personal/Codex/`: es
TASK-0337 (el guard de residuo veta sin mirar scope) mordiendo en vivo. Si murio, re-rutear mensaje
nuevo. **0364 saca a 0340 y 0347 de `blocked` y deja cerrar 0342.**

**4. TASK-0350 en `ready`** con el fix entregado (`192c5dea`) y AC5 enmendado; su RESP esta ruteada.

**5. Higiene y poda pendientes.** `open/` con 7 mensajes, varios consumidos. La poda esta VENCIDA
(`cold_start_tokens` 22523, `released_ratio` 91.89) y **BLOQUEADA**: exige claim sobre `CLAIMS.json`
ENTERO y choca con `CLAIM-20260812-Codex-TASK-0364`, `active` aunque expiro a las 17:36Z.

## COMO LO HAGO (loop gobernado + rieles)
- Ledger: TODA transicion por `runtime/submit_intent.py --actor-id Arquitecto`. Claim acquire ANIDADO con
  `scope` (incluida su propia fila `CLAIMS.json#<claim_id>`); release PLANO. Editar `Area_comun/state/*`
  a mano = drift HARD-FAIL.
- **Gatear por exit code real, sin pipe** (`cmd >/dev/null 2>&1; echo $?`). Un `| tail` devuelve el exit
  del tail y miente.
- **`scan_encoding` da FALSO ROJO transitorio mientras `submit_intent` tiene el `.ledger.lock`**
  (PermissionError al leerlo). Pasado hoy: re-correr y sale limpio. No es un byte no-ASCII real.
- Commit con **pathspec por lista explicita**, nunca `git add -A`. Trailers en el parrafo FINAL sin linea
  en blanco (`Task-Id:` + `Co-Authored-By:`; sin tarea -> `Task-Id: none` + `Ops-Reason:` <=120 chars).
- Subject `fix(`/`revert(`/`hotfix(` exige `Fixes-Task:`; para coordinacion usa `chore(`/`state(`/`coord(`.
- **validate POST-commit ANTES del push.** Memoria justo despues de cada commit.
- **TODO encargo a un peon lleva `task_id: TASK-NNNN` real** -- aunque sea review de SPEC. Sin tarea
  numerada con `scope_routes`, el arnes no produce descriptor, difiere en bucle y el mensaje MUERE a
  las 2 h sin error. Si no hay tarea, se REGISTRA una.
- **`scope_routes` de una review = lo que ESCRIBE** (`Area_comun/mailbox/open/`), no lo que lee. Meter
  ahi el codigo auditado choca con el claim del maker y difiere por `active_external_claim`.
- Tras superseder un mensaje, **borra su entrada del `<peer>_mailbox_cron.retry.json`**: archivar no
  desencola.
- **NO stagear artefactos del peer a medio escribir**: verifica `EXEC_EXIT` antes de commitear.
- ASCII puro en `Area_comun/`: escanear bytes >127 antes de commitear.
- Scratch: TODO bajo `D:/Aegis_Scratch/<proyecto>/<proposito>/`, jamas en la raiz del disco (DECISION-0104).
- **Cola por peon: maximo 2-3 mensajes vivos.** El defer mata a las 2 h. Un exec puede llegar a 75 min.

## LECCIONES CLAVE (el COMO durable)
- **Un invariante puede cumplirse por su LETRA y romperse por su NOMBRE.** I7 pasaba cualquier chequeo
  literal -- las 4 filas con `hot_required=1` tenian su `.md` caliente -- y murio al preguntar que
  poblacion deberia estar ahi. Antes de dar un invariante por cumplido, pregunta por su nombre.
- **Ante "sigue rojo pero es de TASK-XXXX": ABRE la XXXX y lee su `out_of_scope`.** Puede estar
  devolviendotelo por nombre, y entonces el rojo **no es de nadie**. Paso hoy con el paso 50 entre
  0347 y 0350. Exige id concreto de la tarea que lo ACEPTA; "es de otro" a secas no acredita.
- **Un AC que pide "el caso ENTERO verde" mientras el `out_of_scope` excluye otras causas es
  CONTRADICTORIO**: no se puede cumplir ni refutar. Es defecto del encargo. Enmiendalo con la enmienda
  FECHADA y visible, jamas en silencio.
- **Una puerta que aborta pronto OCULTA lo que hay detras.** Al matar la primera causa de un paso,
  presupuesta una segunda; no la trates como regresion.
- **Prueba PREEXISTENTE derivando del diff**, no corriendo el arbol anterior: lo que el cambio no toco
  no lo pudo introducir.
- **El silencio de un instrumento no es evidencia de progreso.** Un cron vivo + mensaje en `open/` +
  cero errores es el cuadro exacto de "esta trabajando" cuando no trabaja nadie.
- **Hora del RELOJ, jamas estimada.** Reincidi hoy (estampe 20:50 cuando eran las 20:33) despues de
  llevar la sesion entera exigiendolo.

## CANAL DE ORDENES + PENDIENTES

**Decidido por el operador en esta ventana (no re-preguntar):**
- **TASK-0353: CERRAR.** Hecho, con el residual declarado. Su sucesora SOLO TEST (mutante M2) **NO se
  abre** por ahora.
- **TASK-0367: promocion APROBADA**, ejecucion aplazada al proximo inicio.
- **No cargar a los peones** mientras el operador este en transito.

**Abierto con el operador:**
1. **NOVA puede arrancar** (respondido). Lo unico marcado como bloqueante: `COMMIT_TRAILERS.json` con
   `enabled: false` en Aegis -> encender con `start_commit`=su HEAD y solo tras verificar que sus
   arneses ya emiten `Task-Id:`. Sus skills apuntan a rutas inexistentes (no fallan a gritos: no hacen
   nada). Su hallazgo del hook con `EXIT=0` sin validar nada **es el mismo codigo que este hub envia**
   y falta censarlo aqui.
2. **Sucesora de TASK-0359** (la sonda escribe a mano `:1475`/`:1485`): sigue sin abrir.
3. **Dieta de triggers** (`branches: [main]`, `paths-ignore: personal/**`): DECISION propia.
4. **Los tres residuales del veredicto de 0365 que mas pesan**: las 222 aristas `implements` inertes
   al 100%, el alcance real de la deteccion agrupada de IBAN (7 separadores; la COMA no caza) y el
   cardinal "219 warnings" que no se re-deriva sin nombrar su poblacion.

## SIGUIENTE ACCION (al retomar, tras el cold-start)
1. Ver si el GO de TASK-0364 murio por defer (~22:07 del 12-ago). Si murio, re-rutear mensaje minimo.
2. **Rutear TASK-0367** (ya en `ready`): es el primer GO aprobado.
3. Promover y rutear **TASK-0368** a Codex en cuanto su cola baje a 1. **TASK-0369 la ejecuto yo.**
4. Higiene de `open/` en lote <=3-4 y reintentar la poda cuando 0364 libere su claim.
