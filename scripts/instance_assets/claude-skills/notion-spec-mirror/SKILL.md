---
name: notion-spec-mirror
description: >-
  Espejo vivo SPEC/DONE -> Notion: cuando el Arquitecto de la instancia crea o actualiza una SPEC
  en el ledger (commit que toca el specs/ gobernado), o cuando una tarea/SPEC llega a DONE (flip
  via submit_intent YA commiteado+pusheado), espejar/actualizar la pagina en la DB Notion del
  proyecto CON LOS PASOS DENTRO de la pagina (checklist de pasos + DoD + puertas/dependencias +
  ejecutor). UPSERT idempotente por spec_id/task_id, jamas duplicar filas. Notion = read-model
  AUDITADO del ledger, NUNCA fuente; disparo SOLO post-commit. USAR en el gate post-commit de cada
  commit que toque una SPEC o cierre un DONE. Si la instancia no tiene Notion conectado, no-op
  declarado. Trigger words: espejo notion, spec mirror, espejar spec, notion spec, pasos dentro,
  upsert notion, done a notion, publicar spec, sincroniza notion.
---

# notion-spec-mirror -- espejo SPEC/DONE -> Notion con pasos-dentro

> Doctrina (no negociable): **Notion = read-model AUDITADO del ledger, NUNCA fuente.** El puente
> es `spec_id`/`task_id` VIA EL LEDGER (id en el titulo de la pagina), NO una relacion
> cross-espacio. La skill LEE del ledger y ESCRIBE en Notion, jamas al reves. Si la instancia
> tiene un proyector ledger->Notion propio, esta skill es su mecanismo para SPEC/DONE, no un
> canal paralelo.

## Cuando dispara (dos gatillos, SIEMPRE post-commit)

1. **SPEC creada/actualizada:** el commit (ya hecho y con gates verdes) toca una SPEC del specs/
   gobernado de la instancia. Por cada SPEC tocada -> UPSERT de su pagina espejo con
   pasos-dentro.
2. **DONE:** un `task_status ... -> done` (o cierre de SPEC) fue aplicado via submit_intent Y
   commiteado+pusheado. -> actualizar la fila espejo: estado -> Done, marcar los checks de los
   pasos cumplidos, sellar la fecha de cierre.

**NUNCA antes del commit.** Espejar antes de que el ledger respalde la transicion = aserto sin
respaldo (antipatron mailbox-antes-del-ledger). La actualizacion de Notion es POST-commit y NO
forma parte del gate de commit (si Notion falla, el commit ya es valido: reintentar el espejo,
no revertir el ledger). Cadena por commit relevante:
`commit -> memoria persistente -> espejo Notion (esta skill)`.

## Procedimiento UPSERT (idempotente)

1. **Deriva la clave:** `spec_id` del filename o `task_id` del flip.
2. **Busca la pagina existente:** busqueda en la data source mapeada con query = la clave;
   verificar que el titulo del hit CONTIENE la clave exacta antes de tratarlo como match.
3. **Si existe -> update** (propiedades + refrescar el bloque de pasos si la SPEC cambio).
   **Si no existe -> create** en la DB mapeada.
4. **Contenido DENTRO de la pagina:**
   - `## Pasos requeridos` -- checklist (bloques to_do) con los pasos concretos de la SPEC.
   - `## DoD` -- criterios de done verificables.
   - `## Puertas / dependencias` -- gates, DECISIONs que la gatean, SPECs/tareas previas.
   - `## Ejecutor` -- maker/checker asignados (trio de la instancia).
5. **En DONE:** estado -> Done, marcar to_dos cumplidos, sellar fecha. Jamas crear duplicado: si
   la busqueda no encuentra la pagina, crearla ya en estado Done (el ledger manda).

## Mapeo de DBs (parametros de instancia -- LLENAR AL ADOPTAR)

| Ambito | DB | page_id | data_source_id |
|---|---|---|---|
| SPECs del proyecto | <configurar-por-instancia> | <configurar-por-instancia> | <configurar-por-instancia> |
| Tareas del proyecto | <configurar-por-instancia> | <configurar-por-instancia> | <configurar-por-instancia> |

Ruteo ante ambiguedad: la DB del proyecto DUENO del artefacto en su ledger.

## Gotchas Notion

- Opciones de select NUEVAS: via update-data-source (ALTER COLUMN); create-pages NO las
  auto-crea.
- Pasos = contenido DENTRO de la pagina (insert content), no una propiedad.
- Si el SQL de query de data sources no esta disponible (plan gratuito agotado): enumerar via
  busqueda semantica con data_source_url y confirmar match exacto por titulo.

## Neutralidad

La mecanica (dos gatillos post-commit + UPSERT + pasos-dentro) no conoce dominio. Las DBs
concretas son parametros de la instancia; esta skill master se exporta con placeholders y cada
instancia la llena al nacer o al conectar su workspace.
