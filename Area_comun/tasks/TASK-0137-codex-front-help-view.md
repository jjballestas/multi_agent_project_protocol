---
task_id: TASK-0137
title: "Proyecto-front - vista Help (RF-14/UX): guia navegable de metodologia y consola, fuente unica docs/MANUAL-operador.md, read-only y honesta (no documenta lo inexistente)"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
linked_decisions: [DECISION-0051]
created_at: 2026-06-20
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0137-codex-front-help-view.md
---

# TASK-0137 - Vista Help (manual de metodologia + consola), read-only (SPEC-0086 ext4, AC23)

> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. Ratificado por el Operador
> (REQ-FB27AF72 -> ext4 SPEC-0086, AC23). UX READ-ONLY: sin nueva superficie de escritura.
> carry AC11/AC12/AC13/AC17.

## Origen
REQ-FB27AF72 (semilla del operador via intake). TITULO de la semilla MANGLEADO ("arrancamos con nova.budget:")
por el bug de campos-stale que arreglo TASK-0135; el intent REAL se re-derivo de la NARRATIVA: un item Help en
la nav que muestra ayuda detallada de la metodologia y la consola, para operar sin conocimiento previo.

## Alcance
1. Nav item **Help** + panel; "help" entra en NAV_VIEWS (routing 1:1, AC12). Activar Help -> solo su panel;
   vista desconocida -> fallback.
2. Guia DETALLADA y NAVEGABLE (secciones + indice/glosario): consola; observar vs operar; submit_intent
   escritor-unico; dry_run vs execute/confirmacion; atestacion #4; las vistas; intake RF-14; pipeline SDD;
   glosario.
3. Fuente UNICA = docs/MANUAL-operador.md (reusar, NO duplicar). Implementacion a eleccion de Codex (servir el
   manual read-only y renderizarlo, o incluirlo en build desde ese unico archivo); sin segunda copia divergente.
4. Honestidad (AC11): refleja lo que la app HACE hoy incl. limitaciones; lo no implementado se marca
   pendiente/fuera-de-alcance.
5. Read-only: sin botones de accion, sin llamadas a submit; conforme al design-system (AC13).

## DoD
- AC23 verde con tests de COMPORTAMIENTO permanentes: routing "help" (solo su panel; fallback); contenido
  derivado de docs/MANUAL-operador.md (no placeholder; cubre secciones clave/glosario); no-bypass (sin
  superficie de escritura en el panel). Carry AC11/AC12/AC13/AC17 verdes.
- node --test/CI verde; npm start ejecutable; Help navegable en vivo.
- validate exit 0 con/sin secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 BYTE-IDENTICA;
  neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Cualquier cambio de superficie de escritura (vista 100% read-only).
- Duplicar/editar el contenido del manual; documentar features inexistentes (PROHIBIDO por AC11).
