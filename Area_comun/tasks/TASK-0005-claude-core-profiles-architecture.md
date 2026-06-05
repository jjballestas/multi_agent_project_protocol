---
id: TASK-0005
owner: Claude
status: done
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0003, TASK-0006, TASK-0007]
phase: P1
review: Done por Claude (arquitecto). Estructura profiles/ + PROFILE_TEMPLATE (manifest neutral) + doc de arquitectura de 3 capas. Contrato profile.manifest definido; registro de adopcion via adopted_profiles/decision documentado. Core neutral (barrido limpio). Desbloquea TASK-0006/0007 (handoff a Codex). No se toco README_INSTANCIACION.md (claim activo de Codex/TASK-0004).
---

# TASK-0005 — Arquitectura core/profiles/examples del protocolo

## objetivo
Materializar la decisión [DECISION-0002](../decisions/DECISION-0002-core-perfiles-profesionales.md):
definir la estructura física y el contrato de los **perfiles profesionales** sin contaminar el
core neutral. Deja la base sobre la que se construye `dotnet_enterprise` (TASK-0006) y el soporte
de estado/validador (TASK-0007).

## entradas
- DECISION-0002 (capas core / profiles / examples; neutralidad innegociable del core).
- DECISION-0001 (introducir un perfil es un cambio MINOR aditivo).
- Repo de referencia `D:\Agentes\entorno_open_cloude` (insumo SOLO para TASK-0006, no para el core).

## archivos_relevantes
- crea: `profiles/README.md` (qué es un perfil, qué puede y qué no puede añadir).
- crea: `profiles/PROFILE_TEMPLATE/` con `profile.manifest.template.json` y estructura mínima de
  un perfil (docs/, templates/, README).
- crea: `Area_comun/artifacts/ARQUITECTURA-core-profiles.md` (diagrama de capas + reglas de
  composición e instanciación core / core+perfiles).
- edita: `README.md` y `README_INSTANCIACION.md` (sección "instanciar con perfiles").

## entregables
- Contrato del manifiesto de perfil (`profile.manifest`): id, versión del perfil,
  `requires_protocol_version` (rango SemVer), stack declarado, qué artefactos aporta, fronteras
  que el perfil añade.
- Plantilla de perfil reutilizable y documentación de la arquitectura de 3 capas.

## definition_of_done
- [x] El **core sigue neutral**: ningún término de stack/negocio entra en archivos del núcleo ni
      en `*.template.*` del core (barrido de neutralidad limpio; el `profile.manifest.template.json`
      solo contiene placeholders).
- [x] Existe `profiles/` con README y `PROFILE_TEMPLATE/` (manifest + README + docs/templates/prompts).
- [x] Documentado cómo un proyecto instancia core o core + N perfiles, y cómo registra la
      adopción (`adopted_profiles` en `PROJECT_STATE.json` y/o decisión de la instancia) —
      ver `profiles/README.md` §4-§5 y `ARQUITECTURA-core-profiles.md`.
- [x] Coherente con DECISION-0001 (perfil = MINOR) y DECISION-0002.
- [x] Handoff a Codex para TASK-0006 y TASK-0007.

## riesgos
- Fuga de dominio al core: el manifiesto y los docs de `profiles/README.md` deben dejar explícito
  el límite (lo específico vive en el perfil, nunca en el núcleo).

## preguntas_abiertas
- ¿`adopted_profiles` en `PROJECT_STATE.json` (recomendado, máquina-legible) y/o decisión de la
  instancia? Proponer en el handoff; decidir junto a TASK-0007.
