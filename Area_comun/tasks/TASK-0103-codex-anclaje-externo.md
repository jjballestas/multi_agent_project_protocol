---
id: TASK-0103
owner: Codex
status: proposed
type: implementation
priority: normal
created_at: 2026-06-12
updated_at: 2026-06-12
depends_on: [TASK-0101]
relates_to: [DECISION-0029, DECISION-0023, DECISION-0019]
phase: P2
spec_id: pending (SPEC a formalizar por Claude antes de GO)
linked_decisions: [DECISION-0029, DECISION-0023, DECISION-0019]
deliverables:
  - anclaje externo periodico del digest de cabeza de la cadena (backend configurable), off-by-default
  - verificador de monotonia contra anclas (anti-rollback)
relevant_files:
  - runtime/eventlog.py
  - scripts/sign_release.ps1
  - protocol.config.json
blocked_by_questions: []
objective: (DECISION-0029 pieza 2c) Publicar periodicamente el digest de cabeza de la cadena prev_hash en al menos un medio fuera del control de escritura del runtime - remoto git independiente, log de transparencia, o sellado RFC 3161. Backend configurable y vendor-neutral (patron DECISION-0023). Cierra la ventana de reescritura - el runtime puede manipular su copia local pero no lo ya publicado.
expected_output: (1) Bloque de config (frecuencia, backend, destino) off-by-default. (2) Comando de anclaje invocable manualmente y desde el orquestador al cierre de turno/corrida. (3) Verificador - dada una serie de anclas externas, valida que la cadena local las contiene en orden (monotonia anti-rollback; cubre A1 y A3-reescritura del modelo de DECISION-0029). (4) Golden cases - rollback de snapshot detectado contra ancla; cadena legitima verifica; ancla faltante reportada como ventana de riesgo (riesgo residual declarado, no error). (5) Sin secretos en el repo; sin dependencia obligatoria de servicios de pago.
question_to_resolve: Q1 backend por defecto con cero coste y cero secretos (remoto git independiente parece el candidato; evaluar). Q2 frecuencia de anclaje por defecto (por corrida vs por N eventos) - trade-off ventana de omision vs ruido. Q3 donde registra el verificador las anclas conocidas (archivo versionado vs config de instancia).
closure_criterion: anclaje bajo flag off-by-default con backend configurable; verificador de monotonia con golden cases verdes (rollback detectado); ventana residual documentada en la SPEC; sin secretos; validador/neutralidad/encoding verdes; handoff con evidencia.
sdd_required: true
---

# TASK-0103 - Anclaje externo periodico de la cadena (DECISION-0029 pieza 2c)

> PROPOSED (Claude 2026-06-12, habilitada por DECISION-0029). Depende de TASK-0101. Puede ejecutarse en
> paralelo con TASK-0102. Promover a ready+GO cuando el operador lo indique y la SPEC este cerrada.

## Contexto

Ver DECISION-0029 (decision 2c y riesgo residual declarado). Sin ancla externa, un runtime comprometido
puede reescribir la cadena completa y recalcular los hashes - el encadenado solo protege contra
manipulacion que no controla el extremo de escritura. El ancla convierte la reescritura en detectable y
acota el riesgo residual a la omision de eventos dentro de la ventana entre anclas.
