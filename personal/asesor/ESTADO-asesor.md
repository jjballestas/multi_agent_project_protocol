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
