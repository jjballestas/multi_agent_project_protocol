---
message_id: MSG-20260620-Analista-to-Operador-TASK-0150-faseA
task_id: TASK-0150
type: REVIEW
from: Analista
to: Operador
status: archived
requires_response: false
response_owner: none
one_line_summary: "Carga por archivo v2 FASE A (TASK-0150): OK -> CERRABLE. 10/10 bounding ingest/egress/PII PASAN por comportamiento; server NUNCA llama a modelo (estructural + control positivo); raw fuera del #4; candidatas no en el ledger; PII honesta best-effort; #4 byte-identica. 2 recomendaciones de endurecimiento para Fase B/C (no bloquean). CRLF previo RESUELTO."
requested_action: "Mi veredicto gatea el cierre de la Fase A: CERRABLE. El Arquitecto puede cerrar. Fases B/C pendientes; nada vivo. Ampliar el guard AC40 + politica de purga del raw ANTES de Fase C. Detalle en el artefacto."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0150-v2-faseA-veredicto.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
---

# Carga por archivo v2 FASE A (TASK-0150) - veredicto adversarial

Corri npm test yo mismo (Zeus clon 5121335, 42/42 estable x3) y verifique el codigo. Anclado en canonico.
Mi hallazgo CRLF previo (TASK-0148) quedo RESUELTO (.gitattributes eol=lf; manual LF-only en clon limpio).

VEREDICTO: **OK -> CERRABLE la Fase A.** 10/10 por comportamiento:
- 1 AC40 no-modelo: server.js + canonicalReader.js CERO egress saliente (sin fetch/socket/import dinamico);
  guard con CONTROL POSITIVO real (atrapa import OpenAI+api.openai.com falso). PASA.
- 2 Store fuera del dataset: git ls-files del store VACIO; storePath fuera del repo; sha256 verificado; raw
  nunca en el repo/#4; drift 0; config byte-identica. PASA.
- 3 PII best-effort HONESTO: screening email/phone/NIT/SQL, guaranteed:false declarado; sin PII cruda en el
  task; no requerida para aterrizar. PASA.
- 4 Contrato extraction: autocontenido (source_file_sha256 + candidate_hash + "store outside ledger" +
  "cada candidata exige revision humana de PII antes del intake"). PASA.
- 5 Candidatas no-ledger: `candidate` NO en VALID_TASK_STATUSES; el core NO cambio. PASA.
- 6 Idempotencia: re-subir identico -> 1 task. PASA.
- 7 OFF/gated: 403 si disabled; off-by-default; env activa; AC42 mode-selector; sin preview-as-green. PASA.
- 8 Atribucion: author=Operador/relayed_by=Arquitecto en el SERVER (producto), no en el core; relay honesto;
  cliente no inyecta actor/paths. PASA.
- 9 Honestidad: contrato exige no-candidate/failed; errores NO ecoan raw (solo metadata); aterrizaje real.
  (El state machine completo 0/basura/cap/failed/timeout/sin-agente es Fase C, gateada.) PASA.
- 10 No-bypass/neutralidad: solo submit_intent; neutralidad+encoding exit 0; #4 byte-identica. PASA.

RECOMENDACIONES (endurecimiento, PREREQUISITO de Fase B/C, NO bloquean Fase A):
1. Ampliar el guard AC40 a todo src/** + marcar CUALQUIER red saliente (no solo proveedores nombrados)
   ANTES de Fase C (cuando enciende el agente = la ventana de modelo real).
2. Politica de purga/TTL del raw en os-tmp para Fase B/C.

Observaciones menores: 1a corrida en frio dio 41/42, luego 42/42 x3 (flake de timeout, verde estable);
Zeus HEAD 5121335 != origin 2f760a6 (commits locales sin pushear, esperado en in_review).

Cierre formal = Arquitecto (checker) + tu visto. Fases B (panel+gate-PII) y C (agente extractor) pendientes;
nada vivo. No promovi, no mute estado, no encendi nada. Scratch limpiado.
