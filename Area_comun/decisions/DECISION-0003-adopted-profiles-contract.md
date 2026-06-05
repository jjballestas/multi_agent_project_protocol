---
decision_id: DECISION-0003
title: Contrato de adopted_profiles y convención de decisión de adopción de perfiles
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [Claude (architect), operador humano]
supersedes: []
superseded_by: []
relates_to: [TASK-0007, TASK-0006, TASK-0005, DECISION-0001, DECISION-0002]
phase: P1
---

# DECISION-0003 — Contrato de `adopted_profiles` y decisión de adopción

> **Estado: ACEPTADA (ratificada 2026-06-05).** Es la especificación autoritativa de **TASK-0007**
> (soporte de perfiles en estado y validador). Cierra la pregunta abierta de DECISION-0002/TASK-0005
> (¿`adopted_profiles` por campo, por decisión, o ambos? → **ambos**). TASK-0007 debe implementar
> contra esta especificación; cualquier desviación necesaria se registra como decisión de
> seguimiento, no se improvisa.
>
> **Enmienda 2026-06-05 (no sustantiva):** §1 precisa el formato de `profile_id` como
> `^[a-z0-9][a-z0-9_-]*$` (minúsculas con dígitos, `-` o `_`) en vez de "kebab_case", para admitir
> el id canónico `dotnet_enterprise`. Detectado por Codex en TASK-0007; no cambia el contrato, solo
> el wording. El validador (`.py`/`.ps1`) ya implementa este patrón.

## Contexto

DECISION-0002 fijó la arquitectura core/profiles/examples y dijo que cada instancia registra los
perfiles que adopta en `adopted_profiles` (estado) y/o en una decisión propia. TASK-0006 ya
demostró una forma concreta en `examples/dotnet_enterprise_instance/`
(`adopted_profiles: [{profile_id, profile_version, adopted_at}]` + una decisión de instancia).
TASK-0007 necesita una **especificación autoritativa** para validar esto de forma aditiva y con
paridad `.py` ↔ `.ps1`. Este borrador la fija.

## Decisión (propuesta)

### 1. Campo `adopted_profiles` (nivel instancia)

- **Ubicación:** `Area_comun/state/PROJECT_STATE.json`, campo de primer nivel.
- **Opcional y aditivo** (cambio MINOR por DECISION-0001). Si está ausente o vacío, la instancia
  es una instancia **solo-core** y se comporta exactamente como hoy.
- **Tipo:** array de objetos. Esquema por entrada:

  | Campo | Req. | Tipo | Regla |
  |-------|------|------|-------|
  | `profile_id` | sí | string | id en minúsculas con letras, dígitos, guion (`-`) o guion bajo (`_`); patrón `^[a-z0-9][a-z0-9_-]*$`. Coincide con `profiles/<profile_id>/` y con `profile.manifest.json.profile_id`. (p.ej. `dotnet_enterprise`). |
  | `profile_version` | sí | string | SemVer exacto del perfil adoptado (pin); coincide con `profile.manifest.json.profile_version`. |
  | `adopted_at` | sí | string | Fecha ISO `YYYY-MM-DD`. |
  | `decision_ref` | reco. | string | Ruta a la decisión de instancia que justifica la adopción (ver §2). |
  | `notes` | no | string | Texto libre. |

  ```json
  "adopted_profiles": [
    {
      "profile_id": "dotnet_enterprise",
      "profile_version": "0.1.0",
      "adopted_at": "2026-06-05",
      "decision_ref": "Area_comun/decisions/DECISION-0001-adopt-dotnet-enterprise.md"
    }
  ]
  ```

- **Unicidad:** un mismo `profile_id` no puede aparecer dos veces (un perfil, una versión activa).
- **Dependencias:** si el manifiesto del perfil declara `depends_on_profiles`, cada dependencia
  debe estar también en `adopted_profiles`.

### 2. Decisión de adopción por instancia (convención)

- Adoptar un perfil **por primera vez** requiere **ambas** cosas (no "o lo uno o lo otro"):
  1. una entrada en `adopted_profiles`, y
  2. una decisión de instancia `Area_comun/decisions/DECISION-XXXX-adopt-<profile_id>.md`.
- Las instancias **numeran sus propias decisiones** (su `DECISION-0001` es independiente de las de
  este repo). El ejemplo `examples/dotnet_enterprise_instance/` usa `DECISION-0001-adopt-dotnet-enterprise.md`.
- Subir de versión un perfil ya adoptado: actualizar `profile_version`/`adopted_at` en el campo y
  registrar una decisión de seguimiento si el cambio del perfil es MAJOR o toca fronteras/gates.
- Plantilla copiable de la decisión de adopción → Apéndice A.

### 3. Especificación para el validador (TASK-0007, aditivo)

Comportamiento esperado de `validate_collaboration_state.{py,ps1}`:

1. **Sin `adopted_profiles`** (ausente o `[]`): **comportamiento idéntico al actual**. Cero nuevos
   chequeos. (Compatibilidad hacia atrás obligatoria.)
2. **Con `adopted_profiles`**, por cada entrada:
   - **ERROR** si falta `profile_id`, `profile_version` o `adopted_at`, o si `profile_version`/
     `adopted_at` no tienen formato válido (SemVer / `YYYY-MM-DD`).
   - **ERROR** si hay `profile_id` duplicado.
   - Si el perfil **está presente** en la instancia (`profiles/<profile_id>/profile.manifest.json`
     existe):
     - **ERROR** si `manifest.profile_id != profile_id`.
     - **ERROR** si `manifest.profile_version != profile_version` (la adopción debe fijar una
       versión real del perfil).
     - **ERROR** si el `protocol_version` de la instancia **no satisface**
       `manifest.requires_protocol_version`.
     - **ERROR** si alguna entrada de `manifest.depends_on_profiles` no está en `adopted_profiles`.
   - Si el perfil **no está presente** (adopción solo por referencia): **WARNING** "no verificable
     localmente" (no error).
   - Si `decision_ref` está presente: **WARNING** si el archivo referenciado no existe (no error).
3. **Rango `requires_protocol_version`:** soportar el subconjunto SemVer simple usado por los
   perfiles: exacto (`"0.2.0"`) y rango con límites (`">=0.2.0 <1.0.0"`, `">=0.2.0"`). Documentar
   el subconjunto soportado; cualquier rango no parseable → **WARNING** (no error).
4. **Paridad:** mismos resultados en `.py` y `.ps1`; añadir **golden tests** positivos y negativos
   (instancia con perfil válido, versión desajustada, protocolo incompatible, dependencia ausente,
   `profile_id` duplicado, perfil solo-referenciado).
5. **Plantilla de estado:** añadir `adopted_profiles` (vacío) a
   `Area_comun/state/PROJECT_STATE.template.json` como campo opcional documentado.

### 4. Errores vs warnings (resumen de criterio)

- **ERROR** (rompe el validador): inconsistencias verificables localmente que invalidan la
  adopción (campos faltantes/mal formados, mismatch de id/versión, protocolo incompatible,
  dependencia ausente, duplicado).
- **WARNING** (no rompe): lo no verificable localmente (perfil solo referenciado, `decision_ref`
  ausente en disco, rango SemVer no parseable).

## Consecuencias

- TASK-0007 tiene una spec concreta y verificable, manteniendo compatibilidad hacia atrás.
- La adopción de perfiles queda trazable (campo máquina-legible + decisión humana).
- Coherente con DECISION-0001 (aditivo = MINOR; entra en v0.3.0) y DECISION-0002 (core neutral).

## Pregunta cerrada

DECISION-0002/TASK-0005 dejó abierto si `adopted_profiles` se declara por campo, por decisión o
ambos. **Resolución propuesta: ambos** para la primera adopción (campo + decisión de instancia).

## Alternativas consideradas

- **Solo campo (sin decisión):** descartado; pierde la justificación/aprobación humana de adoptar
  un perfil que añade fronteras y gates.
- **Solo decisión (sin campo):** descartado; no es máquina-legible y el validador no podría
  verificar compatibilidad.
- **Hacer los chequeos obligatorios siempre:** descartado; convertiría el validador en incompatible
  para instancias solo-core (sería MAJOR). Los chequeos solo aplican si hay `adopted_profiles`.

## Apéndice A — Plantilla de decisión de adopción (para instancias)

```markdown
---
decision_id: DECISION-XXXX
title: Adopt <profile_id> profile
status: accepted
date: YYYY-MM-DD
deciders: [<architect>, <implementer>, <human_owner>]
relates_to: []
---

# DECISION-XXXX — Adopt `<profile_id>`

## Context
Por qué este proyecto adopta el perfil y en qué contexto.

## Decision
Adoptar `profiles/<profile_id>` versión `<profile_version>` sobre el protocolo `<protocol_version>`.

## Consequences
- La instancia sigue siendo una instancia válida del core.
- Las fronteras, gates y puntos de aprobación del perfil aplican a este proyecto.
- Lo específico del stack vive solo en el perfil/instancia; el core sigue neutral.
- Los secretos reales quedan fuera del repo (solo placeholders en archivos versionados).
```
