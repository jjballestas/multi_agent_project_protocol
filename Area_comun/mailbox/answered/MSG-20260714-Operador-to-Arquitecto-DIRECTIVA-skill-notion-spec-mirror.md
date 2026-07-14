---
message_id: MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-skill-notion-spec-mirror
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - "Notion DB 'Specs SDD' (NOVA): b362a337-8b23-4265-ace0-90c92c90c6c3 / ds 5da4b995-bd1b-4f15-95e6-410ac66ec66b"
  - "Notion DB 'Tareas de metodologia' (METODOLOGIA): 24166ad0-9651-4c1c-b094-a75f84ab9bf0 / ds 61f88150-e0be-497b-8d8d-acb4e4ae31c2"
  - "Notion DB 'Tareas' (NOVA): c1d5476b-c951-452d-9a21-f7dc0f343e5b / ds 1136f0e9-c602-4b7e-a567-3ae68a5478cd"
  - "Proyector ledger->Notion = TASK-9310 (Aegis)"
  - DECISION-0026 (golden memory rule; espejo: actualizar Notion tras el commit)
one_line_summary: "Crear una SKILL que MANTENGA Notion como espejo vivo del ledger: cuando se crea/actualiza una SPEC, la espeja en Notion CON LOS PASOS DENTRO (checklist + DoD + puertas/deps + ejecutor, el formato que ya te gusto de las 14 tareas); cuando se da DONE, actualiza la fila (estado + checks). Aplica a Contabilidad y a TODO lo que se publique en Notion, no solo al probe."
requested_action: "Crea la skill (dispara en tus gates de creacion-de-SPEC y de DONE). Diseno abajo. Respeta la doctrina Notion=read-model del ledger (puente=task_id, no relacion cross-espacio) y dispara SOLO tras sellar/commitear la transicion. Entrega la skill + confirma que aplica retroactivo a las SPECs de Contabilidad ya existentes."
question: "Confirmas el diseno de la skill (o propones ajuste) y la dejas viva en tus gates SPEC/DONE?"
---

# DIRECTIVA - Skill: espejo SPEC/DONE -> Notion con pasos-dentro

## Motivacion (lo que me gusto)
Tu trabajo de Notion de hoy dejo las tareas **NO como texto plano**: al hacer click se ven los PASOS
(checklist + DoD + dependencias/puertas + ejecutor). Eso es lo correcto y quiero que sea SISTEMATICO,
no manual: cada vez que se crea una SPEC o se da un DONE, Notion se actualiza solo, con ese formato.
Aplica a **Contabilidad y a todo lo que se publique en Notion**, no solo al probe de memoria.

## Que debe hacer la skill (dos disparadores)
1. **Al crear/actualizar una SPEC** (evento de tu loop del ledger): ESPEJAR la SPEC en la DB Notion que
   corresponda (Specs SDD en NOVA; o la DB de tareas/specs del proyecto), creando/actualizando la pagina
   con un bloque **"## Pasos requeridos" DENTRO de la pagina**: checklist de pasos a realizar + DoD +
   dependencias/puertas + ejecutor. Mismo formato que las 14 tareas de metodologia que ya poblaste.
2. **Al dar DONE** (flip de estado via submit_intent, ya commiteado): ACTUALIZAR la fila espejo -- estado
   -> Done, marcar los checks de los pasos cumplidos, sellar la fecha. No crear duplicado: hace UPSERT.

## Reglas duras (no negociables, de la doctrina ya documentada)
- **Notion = read-model AUDITADO del ledger #4, NUNCA fuente.** El puente es **task_id / spec_id via el
  ledger**, NO una relacion cross-espacio. La skill LEE del ledger y ESCRIBE en Notion, jamas al reves.
- **Dispara SOLO despues de sellar/commitear** la transicion (SPEC registrada / DONE flipeado + push).
  Espejar antes de que el ledger lo respalde = aserto sin respaldo (mismo antipatron que escribir el
  mailbox antes de que el ledger lo backee). Es el espejo Notion de la regla de memoria dorada (0026).
- **Idempotente:** match por task_id/spec_id; re-correr actualiza en sitio, nunca duplica filas.
- **Consistente con el proyector TASK-9310** (ledger->Notion): la skill es el mecanismo automatizado de
  ese proyector para SPEC/DONE, no un canal paralelo. Si ya hay solape, unificalo, no lo dupliques.
- **Neutralidad:** la skill es generica (cualquier proyecto/instancia); las llaves/DBs concretas se
  parametrizan (config de la instancia). Exportable en la capa skills/ neutral al instanciar.

## IDs Notion utiles (de mi workspace, para que no los redescubras)
- Specs SDD (NOVA): page `b362a337-8b23-4265-ace0-90c92c90c6c3` / ds `5da4b995-bd1b-4f15-95e6-410ac66ec66b`
- Tareas de metodologia (METODOLOGIA): page `24166ad0-9651-4c1c-b094-a75f84ab9bf0` / ds
  `61f88150-e0be-497b-8d8d-acb4e4ae31c2` (ya tiene el formato pasos-dentro de referencia)
- Tareas (NOVA): page `c1d5476b-c951-452d-9a21-f7dc0f343e5b` / ds `1136f0e9-c602-4b7e-a567-3ae68a5478cd`
- Nota: el SQL query_data_sources del plan gratuito esta AGOTADO; para enumerar filas usa notion-search
  con data_source_url (semantico). create/update/update-data-source SI funcionan.

## Alcance de la entrega
- La skill viva en tus gates SPEC/DONE + su documentacion.
- Aplicacion **retroactiva a las SPECs de Contabilidad ya existentes** (espejarlas con pasos-dentro una vez).
- Si el disparo automatico al DONE necesita cablearse en tu gate de submit_intent, declaralo; no rompas
  el gate de commit por esto (la actualizacion de Notion es post-commit, no pre-commit).

## Frontera
No toca #4 ni el estudio medido. Notion es aguas abajo del ledger; la skill nunca lo invierte.
