# SESSION START PROMPT -- Arquitecto (2026-08-12)

> SUPERA a SESSION_START_PROMPT_20260801.md (no lo borres). Estado REAL verificado al cierre
> 2026-08-12 14:35 local (UTC+2). **PAUSA PLANIFICADA:** el operador viaja y desconecta el equipo de
> internet; los crons quedaron parados con marcador limpio, no caidos.

## ROL
Arquitecto / Orquestador de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Codex=maker/implementer, Analista=checker-only, operador(John)=aprueba. actor_id ledger="Arquitecto".
DECISION-0038 narracion minima. HORA local (UTC+2) en cada informe. Reportes con dataset recontado.

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
5. Pide autorizacion per-sesion al operador para lanzar/parar crons (powershell .ps1) + taskkill.
6. **Los crons estan PARADOS a proposito** (marcador `.stop` en `.protocol-tmp/<peer>_mailbox_cron/`).
   Para relanzarlos: BORRA el marcador y lanza
   `powershell -NoProfile -File personal/<Peer>/<peer>_mailbox_cron.ps1` (run_in_background). Verifica por
   CONDUCTA (lease con task_id/work_scope/state), nunca por git log.
7. **Verifica los runners propios** (nuevos, DECISION-0112): `gh api repos/jjballestas/
   multi_agent_project_protocol/actions/runners` -> `protocol-win` y `protocol-linux` deben salir `online`.
   Si Linux no esta, la distro de WSL se cerro: relanza el ancla `wsl -d Ubuntu -- sleep infinity`.

## FONDO INTOCABLE (byte-identico, jamas tocar)
`protocol.config.json` sha8 = **2E35F26E**, epoch **1.14.0** PINEADO. Dataset **N=500**. Re-genesis
PROHIBIDO. Cambiar cualquiera = NUEVA DECISION.

## QUE ESTOY HACIENDO (estado al cierre)

**CERRADAS hoy: TASK-0354 y TASK-0359**, las dos con firma del checker.

**DECISION-0112 aprobada y registrada: la CI canonica pasa a runners PROPIOS.** El plan real es GitHub
Free = 2.000 min/mes (Copilot Pro no aporta minutos) y la cadencia consume ~18.000: nueve veces el cupo.
El operador descarto subir el limite (~130-150 $/mes) y publicar el repo -- que ademas PROHIBIRIA el
arreglo, porque un self-hosted en repo publico deja que un PR ajeno ejecute codigo donde viven las llaves
de firma. Medido con control en la misma corrida (run `31588931912`): hosted BLOQUEADO 0/0 pasos, los dos
propios SUCCESS 8/8 con gate real, y `timing.billable` ni los menciona. Detalle de montaje y las cuatro
trampas: memoria [[runners-self-hosted-esquivan-el-cupo]].

**EN VUELO al pausar:**
- **TASK-0364** (`in_progress`, Codex): el corte de `validate.yml` a los runners propios. **Su exec fue
  CORTADO POR EL TECHO DURO a las 14:47:43** (`EXEC_EXIT code=-1 outcome=transient` + `ROLLBACK_DEFER
  reason=head_changed` + `RETRY_SCHEDULED 1/3`), no termino. **Los OCHO commits SI estan pusheados**
  (`cefd5e02` mueve los gates, `f23ef6a7` wrapper pwsh, `6b47e146` safe-directory, `6aee19ac` Python
  provisionado, mas cuatro `docs(...)` de hallazgos de run vivo): el trabajo no se perdio, pero **no
  hubo flip a `in_review` ni handoff**. El GO sigue VIVO en `open/`, fuera del `seen.json` y con entrada
  en `codex_mailbox_cron.retry.json` -> **se re-ejecuta SOLO al relanzar el cron**. Decidir antes si se
  quiere eso o si conviene rutear un mensaje de solo-cierre anclado al ultimo commit.
- **TASK-0353** (`in_review`): el checker firmo **OK-CLOSABLE** en r5 sobre `c92be390`. **NO la cerre a
  proposito** -- ver PENDIENTES.

## COMO LO HAGO (loop gobernado + rieles)
- Ledger: TODA transicion por `runtime/submit_intent.py --actor-id Arquitecto`. Claim acquire ANIDADO con
  `scope` (incluida su propia fila `CLAIMS.json#<claim_id>`); release PLANO. Editar `Area_comun/state/*`
  a mano = drift HARD-FAIL.
- Gatear por **exit code real**, sin pipe (`cmd >/dev/null 2>&1; echo $?`). Un `| tail` devuelve el exit
  del tail y miente.
- Commit con **pathspec por lista explicita**, nunca `git add -A`. Trailers en el parrafo FINAL sin linea
  en blanco (`Task-Id:` + `Co-Authored-By:`; sin tarea -> `Task-Id: none` + `Ops-Reason:` <=120 chars).
- Subject `fix(`/`revert(`/`hotfix(` exige `Fixes-Task:`; para coordinacion usa `chore(`/`state(`/`coord(`.
- **validate POST-commit ANTES del push.** Memoria en el MISMO commit que el trabajo.
- Higiene de mailbox ACOPLADA al mismo gate de commit: archivar consumidos en lotes <=3-4.
- ASCII puro en `Area_comun/`: escanear bytes >127 antes de commitear.
- **NO stagear artefactos del peer a medio escribir**: el checker escribe su veredicto en el arbol
  mientras tu commiteas.
- Scratch: TODO bajo `D:/Aegis_Scratch/<proyecto>/<proposito>/`, jamas en la raiz del disco (DECISION-0104).

## LECCIONES CLAVE (el COMO durable)
- **Refutar enumerando es el mismo defecto que reconocer enumerando.** TASK-0354 costo CINCO vueltas de
  texto: mi parrafo refutaba el cardinal 69 citando cuatro cifras y concluyendo "ninguna da 69" -- pero
  las cuatro eran tres esquinas de una tabla de dos ejes cuya cuarta esquina vale **exactamente 69**.
  Sustituir listas por su criterio de pertenencia, siempre.
- **Un cardinal publicado declara su UNIDAD.** 73 invocaciones y 72 ficheros no son el mismo conjunto; su
  coincidencia era accidental. Antes de decir que dos cifras se corroboran, nombrar que cuenta cada una.
- **Cuando la correccion es transcripcion, se transcribe.** Mi unica desviacion declarada (conservar cuatro
  cifras "porque estaban verificadas") fue justo lo que destapo el defecto siguiente.
- **El hand-feed se muda de coordenada.** TASK-0359: primero `$before`, luego el calendario del muestreo,
  ahora el deadline (`:1485`). Preguntar que ENTRADAS escribe el test en vez de dejar que produccion las
  calcule, y mutar la semilla.
- **Verificar por CONDUCTA, no por estado declarado.** Un servicio "Running" no prueba que pueda correr un
  job: hubo que lanzar la sonda y mirar los 8 pasos.
- **Control en la MISMA corrida.** Es lo que hizo valer la medicion de los runners: sin el job hosted
  bloqueado al lado, "el self-hosted funciona" no discriminaba nada.

## CANAL DE ORDENES + PENDIENTES

**Espera decision del operador (por orden de valor):**
1. **TASK-0353: cerrar o escalar.** El checker firmo OK-CLOSABLE, pero senala que la entrega **retiro el
   guard ansioso ENTERO**, no solo la resta que se autorizo. Eso es alcance por encima de lo pedido y es
   decision del operador. Su veredicto pide ademas abrir sucesora SOLO TEST con el mutante M2 como AC de
   partida: `schema_report` que borra solo `attempt_id` debe MORIR por conducta. Residuales nuevos R14,
   R15, R16; R13 y R10 CERRADAS. Mensaje vivo en `open/`.
2. **Sucesora de TASK-0359**: la sonda aun escribe a mano `:1475` y `:1485`; un mutante de un caracter en
   `:1485` falsifica el texto del contrato con el negativo VERDE. El checker NO pidio vuelta cuatro: lo
   entrega como sucesora y la decision es del operador.
3. **Dieta de triggers** (`branches: [main]`, `paths-ignore: personal/**` = 27% de los commits): pierde
   granularidad de biseccion, va en DECISION propia, no se cuela en TASK-0364.
4. **Runner de Windows como servicio: corre bajo `NT AUTHORITY\Servicio de red`**, no bajo el usuario (el
   operador usa PIN y cuenta MicrosoftAccount, no hay contrasena que dar). Funciona porque se le dio
   lectura/ejecucion sobre el Python del usuario. Residual declarado: no hereda el perfil (no ve
   `.gitconfig` ni variables personales).

## SIGUIENTE ACCION (al retomar, tras el cold-start)
1. `git fetch` y mirar si Codex llego a pushear `6b47e146` y la entrega de **TASK-0364**. Si quedo a
   medias, ese es el primer frente: es la tarea que saca a **0340 y 0347** de `blocked` y permite cerrar
   **0342** -- la cascada que llevaba dias parada por la facturacion.
2. Llevar al operador las decisiones 1 y 2 de PENDIENTES (0353 y la sucesora de 0359).
3. Relanzar los crons SOLO cuando haya cola real y con autorizacion (paso 6 del cold-start).
