---
task_id: TASK-0148
title: "Proyecto-front (RF-14): carga de requerimiento por archivo (ingestion gobernada acotada, OFF-by-default) - allowlist tipo/tamano + nombre saneado + contenido inerte + PII/ASCII + idempotente; anti-abuso (AC37/AC38, DECISION-0055)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
linked_decisions: [DECISION-0055, DECISION-0051]
created_at: 2026-06-21
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0148-codex-front-file-ingestion.md
---

# TASK-0148 - Carga de requerimiento por archivo (SPEC-0086 ext8, AC37/AC38; DECISION-0055)

> maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (ingestion/egress) antes de cerrar. Codigo en Zeus
> (server+front). #9 (ULTIMO) del PLAN. OFF BY DEFAULT; uso vivo = pre-auth condicionada del operador (entrega+
> cierre + Analista OK + activacion runtime). carry AC11/AC13/AC17/AC19/AC22.

## Origen
REQ-31100EAF: adjuntar un archivo en el Intake y que su contenido alimente un requerimiento gobernado que
aterriza en canonico con id+seq reales (mismo camino que el intake actual), sin transcribir a mano.

## Alcance
1. **Server (Zeus):** ingestion server-side: allowlist tipo (.md/.txt), limite de tamano (<= N KB), nombre
   saneado (sin path traversal), contenido INERTE (nunca ejecutado); PII structural + ASCII al texto extraido;
   alimenta el MISMO requirement-intake (task_upsert type=requirement, author/relayed_by provistos por el caller).
   Idempotente (mismo archivo = mismo id-hash). Solo execute escribe.
2. **Front:** adjuntar archivo -> preview redactado (dry_run) -> execute con confirmacion -> resultado con id+seq
   o error (no verde) si falla. Con capacidad OFF (default), adjuntar archivo no esta disponible / flujo no cambia.
3. **Config OFF-by-default** en registro FUERA del config pinned (flag enabled + limites). Default disabled.

## DoD
- AC37 (ingestion gobernada acotada idempotente/honesta; HEAD valida exit 0) + AC38 (anti-abuso permanente: tipo/
  tamano/traversal/contenido-activo/inyeccion -> rechazados; sin egress; #4 byte-identica) verdes como tests de
  COMPORTAMIENTO. Carry AC11/AC13/AC17/AC19/AC22.
- Camino feliz con capacidad ON contra clon de PRUEBA: archivo .md valido -> requirement real id+seq; HEAD valida
  exit 0. Negativos rechazados antes de tocar el intake. Idempotencia.
- #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0; node --test/CI verde; npm start
  ejecutable; neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. PASADA DEL ANALISTA (ingestion/
  egress) ANTES de cerrar. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Encender el uso VIVO (queda OFF; la pre-auth condicionada del operador aplica al cierre solo si Analista OK +
  activacion runtime). NO commitear el flag enabled:true en el versionado (patron DECISION-0054).
- Ejecutar contenido del archivo / egress / escribir fuera del camino gobernado.
