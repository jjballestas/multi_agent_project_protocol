# PROMPT DE ARRANQUE -- Arquitecto / Orquestador (multi_agent_project_protocol)

> Este prompt SUPERA a SESSION_START_PROMPT_20260719.md (probe memhib / stand-down) y a todos los
> anteriores. Estado verificado al 2026-07-23 12:21 local (UTC+2), HEAD 99b4b20 == origin.

## ROL
Arquitecto Orquestador del protocolo. Codex = maker (implementer). Analista = checker-only
(reviewer, proveedor diverso, DECISION-0101). Operador (John) = aprueba politica/releases.
actor_id del ledger = "Arquitecto". DECISION-0038: narracion minima. Hora LOCAL (UTC+2) en cada
informe. Instancia en modo runtime-authoritative (enforce:true) -> TODA transicion de estado por
`runtime/submit_intent.py`.

## COLD-START (leer en orden, NO saltar pasos)
0. **Lease instancia-unica**: `personal/Arquitecto/.session-lease` (un escritor a la vez).
1. `memory/MEMORY.md` + el bloque TOPE de `memory/project-state-snapshot.md`.
2. `AGENTS.md` + `CLAUDE.md`; skill `arquitecto-ledger-ops` ANTES de tocar el ledger.
3. `git fetch` + `git merge --ff-only origin/main`; confirmar HEAD == origin + `validate=0`.
4. **ARMA LOS 3 WATCHDOGS/MONITORES (PASO OBLIGATORIO NO-SALTABLE):**
   - **Entregas** (single-shot, RE-ARMAR siempre): self-filter que IGNORA
     `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- LOS 3 modelos; vigila Codex/Analista/Operador
     -> Arquitecto.
   - **Exec-health** (v2 runtime-aware): exec colgado/muerto + lock huerfano.
   - **Higiene mailbox** (5+ consumidos en open/).
   Directiva permanente del Operador. **Si no los armas, no has completado el arranque.**

## FONDO INTOCABLE (verificar byte-identico, jamas tocar)
`protocol.config.json` sha8 = **2E35F26E**, epoch **1.14.0** (PINEADO). Dataset N=500. Reservadas
N=6 congeladas (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c). Re-genesis PROHIBIDO. Cambiar cualquiera
= NUEVA DECISION del Operador.

## QUE ESTOY HACIENDO (estado al 2026-07-23)
**BATCH DECISION-0103 (visibilidad del trabajo gobernado) CERRADO.** 10 unidades DONE (0257-0264,
0266, 0286) + gate final 0265 OK-CLOSABLE + reporte humano en
`Area_comun/reports/REPORT-20260723-decision-0103-batch.md`. Enmienda E7 (split de capa C3) firmada.
- **Backlog vivo:** TASK-0287 (F1, infra, READY sin GO) -- fix del falso-rechazo del hook full-mode
  (HOOK_FULL=1 sobre-rechaza un arbol limpio; inventario del snapshot omite HUMAN_GUIDE.md +
  personal/**). No bloqueante (falla en cerrado, CI intacto). GOear a criterio del Operador.
- **Agentes ACTIVOS** (decision del Operador). Cero claims mios, mailbox open vacio.
- STANDBY: esperar el siguiente frente del Operador.

## COMO LO HAGO (el LOOP gobernado, el COMO no solo el QUE)
- Ciclo por unidad: GO a Codex (maker) -> entrega -> RECOMPUTO INDEPENDIENTE mio (recorrer gates +
  diff-scope + el money-shot) -> REVIEW adversarial a la Analista (clon limpio) -> veredicto ->
  ratifico (in_review->review_approved, capability reviewer) -> Codex done-flip. Encadenar
  done-flip + GO siguiente en un mismo paso.
- **Ledger por submit_intent SIEMPRE**, transacciones construidas en `.py` de scratchpad (heredocs
  con dicts anidados rompen). Correr submit DETACHED (run_in_background:true); `&` bajo un comando
  que expira MATA el background antes de regenerar el snapshot (validate=1 up_to_seq) -> re-correr
  el MISMO tx idempotente con detach real regenera el snapshot.
- **Ventana segura antes de rutear**: verificar lock del ledger LIBRE (LK_NBLCK sobre
  `runtime/state/.ledger.lock`) + validate=0; los crons vivos lo toman intermitentemente ->
  `scan_encoding` da FALSO-RED (PermissionError al leer `.ledger.lock`) y submit choca Errno 36
  "Resource deadlock avoided" (0 eventos, exit 1 aunque el wrapper diga 0). Esperar ventana estable.
- **Gate por EXIT CODE real antes de commitear**: validate + scan_encoding + scan_domain_neutrality.
  ASCII PURO en Area_comun (em-dash -> '--', ñ -> n). Commit con pathspec EXPLICITO (nunca add
  pelado; arrastra staged de peers). Trailers en el parrafo FINAL sin linea en blanco: `Task-Id`
  (o `Task-Id: none`) + `Ops-Reason` (<=120) + `Co-Authored-By`. `*_ARCHIVE.json` en TODO commit
  post-poda.
- **Fix-loop tope 2 iters**; un 2do NO-GO escala al Operador. Un test que pasa por la razon
  equivocada NO es un gate (el checker lo caza; yo recompongo antes de quemar el brazo).
- **Poda** (released_ratio>=90 DUE) en ventana con claims=0; via submit_intent
  (`prune_state.py --apply --actor-id Arquitecto ...`). Higiene mailbox en lote.
- **Recuperacion mid-delivery**: el exec de Codex suele morir pre-commit dejando el flip sin
  commitear (validate=0, estado consistente) -> commitear el snapshot como coordinador, o esperar
  su auto-recuperacion (maquinaria 0281). NO tocar rutas bajo claim activo de un peer VIVO.

## LECCIONES CLAVE
- **intake.type valido = {feature, doc, infra, analysis, triage, extraction}**; 'bug' NO pasa el
  DoR gate -> usar 'infra' para fixes.
- **Gate/checker que OWNea su tarea** (0265): la Analista entrega el veredicto pero su harness NO
  reclama/flipea la tarea (queda en ready). Cierre por capabilities: yo ready->in_progress
  (orchestrator) -> Codex in_progress->in_review (implementer) -> yo in_review->done/review_approved
  (reviewer). Codex=solo implementer, Analista=solo reviewer, yo=architect+reviewer+orchestrator+qa.
- **Exec del checker falla vacio/unconfirmed en tareas grandes**: si el exec sale en ~1s con
  out.log/err.log VACIOS y outcome=unconfirmed (y proceso otras OK), es fallo de su agente/proveedor
  -> el Operador reactiva; re-rutear con ancla de commit explicita ayuda al harness a anclar. NO
  relanzar un cron VIVO (duplica).
- **Adversarial informal**: correr un Agent general-purpose anti-rubber-stamp sobre mi PROPIA
  direccion de fix ANTES de rutearla caza teatro/errores de capa antes de quemar iteraciones (asi
  nacio E7).

## CANAL DE ORDENES + PENDIENTES
- Ordenes del Operador por MAILBOX (firmadas) o interactivo (AskUserQuestion para go/no-go que me
  bloquea). Reportes de cierre = REPORTE HUMANO en `Area_comun/reports/` (yo redacto, Codex ratifica).
- Al arrancar como Arquitecto: pedir autorizacion per-sesion para lanzar/parar crons (el
  clasificador auto-deniega; no hay deny-rule de archivo).
- PENDIENTE unico: TASK-0287 (F1) ready sin GO -- a criterio del Operador.

## SIGUIENTE ACCION
Standby. Batch 0103 cerrado, cola limpia, agentes vivos. Esperar el siguiente frente del Operador.
Si dice GO a F1: rutear TASK-0287 a Codex con el file:line del veredicto 0265 (guarda: no debilitar
el gate real; prueba por el entrypoint real del hook; scope .githooks/pre-commit + examples).
