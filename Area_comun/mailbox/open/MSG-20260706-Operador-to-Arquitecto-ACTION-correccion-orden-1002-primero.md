---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-correccion-orden-1002-primero
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-RESPUESTA-pendientes-vivos-brc4-orden-1001-1002.md
  - Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md
one_line_summary: "CORRECCION de orden: promover DECISION-1002 (memoria-hibrida) PRIMERO, luego DECISION-1001. Supersede el orden 1001->1002 de mi mensaje anterior. Razon: la memoria hibrida es prerequisito de que los peones revivan con contexto (contraste peones de Etapa 2)."
requested_action: "Invierte el orden de promocion que te di antes: promueve PRIMERO DECISION-1002, empezando por su tarea F0 (discovery/inventario, owner Arquitecto), y DESPUES DECISION-1001 (tarea 1 = SPEC de interrogacion). Todo lo demas de mi respuesta anterior sigue igual (BR-C4 opcion b, gate 2-clones antes de Contabilidad, prioridad dura Sprint 1 desde 30-jul)."
question: "Confirmas el nuevo orden 1002 -> 1001? Si ves una dependencia dura que lo impida (p.ej. 1001 habilita algo que 1002 necesita), dilo antes de promover."
---

# ACTION - Correccion de orden: 1002 primero

El Operador reprioriza: **DECISION-1002 (memoria-hibrida) se promueve PRIMERO**, luego DECISION-1001. Esto
supersede el orden 1001->1002 que te di en `MSG-...-RESPUESTA-pendientes-vivos-brc4-orden-1001-1002`.

**Razon:** la memoria hibrida es prerequisito de que los peones revivan con contexto (sinergia declarada en
DECISION-1002 s.7 + el contraste peones-vs-tokens del sello Etapa 2). Construir primero la base de memoria
tiene mas palanca para lo que viene.

**Nota:** este orden es de PRIORIDAD DE PRODUCTO (Aegis), no un elemento sellado del estudio -> reordenarlo
es libre, no toca el pre-registro ni lo medido. La doctrina anti-vibecoding de 1001 ya esta vigente por
DECISION-0084; su IMPLEMENTACION (la capa de interrogacion UX) puede ir despues de la base de memoria sin
conflicto.

**Concreto:**
- Primero: DECISION-1002, tarea F0 (discovery/inventario de artefactos + medicion de cold-start + politica
  hot/cold inicial; owner Arquitecto).
- Despues: DECISION-1001, tarea 1 (SPEC de la capa de interrogacion; owner Arquitecto, review Analista).
- Sin cambios: BR-C4 opcion (b), gate e2e-2-clones antes de Contabilidad, prioridad dura Sprint 1 desde 30-jul.

-- Operador
