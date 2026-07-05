---
task_id: TASK-0246
title: "[VISION-NOVA][NOVA-DEV] Revision adversarial del paquete Ingenas + generar SPECs gobernadas del Sprint 1 (brazo gobernado, NOVA-SPEC-T-001 unificada con intake-v2/DoR)"
type: docs
status: in_review
owner: Arquitecto
phase: P2
priority: high
created_at: 2026-07-03
reviewer: Analista
checker: Analista
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, DECISION-0084, DECISION-0085, DECISION-0050]
linked_decisions: [DECISION-0084, DECISION-0085, DECISION-0050, DECISION-0083]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0246-nova-dev-revision-adversarial-specs-sprint1.md
intake:
  type: doc
  goal: Revision adversarial del paquete NOVA-DEV construido por el Operador (docs Ingenas, fuera del hub) y generacion de las SPECs gobernadas del Sprint 1 del brazo GOBERNADO, partiendo del catalogo de requisitos RES-000..012, con una plantilla UNICA (NOVA-SPEC-T-001 v1.1 unificada con el intake-v2/DoR de DECISION-0084).
  acceptance:
    - Informe adversarial corto del paquete NOVA-DEV (GOAL + prompt de arranque + plantilla de requisitos + maestro NOVA_PRES_00 Docs 00-12): toma lo bueno, complementa huecos, senala contradicciones con la doctrina v1.18.0. Las mejoras al NOVA_PROMPT se PROPONEN en el informe (las aplica el Operador; los docs viven fuera del hub).
    - SPECs gobernadas del Sprint 1 generadas desde el catalogo RES del brazo GOBERNADO (no se reinventan requisitos), con NOVA-SPEC-T-001 UNIFICADA con intake-v2/DoR (un solo formato, no dos compitiendo). Cada campo cita su fuente contra la BD real de 01_Sources.
    - Cada SPEC llena tech_constraints con la ARQUITECTURA OBLIGATORIA (React+TS+Vite front sin SQL; ASP.NET Core .NET 10 en capas NOVA.Api/Application/Domain/Infrastructure/Contracts + NOVA.Mcp; SQL Server 2025 via SPs con gateways tipados EF Core/Dapper; OpenTelemetry; tests unit+integration+architecture; errores de negocio como ProblemDetails). Contradecir la arquitectura o caer en anti-patrones (WebForms/PageMethods, DataTable entre capas, DLLs manuales/HintPath, capa DATABASE generica, secretos en .config, centinelas -99) = hallazgo del gate adversarial.
    - Alcance ACOTADO al brazo GOBERNADO segun NOVA_ESTUDIO_Particion (miembros gobernados de pares, familia P3, pool Q4, BR-C4). NO se tocan ni se leen las fuentes de las unidades BASELINE (GOAL-P1, P2.1, P2.2, P4.1, miembros baseline) -- aislamiento intra-par.
    - Entregable: SPECs commiteadas (hub) + informe adversarial + FYI al Operador. GO adversarial del Analista.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/specs/nova/
    - personal/Arquitecto/
  out_of_scope:
    - NO toca ni lee las fuentes de las unidades BASELINE del estudio (son del Operador; aislamiento intra-par).
    - NO redefine alcances de unidades selladas (cambios = enmienda fechada via Operador).
    - NO aplica mejoras al NOVA_PROMPT directo (se proponen en el informe; los aplica el Operador fuera del hub).
    - NO toca el core pineado (epoch 1.14.0 byte-identico) ni el N=500 sellado.
  risk: medium
  estimate: L
---

# TASK-0246 - [VISION-NOVA][NOVA-DEV] Revision adversarial + SPECs gobernadas Sprint 1

- **Owner:** Arquitecto - **Gate adversarial:** Analista (checker-only). **Decision de producto:** Operador.
- **Fuente de la orden:** MSG-20260703-Operador-to-Arquitecto-ACTION-orden-NOVA-DEV-specs (hold expiro al cerrar F1/F2).

## Contexto
El Operador construyo el paquete NOVA-DEV en `D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/`
(GOAL + prompt de arranque del agente dev + plantilla NOVA-SPEC-T-001 v1.1 + maestro NOVA_PRES_00 Docs
00-12 con el catalogo de requisitos RES-000..012 en s.08). Disciplina documental fuerte + gate adversarial
informal, SIN ledger/firmas/medicion -> pasa por el Arquitecto para mirada adversarial + SPECs gobernadas.

## Alcance (2 partes)
1. **Revision adversarial** del paquete: tomar lo bueno, complementar huecos, senalar contradicciones con la
   doctrina v1.18.0 y con la arquitectura obligatoria. Mejoras al NOVA_PROMPT -> se proponen en el informe.
2. **Generar SPECs gobernadas del Sprint 1** desde el catalogo RES del brazo GOBERNADO, con NOVA-SPEC-T-001
   UNIFICADA con el intake-v2/DoR de DECISION-0084 (un solo formato). Cada campo cita fuente contra la BD real
   de `01_Sources`. tech_constraints = arquitectura obligatoria (ver acceptance).

## Alcance acotado (aislamiento intra-par del estudio)
SOLO unidades del brazo GOBERNADO (NOVA_ESTUDIO_Particion): miembros gobernados de pares, familia P3, pool
Q4, BR-C4. Las unidades BASELINE (GOAL-P1, P2.1, P2.2, P4.1, miembros baseline) NO se tocan ni se leen sus
fuentes. Respetar el sello del estudio (alcances sellados no se redefinen; cambios = enmienda via Operador).

## Secuencia sugerida (RECOMENDACION del Operador)
Primera unidad P3.1 -> pool Q4 en orden del sorteo de Etapa 2 -> miembros gobernados de pares al final
(post-17-jul, cuando el patron congelado exista). Sprint 1 abre 30-jul.

## DoD
- Informe adversarial + SPECs commiteadas en el hub (`Area_comun/specs/nova/`) + FYI al Operador.
- Un solo formato de SPEC (NOVA-SPEC-T-001 unificada intake-v2/DoR). tech_constraints = arquitectura obligatoria.
- Aislamiento respetado (no se leyeron fuentes baseline). ASCII, neutralidad, validate/encoding verdes.
- GO adversarial del Analista (checker-only).

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta al Operador via mailbox.
