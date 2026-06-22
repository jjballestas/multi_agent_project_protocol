---
task_id: TASK-0151
title: "Proyecto-front (RF-14): carga por archivo v2 FASE B - candidatas store-no-ledger + panel de revision + GATE HUMANO DURO de PII (aprobar por candidata declarando PII revisada) + re-screen candidate->intake + estabilizar flake de timeout (AC41/AC43, SPEC-0086 ext10, DECISION-0056)"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0056, DECISION-0055, DECISION-0051]
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0151-codex-file-intake-v2-faseB.md
---

# TASK-0151 - Carga por archivo v2 FASE B (candidatas + panel + gate humano PII) (SPEC-0086 ext10, AC41/AC43; DECISION-0056)

> maker=Codex / checker=Arquitecto DESDE CLON LIMPIO + PASADA DEL ANALISTA al cierre (toca el gate de PII).
> Codigo en Zeus. OFF-by-default. Construye sobre Fase A (TASK-0150 done). Fase C (agente extractor) pendiente.

## Alcance (Fase B)
1. **Candidatas en STORE NO-LEDGER (AC41):** las candidatas viven en un store gitignored FUERA del dataset (igual
   que el raw en os-tmp), con ciclo de vida propio que NO es `task_status`; el ledger NUNCA ve `candidate`; drift 0
   con candidatas presentes; clon limpio sin el store valida exit 0.
2. **Panel de revision + GATE HUMANO DURO de PII (AC43):** el front expone, POR CANDIDATA, revisar / editar /
   aprobar / descartar. Para APROBAR, el operador DECLARA explicitamente que reviso PII (atestacion humana).
   Solo aprobadas pasan por el `requirement-intake` EXISTENTE (AC39) con RE-SCREENING de PII en la frontera
   candidate->intake (el texto EDITADO se valida por los MISMOS guards). El id/idempotency deriva del CONTENIDO
   EDITADO (no del archivo) -> 1 archivo -> N candidatas -> N REQ distintos. Atribucion relay honesto
   (author=Operador/relayed_by=Arquitecto, #4 byte-identica). Procedencia PII-free (sha256 archivo + id
   extraction-task + hash candidato pre-edicion).
3. **Estabilizar el flake de timeout (AC45 c):** los tests del flujo deterministas / no sensibles a timeout
   (sin parpadeo frio-vs-caliente).

## DoD
- AC41 + AC43 verdes con tests de COMPORTAMIENTO permanentes (candidatas no en TASK_INDEX/atestado, drift 0;
  aprobar sin declarar PII -> bloqueado; editar candidato para inyectar PII/contenido activo -> redactado/
  rechazado al aprobar; 1 archivo -> 3 candidatas -> 3 REQ ids distintos; re-aprobar = idempotente). Carry
  AC39/AC11/AC13. Flake de timeout resuelto (AC45 c).
- node --test/CI verde **EN CLON LIMPIO** (gate eol=lf); #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos
  exit 0; drift 0; neutralidad/encoding limpio.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar. Commit como
  Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Fase C: el AGENTE que efectivamente extrae candidatas (AC41 loop) + AC45 (guard a todo src/** + purga/TTL,
  prereq de C). La rama "por carga de archivo" del selector sigue GATEADA tras B+C. NO encender vivo (OFF; uso
  vivo = GO aparte del operador + Analista al cierre de C).
