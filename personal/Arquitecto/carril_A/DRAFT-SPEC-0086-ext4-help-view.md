# DRAFT - Extension 4 de SPEC-0086: vista Help (manual de metodologia + consola) [RF-14/UX]

> DRAFT en personal/Arquitecto; NO promovido. Triage del REQ-FB27AF72 (semilla del operador, intake).
> UX READ-ONLY: NO nueva superficie de escritura -> EXTENSION de SPEC-0086, SIN DECISION.
> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol.

## Origen (REQ-FB27AF72, author=Operador)
OJO: el TITULO de la semilla viene MANGLEADO ("arrancamos con nova.budget:") por el bug de campos-stale que
arreglo TASK-0135 (#1). El intent REAL se re-deriva de la NARRATIVA:
"Como cualquier usuario del front (no solo el operador experto), quiero una opcion Help en el menu que
muestre ayuda DETALLADA de como funciona la metodologia y como usar la consola, para entender y operar sin
conocimiento previo." (intencion de aceptacion: item Help navegable que cubre observar-vs-operar,
submit_intent escritor-unico, dry_run-vs-execute, atestacion #4, las vistas, el intake, el pipeline SDD y un
glosario; reusa docs/MANUAL-operador.md como fuente; honesto a lo que la app HACE hoy incl. limitaciones;
read-only; conforme al design-system).

## AC23 (NUEVO) - Vista Help: guia navegable de metodologia y consola, read-only, honesta [comportamiento PERMANENTE]
- **Nav item Help** presente en la barra de navegacion; al activarlo, el ROUTING muestra SOLO el panel Help y
  oculta el resto (hereda AC12: NAV_VIEWS incluye "help" 1:1 con su panel; nada de scroll-unico). Fallback de
  vista desconocida intacto.
- **Contenido detallado y navegable** sobre: que es la consola; observar vs operar; `submit_intent` como
  ESCRITOR UNICO del ledger; dry_run vs execute/confirmacion; atestacion #4 (cadena/firmas/anclaje); las
  vistas del front; el intake gobernado de requisitos (RF-14); el pipeline SDD; y un GLOSARIO. Con navegacion
  interna (secciones/indice) para un usuario sin conocimiento previo.
- **Fuente unica = `docs/MANUAL-operador.md`**: el contenido se REUSA de ese manual (no se duplica una segunda
  copia que pueda divergir). El manual es la fuente de verdad del texto.
- **Honestidad (hereda AC11):** la vista refleja lo que la app HACE HOY, incluidas sus limitaciones; NO
  documenta capacidades que no existen (p.ej. no afirma multi-tenant, ni features gateadas/diferidas como si
  estuvieran activas). Si una seccion describe algo no implementado, lo marca como pendiente/fuera-de-alcance.
- **Read-only:** la vista Help NO escribe estado ni ledger; NO agrega superficie de escritura (no toca
  submit_intent, no hay botones de accion). Extiende la prueba negativa de no-bypass (AC17) por construccion.
- **Conforme al design-system (hereda AC13):** dark-first, tokens del design-system, tipografia y layout
  coherentes con las demas vistas; la vista EXISTE y es navegable.

## test_plan (anadido)
- **Comportamiento de routing (Zeus, permanente):** "help" en NAV_VIEWS; activar Help -> solo el panel help
  visible, los demas hidden; vista desconocida -> fallback DEFAULT_VIEW (extiende el test AC12 existente).
- **Contenido/fuente (Zeus):** el render del Help deriva su contenido de `docs/MANUAL-operador.md` (single
  source; un test asegura que el panel NO es un placeholder vacio y que cubre las secciones clave/glosario).
- **No-bypass (Zeus):** asertar que la vista Help no expone ninguna superficie de escritura (sin botones de
  accion / sin llamadas a /actions/submit desde el panel help).
- **Conformidad de diseno (AC13):** contra el design-system (tokens/tipografia); la vista existe y navega.

## Carry permanentes
AC11 (honestidad) / AC12 (routing) / AC13 (conformidad-diseno) / AC17 (no-bypass) verdes. SIN cambio de
superficie de escritura (no aplica AC18/19/20). #4 epoca 1.14.0 byte-identica (no toca ledger/config/keys).
Gates: validate exit 0 con/sin secretos, drift 0, npm test verde, neutralidad/encoding 0.
