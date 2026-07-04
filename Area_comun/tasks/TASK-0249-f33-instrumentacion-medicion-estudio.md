---
task_id: TASK-0249
title: "[VISION-NOVA][F3.3] Instrumentacion del estudio: motor de medicion automatizado (cost.attributed + defect.reported + manual.intervention + study_metrics.py)"
type: feature
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-04
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, DECISION-0091, DECISION-0033]
linked_decisions: [DECISION-0091, DECISION-0033]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0249-f33-instrumentacion-medicion-estudio.md
intake:
  type: feature
  goal: Automatizar la captura de medicion del estudio NOVA (hoy 100% manual) con 3 eventos applied:false (cost.attributed automatico via err.log, defect.reported validado contra schema_defectos v1.0, manual.intervention como overhead-fijo) + un motor determinista study_metrics.py que computa Q1-Q5 del plan de analisis sellado en DECISION-0091, para que el dev medido P2 sea el primer brazo instrumentado.
  acceptance:
    - cost.attributed reusa SPEC-0079/DECISION-0033, escribe tokens_total_atribuibles == cumulativo del err.log, idempotente por tarea_id, degradacion por-cubeta a NA verificada (no inventa split).
    - defect.reported valida contra schema_defectos.json v1.0; rechaza malformados a rejected (nunca escribe fila invalida); paridad_detector particiona confirmatorio vs descriptivo.
    - manual.intervention produce fila OVERHEAD-FIJO con tag_incidente_maquinaria; test que asierta que ninguna tarea de producto recibe tokens de un incidente.
    - study_metrics.py determinista (now parametrizado, sin Date.now()/random) con golden que ejercita Q1 (con/sin overhead, regimen/arranque), Q2 (solo paridad_detector=true + Plan B efecto-techo), Q3 (guard duro, se niega a emitir p-value/IC/regresion), Q4 (esqueleto pre-ventana + subpotenciado declarado), Q5 (descriptivo).
    - Los 3 eventos son applied:false (no pasan por submit_intent, no tocan el escritor unico/enforce/authoritative); off-by-default deja el event log byte-equivalente.
    - Gates verdes en clon limpio (validate/encoding/domain_neutrality); drift 0; protocol.config.json byte-identico; epoch pineado intacto.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - personal/Arquitecto/TFM-medicion/
    - Area_comun/specs/nova/SPEC-NOVA-F3.3-instrumentacion-medicion.md
  out_of_scope:
    - NO toca protocol.config.json ni el epoch pineado (1.14.0 byte-identico).
    - NO re-congela schema_medicion.json/schema_defectos.json v1.0 (los consume tal cual).
    - NO toca codigo de dominio Nova-Budget (.NET/React); es instrumentacion del lado-estudio, no producto.
    - NO ejecuta peones/subagents (F6, DECISION-0078); solo mide orchestration_mode como dimension.
  risk: medium
  estimate: M
---

# TASK-0249 - [VISION-NOVA][F3.3] Instrumentacion del estudio (motor de medicion automatizado)

Owner: Codex (implementa) + Analista (gate FORMAL, checker-only) + Arquitecto (checker de neutralidad y
alcance).

## Contexto (DIRECTIVA operador cola-F3.3-lista-no-idle, item Q1 CRITICAL-PATH)
El sello Etapa 1 (DECISION-0091) congelo el schema y el plan de analisis, pero la captura de medicion
sigue siendo manual (`medicion_ledger.py`). F3.3 automatiza la captura ANTES de que abra el dev medido
P2.1/P2.2 (ventana baseline 3-25-jul), para que P2 corra ya instrumentado en vez de reconstruido a mano.
SPEC completa: `Area_comun/specs/nova/SPEC-NOVA-F3.3-instrumentacion-medicion.md` (formalizada por el
Arquitecto desde el draft de diseno del Asesor).

## Alcance
3 eventos `applied:false` + 1 motor determinista, en la capa de instrumentacion de la INSTANCIA del
estudio (Python, fuera del core neutral y fuera del stack .NET/React de Nova-Budget). Ver la SPEC para
el contrato de aceptacion completo (s.7) y la traza a las preguntas Q1-Q5 del sello (s.4 de la SPEC).

## DoD (testable)
Ver bloque intake (acceptance) + contrato de aceptacion s.3/s.7 de la SPEC. Cierre: gate FORMAL del
Analista (NO informal; es infraestructura gobernada, no unidad de contraste baseline) + gates del hub
verdes + atestacion sha256 de la SPEC.
