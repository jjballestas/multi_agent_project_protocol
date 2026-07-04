# ESTADO del Asesor - fuente de verdad canonica (leer al arrancar)

> Reemplaza al snapshot compartido de .claude (memory/project-state-snapshot.md), DEPRECADO para
> el Asesor. El Asesor mantiene SU estado aqui. Historial completo en git.
> Ultima actualizacion: 2026-07-04 (sesion de arranque de build; DIRECTIVA de arranque de GOAL-P1 RUTEADA
> al Arquitecto -commit d55cfc9-; DECISION-0088 ya REGISTRADA por el Arquitecto -512e35c- formaliza el asiento
> escalonado hub/Aegis. Base previa: NOVA-DEV gate-atestado e2e, DD baseline OK, piloto de medicion validado
> -smoke-, DECISION-0087 nombres Aegis, estimates Q4 resueltos). AHORA: reactivo, esperando confirmacion del
> Arquitecto (repo Nova-Budget + Codex activo + tarea baseline -> NOVA-GOAL-001) y el build real para cosechar medicion.

## Identidad y reglas de operacion (no negociable)
- Soy el ASESOR del Operador (John Ballestas), NO el Arquitecto (otra sesion, ejecuta el ledger).
  Participante NO-FIRMANTE (alta REGISTRADA: DECISION-0086, commit 26ac919; id `asesor`, cero
  capabilities de ledger, canal=mailbox firmado Operador, area personal/asesor/, agent_registry NO tocado).
- CANAL: ordenes/respuestas al Arquitecto SOLO por MAILBOX (MSG-YYYYMMDD-Operador-to-Arquitecto-*)
  firmado como Operador, commit con pathspec explicito + push. NUNCA submit_intent, NUNCA paste-ready.
- CARRIL: NO actuar como Arquitecto. Tablero, crons y procesos son suyos -> los SENALO/RUTEO por
  mailbox, no los edito/opero (excepcion: la PRESENTACION del pipeline -acordeon- la edite bajo orden
  directa del operador; su DATA jamas). Stall = diagnostico LIGERO + nudge, sin operar crons ni process trees.
- GATE ASCII PRE-COMMIT BLOQUEANTE: escaneo bytes>127 y ABORTO el commit si hay (patron
  `python -c '...sys.exit(1 if bad)' || { echo ABORTA; exit 1; }`). Acentos/em-dash son mi vicio; el gate
  bloqueante YA me salvo 2 veces esta sesion (cazo "genere"/"especifico" con acento, aborto). Uso siempre.
- TRAILERS opcion A (COMMIT_TRAILERS.json, operator_advisor_rule): Task-Id: none + Ops-Reason:
  coordinacion-asesor-mailbox + Co-Authored-By, parrafo final sin lineas en blanco. Mi self-filter del monitor caza el Ops-Reason.
- CORTAFUEGOS: ordenes [DIRECTIVA]/[RECOMENDACION]; PRE-DECISION jamas se referencia; DECISIONes =
  requisitos no verbatim; snapshot compartido = solo hechos.
- PROACTIVIDAD SIN PREGUNTAR: preparo el siguiente entregable de cada gate; solo orden contraria frena.
- LECCION CLAVE (validada esta sesion): mis revisiones son DESIGN + STUDY-INTEGRITY, NO sustituyen la
  VERIFICACION EMPIRICA contra la BD desplegada (no tengo readonly aqui; el Analista si). El gate formal
  cazo 2 bugs de falsabilidad que mi revision informal dejo pasar -> es la TESIS DEL ESTUDIO en vivo
  (checker formal > informal) y ademas el ALCANCE del gate importa (un gate estrecho tiene punto ciego).
- LECCION watchdog (falso-jam): NO llamar jam por DURACION en tareas pesadas conocidas (e2e/harness 35+
  min legitimo). Solo jam con firma real: err.log de hang, lease vencida, sin heartbeat.
- MINIMIZAR CHURN: no commitear ESTADO por cada micro-evento del monitor; capturar el estado RESUELTO de
  cada hilo. Mailbox: no re-enviar directivas ya en open/ (el peer las consume).
- ANTI-COLISION EN ARBOL COMPARTIDO (leccion 2026-07-04): comparto working tree con el Arquitecto; su
  submit_intent en curso (enforce+authoritative ON, materialize) materializa state en el arbol comun ANTES
  del commit atomico -> aparece como ` M CLAIMS.json` sin commitear. ANTES de commitear: `git status --short
  Area_comun/state/` -> si hay half-written peer state, ESPERAR a que aterrice (DECISION-0020). Yo staging-
  explicito (solo mis rutas) me protege de clobber, pero igual reviso. NO es anomalia: es su op en vuelo.

## Deberes al arrancar
1. AUTO-POLL: git fetch/pull, git log -8, ls Area_comun/mailbox/open/, pendientes TASK_INDEX.
2. Arma MONITOR persistente sobre origin/main con SELF-FILTER por trailer (salta "Ops-Reason:
   coordinacion-asesor"): commits de peers (PIPELINE + *-to-Operador-*) + stall 30min.
3. Auto-poll de cada turno = red primaria; monitor = respaldo.

## Estado del proyecto (2026-07-03 noche)
- **F1 (nucleo doctrinal) CERRADO 7/7** (v1.18.0, gate de trailers activo, epoch 1.14.0 PINEADO).
- **F2 (instancia distribuida) COMPLETA 4/4** (instancia Aegis en D:/Agentes/Zeus/NOVA/Aegis, harness, e2e,
  runbook). DECISION-0085: NOVA/ paraguas + Aegis instancia-metodologia NEUTRAL + NOVA/Nova-X productos LAZY.
- **NOVA-DEV (TASK-0246) = TANDA ACTUAL COMPLETA Y GATEADA DE PUNTA A PUNTA.** 9 SPECs gobernadas (informe
  adversarial + familia P3 P3-001..005 + pool Q4 P4-004/P2-004/P2-003/P6-003), formato unificado NOVA-SPEC-T-001
  + intake-v2/DoR, aislamiento intra-par declarado y verificado. Gate Analista OK/CERRABLE en core (F-0246-01
  q4_membership + F-0246-02 THROW) + db_verified_at (audit de THROW cerrado, 070b533). Sigue in_progress por
  directiva del operador. FALTA solo: **miembros GOBERNADOS de pares** (bloqueados por diseno hasta 17-jul;
  heredan el patron congelado de P4.1 cuando arranque el miembro baseline).
- **4a ACTION HECHA:** el Arquitecto EMPLAZO mis scripts-medicion al hub
  (personal/Arquitecto/TFM-medicion/corpus/medicion/) -- version correcta verificada (52 cols, 5 peones, motor
  identico). Listos para congelar a v1.0 en el sello.
- **Pendientes backlog VN (no urgentes):** TASK-0231 (F6.1 peones) + TASK-0245 (watchdogs->skills), proposed.

## Trabajo en vuelo (con dueno)
- **2 DIRECTIVAs previas CERRADAS Y VERIFICADAS por el Asesor:** (1) DD-01/02/03 horneadas en las SPECs
  (01f05db; verificado: DD-01 confirmado, DD-02 objeto min 20 chars con 400 si <20, DD-03 SECOP='N/A');
  (2) pipeline al dia (2320acd; F4.0 NOVA-DEV + F3.0 GOAL-P1 anadidos, F3.3/F3.4 refrescados con evidencia =
  panel de control completo). SEGUIMIENTO suelto: DD-02 toca criterio falsable -> debe viajar en un gate del lote.
- **Arquitecto (ventana muerta, su carril):** REDACTAR la DECISION formal de nombres Aegis -- RUTEADA por el
  Asesor (MSG DIRECTIVA-redacta-decision-nombres-aegis, 8eb966d). Solo fija direccion; ejecucion = Carril B post-sello.
- **Operador (EL RELOJ REAL, no eclipsar):** estimates Q4 RESUELTOS (6 M + 4 S, ESTIMATES-Q4-para-sorteo.md).
  GOAL-P1: **maquinaria de medicion VALIDADA (smoke, 2026-07-04)** -- el Operador corrio abrir/actualizar/cerrar/
  verificar con el helper medir-goalp1.ps1 (verificar OK, 3 eventos); PERO la fila es SMOKE con valores de
  ejemplo (tokens=12000, fecha_fin=08-jul futuro), NO el build real. FALTA: correr el BUILD real de GOAL-P1
  (3-8 jul, tarea de dev) y re-medir con numeros reales -> ESE journal se congela. Heads-up al Arquitecto
  ruteado (dbd9ab4: atesta el sha256 REAL, no el smoke). Yo coordino la recaptura. GRANT EXECUTE (<=14-jul).
- **Yo (reactivo):** cosechar la medicion de GOAL-P1 al sello cuando corra; vigilar que el sello (08-jul) no
  se quede sin inputs del operador.

## >> HILOS DE LA SESION 2026-07-04 (todos RUTEADOS; esperando respuestas del Arquitecto)
1. **ARRANQUE BUILD GOAL-P1** (d55cfc9, req_resp): ACTIVA Codex + repo NOVA/Nova-Budget + apunta a NOVA-GOAL-001
   (fundacion tecnica, brazo baseline). Asiento = HUB (DECISION-0088, 512e35c). REMOTO CONFIRMADO por el operador:
   https://github.com/jjballestas/Nova-Budget.git (existe, VACIO; ruteado FYI 19cd60a). Espero: ruta repo + Codex
   activo + id tarea baseline. Luego operador mide con medir-goalp1.ps1 (BUILD REAL, no smoke) -> journal al sello.
2. **SEMANTICA CHECKER GOAL-P1 = OPCION B** (fe83c84, resuelto): el Arquitecto cazo conflicto real (schema sellado
   baseline=>checker_formal=0 vs mi fraseo Analista-checker). Ruling: B (baseline fiel, checker vivo = adversarial
   informal, checker_formal=0). El valor de A ya esta sellado: frontera P1 read-only 26-29 jul -> FRONTERA-FIX +
   ensayo de maquinaria gobernada en categoria propia fuera de Q1. Corregi mi DIRECTIVA (Analista-checker-FORMAL =
   solo tareas gobernadas post-30-jul). Operador clico B en el panel del Arquitecto.
3. **DOMINIO NOVA-BUDGET ABSORBIDO** (brief durable 042eb72, personal/asesor/NOVA-BUDGET-brief-dominio.md):
   cadena de gasto (Aprop->CDP->RP->OBL->Pago, 4 reglas de oro en procs SQL), Clean Arch .NET 10, NO green-field
   (BD endurecida + reconciliada al centavo; hibrido 2024-26 fiel / 2027 limpio), ~45-55% del build = superficies
   sobre procs existentes, brechas de verdad -> nova-hardening (regla 8).
4. **VEREDICTO ULTRACODE** (panel adversarial 8 agentes, en transcript): NO en bloque; depende de 2 REGIMENES.
   Ventana MEDIDA (3-30 jul, baseline+Q4) = mono-orquestador, ultracode PROHIBIDO (rompe Q1/Q4, irreversible).
   POST-medicion (90%+ de Nova) = ultracode SELECTIVO-AMPLIO gatillado por dominio (compone >1 mutacion / cruza
   modulo / toca SESSION_CONTEXT-saldos / alimenta regulatorio). Magnitud = ANCHO -> pipeline barato, no esfuerzo
   por-tarea. "Superficie mecanica" solo si 1-proc/1-vista sin composicion. nova-hardening = ultracode paga pleno.
5. **CODEGEN (aprobado por operador) + SKILL codegen-triage RUTEADA** (draft fd8b2ad, DIRECTIVA 9256bb7, req_resp):
   codegen != peon -> LEGITIMO en ambos brazos incl GOAL-P1 (determinista, cero-tokens, un dev, NO tratamiento),
   simetrico por par. Cero peones en brazos medidos SE MANTIENE. Skill en 2 capas (neutral + recetas instancia Nova),
   owner Codex-maker/Analista-checker, gobierna Arquitecto. ACCION 2 pedida: SELLAR codegen!=peon en def del brazo
   baseline antes del 08-jul. Espero: id tarea skill + confirmacion clarificacion sellada.
6. **PEONES (aclarado, POST-SELLO):** NO se dan de alta (no participante, no area personal, no agent_registry); son
   herramienta no-firmante que Codex opera bajo contrato de asignacion (DECISION-0078 PROPOSED, a ajustar+aprobar +
   TASK-0231 F6, sandbox piloto-peones). Runbook = TEMP_Guia_Modelos_Peones (personal/ungobernado). NO ahora (reloj=sello).

## SIGUIENTE (hitos)
1. **SELLO ETAPA 1 (<=08-jul) = reloj duro.** Draft listo (SELLO-ETAPA-1-nova-budget-DRAFT.md). Congela
   schema/scripts/corpus/enumeracion Q4/sorteo. Inputs que faltan: GOAL-P1 corrido + estimates S/M/L (operador),
   scripts ya emplazados (hecho), sorteo NIST + T + sha256 (dia del sello). GRANT EXECUTE para paridad (<=14-jul).
2. **17-jul:** miembros gobernados de pares (desbloqueo por congelamiento baseline).
3. **30-jul:** gate duro Sprint 1.
4. **Carril B (post-sello, gateado):** ejecucion de la marca Aegis en la superficie publicada + i18n del
   core/templates/spec. LA MEDICION NO HA ARRANCADO (F1/F2/NOVA-DEV = infraestructura, no desarrollo medido).

## Decisiones durables de esta sesion (2026-07-03)
- **DECISIONES DE DOMINIO resueltas por el operador + RUTEADAS (MSG DIRECTIVA-decisiones-dominio-nova),
  a hornear en las SPECs por el Arquitecto:**
  - DD-01 (autorizacion, las 5 SPECs P3-001..005): (a) ACEPTADO el supuesto temporal (usuario autenticado con
    rol presupuesto captura/aprueba/emite) para Sprint 1; BR-C4 (policy por operacion) CONFIRMADA post-Sprint-1.
  - DD-02 (P3-003, objeto del RP): NORMADO a min. 20 caracteres (cambia el legacy de 15). Toca criterio falsable.
  - DD-03 (P3-003, referencia SECOP vacia): default = marca 'N/A' declarada; jamas el centinela '0' legacy.
  - Tracker: personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md (todas RESUELTA/ruteada).
- **DECISION DE NOMBRES AEGIS (debatida y CONVERGIDA con el operador; opcion (i) MARCA-SOLO confirmada):**
  - **Aegis** = MARCA de la METODOLOGIA (palabra neutra, NO rompe neutralidad de dominio, citable p/ publicar).
  - Instancia por proyecto = carpeta/repo **`aegis/`** (convencion tipo `.git`, sin ambiguedad; ya existe NOVA/Aegis).
  - Producto/front = **Zeus-Aegis**; productos de dominio = **Nova-X** (Nova-Budget/Treasury/...).
  - Namespace de skills en el CLI = **`aegis:`** (como `anthropic-skills:`), VIA LOADER (DECISION-0061),
    NO renombrar archivo por archivo. **Scripts SIN tocar** (no se ven como skills; costo/riesgo alto por CI/crons/#4).
  - Hub = **"Aegis-core"**. Convencion de habla: "Aegis-core/hub" = fuente canonica vs "la instancia aegis de <proyecto>".
  - **OPCION (i) MARCA-SOLO:** NO se toca `project_name` en protocol.config.json (genesis-bound, linea 5) ->
    CERO re-genesis, CERO riesgo sobre N=500/cadena #4 (dataset sellado inmutable; el rename es ORTOGONAL a lo
    medido, solo se anota procedencia). H1-H3 no se tocan.
  - **i18n del core/templates/spec para publicar = Carril B** (post-sello, acotado a la superficie publicada,
    NO todo el repo; el dogfooding en espanol no se publica). NO es cosmetico -> es un programa Carril B.
  - HECHO: DECISION-0087 registrada (bc95ad3 + forma 18499e4: instancia = `Aegis/` capitalizada). Fija la
    DIRECCION. La EJECUCION (adoptar la marca + namespacing `aegis:` en el loader + i18n) es Carril B POST-SELLO.
  - PREFIJO `aegis:` EN EL CLI: NO visible aun (decidido, no ejecutado). Hoy las skills muestran nombres planos;
    el prefijo aparece cuando se implemente el namespacing via loader (Carril B). Scripts sin tocar.

## Mis entregables (todos versionados)
- scripts-medicion/ (medicion_ledger.py + schema_medicion.json [52 cols, 5 campos peones + par_id na_ok] +
  schema_defectos.json + README): commiteados (11fddf4), smoke verde ciclo completo, EMPLAZADOS al hub por el
  Arquitecto (personal/Arquitecto/TFM-medicion/corpus/medicion/). Listos para congelar a v1.0 en el sello.
- SELLO-ETAPA-1-nova-budget-DRAFT.md (pre-registro; placeholders [LLENAR-AL-SELLAR]). COSECHAS aplicadas:
  s.5 = verificacion de EXISTENCIA readonly es posible ya (F-NOVA-01; paridad requiere GRANT EXECUTE);
  NOTA DE INDEPENDENCIA = los ~4 Get_*_List son CLUSTER casi isomorfo load-bearing para n>=10 -> Q4 declara
  n EFECTIVO reducido; doble rol PAR-D/Q4 NO es confound (contrastes pre-registrados distintos).
- Tracker de decisiones de dominio + separacion de memoria (esta area) + alta ruteada.

## Asiento de coordinacion del build de Nova (DECISION-0088, 512e35c; enmienda a 0050 #5)
- **AHORA (ventana del estudio, hasta sello/30-jul): asiento = HUB.** El brazo gobernado es el TRATAMIENTO
  medido -> su atestacion debe estar en el MISMO #4 que la medicion + sello, en un solo asiento. Meter
  NOVA/Aegis a mitad del estudio = costura de cross-atestacion antes del sello (viola regla de oro del sello).
- **Codigo siempre = NOVA/Nova-Budget; estudio/medicion/sello/#4 siempre = HUB.** Workflow VS Code del
  Operador: abre Nova-Budget para codigo + coordina desde el hub (sin multi-root).
- **POST-sello: migra a NOVA/Aegis** (instancia operativa del equipo). Regla dual cross-atestacion: hub =
  #4 del estudio/meta + sello; NOVA/Aegis = #4 operativo del build; el journal del hub registra el sha256
  de la atestacion de Aegis por gate. ELEGANTE (study-relevant): esa migracion ES la evidencia de
  transferibilidad (la replica employee-run pre-registrada) -> arquitectura y estudio se alinean.
  FORMALIZADO en DECISION-0088 (512e35c): meta/estudio/metodologia canonica = hub SIEMPRE (nunca migra);
  governance operativa del producto = su instancia Aegis/ tras adoptar; migracion post-sello, dual cross-atest.

## Contexto real del negocio (clave)
Objetivo real = Nova Budget/Accounting/Payroll/Treasury para la EMPRESA del operador, employee-ready.
Stack: Clean Architecture .NET 10 (Api/Application/Domain/Infrastructure/Mcp/Contracts) + React/TS/Vite
+ SQL Server 2025 + OpenTelemetry; anti-patrones prohibidos (WebForms, DataTable entre capas, DLLs
manuales, secretos en .config, centinelas -99). Requisitos = RES-000..012 (brechas s.08 de NOVA-PRES-000);
SPECs desde NOVA-SPEC-T-001 v1.1. FUENTE DE VERDAD del diseno = D:/Agentes/Ingenas/Budget/ (paquete del
operador, FUERA del hub): NOVA_GOAL, NOVA_Arquitectura, NOVA_PRES_00..12, NOVA_SPEC_Plantilla, NOVA_ESTUDIO_*;
BD/legacy en 01_Sources. El hub Area_comun/specs/nova/ guarda la DERIVACION gobernada (SPECs), no el diseno-fuente.
Composicion del equipo: 12 roles -> 4 firmantes (Operador=dominio, Arquitecto=arquitectura+docs, Codex=maker,
Analista=security+QA checker); Legacy Analyst sin firmante = eslabon debil de atestacion.

## Que afirma / NO afirma el estudio (delimitacion sellada)
Da: instrumentacion + Q4 causal (ligero-vs-completo) + serie honesta de calidad (checker formal atrapa
lo que el informal dejo pasar) + transferibilidad (2a instancia dominio real vs N=500 auto-dogfood). NO
da: "el gobierno mejora la calidad" causal (maker!=checker YA existe en ambos brazos; el tratamiento es
el checker FORMAL atestado). Veredicto de compra se difiere a replica employee-run pre-registrada.
Peones: se mide el USO (5 campos), su EFECTO solo en F6 aislado (no confundir el contraste central).

## Pendientes del operador (recordar con tacto)
Abrir GOAL-P1 (piloto, 3-8 jul, EL RELOJ); estimates S/M/L (<=08-jul); GRANT EXECUTE + sandbox mutadores
(<=14-jul); revision legal del consentimiento. F1.6 (aprendizajes-externos, extraccion de reglas) pendiente,
paralelo, NO es entregable del Asesor.
