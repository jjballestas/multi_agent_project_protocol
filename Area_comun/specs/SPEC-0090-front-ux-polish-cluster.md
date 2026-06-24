# SPEC-0090 - Front UX polish cluster (navegacion, busqueda, KPIs, chips, mailbox, intake)

- **Estado:** draft (registrada en el ledger; pendiente GO ejecutado a Codex). Maker: Codex. Checker: Arquitecto.
- **Fecha:** 2026-06-24. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen (REQ del operador, extraction TASK-EXTRACT del backlog del panel):** REQ-11A2A57C (hash routing),
  REQ-07DD94CE (busqueda Artifacts), REQ-16BDAA88 (descripcion inline en Operate), REQ-524372E9 (KPIs
  contextuales), REQ-A4B9FE80 (chips Backlog), REQ-CD4CE3F1 (agrupacion Mailbox), REQ-7857CDE9 (modal Intake).
- **Relacionada:** SPEC-0086 (front MVP; AC11 badge-honesto, AC12 routing-comportamiento, AC13
  conformidad-diseno -- PERMANENTES, condicion de cierre del operador), DECISION-0050 (front=panel del operador).

## Objetivo

Pulir la capa de presentacion del panel para uso diario del operador, SIN agregar capacidades de escritura ni
tocar la atestacion. Todo es read-side / presentacion sobre el estado ya cargado (observe/mailbox/ledger): mejor
navegacion (URL), busqueda y filtros, jerarquia visual (chips, KPIs contextuales), y formularios legibles. Cero
nuevas rutas de escritura de estado; cero cambios al config atestado; #4 byte-identica.

## Alcance / Out of scope

- En alcance: las 7 mejoras UX abajo (AC1-AC7), todas sobre vistas/datos existentes.
- Fuera de alcance: cualquier nueva accion gobernada o ruta de escritura, cambios al submit_intent, al roster, al
  #4 o al config pinned; logica de negocio; multi-tenant. La navegacion y los filtros NO mutan estado.

## acceptance_criteria

- **AC1 - Routing por hash URL (REQ-11A2A57C, RF-1..RF-14).** Click en un item de la sidebar cambia la URL a
  `/#<vista>` sin recargar; cargar con un hash valido (ej `/#mailbox`) activa esa vista directamente; Atras/Adelante
  del navegador navegan correctamente (popstate/hashchange); hash invalido cae a la vista por defecto (fail-safe,
  no pantalla vacia). Construye sobre el view-routing existente (showView), NO lo reemplaza; AC12 (routing-
  comportamiento) sigue verde. Behavior-test: hash inicial -> vista; cambio de hash -> vista; hash invalido ->
  default.
- **AC2 - Busqueda por texto en Artifacts (REQ-07DD94CE, RF-3).** Campo de busqueda que filtra en vivo (sin Enter,
  case-insensitive) por ID o nombre; borrar restaura todos; placeholder indicativo; el contador refleja los items
  visibles tras filtrar. Behavior-test: texto -> subset por substring case-insensitive; vacio -> set completo.
- **AC3 - Descripcion inline en acciones de Operate (REQ-16BDAA88, RF-5..RF-10).** Cada tarjeta de accion
  gobernada muestra una descripcion estatica de una linea (<=80 chars) debajo del titulo y encima del tipo de
  intent, en lenguaje del operador (no el nombre tecnico del intent), visible siempre (sin hover). Behavior-test:
  cada accion expone una descripcion no vacia, <=80 chars, distinta del id/tipo de intent.
- **AC4 - KPIs de cabecera contextuales (REQ-524372E9).** En Mailbox, el KPI Open Mailbox lleva acento (fondo/
  borde) cuando su valor > 0; en Backlog, igual para Open Tasks; en Help/Projects los KPIs van en modo compacto
  (no accionables). El acento es DERIVADO del valor real, no estatico. Behavior-test: valor>0 -> clase de acento;
  valor 0 -> sin acento; vista no-accionable -> modo compacto.
- **AC5 - Chips de estado y prioridad en Backlog (REQ-A4B9FE80, RF-1).** Las tarjetas del kanban muestran un chip
  de prioridad con color diferenciado (high acento calido, normal neutro) y color de estado semantico consistente
  con los badges de la barra de integridad (tokens del design-system, no colores ad-hoc); high lleva marca visual
  (borde/realce). Behavior-test: priority high -> clase chip-high + marca; normal -> chip-normal; estado -> clase
  semantica esperada.
- **AC6 - Agrupacion temporal y filtros en Mailbox (REQ-CD4CE3F1, RF-2).** answered/archived se agrupan bajo
  encabezados de fecha colapsables con contador por grupo; el periodo actual (hoy/esta semana) inicia expandido;
  el filtro por direccion (from/to) muestra solo esos mensajes. Solo presentacion: NO cambia el estado del mailbox
  ni archiva. Behavior-test: mensajes datados -> grupos correctos con contador; filtro direccion -> subset.
- **AC7 - Modal fullscreen para nueva historia/requisito en Intake (REQ-7857CDE9, RF-14).** El formulario de nueva
  historia abre en un modal que ocupa >=80% del viewport; las textareas de Narrativa e Intencion (rows>=8) se ven
  completas sin scroll interno; el wizard de 4 pasos y los botones Preview dry_run / EXECUTE submit_intent son
  visibles sin scrollear el modal; confirmar o cancelar cierra el modal y restaura el foco. El flujo gobernado de
  Intake (RF-14, submit_intent, sin preview-as-green) NO cambia: solo su contenedor visual. Behavior-test: el modal
  expone el wizard de 4 pasos + ambos botones; cancelar cierra sin enviar.

## Carries permanentes (condicion de cierre del operador, SPEC-0086)

- **AC11 badge-honesto:** cualquier indicador de integridad/estado sigue DERIVADO de la verificacion real, nunca
  verde estatico. Ninguna mejora visual introduce un verde hardcodeado.
- **AC12 routing-comportamiento:** la navegacion sigue siendo routing real (toggle de vistas), no scroll; AC1 lo
  extiende con URL, no lo degrada.
- **AC13 conformidad-de-diseno:** todo usa tokens del design-system de Zeus-protocol/design/ (sin colores/espaciados
  ad-hoc); fidelidad al diseno citada por el commit de design-system vigente.

## DoD

- AC1-AC7 verdes con behavior-tests deterministas; AC11/AC12/AC13 permanentes verdes; carry AC16/AC17/AC58/AC72.
- node --test clon limpio exit 0; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4
  byte-identica (no toca protocol.config.json ni el ledger). PII: cualquier texto libre renderizado sigue redactado
  (safePayloadPreview), export PII-free.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. Sin nueva ruta de escritura de estado:
  prueba negativa de que ninguna mejora UX (busqueda, agrupacion, modal, routing) emite submit_intent ni muta
  mailbox/ledger.

## Notas de diseno

- Todo opera sobre el modelo ya cargado en el cliente; busqueda/filtros/agrupacion son puramente de vista. El
  routing por hash es la unica integracion con el navegador (history/popstate); debe ser fail-safe a la vista por
  defecto y no romper el deep-link.
- Insumos de diseno: Zeus-protocol/design/ (design-system + componentes dashboard/kanban/timeline/claims-table/
  badges). Citar el commit de design-system vigente en la entrega.
- Si el operador prefiere fraccionar, AC1-AC4 (navegacion+busqueda+KPIs+inline) y AC5-AC7 (chips+mailbox+modal) son
  dos lotes independientes; por defecto se entregan como una sola tarea (todas presentacion, bajo riesgo).
