---
task_id: TASK-1205
title: "[DECISION-1002][t5] Piloto de archivo frio (movimiento hot->cold real + rehidratacion verificada) segun SPEC-AEGIS-1002 s.3.4/s.4"
type: build
status: ready
owner: Codex
phase: instancia-aegis
priority: high
created_at: 2026-07-07
reviewer: Analista
checker: Arquitecto
project: aegis-instance
relates_to: [DECISION-1002, SPEC-AEGIS-1002, TASK-1203, TASK-1204]
file: Area_comun/tasks/TASK-1205-memoria-piloto-frio.md
intake:
  type: infra
  goal: Implementar la Fase 3 (piloto) de DECISION-1002 -- el PRIMER movimiento hot->cold REAL de un subset pequeno y SEGURO de artefactos historicos, empaquetados con los formatos de TASK-1204 (cold pack + manifest.json + stub caliente), MAS el comando de rehidratacion `memdb retrieve` que verifica sha256 contra el manifest ANTES de entregar. Demuestra el ciclo completo archivar->recuperar sin perdida, con check-drift verde. NO es la operacion estable (F5); es el piloto acotado.
  acceptance:
    - "SUBSET SEGURO: mover a frio entre 3 y 6 artefactos HISTORICOS cuya ausencia del working tree NO rompe validate -- es decir, artefactos NO referenciados por ningun campo file: de TASK_INDEX/CLAIMS/PROJECT_STATE vivos (p.ej. mensajes viejos de Area_comun/mailbox/archived/, handoffs cerrados, o artifacts historicos). Documentar en el handoff la regla de seleccion y por que cada uno es seguro. NUNCA mover un .md de tarea referenciado por el ledger vivo."
    - "Movimiento GOBERNADO (SPEC s.3.4): la promocion hot->cold se hace como tarea gobernada con claim + commit explicito; por cada artefacto movido queda (a) su cold pack real bajo cold/<pack_id>/ con manifest.json valido (formato t4), (b) su stub caliente en la ruta original (o stubs/) con el frontmatter t4 y rehydration_command, (c) el artefacto original YA NO esta hot (movido, no copiado)."
    - "memdb retrieve <artifact_id> implementado: localiza el cold pack via el manifest, verifica sha256 del contenido frio contra el manifest ANTES de entregar (fail-closed si no cuadra), entrega los bytes, y registra retrieval_log (retrieved_at, actor, resultado). Test con caso NEGATIVO: manifest/sha manipulado -> retrieve FALLA (exit != 0), no entrega."
    - "REHIDRATACION VERIFICADA (gate bloqueante de la tarea): para CADA artefacto del piloto, retrieve devuelve bytes IDENTICOS al original (sha256 == el que se archivo); test automatizado que archiva -> borra hot -> retrieve -> compara byte-a-byte."
    - "check-drift VERDE post-piloto: los artefactos movidos tienen cold_pack+stub -> la guarda 'artefacto ausente sin cold_pack+stub' NO dispara para ellos; y SI dispara (exit != 0) si se elimina uno de sus stubs o packs (fixture negativo). La guarda de decision-activa-fria-sin-stub sigue intacta."
    - "Round-trip / cero-writers preservados: memdb build --from cold-packs incorpora los artefactos frios; dos builds seguidos dan db_hash identico. CERO escrituras del indexador/retrieve a Area_comun/state/** y runtime/state/** (retrieve solo escribe retrieval_log en el memdb, gitignored). Auditoria estatica + hash de arbol."
    - "Neutralidad GENUINA (cierra el hallazgo del gate de t4): scan_domain_neutrality exit 0 SIN ofuscacion -- reemplazar en scripts/test_memdb.py::test_ca11 los nombres de agente escritos como tuplas de bytes ASCII por placeholders neutrales reales (agent-a/agent-b o lookup del agent_registry). La evasion por byte-encoding NO cuenta como neutralidad."
    - "Etiquetas de honestidad de SPEC-AEGIS-1002 (s.3.4/s.4) actualizadas en el handoff: retrieve/movimiento-hot-cold suben de [EST-PEND] a [ESTRUCTURAL] SOLO con el test verde citado; F4 (FTS/embeddings) y F5 (operacion estable) quedan EST-PEND explicito."
  verification_cmd:
    - python scripts/validate_collaboration_state.py
  scope_routes:
    - scripts/memdb.py
    - scripts/test_memdb.py
    - cold/ (packs reales del piloto)
    - stubs/ (stubs reales del piloto)
    - Area_comun/mailbox/archived/ (si el subset sale de ahi; declarar los MSG concretos en el claim)
    - runtime/memory/ (gitignored)
    - Area_comun/tasks/TASK-1205-memoria-piloto-frio.md
  out_of_scope:
    - FTS / embeddings / clasificador PII (F4); operacion estable / watcher (F5); mover artefactos referenciados por el ledger vivo; el hub; tocar el config pineado de la instancia.
  risk: medium
  estimate: L
---

# TASK-1205 - [DECISION-1002][t5] Piloto de archivo frio (movimiento hot->cold + rehidratacion)

Contrato: `Area_comun/specs/SPEC-AEGIS-1002-arquitectura-memoria.md` s.3.4 (promocion gobernada
hot->cold), s.4 (memdb retrieve / rehidratacion), s.5 (formatos de frio de t4), s.6 (guardas de
check-drift). Insumo: memdb de TASK-1203 + formatos/goldens de TASK-1204 (done). Coordinacion:
mecanismo Codex->Aegis v1 (runbook s.6).

CANDADO DE SEGURIDAD: el piloto mueve solo artefactos HISTORICOS no referenciados por el ledger
vivo; el movimiento es SIEMPRE gobernado (claim + commit); la ausencia de un artefacto movido no
debe romper validate (queda su stub). Gate: Arquitecto (subagente adversarial, clon limpio) +
Analista segun DECISION-1002 s.17.5.
