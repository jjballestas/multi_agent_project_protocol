---
task_id: TASK-0295
title: "[DECISION-0104] Detector de higiene de scratch root: FLAGea (no borra) dirs de la metodologia en la raiz del disco fuera del scratch root"
type: infra
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-26
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0104, DECISION-0098, DECISION-0018, DECISION-0057]
linked_decisions: [DECISION-0104]
file: Area_comun/tasks/TASK-0295-detector-scratch-root-discipline.md
intake:
  type: infra
  goal: Implementar los teeth de deteccion de DECISION-0104 clausula 5b. El validador de estado solo ve el campo scratch_root del config (DECISION-0098 cl.3/4); NO ve la raiz real del disco, donde los agentes acumularon ~75 dirs de trabajo (~81 GB) fuera del scratch root. Esta unidad entrega un detector de higiene (script + suite) que escanea la raiz de disco(s) configurada, identifica directorios con huella de metodologia (un .git cuyo remote apunta al repo de la instancia/producto, o marcadores de arbol del protocolo) que NO viven bajo el scratch root designado, y los REPORTA como anomalia DECISION-0018 accionable al owner. NUNCA borra ni mueve nada (la limpieza es manual, autorizada por el operador, por bloques). Neutral de dominio: el scratch root y el conjunto de repos-conocidos son parametros/config, sin terminos de dominio ni nombres de marca hardcodeados.
  acceptance:
    - Un script nuevo (p.ej. scripts/scan_scratch_discipline.py) recibe el scratch root (del campo scratch_root del config si existe, o por parametro) y una o mas raices de disco a inspeccionar (por parametro; NUNCA hardcodea D:/ ni Aegis).
    - Lista los directorios de nivel superior de cada raiz que tengan huella de metodologia -- un .git con remote resoluble al repo de la instancia/hub/producto, O marcadores del arbol atestado (Area_comun/ + runtime/ + protocol.config.json) -- y que NO esten bajo el scratch root -> los reporta como anomalia DECISION-0018 (lista accionable: ruta, por que se flagea, y el recordatorio de la regla). Modo --check: exit no-cero si hay >=1 hallazgo, exit 0 si limpio.
    - NUNCA borra, mueve, ni modifica ningun directorio ni archivo (solo lee y reporta). Un test lo verifica (el arbol de fixtures queda byte-identico tras correr el detector).
    - Neutralidad: cero terminos de dominio/marca hardcodeados en el script (scan_domain_neutrality verde); el scratch root y las raices/repos-conocidos son parametros.
    - Suite de test en examples/ (patron run_*.py) que arma un directorio-raiz simulado BAJO EL SCRATCH ROOT (regla DECISION-0104: los fixtures del test viven bajo Aegis_Scratch, NUNCA en la raiz real) con: (a) un dir compliant bajo el scratch root, (b) un clon con remote-al-repo suelto en la raiz simulada, (c) un dir con marcadores de arbol suelto, (d) un dir ajeno sin huella -> asevera que flagea (b)+(c), ignora (a)+(d), y exit-code correcto en --check.
    - Gates verdes por exit code: la suite nueva, validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py.
    - El detector NO corre destructivamente sobre la maquina real en CI/test; solo deteccion, y solo sobre fixtures simulados.
  verification_cmd:
    - Suite nueva del detector en examples/ (patron run_*.py) en verde
    - python scripts/scan_scratch_discipline.py --check (sobre un fixture simulado limpio -> exit 0; sobre uno con stray -> exit no-cero)
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - scripts/scan_scratch_discipline.py
    - scripts/
    - examples/
  out_of_scope:
    - Borrar/mover/reapear cualquier directorio -- la limpieza es manual, autorizada por el operador, por bloques (LISTA-candidatos-limpieza-D-raiz.md). El detector SOLO reporta.
    - El campo scratch_root del config y su chequeo en el validador -- ya cableado por DECISION-0098 (cl.3/4); esta unidad NO lo re-implementa.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 -- FUERA (fondo intocable).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) -- FUERA.
    - Hardcodear rutas de disco, nombres de marca (Aegis) o terminos de dominio en el script neutral -- FUERA (parametros/config).
  risk: low
  estimate: M
---

# TASK-0295 - [DECISION-0104] Detector de higiene de scratch root

Origen: DECISION-0104 clausula 5b (FIRMADA por el operador 2026-07-26). La 0098 cableo el campo
`scratch_root` en config + validador (chequeo condicional del campo), pero el validador NO puede ver
la raiz real del disco -- donde se acumularon ~75 dirs de trabajo (~81 GB) fuera del scratch root
entre el 20 y el 24 de julio. Esta unidad entrega el detector que caza ese desvio: escanea la raiz
de disco(s) y FLAGea como anomalia DECISION-0018 lo que tenga huella de metodologia y no viva bajo el
scratch root. NUNCA borra (la limpieza es manual, por bloques, autorizada por el operador). Neutral:
el scratch root y las raices/repos-conocidos son parametros. Ciclo gobernado normal: maker Codex ->
recomputo del Arquitecto -> review adversarial de la Analista (clon limpio, proveedor diverso) ->
cierre.
