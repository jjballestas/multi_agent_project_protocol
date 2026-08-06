---
task_id: TASK-0314
file: Area_comun/tasks/TASK-0314-port-f1-memoria-hibrida-hub.md
title: "F1-PORT: promover el motor de memoria hibrida de la instancia a master NEUTRAL del hub (SPEC-MEMORIA-HIBRIDA s.16; DECISION-0100 s.2)"
status: in_progress
type: feature
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - DECISION-0100
  - DECISION-0096
  - DECISION-0081
  - DECISION-0026
  - SPEC-MEMORIA-HIBRIDA
created_at: 2026-08-06
intake:
  type: feature
  goal: >
    Portar el motor de memoria hibrida ya probado en la instancia Nova-Payroll a master NEUTRAL del
    hub, alcance F1 SOLO (indexador read-only + query/retrieve + revive_pack + gates fast/full +
    suite de tests + cableado del repo + export a instancias). El port NO es copia: exige resolver
    los 12 hallazgos P1-P12 de SPEC-MEMORIA-HIBRIDA s.16.3 (neutralidad de dominio, calibracion al
    vocabulario real del hub, y acotado del revive_pack), cada uno con su test. La viabilidad ya
    esta MEDIDA sobre el corpus real del hub (s.16.2): 4150 artefactos, round-trip AC5 byte a byte,
    drift --fast y --full verdes, I2 read-only verificado. Ni el ledger ni el fondo intocable se
    tocan: el indexador es read-only y su unico output es runtime/memory/index.db (gitignored).
  acceptance:
    - "AC1 (neutralidad, frontera dura): P1-P4 resueltos. El nucleo NO contiene lexico de dominio (nada de salario/empleado/nombre/iban como patron PII del nucleo); el lexico de dominio vive en archivo configurable por instancia FUERA del config pineado y VACIO por defecto; project se deriva del protocol.config.json (no literal); el nombre del formato de dump es neutro. scan_domain_neutrality.py exit 0."
    - "AC2 (calibracion sin relajar garantias): P5-P10 y P12 resueltos ampliando el dominio de valores ACEPTADOS conservando la validacion por VALOR de s.7 (enums FINITOS, regex ancladas, PII por valor). Prohibido resolver un rechazo desactivando su validacion o admitiendo texto libre en el indice."
    - "AC3 (tests): suite VERDE COMPLETA en clon limpio, incluidos los 2 casos que hoy fallan (test_scan_encoding_excludes_runtime_memory y test_current_tree_build_does_not_change_tracked_status), mas un test NUEVO por cada hallazgo P1-P12, con un negativo que demuestre que el lexico de dominio ya no vive en el nucleo."
    - "AC4 (cableado del repo): .gitignore incluye runtime/memory/; scan_encoding.py y scan_encoding.ps1 excluyen esa ruta; scan_encoding.py exit 0 con los scripts nuevos en el arbol."
    - "AC5 (gates sobre el corpus real, por EXIT CODE en clon limpio): build sin error duro; round-trip AC5 byte a byte (dump A == dump B); check_memory_db_drift --fast y --full exit 0. Los warnings restantes deben ser SOLO frontmatter realmente malformado (H2 de s.16.4), no metadata bien formada del hub."
    - "AC6 (I2 read-only): tras correr el indexador sobre un arbol limpio, git status --porcelain vacio y validate_collaboration_state.py exit 0 antes y despues."
    - "AC7 (revive_pack acotado, P11): presupuesto declarado, seleccion por is_current + recencia, resumen determinista derivado de metadata (jamas del cuerpo por LLM), token_estimate emitido y declaracion explicita de lo que quedo fuera del pack."
    - "AC8 (export born-operational, DECISION-0096): scripts/new_instance.py publica scripts/memory/ en la instancia nueva, con test que lo demuestre."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/scan_encoding.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/memory/
    - scripts/scan_encoding.py
    - scripts/scan_encoding.ps1
    - scripts/new_instance.py
    - .gitignore
  out_of_scope: >
    F2 (stubs/manifests, --propose-cold), F3 (enfriado real de historia: exige DECISION de
    activacion + MEMORY_HOT_COLD_RULES.json + regla anti-B1), F4 (FTS de contenido, embeddings,
    deteccion de contradicciones). Tampoco entra la remediacion de los defectos de corpus H1-H3
    (s.16.4): son higiene gobernada aparte. PROHIBIDO modificar validate_collaboration_state.*,
    submit_intent.py, protocol.config.json, agent_registry, el genesis o cualquier archivo de
    runtime/state/ (fondo intocable: config 2E35F26E, epoch 1.14.0, dataset N=500).
  risk: medium
  estimate: L
notes: >
  Contrato completo en SPEC-MEMORIA-HIBRIDA s.16 (v0.3.0). Precondicion satisfecha: DECISION-0100
  s.2 agendo la promocion para post-ventana-medida y la ventana cerro el 2026-08-02 con TASK-0308
  done; GO explicito del operador el 2026-08-06 con alcance F1 y cadena Codex maker + Analista
  checker. Fuente del motor: instancia Nova-Payroll HEAD 0a33fed, scripts/memory/ (6 archivos,
  stdlib pura, sin dependencias externas). La medicion de viabilidad (s.16.2) la corrio el
  Arquitecto en clon de scratch bajo D:/Aegis_Scratch/ (DECISION-0104), sin tocar el arbol vivo.
  H1 de s.16.4 (3 mensajes duplicados answered/archived con blobs divergentes) ABORTA el build del
  corpus completo: si el maker lo encuentra sin remediar, lo reporta y sigue con el resto -- NO lo
  arregla por su cuenta (rutas de mailbox bajo gobierno del Arquitecto, DECISION-0018).
