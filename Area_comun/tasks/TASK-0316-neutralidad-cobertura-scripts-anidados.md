---
task_id: TASK-0316
file: Area_comun/tasks/TASK-0316-neutralidad-cobertura-scripts-anidados.md
title: "Ceguera del gate de neutralidad de dominio: scan_globs no cruza subdirectorios, asi que scripts/memory/** y los JSON de Area_comun/protocol/ nunca se escanean"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0314
  - SPEC-MEMORIA-HIBRIDA
  - DECISION-0002
created_at: 2026-08-06
intake:
  type: infra
  goal: >
    Cerrar un hueco REAL del gate que sostiene la frontera dura del proyecto (neutralidad de
    dominio, AGENTS.md s.4 / CLAUDE.md regla 1). `protocol.config.json.domain_neutrality.scan_globs`
    declara `scripts/*.py` y `scripts/*.ps1`, y `glob_to_regex` mapea `*` a `[^/]*`, que NO cruza
    barra. Consecuencia: todo script en un SUBDIRECTORIO de scripts/ queda invisible al escaner.
    Hoy eso son las 3863 lineas de `scripts/memory/**` recien portadas; manana, cualquier paquete
    nuevo. Ademas `Area_comun/protocol/*.md` no cubre los `.json` de esa carpeta, asi que
    `MEMORY_INDEX_POLICY.json` -- el archivo cuyo proposito ES declarar terminos de dominio por
    instancia -- tampoco se escanea. El gate sale exit 0 y esa luz verde es CIERTA pero VACIA para
    la superficie entregada.
  acceptance:
    - "AC1 (falsacion antes del fix): se planta un termino de dominio en scripts/memory/*.py y en Area_comun/protocol/MEMORY_INDEX_POLICY.json sobre un arbol de scratch y se demuestra que scan_domain_neutrality.py sale exit 0 (ciego). Es la evidencia de partida, no una suposicion."
    - "AC2 (cobertura): tras el fix, el mismo plantado hace salir el escaner exit != 0, y la lista de archivos escaneados incluye los 6 de scripts/memory/ y el policy JSON. Conteo antes/despues declarado (hoy: 179 archivos, 0 del motor)."
    - "AC3 (sin re-genesis): el fix NO modifica protocol.config.json. El config esta pineado por el hash del genesis (chain.genesis liga canonical_hash del config), asi que ampliar scan_globs ahi exigiria una ceremonia de re-genesis. El fix va en el CODIGO del escaner, con el mismo patron de auto-append que ya aplica a connectors/** y skills/**."
    - "AC4 (sin falsos positivos): validate_collaboration_state.py, scan_encoding.py y el propio scan_domain_neutrality.py salen exit 0 sobre el arbol real tras el fix; ningun archivo legitimo del repo pasa a fallar."
    - "AC5 (regresion): test que planta un termino de dominio en un script anidado y exige exit != 0, para que la ceguera no pueda volver en silencio."
    - "AC6 (exencion de artefactos generados): runtime/memory/ queda EXENTO del escaner de neutralidad. Hoy scan_globs incluye runtime/** y exempt_globs trae runtime/state/** pero NO runtime/memory/, mientras revive_pack.py se niega a escribir fuera de runtime/memory/ (guard explicito) y los packs inlinean corpus gobernado por diseno: usar la herramienta como esta disenada deja el gate en ROJO hasta borrar el pack. Reproducido en vivo el 2026-08-06. La exencion va por la misma via de codigo que AC3 (sin tocar el config pineado), y con test que demuestre que un pack generado ya no ensucia el gate."
  verification_cmd:
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/scan_domain_neutrality.py
    - scripts/scan_domain_neutrality.ps1
    - scripts/test_scan_domain_neutrality.py
  out_of_scope: >
    Modificar protocol.config.json o cualquier clave pineada por el genesis; re-genesis; el lazo de
    remediacion de TASK-0314 (F1/F2/F3/R4, que son del maker); los residuales R1-R3 del veredicto.
  risk: medium
  estimate: S
notes: >
  GO del operador 2026-08-06. Owner reasignado a Codex (implementador) con el Analista de
  checker: el Arquitecto redacto el contrato y los AC, asi que no debe ademas codificarlo y
  auto-certificarlo. La responsabilidad arquitectonica del hallazgo sigue siendo del Arquitecto.
  Hallazgo F4 del veredicto del Analista sobre TASK-0314
  (Area_comun/artifacts/Analista-TASK-0314-port-memoria-hibrida-verdict.md), falsificado por el
  checker plantando terminos de dominio y verificado INDEPENDIENTEMENTE por el Arquitecto:
  `iter_scanned_files` selecciona 179 archivos y NINGUNO bajo scripts/memory/;
  `glob_to_regex("scripts/*.py")` produce `^scripts/[^/]*\.py$`, que no matchea
  `scripts/memory/build_memory_db.py`. Explicitamente NO imputable al maker de TASK-0314: el
  out_of_scope de esa tarea le prohibia tocar protocol.config.json y el escaner no estaba en sus
  scope_routes. Mientras esto siga abierto, el AC1 de TASK-0314 no debe declararse "verificado por
  gate": la neutralidad del motor la sostiene hoy un unico test unitario con tres terminos legacy
  escritos a mano sobre un solo modulo, que es util pero no es una frontera mecanica.
