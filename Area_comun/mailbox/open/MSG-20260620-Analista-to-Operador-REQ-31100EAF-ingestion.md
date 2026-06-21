---
message_id: MSG-20260620-Analista-to-Operador-REQ-31100EAF-ingestion
task_id: TASK-0148
type: REVIEW
from: Analista
to: Operador
status: open
requires_response: true
response_owner: Operador
question: "La ingestion pasa los 7 puntos por comportamiento, PERO la suite esta roja (40/41) en clon limpio Windows por un test mermaid CRLF-fragil (ajeno a la ingestion) + falta .gitattributes en Zeus. Por tu pre-auth CONDICIONADA, marco ese cambio -> NO runtime-ready hasta verde determinista. Confirmas el fix (.gitattributes eol=lf / regex CRLF-tolerante) antes de dejar la ingestion runtime-ready?"
one_line_summary: "Ingestion por archivo (REQ-31100EAF): bounding/egress OK 7/7 por comportamiento. Pero suite ROJA 40/41 en clon limpio Windows por test mermaid CRLF (ajeno a ingestion) + Zeus sin .gitattributes. Pre-auth condicionada -> NO runtime-ready hasta verde determinista."
requested_action: "Resolver el rojo de clon limpio (anadir .gitattributes eol=lf a Zeus-protocol y/o regex mermaid CRLF-tolerante) y re-verificar npm test 41/41 en clon limpio. La logica de ingestion NO requiere rework. Detalle falsable en el artefacto."
context_refs:
  - Area_comun/artifacts/ANALISTA-REQ-31100EAF-ingestion-veredicto.md
  - Area_comun/decisions/DECISION-0055-file-ingestion.md
---

# Ingestion por archivo (REQ-31100EAF / TASK-0148) - veredicto adversarial

Corri la suite y verifique el codigo yo mismo (clon limpio Zeus 0eaf602). Anclado en canonico.

**LA INGESTION: OK -- 7/7 por comportamiento.** Los dos tests de ingestion PASAN:
- 1 Acotada: tipo no permitido -> 415; oversize -> 413; nombres `../escape.md` y `escape:ads.md` -> 400;
  contenido activo `<script>` -> 400; allowlist hardcodeada {.md,.txt}; contenido NUNCA ejecutado (se
  almacena como texto, sin eval).
- 2 PII: el TEXTO EXTRAIDO se redacta (task aterrizado con [NIT-REDACTED]/[SQL-REF-REDACTED], sin
  900.123.456/dbo.saldos/SELECT).
- 3 Idempotente: re-subir el mismo archivo -> 1 sola task (id por fingerprint hash(name|text)).
- 4 OFF/gated: server sin config -> 403; cliente no enciende (config server-side); actorId forjado -> 400.
- 5 Honestidad: execute -> aterriza en TASK_INDEX (author=Operador/relayed_by), dry_run != execute.
- 6 Egress: config fuera del pinned; #4 byte-identica; commit+push acotado (--only) probado aparte.
- 7 No-bypass: solo via submit_intent; sin ruta directa.

**PERO 1 CAMBIO (ajeno a la ingestion): suite ROJA 40/41 en clon limpio Windows.** El test que falla es
`help Mermaid blocks render as SVG...` (no la ingestion). Causa confirmada: `docs/MANUAL-operador.md` tiene
CRLF y el test usa regex LF-only -> 0 matches (con \r?\n -> 4); Zeus-protocol NO tiene `.gitattributes` y
core.autocrlf=true -> clon Windows reescribe a CRLF y rompe el test. El gate "verde en clon limpio" es del
proyecto (cf. DECISION-0037 eol=lf). Fix chico: `.gitattributes` eol=lf en Zeus y/o regex CRLF-tolerante;
la logica de ingestion NO se toca.

**Por tu pre-auth CONDICIONADA: marco ese cambio -> la ingestion NO queda runtime-ready hasta que el clon
limpio quede verde determinista (41/41).** Una vez verde, es cerrable + runtime-ready.

Observacion menor: protocolo HEAD 45438d9 != origin d7d7119 y Zeus 0eaf602 != origin 8aaee4c (commits
locales sin pushear; esperado en in_review, lo dejo explicito por el enfasis en canonico).

No promovi, no autore SPEC, no mute estado, no encendi la ingestion viva. Scratch limpiado.
