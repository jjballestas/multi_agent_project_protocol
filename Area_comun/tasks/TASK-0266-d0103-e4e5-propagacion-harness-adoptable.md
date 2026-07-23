---
task_id: TASK-0266
title: "[DECISION-0103][C5/E4-E5] Propagacion del harness: .githooks/** adoptable en upgrade_instance + cableado core.hooksPath en new_instance"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0096]
linked_decisions: [DECISION-0103, DECISION-0096]
file: Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
intake:
  type: infra
  goal: Cerrar el hueco de propagacion de la clausula C5 (enmiendas E4/E5 de DECISION-0103, firma del Operador 2026-07-19), (E4) .githooks/** entra al conjunto adoptable de upgrade_instance.py (DEFAULT_ADOPTABLE_GLOBS o bloque upgrade.adoptable_globs del config, lo que resulte mas limpio) para que las instancias EXISTENTES -- NOVA incluida -- reciban el hook por la via de upgrade; y (E5) new_instance.py CABLEA core.hooksPath al instanciar, porque copiar el hook sin armar el path lo deja muerto (el mismo error que motivo la C5, un nivel mas arriba). Unidad hermana de TASK-0257: no toca el hook en si, arregla su PROPAGACION.
  acceptance:
    - E4, upgrade_instance.py contra una instancia real en sandbox reporta el delta de .githooks/ como adoptable; el mecanismo elegido (globs por defecto o bloque upgrade del config) queda documentado con su racional.
    - H1, runtime/vcs.py commit_turn pasa a verify=True por defecto (hoy anade --no-verify por defecto y todo commit de turno del runtime salta el hook); el bypass queda solo como excepcion explicita y declarada (p.ej. commits de rollback/remediacion del propio gate), documentada con racional.
    - H1 verificacion, un turno de replay en instancia scratch FALLA si su snapshot deja el estado colaborativo en rojo, y pasa en verde (el runtime queda gateado por el hook).
    - E5, instancia NUEVA en sandbox nace con git config core.hooksPath devolviendo la ruta SIN paso manual, y una prueba negativa (estado gobernado roto staged) aborta el commit en esa instancia.
    - Instancia EXISTENTE upgradeada en sandbox recibe .githooks/ y queda armable con la instruccion documentada; su validate sale verde tras el upgrade.
    - Cero cambios de comportamiento en .githooks/pre-commit (eso es TASK-0257 y su fix-loop); esta unidad solo toca la propagacion.
    - Neutralidad de dominio, validate y scan_encoding verdes.
  verification_cmd:
    - Dry-run/delta de upgrade_instance.py sobre instancia sandbox mostrando .githooks/ adoptable
    - new_instance.py a directorio temporal + git config core.hooksPath + prueba negativa de commit
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - scripts/upgrade_instance.py
    - scripts/new_instance.py
    - runtime/vcs.py
    - examples/
    - protocol.config.template.json
    - README_INSTANCIACION.md
  out_of_scope:
    - Tocar .githooks/pre-commit - FUERA (es TASK-0257 y su fix-loop activo).
    - Aplicar el upgrade a NOVA real u otra instancia viva - FUERA (operacion aparte gateada por el Operador).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado del hub (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable; el bloque upgrade, si se usa, va en el TEMPLATE).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: low
  estimate: S
---

# TASK-0266 - [DECISION-0103][E4/E5] Propagacion del harness

Origen: enmiendas E4/E5 de DECISION-0103 (hallazgo del Asesor verificado en codigo,
firma del Operador en MSG-20260719-Operador-to-Arquitecto-ENMIENDA-E4-E5-adoptable-
githooks; ruteo como unidad hermana decidido por el Arquitecto con preferencia declarada
del Operador). AMPLIACION PRE-ARRANQUE (2026-07-19, antes de cualquier GO): H1 del
MSG-...-HALLAZGOS-hook-runtime-bypass-y-mutex plegado aqui por ruteo delegado -- el
runtime comitea con no-verify por defecto (runtime/vcs.py:56) y debe quedar gateado
ANTES de que esta unidad propague runtime/** a las instancias. La ampliacion es
pre-arranque (la unidad no tiene GO ni claim), no un cambio a mitad de vuelo.
Secuencia: arranca tras el CIERRE de TASK-0257 (comparte scripts/new_instance.py con su
scope); puede correr en paralelo con TASK-0258 (rutas disjuntas), manteniendo GO de a
una.
