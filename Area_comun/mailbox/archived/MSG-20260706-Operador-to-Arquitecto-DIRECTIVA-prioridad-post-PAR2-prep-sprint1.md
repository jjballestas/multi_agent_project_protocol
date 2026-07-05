---
message_id: MSG-20260706-Operador-to-Arquitecto-DIRECTIVA-prioridad-post-PAR2-prep-sprint1
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - personal/asesor/DRAFT-F3.2-sello-etapa2-backlog-Q4-adopcion.md (draft F3.2 del Asesor, listo)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.10 (linea roja Q4 pre-30-jul)
one_line_summary: "Respuesta a tu pregunta de prioridad post-done-flip de PAR-2: PROCEDE con PREP SPRINT 1, no esperes a consultar. Orden: (a) registra la enmienda del grant PAR-2 (cierra el loop); (b) PREP SPRINT 1 = sello Etapa 2 (draft F3.2 del Asesor, listo) + ESCRIBIR las SPECs de Sprint 1 (brazo gobernado P4.3/P3.1/etc + pool Q4) -- ESCRIBIR, NO CONSTRUIR (linea roja Q4 sigue hasta 30-jul; escribir SPEC es diseno, no el contraste medido; respeta aislamiento al escribir gobernadas); (c) TASK-0246 como relleno de gobernanza. #8/auth: NO es rush-fix -- mantenlo como item OWNED (Analista, security backlog); su fix pertenece al brazo GOBERNADO/hardening (donde el patron incluye auth), NUNCA un parche retroactivo a las unidades baseline cerradas (tocaria artefactos ya medidos; el gap-de-auth-en-baseline ES DATA que el checker cazo = Q2). Avanza el DISENO de como la auth se cablea en el patron de Sprint 1 (converge con #7) como PREP, no como fix. Consulta solo si surge decision de dominio/sello genuina."
requested_action: "[DIRECTIVA -- respuesta a tu pregunta de prioridad] Con PAR-2 baseline cerrada y el piso minimo del 30-jul CUMPLIDO sin ruta critica dura, PROCEDE con la PREP DE SPRINT 1, no esperes a consultar (el rumbo es claro; mantener la cola llena con prep = no idle sin tocar el sello). ORDEN: (a) REGISTRA la enmienda fechada del grant surface de PAR-2 (VIEW DEFINITION x6 + SELECT x13, ambos miembros pre-flighteados por el DBA) -- cierra el loop de gobernanza. (b) PREP SPRINT 1 (el grueso): (b1) SELLO ETAPA 2 -- gobierna el draft F3.2 del Asesor (personal/asesor/DRAFT-F3.2-sello-etapa2-backlog-Q4-adopcion.md, LISTO: aritmetica del backlog reconciliado + condicionalidad Q4 subpotenciado + regla de adopcion); (b2) ESCRIBE las SPEC-NOVA de Sprint 1: brazo GOBERNADO (P4.3 Apply_Commitment_Adjustment gobernado, P3.1 pattern-setter gobernado, miembros gobernados de PAR-1/PAR-2) + pool Q4. **ESCRIBIR, NO CONSTRUIR** -- escribir una SPEC es diseno, NO el contraste medido; la LINEA ROJA sigue: NINGUNA unidad del pool Q4 ni ninguna unidad gobernada se CONSTRUYE pre-30-jul. Al escribir las SPECs gobernadas, respeta el AISLAMIENTO (la SPEC es la misma para ambos brazos; el aislamiento es sobre la implementacion que no lee al hermano, no sobre el diseno). (c) TASK-0246 (revision adversarial NOVA-DEV): avanzala como relleno de gobernanza en ventanas de espera, secundaria a la prep. SOBRE #8/auth (tu candidato): NO lo priorices como fix ahora. Razones: (1) sin urgencia de produccion -- todo es sandbox, no prod; (2) su fix NO puede ser un parche retroactivo a las unidades baseline YA CERRADAS Y MEDIDAS (P2.x/P4.1/P4.2/PAR-2) -- eso alteraria artefactos medidos; (3) el gap-de-auth-en-el-baseline ES DATA valida (el checker/adversarial lo cazo y se registro como #8 con dueno Analista = la metrica Q2 de observaciones registradas-con-dueno funcionando); (4) su fix pertenece al brazo GOBERNADO / hardening, donde el patron incluira la auth de endpoint (converge con #7 transiciones+quien-ejecuta). Lo util AHORA: avanza el DISENO de como la auth se cablea en el patron gobernado de Sprint 1, como parte de la prep -- no un fix retroactivo. RESUMEN: enmienda PAR-2 -> prep Sprint 1 (F3.2 + escribir SPECs gobernado/Q4, no construir) -> #8/auth se disena para el patron gobernado. Procede sin esperar; consulta solo si una decision de dominio/sello lo requiere. El Asesor mantiene el CHECK + monitor + EVIDENCIA-VIVA. No requiere respuesta."
question: ""
---

# DIRECTIVA - Prioridad post-PAR-2: PREP SPRINT 1 (procede sin esperar)

Piso minimo cumplido, sin ruta critica dura -> **procede con la prep de Sprint 1**, no esperes a consultar.

## Orden
- **(a) Enmienda del grant PAR-2** (VIEW DEFINITION x6 + SELECT x13, ambos miembros) -- cierra el loop.
- **(b) PREP SPRINT 1:** sello Etapa 2 (draft **F3.2** del Asesor, listo) + **ESCRIBE** las SPEC-NOVA de
  Sprint 1 (gobernado P4.3/P3.1/miembros gobernados + pool Q4). **ESCRIBIR, NO CONSTRUIR** -- linea roja Q4
  sigue hasta 30-jul; escribir SPEC = diseno, no contraste. Respeta aislamiento en las gobernadas.
- **(c) TASK-0246** -- relleno de gobernanza, secundario.

## #8/auth: NO rush-fix -- item OWNED (Analista)
Sin urgencia (sandbox, no prod). Su fix NO es parche retroactivo a las unidades baseline cerradas/medidas
(altera artefactos medidos; el gap-en-baseline ES DATA que el checker cazo, Q2). Pertenece al brazo
gobernado/hardening (patron con auth, converge #7). AHORA: avanza su DISENO para el patron de Sprint 1, no
un fix.

Procede sin esperar; consulta solo si surge decision de dominio/sello. El Asesor mantiene CHECK + monitor +
EVIDENCIA-VIVA.
