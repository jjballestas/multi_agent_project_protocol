---
message_id: MSG-20260630T011055Z-Operador-to-Arquitecto-DIRECTIVA-medicion-H1-H3
task_id: OPS-MEDICION-H1-H3-20260630
type: DIRECTIVE
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
operator_directive: true
created_at: 2026-06-30T01:10:55Z
context_refs:
  - personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md
  - personal/operador/TFM/FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md
  - Area_comun/reports/REPORT-20260630-dataset-tfm-n500-sello.md
question: "Medicion H1-H3 ejecutada sobre el corpus sellado y el informe HTML de auditoria entregado y revisado por la Analista? Confirmar con FYI de cierre (hora real + dataset recontado por agente)."
requested_action: "Ejecutar la medicion H1-H3 (Fases 0-5 del PLAN-EJECUCION-MEDICION-H1-H3.md) sobre el corpus sellado tag TFM-dataset-N500, emitir veredicto por hipotesis contra los umbrales s.5, entregar un informe HTML de auditoria autocontenido (estilo documento imprimible, no pagina web) con datos crudos reproducibles, pasar el gate adversarial de la Analista, y cerrar de forma gobernada (submit_intent + commit + push si verde)."
one_line_summary: "Operador des-ciega y ordena ejecutar la medicion H1-H3 sobre el corpus N=500 sellado y entregar un informe HTML de auditoria profesional."
---

Directiva del Operador al Arquitecto.

CONTEXTO
- El Operador congelo formalmente el pre-registro v2.0 (FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md).
  Eso des-ciega la medicion: H1-H3 ya pueden medirse.
- Corpus sellado bajo medicion: tag TFM-dataset-N500 -> commit e3646ae (N=500; Arquitecto 253 / Codex 195 / Analista 52).

ORDEN
1) Ejecutar la medicion H1-H3 siguiendo el plan personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md
   (Fases 0 a 5). Resumen de criterios pre-comprometidos (s.5 del pre-registro):
   - H1: deteccion = 100% en A1/A2/A3 (binario) AND FPR = 0% sobre los 500 legitimos AND salud AC2 >= 99%.
   - H2: Delta latencia mediana <= 50 ms/ev AND p95 <= 200 ms/ev; Delta almacenamiento <= 4 KB/ev; Delta tokens <= 5%.
   - H3: acuerdo verificador externo = 100% AND match hash canonico clon-limpio = si (solo claves publicas, DECISION-0046).
2) Reglas de integridad audit-first (vinculantes): medir SOLO sobre el corpus del tag (no el working tree vivo);
   inyeccion de ataques PROGRAMATICA y reproducible con conteos (no juicio de agente, s.8); H3 en clon limpio sin
   secretos; reportar los fallos sin maquillaje.
3) Entregar un informe HTML de AUDITORIA profesional segun el SPEC del plan: archivo .html unico autocontenido,
   estilo documento imprimible (serif, A4, secciones numeradas, portada, tabla de control, anexo de evidencia con
   hashes y conteos crudos), SIN apariencia de pagina web (nada de JS interactivo, menus, animaciones ni assets
   externos). El informe lleva SIEMPRE hora real UTC + estado del dataset recontado por agente.
4) GATE maker != checker: que la Analista haga verificacion adversarial del informe (inyeccion reproducible,
   conteos correctos, veredicto vs s.5 correcto) antes de darlo por final; veredicto en Area_comun/artifacts.
5) Cierre gobernado: submit_intent + commit; memoria (DECISION-0026); push si verde.

ENTREGABLES
- Informe HTML de auditoria (autocontenido) + datos crudos reproducibles junto a el.
- Veredicto por hipotesis (CONFIRMADA/REFUTADA) contra los umbrales s.5, con limitaciones declaradas (s.8).

Reportar cierre con FYI: hora real + dataset recontado (ed25519 seq>=2221 por agente) + ruta del informe HTML.
