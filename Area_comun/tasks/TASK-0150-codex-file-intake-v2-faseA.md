---
task_id: TASK-0150
title: "Proyecto-front (RF-14): carga por archivo v2 FASE A - plumbing determinista (upload no-MODELO-egress + screening PII real + store FUERA del dataset + emit extraction-task con contrato + selector de modo) (AC40/AC42, SPEC-0086 ext10, DECISION-0056)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0056, DECISION-0055, DECISION-0051]
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0150-codex-file-intake-v2-faseA.md
---

# TASK-0150 - Carga por archivo v2 FASE A (plumbing determinista) (SPEC-0086 ext10, AC40+AC42; DECISION-0056)

> maker=Codex / checker=Arquitecto DESDE CLON LIMPIO + PASADA DEL ANALISTA al cierre (ingest/egress/PII).
> Codigo en Zeus. OFF-by-default. Fase A NO depende del agente extractor (eso es Fase C).
> Incorpora el red-team (artefacto REDTEAM-ingestion-v2-OPCION4-veredicto.md) + decisiones D-PII/D-ACTOR.

## Alcance (Fase A)
1. **Upload gobernado server-side, NO-MODELO-EGRESS (AC40):** el server NO llama a ningun endpoint de modelo
   (sin SDK/socket/API-key de LLM). (a) screening PII REAL best-effort (email/tel/doc-cedula/NIT/razon-social/
   SQL/nombres) + ASCII, HONESTO (no garantizado); (b) guarda el archivo en STORE FUERA DEL DATASET (tmp del SO o
   area gitignored entregada con su linea .gitignore en el mismo commit + excluida del git-status del indicador),
   ruta acotada server-derived, nombre saneado, allowlist .md/.txt + limite tamano, contenido inerte; hash
   atestado = SHA-256 de BYTES CRUDOS; (c) emite extraction-task con CONTRATO autocontenido (ruta/formato/done)
   via task_upsert con status YA valido (sin kind/status nuevo). Idempotente por (sha256+project).
2. **Selector de modo (AC42):** (a) digitado (campos actuales) / (b) por carga de archivo; ambos validan
   obligatorios antes de EXECUTE (carry AC39). La rama "por carga de archivo" se GATEA detras de B+C (feature-flag
   de UI; no se ofrece vacia en Fase A) o lleva consumidor minimo no-LLM.

## DoD
- AC40 + AC42 verdes con tests de COMPORTAMIENTO permanentes (no-MODELO-egress estatico falsable + control
  positivo; store FUERA del dataset `git ls-files` vacio; SHA-256 bytes crudos; emit-task-con-contrato; idempotente;
  selector valida obligatorios; rama-archivo gateada). Carry AC37/AC38/AC39/AC13.
- node --test/CI verde **EN CLON LIMPIO** (gate eol=lf); #4 epoca 1.14.0 BYTE-IDENTICA (config/genesis/registry/
  keys sin cambio); validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
  Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance (Fases B/C)
- B: candidatas store-no-ledger + panel de revision + gate-humano-PII (AC43) + aprobar->intake.
- C: el agente que efectivamente extrae candidatas (AC41) + frontera de egress del agente.
- NO encender vivo (OFF; activacion por env; pasada del Analista + uso vivo gateado).
