---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-brc4-opcion-b-dba-encargo
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/artifacts/PAQUETE-DEC-DOMINIO-P3x-sello-etapa2.md
  - personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
one_line_summary: "BR-C4 (item 3 del paquete P3.x) RESUELTO por el Operador: opcion (b) -- el Operador tiene DBA y compromete el sembrado de BR-C4 en sandbox antes del 29-jul para preservar Q4 n=10. El Asesor redacto el encargo del DBA (draft). Red de seguridad: si no se entrega verificado <=29-jul, la condicion sellada cae a n=7 (opcion a) sin accion."
requested_action: "Trackear el deadline 29-jul de BR-C4 (opcion b): P3.2/P3.3/P3.4 quedan en el pool Q4 con elegibilidad CONDICIONAL (n=10 condicional) hasta la entrega. Cuando el DBA entregue BR-C4 verificado en sandbox (guardas de permiso + set THROW + smoke de separacion emitir/aprobar/anular, ver el encargo del Asesor), registra la ENMIENDA FECHADA del sello (formato s.24/s.25) confirmando P3.2/P3.3/P3.4 elegibles Q4 -> n=10. Si NO llega verificado <=29-jul, ejecuta la condicion ya sellada: caen del pool -> Q4 n=7 (opcion a), sin penalidad. Es HARDENING simetrico (no altera el contraste; el dev no crea los procs, regla 8)."
question: "Confirmas el tracking de BR-C4 opcion (b) con deadline duro 29-jul y auto-fallback a n=7? El encargo del DBA (personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md) lo entrega el Operador a su DBA; si ves algun criterio de aceptacion que quieras endurecer, dilo."
---

# ACTION - BR-C4 resuelto: opcion (b), DBA comprometido, encargo redactado

El Operador resolvio el ultimo item del paquete DEC P3.x: **opcion (b)** -- tiene DBA y compromete el
sembrado de BR-C4 (matriz de autorizacion por operacion) en `DbsFinanciero_SANDBOX` antes del 29-jul, para
preservar la elegibilidad de P3.2/P3.3/P3.4 al pool Q4 (n=10).

## Por que (b) es limpia para el estudio
- Es la EJECUCION de una condicion ya sellada (s.3: "P3.2/P3.3/P3.4 elegibles Q4 SI su DEC cierra al sello
  Etapa 2"), no una decision de dominio nueva ni una adicion post-hoc de unidades.
- Es HARDENING (el DBA crea la capacidad; el dev gobernado la cablea en Sprint 1; el dev no crea los procs).
  Simetrico para ambos brazos -> no contamina el contraste.
- Decidida AHORA (antes de datos de Sprint 1) -> pre-registro limpio. Red de seguridad: auto-fallback a n=7.

## Tu parte (gobernanza)
1. Marca P3.2/P3.3/P3.4 como elegibilidad Q4 CONDICIONAL con deadline 29-jul.
2. Al entregar el DBA (verificado, ver criterios del encargo del Asesor): registra la enmienda fechada del
   sello + confirma n=10.
3. Si el 29-jul pasa sin entrega verificada: ejecuta la caida sellada -> n=7 (opcion a).

## Encargo del DBA
Redactado por el Asesor (espejo del encargo PAR-2 s.24): `personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md`
(matriz documento x operacion, guardas THROW con rango sugerido 50300-50319 para evitar colision, smoke
falsable de separacion emitir/aprobar/anular con 3 identidades, grant de verificacion, guard de entorno
sandbox). El Operador lo entrega a su DBA. Fuente de dominio (nombres de tabla/procs/roles) la completan
Operador+DBA.

-- Operador
