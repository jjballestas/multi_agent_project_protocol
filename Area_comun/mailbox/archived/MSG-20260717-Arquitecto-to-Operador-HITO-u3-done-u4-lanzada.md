---
message_id: MSG-20260717-Arquitecto-to-Operador-HITO-u3-done-u4-lanzada
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-FYI-clasificador-proveedor-recurrente-fallback-checker.md
one_line_summary: "HITO U3 = DONE (via fallback: checker informal modelo fuerte tras 2 bloqueos del clasificador del proveedor; GO con todos los vectores PASS por conducta en clon limpio + 1 hallazgo MEDIO diferido a F2 con criterio correctivo + residuales declarados; checker_formal=0 en el artefacto) + U4 LANZADA (revive_pack atestado, ULTIMA unidad de F1). Tras U4: DEMO REVIVE (criterio 6d) y F1 completa para tu decision de adopcion."
---

# HITO - U3 done (fallback ejecutado) + U4 lanzada (F1 3/4)

## U3 cerrada (TASK-0003, instancia 4a5bf64)

- Review formal bloqueada 2x por el clasificador del proveedor (FYI previo) -> fallback aplicado:
  checker INFORMAL anti-rubber-stamp en modelo fuerte, mismo mandato POR CONDUCTA en clon limpio.
- Veredicto GO con evidencia dura: I5 verificado (--fast verde sin DB y con DB basura; jamas abre
  sqlite3), --full fail-closed en LAS 6 mutaciones + 2 clases extra (edge falso y summary
  tampereado los caza el round-trip), query sin fuga de cuerpos + fallback DECLARADO, retrieve
  emite el BLOB citado (no el working tree dirty) y falla cerrado en tamper con log sin crecer.
- 1 hallazgo MEDIO diferido a F2 (registrado con criterio correctivo): una fila de clasificacion
  PII FORJADA (public_plane_allowed=1) pasa --full verde porque la tabla es operacional; sin
  consumidor del flag en F1 y la PII por patron se caza igual -> para F2: fail-closed ante
  cualquier flag de publicabilidad mientras el clasificador sea none-f1.
- Sustitucion DECLARADA (checker_formal=0 en el artefacto); re-judgement formal del Analista
  re-ejecutable cuando el proveedor desbloquee. Ratificacion seq 97 + done-flip.

## U4 LANZADA (TASK-0004, instancia 3c46ad7) - ULTIMA de F1

revive_pack.py: pack de arranque determinista por agente (memoria vigente + tareas/claims +
mailbox + decisiones aplicables + context cache) con ATESTACION por fuente (path+commit+sha de
blob, fail-closed), identidad I6 por chokepoint, nota de no-autoridad y token_estimate. La DEMO
REVIVE end-to-end (6d: peon muere -> revive SOLO con su pack -> continua tarea real) la orquesto
yo tras el done de U4, como cierre de F1.

F1: 3/4 done. Sin accion tuya requerida; el FYI del clasificador sigue abierto por si decides
la opcion estructural (Trusted Access / otro CLI).

-- Arquitecto. Hora local ~19:50 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
