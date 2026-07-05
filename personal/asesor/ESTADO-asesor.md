# ESTADO del Asesor - fuente de verdad canonica (leer al arrancar)

> Reemplaza al snapshot compartido de .claude (memory/project-state-snapshot.md), DEPRECADO para
> el Asesor. El Asesor mantiene SU estado aqui. Historial completo en git.
> Ultima actualizacion: 2026-07-04 ~14:00Z (CIERRE DE SESION). **SELLO ETAPA 1 EJECUTADO Y ATESTADO**
> (DECISION-0091, #4 seq 3831; corpus congelado + schema v1.0 + sorteo pre-registrado corrido con semilla NIST
> pulso 1844242 -- VERIFICADO independiente por el Asesor byte a byte: 2 completo / 8 ligero). Se construyo
> Nova-Budget de cero: GOAL-P1 (done+medido+atestado sha256 d2a13216) + skill codegen-triage (viva) + 14 SPECs
> baseline atestado + sandbox mutadores sellado (P4.x READY) + estimates Q4 locked + TASK-0245 aprobada.
> HALLAZGO CLAVE: el sorteo 8/2 hace Q4 SUBPOTENCIADO (se declara poder efectivo, no se fuerza). CAMINO OPTIMO
> routado (NO stand-down): F3.3 instrumentacion (Codex) + F3.2 diseno (yo) + dev medido P2.1/P2.2 (3-25 jul) +
> PAR-2 condicional. >> BLOQUE DE TRABAJO DE LA PROXIMA SESION: ver seccion ">> PROXIMA SESION - BLOQUE DE TRABAJO".

## >> REACTIVACION 2026-07-04 (tarde) -- entregables shipped, en vuelo
Operador reactivo + directiva "no dejes al Arquitecto sin trabajo, trabaja rapido". Estado al reactivar:
HEAD==origin limpio, mailbox/open vacio, sin drift. Hecho esta reactivacion:
- **SPEC de diseno F3.3 ENTREGADA** (personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md): 3 eventos
  (cost.attributed auto reusa SPEC-0079/DECISION-0033 + defect.reported vs schema_defectos + manual.intervention)
  + study_metrics.py determinista Q1-Q5. Commit ffad74e.
- **COLA PRIORIZADA SIN-IDLE ruteada** al Arquitecto (MSG-...-DIRECTIVA-cola-F3.3-lista-no-idle, ffad74e):
  Q1 F3.3 a Codex (critical-path, spec lista) | Q2 dev medido P2.1/P2.2 en paralelo | Q3 monitor PAR-2 condicional
  (<=15-jul) | Q4 backlog miembros gobernados (17-jul). Trabajar en paralelo, re-llenar al drenar.
- **DRAFT F3.2 ENTREGADO** (personal/asesor/DRAFT-F3.2-sello-etapa2-backlog-Q4-adopcion.md, a913cc4): aritmetica
  backlog reconciliado + condicionalidad Q4 (subpotenciado 2/8 con n efectivo<10 por cluster BR-C3) + regla de
  adopcion/transferibilidad Aegis. NO ruteado aun (para Etapa 2 <=29-jul; el MSG ya aviso que llega; evito churn).
- MONITOR armado sobre origin/main con self-filter (salta mi Ops-Reason).
**RESUELTO (esta reactivacion):** el Arquitecto respondio (a) F3.3 = TASK-0249 GO-eada a Codex (critical-path);
(b) P2.1/P2.2 = TASK-0250/0251 proposed en cola detras de F3.3; (c) PAR-2 deadline trackeado (no verifico en
vivo: guard de seguridad bloqueo lectura de produccion sin autorizacion). Dejo 2 preguntas al operador ->
OPERADOR DECIDIO: (b) ESPERAR a F3.3 (P2 abre auto-instrumentado; proposed en cola, NO manual); (c) DIFERIR la
verificacion PAR-2 a 15-jul (procs Annul_* son brechas B-04 conocidas, hoy ausentes; no autoriza readonly ahora).
Rutee la respuesta (a5323ba).
**GRANT EXECUTE del estudio (item #2 operador) EJECUTADO Y VALIDADO (df34ec3) -- CERRADO por adelantado
(<=14-jul):** el operador corrio el GRANT en DbsFinanciero_SANDBOX: 105 permisos en el rol
budget_sandbox_verifier (15 EXECUTE procs Budget.* + 90 SELECT = 89 vistas + Security.Permission); guard
DB_NAME() NOT LIKE '%SANDBOX%' anadido y PROBADO (aborto 51011 contra prod antes de otorgar); smoke OK;
script sin secretos. CORRECCION de login: el harness usa nova_budget_verifier (NO nova_sandbox_verifier que
sugeri; ya estaba en .env sellado) -> rutee la correccion a Codex (supersede el FYI previo). Historico:
**GRANT EXECUTE del estudio DEFINIDO y RUTEADO (7bd3ea4):** el operador creo el script
sandbox-grant-execute.sql (paquete fuente FUERA del hub, D:/Agentes/Ingenas/Budget/.../DATA/): rol
budget_sandbox_verifier sobre DbsFinanciero_SANDBOX, superficie IDENTICA baseline/gobernado (15 EXEC procs +
89 SELECT vistas + 1 dep Security.Permission) = no confound. Revision adversarial mia: diseno correcto
(sandbox no prod, simetrico, fail-closed rol). Rutee a Codex (via Arquitecto) cablear el harness de paridad
exec-vs-endpoint al sandbox con ese rol (reemplaza readonly_s9) + hardening guard DB_NAME() recomendado +
notas: Annul_* por enmienda fechada cuando existan (PAR-2 difiere), reset sandbox entre corridas. El operador
ejecuta el GRANT de su parte.
**CONSENTIMIENTO EMPLEADOS (item #1 operador):** revision adversarial hecha (personal/operador/legal/
CONSENTIMIENTO-EMPLEADOS-NOVA.docx). 3 CRITICOS (C1 Responsable sin identificar; C2 contradiccion
retencion-vs-publicacion; C3 sobredeclara anonimato vs seudonimo re-identificable SPEC-0079 C3) + 3 ALTOS
(A1 falta clausula no-evaluacion-desempeno = sesgo observador; A2 base legal RGPD empleado presumido no-libre;
A3 sin procesadores/transferencia internacional) + medios/bajos. NO edite el docx (operador revisa primero).
Brief legal mio en personal/asesor/BRIEF-revision-legal-consentimiento.md (d6b50c8).
**>> PENDIENTE-TRIGGER (orden operador 2026-07-05):** AL CERRAR P4.1 (monitor detecta TASK-0253 -> done o
fila CLOSE J9 en el journal) -> preguntar al Arquitecto por mailbox la CADENCIA DE ATESTACION del journal de
medicion (por-unidad como GOAL-P1 sha256 d2a13216, vs por-checkpoint sello/reconciliacion). Contexto: el corpus
esta gitignored a proposito (.gitignore:37, atestado por manifiesto), pero las filas P2.1/P2.2/P4.1 no se ven
atestadas por sha256 en el #4 aun -> confirmar si es diseno (checkpoint) o hueco (data local sin sellar). NO
rutear antes del cierre de P4.1. Monitor activo: b0ui9enn0 (dev-hitos).

**>> 2026-07-05 TURNO DE NOCHE del Arquitecto QUEUED (~6h, operador durmiendo):** rutee
MSG-...-DIRECTIVA-turno-noche-cola-6h (4787c5b) -- cola ordenada+PRE-DECIDIDA para sesion fresca autonoma:
(0) cutover+higiene+responde directivas; (1) cierra TASK-0252; (2) gobierno (PAR-2 flip+enmienda, filas P2);
(3) CICLO COMPLETO P4.1 ruta critica+captura OPEN/CLOSE; (4) miembro baseline PAR-1; (5) extra si sobra
(superficie PAR-2 detras de P4.1, o TASK-0246). Pre-resueltas: P3.1=diferir, linea roja Q4, blocked-con-pregunta
sin parar el turno, no inventar trabajo que rompa el sello. CHECK para el operador en personal/asesor/
CHECK-turno-noche-20260705.md. AL RETOMAR: revisar el resumen *-to-Operador-* del Arquitecto + el CHECK.

**>> 2026-07-05 PAR-2 ASEGURADO (adelantado ~10 dias del 15-jul):** el DBA del Operador cerro la brecha
B-04/RN-08 en sandbox -- Annul_Availability_Certificate + Annul_Commitment, 10/10 pruebas (guardas THROW
50293 CDP / 50283 RP, cuadre, idempotencia, rollback, tenant), grant surface 107 (17 EXEC + 90 SELECT). Yo
redacte la DRAFT-SPEC de hardening (1f666be) + el encargo detallado al DBA. Rutee (eaa4704) el flip PAR-2
CONDICIONAL->CONFIRMADO + enmienda fechada del grant + nota contable-no-op (correcto: CDP/RP = reserva, no
movimiento contable) + superficie C# de PAR-2 EN COLA detras de P4.1/PAR-1 (no salta ruta critica). PENDIENTE
Arquitecto: registrar flip + enmienda + (opcional) confirmacion read-only Analista.
**PIPELINE (2026-07-05):** Codex reactivado, en fix-loop de TASK-0252 (harness paridad; Analista NOGO: guard BD
bypasseable + rol no verificado). Mi DIRECTIVA P4.1 (ruta critica, 862fa7f) ruteada, en open/ -- el Arquitecto
probablemente cierra 0252 antes de GO-ear P4.1. WATCH: que P4.1 se GO-ee tras 0252 (piso minimo 30-jul).

**F3.3 CERRADO** (Analista OK re-gate 2; fix-loop cazo F-0249-01/02/03 = reproducibilidad clon limpio =
tesis del estudio en vivo). **P2.1 (TASK-0250) y P2.2 (TASK-0251) DONE** (primeras 2 unidades baseline; cada
una fix-loop 1/2 real). P2.1: baseline/par_id=NA/M/reworks=1. P2.2: baseline/PAR-D anclado/spec_prepagado=true/
M/reworks=1.

**>> PAUSA 2026-07-04 (tarde) -- monitor DETENIDO por el operador ("continuamos luego"). AL RETOMAR: re-armar
monitor + auto-poll. 3 HILOS EN VUELO esperando al Arquitecto:**
1. **INTEGRIDAD (urgente, b8cb6b7):** P2.1/P2.2 DONE pero SIN fila de medicion (journal solo tiene GOAL-P1);
   F3.3 se construyo y NO se corrio sobre ellas. Rutee cosecha urgente (err.log VOLATIL -> tokens baseline Q1
   se pierden si se rota). Le pase los campos no-token reconstruidos de git. PENDIENTE su respuesta: existen los
   err.log de P2.1/P2.2 o degradan a tokens=NA?
2. **SECUENCIA (fb78b82):** pregunte si P3.1 (SPEC-NOVA-P3-001, pattern-setter EXCLUIDA del pool Q4) es
   construible YA como unidad no-contraste, o ancla Sprint 1 (su decision de estudio) + confirma drenar TASK-0252
   (harness paridad, baja) a Codex. PENDIENTE su veredicto.
3. **LINEA ROJA reafirmada:** NO construir unidades del pool Q4 (P2.3, P2-004, P3.2/3.3/3.4, P4.1-4.4, P6.3)
   pre-30-jul (rompe contraste irreversible). Codex idle tras 0252/P3.1 = estado CORRECTO por diseno.

**CONSENTIMIENTO EMPLEADOS: ENVIADO A LEGAL (2026-07-04) -- hilo cerrado de mi lado; espera turnaround de legal.**
P3.1: el Arquitecto CORRIGIO mi lectura -- P3.1 NO es baseline; el sello (DECISION-0091 s.3.3) la clasifica
GOBERNADO/Sprint-1 (excluida de Q4 != baseline; fue error mio de framing). Recomende OPCION 3 (esperar Sprint 1,
NO construir): no desviar el sello por evitar idle; sin necesidad real; Codex idle tras 0252 = correcto por
diseno. Warn contra Opcion 2 (reclasificar = alteracion post-hoc del pre-registro). PENDIENTE decision operador.
**CONSENTIMIENTO EMPLEADOS: CONVERGIO (v5.0) -- LISTO PARA LEGAL (historico).** Revisiones adversariales v1->v5: de 3
criticos + varios altos a CERO hallazgos. v5 cerro los 2 flujos de procesadores (A metricas Microsoft/AWS / B
contenido-codigo-prompts Anthropic) + re-confirmacion en 2 pasos + Considerando 33. Cerre mi pasada adversarial.
Quedan 2 NOTAS DE CONCIENCIA (no defectos del form, gobernanza INGENAS): codigo como IP/confidencialidad a
Anthropic (Foco B del brief); supervision etica para apoyar Cons.33. NO edite el docx (operador revisa).

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
- ANTI-COLISION EN ARBOL COMPARTIDO (leccion 2026-07-04, REFORZADA): comparto working tree + INDICE GIT con el
  Arquitecto; su submit_intent en curso stagea archivos (decisions/, state/) en el INDICE COMPARTIDO antes de su
  commit atomico. **ERROR QUE COMETI (568b8d4):** `git add <mifile>` + `git commit` SIN pathspec commitea el
  INDICE COMPLETO -> arrastre su DECISION-0091 (sello) staged, quedo commiteada sin atestar en #4 = DRIFT (dato
  intacto, recuperable via regenesis+submit_intent, pero ruido en su transaccion). **REGLA DURA:** SIEMPRE
  `git commit -m "..." -- <pathspec>` (pathspec-limitado; commitea SOLO mi ruta, ignora lo staged por el peer).
  NUNCA `git add`+`git commit` pelado en arbol compartido. Ademas ANTES: `git status --short` -> si hay archivos
  con `^[AMD]` (staged) que NO son mios, o half-written peer state en Area_comun/state|decisions/, ESPERAR
  (DECISION-0020). El staging-explicito NO basta; el pathspec en el COMMIT es lo que protege.

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

## >> PROXIMA SESION - BLOQUE DE TRABAJO (indicarselo al operador al arrancar)
**EL SELLO ETAPA 1 YA ESTA HECHO Y ATESTADO** (DECISION-0091, #4 seq 3831; sorteo verificado). El pipeline esta en
el CAMINO OPTIMO (no stand-down, confirmado por el Arquitecto). **BLOQUE DE TRABAJO = arrancar la instrumentacion
y el dev medido post-sello.** Al arrancar, INDICALE AL OPERADOR este bloque, en orden:
1. **MIS DELIVERABLES (carril diseno Asesor) -- PREPARAR YA:**
   - **SPEC de F3.3** (instrumentacion): cost.attributed automatico por task_id (captura del total del stderr;
     por-cubeta solo via sesion-separada; degradacion a total sellada) + defect.reported (evento validado vs
     schema_defectos, con detector para la paridad) + manual.intervention + study_metrics.py (determinista con
     golden; Q1-Q5 del plan s.7 del SELLO). Prior art: DECISION-0033 + SPEC-0079 (cost-attribution-por-handoff,
     en .protocol-tmp/zc-proto/). -> Rutear al Arquitecto para que Codex la construya ANTES de que abra P2.
   - **DRAFT de F3.2** (aritmetica del backlog + condicionalidad Q4 consolidada + regla de adopcion) para el
     sello Etapa 2 (<=29-jul). RELEVANTE por el hallazgo: el sorteo 8/2 hace Q4 subpotenciado -> declarar poder efectivo.
2. **COORDINAR el camino optimo (mailbox + monitor):** F3.3 build (Codex via Arquitecto) -> dev medido P2.1/P2.2
   (ventana baseline 3-25 jul; Codex maker + adversarial SESION SEPARADA; abre con F3.3 listo o manual fallback) ->
   PAR-2 condicional (monitor checkpoint hardening <=15-jul; procs Annul_*; si no llegan, PAR-2 cae).
3. **COSECHAR la medicion** de cada unidad medida cuando corra; verificar integridad de estudio en cada gate.
PENDIENTES DEL OPERADOR: GRANT EXECUTE <=14-jul (paridad de mutadores); revision legal del consentimiento.
CALENDARIO: 14-jul GRANT EXECUTE + P4.1 | 15-jul checkpoint hardening (PAR-2) | 17-jul miembros gobernados de pares |
25-jul cierre duro ventana baseline | 29-jul sello Etapa 2 | 30-jul Sprint 1 gobernado (gate duro).

## >> CIERRE SESION 2026-07-04 - SELLO ETAPA 1 EJECUTADO Y ATESTADO (historico)
Ciclo de build cerrado de punta a punta: GOAL-P1 (construido+medido+atestado+ratificado, sha256 d2a13216) +
skill codegen-triage (viva, DECISION-0061, aun NO invocada como triage -- 1a ocasion = dev baseline P2.1/P2.2
post-sello; tooling Vite/dotnet-new SI se uso en scaffold) + 14 SPECs (P2/P3/P4/P6, baseline ATESTADO por
Analista rejuicio-2) + sandbox mutadores (construido por operador + sellado, RESET verificado, P4.x READY) +
estimates Q4 LOCKED (6M+4S). SELLO ETAPA 1 = 100% PRE-ARMADO: manifiesto+sha256, s.5 Q4 existencia, s.6.1
sorteo PRE-COMMIT (par_ids+estimates+algoritmo+T=commit cbc1ee2 2026-07-04T03:52:25Z), s.11.1 calendario;
FALTA SOLO la semilla NIST posterior a T + atestacion sha256 el 08-jul. TASK-0245 (watchdogs->skill neutral exportable) APROBADA por Analista (fix-loop 2 iters, sin escalar) -> deepened cola 100pct COMPLETA.
PENDIENTE OPERADOR: (a) ratificar el reporte humano (REPORT-20260704-...-ciclo.md; lo revise: EXACTO, con hora;
sugerencia menor opcional = anadir frase de delimitacion explicita 'infra+piloto, no resultados de estudio, GOAL-P1
excluido del contraste'); (b) P3(c) pre-diseno cross-atestacion+i18n = relleno, no bloquea. PROXIMO EVENTO REAL:
sello 08-jul (semilla-del-dia). Fondo intocable verificado (N=500, config 2e35f26e, epoch 1.14.0). Ver revision
cuidadosa del sorteo pre-commit -> hacerla el dia del sello.

## >> DEBATE CERRADO - BUILD REANUDADO 2026-07-04 (orden explicita del operador: "a trabajar el goal")
El operador cerro el debate y ORDENO: metodologia se mantiene + incluir la skill codegen + arrancar el goal hasta
terminar el desarrollo. Rutee DIRECTIVA consolidada 9e2f660 (supersede la pausa 39fd498). Estoy en modo COORDINAR
(monitor activo). Esperando respuesta del Arquitecto: ruta repo + Codex activo + id tarea baseline + id tarea skill + confirm checker B.
1. **METODOLOGIA AS-IS (decidido, sin cambio):** firmantes = Operador(dominio)/Arquitecto(arq+docs)/Codex(maker)/
   Analista(security+QA checker). NO se separan roles en mas firmantes: los ~10 roles del GOAL colapsan sobre los 4
   con ROL ACTIVO EXPLICITO por artefacto; maker!=checker DURO (Codex hace, Analista verifica; nunca auto-verificacion).
2. **GOAL-P1 ENTREGADO Y ATESTADO (TASK-0247 review_approved):** ciclo completo en una sesion. Codex construyo la
   fundacion (commit producto **02f5d5a** pusheado a Nova-Budget main): NOVA.sln 6 capas + nova-web + 3 test proj +
   5 architecture tests + health/OpenAPI/ProblemDetails/correlation-id(TASK-0247) + CI. GATE REAL: dotnet build PASS,
   dotnet test **9/9** verde, npm typecheck PASS, smoke runtime OK, adversarial informal APPROVED (docs/adversarial-goalp1.md).
   El Arquitecto VERIFICO INDEPENDIENTE (re-corrio dotnet test 9/9) + ratifico. Opcion B intacta (checker_formal=0).
   Verifique la evidencia: entrega REAL, sin drift. Riesgo menor NU1903 (NuGet audit OpenApi 2.3.0, no bloquea).
   **MEDICION RESUELTA (fa387a3):** el operador decidio -> Arquitecto CIERRA la fila real + atesta, operador RATIFICA;
   DEGRADACION ACEPTADA. Datos reales: build 0.20h, mono, sesiones=1, reworks=0, APROBADO, done, tokens_total=165844.
   **HALLAZGOS DEL PILOTO (para el freeze del schema v1.0):** (1) el runtime codex solo da UN cumulativo en STDERR
   (err.log, NO out.log); no separa cubetas -> degradacion sellada a tokens_total_atribuibles (per-cubeta=NA). Q4
   total-vs-total INTACTO; Q1 degrada a total-marginal. (2) el adversarial de GOAL-P1 corrio DENTRO de la sesion de
   Codex -> tokens_adversarial no separable (refuerza P2 = sesion separada). (3) FOLLOW-UP P2 (no bloquea GOAL-P1): el
   total incluye cache no aislable -> ambos brazos MISMO tipo de sesion o declarar cache-confound; captura lee stderr.
   **PILOTO CERRADO Y RATIFICADO (97fd09e):** fila real GOAL-P1 cerrada + atestada; sha256 journal =
   d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5 (anclado en #4 por el commit del Arquitecto).
   Operador RATIFICO. Atestacion de primera clase VIAJA EN EL GATE DEL SELLO (08-jul), NO intent standalone (GAP-5).
   El piloto de medicion CUMPLIO su proposito (valido captura end-to-end + surfaceo la degradacion de cubetas).
   **ADVERSARIAL-SEPARADO P2+ CONFIRMADO** y horneandose en SPECs P2.x (el Arquitecto ya documento hallazgos, ca548d08).
   **SKILL codegen-triage (TASK-0248):** entregada por Codex FIEL al diseno (banderas rojas ok), in_review, gate formal
   ruteado al Analista (51f7574c). SKILL.md viva en .claude/skills/codegen-triage/.
3. **CHECKER GOAL-P1 = OPCION B (ruteado):** fila medida = Codex maker + adversarial informal + arch-tests/CI, checker_formal=0
   (fiel al schema sellado). Escrutinio formal de P1 = frontera read-only 26-29 jul -> FRONTERA-FIX. Analista-checker-FORMAL
   = solo gobernadas post-30-jul.
4. **SKILL codegen-triage (APROBADA por operador, ruteada):** tarea gobernada Codex-maker/Analista-checker; 2 capas
   (neutral codegen-vs-frontera + recetas instancia Nova); la usa Codex desde P1/P2. codegen!=peon (determinista, cero-tokens,
   NO tratamiento; simetrico por par). Diseno en personal/asesor/DRAFT-skill-codegen-triage.md.
5. **PENDIENTE PARA EL SELLO (NO sellado ahora):** clarificacion codegen!=peon en la def del brazo baseline = INPUT del
   sello 08-jul; el operador la confirma al sellar. NO rutear su sello hasta entonces.
6. **PEONES:** siguen POST-SELLO / F6 (DECISION-0078 + TASK-0231); no se dan de alta; herramienta bajo contrato. No ahora.
8. **SPECs P2 ENTREGADAS Y VERIFICADAS (b3607910):** el Arquitecto entrego 4 SPECs P2 (P2-001 reporte ejecucion
   spec_prepagado/PAR-D anclado, P2-002 parametros, P2-003 UI shell, P2-004 Get_*_List BR-C3). Verifique study-integrity:
   FIELES + con los 3 hallazgos del piloto horneados -> adversarial-separado (SESION SEPARADA, contexto limpio, dev!=
   adversarial, tokens_adversarial_informal taggeados; en tabla de riesgos como DoR), checker_formal=0, spec_prepagado,
   correlation+task_id, y mi deuda GOAL-P1 (harness test del front) como BLOQUEANTE del front P2. Son PREP post-sello (dev
   medido de P2 NO abre pre-sello). Iran a review del Analista. Sin gap que rutear.
7. **DIRECTIVA PERMANENTE "Arquitecto no idle" (1c33540):** mantener la cola del Arquitecto llena. Ruteada cola: (1)
   arranque+registro GOAL-P1+skill; (2) coordinar+gatear P1 con Codex + cerrar fila-piloto; (3) prep/ensayo del sello
   08-jul (manifiesto corpus + sha256 + dry-run submit_intent + validar schema v1.0); (4) preparar SPECs P2.1/P2.2
   (dev medido NO pre-sello). Mientras Codex codea, el Arquitecto avanza 3 y 4 en paralelo. Re-llenar la cola al cerrar
   cada item. Ver [[feedback-arquitecto-no-idle]].
3. **DOMINIO NOVA-BUDGET ABSORBIDO** (brief durable 042eb72, personal/asesor/NOVA-BUDGET-brief-dominio.md):
   cadena de gasto (Aprop->CDP->RP->OBL->Pago, 4 reglas de oro en procs SQL), Clean Arch .NET 10, NO green-field
   (BD endurecida + reconciliada al centavo; hibrido 2024-26 fiel / 2027 limpio), ~45-55% del build = superficies
   sobre procs existentes, brechas de verdad -> nova-hardening (regla 8).
4. **VEREDICTO ULTRACODE** (panel adversarial 8 agentes, en transcript): NO en bloque; depende de 2 REGIMENES.
   Ventana MEDIDA (3-30 jul, baseline+Q4) = mono-orquestador, ultracode PROHIBIDO (rompe Q1/Q4, irreversible).
   POST-medicion (90%+ de Nova) = ultracode SELECTIVO-AMPLIO gatillado por dominio (compone >1 mutacion / cruza
   modulo / toca SESSION_CONTEXT-saldos / alimenta regulatorio). Magnitud = ANCHO -> pipeline barato, no esfuerzo
   por-tarea. "Superficie mecanica" solo si 1-proc/1-vista sin composicion. nova-hardening = ultracode paga pleno.
5. **CODEGEN / SKILL codegen-triage = DEBATE, NO APLICADO** (draft fd8b2ad queda como borrador; DIRECTIVA 9256bb7
   RETIRADA por FYI 3292f86). El operador aclaro: el hilo peones/codegen/skill es DEBATE, no orden -> me pase
   ruteando la skill+sello; los retire. Contenido del debate (SIN aplicar): codegen != peon (determinista, cero-tokens,
   un dev, NO tratamiento) -> podria ser legitimo en ambos brazos, simetrico por par; skill en 2 capas (neutral +
   recetas instancia Nova). NADA sellado, NADA creado. Espera orden explicita para actuar.
6. **PEONES (DEBATE, aclarado):** NO se dan de alta (no participante, no area personal, no agent_registry); herramienta
   no-firmante que Codex operaria bajo contrato (DECISION-0078 PROPOSED + TASK-0231 F6, sandbox piloto-peones). Runbook
   = TEMP_Guia_Modelos_Peones (personal/ungobernado). POST-SELLO. Es DEBATE; no aplicar.
7. **LECCION (2026-07-04):** cuando el operador dice "para debatir" / "es un debate", es DEBATE -> preparo DRAFTS en mi
   area, pero NO ruteo DIRECTIVAs gobernadas al Arquitecto ni sello nada hasta orden explicita ("rutea/ejecuta esto").
   NO usar AskUserQuestion para convertir un debate en go/no-go (eso me hizo enrutar de mas). Ver [[feedback-debate-no-rutear]].

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
