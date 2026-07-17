---
message_id: MSG-20260717-Arquitecto-to-Operador-HITO-f1-completa-demo-revive-exitosa
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/artifacts/CROSS-ATESTACION-hub-nova-payroll-registro.md
one_line_summary: "HITO MAYOR: F1 COMPLETA (4/4 done en un dia de carril automatizado) + DEMO REVIVE EXITOSA end-to-end (criterio 6d): el peon murio, un worker de contexto CERO revivio SOLO con su pack atestado, verifico el pack contra el ledger vivo y continuo una tarea real hasta in_review con gates verdes. Cross-atestada en el hub (Entrada 1). Fase A lista para tu DECISION DE ADOPCION."
---

# HITO - F1 completa + DEMO REVIVE exitosa (Fase A lista para decision)

## La demostracion (criterio 6d, cumplida)

1. Peon Codex MUERTO de verdad (stop-marker, log citado en la atestacion).
2. Tarea real pendiente (TASK-0005, runbook F1) registrada tras la muerte: nadie podia tomarla.
3. Pack atestado generado del canon (sha 9866792a..., anclado al commit 23259a8; identidad +
   memoria real + tarea + GO + decisiones aplicables; atestacion por blob por fuente; nota de
   no-autoridad).
4. Worker de CONTEXTO CERO revivio SOLO con el pack: dedujo su identidad, VERIFICO el pack
   contra el ledger vivo antes de actuar (detecto trabajo ya hecho y NO lo repitio), claimo por
   intents firmados (autoridad = llaves de instancia, no el pack), verifico EN VIVO los 6 flujos
   para el runbook, entrego a in_review con claims liberados, gates 0/0/0, clean-clone verde,
   drift 0 (seq 129-137), y cumplio la regla de memoria dorada.
5. Verificacion independiente mia + atestacion completa en la instancia + cross-atest Entrada 1
   en el hub con hashes por blob.

**El pack fue SUFICIENTE y SEGURO. Los peones REVIVEN. Es la evidencia employee-ready que
ningun motor externo tiene.**

## F1: 4/4 done en un dia

U1 indexador+DDL (NO-GO 3 blockers -> GO formal) | U2 round-trip AC5 (NO-GO AC5-vacuo ->
incremental real -> GO formal) | U3 drift+query (GO informal-sustituto declarado) | U4
revive_pack (GO informal-sustituto declarado). 2 ciclos de remediacion reales cazados por el
checker; 2 sustituciones de checker por el clasificador del proveedor, ambas DECLARADAS
(checker_formal=0) y en modelo fuerte (0099 r3). TASK-0005 (runbook) en review normal.

## Que decides tu (cuando quieras; nada urge)

(a) **Decision de adopcion de la memoria hibrida** (el objetivo del GO: F1 end-to-end +
demostracion lista); (b) si el fallback informal te vale para cerrar TASK-0005 o esperamos al
formal desbloqueado; (c) la opcion estructural del clasificador (FYI previo); (d) GO de F2
minimo solo si el probe lo pide (hoy nada lo pide). Los encargos E2 de NOVA conservan su
prioridad (corpus <=25-jul, BR-C4 <=29-jul, reconciliacion 26-29).

-- Arquitecto. Hora local ~21:15 (UTC+2). Fondo intacto: N=500, 2E35F26E, 1.14.0.
