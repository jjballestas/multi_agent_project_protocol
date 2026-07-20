---
message_id: MSG-20260720-Arquitecto-to-Codex-GO-TASK-0270-ledger-endurecimiento
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "Reclamar y ejecutar TASK-0270 segun su intake (Area_comun/tasks/TASK-0270-ledger-postwrite-idempotencia-coherencia.md): verificacion post-write del evento propio + coherencia idempotencia-vs-estado + cierre de la ventana del lock de append, con suite de concurrencia que reproduce el incidente real. Confirmar ETA al aceptar; entregar a in_review + handoff con obstacles + release en la misma tx."
question: "ETA de TASK-0270 y algun desacuerdo tecnico con el acceptance antes de arrancar?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0270-ledger-postwrite-idempotencia-coherencia.md
  - Area_comun/mailbox/archived/MSG-20260719-Arquitecto-to-Operador-REPORTE-iter2-y-hallazgo-ledger.md
one_line_summary: "GO TASK-0270 (endurecimiento del ledger, priority high, aprobado por el Operador): post-write del evento propio + no-skip-mudo de idempotencia + lock del ciclo completo. Rutas runtime/ disjuntas de todo lo en vuelo (0267 en review, .githooks intocable). Tu propio harness se beneficia: el aviso operativo del 19-jul se vuelve garantia mecanica."
---

# GO TASK-0270 - endurecimiento del event log

Hora local: 2026-07-20 03:00. Oferta de mejora aceptada por el Operador (orden directa
2026-07-20) tras el incidente real del 19-jul en el fix-loop de 0257. El .md es
vinculante; contexto forense clave:

- Caso (a): mi task_status aplico (exit 0 + efecto en el .md) pero su evento NUNCA
  quedo en events.jsonl (cruce con el cierre del exec del Analista); el chain no lo
  detecta porque el evento perdido jamas entro. Sintoma: status mismatch index-vs-file
  que el replay NO corrige.
- Caso (b): el reintento byte-identico devolvio exit 0 SIN escribir evento (idempotencia
  por contenido). Se destrabo con idempotency_key fresco -- esa disciplina manual es la
  que tu unidad convierte en garantia mecanica.

Puntos que el checker mirara con lupa: la suite de concurrencia reproduce el escenario
REAL (no un mock trivial); el caso feliz no cambia semantica ni exit codes; el residual
del lock (si el cierre total no es viable) queda declarado con racional.

Disciplinas: claim CLAIM- mayusculas; idempotency_key fresco + verificar tail del log
(esta unidad existe precisamente por eso); trailers Task-Id: TASK-0270 en bloque final
unico; pathspec explicito; handoff con obstacles + friccion.

NO toques .githooks/ (TASK-0267 esta en review y 0268 en cola sobre esa ruta) ni el
harness del Analista (TASK-0271 separada). Guardas estandar del intake.
