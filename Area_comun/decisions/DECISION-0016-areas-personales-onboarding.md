---
decision_id: DECISION-0016
title: Areas personales bajo personal/<id>/ + regla de onboarding (cada participante crea la suya al darse de alta)
status: accepted
date: 2026-06-06
ratified_at: 2026-06-06
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0015, DECISION-0007, DECISION-0011, DECISION-0001]
phase: P2
---

# DECISION-0016 - Areas personales bajo personal/<id>/ + regla de onboarding

> Estado: ACCEPTED (2026-06-06, aprobada por el operador). Cambio de estructura del protocolo, aditivo y
> con reubicacion (git mv, historia preservada). SemVer MINOR (DECISION-0001).

## Contexto
Al arrancar el proyecto, cada agente recibio un area personal top-level (`Claude/`, `Codex/`). Con el
modelo N-agente (DECISION-0015: roster por capacidades, N agentes + humanos), ir sumando carpetas en la
raiz no escala ni queda limpio. El area personal es el correlato fisico de cada entrada del
`agent_registry`/`agents`.

## Decision
1. **Regla de onboarding (metodologia):** todo participante (agente o humano) que se da de alta en el
   proyecto **crea su area personal en `personal/<id>/`**, donde `<id>` es su identificador en
   `agent_registry`/`agents`. Los borradores y notas privadas viven ahi. Sigue aplicando "claim activo
   antes de tocar rutas compartidas" (DECISION-0007); el area personal propia no requiere claim salvo que
   otra ruta compartida la cubra.
2. **Reubicacion:** las areas existentes pasan a `personal/`: `Claude/` -> `personal/Claude/`,
   `Codex/` -> `personal/Codex/` (via `git mv`, sin perder historia). La raiz queda limpia.
3. **Config:** `domain_neutrality.exempt_globs` reemplaza `"Claude/**"`,`"Codex/**"` por un unico
   `"personal/**"` (cubre todos los participantes presentes y futuros).
4. **Scaffolding:** `scripts/new_instance.py` crea `personal/<id>/` para cada participante declarado al
   instanciar (architect/implementer/human_owner y, en general, cada id del roster).

## Versionado y neutralidad (DECISION-0001)
Aditivo + reubicacion, backward-compatible para el comportamiento (validadores leen globs de config; no se
toca codigo de validacion). **MINOR.** Neutral de dominio: `personal/` es estructura de proceso, sin
terminos de negocio. Instancias existentes adoptan via su propia decision (el protocolo no se autopropaga).

## Consecuencias
- **Positivas:** raiz limpia; escala a N participantes; onboarding explicito y uniforme; un solo glob de
  exencion; alineado con el registry de capacidades (DECISION-0015).
- **Costo:** una reubicacion unica + actualizar docs/plantillas/scaffolding; las instancias que adopten
  deben mover sus areas (git mv) y actualizar su exempt_globs.

## Alternativas consideradas
- **Mantener `Claude/`,`Codex/` top-level:** descartada; no escala y ensucia la raiz con N agentes.
- **Nombre `Personal_Area/` (propuesta inicial del operador):** se opto por `personal/` (neutral, en
  ingles, consistente con los templates en ingles).
