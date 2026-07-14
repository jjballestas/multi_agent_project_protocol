---
name: notion-spec-mirror
description: >-
  Espejo vivo SPEC/DONE -> Notion (DIRECTIVA Operador 2026-07-14): cuando el Arquitecto crea o
  actualiza una SPEC en el ledger (commit que toca Area_comun/specs/**), o cuando una tarea/SPEC
  llega a DONE (flip via submit_intent YA commiteado+pusheado), espejar/actualizar la pagina en la
  DB Notion del proyecto CON LOS PASOS DENTRO de la pagina (checklist de pasos + DoD + puertas/
  dependencias + ejecutor). UPSERT idempotente por spec_id/task_id, jamas duplicar filas. Notion =
  read-model AUDITADO del ledger #4, NUNCA fuente; disparo SOLO post-commit (espejo Notion de la
  regla de memoria dorada DECISION-0026). USAR en el gate post-commit de cada commit que toque una
  SPEC o cierre un DONE, y para aplicaciones retroactivas cuando el operador lo pida. Trigger
  words: espejo notion, spec mirror, espejar spec, notion spec, pasos dentro, upsert notion, done
  a notion, publicar spec, sincroniza notion, retroactivo specs.
---

# notion-spec-mirror -- espejo SPEC/DONE -> Notion con pasos-dentro

> Doctrina (no negociable): **Notion = read-model AUDITADO del ledger #4, NUNCA fuente.** El
> puente es `spec_id`/`task_id` VIA EL LEDGER (id en el titulo de la pagina), NO una relacion
> cross-espacio. La skill LEE del ledger y ESCRIBE en Notion, jamas al reves. Es el mecanismo
> automatizado del proyector ledger->Notion (TASK-9310) para los eventos SPEC y DONE -- no un
> canal paralelo.

## Cuando dispara (dos gatillos, SIEMPRE post-commit)

1. **SPEC creada/actualizada:** el commit (ya hecho y con gates verdes) toca
   `Area_comun/specs/SPEC-*.md` (o el specs/ de la instancia). Por cada SPEC tocada -> UPSERT de
   su pagina espejo con pasos-dentro.
2. **DONE:** un `task_status ... -> done` (o cierre de SPEC) fue aplicado via submit_intent Y
   commiteado+pusheado. -> actualizar la fila espejo: estado -> Done, marcar los checks de los
   pasos cumplidos, sellar la fecha de cierre.

**NUNCA antes del commit.** Espejar antes de que el ledger respalde la transicion = aserto sin
respaldo (mismo antipatron que el mailbox-antes-del-ledger, DECISION-0020 #3). La actualizacion
de Notion es POST-commit y NO forma parte del gate de commit (si Notion falla, el commit ya es
valido: reintentar el espejo, no revertir el ledger). Cadena por commit relevante:
`commit -> memoria (DECISION-0026) -> espejo Notion (esta skill)`.

## Procedimiento UPSERT (idempotente)

1. **Deriva la clave:** `spec_id` del filename (`SPEC-CONT-S2-...` -> `SPEC-CONT-S2`;
   `SPEC-0110-...` -> `SPEC-0110`) o `task_id` del flip.
2. **Busca la pagina existente:** `notion-search` con `data_source_url` de la DB mapeada y query
   = la clave. (El SQL `query-data-sources` del plan gratuito esta AGOTADO; usar busqueda
   semantica y verificar que el titulo del hit CONTIENE la clave exacta antes de tratarlo como
   match.)
3. **Si existe -> update** (`notion-update-page` + `insert_content`/edicion de bloques): refresca
   propiedades (Estado, fechas) y el bloque de pasos si la SPEC cambio. **Si no existe ->
   create** (`notion-create-pages` en la DB mapeada).
4. **Contenido DENTRO de la pagina** (formato de referencia: las 14 tareas de metodologia del
   14-jul):
   - `## Pasos requeridos` -- checklist (bloques to_do) con los pasos concretos de la SPEC.
   - `## DoD` -- criterios de done verificables.
   - `## Puertas / dependencias` -- gates, DECISIONs que la gatean, SPECs/tareas previas.
   - `## Ejecutor` -- maker/checker asignados (trio de la instancia).
5. **En DONE:** estado -> Done, marcar to_dos cumplidos, sellar fecha. Jamas crear duplicado: si
   la busqueda no encuentra la pagina, crearla ya en estado Done (el ledger manda).

## Mapeo de DBs (instancia hub / workspace del operador)

| Ambito | DB | page_id | data_source_id |
|---|---|---|---|
| SPECs NOVA (incl. Contabilidad) | Specs SDD (NOVA) | b362a337-8b23-4265-ace0-90c92c90c6c3 | 5da4b995-bd1b-4f15-95e6-410ac66ec66b |
| Tareas metodologia (hub) | Tareas de metodologia (METODOLOGIA) | 24166ad0-9651-4c1c-b094-a75f84ab9bf0 | 61f88150-e0be-497b-8d8d-acb4e4ae31c2 |
| Tareas NOVA | Tareas (NOVA) | c1d5476b-c951-452d-9a21-f7dc0f343e5b | 1136f0e9-c602-4b7e-a567-3ae68a5478cd |

Ruteo: SPEC-CONT-* / SPEC-NOVA-* -> Specs SDD (NOVA). SPEC-<numero> del hub y tareas TASK-* del
hub -> Tareas de metodologia. TASK-9xxx de NOVA -> Tareas (NOVA). Ante ambiguedad: la DB del
proyecto DUENO del artefacto en su ledger.

## Gotchas Notion (verificados 13/14-jul)

- Opciones de select NUEVAS: via `notion-update-data-source` (ALTER COLUMN); `create-pages` NO
  las auto-crea.
- Pasos = contenido DENTRO de la pagina (`insert_content`), no una propiedad.
- `query_data_sources` SQL agotado (plan gratuito): enumerar filas via `notion-search` con
  `data_source_url` (semantico) y confirmar match exacto por titulo.
- Fechas: propiedad tipo date (la conversion Fecha->date ya se hizo el 13-jul).

## Neutralidad / exportacion

Esta skill es GENERICA: la mecanica (dos gatillos post-commit + UPSERT + pasos-dentro) no conoce
dominio. Las DBs concretas son parametros de instancia: el master exportable vive en
`scripts/instance_assets/claude-skills/notion-spec-mirror/` con la tabla de mapeo en placeholders
`<configurar-por-instancia>`; cada instancia la llena al nacer (born-operational, DECISION-0096)
o al conectar su workspace. Si la instancia no tiene Notion conectado, la skill es no-op
declarado (no bloquea ningun gate).
