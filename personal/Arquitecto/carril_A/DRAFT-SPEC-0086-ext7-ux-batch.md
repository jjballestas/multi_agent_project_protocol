# DRAFT - Extension 7 de SPEC-0086: batch UX (8 requisitos, read-only) [AC29..AC36]

> DRAFT en personal/Arquitecto; NO promovido. Triage de 8 requisitos UX del operador (PROPOSED, Zeus-protocol).
> Todos READ-ONLY: NO nueva superficie de escritura -> EXTENSIONES de SPEC-0086, SIN DECISION.
> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. Carry permanentes AC11/AC12/AC13. #4 byte-identica.
> Se promueven de a uno (o por bloque) en el orden del PLAN; cada AC con su TASK.

## AC29 - Refetch fresco al navegar (REQ-C1976857) [comportamiento PERMANENTE]
Al activar un nav-item, la vista hace **fetch fresco** al server y actualiza su contenido sin requerir F5: el
Ledger seq, el conteo del Backlog, el Mailbox y la barra de integridad reflejan el canonico ACTUAL. Incluye un
**boton de recarga manual** por seccion y un **refresco por intervalo** configurable (opt-in, default off o N
configurable). Read-only (solo GETs de observe; no toca submit_intent). Test: navegar a una vista dispara el
fetch (mock) y re-renderiza con el dato nuevo; el intervalo configurable se respeta; sin intervalo no hay
polling. Honestidad (AC11): si el fetch falla, estado de error, no datos stale pintados como frescos.

## AC30 - Indicador de frescura + staleness (REQ-547C6C54) [comportamiento PERMANENTE]
La barra de integridad / pie de seccion muestra **"actualizado hace Ns"**; durante una carga, un spinner/
indicador sutil; si el dato es STALE (> N s sin refrescar) el indicador cambia de estado visual. Deriva del
timestamp REAL del ultimo fetch exitoso (no estatico). Test: tras un fetch, el indicador muestra la antiguedad;
pasado el umbral, pasa a STALE; durante carga, muestra el spinner. Construye sobre AC29.

## AC31 - Tooltips en badges de integridad (REQ-4120B017) [comportamiento PERMANENTE]
Hover sobre cada badge (epoch/drift/attested/canonical/validator-exit) muestra un tooltip corto: valor normal,
que significa al cambiar, cuando preocuparse (ej. drift=0 OK, drift>0 atencion). Texto fuente consistente con
el glosario del Help. Test: cada badge expone su tooltip con el contenido esperado; accesible (aria/title).

## AC32 - Tooltips en codigos RF-N y acronimos (REQ-3E31293F) [comportamiento PERMANENTE]
Hover sobre un codigo RF-N (RF-5, RF-14...) o acronimo (SDD/T0/HMAC/PII...) en cualquier vista muestra su
nombre completo; los codigos son interactivos (cursor pointer). El diccionario es **una fuente unica** (compartida
con el glosario del Help, no duplicada). Test: hover sobre RF-5/SDD/HMAC rinde el texto esperado; el set cubre
los codigos que el front realmente muestra.

## AC33 - Render de diagramas Mermaid en Help (REQ-D2C6579F) [comportamiento PERMANENTE]
Los bloques Mermaid de las secciones 4/5/6/7 del Help se renderizan como diagramas (SVG) en vez de texto crudo.
**SIN agregar dependencia de servidor / npm install:** vendorizar la lib como asset estatico servido por el
propio server, o SVG pre-generado; preserva la propiedad "sin dependencias" de la consola. Read-only. Test: el
panel Help no muestra el codigo mermaid crudo de esos bloques; render presente; el server sigue sin deps de npm.

## AC34 - Jerarquia tipografica Mailbox/Backlog (REQ-28118FC3) [conformidad-diseno]
En tarjetas de Mailbox el ASUNTO es prominente y el `MSG-...` secundario (menor tamano/contraste); en Backlog
el TITULO primero y el `REQ-/TASK-id` secundario debajo. Tokens del design-system (AC13). Test (conformidad):
el id tecnico no tiene el mismo peso visual que el asunto/titulo (clases/tokens correctos).

## AC35 - Kanban: colapsar columnas vacias + mostrar done (REQ-B97838C6) [comportamiento PERMANENTE]
Las columnas con count=0 se muestran compactas (solo cabecera, sin hueco); la columna **done MUESTRA su
contenido** (lista o resumen paginado, no solo el numero). El ancho se adapta al contenido real. Test: con una
columna en 0 -> modo compacto; done con N tareas -> renderiza/pagina; no queda done con count pero sin lista.

## AC36 - Filtros + paginacion del Ledger #4 (REQ-9AF54A75) [comportamiento PERMANENTE]
La cabecera del Ledger ofrece filtro por **actor** y por **tipo de evento**; al seleccionar, la lista se reduce
a los que coinciden; **paginacion/carga progresiva** para no renderizar 900+ a la vez. Read-only sobre el ledger
atestado; el texto libre sigue redactado (no afloja PII). Test: filtrar por actor=Codex / tipo=intent.applied
reduce la lista; la paginacion limita el render; sin filtro, pagina por defecto.

## Carry permanentes (todos)
AC11 (honestidad: nada verde/fresco sin verificacion real) / AC12 (routing intacto) / AC13 (conformidad design-
system). READ-ONLY: ninguno toca submit_intent ni abre superficie de escritura (carry AC17). #4 epoca 1.14.0
byte-identica (no toca core/ledger/config). Gates por TASK: validate con/sin secretos exit 0, drift 0, npm test
verde, neutralidad/encoding 0, reproduccion desde clon limpio (maker!=checker).
