# DRAFT TASK-0266 (ejecutar cuando cierre la re-entrega de 0257: ventana limpia)

Lote a ejecutar en orden:
1. Amendar DECISION-0103 .md: seccion E4/E5 (texto del MSG del Operador, firma =
   MSG-20260719-Operador-to-Arquitecto-ENMIENDA-E4-E5-adoptable-githooks).
2. Crear Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
   (contenido abajo).
3. Ledger: claim CLAIM-arq-e4e5-20260719 (fragmentos 0266 + decision .md + self) ->
   task_upsert 0266 -> task_status proposed->ready -> release.
4. RESP al Operador (unidad hermana registrada, fila de tabla para C1) + rutear
   re-juicio 0257 al Analista + commitear REPORTE-fixloop pendiente. Push. Monitor.

## Intake propuesto para el .md

- task_id: TASK-0266 | type: infra | owner: Codex | reviewer: Analista | priority: normal
- title: "[DECISION-0103][C5/E4-E5] Propagacion del harness: .githooks/** adoptable en
  upgrade_instance + cableado core.hooksPath en new_instance"
- goal: Cerrar el hueco de propagacion de C5 (enmiendas E4/E5): .githooks/** entra al
  conjunto adoptable de upgrade_instance.py (DEFAULT_ADOPTABLE_GLOBS o bloque
  upgrade.adoptable_globs del config, lo mas limpio) para que las instancias EXISTENTES
  (NOVA incluida) reciban el hook por upgrade; y new_instance.py CABLEA core.hooksPath
  al instanciar (copiar el hook sin armar el path lo deja muerto).
- acceptance:
  - upgrade_instance.py contra una instancia real (sandbox) reporta el delta de
    .githooks/ como adoptable (E4).
  - Instancia nueva en sandbox: git config core.hooksPath devuelve la ruta SIN paso
    manual y una prueba negativa aborta el commit (E5).
  - Instancia EXISTENTE upgradeada en sandbox: hook presente y armable con la
    instruccion documentada; validate de la instancia verde.
  - Cero cambios al comportamiento del hook en si (eso es 0257); solo propagacion.
  - Neutralidad + validate + encoding verdes.
- verification_cmd: upgrade_instance.py dry-run/delta en sandbox; new_instance a
  temporal + git config core.hooksPath + prueba negativa; validate; scans.
- scope_routes: scripts/upgrade_instance.py, scripts/new_instance.py,
  protocol.config.template.json (si el bloque upgrade resulta lo mas limpio),
  README_INSTANCIACION.md.
- out_of_scope: tocar .githooks/pre-commit (es 0257 y su fix-loop) - FUERA; aplicar el
  upgrade a NOVA real (va como operacion aparte gateada por el operador) - FUERA;
  reservadas N=6 - FUERA; fondo intocable - FUERA.
- risk: low | estimate: S
- SECUENCIA: arranca tras el cierre de 0257 (comparte scripts/new_instance.py con su
  scope); puede correr en paralelo con 0258 (rutas disjuntas), GO de a una igualmente.
