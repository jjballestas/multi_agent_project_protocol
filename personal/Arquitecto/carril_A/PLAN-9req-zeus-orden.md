# PLAN / ORDEN - SPECs de los 9 requisitos PROPOSED de Zeus-protocol

> Respuesta al GO del operador (MSG GO-SPECS-ZEUS-PROPOSED). Yo propongo el orden; el operador ratifica.
> Modelo SDD: (DECISION cuando aplica) -> SPEC con AC+test_plan -> TASK (maker=Codex/checker=Arquitecto).

## Clasificacion
- **8 UX aditivos** (read-only, SIN nueva superficie de escritura) -> EXTENSIONES de SPEC-0086, SIN DECISION.
  Carry permanentes AC11 (honestidad) / AC12 (routing) / AC13 (conformidad-diseno). Cada uno: 1 AC nuevo +
  test de comportamiento + su TASK.
- **1 ingestion de archivos** REQ-31100EAF -> superficie de INGRESO NUEVA -> **DECISION-0055 propia** + SPEC ext
  + PASADA DEL ANALISTA (ingestion/egress) al cierre; nace OFF/gateada y reversible por flag.

## Orden de ejecucion propuesto (de menor a mayor riesgo; agrupado por afinidad y dependencias)

### Bloque A - frescura de datos (fundacional; 547 depende de 197)
1. **REQ-C1976857** -> AC29: refetch fresco al navegar a cada vista (sin F5); boton de recarga manual; refresco
   por intervalo configurable opcional. Fundacional: muchas vistas se benefician.
2. **REQ-547C6C54** -> AC30: indicador "actualizado hace Ns" + spinner durante carga + estado STALE (>N s).
   Construye sobre AC29.

### Bloque B - comprension / tooltips (UI pura, riesgo minimo)
3. **REQ-4120B017** -> AC31: tooltips en los badges de la barra de integridad (epoch/drift/attested/canonical/
   validator): que es normal, que significa cuando cambia, cuando preocuparse.
4. **REQ-3E31293F** -> AC32: tooltips en codigos RF-N y acronimos (SDD/T0/HMAC/PII...) en todas las vistas;
   interactivos (cursor pointer). Fuente del glosario = el mismo manual/Help (consistencia).
5. **REQ-D2C6579F** -> AC33: renderizar los bloques Mermaid del Help como diagramas (SVG), SIN agregar una
   dependencia de servidor / npm install (vendorizar la lib como asset estatico, o SVG pre-generado). Honra la
   propiedad "sin dependencias" de la consola. Mejora el Help recien actualizado.

### Bloque C - densidad / layout (UI, riesgo bajo)
6. **REQ-28118FC3** -> AC34: jerarquia tipografica en Mailbox/Backlog (asunto/titulo prominente; ID tecnico
   secundario). Tokens del design-system.
7. **REQ-B97838C6** -> AC35: kanban colapsa columnas con count=0 (modo compacto) + la columna done MUESTRA su
   contenido (lista o resumen paginado).
8. **REQ-9AF54A75** -> AC36: filtros del Ledger #4 por actor y por tipo de evento + paginacion/carga progresiva
   (no renderizar 900+ a la vez). Algo mas de logica que el resto del bloque.

### Bloque D - ingestion (LO MAS SENSIBLE; va al final)
9. **REQ-31100EAF** -> DECISION-0055 + AC37 (ingestion gobernada acotada) + AC38 (anti-abuso de ingestion,
   prueba negativa permanente). OFF/gateada, reversible por flag; PASADA DEL ANALISTA al cierre.

## Notas transversales
- Cada UX: prueba de COMPORTAMIENTO permanente; read-only (no toca submit_intent / no nueva superficie de
  escritura); conforme al design-system (AC13); #4 epoca 1.14.0 byte-identica (no toca core/ledger).
- Promocion gobernada de a una (o por bloque) tras ratificacion: SPEC-0086 gana el AC + se promueve la TASK
  (maker=Codex/checker=Arquitecto), gates validate con/sin secretos exit 0 + npm test verde + neutralidad 0.
- REQ-31100EAF NO se enciende vivo sin GO posterior del operador (mirror connector s9 / auto-push).
