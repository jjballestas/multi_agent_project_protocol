---
message_id: MSG-20260702-Operador-to-Arquitecto-FYI-cortafuegos-asesor
from: Operador
to: Arquitecto
type: FYI
status: open
requires_response: false
created_at: 2026-07-02
context_refs:
  - personal/operador/vision-nova/FIREWALL-ASESOR-ARQUITECTO.md
one_line_summary: "Cortafuegos anti-contaminacion Asesor->Arquitecto vigente: provenance en ordenes, cuarentena PRE-DECISION, verificacion contra ledger, checker ciego."
---

# FYI - Cortafuegos Asesor -> Arquitecto (vigente desde hoy)

El Operador formaliza reglas anti-contaminacion sobre el canal de ordenes
(detalle completo en personal/operador/vision-nova/FIREWALL-ASESOR-ARQUITECTO.md).
Lo que te ata a ti:

1. Las ordenes entrantes traeran secciones [DIRECTIVA] (vinculante) y
   [RECOMENDACION] (juicio del asesor: puedes objetar/mejorar/sustituir sin pedir
   permiso, dejando tu razon en el entregable). Orden sin marcas = todo
   [RECOMENDACION] salvo la accion pedida.
2. Verifica toda orden contra el ledger/estado real antes de ejecutar; si la orden
   contradice el ledger o una DECISION vigente: blocked + una pregunta concreta
   (DECISION-0018). Nunca ejecucion complaciente.
3. NO leas documentos marcados PRE-DECISION en personal/operador/**; no son
   contexto tuyo aunque los encuentres.
4. Las reviews del Analista siguen ancladas a clon limpio + AC del ledger; ningun
   racional del asesor se le rutea.

La orden F1 ya emitida (MSG-...-ACTION-orden-F1-registro-backlog) se ejecuta tal
cual; estas reglas aplican desde la proxima orden en adelante.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
