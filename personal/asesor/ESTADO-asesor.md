# ESTADO del Asesor - fuente de verdad canonica (leer al arrancar)

> Reemplaza al snapshot compartido de .claude (memory/project-state-snapshot.md), que queda
> DEPRECADO para el Asesor. El Asesor mantiene SU estado aqui. Historial completo en git.
> Ultima actualizacion: 2026-07-03 (sesion asesor, tarde).

## Identidad y reglas de operacion (no negociable)
- Soy el ASESOR del Operador (John Ballestas), NO el Arquitecto (corre en otra sesion y ejecuta
  el ledger). Participante NO-FIRMANTE (alta ruteada 2026-07-03).
- CANAL: toda orden/respuesta al Arquitecto por MAILBOX (Area_comun/mailbox/open/,
  MSG-YYYYMMDD-Operador-to-Arquitecto-*.md) firmada como Operador, commiteada con pathspec
  explicito y pusheada. NUNCA submit_intent. NUNCA paste-ready por chat.
- CARRIL (directiva operador 2026-07-03): NO actuar como Arquitecto. Tablero, crons y procesos
  son del Arquitecto -> los SENALO/RUTEO por mailbox, no los edito/opero yo. Diagnostico de
  stall LIGERO (observacion -> nudge por mailbox), sin operar sus crons ni leer sus process trees.
- GATE ASCII PRE-COMMIT BLOQUEANTE: antes de commitear CUALQUIER archivo, escaneo bytes>127 y
  ABORTO el commit si hay (no solo aviso). Em-dash/acentos son mi vicio recurrente (paso 2 veces
  hoy: 'romperia' y el em-dash). Normalizo -> '--' y acentos -> ascii.
- TRAILERS opcion A (persistida en COMMIT_TRAILERS.json): mis commits llevan Task-Id: none +
  Ops-Reason: coordinacion-asesor-mailbox (o Task-Id: TASK-XXXX si aplica) + Co-Authored-By, en el
  parrafo final sin lineas en blanco entre trailers. Mi self-filter del monitor caza el Ops-Reason.
- PROACTIVIDAD SIN PREGUNTAR: preparo el siguiente entregable de cada gate sin pedir permiso; solo
  una orden contraria me frena. Tablero desactualizado vs ledger = reporte falso.

## Deberes al arrancar
1. AUTO-POLL: git pull/fetch, git log, ls Area_comun/mailbox/open/, pendientes de TASK_INDEX.
2. Armar MONITOR persistente sobre origin/main (self-filter por trailer Ops-Reason): PIPELINE de
   peers + mensajes *-to-Operador-* nuevos + stall 30min. (Comando en git history del monitor.)
3. Auto-poll de cada turno = red primaria; el monitor = respaldo.

## Estado del proyecto (2026-07-03 tarde)
- **F1 (nucleo doctrinal) CERRADO 7/7** (v1.18.0 tageada, gate de trailers activo, epoch 1.14.0
  pineado intacto).
- **F2 (instancia distribuida) en el cierre:** 0230 (instancia Aegis en D:/Agentes/Zeus/NOVA/Aegis
  por DECISION-0085) + 0232 (harness distribuido) + 0233 (e2e) = DONE; **0234 (runbook) in_review**
  = ultimo. DECISION-0085: NOVA/ carpeta paraguas + Aegis instancia-metodologia NEUTRAL (arm
  nova-suite) + NOVA/Nova-X productos lazy. Atestacion del estudio se queda en el HUB.
- **Ordenes vivas en mailbox (mias, al Arquitecto):** F2-instancia, NOVA-DEV-specs (con RES-000..012
  + tech-stack .NET10/React + SPEC-T-001), peones-medicion-aislamiento, emplaza-scripts-medicion-hub,
  alta-asesor-no-firmante.

## Mis entregables
- HECHO: scripts de medicion (personal/operador/vision-nova/scripts-medicion/: medicion_ledger.py +
  schema_medicion.json [52 cols, incluye 5 campos peones + par_id na_ok] + schema_defectos.json +
  README). Modelo journal append-only -> vista materializada. Probados. Ruteados al hub (directiva).
- HECHO: SELLO ETAPA 1 DRAFT (personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md):
  pre-registro con diseno congelado + placeholders [LLENAR-AL-SELLAR] (sha256 corpus, pulso NIST,
  verificacion readonly Q4). Se sella <=08-jul.
- PENDIENTE: al sellar (08-jul) llenar placeholders + sorteo NIST.

## La medicion NO ha arrancado aun
Lo que corre (F2) es INFRAESTRUCTURA de la metodologia, no desarrollo medido. Falta: Arquitecto
emplaza scripts en el hub; Operador abre GOAL-P1 (fila 6-campos + estimates + GRANT EXECUTE);
sello 08-jul. El corpus del hub tiene el N=500 viejo (Zeus-Protocol, sellado, FONDO INTOCABLE),
separado del estudio NOVA.

## Contexto real del negocio (clave)
Objetivo real = Nova Budget/Accounting/Payroll/Treasury para la EMPRESA del operador, con la
metodologia employee-ready. Stack: Clean Architecture .NET 10 (Api/Application/Domain/Infrastructure/
Mcp/Contracts) + React/TS/Vite + SQL Server 2025 + OpenTelemetry; anti-patrones prohibidos (WebForms,
DataTable entre capas, DLLs manuales, secretos en .config, centinelas -99). Requisitos = RES-000..012
(brechas s.08 de NOVA-PRES-000); SPECs desde NOVA-SPEC-T-001 v1.1. Todo en D:/Agentes/Ingenas/Budget/.

## Que afirma / NO afirma el estudio (delimitacion sellada)
Da: instrumentacion + Q4 causal (ligero-vs-completo) + serie honesta de calidad (checker formal
atrapa lo que el informal dejo pasar) + transferibilidad. NO da: "el gobierno mejora la calidad"
causal (maker!=checker ya existe en ambos brazos; el tratamiento es el checker FORMAL atestado). El
veredicto de compra se difiere a una replica employee-run pre-registrada.

## Pendientes del operador (recordar con tacto)
Abrir GOAL-P1 (fila 6-campos); GRANT EXECUTE; sandbox mutadores (<=14-jul); estimates S/M/L (<=08-jul);
revision legal del consentimiento. F1.6 (aprendizajes-externos, extraccion de reglas) sigue pendiente,
paralelo, no es entregable del Asesor.
