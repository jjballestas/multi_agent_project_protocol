---
task_id: TASK-0315
file: Area_comun/tasks/TASK-0315-higiene-corpus-h1-h3.md
title: "Higiene de corpus H1/H3: de-duplicar 3 mensajes presentes a la vez en answered/ y archived/, y restaurar 7 bytes de control incrustados en 3 archivos"
status: done
type: triage
owner: Arquitecto
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - SPEC-MEMORIA-HIBRIDA
  - TASK-0314
  - DECISION-0018
created_at: 2026-08-06
intake:
  type: infra
  goal: >
    Remediar los defectos de corpus H1 y H3 que el indexador de la memoria hibrida caza
    (SPEC-MEMORIA-HIBRIDA s.16.4). H1: tres mensajes existen fisicamente a la vez en
    Area_comun/mailbox/answered/ y en Area_comun/mailbox/archived/; el par difiere SOLO en el campo
    status del frontmatter (cuerpo identico), y la copia de archived/ es en los tres casos el estado
    posterior. Eso aborta el build del corpus completo por duplicate artifact_id. H3: tres archivos
    contienen bytes de CONTROL reales (0x00, 0x1f, 0x7f) donde el autor escribia el TEXTO de escape
    de una clase de regex documentada; el byte real vuelve el archivo binario para grep y contamina
    cualquier pack que lo inline. H2 NO entra: el analisis mostro que no es defecto de corpus sino
    calibracion del indexador (ver notes).
  acceptance:
    - "AC1 (H1 de-duplicacion): las 3 copias stale de Area_comun/mailbox/answered/ quedan borradas; la copia de archived/ permanece INTACTA (mismo blob, sin re-escribir). Cero pares duplicados entre answered/ y archived/ en todo el mailbox."
    - "AC2 (H1 canonicidad justificada): para MSG-20260628-Arquitecto-to-Analista-REPASS2-TASK-0208 la copia de archived/ esta respaldada por el evento mailbox_archive seq 2558 del ledger (from open to archived); para las otras dos no existe evento de archivado en el ledger y la copia de archived/ es la creada mas tarde en git. En NINGUN caso se emite una transicion nueva de mailbox: es de-duplicacion fisica, no cambio de estado."
    - "AC3 (H3 restauracion de intencion): los 7 bytes de control reales se sustituyen por su TEXTO de escape (0x00 -> \\x00, 0x1f -> \\x1f, 0x7f -> \\x7f), preservando el sentido de la clase de regex documentada. Ningun otro byte del archivo cambia."
    - "AC4 (procedencia no rota): verificado que ninguno de los archivos editados esta pineado por blob ni por sha256 en atestacion, reporte o evento alguno (0 citas). El fondo intocable no se toca."
    - "AC5 (gates): validate_collaboration_state.py, scan_encoding.py y check_commit_trailers exit 0 en clon limpio tras la remediacion; cero bytes de control (0x00/0x1f/0x7f) en Area_comun/ y personal/Arquitecto/."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - Area_comun/mailbox/answered/
    - Area_comun/artifacts/ANALISTA-REQ-31100EAF-ingestion-veredicto.md
    - Area_comun/mailbox/archived/MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0166-fix.md
    - personal/Arquitecto/MEMORY.md
  out_of_scope: >
    H2 (frontmatter con valor centinela none/null, con RUTA en vez de id, o con lista por coma en
    campo escalar): 206 artefactos historicos afectados. NO se reescriben -- el analisis mostro que
    son CONVENCIONES del corpus, no defectos, y reescribir historia gobernada para complacer a un
    indice es invertir la relacion. La correccion va en el indexador (enmienda P12b/P12c del
    contrato de port, SPEC s.16.3). Tampoco se toca la copia de archived/ de los pares H1, ni el
    ledger, ni el fondo intocable (config 2E35F26E, epoch 1.14.0, dataset N=500).
  risk: low
  estimate: S
notes: >
  Los defectos los descubrio el indexador de la memoria hibrida al correr contra el corpus real del
  hub durante el analisis de viabilidad de TASK-0314 (SPEC s.16.2): el indexador funciona ademas
  como LINTER del corpus, y H1 lo hace fallar CERRADO, que es el comportamiento correcto.
  Sobre H2, el desglose medido es: 98 casos de centinela (spec_id/task_id con valor `none`, una
  convencion de declaracion-de-ausencia extendida por handoffs y tasks), 106 casos de RUTA en un
  campo de id (convencion temprana anterior a los ids, p.ej. `spec_id: Area_comun/specs/SPEC-0039-
  ....md`) y 2 casos de lista por coma en campo escalar. Reescribir 206 artefactos gobernados
  historicos cambiaria sus blobs sin ganancia y es exactamente lo contrario de lo que corresponde:
  el indice debe modelar el corpus. Se enmienda el contrato del port en su lugar.
