# Informe adversarial - Paquete NOVA-DEV (Ingenas) [TASK-0246, parte 1/2]

> Revision del Arquitecto sobre el paquete construido por el Operador en
> `D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/` (fuera del hub, solo lectura). Alcance acotado al
> brazo GOBERNADO (miembros gobernados de pares, familia P3, pool Q4, BR-C4); NO se leyeron fuentes de
> las unidades BASELINE del estudio. Mejoras al NOVA_PROMPT se PROPONEN aqui; las aplica el Operador fuera
> del hub (no se edita el paquete Ingenas desde este informe).

## 1. Inventario verificado

- Raiz: `NOVA_Apendice_Estructura_DotNet10_Dominios.html`, `NOVA_Architecture_ExperienciasGH.{html,md}`,
  `NOVA_Arquitectura_y_Estandar_Desarrollo.html`, `TEMP_Guia_Modelos_Peones_y_Medicion.md`.
- `NOVA_Budget_Process/`: `NOVA_PRES_00_Pipeline_Proceso_Presupuestal.html` (maestro, v1.6, "serie completa
  13/13") + `NOVA_PRES_01..12` (Parametrizacion, Presupuesto_Inicial, Modificaciones, CDP, Compromiso,
  Obligacion, Pago_Egreso, Reversos_Anulaciones, Cierre_Vigencia, PAC_Ingresos, Ejecucion_Consultas,
  Reportes_Regulatorios) + `NOVA_PROMPT_Arranque_Agente_Desarrollo.md` + `NOVA_SPEC_Plantilla_Requisitos.md`
  + `NOVA_ESTUDIO_Anexo_Diseno_Completo.json` + `NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md` +
  `NOVA_ESTUDIO_Protocolo_Medicion.md` + `DATA/` (evidencia sandbox: grants, resets, listas de procs/vistas).
- `NOVA_Development_Goal/`: `NOVA_GOAL_Desarrollo_Aplicacion.{md,html}`, `NOVA_GOAL_Verification_Report.md`,
  `README.md`.
- Catalogo RES-000..012 = las 13 secciones de `NOVA_PRES_00` + su detalle en `NOVA_PRES_01..12` (no un
  archivo de catalogo separado). Plantilla NOVA-SPEC-T-001 v1.1 en `NOVA_SPEC_Plantilla_Requisitos.md`
  (nota propia del doc: "v1.0 RECHAZADA por su propio protocolo adversarial, 9 hallazgos, 2 criticos; v1.1
  los corrige" -- disciplina de auto-correccion ya presente en el paquete, buena senal).
- GOAL en `NOVA_Development_Goal/NOVA_GOAL_Desarrollo_Aplicacion.md` (NOVA.sln 6 capas + apps/nova-web, 10
  reglas no negociables, backlog GOAL-P1..P6). Prompt de arranque en `NOVA_PROMPT_Arranque_Agente_Desarrollo.md`,
  que remite en orden GOAL -> arquitectura HTML -> PRES_00 -> PRES-XXX de la tarea -> plantilla SPEC.

## 2. Lo bueno (se conserva, no se toca)

- Serie RES-000..012 completa (13/13), consistente entre si.
- La arquitectura obligatoria (`NOVA_Arquitectura_y_Estandar_Desarrollo.html`,
  `NOVA_Apendice_Estructura_DotNet10_Dominios.html`) es explicita y NO contradice la doctrina del hub:
  React+TS+Vite sin SQL, capas .NET, "sin capa DATABASE generica", DTOs/OpenAPI, cero DataTable entre
  capas, ProblemDetails, OpenTelemetry, SPs controlados como fuente de verdad transaccional.
- `NOVA_Architecture_ExperienciasGH.{html,md}` documenta las lecciones de un sistema legacy real
  (ExperienciasGHv3.1) y usa los nombres de los anti-patrones prohibidos (WebForms/PageMethods, HintPath,
  DataTable, centinelas -99, capa DATABASE generica, secretos en `.config`) EXCLUSIVAMENTE en la columna
  "que NO replicar" -- verificado con grep dirigido, cero aparicion fuera de ese contexto. Es la fuente
  correcta de por-que existen esas prohibiciones, no una contradiccion.
- El propio paquete se auto-declara honesto sobre sus huecos: RES-010 (PAC/ingresos) se marca "brecha de
  modelo" y RES-012 (reportes regulatorios) declara "catalogos listos, generadores por construir" -- no
  finge cobertura que no tiene.

## 3. Mapeo RES -> SPEC (contra `Area_comun/specs/nova/`, 12 SPECs existentes al momento de este informe)

| RES | Cobertura | Estado |
|---|---|---|
| RES-000 (pipeline maestro) | documento marco, no ejecutable | sin gap (no aplica SPEC) |
| RES-001 (Parametrizacion) | P2-002 | cubierto |
| RES-002 (Presupuesto inicial) | P2-001 (lectura) + P3-001 (escritura) | cubierto |
| RES-003 (Modificaciones) | P4-001 | cubierto |
| RES-004 (CDP) | P3-002 + P4-002 + P4-005 | cubierto |
| RES-005 (Compromiso) | P3-003 + P4-003 + P4-006 | cubierto |
| RES-006 (Obligacion) | P3-004 + P4-004 | cubierto para draft/ajuste; **SIN SPEC de anulacion de Obligacion** |
| RES-007 (Pago) | P3-005 | cubierto para draft; **SIN SPEC de ajuste/anulacion de Pago** |
| RES-008 (Reversos/anulaciones) | P4-005/P4-006 cubren CDP/Compromiso | **SIN SPEC de la cascada Pago->Radicacion->Obligacion** |
| RES-009 (Cierre de vigencia) | ninguna | **gap, ya declarado por el propio paquete** |
| RES-010 (PAC/ingresos) | ninguna | **gap, ya declarado "brecha de modelo" por el paquete** |
| RES-011 (Ejecucion/consultas/libros) | P2-001 + P2-004 (listados) | parcial: libros oficiales sin SPEC |
| RES-012 (Reportes regulatorios) | ninguna | **gap, ya declarado "por construir" por el paquete** |
| transversal | P6-003 (OpenTelemetry) + F3.3 (instrumentacion) | requisitos de arquitectura, no de RES especifico |

**Nota de alcance (no una omision):** los gaps de RES-006-anulacion/RES-007/RES-008-cascada/RES-009/RES-010/
RES-011-libros/RES-012 caen FUERA del alcance acotado de TASK-0246 (`Alcance acotado`: miembros gobernados
de pares + familia P3 + pool Q4 declarado de 10 unidades + BR-C4). Ninguno de estos RES esta en el pool Q4
sellado (s.5 del sello) ni es miembro de un par ya sorteado. Escribir SPECs especulativas para ellos
violaria "no redefine alcances de unidades selladas (cambios = enmienda fechada via Operador)". Se dejan
registrados aqui como backlog FUTURO explicito (post-Sprint-1 o enmienda), no como trabajo pendiente de
esta tarea.

## 4. Contradicciones con la doctrina/arquitectura obligatoria

Ninguna encontrada en el material revisado (grep dirigido a WebForms/PageMethods/HintPath/DataTable/
centinelas -99/capa DATABASE generica/secretos en `.config`: todas las apariciones estan en el documento de
lecciones legacy, en la columna "que evitar", nunca en una recomendacion positiva).

## 5. Mejoras propuestas al NOVA_PROMPT (el Operador decide si aplicarlas; NO se editan aqui)

1. **Bakear el guard de procedencia en el prompt de arranque, no solo en cada SPEC.** El mismo defecto
   (mock/Recording* in-memory disfrazado de evidencia SQL real) fue cazado 2 veces en unidades distintas
   del estudio (TASK-0250, TASK-0253) antes de adoptarse como regla dura. Si el `NOVA_PROMPT_Arranque_
   Agente_Desarrollo.md` incluyera la regla explicita ("el harness de evidencia F-NOVA-01 SIEMPRE usa una
   clase SQL real, gateada por env vars, NUNCA un mock/Recording* con resultados hardcodeados") desde el
   arranque, se evitaria depender de que el checker lo cace despues del hecho en cada unidad nueva.
2. **Bakear la re-verificacion F-NOVA-01 contra `OBJECT_DEFINITION` como paso obligatorio del prompt.** En
   3 unidades distintas (P4.1, P4.2, PAR-2/TASK-0255) el set de THROW documentado en la SPEC/PRES difirio
   del realmente desplegado (F-0246-02, ya nombrado como patron recurrente en el propio hub). Si el prompt
   de arranque exige explicitamente "antes de fijar los criterios de aceptacion, RE-CONFIRMA el set de
   THROW contra OBJECT_DEFINITION del proc desplegado, NO asumas el rango documentado en el PRES", se reduce
   la tasa de este hallazgo repetido en las unidades futuras.
3. **Anadir un checklist explicito de campos DoR obligatorios al prompt** (q4_membership, isolation,
   leyo_codigo_hermano, measurement/cache-confound) -- el propio hub registra `F-0246-01: bloqueo P3 por
   omitir q4_membership` como incidente ya ocurrido; una checklist en el prompt de arranque (espejo de la
   que ya usa el Arquitecto al escribir SPECs en el hub) previene la omision en el origen, no solo en el
   gate posterior.

Ninguna de estas 3 propuestas cambia el contrato tecnico ni el alcance del paquete -- son refuerzos de
disciplina de proceso ya validados por incidentes reales de este mismo estudio.

## 6. Conclusion

Paquete SOLIDO, sin contradicciones con la arquitectura obligatoria, con disciplina de auto-critica ya
presente (plantilla v1.1 corrigiendo v1.0, gaps de RES-009/010/012 auto-declarados). Los gaps de cobertura
RES identificados en s.3 son reales pero estan correctamente FUERA del alcance sellado de Sprint 1 -- se
registran como backlog futuro, no como defecto de esta entrega. Las 3 mejoras de proceso (s.5) se proponen
al Operador para aplicar en el paquete Ingenas si lo considera valioso.

---
task_id: TASK-0246
status: informe-adversarial-completo
executive_summary: Revision adversarial del paquete NOVA-DEV completa. Sin contradicciones con la arquitectura obligatoria. Mapeo RES->SPEC confirma cobertura completa del alcance sellado (pares gobernados + P3 + pool Q4 + BR-C4); gaps fuera de alcance (RES-006-anulacion/007/008-cascada/009/010/011-libros/012) registrados como backlog futuro explicito, no defecto. 3 mejoras de proceso propuestas al NOVA_PROMPT (guard de procedencia, F-NOVA-01/OBJECT_DEFINITION, checklist DoR) -- las aplica el Operador.
artifacts: Area_comun/specs/nova/INFORME-ADVERSARIAL-NOVA-DEV-paquete-ingenas-TASK-0246.md; SPECs previamente commiteadas P2-001..004, P3-001..005, P4-001..006, P6-003, F3.3.
gates: N/A (informe de revision, no cambia codigo/estado gobernado).
next_recommended: Rutear a Analista para gate adversarial de este informe (checker-only) antes de cerrar TASK-0246; FYI al Operador con las 3 mejoras de proceso propuestas.
risks: Ninguno -- informe de solo lectura, no toca el core pineado ni el N=500 sellado, no redefine alcances.
