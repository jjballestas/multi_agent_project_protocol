---
message_id: MSG-20260703-Operador-to-Arquitecto-DIRECTIVA-pipeline-al-dia-control-total
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - personal/operador/vision-nova/pipeline-vision-nova.html (bloque PIPELINE-DATA)
  - Area_comun/specs/nova/ (NOVA-DEV: 9 SPECs + informe)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
one_line_summary: "El Operador quiere el pipeline como PANEL DE CONTROL COMPLETO: falta NOVA-DEV entero, GOAL-P1, y F3.3/F3.4 estan stale (reporte falso). Pon el tablero al dia editando SOLO el bloque PIPELINE-DATA con la skill arquitecto-pipeline-vision-nova, con evidencia y sello de hora."
requested_action: "[DIRECTIVA del Operador] 'Todo debe quedar en el pipeline para yo controlar.' Actualiza personal/operador/vision-nova/pipeline-vision-nova.html editando SOLO el bloque PIPELINE-DATA (skill arquitecto-pipeline-vision-nova; evidencia obligatoria en 'hecho', sello de hora, no borrar items sin orden). Coloca en la fase que corresponda segun tu diseno del tablero: (1) AGREGAR NOVA-DEV / TASK-0246 -- 9 SPECs gobernadas (familia P3 P3-001..005 + pool Q4 P4-004/P2-004/P2-003/P6-003) + informe adversarial; prerequisito de F4 Sprint 1; estado en_curso; evidencia: Area_comun/specs/nova/ + gate Analista OK/CERRABLE en F-0246-01/02 (re-juicio 50cb3fd), sub-loop db_verified_at THROW en cierre (iter 2, commit 5669665, re-juicio pendiente). (2) AGREGAR GOAL-P1 -- fundacion tecnica / piloto de medicion baseline (sln, React+TS+Vite, capas .NET, health/OpenAPI/ProblemDetails/correlation-id+task_id, architecture tests, CI); ventana 3-8 jul; su medicion_journal.csv alimenta el corpus del sello; estado pendiente (abrir). (3) REFRESCAR F3.3 Instrumentacion -> en_curso; evidencia: scripts-medicion commiteados (medicion_ledger.py + schema_medicion 52 cols + schema_defectos, commit 11fddf4, smoke verde); pendiente EMPLAZAR al hub (personal/Arquitecto/TFM-medicion/corpus/) y congelar a v1.0 en el sello (4a ACTION mia, ver MSG ACTION-emplaza-scripts-medicion-hub). (4) REFRESCAR F3.4 SELLADO pre-registro -> nota que el SELLO-ETAPA-1-nova-budget-DRAFT.md esta listo; sella <=08-jul; CHECKLIST de inputs pendientes: estimates S/M/L de las ~10 unidades Q4 (Operador, <=08-jul), GRANT EXECUTE para paridad (Operador, <=14-jul, no bloquea), scripts emplazados+congelados, corpus GOAL-P1, sorteo NIST + sha256. (5) NOTAR que las 3 decisiones de dominio DD-01/02/03 quedaron RESUELTAS (commit 3093d6a) y se hornean en las SPECs (parte de NOVA-DEV). Objetivo: que el Operador vea en un solo tablero lo hecho (NOVA-DEV), lo time-critical (GOAL-P1 3-8 jul) y el avance de medicion/sello. No urge por horas pero es alta prioridad de control; cabe en la ventana muerta o junto a lo que ya estas haciendo."
question: ""
---

# DIRECTIVA - Pipeline como panel de control completo

El Operador quiere controlar TODO desde el pipeline y hoy faltan piezas grandes: NOVA-DEV entero no tiene
fila, GOAL-P1 no aparece, y F3.3/F3.4 estan en 'pendiente' sin evidencia aunque ya haya avance real
(scripts commiteados, SELLO en draft) -- tablero desactualizado = reporte falso.

Edita SOLO el bloque PIPELINE-DATA (tu skill) para dejar el tablero fiel:
1. **NOVA-DEV / TASK-0246** (9 SPECs + informe, gateado) como prerequisito de F4.
2. **GOAL-P1** (piloto baseline, 3-8 jul, alimenta el corpus del sello).
3. **F3.3 Instrumentacion** -> en_curso (scripts 11fddf4, pendiente emplazar al hub).
4. **F3.4 Sellado** -> draft listo + checklist de inputs (estimates, GRANT EXECUTE, emplace, corpus GOAL-P1, sorteo).
5. **DD-01/02/03** resueltas (3093d6a), hornear en SPECs.

Detalle con evidencia en requested_action. La presentacion (acordeon) ya esta; esto es solo DATA.
