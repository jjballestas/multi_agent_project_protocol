---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-orden-NOVA-DEV-specs
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_GOAL_Desarrollo_Aplicacion.md
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_PROMPT_Arranque_Agente_Desarrollo.md
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/NOVA_SPEC_Plantilla_Requisitos.md (NOVA-SPEC-T-001 v1.1)
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/NOVA_PRES_00_Pipeline_Proceso_Presupuestal.html (maestro; reporte de brechas RES-000..012 en s.08)
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Architecture_ExperienciasGH.md (STACK de desarrollo obligatorio)
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Arquitectura_y_Estandar_Desarrollo.html (estandar de desarrollo)
  - D:/Agentes/Ingenas/Budget/01_Sources/ (BD real dbsystem.mdb + convenciones SQL + catalogos; fuentes verificables de las SPEC)
one_line_summary: "Con F1 cerrada expira el hold NOVA-DEV: revision adversarial del paquete Ingenas + generar SPECs gobernadas del Sprint 1 (NOVA-SPEC-T-001 unificada con intake v2/DoR), alcance SOLO brazo gobernado por aislamiento intra-par del estudio."
requested_action: "[DIRECTIVA] (1) El Operador construyo el paquete NOVA-DEV en D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/ (NOVA_GOAL_Desarrollo_Aplicacion.md, NOVA_PROMPT_Arranque_Agente_Desarrollo.md, NOVA_SPEC_Plantilla_Requisitos.md, maestro NOVA_PRES_00 + Docs 01-12). FUENTE DE VERDAD DE REQUISITOS: los requisitos ya existen catalogados como RES-000..012 (reporte de brechas s.08 del maestro NOVA-PRES-000, uno por fase del proceso PRES 00-12) -- son el backlog de QUE se desarrolla; NO se reinventan requisitos. Las SPEC por tarea (SPEC-NOVA-<fase>-<nnn>) se GENERAN desde ese catalogo usando la plantilla NOVA-SPEC-T-001 v1.1 (10 campos, cada campo cita su fuente contra la BD real de 01_Sources). Tu tarea (registrala con intake, owner Arquitecto): (a) REVISION ADVERSARIAL del paquete (tomar lo bueno, complementar huecos, senalar contradicciones con la doctrina v1.18.0); (b) GENERAR las SPECs gobernadas del Sprint 1 partiendo de los RES del brazo gobernado, con NOVA-SPEC-T-001 UNIFICADA con el intake v2/DoR de DECISION-0084 (un solo formato, no dos compitiendo). TECH-STACK OBLIGATORIO (fuente NOVA_Architecture_ExperienciasGH.md + NOVA_Arquitectura_y_Estandar_Desarrollo.html): React+TypeScript+Vite (el frontend jamas toca SQL); ASP.NET Core .NET 10 en capas NOVA.Api/Application/Domain/Infrastructure/Contracts + NOVA.Mcp (APIs internas para agentes, no la BD); SQL Server 2025 con SPs via gateways TIPADOS (EF Core/Dapper); OpenTelemetry (logs/traces/metrics); tests unit+integration+architecture; errores de negocio como ProblemDetails. ANTI-PATRONES PROHIBIDOS: WebForms/PageMethods, DataTable como contrato entre capas, DLLs manuales/HintPath, capa DATABASE generica sin contratos, secretos en .config, centinelas magicos (-99). El campo tech_constraints de cada SPEC se llena con esta arquitectura; contradecirla = hallazgo del gate adversarial. (2) ALCANCE ACOTADO POR EL ESTUDIO: SPECs SOLO para unidades del brazo GOBERNADO segun NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md (misma carpeta Ingenas): miembros gobernados de pares, familia P3, pool Q4, BR-C4. Las unidades BASELINE (GOAL-P1, P2.1, P2.2, P4.1, miembros baseline de pares) son del Operador y NO se tocan ni se leen sus fuentes (regla de aislamiento intra-par del estudio). (3) RESPETAR el sello del estudio: los alcances de unidades selladas no se redefinen; cambios = enmienda fechada via Operador. (4) Entregable: SPECs commiteadas + informe corto de la revision adversarial (hallazgos/complementos) + FYI al Operador. [RECOMENDACION] Secuencia sugerida de SPECs: primera_unidad P3.1, luego pool Q4 en el orden del sorteo de Etapa 2; los miembros gobernados de pares al final (encajan post-17-jul cuando el patron congelado exista). El informe adversarial puede proponer mejoras al NOVA_PROMPT para v1.1 del paquete; se aplican por el Operador, no directo (los docs viven fuera del hub)."
question: ""
---

# ACTION - Revision adversarial NOVA-DEV + SPECs gobernadas del Sprint 1

Con F1 cerrada expira el hold que el Operador puso sobre el paquete NOVA-DEV
("nada al Arquitecto hasta que termine lo que esta haciendo"). El Operador ya
construyo el paquete de desarrollo de la app (GOAL + prompt de arranque del agente
dev + plantilla de requisitos + maestro de proceso presupuestal Docs 00-12) en la
carpeta Ingenas. Tiene disciplina documental fuerte y un gate adversarial informal,
pero SIN ledger/firmas/medicion: por eso pasa por ti.

El detalle vinculante esta en `requested_action`. Lo critico:
- Alcance SOLO del brazo GOBERNADO del estudio (aislamiento intra-par): NO tocar ni
  leer las fuentes de las unidades baseline (son del Operador).
- Un solo formato de SPEC: NOVA-SPEC-T-001 unificada con el intake v2/DoR de
  DECISION-0084 (no dos plantillas compitiendo).
- Los docs del paquete viven FUERA del hub; las mejoras al NOVA_PROMPT se proponen
  en tu informe y las aplica el Operador, no tu directo.

Esta orden va DESPUES de la de F2 a proposito: la instancia (F2.1) es el camino
critico; estas SPECs alimentan el arranque del brazo gobernado (Sprint 1, apertura
30-jul).

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
