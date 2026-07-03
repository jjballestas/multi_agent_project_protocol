# ESTADO del Asesor - fuente de verdad canonica (leer al arrancar)

> Reemplaza al snapshot compartido de .claude (memory/project-state-snapshot.md), DEPRECADO para
> el Asesor. El Asesor mantiene SU estado aqui. Historial completo en git.
> Ultima actualizacion: 2026-07-03 (tarde, F2 COMPLETA + separacion de memoria hecha).

## Identidad y reglas de operacion (no negociable)
- Soy el ASESOR del Operador (John Ballestas), NO el Arquitecto (otra sesion, ejecuta el ledger).
  Participante NO-FIRMANTE (alta REGISTRADA: DECISION-0086, commit 26ac919, 2026-07-03; id `asesor`,
  cero capabilities de ledger, canal=mailbox firmado Operador, area personal/asesor/, agent_registry NO tocado).
- CANAL: ordenes/respuestas al Arquitecto SOLO por MAILBOX (MSG-YYYYMMDD-Operador-to-Arquitecto-*)
  firmado como Operador, commit con pathspec explicito + push. NUNCA submit_intent, NUNCA paste-ready.
- CARRIL (directiva operador 2026-07-03): NO actuar como Arquitecto. Tablero, crons y procesos son
  suyos -> los SENALO/RUTEO por mailbox, no los edito/opero. Stall = diagnostico LIGERO + nudge por
  mailbox, sin operar crons ni leer process trees. (Me sali del carril antes: edite el tablero,
  diagnostique el cron a fondo -> corregido.)
- GATE ASCII PRE-COMMIT BLOQUEANTE: escaneo bytes>127 y ABORTO el commit si hay (no solo aviso;
  patron `python -c '...sys.exit(1 if bad)' || { echo ABORTA; exit 1; }`). Acentos/em-dash son mi
  vicio (paso 3 veces hoy). El gate bloqueante YA me salvo una vez (cazo un acento, aborto). Uso.
- TRAILERS opcion A (persistida en COMMIT_TRAILERS.json, campo operator_advisor_rule): mis commits
  llevan Task-Id: none + Ops-Reason: coordinacion-asesor-mailbox (o Task-Id: TASK-XXXX) + Co-Authored-By,
  en el parrafo final sin lineas en blanco entre trailers. Mi self-filter del monitor caza el Ops-Reason.
- CORTAFUEGOS: ordenes [DIRECTIVA]/[RECOMENDACION]; PRE-DECISION jamas se referencia; DECISIONes =
  requisitos no verbatim; snapshot compartido = solo hechos.
- PROACTIVIDAD SIN PREGUNTAR: preparo el siguiente entregable de cada gate; solo orden contraria frena.
- LECCION watchdog (falso-jam 2026-07-03): NO llamar jam por DURACION en tareas pesadas conocidas
  (e2e/harness corren 35+ min legitimo). Solo jam con firma real: err.log de hang, lease vencida, sin
  heartbeat. Los node/esbuild huerfanos NO son conclusivos (persisten entre builds).

## Deberes al arrancar
1. AUTO-POLL: git fetch/pull, git log -8, ls Area_comun/mailbox/open/, pendientes TASK_INDEX.
2. Arma MONITOR persistente sobre origin/main con SELF-FILTER por trailer (salta commits con
   "Ops-Reason: coordinacion-asesor"): PIPELINE de peers + *-to-Operador-* nuevos + stall 30min.
3. Auto-poll de cada turno = red primaria; monitor = respaldo.

## Estado del proyecto (2026-07-03 tarde)
- **F1 (nucleo doctrinal) CERRADO 7/7** (v1.18.0 tageada, gate de trailers activo, epoch 1.14.0 pineado).
- **F2 (instancia distribuida) COMPLETA 4/4:** 0230 (instancia Aegis en D:/Agentes/Zeus/NOVA/Aegis) +
  0232 (harness distribuido) + 0233 (e2e) + 0234 (runbook, cerro en fix-loop 2/2). Todas con ciclo
  adversarial real. DECISION-0085: NOVA/ paraguas + Aegis instancia-metodologia NEUTRAL (arm nova-suite)
  + NOVA/Nova-X productos LAZY. Atestacion del estudio se queda en el HUB.
- **Pendientes backlog VN:** TASK-0231 (F6.1 peones, proposed) + TASK-0245 (watchdogs->skills, proposed).
  No urgentes.
- **Arquitecto REINICIO sesion** (2026-07-03 tarde) tras cerrar F2. Su cold-start debe tomar del mailbox:
  mi alta de Asesor + la orden NOVA-DEV + la de emplazar scripts de medicion.

## SIGUIENTE (el pivote a producto + medicion)
1. **NOVA-DEV = TASK-0246** (proposed, owner Arquitecto, checker Analista; registrada 93c7448 2026-07-03):
   revision adversarial del paquete Ingenas + SPECs gobernadas Sprint 1 (RES-000..012 + arquitectura
   obligatoria .NET10/React + SPEC-T-001 UNIFICADA con intake-v2/DoR). Alcance SOLO brazo gobernado,
   aislamiento intra-par (no lee fuentes baseline). SPECs al hub Area_comun/specs/nova/ (NO crea repo
   producto aun; Nova-X LAZY). ENLACE: su verificacion de cada campo contra la BD real de 01_Sources
   produce la evidencia readonly (proc/vista existe) que mi SELLO s.5 tiene como [LLENAR-AL-SELLAR] ->
   COSECHAR al entregar para enumerar el pool Q4. Mi tarea: revision adversarial cuando entregue.
   RONDA 1 ENTREGADA (ff68ee8): informe adversarial + SPEC-NOVA-P3-001 (P3.1 Initial Budget Draft).
   Revision Asesor = LIMPIA (unificacion plantillas OK, aislamiento OK, pool Q4 identico a mi SELLO s.5,
   P3.1 fuera de Q4 como pattern-setter). COSECHA aplicada a SELLO s.5: F-NOVA-01 confirma readonly con
   SELECT/VIEW-DEF pero SIN EXECUTE -> existencia verificable YA (sin GRANT), paridad requiere GRANT EXECUTE.
   Gate formal = Analista (pendiente). Siguientes rondas NOVA-DEV: pool Q4 en orden de sorteo + pares al final.
   RONDAS 2-3 (P3-002 CDP, P3-003 RP): AMBAS LIMPIAS en mi revision -- aislamiento gemelos OK (P3.2/P3.3
   separadas de hermanos baseline P4.2/P4.3; ajustes 08/09/11/12 fuera de alcance), Q4-condicional correcto,
   coherencia cross-SPEC (P3-003 reusa B-01 de P3-002), compensaciones de brechas BD = senal de calidad no confound.
   GO-CONTINUA enviado al Arquitecto (89d926f, orden operador "manten al Arquitecto trabajando"): sigue P3-004
   Obligation -> P3-005 Payment -> pool Q4 no-P3, sin reposo. NOTAS DE ESTUDIO ruteadas: P3-005 Payment = ALTA
   (frontera Treasury) FUERA de Q4 (solo descriptiva, regla criticidad sellada); P4.4 = media DENTRO de Q4.
   Advertencia al operador: SPECs acumulan decisiones de dominio (objeto min-15, default SECOP) marcadas
   como preguntas -> resolver al construir (se mide la coordinacion). TRACKER VIVO en
   personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md (DD-01 auth, DD-02 objeto, DD-03 SECOP).
   RONDAS 6-8 LIMPIAS: P4-004 (aislamiento CRITICO impecable, excluye P4.1/P4.2/P4.3 baseline), P6-003
   (OTel infra, borde con reporte P2.2 baseline OK; OTel = telemetria operacional != medicion del ledger),
   P2-004 (Get_*_List, miembro gobernado PAR-D + fabrica Q4). CATCH CLAVE cosechado al SELLO s.5: los ~4
   Get_*_List son CLUSTER casi isomorfo load-bearing para n>=10 -> Q4 declara n efectivo reducido; doble rol
   PAR-D/Q4 NO es confound (contrastes pre-registrados distintos).
   RONDA 9 (P2-003 UI exploracion): LIMPIA, cierra POOL Q4. NOVA-DEV TANDA ACTUAL COMPLETA = 9 SPECs
   (familia P3 P3.1-3.5 + pool Q4: P4.4/P2.3/P6.3/Get_*_List, n=10 nominal / n efectivo<10 sellado). Las 9
   revisadas limpias por el Asesor; aislamiento intacto en todas (gemelos P4.x, PAR-D, borde P2.2). FALTAN:
   (a) miembros GOBERNADOS de pares (post-17-jul, heredan patron congelado P4.1); (b) GATE FORMAL del Analista
   sobre TASK-0246 (mis revisiones = asesoria, no la gobernanza). DECISIONES DE DOMINIO estables en 3
   (DD-01 auth/DD-02 objeto/DD-03 SECOP) -> listas para resolver en lote con el operador.
   GATE FORMAL ANALISTA = CAMBIO-REQUERIDO (9a2c211): F-0246-01 (q4_membership ausente en P3-001/002/003,
   previas a mi GO, sin back-fill) + F-0246-02 (P4-004 exige THROW 50256/50254 pero el proc desplegado
   Apply_Obligation_Adjustment emite 50265, verificado por el Analista via readonly). AMBOS los PASO POR ALTO
   mi revision de asesor. LECCION CLAVE: mis revisiones son design + study-integrity, NO sustituyen la
   VERIFICACION EMPIRICA contra la BD desplegada (no tengo readonly en esta sesion). Este NO-GO es DEMOSTRACION
   EN VIVO de la tesis del estudio (checker formal atrapo un bug de falsabilidad que las revisiones informales
   dejaron pasar) -> evidencia anecdotica. VALOR-ADD ruteado al Arquitecto (RECOMENDACION, no-firmante via
   Operador): generalizar la re-verificacion de THROW a las 9 SPECs (riesgo sistemico, mismos codigos escritos
   desde PRES no desde procs). Remediacion = del Arquitecto (fix-loop max 2 iter). Yo espero el re-juicio.
   RONDAS 4-5 (P3-004 Obligation, P3-005 Payment): AMBAS LIMPIAS. FAMILIA P3 COMPLETA 5/5 (presupuesto->CDP->
   RP->obligacion->pago). P3-005 marcada q4_membership=FUERA (ALTA/Treasury) segun mi GO -> el Arquitecto
   aplico mi nota de estudio. Disciplina de frontera: P3-004 difiere radicacion a GOAL-P5; P3-005 difiere el
   egreso real (banco/retenciones/comprobante) a Tesoreria/PayControl. TALLY POOL Q4 revisado = 3 unidades
   (P3.2/P3.3/P3.4); faltan del pool: P4.4, P2.3, P6.3, Get_*_List. P3.1 y P3.5 fuera de pool (pattern-setter / ALTA).
2. **F3 / medicion:** mi SELLO ETAPA 1 (draft listo, se sella <=08-jul, llenar placeholders + sorteo
   NIST) + scripts al hub (ruteado) + Operador abre GOAL-P1 (piloto baseline). LA MEDICION NO HA
   ARRANCADO AUN (F1/F2 = infraestructura, no desarrollo medido).
3. Sprint 1 gobernado: 30-jul (gate duro).

## Mis entregables (todos en personal/operador/vision-nova/)
- HECHO Y COMMITEADO (11fddf4, 2026-07-03): scripts-medicion/ (medicion_ledger.py + schema_medicion.json
  [52 cols, 5 campos peones + par_id na_ok] + schema_defectos.json + README). Journal append-only -> vista
  materializada. Smoke re-verificado verde ciclo completo (OPEN/UPDATE/CLOSE/verificar/sha256 incl. peones).
  README corregido 47->52 cols. ANTES estaban solo en disco (sin commitear); ahora en git, atestables.
  Listos para congelar a v1.0 en el sello Etapa 1.
- HECHO: SELLO-ETAPA-1-nova-budget-DRAFT.md (pre-registro; placeholders [LLENAR-AL-SELLAR]).
- HECHO: separacion de memoria (esta area personal/asesor/ + alta ruteada).

## Contexto real del negocio (clave)
Objetivo real = Nova Budget/Accounting/Payroll/Treasury para la EMPRESA del operador, employee-ready.
Stack: Clean Architecture .NET 10 (Api/Application/Domain/Infrastructure/Mcp/Contracts) + React/TS/Vite
+ SQL Server 2025 + OpenTelemetry; anti-patrones prohibidos (WebForms, DataTable entre capas, DLLs
manuales, secretos en .config, centinelas -99). Requisitos = RES-000..012 (brechas s.08 de NOVA-PRES-000);
SPECs desde NOVA-SPEC-T-001 v1.1. Todo en D:/Agentes/Ingenas/Budget/. Composicion del equipo: 12 roles
-> 4 firmantes (Operador=dominio, Arquitecto=arquitectura+docs, Codex=maker, Analista=security+QA checker);
Legacy Analyst sin firmante = eslabon debil de atestacion.

## Que afirma / NO afirma el estudio (delimitacion sellada)
Da: instrumentacion + Q4 causal (ligero-vs-completo) + serie honesta de calidad (checker formal atrapa
lo que el informal dejo pasar) + transferibilidad (2a instancia dominio real vs N=500 auto-dogfood). NO
da: "el gobierno mejora la calidad" causal (maker!=checker YA existe en ambos brazos; el tratamiento es
el checker FORMAL atestado). Veredicto de compra se difiere a replica employee-run pre-registrada.
Peones: se mide el USO (5 campos), su EFECTO solo en F6 aislado (no confundir el contraste central).

## Pendientes del operador (recordar con tacto)
Abrir GOAL-P1 (fila 6-campos); GRANT EXECUTE; sandbox mutadores (<=14-jul); estimates S/M/L (<=08-jul);
revision legal del consentimiento. F1.6 (aprendizajes-externos, extraccion de reglas) pendiente, paralelo,
NO es entregable del Asesor.
