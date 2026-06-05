---
decision_id: DECISION-0001
title: Política de versionado (SemVer) del protocolo + CHANGELOG + protocol_version
status: accepted
date: 2026-06-05
deciders: [Claude (architect), operador humano]
supersedes: []
superseded_by: []
relates_to: [TASK-0003, TASK-0001]
phase: P0
---

# DECISION-0001 — Versionado del protocolo (SemVer), CHANGELOG y `protocol_version`

## Contexto

El protocolo ya tiene una versión publicada (`v0.1.0`, tag de git) pero no existía una política
escrita de cómo evoluciona. Las instancias (p.ej. `bot_spot_ai_strategy_pack`) necesitan poder
decir **"sigo el protocolo vX.Y.Z"** y rastrear qué cambió entre versiones. Como el protocolo es
un conjunto de **archivos** (Markdown + JSON + validador + plantillas), "cambio incompatible" no
es tan obvio como en una librería: hay que definirlo con ejemplos concretos.

## Decisión

Adoptamos **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`) interpretado para un protocolo de
archivos, un `CHANGELOG.md` en formato *Keep a Changelog*, un mecanismo explícito para que cada
instancia declare la versión que sigue, y un procedimiento de publicación de releases.

### 1. Qué versiona SemVer aquí

La versión describe **el protocolo en sí** (su estructura, ciclo de vida, campos obligatorios,
plantillas y validador), **no** el contenido de negocio de ninguna instancia.

| Incremento | Cuándo | Ejemplos concretos en este protocolo |
|------------|--------|--------------------------------------|
| **MAJOR** (`X.0.0`) | Cambio **incompatible**: una instancia válida con la versión anterior podría dejar de validar o de poder operarse sin migración. | Renombrar/eliminar carpetas de `Area_comun/`; cambiar el ciclo de vida de tareas (estados o transiciones); **añadir o renombrar un campo obligatorio** en `state/*.json`, claims, mailbox o handoffs; cambiar reglas que el validador exige (romper paridad de comportamiento); cambios incompatibles en el formato de los `*.template.*`; eliminar un comando/flag del validador. |
| **MINOR** (`0.Y.0`) | Nueva **capacidad compatible** hacia atrás: lo anterior sigue siendo válido. | Nuevas plantillas; **nuevos campos opcionales** (p.ej. `protocol_version`, `adopted_profiles`); validadores adicionales o nuevos chequeos que solo emiten *warnings*; **perfiles/extensiones** nuevos; nuevos ejemplos de instancia; nuevos documentos de protocolo opcionales. |
| **PATCH** (`0.0.Z`) | Corrección sin cambiar el contrato. | Fixes de redacción/typos; aclaraciones de documentación; correcciones de bugs del validador que **no** cambian qué se considera válido; reordenar/formatear sin cambio semántico. |

Regla de desempate: **ante la duda entre MINOR y MAJOR, gana MAJOR.** Si un cambio *podría*
romper una instancia existente, se trata como incompatible.

Pre-1.0.0 (estado actual): seguimos la convención SemVer de que la API puede cambiar; aun así
documentamos los breaking en MAJOR-intención y los anunciamos en el CHANGELOG. La estabilización
formal del contrato se marca con `v1.0.0` (requiere aprobación humana, ver §4).

### 2. Cómo una instancia declara `protocol_version`

Cada instancia declara la versión del protocolo que sigue en **`protocol.config.json`**, con un
campo de primer nivel:

```json
{
  "schema_version": "1.0",
  "protocol_version": "0.2.0",
  "project_name": "mi_proyecto",
  "...": "..."
}
```

- `protocol_version` es un string SemVer (`MAJOR.MINOR.PATCH`) que apunta a una versión publicada
  del protocolo (las del `CHANGELOG.md` / tags `vX.Y.Z`).
- Es un campo **opcional y aditivo** (su introducción es, por tanto, un cambio MINOR). El validador
  no lo exige todavía; cuando una instancia lo omite, se asume "sin declarar".
- La compatibilidad se lee por MAJOR: una instancia que declara `0.2.0` es compatible con el
  protocolo mientras el MAJOR no cambie. Un salto de MAJOR obliga a la instancia a migrar y a
  re-declarar `protocol_version`.
- En este repo (dogfooding), `protocol.config.json` declara la versión del protocolo que esta
  propia instancia implementa.

### 3. Cómo se publican las releases

1. Acumular cambios bajo `## [Unreleased]` en `CHANGELOG.md` a medida que se hacen.
2. Al cerrar la versión: mover lo de *Unreleased* a una sección `## [X.Y.Z] — YYYY-MM-DD`.
3. Actualizar `PROJECT_STATE.json` (`version`, `released_versions`) y la línea
   *"Released version"* de `AGENTS.md`.
4. Asegurar el **quality gate**: validador verde (`.ps1` y `.py`) sobre la raíz y
   `examples/minimal_instance/`, y barrido de neutralidad de dominio limpio.
5. Commit de release y **tag anotado** `vX.Y.Z` en git. El tag es la fuente de verdad de "qué se
   publicó".
6. Las instancias que quieran adoptar la nueva versión lo hacen **por decisión propia** (el
   protocolo no se propaga solo); registran el cambio de `protocol_version` en su instancia.

### 4. Aprobación humana

Coherente con `AGENTS.md` §5 y §4:

- **MAJOR** (cambio incompatible) y **cualquier `v1.0.0`+**: requieren **aprobación humana
  explícita** registrada (decisión y/o ratificación del operador humano) antes del tag.
- **MINOR / PATCH**: los publica el arquitecto siguiendo §3, sin aprobación humana obligatoria,
  pero siempre con validador verde y CHANGELOG actualizado.

## Consecuencias

- **Positivas:** trazabilidad de cambios; las instancias pueden fijar y comprobar compatibilidad;
  criterio objetivo (con ejemplos) para clasificar cambios; releases reproducibles.
- **Costo:** disciplina de mantener el CHANGELOG y de clasificar cada cambio; añade un campo
  opcional al config (impacto en TASK-0004, scaffolding, que debe poblarlo).
- **Seguimiento:** TASK-0004 (Codex) debe rellenar `protocol_version` al instanciar. La adopción
  de perfiles (DECISION-0002) usará la misma mecánica de versión MINOR.

## Alternativas consideradas

- **CalVer (versionado por fecha):** descartado; no comunica compatibilidad, que es justo lo que
  las instancias necesitan saber.
- **Sin versión formal (solo git tags):** insuficiente; no define qué es breaking ni cómo lo
  declara una instancia.
