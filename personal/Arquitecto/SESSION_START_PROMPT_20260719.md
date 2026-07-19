# SESSION START PROMPT - Arquitecto/Orquestador (2026-07-19, checkpoint ~13:50 local)

> SUPERSEDE a SESSION_START_PROMPT_20260718.md (historico, no borrar).
> Test del lector frio: con este archivo + memory/MEMORY.md + el bloque TOPE del
> snapshot, una sesion nueva retoma sin el chat.

## ROL
Arquitecto/Orquestador del protocolo (actor_id ledger = "Arquitecto"). Codex = maker
(cron CLI), Analista formal = proveedor diverso (DECISION-0101), checker 0101 informal =
subagent anti-rubber-stamp, operador (John) = aprueba lo soberano; el ASESOR relaya
DIRECTIVAs por el mailbox del hub. DECISION-0038: narracion minima. HORA LOCAL (UTC+2)
en cada informe, TOMADA DEL RELOJ (no estimada; me mordio 2x).

## COLD-START (ejecutar EN ORDEN; no saltar)
0. Lease instancia-unica: personal/Arquitecto/.session-lease (si hay lease fresco <30min
   de OTRO session_id: no coordinar, consultar al Operador). Al cerrar sesion: borrarlo.
1. memory/MEMORY.md + memory/project-state-snapshot.md (bloque TOPE = accion inmediata).
2. Skill arquitecto-ledger-ops ANTES de cualquier escritura de ledger.
3. git fetch + git merge --ff-only origin/main (hub); auto-poll de AMBOS repos:
   hub D:\Agentes\multi_agent_project_protocol (remoto SI) e instancia Nova-Payroll
   D:\Agentes\NOVA-Suite\Nova-Payroll\Aegis (LOCAL-ONLY, JAMAS push; citar commits como
   "instancia <sha> (local-only)"). git log -3 + open/ + claims + validate en ambos.
4. **ARMA LOS 3 WATCHDOGS OBLIGATORIOS -- si no los armas, NO has completado el
   arranque**: (a) watch de entregas del hub (single-shot, RE-ARMAR tras cada disparo;
   self-filter ignora Co-Authored-By: Claude (Opus|Fable|Sonnet) -- LOS 3 modelos -- +
   Co-Authored-By: asesor + ^checkpoint\(asesor\)); (b) watchdog salud-exec instancia
   (persistente; falsa alarma con Ollama cargado = diagnostico read-only primero);
   (c) watchdog higiene mailbox hub (persistente, umbral 10). Scripts exactos en la
   skill arquitecto-monitor-coordina. NOTA: si los agentes siguen STOPPED (ver abajo),
   (b) no alarmara -- armalo igual, es barato y cubre la reactivacion.

## FONDO INTOCABLE
Dataset N=500; protocol.config.json byte-identico sha8 2E35F26E; epoch 1.14.0. La
instancia Nova-Payroll tiene su config PINEADO por chain.genesis (agentes nuevos =
re-genesis = NO). La instancia NO tiene .slim.json: al commitear estado se stagean SOLO
los 3 state json + el .md de la tarea + events.jsonl + snapshot.json.

## QUE PASO (2026-07-19, cierre) -- PROBE MEMHIB COMPLETO + STAND-DOWN
- PROBE PRIVADO DE MEMORIA HIBRIDA: LAS 6 CELDAS CERRADAS (B / B-bis / A / D / C /
  A-bis; TASK-0021..0027 done en la instancia). A-bis (TASK-0027): matriz 2x3 completa,
  sets sellados ex-ante (9f83a59 T1 / a29628d T2), gradings mios + SELLO 0101 con
  recomputo independiente adversarial = GO-CON-HALLAZGOS (artefacto
  VEREDICTO-0101-TASK-0027-ABIS-GO.md, instancia 00300dc). Resultado: CAPACIDAD EXITO en
  ambos trials (CON 20/20 fidelidad 100 vs cold puro 0/20) + COMPARTIR cross-agente EN
  AMBOS SENTIDOS (T1 Codex->Analista-0101; T2 Analista-0101->Codex-0101, sha-verificado)
  + AHORRO INCONCLUSO (split T1 -18.7pct / T2 +2.8pct + confusor H1). REPORTE GLOBAL al
  hub PUSHEADO (aec91be): capacidad-con-integridad SI, eficiencia de tokens NO; la
  atestacion cazo 2x la contaminacion del propio harness (NO-GO serie C + H1 A-bis).
- STAND-DOWN por orden del operador (~13:45): crons MUERTOS (instancia codex 49220,
  instancia analista 14700, hub analista 36900; hub codex ya muerto), monitores parados,
  lease borrado. El operador reactiva agentes para el proximo proceso.
- HIGIENE: hub open/ = 6 vivos (REPORTEs sustantivos para el operador). Instancia: hilo
  0027 archivado completo (21 msgs, 7 txs); QUEDAN 40 msgs viejos de celdas B..C =
  higiene stand-down PENDIENTE (mailbox_archive orchestrator, lotes de 3).

## PENDIENTES SOBERANOS (no iniciar sin orden del operador)
1. FASE B memhib: estudio sellado citable de la memoria hibrida (pre-registro lo redacta
   el ASESOR; yo SOLO anclo el intent del sello). DISTINTO de Contabilidad N=6.
2. Contabilidad N=6: pre-registro YA SELLADO (DECISION-0094, sha 28fd963b); espera GO
   build post-30-jul + confirmacion jheredia (prep 100pct: NOVA TASK-9401..9406 ready).
3. Firma DECISION-0102 (no-adopcion peones; draft en personal/Arquitecto/).
4. Promocion memoria hibrida al MASTER del hub: AGENDADA Fase 3+ post-ventana-medida
   (DECISION-0100, via export 0096). HOY el hub NO tiene scripts/memory -> una instancia
   nueva NO nace con memhib. Adelantarla = nueva DECISION del operador. Port manual por
   instancia posible via runbook U5 (adopcion de instancia, no master).

## COMO LO HAGO (loop por celda, rodado ~10x; sigue vigente para el proximo proceso)
registro tx atomica (claim anidado 4 fragmentos -> upsert -> ready -> release plano) ->
ACTION a Codex (cron instancia; waiter grep -ac EXEC_EXIT > N con deteccion cron-muerto)
-> exec entrega -> grading/verificacion contra el err.log REAL (fuentes + orden
materializar-antes-de-mv + tokens "tokens used" al final del log) -> sello 0101 en
BACKGROUND (subagent anti-rubber-stamp; los 100pct se atacan mas duro -- cazo H1 que yo
no vi) -> ratificar (tx claim+status+release) -> ACTION doneflip (solo Codex tiene
implementer) -> REPORTE al hub con numeros TAL CUAL + caveats declarados. Gates por
EXIT-CODE antes de todo add. Hub: trailers Task-Id + Ops-Reason<=120 MEDIDO en paso
aparte; push tras validate post-commit. Instancia: sin trailers, Co-Authored-By SIEMPRE,
JAMAS push. Higiene por lotes <=3 con claim file-scoped (author=autor real,
relayed_by=Arquitecto, message_id sin .md) -- 7 lotes seguidos corrieron limpios.
Memoria tras cada commit.

## LECCIONES CLAVE (las que muerden; nuevas de esta sesion marcadas *)
- *ESTAMPA DE HORA: SIEMPRE del reloj (date), JAMAS estimada. Reincidi (2 estampas
  corregidas en 21e6f27). Antes de escribir una hora en un MSG/artefacto: date +%H:%M.
- *COLD-START DEL CRON vuelca personal/Codex/ RECURSIVO al contexto: controla el volcado
  TAMBIEN para artefactos PERMITIDOS si quieres brazos/mediciones homogeneas (H1: el
  destilado T2 entro integro al contexto de T2-CON pre-ACTION y confundio el costo).
  Cuarentena fisica previa (git mv) para TODO lo que no deba pesar en el exec.
- *Los archivos con respuestas/claves de una medicion (RESULTADO master, sets) son
  vectores de contaminacion para execs posteriores: materializacion POR-BRAZO en archivo
  propio + prohibicion de abrir los previos + consolidacion solo al cierre.
- *Reglas de normalizacion de grading: TODAS ex-ante en el set (palabra==cifra,
  decimales numericos, 2-campos); anadir una regla en el grading = hallazgo del sello.
- Validador hub: requires_response exige requested_action Y question; la bandera LITERAL
  en el CUERPO tambien dispara -> parafrasear. Mensajes ajenos rotos: responder +
  archivar, JAMAS editarlos.
- Invariante handoff-release: tarea in_review sin claim del owner; la remediacion exige
  rechazo formal (reviewer la devuelve a in_progress primero).
- Declaraciones de fuentes se derivan DEL LOG (err.log), no de la intencion.
- Enmiendas de MEDIOS con declaracion fechada = via valida; umbrales/N JAMAS post-datos.
- Ollama en exec largo = watchdog falsa alarma (diagnostico read-only pid + /api/ps).
- git add en bloque falla ENTERO si una ruta no existe (la instancia no tiene slims) ->
  el archivo nuevo queda sin stagear y el commit por pathspec revienta; add por partes.

## CANAL DE ORDENES
Ordenes del Operador llegan por MAILBOX del hub via Asesor (a veces untracked: el
auto-poll por NOMBRE los caza) o por chat directo. Los agentes estan STOPPED: rutear
ACTIONs a un cron muerto NO hace nada -- verificar liveness (pid) antes de rutear;
si el proceso nuevo exige peers, pedir al operador que reactive los crons.

## SIGUIENTE ACCION CONCRETA
Standby. Al abrir la proxima sesion: cold-start completo + esperar la decision del
operador (Fase B memhib / GO N=6 / firma 0102 / reactivacion de agentes). Si hay ventana
idle autorizada: higiene stand-down de los 40 msgs viejos de la instancia (lotes de 3).
