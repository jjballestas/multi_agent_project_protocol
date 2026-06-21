---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0150
task_id: TASK-0150
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0150 (ready, maker=Codex): carga por archivo v2 FASE A (plumbing determinista). Upload gobernado server-NO-MODELO-EGRESS (no SDK/socket/API-key de LLM) + screening PII real best-effort honesto + store FUERA del dataset (gitignored entregado + git ls-files vacio + excluido del git-status del indicador) + hash SHA-256 bytes crudos + emit extraction-task con contrato autocontenido (task_upsert status valido, sin kind/status nuevo) + idempotente; + selector de modo (digitado vs archivo) validando obligatorios (AC39), rama-archivo GATEADA detras de B+C. AC40/AC42 SPEC-0086 ext10, DECISION-0056. Codigo en Zeus; yo checker DESDE CLON LIMPIO + Analista antes de cerrar. Incorpora el red-team (38/40)."
context_refs:
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0150-codex-file-intake-v2-faseA.md
  - Area_comun/artifacts/REDTEAM-ingestion-v2-OPCION4-veredicto.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: blocking
---

# GO - TASK-0150 carga por archivo v2 FASE A (AC40/AC42; DECISION-0056)

Ratificado (DECISION-0056 + ext10) + decisiones del operador D-PII (detector real best-effort + honesto + gate
humano duro en Fase B) y D-ACTOR (relay honesto como Arquitecto, sin re-genesis). Incorpora el red-team
adversarial (38/40 confirmados; artefacto citado). maker=Codex / checker=Arquitecto DESDE CLON LIMPIO + PASADA
DEL ANALISTA al cierre. Codigo en Zeus. OFF-by-default. Fase A NO depende del agente extractor.

## Alcance (Fase A = plumbing determinista)
1. **AC40 Upload no-MODELO-egress:** el server NO llama a ningun MODELO (sin SDK/socket/API-key de LLM; el
   git-push gobernado existente NO cuenta). (a) screening PII REAL best-effort (email/tel/doc/NIT/razon-social/
   SQL/nombres) + ASCII, HONESTO (no garantizado); (b) STORE FUERA del dataset (tmp SO o gitignored entregado +
   `git ls-files` vacio + excluido del git-status del indicador), ruta acotada/saneada, allowlist+tamano, inerte;
   hash atestado = **SHA-256 bytes crudos**; (c) emit extraction-task con CONTRATO autocontenido via task_upsert
   status YA valido (NO kind/status nuevo); idempotente por (sha256+project). #4 byte-identica.
2. **AC42 Selector de modo:** digitado vs archivo; ambos validan obligatorios (AC39); rama-archivo GATEADA detras
   de B+C (no vacia).

## Cierre
- AC40+AC42 verdes (prueba negativa no-MODELO-egress estatica + control positivo; store fuera del dataset;
  SHA-256; emit-task; idempotente; selector). Carry AC37/AC38/AC39/AC13.
- npm test verde **EN CLON LIMPIO**; #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0;
  neutralidad/encoding 0. Checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.

NO encender vivo. Entrega in_review con handoff autocontenido y libera tu claim. Es la Fase A de 3 (B panel+gate
PII / C agente extractor). Canal ASCII.
