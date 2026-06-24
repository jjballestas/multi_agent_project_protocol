# SPEC-0092 - Front: rediseno de la seccion Intake (cluster RC-01..RC-06)

- **Estado:** draft (registrada en el ledger; pendiente GO ejecutado a Codex). Maker: Codex. Checker: Arquitecto
  + **pasada del Analista** (fronteras: sin nueva ruta de escritura; gate de PII intacto en la aprobacion de
  candidatas; file-intake off-by-default).
- **Fecha:** 2026-06-24. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen (REQ del operador):** REQ-EE0CA804 (RC-01), REQ-3F85B44C (RC-02), REQ-E0606D12 (RC-03), REQ-1C7B4275
  (RC-04), REQ-E6B404D5 (RC-05), REQ-01193FD6 (RC-06). (RC-03/RC-04 con un duplicado cada uno: REQ-FA303A81,
  REQ-B6146E35.)
- **Relacionada:** SPEC-0086 (front MVP; RF-14 Intake; AC17 no-bypass / AC72 error amable), SPEC-0090 (UX polish;
  AC7 modal Intake -- RC-03 lo refina), DECISION-0040 (PII gate), DECISION-0050 (front=panel). Insumo de diseno:
  Zeus-protocol/design/interface/intake_design_brief.md + components/intake.

## Objetivo

Rediseno cohesivo de la seccion **Intake** del panel: pasar de controles/listas inline a un **header con barra de
control unificada** + **dashboard de 4 carpetas** + **modales** (entrada Manual, carga por Archivo, revision de
candidata). Es **presentacion/reorganizacion**: el flujo gobernado de Intake (RF-14, `submit_intent`), el gate de
PII de candidatas y el off-by-default de la carga por archivo **NO cambian**.

## Alcance / Out of scope

- En alcance: RC-01..RC-06 (abajo), todo sobre las vistas/datos existentes del Intake y la carga por archivo v2.
- Fuera de alcance: cambiar el camino gobernado (`submit_intent`), el detector/gate de PII, la habilitacion del
  extractor (off-by-default), o cualquier logica de negocio; ninguna nueva ruta de escritura de estado.

## acceptance_criteria

- **AC1 (RC-01) - Barra de control unificada en el header.** El header de Intake muestra en una fila: badge RF-14,
  titulo+subtitulo, selector de Modo (radios Manual/Archivo con su label contiguo), boton "Nueva historia" y
  Refresh. Behavior-test: el header expone los controles esperados en una fila; cada radio inmediatamente antes de
  su label.
- **AC2 (RC-02) - Dashboard de 4 carpetas.** La vista principal del Intake muestra 4 carpetas en grid: Pendientes
  aprobacion (badge rojo + conteo), Borrador (azul), En Preview (amarillo), Aprobados (verde); cada una con icono +
  nombre + descripcion + badge de conteo DERIVADO del estado real. Behavior-test: 4 carpetas con sus badges; el
  conteo refleja el modelo real, no estatico.
- **AC3 (RC-03) - Modal modo Manual (nuevo requisito).** El modo Manual abre un modal con: barra de modo (radios
  contiguos), grid 2 columnas proyecto/titulo, narrativa e intencion full-width, footer con meta del firmante +
  Cancelar/Preview. El flujo gobernado RF-14 (preview dry_run -> confirm -> submit_intent) NO cambia: solo su
  layout. Behavior-test: el modal expone el form + Preview/Cancelar; el submit sigue siendo el gobernado.
- **AC4 (RC-04) - Modal revision de candidata (prellenado).** Para una candidata de archivo, un modal titulado
  "Revisar requisito REQ-..." con el radio Archivo bloqueado + chip "modo bloqueado / revision de candidata";
  campos (proyecto, titulo, narrativa, intencion) **prellenados desde la candidata**; tras un Submit exitoso la
  tarjeta pasa a Aprobado. **El gate de PII se PRESERVA**: no se puede aprobar sin la revision/declaracion de PII
  existente; la aprobacion sigue yendo por el intake gobernado. Behavior-test: el modal prellena desde la
  candidata; aprobar exige el gate de PII y va por submit_intent (sin ruta directa).
- **AC5 (RC-05) - Modal de carga por archivo (solo uploader).** El modo Archivo abre un modal con SOLO: zona de
  drop (formatos aceptados), estado procesando (amarillo), estado OK (verde con nombre + cantidad de candidatas),
  error (rojo con descripcion), boton Aceptar SOLO en estado OK. Al Aceptar, el modal cierra y las candidatas
  aparecen en la carpeta Pendientes. Off-by-default del extractor INTACTO. Behavior-test: el modal expone uploader
  + estados; Aceptar solo habilitado en OK; candidatas -> Pendientes.
- **AC6 (RC-06) - Limpieza de la vista standalone de extraccion.** En la vista de extraccion por archivo: NO
  radios de modo, NO listado de candidatas inline; solo uploader + estados de procesamiento; las candidatas
  aparecen en la carpeta Pendientes (RC-02) tras completar. Behavior-test: la vista no expone radios de modo ni
  lista inline de candidatas.

## Fronteras (carry + prueba negativa)

- **AC17 no-bypass:** ninguna pieza del rediseno crea una nueva ruta de escritura de estado; toda escritura sigue
  por `submit_intent` / el intake gobernado. Prueba negativa: el rediseno no agrega emisores de submit_intent
  nuevos ni rutas directas al ledger.
- **PII:** el gate de PII de candidatas se preserva (no aprobar sin declaracion); texto libre redactado
  (export PII-free). El extractor sigue off-by-default.
- **AC11 badge-honesto / AC12 routing / AC13 conformidad-de-diseno** (tokens del design-system; insumo design/
  interface/intake_design_brief.md + components/intake).

## DoD

- AC1-AC6 verdes con behavior-tests deterministas; fronteras (no-bypass, PII gate, off-by-default) verdes;
  AC11/AC12/AC13 verdes. node --test clon limpio exit 0; validate con/sin secretos exit 0; drift 0;
  neutralidad+encoding 0; #4 byte-identica.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. **PASADA DEL ANALISTA** (foco:
  sin nueva ruta de escritura; gate de PII intacto en la aprobacion de candidatas; off-by-default; no se filtra
  PII en el prellenado del modal de revision).
- REPRO: header con barra unificada; dashboard de 4 carpetas con conteos reales; modal Manual con form gobernado;
  modal de archivo solo uploader (candidatas -> Pendientes); modal de revision prellenado que aprueba via intake
  gobernado con gate de PII; la vista de extraccion sin radios ni lista inline.

## Notas de diseno

- Reusar el design-system y los componentes de design/interface/components/intake (wizard, estados, lista) y la
  barra de integridad persistente. Si se prefiere fraccionar: lote A (RC-01/02/03 layout+manual) y lote B
  (RC-04/05/06 flujo de archivo); por defecto una sola entrega cohesiva (evita estados intermedios inconsistentes).
- RC-03 refina el modal AC7 de SPEC-0090 (no lo reimplementa).
