---
id: TASK-0373
title: F2 de la memoria hibrida -- formato de stub y manifiesto, goldens, y la propuesta de enfriado en seco que nunca ha corrido
status: in_review
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0373-f2-stubs-manifiestos-y-propuesta-de-enfriado-en-seco.md
created: 2026-08-13
reviewer: Analista
intake:
  type: feature
  goal: >
    Fase F2 de SPEC-MEMORIA-HIBRIDA, que hoy NO existe ni en borrador. La instancia tiene el plano
    caliente y su indice derivado -- 4717 artefactos, 2447 aristas, packs de revival que comprimen
    1,5 MB a 115 KB --, pero la mitad que da nombre a la memoria "hibrida" esta vacia: medido sobre
    la DB viva, `cold_packs`=0, `stubs`=0, `hot_cold_rules`=0, y el fichero canonico
    `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json` no existe. No hay `Area_comun/archive/`. El
    camino que mueve historia no ha corrido NUNCA: su unico ejercicio han sido los mutantes del
    checker en la review formal. F2 construye ese camino en SECO -- formato de stub y de manifiesto,
    goldens estables, y `--propose-cold` como dry-run -- sin mover ni un fichero de sitio. Mover es
    F3 y exige la DECISION de activacion, que el operador ya pre-aprobo pero que se emite cuando F2
    este acreditada, no antes.
  acceptance:
    - "AC1 (el manifiesto reconstruye la tabla 1:1): `pack.manifest.json` lleva por artefacto todos
      los campos que `cold_packs` necesita -- artifact_id, original_path, cold_path, sha256,
      git_commit_at_freeze, artifact_type, status, closed_at -- y `manifest-index.json` los suyos.
      Se acredita reconstruyendo la tabla DESDE los manifiestos y comparandola con la que el motor
      produciria: es el requisito del round-trip de la s.6, el gap que mato a Engram. Una cabecera
      que no reconstruye no acredita."
    - "AC2 (la REGLA DE ORO anti-B1, verificada por conducta): todo artefacto referenciado por `file`
      o `deliverables` del indice fusionado lleva `requires_stub=1` OBLIGATORIO, y el stub se
      materializa EN LA RUTA ORIGINAL EXACTA conservando en su frontmatter el status espejo y el
      puntero verificable (cold_path + sha256 + rehydration_command). Se acredita en seco sobre
      fixture: simular el enfriado de una tarea done referenciada y comprobar que
      `validate_collaboration_state` sigue VERDE porque el puntero del indice resuelve a un fichero
      real. Un stub que deje el puntero colgando es el BLOCKER que la review adversarial ya cazo una
      vez."
    - "AC3 (`--propose-cold` es dry-run de verdad): lista candidatos segun las reglas HABILITADAS del
      fichero canonico, excluye rutas bajo claim activo, y NO escribe nada. Se acredita corriendolo
      con el arbol sucio a proposito y comprobando por `git status --porcelain` que no toco un solo
      byte, mas su exit code. Un dry-run que escriba algo no es un dry-run."
    - "AC4 (la seleccion se DERIVA de las reglas, no se cablea): el conjunto propuesto sale de
      evaluar `MEMORY_HOT_COLD_RULES.json` sobre el indice. Se acredita cambiando UNA regla del
      fichero y observando que el conjunto propuesto cambia en consecuencia. Si la propuesta no se
      mueve al mover la regla, la regla es decorativa."
    - "AC5 (goldens estables y discriminantes): existen goldens del stub y del manifiesto que fallan
      si el formato cambia. Se acreditan por el PAR: mutar un campo del formato pone rojo, y el
      formato correcto pasa. Un golden que pase con el campo mutado no es un golden."
    - "AC6 (cero movimiento): esta tarea NO mueve ningun artefacto ni crea `Area_comun/archive/` con
      contenido real. Se acredita con `git status` y con el conteo de `cold_packs` en la DB, que
      sigue en 0. Mover es F3."
  verification_cmd:
    - "python scripts/memory/build_memory_db.py --propose-cold --root ."
    - "python scripts/memory/check_memory_db_drift.py --root . --fast"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/memory/test_memory_db.py"
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/query_memory_db.py
    - Area_comun/protocol/MEMORY_HOT_COLD_RULES.json
    - scripts/memory/test_memory_db.py
  out_of_scope:
    - "Mover historia de verdad, crear packs con contenido y la DECISION de activacion: es F3. Esta
      tarea deja el camino construido y probado en seco, no lo recorre."
    - "El mapeo de estado de politica por literal (`status == \"active\"`): es TASK-0368 y es
      PRECONDICION de F3, no de F2. Con 105 de 109 politicas vistas como historicas, encender el
      enfriado archivaria justo lo vigente."
    - "Las tres divergencias del texto de la s.7: TASK-0369."
    - "El validador archive-aware: la s.5.3 lo declara tarea F3+ separada con su propia DECISION, y
      NO precondicion del piloto. La regla del stub-espejo existe precisamente para no necesitarlo."
    - "Las 215 aristas `implements` que no resuelven destino y el banco de 72 tests que nace rojo:
      TASK-0371 y su hermana; no se arreglan de paso aqui."
  risk: medium
  estimate: L
---

# TASK-0373 -- F2: construir el camino frio sin recorrerlo

## Lo que hay hoy, medido

    artifacts          4717        cold_packs            0
    artifact_versions  4717        stubs                 0
    search_terms      22927        hot_cold_rules        0
    artifact_edges     2447        task_context_cache    0
    agent_memory        746        retrieval_log         0
    policy_status       109        embeddings            0

Diez tablas con datos, seis a cero. Las seis a cero son exactamente las de F2 y F3. El fichero
canonico de reglas no existe y no hay `Area_comun/archive/`.

## Por que en SECO

Porque mover historia es irreversible en la practica y porque la review adversarial de esta SPEC ya
encontro una vez el modo de romperlo: un `git mv` que deja colgando un puntero del indice fusionado
pone ROJO el validador canonico. La regla de oro anti-B1 (s.5.3) existe por eso, y su sitio de
prueba es una fixture, no el corpus real.

F2 termina cuando el camino esta construido y **probado sobre fixture**, con los goldens que
detectan un cambio de formato y un `--propose-cold` que no escribe nada. F3 lo recorre.

## La precondicion que NO es de esta tarea pero manda en el orden

`policy_status` da hoy **4 active / 105 historical**, y entre las 105 estan DECISION-0026, 0020,
0038 y 0104 -- las que AGENTS.md cita como vinculantes. **F3 no se puede encender en ese estado**:
marcaria como archivable justo la politica en vigor, y el gate callaria. Esa puerta es TASK-0368.

F2 se puede construir en paralelo; F3 no arranca hasta que 0368 cierre.

## Implementation evidence (Codex, 2026-08-15)

- `MEMORY_HOT_COLD_RULES.json` declares the enabled dry-run rule. The live proposal evaluates
  that file and reports 272 candidates; changing its selector from `status=done` to
  `status=blocked` changes the fixture proposal from one candidate to zero.
- `--propose-cold` reads the derived index, merged task indexes, canonical rules, and active
  claims. The fixture proves that an active file-scoped claim removes the candidate and that
  repository porcelain is byte-for-byte unchanged by the command.
- Stub rendering is LF/ASCII byte-stable, keeps the mirrored status and verifiable cold pointer,
  and is materialized at the exact indexed task path in the acceptance fixture. The canonical
  collaboration validator exits 0 on that fixture.
- Pack and manifest-index rendering require every specified field, sort deterministically, and
  are covered by exact goldens plus field mutations. Loading the generated pack manifest
  reconstructs the expected `cold_packs` row 1:1.
- The complete memory suite passes 78/78. The live proposal exits 0. The DB still contains zero
  `cold_packs`; no archive directory or cold artifact was created.

## Remediation r1 evidence (Codex, 2026-08-15)

- Task stubs now require the original bytes and preserve the complete literal `intake` block. A
  canonical TASK-0350 fixture (above the TASK-0238 exemption boundary) remains validator-green
  after replacement; a zero-byte replacement fails the same test.
- The literal rehydration command includes `--requested-by Codex` and is executed end to end by
  the permanent F2 suite against a built fixture database.
- Pack-manifest and manifest-index tests compare production bytes with independent literal ASCII
  goldens. They bind indentation, key sorting, root names, and every required field.
- A rule fixture sets `requires_stub: false` for an indexed task and still requires a stub. Removing
  the production forcing clause makes this negative fail.

## Remediation r2 evidence (Codex, 2026-08-15)

- Stub rendering now applies the canonical intake frontier: a numbered task above TASK-0238 must
  preserve intake, while exempt legacy tasks and non-numbered task artifacts may omit it. The live
  dry-run and renderer now agree: 273 candidates, 273 rendered, zero failures.
- The permanent boundary negative accepts TASK-0238 without intake and rejects TASK-0239 without
  intake. A separate negative rejects an empty requester.
- Rehydration shell arguments use `shlex.quote`; the executable test traverses every identity
  declared by the fixture instead of choosing one whitespace-free identity.
- Pack-manifest tests remove every required header and artifact field one at a time and require
  production to fail closed.
