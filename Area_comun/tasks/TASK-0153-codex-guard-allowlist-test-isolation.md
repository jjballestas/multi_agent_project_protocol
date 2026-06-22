---
task_id: TASK-0153
title: "Proyecto-front: endurecer guard de egress a ALLOWLIST deny-all + marcar eval/new Function (AC46) + AISLAMIENTO de la suite del entorno de runtime del operador (AC47) -- precondicion del uso vivo del extractor (SPEC-0086, DECISION-0056)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0056]
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
---

# TASK-0153 - Guard ALLOWLIST (AC46) + aislamiento de test (AC47); precondicion del uso vivo

> GO del operador (MSG GO-GUARD-ALLOWLIST-PRE-USOVIVO). Cierra el residual que el Analista declaro en el cierre de
> Fase C. **NO enciende el uso vivo del extractor** (eso es un GO aparte y posterior). maker=Codex /
> checker=Arquitecto + PASADA DEL ANALISTA. OFF-by-default intacto.

## Alcance
1. **AC46 - Flip del guard a ALLOWLIST deny-all + ejecucion dinamica:**
   - El scan estatico sobre TODO `src/**` marca CUALQUIER `import`/`require` cuyo modulo NO este en una **lista
     permitida explicita** (deny-by-default), no solo proveedores/clientes nombrados. Cierra el residual (clientes
     HTTP no listados phin/needle/bent/ky/...).
   - Marca tambien `eval(` y `new Function(` (ofuscacion / ejecucion dinamica).
   - Unico egress permitido = `git push` gobernado + lecturas read-only ya allowlisted.
   - Control positivo POR familia: cliente HTTP no listado -> FLAGGED; `eval(`/`new Function(` -> FLAGGED; import
     permitido (fs/path/...) -> `[]`; git push gobernado -> `[]`. El src real da `[]` (sin falso positivo).
2. **AC47 - Aislamiento de la suite del entorno de runtime del operador:**
   - `npm test` limpia/sobrescribe al arrancar `AUTO_COMMIT_PUSH_CONFIG_PATH`, `FILE_INGESTION_CONFIG_PATH` (y
     cualquier env que altere off-by-default) con fixtures propias -> resultado determinista independiente del shell.
   - Test falsable: con esos env apuntando a configs "ON", la suite sigue verde (off-by-default 403, executes 200)
     porque los aisla.

## DoD
- AC46 + AC47 verdes (controles positivos por familia; suite determinista aunque el shell tenga env de runtime ON).
- Carry AC40/AC41/AC43/AC44/AC45 + vectores ya verdes intactos. Cambio acotado (guard/test + harness); core/config/
  genesis/registry/keys SIN tocar.
- node --test/CI verde EN CLON LIMPIO; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad+
  encoding 0.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
- **NO enciende el uso vivo del extractor** (sigue OFF-by-default, env-gated). El GO de uso vivo es aparte y posterior.

## Prereq
Fase C (TASK-0152) cerrada (hecho). GO del operador (hecho).
