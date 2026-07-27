# PROMPT DE ARRANQUE -- Arquitecto / Orquestador (multi_agent_project_protocol)

> SUPERA a SESSION_START_PROMPT_20260724.md y anteriores.
> Estado verificado al 2026-07-27 ~03:00 local (UTC+2), HEAD 34a7b8d == origin, validate=0.

## ROL
Arquitecto Orquestador. Codex = maker. Analista = checker-only (proveedor diverso, DECISION-0101).
Operador (John) = aprueba politica/releases. actor_id ledger = "Arquitecto". DECISION-0038: narracion
minima. HORA LOCAL (UTC+2) ACTUAL en cada informe (el reloj avanza; nunca cachees). Instancia
runtime-authoritative (enforce:true) -> TODA transicion por `runtime/submit_intent.py`.

## COLD-START (en orden, no saltar)
0. **Lease instancia-unica:** `personal/Arquitecto/.session-lease` (un escritor; puede estar STALE, re-tomar).
1. `memory/MEMORY.md` + bloque TOPE de `memory/project-state-snapshot.md`.
2. `AGENTS.md` + `CLAUDE.md`; skill `arquitecto-ledger-ops` ANTES del ledger.
3. `git fetch` + `git merge --ff-only origin/main`; confirmar HEAD==origin + validate=0 (~2min, timeout amplio).
4. **ARMA LOS 3 WATCHDOGS (PASO OBLIGATORIO NO-SALTABLE):** (a) Entregas single-shot con self-filter que
   IGNORA `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- LOS 3 modelos; vigila Codex/Analista/Operador->
   Arquitecto; RE-ARMAR siempre. (b) Exec-health (exec colgado/muerto + lock huerfano + err.log CONGELADO
   0-byte/mtime>13min). (c) Higiene mailbox (>=10 consumidos). **Si no los armas, no completaste el arranque.**

## FONDO INTOCABLE (byte-identico, jamas tocar)
`protocol.config.json` sha8 = **2E35F26E**, epoch **1.14.0** PINEADO. Dataset N=500. Reservadas N=6
(R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c). Re-genesis PROHIBIDO. Cambiar cualquiera = NUEVA DECISION.

## QUE ESTOY HACIENDO (al 2026-07-27)
**SESION ANTERIOR CERRADA. SIGUIENTE: arrancar el DESARROLLO del Aegis Front.** El Operador arrancara con
un **"goal"**; el **PRIMER entregable recibe revision adversarial** (el lo pidio explicito). Cerrado la
sesion pasada: DECISION-0104 (regla scratch root inquebrantable) + TASK-0295 (detector) + TASK-0296
(enforcement; fix-loop 2 iters, evidencia viva doble: B1 quoting + B2 raiz-de-volumen) done; guardarailes
documentados (HUMAN_GUIDE 18.1 + Notion); mailbox VACIO; poda aplicada; limpieza de D:/ raiz (~49 GB).
- **TASK-0178 (Aegis Front) -- DISENO ENTREGADO Y LISTO PARA CONSTRUIR:** deliverable
  `Area_comun/artifacts/DESIGN-0178-aegis-front.md` (commit 34a7b8d; status sigue `proposed`, se promueve al
  arrancar el desarrollo). Reencuadrado tras debate largo + critica adversarial. Puntos clave del diseno:
  - **3 capas:** L1 observacion (read-model, streaming del Arquitecto, como VS Code) / L2 asistente
    no-firmante (Asesor productizado; draftea, JAMAS firma) / L3 firma humana consciente (el front FUERZA
    ver+firmar). **Invariante I1: el Arquitecto NUNCA firma ni actua por el usuario** (lo dirige el flujo
    gobernado, no un chat). I2: firmar es acto humano consciente. I3: privada humana solo en su maquina.
  - **App auto-provisionable** (envuelve new_instance.py + ceremonia born-operational). Orden: alta humano
    -> llaves humanas locales -> alta agentes + mapeo LLM->rol -> firmas de agentes -> genesis soberano -> ancla.
  - **CLAVES separan ROLES (siempre 3: Arq/Codex/Analista) vs LLMs = MOTOR (mapeo 1..N).** Escalera honesta:
    1 LLM = review debil (avisar), 2 = proveedor-diverso, 3+/peones = pleno.
  - **SOBERANO** (sin dataset global de clientes). **Dos modos de medicion:** DUENO (tus instancias -> tu
    dataset global, es tu trabajo) / SOBERANO (cliente -> cero egreso). Ancla = **Sigstore/Rekor** (gratis).
  - **Open-core Apache-2.0** (motor+spec). **FOSO = el CORPUS de datos normativos** (NO certificacion,
    imposible ISO 17065; NO anclaje). Aparato de mercado (licencia/distribucion/marca) = fase POSTERIOR
    gateada por reality-check de desplegabilidad. En paralelo: servicio de linea-base (revenue + corpus).
  - **FRONT-INTERNO-PRIMERO:** construir ya = operar instancias propias + gobernar la migracion **T0
    Access->SQL Server** + medir. T0 arranca el reloj del corpus (cada dia sin registrar = dataset tirado).
  - **CODIGO en `Zeus-protocol` bajo `D:/Agentes/Zeus/`, NUNCA el hub** (diseno/gobernanza aqui, codigo
    alla, cross-atestado por DECISION-0095). Stack front: React+TS+Vite (paridad NOVA).
- **Agentes ACTIVOS** (Codex + Analista crons vivos). Cero claims mios, mailbox open vacio.

## COMO LO HAGO (loop gobernado -- el COMO)
- **Ciclo por unidad:** GO a Codex (maker) -> RECOMPUTO INDEPENDIENTE mio (money-shots por el ENTRYPOINT
  REAL, no confiar en la evidencia del maker; ESTA SESION cazo B1/B2 solo al reproducir el caso exacto en el
  instalador real via -WhatIf + CommandLineToArgvW) -> REVIEW adversarial a la Analista (clon limpio) ->
  veredicto -> ratifico in_review->review_approved -> Codex flip review_approved->done (implementer). Design
  tasks: el flip a in_review/done tambien exige implementer=Codex.
- **Ledger por submit_intent SIEMPRE**, tx en `.py` de scratchpad, DETACHED (run_in_background:true; `&` bajo
  comando que expira mata el snapshot-regen). Claim ANIDADO + scope#self + fragmentos + el `.md` de la tarea.
  Register+GO = una tx (claim + task_upsert proposed + task_status proposed->ready + release). Ratify =
  claim + task_status(in_review->review_approved) + release. Rechazo (NO-GO) = flip in_review->in_progress
  ANTES de que el maker reclame (invariante handoff-release). Verificar out.json (applied) + snapshot==head.
- **Gate por EXIT CODE:** validate + scan_encoding + scan_domain_neutrality. ASCII PURO en Area_comun (em-dash
  ->'--', n->n). Commit pathspec EXPLICITO. Trailers en parrafo FINAL sin blank line: Task-Id + (si none)
  Ops-Reason<=120 + Co-Authored-By. `*_ARCHIVE.json` en TODO commit post-poda. HOOK_FULL=1 puede expirar el
  commit a 2min (el commit SI aterriza local; solo falto el push -> pushear). Para commits solo-mailbox usa
  hook default (mas rapido).
- **Fix-loop tope 2 iters; 2do NO-GO ESCALA AL OPERADOR** (esta sesion: B2 escalo, el Operador autorizo iter2).
- **Poda** (released_ratio>=90 DUE) en ventana claims=0: `prune_state.py --apply --actor-id Arquitecto
  --timestamp <ts> --commit <HEAD>` (via submit_intent). **Higiene mailbox** (lotes de ~5, `mailbox_archive`
  con author/relayed_by por MSG, claim task_id OPS-MAILBOX-HYGIENE-<fecha>).

## LECCIONES CLAVE (nuevas de esta sesion)
- **El ciclo de 2 capas es la joya, demostrado 2x:** la Analista cazo B1 (quoting corrompe argv ante ruta con
  `\` final) y B2 (el TrimEnd del fix colapsa la raiz de volumen `D:/`->`D:` = ruta relativa a la unidad ->
  tarea instalada ciega, exit 0 silencioso) -- dos bugs de Windows que mi recomputo de fixtures NO vio. Yo
  los reproduje independientemente antes de rutear. Un checker honesto retira su propia sugerencia si
  introduce un defecto (el TrimEnd fue idea de la Analista en iter0, lo retiro en iter1).
- **Recomputo por el ENTRYPOINT REAL, no por fixtures comodos:** B2 solo aparecio al probar `-ScanRoot 'D:/'`
  (raiz de volumen), no `D:\vol\` (subdir). Prueba el caso que el contrato persigue de verdad.
- **Harness del checker colgado en bucle de residuo:** bajo re-exec-en-residuo (agravado si YO commiteo algo
  que cambia el arbol bajo su exec), el checker deja el veredicto SIN COMMITEAR (err.log 0-byte >13min = fallo
  proveedor). Destrabe: commitea TU su veredicto completo con ATRIBUCION (anomalia DECISION-0018); a menudo
  su re-exec eventualmente commitea solo (verifica HEAD antes). taskkill del exec colgado con autorizacion del
  Operador; el barrido de "HUNG?" por FILE err.log-0-byte-viejo es FALSO POSITIVO (execs completados dejan
  err.log vacio; chequea el PROCESO, no el archivo).
- **Watchdog SEEN-BURN = falso positivo cuando la tarea AVANZO** por el ciclo (los MSGs se consumieron bien).
- **HUMAN_GUIDE.md:** el generador valida contra 21 secciones FIJAS (compartidas con el template); NO anadir
  seccion nueva -> incrustar como subseccion `### N.x` (contenido instancia-especifico no va al template neutral).
- **Notion:** `**\`code\` (\`code\`)**` (bold envolviendo code+parentesis) se mangle; usa `**\`code\`** (\`code\`)`.

## CANAL + PENDIENTES
- Ordenes por MAILBOX firmado o interactivo. Al arrancar: pedir autorizacion per-sesion para crons + taskkill.
- **PENDIENTE UNICO: TASK-0178 (Aegis Front) -- arrancar DESARROLLO en Zeus-protocol** cuando el Operador de
  el "goal". El primer entregable recibe revision adversarial. Diseno completo en DESIGN-0178.

## SIGUIENTE ACCION
Esperar el "goal" del Operador para arrancar el desarrollo del Aegis Front. Al llegar: promover TASK-0178
proposed->ready (o registrar unidades hijas), y construir el **MVP L1 (operabilidad/observacion) + medicion
modo-dueno** en `Zeus-protocol` (NO el hub), gobernado desde aqui, con el primer entregable a revision
adversarial. Lee DESIGN-0178-aegis-front.md (seccion 0 MANDA sobre el resto).
