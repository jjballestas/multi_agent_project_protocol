---
id: TASK-0392
title: El self-filter que la skill documenta deja un vigia MUDO en cualquier instancia donde los agentes compartan firma
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0392-el-self-filter-documentado-deja-un-vigia-mudo.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Defecto D-2 del informe de campo de NOVA, y es un defecto de la GUIA EXPORTABLE, no de una
    instancia concreta. La skill de coordinacion prescribe que el monitor de entregas filtre los
    commits propios por `Co-Authored-By: Claude (Opus|Fable|Sonnet)`. En NOVA eso NO DISCRIMINA
    NADA: medido sobre 7 commits reales, los 7 salieron clasificados como propios, incluidos los
    DOS CHANGE-REQUIRED del checker. Motivo: todos los commits de la instancia -- Arquitecto, Codex
    y Analista -- llevan `author=Codex` y la misma firma de modelo, porque el checker corre el CLI
    de Anthropic con `--model opus`. El campo `%an` tampoco separa. Un monitor armado SIGUIENDO LA
    DOCUMENTACION no avisa de ninguna entrega, y su silencio se lee como "los peones trabajan": es
    la familia de silencio-no-es-exito, agravada porque el vigia PARECE bien armado. En el hub el
    filtro funciona hoy por accidente -- los commits de Codex no llevan el trailer de Claude -- y esa
    coincidencia es justo lo que oculta el defecto al exportarlo. Hermana de TASK-0386 (la identidad
    de git no distingue a los agentes) y de TASK-0383.
  acceptance:
    - "AC1 (la senal primaria no depende de la identidad git): el monitor detecta una entrega por el
      MAILBOX -- un `MSG-<fecha>-<emisor>-<destino>-*.md` lleva el emisor en el NOMBRE del fichero --
      y no por el autor ni la firma del commit. Se acredita con una entrega de peon cuyo commit es
      indistinguible del propio: el monitor avisa igual."
    - "AC2 (el self-filter va por marca propia): el descarte de los commits del coordinador se hace
      por una marca que SOLO el coordinador escribe, no por el modelo del proveedor. Se acredita
      mostrando que un commit de peon con la misma firma de modelo NO se descarta."
    - "AC3 (el filtro se comprueba antes de confiar en el): se entrega un procedimiento EJECUTADO que
      pasa el filtro por dos commits propios y dos de un peon y exige que los separe. Es lo que NOVA
      pide explicitamente: hoy nada obliga a validar el vigia antes de fiarse de su silencio."
    - "AC4 (la guia exportable queda corregida): el texto que se instancia en cada proyecto nuevo ya
      no prescribe el filtro por modelo. Se acredita con el diff de la guia, no con una nota."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - skills
    - scripts/harness/README.md
  out_of_scope:
    - "La identidad de los agentes en el gate de claim de producto: eso es TASK-0386. Aqui se arregla
      el VIGIA, alli la AUTORIZACION."
    - "El monitor de la sesion interactiva del Arquitecto del hub, que se corrige en su skill
      directamente. Esta tarea entrega la version EXPORTABLE."
  risk: medium
  estimate: S
---

# TASK-0392 -- el vigia que parece armado

## Lo medido en NOVA

    7 commits reales, filtro `Co-Authored-By: Claude (Opus|Fable|Sonnet)`
    -> 7 de 7 clasificados como PROPIOS
    -> incluidos los DOS CHANGE-REQUIRED del checker

## Por que el hub no lo vio

Porque aqui funciona por casualidad: los commits de Codex no llevan el trailer de Claude, asi que el
filtro separa. En cuanto una instancia corre su checker con un CLI de Anthropic -- que es la
configuracion recomendada por DECISION-0101 para tener diversidad de proveedor -- la coincidencia
desaparece y el filtro deja de discriminar.

**El defecto estaba en la guia desde el principio; el hub solo no lo notaba.** Es exactamente la
razon por la que un informe de campo de una instancia real vale mas que una revision del hub sobre
si mismo.

## Maker evidence

- The exportable watchdog now treats the mailbox filename as the primary delivery signal.
- Commit context is filtered only by an exact coordinator-only `Protocol-Monitor-Origin` value.
- The executable proof creates two coordinator and two worker commits with identical Git author
  and provider/model trailer, then requires a 2/2 split and a worker mailbox alert.
- Executed command: `python scripts/harness/test_session_watchdog_filter.py --scratch-root
  D:/Aegis_Scratch/multi_agent_project_protocol/task0392-filter-proof`.
