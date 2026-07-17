---
message_id: MSG-20260717-Arquitecto-to-Operador-HITO-u2-done-u3-lanzada
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-HITO-u1-done-u2-lanzada.md
one_line_summary: "HITO U2 = DONE (2do ciclo adversarial completo) + U3 LANZADA (drift --fast/--full + query/retrieve). Hallazgo estrella del checker en U2: AC5 VACUO (build normal borraba la DB igual que --rebuild -> la igualdad era fresh-vs-fresh); remediado con incremental real + test de DB sembrada; re-judgement GO sin slips. F1 = 2/4 unidades done; higiene instancia hecha (21 archivados)."
---

# HITO - U2 done + U3 lanzada (F1 al 50%)

## U2 cerrada (TASK-0002, instancia d554749)

- Cadena: entrega -> **NO-GO con hallazgo de clase evidencia-vacua**: el test AC5 comparaba dos
  builds frescos porque el modo normal borraba la DB igual que --rebuild -- la "demostracion" de
  reconstruible no ejercitaba el camino incremental que la SPEC s.6 exige. Exactamente el tipo de
  rubber-stamp tecnico que el carril existe para cazar.
- Remediacion (53ab2a1): incremental real (upsert in-place + eliminacion de huerfanas con cascada,
  sin borrar la DB) + test AC5 con DB SEMBRADA y mutaciones commiteadas (add/modify/delete) +
  idempotencia. Re-judgement independiente: GO sin slips (sentinelas operacionales sobreviven,
  reconciliacion correcta, byte-igual al rebuild fresco, regresion F1-F3 intacta).
- Ratificacion seq 51 + done-flip de Codex. Validate 0, drift 0, cero claims.

## U3 LANZADA (TASK-0003, instancia 812a7c4)

check_memory_db_drift --fast (solo archivos canonicos; sin DB = verde, I5) / --full (sweep
bidireccional fail-closed + round-trip como sub-chequeo) + query_memory_db (FTS5 con fallback
declarado + --retrieve con sha por blob git + retrieval_log). GO en cola de Codex.

## Estado F1: 2/4 done (U1 indexador, U2 round-trip); U3 en build; U4 (revive_pack + DEMO
REVIVE, criterio 6d) al cerrar U3. Higiene instancia: 21 consumidos archivados (open = solo
el GO vivo). Ambos crons del trio vivos. Sin accion tuya requerida.

-- Arquitecto. Hora local ~18:25 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
