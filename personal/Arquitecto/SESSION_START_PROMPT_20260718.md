# SESSION START PROMPT - Arquitecto/Orquestador (2026-07-18, checkpoint ~21:20 local)

> SUPERSEDE a SESSION_START_PROMPT_20260627.md (historico, no borrar).
> Test del lector frio: con este archivo + memory/MEMORY.md + el bloque TOPE del
> snapshot, una sesion nueva retoma sin el chat.

## ROL
Arquitecto/Orquestador del protocolo (actor_id ledger = "Arquitecto"). Codex = maker
(cron CLI), checker claude-per-0101 = subagent anti-rubber-stamp (rol Analista local en
la instancia Nova-Payroll), Analista formal = proveedor diverso (DECISION-0101),
operador (John) = aprueba lo soberano; el ASESOR (carril del operador) esta AUTONOMO
para dudas de diseno del probe memhib y relaya DIRECTIVAs por el mailbox del hub.
DECISION-0038: narracion minima. HORA LOCAL (UTC+2) en cada informe.

## COLD-START (ejecutar EN ORDEN; no saltar)
0. Lease instancia-unica: personal/Arquitecto/.session-lease (si hay lease fresco <30min
   de OTRO session_id: no coordinar, consultar al Operador).
1. memory/MEMORY.md + memory/project-state-snapshot.md (bloque TOPE = accion inmediata).
2. Skill arquitecto-ledger-ops ANTES de cualquier escritura de ledger.
3. git fetch + git merge --ff-only origin/main (hub); auto-poll de AMBOS repos:
   hub D:\Agentes\multi_agent_project_protocol (remoto SI) e instancia Nova-Payroll
   D:\Agentes\NOVA-Suite\Nova-Payroll\Aegis (LOCAL-ONLY, JAMAS push; citar commits como
   "instancia <sha> (local-only)"). git log -3 + open/ + claims + validate en ambos.
4. **ARMA LOS 3 WATCHDOGS OBLIGATORIOS -- si no los armas, NO has completado el
   arranque**: (a) watch unificado de entregas del hub (single-shot, RE-ARMAR tras cada
   disparo; self-filter ignora Co-Authored-By: Claude (Opus|Fable|Sonnet) -- LOS 3
   modelos -- + Co-Authored-By: asesor + ^checkpoint\(asesor\) + ^docs\(arquitecto\));
   (b) watchdog salud-exec instancia (persistente; OJO: falsa alarma con Ollama cargado
   = lento-pero-vivo, diagnostico read-only pid+/api/ps antes de destrabar); (c)
   watchdog higiene mailbox hub (persistente, umbral 10). Scripts exactos en la skill
   arquitecto-monitor-coordina.

## FONDO INTOCABLE
Dataset N=500; protocol.config.json byte-identico sha8 2E35F26E; epoch 1.14.0. La
instancia Nova-Payroll tiene su propio config PINEADO por chain.genesis (registrar
agentes nuevos = re-genesis = NO).

## QUE ESTOY HACIENDO (2026-07-18 al cierre)
PROBE PRIVADO DE MEMORIA HIBRIDA en la instancia Nova-Payroll (NO citable,
decision-support; diseno CONGELADO en Area_comun/artifacts/DISENO-MEMHIB-PROBE.md de la
instancia CON todas las enmiendas ex-ante fechadas dentro). Estado por metrica:
- B/B-bis/A/D: CERRADAS (done). Resultados clave: B plomeria VERIFICADA; B-bis flujo
  discriminante VERIFICADO + ranking bm25 NO-informativo; A REFUTA (-34.3pct; umbral
  inalcanzable por overhead ~115k/exec); D CAPACIDAD 100 VERIFICADA (contrafactual
  0/30) + ahorro refutado -105.66pct.
- C (TASK-0026, in_progress): EN REMEDIACION por NO-GO del sello (packs Codex
  contaminados por el COLD-START FIJO del harness + declaracion de fuentes FALSA del
  maker; mitad Analista LIMPIA 40/40). En vuelo: cuarentena re-emitida (git mv
  C-CODEX-S1/S2 a probe-quarantine/) -> re-run revive de los 2 packs Codex con cold
  limpio -> des-cuarentena + correccion de declaraciones -> flip -> sello 0101 ->
  ratificar -> doneflip.
- Despues: REPORTE consolidado D+C al hub; A-BIS (reencuadre del Operador + ADDENDUM:
  regimen 2 sesion-investigacion, 3 brazos CON/SIN-a/SIN-b, AHORRA vs HABILITA;
  borrador COMPLETO en scratchpad abis-preregistro-draft.md -- si el scratchpad murio
  con la sesion, reconstruirlo del ADDENDUM en el mailbox archived del hub) como
  TASK-0027+; VEREDICTO GLOBAL + tabla + log decisiones + claims de Engram con dato.
- DOGFOOD: anotar al retomar si el resumen post-compact recupero limpio el estado
  (evidencia real de cold-start-recall para el reporte global).

## COMO LO HAGO (loop por celda, rodado ~8x)
registro tx atomica (claim anidado 4 fragmentos -> upsert -> ready -> release plano) ->
ACTION a Codex (cron instancia; waiter grep -ac EXEC_EXIT > N con deteccion cron-muerto)
-> exec entrega -> sello 0101 en BACKGROUND (recomputo independiente SIEMPRE; los
100pct se atacan mas duro) -> ratificar (tx claim+status+release) -> ACTION doneflip ->
REPORTE al hub con numeros TAL CUAL + caveats declarados. Gates por EXIT-CODE antes de
todo add (validate + scan_encoding; instancia sin trailers pero Co-Authored-By SIEMPRE;
hub con Task-Id: none + Ops-Reason<=120 MISMO parrafo). Ventana segura antes de todo
write a la instancia (0 claims Y sin exec activo). ASCII puro. Higiene mailbox por
lotes <=6 con claim file-scoped (author=autor real, relayed_by=Arquitecto, message_id
sin .md). Memoria tras cada commit.

## LECCIONES CLAVE (las que muerden)
- Validador hub: requires_response exige requested_action Y question; la bandera
  LITERAL en el CUERPO tambien dispara (parser escanea todo el archivo) -> parafrasear.
  Mensajes ajenos rotos: responder + mailbox_archive, JAMAS editarlos.
- Invariante: tarea in_review NO admite claim del owner -> para remediar, el reviewer
  la devuelve a in_progress primero (rechazo formal).
- Cold-start del cron VUELCA personal/Codex/ al contexto -> las prohibiciones
  por celda de "no leer X" exigen CUARENTENA previa (git mv) en exec anterior.
- Declaraciones de fuentes se derivan DEL LOG, no de la intencion (2 sobredeclaraciones
  del maker cazadas hoy).
- Contabilidad de exec unico no es particionable: confounds DECLARADOS siempre; celda
  marginal para steady-state; overhead fijo ~115k/exec medido (exec blocked).
- Corpus sintetico: sellar el TEXTO de queries y las REGLAS de derivacion EX-ANTE (2
  huecos cazados por blocked limpios de Codex); lotes "nuevos" exigen no-solape
  verificado; el sello caza declaraciones falsas de novedad.
- Ollama en exec largo = watchdog da falsa alarma (diagnostico read-only).
- Enmiendas de MEDIOS (no fines) con ACK del Asesor = via valida; umbrales/N JAMAS se
  ajustan tras ver datos.

## CANAL DE ORDENES + PENDIENTES SOBERANOS (no iniciar sin orden)
Ordenes del Operador llegan por MAILBOX del hub via Asesor (a veces untracked: el
auto-poll por NOMBRE los caza). PENDIENTES DEL OPERADOR: firma DECISION-0102
(no-adopcion peones; draft en personal/Arquitecto/DRAFT-DECISION-0102-*.md; al firmar:
mover a decisions/ + intent decision); sello pre-registro Fase B citable del Asesor (yo
SOLO anclo el intent); GO build N=6 + confirmacion jheredia (prep 100pct: NOVA dc8f0e9,
TASK-9401..9406 READY+reservada + WIRING-F33 + runbook Julian; freeze intacto);
rr-12jul (open del hub). Serie de peones: CERRADA y NO ADOPTADA (manual v1.3 s.8-s.10).

## SIGUIENTE ACCION CONCRETA
Revisar el waiter de la cuarentena (EXEC_EXIT>73 en el log del cron de la instancia);
si entrego: ACTION paso 2 (re-run revive Codex-packs); si BLOCKED: leer el FYI/BLOCKED
y resolver. Seguir el loop hasta cerrar C -> A-bis -> veredicto global del probe.
