---
task_id: TASK-0308
file: Area_comun/tasks/TASK-0308-medicion-preregistrada-h1-h3.md
title: "Medicion pre-registrada H1-H3 sobre el corpus sellado TFM-dataset-N500 (informe de auditoria + datos crudos, dos brazos adversariales)"
status: review_approved
type: analysis
owner: Arquitecto
reviewer: Analista
priority: normal
relates_to:
  - DECISION-0105
created_at: 2026-08-02
intake:
  type: research
  goal: >
    Ejecutar la medicion PRE-REGISTRADA H1-H3 (PRE-REGISTRO-H1-H3-v2.md, FROZEN v2.0; freeze del operador
    FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md) sobre el corpus SELLADO TFM-dataset-N500 (commit e3646ae, N=500,
    core e1dc631, epoch 1.14.0) y entregar (a) el informe HTML de auditoria y (b) los datos crudos reproducibles,
    con veredicto MECANICO contra los umbrales pre-comprometidos s.5, sin maquillaje. La medicion es READ-ONLY sobre
    el tag (no toca el corpus, el config pineado, el epoch ni genera eventos para el dataset). Diseno de DOS BRAZOS
    adversariales independientes (Arquitecto + recomputo ciego) para cazar subdeterminaciones (diff-entre-brazos).
    Etiquetado de veredictos: CONSERVADOR contra el umbral literal s.5 (decision del operador 2026-08-02).
  acceptance:
    - "AC1 (recomputo independiente del sello, FASE 0): en clon limpio del tag, los 5 pineados byte-identicos (eventlog 59a8ae87, validator eb04799f, config 2e35f26e, override event-state.runtime.json b9706842, pre-registro v2.0 e8277cc7), 500/500 eventos elegibles (seq>=2221 AND intent.applied AND actor_auth.method==ed25519) con desglose {Arquitecto 253, Codex 195, Analista 52} == reporte de sello 2026-06-30; validate + scan_encoding exit 0."
    - "AC2 (H1, FASE 1-2): inyeccion PROGRAMATICA y reproducible de ataques por vector (A1 alteracion/borrado/insercion/reordenamiento; A2 atribucion-cruzada/keyid-no-registrado/firma-invalida) sobre copias del corpus, con CONTEOS (no juicio de agente); TPR por vector contra umbral 100%. FPR=0% sobre los 500 legitimos; AC2 salud >=99%. El vector borrado-de-evento REPORTA sin maquillaje la evasion de TRUNCAMIENTO DE COLA (cabeza no anclada, corpus con 0 anclas = limitacion A3 declarada). A3 rollback: no ejercitable en corpus (0 anclas); rollback sintetico rechazado."
    - "AC3 (H2, FASE 3): sobrecoste #4 vs baseline sin #4 sobre la misma carga. Almacenamiento <=4KB/ev; tokens <=5% (estructural: campos #4 fuera del contexto del agente). Latencia: AMBAS lecturas -- coste marginal de la cripto de #4 (ed25519+prev_hash+HMAC) Y Delta end-to-end de submit_intent (mediana/p95); el veredicto contra la metrica literal (camino submit_intent, end-to-end) se etiqueta REFUTADA y se caracteriza como artefacto O(n) del core sellado fijado post-sello por DECISION-0105 (no retro-aplicable por audit-first)."
    - "AC4 (H3, FASE 4): en clon limpio SIN secretos (solo publicas), los 500 actor_auth verifican (acuerdo 100%); protocol_state_drift has_drift=False; gate real validate_collaboration_state.py exit 0. Cita CORREGIDA: runtime/protocol_replay.py --check-drift es no-op en el tag (sin __main__) -> su exit 0 es vacuo, NO se cita como verificacion externa."
    - "AC5 (entregables + integridad): informe HTML de auditoria (self-contained, print-friendly, hora real local+UTC, dataset recontado por agente) + datos crudos de AMBOS brazos (CONSOLIDATED_arm1/arm2, RECONCILE, drivers fase1/fase3) re-ejecutables sobre un clon limpio del tag, en Area_comun/reports/. Veredicto mecanico conservador vs s.5 + limitaciones s.8. Fondo intocable NO modificado (corpus N=500, config 2e35f26e, epoch 1.14.0). Gates verdes."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - Area_comun/reports/REPORT-20260802-medicion-H1-H3-audit.html
    - Area_comun/reports/data-medicion-H1-H3-20260802
  out_of_scope: >
    Modificar el corpus sellado (TFM-dataset-N500 / events.jsonl), el config pineado (2e35f26e), el epoch (1.14.0),
    el genesis, o generar eventos "para el dataset". Cambiar hipotesis/metricas/umbrales del pre-registro (estan
    congelados; esto solo MIDE). Vector A4 (fuera de alcance por el pre-registro). Codigo de producto Zeus.
  risk: low
  estimate: M
notes: >
  Directiva del operador 2026-08-02: "iniciar con el sello N=500 -> ejecutar los brazos del estudio". Plan de
  ejecucion: personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md. Maker = Arquitecto (single-writer/runtime, por
  designacion del plan del operador); checker = Analista (gate maker != checker, FASE 6c). El diff-entre-brazos cazo
  dos subdeterminaciones reales del brazo 1 (falso-100% en borrado-de-evento por truncamiento de cola; verificador
  externo vacuo), ambas re-verificadas y corregidas -> evidencia viva de que el metodo detecta defectos de su sujeto.
---

# TASK-0308 - Medicion pre-registrada H1-H3 sobre el corpus sellado N=500

## Contexto
El dataset del TFM esta SELLADO en N=500 (tag TFM-dataset-N500 -> e3646ae; reporte de sello 2026-06-30). El operador
congelo el pre-registro v2.0 (des-ciega H1-H3). Esta tarea EJECUTA la medicion pre-registrada sobre ese corpus y
entrega el informe de auditoria + datos crudos, con veredicto mecanico contra los umbrales pre-comprometidos s.5.

## Entregables
- Area_comun/reports/REPORT-20260802-medicion-H1-H3-audit.html (informe de auditoria formal).
- Area_comun/reports/data-medicion-H1-H3-20260802/ (datos crudos de ambos brazos + drivers reproducibles).

## Gate maker != checker
El Analista verifica adversarialmente: (1) que la inyeccion fue programatica/reproducible (no juicio de agente);
(2) que los conteos cuadran (recomputo independiente); (3) que el veredicto contra s.5 es correcto y sin maquillaje;
(4) que el fondo intocable no se modifico. Veredicto en Area_comun/artifacts/.

## Resultado (resumen, etiquetado conservador vs umbral literal)
- H1: deteccion 100% en 6/7 vectores + FPR 0% + AC2 100% (CONFIRMADO); clausula universal "100% en TODO vector"
  REFUTADA por truncamiento de cola (limitacion A3 cabeza-no-anclada declarada; corpus con 0 anclas).
- H2: almacenamiento (+359..387 B/ev) y tokens (~0%) CONFIRMADOS; latencia end-to-end REFUTADA (artefacto O(n) del
  core sellado, fijado post-sello por DECISION-0105); coste marginal de #4 = 0.03-0.07 ms/ev.
- H3: CONFIRMADA (500/500 verificables sin secretos, drift False).
