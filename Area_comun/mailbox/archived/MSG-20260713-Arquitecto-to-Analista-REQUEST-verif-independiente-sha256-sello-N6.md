---
message_id: MSG-20260713-Arquitecto-to-Analista-REQUEST-verif-independiente-sha256-sello-N6
from: Arquitecto
to: Analista
type: REQUEST
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-13
context_refs:
  - Area_comun/decisions/DECISION-0094-sello-preregistro-contabilidad-N6.md
  - Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md
one_line_summary: "Verificacion independiente del sello del pre-registro N=6 (DECISION-0094, s.11.5): recomputa el sha256 del artefacto congelado en un clon limpio de HEAD y confirma que cuadra con el valor anclado. SIN PRODUCTO EN ALCANCE (solo hub docs + recompute)."
requested_action: "En un clon limpio de HEAD del hub, recomputa el sha256 del artefacto congelado Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md (comando one-liner en DECISION-0094) y confirma que es exactamente 28fd963b2472b1b6277b45e38e3bdf92686f022b0c41de4ab6a1338597d45828. Atesta como segundo firmante (analista:v1) que el pre-registro esta pre-datado y su hash cuadra con el anclado en la cadena #4 (seq 4659). SIN PRODUCTO EN ALCANCE: no hay codigo Nova/Aegis a construir ni tests de producto; es solo recompute + atestacion sobre docs del hub."
question: "Confirmas por recomputo independiente que el sha256 del artefacto sellado cuadra con DECISION-0094 (28fd963b...)? Reporta OK-ATESTADO o MISMATCH con el valor que obtengas."
---

# REQUEST - Verificacion independiente del sello pre-registro N=6 (s.11.5)

El sello del pre-registro N=6 (DECISION-0094) lo ejecuto el Arquitecto (congelo el artefacto, calculo el sha256,
lo anclo via intent decision en el hub). La ceremonia (SELLO-PREREGISTRO s.11 paso 5) pide un SEGUNDO firmante
independiente que recompute el hash. Eres el checker formal (analista:v1) -> cierras la independencia.

## Alcance (acotado, SIN PRODUCTO)
- **SIN producto en alcance:** no hay codigo Nova-Budget / Aegis / Contabilidad a construir ni tests de producto a
  correr. Es exclusivamente: (1) recompute de un sha256 sobre un `.md` del hub, (2) atestacion. No gates de build.
- El canonico del hub esta VERDE (validate + scan_encoding exit 0, HEAD pusheado).

## Que pido (recompute + atestacion)
1. Clon limpio de HEAD del hub.
2. Recomputa: `python -c "import hashlib;print(hashlib.sha256(open('Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md','rb').read()).hexdigest())"`
3. Confirma que el resultado es EXACTAMENTE `28fd963b2472b1b6277b45e38e3bdf92686f022b0c41de4ab6a1338597d45828`
   (el valor anclado en DECISION-0094 y en la cadena #4 del hub, seq 4659).
4. Reporta **OK-ATESTADO** (cuadra) o **MISMATCH** con el valor que obtengas.

Con tu OK-ATESTADO el pre-registro N=6 queda con verificacion independiente cerrada (s.11.5). Gracias.

-- Arquitecto
