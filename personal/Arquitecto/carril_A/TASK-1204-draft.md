---
task_id: TASK-1204
title: "[DECISION-1002][t4] Stubs/manifests de archivo frio (formato estable + goldens) segun SPEC-AEGIS-1002 s.5"
type: build
status: ready
owner: Codex
phase: instancia-aegis
priority: high
created_at: 2026-07-07
reviewer: Analista
checker: Arquitecto
project: aegis-instance
relates_to: [DECISION-1002, SPEC-AEGIS-1002, TASK-1202, TASK-1203]
file: Area_comun/tasks/TASK-1204-memoria-stubs-manifests.md
intake:
  type: infra
  goal: Implementar la Fase 2 de DECISION-1002 -- el FORMATO ESTABLE de archivo frio (cold pack + manifest.json y stub caliente) EXACTAMENTE segun SPEC-AEGIS-1002 s.5, con goldens commiteados como fixtures, la tabla hot_cold_rules poblada con la politica v1 adjudicada (s.1), y las guardas de stub en memdb check-drift. NO mueve artefactos reales (eso es F3/t5); esta tarea entrega el CONTRATO de formato + validadores + goldens sobre el memdb ya construido en TASK-1203.
  acceptance:
    - "Cold pack manifest.json implementado byte-a-byte segun s.5: campos {pack_id, pack_type, created_at, git_ref, artifacts:[{artifact_id, original_path, cold_path, sha256, bytes}], sha256_manifest}; sha256_manifest = sha256 del manifest canonicalizado SIN ese campo (test que verifica la exclusion y la canonicalizacion determinista)."
    - "Stub caliente (markdown) implementado segun s.5: frontmatter {stub_of, original_path, cold_path, pack_id, sha256, git_commit, rehydration_command} + resumen corto; validador de forma con caso negativo (frontmatter incompleto RECHAZADO)."
    - "Goldens (s.5): 1 cold pack de ejemplo + 1 stub de ejemplo commiteados como fixtures de test; un test de regresion los valida contra el schema y verifica que sha256/sha256_manifest cuadran."
    - "Tabla hot_cold_rules poblada con la politica v1 NORMATIVA (s.1: siempre-hot, frio-candidato-con-ventanas, frio-con-stub, nunca-por-esta-via) con los parametros numericos (ventanas N, umbrales de antiguedad) materializados; test que verifica que las 4 clases estan presentes y que un artefacto se clasifica de forma determinista."
    - "memdb check-drift EXTENDIDO con las 2 guardas de stub de s.6 -- (a) stub huerfano (stub cuyo pack/artifact no existe) y (b) decision ACTIVA fria sin stub (policy_status.hot_required=true y el archivo no esta hot ni tiene stub) -- cada una con su fixture NEGATIVO que hace fallar check-drift (exit != 0) y su caso positivo verde."
    - "Round-trip / cero-writers preservados: memdb build sigue reconstruyendo db_hash identico (gate de t3 intacto); auditoria estatica + test de hash de arbol confirman CERO escrituras a Area_comun/state/** y runtime/state/** desde el codigo de esta tarea."
    - "Etiquetas de honestidad de SPEC-AEGIS-1002 actualizadas en el handoff: stub/cold-pack/goldens suben de [EST-PEND] a [ESTRUCTURAL] SOLO con el test verde citado; lo que quede pendiente (F3, packs reales) se declara EST-PEND explicito."
  verification_cmd:
    - python scripts/validate_collaboration_state.py
  scope_routes:
    - scripts/memdb.py (o el modulo de formato de frio declarado en el claim)
    - cold/ (goldens; o la ruta de fixtures declarada en el claim)
    - stubs/ (goldens; o la ruta declarada en el claim)
    - runtime/memory/ (gitignored)
    - Area_comun/tasks/TASK-1204-memoria-stubs-manifests.md
  out_of_scope:
    - Mover/archivar artefactos REALES (F3/t5); piloto de rehidratacion (t5); embeddings; clasificador PII; FTS (F4); el hub; tocar el config pineado de la instancia.
  risk: medium
  estimate: M
---

# TASK-1204 - [DECISION-1002][t4] Stubs/manifests de archivo frio (formato estable + goldens)

Contrato: `Area_comun/specs/SPEC-AEGIS-1002-arquitectura-memoria.md` s.5 (Formatos de frio) + s.6 (guardas
de stub en check-drift), HEAD de main. Insumo: memdb read-only de TASK-1203 (done) + DISCOVERY F0
(TASK-1201). Coordinacion: mecanismo Codex->Aegis v1 (runbook s.6): senal por el mailbox del HUB,
atestacion en el ledger de AEGIS con las llaves propias de Codex.

Alcance F2 (NO F3): esta tarea entrega el FORMATO estable + goldens + guardas, NO el movimiento real de
artefactos a frio (eso es t5). Gate: Arquitecto + Analista (adversarial, clon limpio).
