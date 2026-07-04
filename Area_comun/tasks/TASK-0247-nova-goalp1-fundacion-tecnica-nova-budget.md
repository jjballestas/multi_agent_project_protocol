---
task_id: TASK-0247
title: "[VISION-NOVA][NOVA-GOAL-001][GOAL-P1] Fundacion tecnica de Nova-Budget (sln + capas .NET 10 + apps/nova-web + architecture tests + infra transversal + CI). Piloto baseline (opcion B, checker_formal=0)."
type: build
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-07-04
reviewer: Arquitecto
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, NOVA-GOAL-001, DECISION-0088, DECISION-0050, DECISION-0085]
linked_decisions: [DECISION-0088, DECISION-0050, DECISION-0085, DECISION-0084]
linked_reqs: []
file: Area_comun/tasks/TASK-0247-nova-goalp1-fundacion-tecnica-nova-budget.md
intake:
  type: infra
  goal: Levantar la FUNDACION TECNICA de Nova-Budget (GOAL-P1, primer item del backlog NOVA-GOAL-001): el esqueleto gobernado y las barandas, sin verticales de negocio. Es el piloto de medicion del brazo BASELINE (excluido del contraste). Codigo en el repo propio Nova-Budget (fuera del hub, DECISION-0050); governance/coordinacion en el HUB durante la ventana del estudio (DECISION-0088). El contrato de build son los docs de D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura (NOVA_GOAL_Desarrollo_Aplicacion, NOVA_PROMPT_Arranque_Agente_Desarrollo, apendice .NET10).
  target_user: El equipo de desarrollo de Nova-Budget (agentes NOVA) y el Operador que opera/mide el piloto.
  acceptance:
    - NOVA.sln con las 6 capas src/NOVA.Api, NOVA.Application, NOVA.Domain, NOVA.Infrastructure, NOVA.Contracts, NOVA.Mcp (dependencias Api -> Application -> Domain/Infrastructure; Mcp cliente hermano de Api, no ruta de datos).
    - apps/nova-web (React + TypeScript + Vite) shell operativo (typecheck verde).
    - tests/NOVA.UnitTests, NOVA.IntegrationTests, NOVA.ArchitectureTests creados.
    - Los 5 architecture tests como MECANISMO de enforcement, verdes: Domain no depende de Infrastructure; Application no depende de ASP.NET; Api no accede SQL directo; Mcp no accede SQL directo; cero DataTable entre capas.
    - Infra transversal: health checks, OpenAPI publicado, ProblemDetails middleware, logging estructurado + correlation-id (que carga el task_id de medicion).
    - CI minimo verde: restore, build, tests, typecheck del front.
    - Stack fijo: ASP.NET Core .NET 10, React/TS/Vite. P1 usa SOLO el conector READ-ONLY (EXECUTE no se pide hasta GOAL-P2); los integration tests de P1 son de esquema/conectividad, NO de EXEC de procs.
    - Gate de cierre = el GATE SELLADO de GOAL-P1 (NOVA_ESTUDIO_Particion s.2.1): "architecture tests + CI verde + adversarial informal" (veredicto APROBADO del checklist de 12 puntos, agente separado en contexto limpio; corre en AMBOS brazos, NO es tratamiento) + evidencia real. El hub SOLO coordina + atesta; SIN gate formal del Analista sobre el codigo (opcion B; el Analista PUEDE validar DoD/evidencia sin contar como checker_formal). DoD = GOAL s.10 adaptado a P1.
    - Orquestacion MONO (operador + 1 dev + 1 adversarial por tarea; sin peones, orchestration_mode=mono). CHECKPOINT sellado 11-jul: P1 completa (architecture tests + CI + adversarial informal); si no, orden de caida.
    - Repo Nova-Budget inicializado por Codex como PRIMER paso: git init + remote add origin https://github.com/jjballestas/Nova-Budget.git + scaffold P1 + primer push a la rama principal (remoto hoy vacio).
    - Entregable: codigo commiteado y pusheado a Nova-Budget + handoff autocontenido en el hub + evidencia real (salidas de tests, OpenAPI, ProblemDetails provocado). NO auto-cierra: el Arquitecto atesta y el Operador mide con medir-goalp1.ps1.
  verification_cmd:
    - "(en D:/Agentes/Zeus/NOVA/Nova-Budget) dotnet build"
    - "(en D:/Agentes/Zeus/NOVA/Nova-Budget) dotnet test"
    - "(en D:/Agentes/Zeus/NOVA/Nova-Budget/apps/nova-web) npm run typecheck"
    - python scripts/validate_collaboration_state.py
  scope_routes:
    - D:/Agentes/Zeus/NOVA/Nova-Budget
    - Area_comun/tasks/TASK-0247-nova-goalp1-fundacion-tecnica-nova-budget.md
    - Area_comun/handoffs/
  out_of_scope:
    - NO verticales de negocio (P2..P6): sin read model, sin drafts/aprobaciones, sin ajustes/reversos, sin integraciones. Solo la fundacion.
    - NO EXECUTE de stored procs (P1 = conector read-only; EXECUTE se pide en GOAL-P2).
    - NO governance ni atestacion DENTRO del repo Nova-Budget (DECISION-0050 #1: solo codigo; la governance vive en el hub).
    - NO reimplementar en C# reglas SQL (saldos/cuadre/numeracion/cierre): la capa de datos ya esta completa; el C# arma draft -> llama proc -> traduce.
    - NO tocar el core pineado del hub (epoch 1.14.0 byte-identico) ni el N=500 sellado.
    - NO segunda instancia Aegis ahora (DECISION-0088: NOVA/Aegis en reserva probada para post-sello).
  tech_constraints:
    - ASP.NET Core .NET 10 en capas (Api/Application/Domain/Infrastructure/Contracts/Mcp); React+TS+Vite (apps/nova-web) sin SQL; SQL Server 2025 via gateways tipados (EF Core/Dapper/SP), reads via vistas/Get_*; OpenTelemetry; OIDC/JWT; FluentValidation; ProblemDetails.
    - Anti-patrones PROHIBIDOS (hallazgo del gate): WebForms/PageMethods, DataTable entre capas, DLLs manuales/HintPath, capa DATABASE generica, secretos en .config, usuario privilegiado/sa, centinelas -99/-999, numeracion de documentos en UI, SQL directo/dinamico desde cualquier capa, React consumiendo DLLs de negocio, reglas SQL reimplementadas en C#.
  assets_inputs:
    - Contrato de build (read-only, fuera del hub): D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Development_Goal/NOVA_GOAL_Desarrollo_Aplicacion.md (s.6 layout, s.8 P1, s.10 DoD, s.3 reglas) + NOVA_Budget_Process/NOVA_PROMPT_Arranque_Agente_Desarrollo.md + NOVA_Apendice_Estructura_DotNet10_Dominios.html.
    - Remoto de producto: https://github.com/jjballestas/Nova-Budget.git (existe, vacio). Clon local: D:/Agentes/Zeus/NOVA/Nova-Budget.
  risks_list:
    - Conector read-only sin EXECUTE limita los integration tests de P1 a esquema/conectividad (declarado; EXEC llega en P2).
    - MAX_PATH en Windows para el checkout: usar core.longpaths=true.
  priority: high
  risk: medium
  estimate: L
  measurement_note: "Fila BASELINE del piloto de medicion (opcion B, DIRECTIVA-checker-semantics-goalp1): checker_formal=0 y coordinacion_gobierno=0 por definicion del schema sellado; el checker VIVO es el adversarial informal de 12 puntos; el gate formal del Analista se reserva a lo gobernado post-30-jul. El Operador opera medir-goalp1.ps1 (BUILD REAL, no el smoke); el Arquitecto atesta el sha256 -> #4 del hub."
---

# TASK-0247 - GOAL-P1: Fundacion tecnica de Nova-Budget (piloto baseline)

Primer item del backlog NOVA-GOAL-001. Levanta el esqueleto .NET 10 + React/TS/Vite de Nova-Budget con las
barandas (architecture tests, ProblemDetails, health/OpenAPI/correlation-id, CI) SIN verticales de negocio.
Codigo en el repo propio Nova-Budget (DECISION-0050); governance en el hub (DECISION-0088). Es el piloto de
medicion del brazo BASELINE (opcion B: checker_formal=0; el checker vivo es el adversarial informal de 12
puntos que corre en ambos brazos). Detalle vinculante en el bloque intake. Owner Codex (maker); el Arquitecto
atesta; el Operador mide.
