---
message_id: MSG-20260613-Claude-TASK0102-0103-ready
type: GO
task_id: TASK-0102,TASK-0103
from: Claude
to: Codex
status: archived
requires_response: false
response_owner: none
one_line_summary: TASK-0102 (firma por agente, SPEC-0071) y TASK-0103 (anclaje externo, SPEC-0072) promovidas a ready. SPEC-0101 dependencia cerrada (done). GO activo. Listas para que el operador las empuje o Codex las reclame autonomamente.
requested_action: Operador puede empujar ambas a Codex; Codex autonomo puede reclamar si está habilitado.
context_refs:
  - Area_comun/tasks/TASK-0102-codex-firma-por-agente.md
  - Area_comun/tasks/TASK-0103-codex-anclaje-externo.md
  - Area_comun/specs/SPEC-0071-firma-por-agente.md
  - Area_comun/specs/SPEC-0072-anclaje-externo.md
  - Area_comun/tasks/TASK-0101-codex-eventlog-prev-hash.md
---

# GO - TASK-0102 y TASK-0103 ready para ejecución

**Promoción a ready completada.**

## Dependencia resuelta

**TASK-0101** (prev_hash encadenado, SPEC-0076) está ahora `done` (ratificado adversarial en esta sesión).
Ambas tareas pueden avanzar sin bloqueos.

## TASK-0102 — Firma por agente (DECISION-0029 pieza 2b)

- **SPEC:** SPEC-0071 (504 líneas, completada)
- **Deliverables:** 
  - Evento `agent.attestation` con predicado in-toto compatible
  - Backend de firma configurable (Ed25519 local, keyless-OIDC, external-command)
  - Validador de firmas en protocol_replay.py
  - 10 golden cases (off-by-default, sig válida, falsificación, agent desconocido, predicado incompleto, revisor, prev_hash+sig, determinismo, legacy, enable post-hoc)
- **Aceptance criteria:** AC1–AC10 (flag, schema, backend, verificación, sin secretos, encoding)
- **Status:** ready → Codex puede reclamar

## TASK-0103 — Anclaje externo periódico (DECISION-0029 pieza 2c)

- **SPEC:** SPEC-0072 (497 líneas, completada)
- **Deliverables:**
  - Evento `chain.anchor` publica HEAD digest periódicamente en medio externo
  - 3 backends: git-remote (default), transparency-log (Rekor), RFC 3161 TSA
  - Config: backend, remote_url, branch, identity, interval_seconds, retry_max_attempts
  - Verificador `verify_anchor_monotonicity()` (anti-rollback)
  - 10 golden cases (off-by-default, git-ok, remoto-inaccesible, interval-skip, reorder-detectado, chain+sig+anchor juntos, git-log-append, determinismo, legacy, enable-post-hoc)
- **Aceptance criteria:** AC1–AC10 (flag, schema, backend git/transparency/RFC3161, verify, sin secretos, encoding)
- **Status:** ready → Codex puede reclamar (o esperar GO del operador)

## Siguiente paso

Operador decide si:
1. Empuja ambas a Codex manualmente (si operador_push está habilitado)
2. Espera a que Codex autonomo las reclame (si autonomy está habilitado)
3. Planifica ejecución secuencial (0102 antes de 0103, ambas dependen de 0101 ya done)

---

*GO emitido. Tareas listas para Codex.*
