---
task_id: TASK-0149
title: "Proyecto-front (RF-14): Intake honesto - rechazar requerimientos fantasma desde placeholder/vacio + exigir proyecto destino explicito (no default a Zeus-protocol) (AC39, SPEC-0086 ext9)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0051, DECISION-0052]
created_at: 2026-06-21
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0149-codex-intake-no-phantom.md
---

# TASK-0149 - Intake honesto: no fantasmas + proyecto explicito (SPEC-0086 ext9, AC39; REQ-643B160A)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. Remedia el defecto del fantasma REQ-984A85C6 (cancelado).
> carry AC11/AC14/AC22. Tightening de validacion del execute ya gobernado (no abre superficie de escritura).

## Origen
REQ-643B160A: el Intake persistio texto de ejemplo/placeholder como requerimiento real (REQ-984A85C6, narrativa
e intencion de aceptacion vacias, proyecto defaulteado a Zeus-protocol). El operador no lo escribio.

## Alcance
1. **Server-side:** el EXECUTE del intake RECHAZA (sin preview-as-green) si narrativa o intencion de aceptacion
   estan VACIAS o IGUALES al placeholder/ejemplo conocido. Validacion en el server, no solo en el cliente.
2. **Proyecto explicito:** el EXECUTE exige proyecto destino elegido por el operador; NO defaultea a Zeus-protocol
   (ni a ninguno). Sin proyecto explicito -> rechazo.
3. **Front:** refleja el error real (no verde) cuando el execute rechaza; el wizard no permite avanzar con
   campos placeholder/vacios.

## DoD
- AC39 verde con test de COMPORTAMIENTO permanente (narrativa/aceptacion vacias o == placeholder -> RECHAZADO,
  no se crea REQ, no verde; proyecto no elegido -> RECHAZADO; contenido real + proyecto explicito -> requirement
  real id+seq). Carry AC11/AC14/AC22.
- node --test/CI verde **en CLON LIMPIO** (gate eol=lf, reproducir clonando, no in-place); #4 byte-identica;
  validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Cambiar la superficie de escritura del intake (sigue el mismo execute gobernado; esto es tightening de su
  validacion). No tocar la ingestion por archivo (TASK-0148, ya done).
