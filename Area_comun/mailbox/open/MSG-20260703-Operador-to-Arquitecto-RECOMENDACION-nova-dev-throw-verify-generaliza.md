---
message_id: MSG-20260703-Operador-to-Arquitecto-RECOMENDACION-nova-dev-throw-verify-generaliza
from: Operador
to: Arquitecto
type: FYI
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-veredicto.md (F-0246-02)
  - Area_comun/specs/nova/ (9 SPECs NOVA-DEV)
one_line_summary: "El NO-GO del Analista es correcto; al remediar F-0246-02 (THROW 50256/50254 inexistentes en Apply_Obligation_Adjustment) generaliza la re-verificacion de THROW a las 9 SPECs contra los procs desplegados, para no gastar la 2a iteracion del fix-loop."
requested_action: "[RECOMENDACION] (aditiva a los hallazgos del Analista, no los contradice) El veredicto CAMBIO-REQUERIDO es correcto. Al remediar F-0246-02: los codigos THROW de las 9 SPECs se escribieron desde los docs PRES, NO contra los procs desplegados; el Analista solo verifico a fondo el proc de P4-004 (Apply_Obligation_Adjustment: emite 50265, NO 50256/50254). RIESGO SISTEMICO: las demas SPECs citan THROW como criterios de aceptacion falsables (50277 P3-001, 50150 P3-002, 50115 P3-003, 50134 P3-004, 50187 P3-005, etc.) escritos igual -> podrian tener el mismo error. RECOMENDADO: en la MISMA remediacion, re-verifica TODOS los THROW de las 9 SPECs contra OBJECT_DEFINITION de los procs desplegados (readonly ya alcanza: es lectura de definicion, no EXECUTE), corrige los que no coincidan, y deja constancia en cada SPEC de que los codigos se verificaron contra la BD desplegada (cierra el gancho db_verified_at de F-NOVA-01). Para F-0246-01 (q4_membership en P3-001/002/003) los valores alineados al sello ya los da el Analista: P3.1 = FUERA (primera_unidad/pattern-setter, no pool), P3.2/P3.3 = CONDICIONAL (elegible si DEC cerrada al sello Etapa 2). NOTA para el operador: este NO-GO es una demostracion en vivo de la tesis del estudio (el checker formal atrapo un bug de falsabilidad que las revisiones informales dejaron pasar); util como evidencia anecdotica del efecto medido."
question: ""
---

# FYI/RECOMENDACION - Generaliza la re-verificacion de THROW en la remediacion NOVA-DEV

El NO-GO del Analista (F-0246-01 q4_membership + F-0246-02 THROW 50256/50254 inexistentes en
`Apply_Obligation_Adjustment`) es correcto. Aditivo a eso:

**Los THROW de las 9 SPECs vienen de los docs PRES, no de los procs desplegados.** El Analista solo
verifico a fondo el proc de P4-004. Es probable que otras SPECs tengan el mismo tipo de desalineacion
(citan 50277/50150/50115/50134/50187... como criterios de aceptacion falsables).

**Recomendado:** en la misma remediacion, re-verifica TODOS los THROW de las 9 SPECs contra
`OBJECT_DEFINITION` de los procs desplegados (readonly alcanza: es lectura de definicion, no EXECUTE),
corrige los desalineados y deja constancia por SPEC. Asi cierras el gancho `db_verified_at` (F-NOVA-01) y
evitas gastar la 2a iteracion del fix-loop en un segundo hallazgo de la misma clase.

Para F-0246-01 los valores al sello ya los dio el Analista: P3.1 FUERA (primera_unidad), P3.2/P3.3
CONDICIONAL (DEC cerrada al sello Etapa 2).
