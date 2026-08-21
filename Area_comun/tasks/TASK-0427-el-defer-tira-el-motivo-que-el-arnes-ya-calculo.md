---
id: TASK-0427
title: El defer de la sonda de residuo tira el motivo exacto que el arnes ya calculo
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0427-el-defer-tira-el-motivo-que-el-arnes-ya-calculo.md
created: 2026-08-22
reviewer: Analista
intake:
  type: fix
  goal: >
    La sonda de residuo produce un motivo EXACTO: devuelve objetos con reason "drain_timeout"
    (scripts/harness/peer_mailbox_cron.ps1:805) y "malformed_status" (:864, :868). El llamante lo
    descarta: cuando el estado resuelve a "unknown", registra el defer con la constante
    Register-PreExecDefer -Reason "residue_probe_failed" (:1529). Con esa constante, "la sonda no
    pudo decidir" queda indistinguible de "hay residuo en el arbol", que son diagnosticos opuestos:
    el primero es un fallo del instrumento y el segundo un estado legitimo del arbol que exige
    esperar. La instancia NOVA reporta ocho aplazamientos sin causa probada por esta razon.
  acceptance:
    - "AC1: el defer registra el motivo REAL producido por la sonda (drain_timeout,
      malformed_status y los demas que existan), no una constante. Acreditar los motivos uno por
      uno, forzando cada rama."
    - "AC2: un motivo no contemplado NO se pierde ni se inventa: se propaga tal cual con una marca
      de desconocido. Acreditar con un motivo nuevo inyectado en banco."
    - "AC3: la distincion es OBSERVABLE donde se diagnostica -- log del cron y retry.json --, no
      solo en el interior de la funcion. El criterio es que un tercero pueda separar fallo de
      instrumento de residuo real leyendo unicamente lo que el arnes deja escrito."
    - "AC4: no cambia la DECISION de aplazar. Se aplaza igual y en los mismos casos; lo que cambia
      es que la causa sobrevive al viaje."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/
  out_of_scope:
    - "NO se cambia el presupuesto ni el tope de los defers: eso es TASK-0387."
    - "NO se cambia el criterio de residuo. Solo se conserva el motivo."
  risk: low
  estimate: S
---

# TASK-0427 -- el motivo existe, viaja y se tira en la ultima linea

    :805    return [pscustomobject]@{ ok = $false; raw = ""; reason = "drain_timeout" }
    :864    ... reason = "malformed_status"
    :868    ... reason = "malformed_status"
    :1529   Register-PreExecDefer -Message $Message -Reason "residue_probe_failed"

El arnes calcula la causa con precision y la sustituye por una etiqueta generica en el punto exacto
en que alguien la va a leer. El coste no es teorico: sin ese dato, un instrumento roto y un arbol
sucio producen el mismo aplazamiento, y el que diagnostica no tiene como separarlos.
