---
message_id: MSG-20260703-Operador-to-Arquitecto-DIRECTIVA-redacta-decision-nombres-aegis
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md (usa "Aegis" como nombre de instancia)
  - Area_comun/decisions/DECISION-0061-skills-registry-coldstart-loader.md (loader de skills)
  - protocol.config.json (project_name, linea 5, genesis-bound)
one_line_summary: "El Operador decidio nombrar la METODOLOGIA 'Aegis' (marca), en modo MARCA-SOLO (sin tocar la config genesis-bound). Redacta la DECISION formal de nombres que fija la familia + el namespace de skills 'aegis:' via loader, y difiere la i18n a Carril B. Cerradas las 2 DIRECTIVAs previas (DD horneadas 01f05db + pipeline al dia 2320acd), este es el siguiente paso acordado."
requested_action: "[DIRECTIVA] Redacta y registra una DECISION de nombres (naming/governance) que formalice lo que el Operador decidio tras debate. FAMILIA DE NOMBRES: (1) **Aegis** = MARCA de la METODOLOGIA (palabra neutra -- un escudo, sin termino de dominio; NO rompe la neutralidad); es el nombre citable para publicar. (2) Instancia por proyecto = carpeta/repo **`aegis/`** (convencion reconocible tipo `.git`/`node_modules`: el nombre se repite en cada proyecto y significa 'la capa Aegis aplicada aqui'; NO es ambiguo). Ya existe `NOVA/Aegis`. (3) Producto/front = **Zeus-Aegis**; productos de dominio = **Nova-X** (Nova-Budget/Treasury/...). (4) Hub = **'Aegis-core'** (la fuente canonica de la metodologia). Convencion de habla para desambiguar: 'Aegis-core/hub' = la fuente vs 'la instancia aegis de <proyecto>'. MECANISMO PARA SKILLS: el prefijo visible en el CLI (`aegis:mailbox-hygiene`, como `anthropic-skills:docx`) se logra por NAMESPACING via el loader de skills (DECISION-0061), NO renombrando archivo por archivo. Define en la DECISION el detalle de resolucion del loader cuando coexistan skills `aegis:` del hub y locales de la instancia (la mas especifica gana o sub-namespace). SCRIPTS: NO se tocan (no se ven como skills en el CLI; costo/riesgo alto por CI/crons/verification_cmd/cadena #4; atribucion via encabezado o nombre de directorio si acaso). ALCANCE = MARCA-SOLO (OPCION i, confirmada por el Operador): NO se toca `project_name` en protocol.config.json (esta genesis-bound, linea 5) -> CERO re-genesis, CERO riesgo sobre el N=500 sellado ni la cadena #4 (el dataset es historia inmutable; el rename es ORTOGONAL a lo medido, solo se anota procedencia; H1-H3 no se tocan). 'Aegis' vive en README/docs publicados/spec/namespace/carpetas de instancia, NO en el id tecnico del config. RELACION CON 0085: esta DECISION ACLARA/eleva el uso de 'Aegis' de 0085 (donde nombra la instancia de Nova) a 'marca de la metodologia'; 0085 no se contradice (NOVA/Aegis sigue siendo la instancia aegis de Nova). PUBLICACION (i18n): traducir el core neutral + `.template.*` + README + spec de referencia a INGLES para publicar NO es cosmetico -> es un PROGRAMA de **Carril B** (post-sello, acotado a la superficie publicada, NO todo el repo; el dogfooding en espanol no se publica). La DECISION debe crear/anotar el item Carril B correspondiente y dejar la EJECUCION (adopcion de marca + i18n) para despues del sello. APROBACION: el naming publico de la metodologia es identidad -> ya aprobado por el Operador en debate 2026-07-03; la DECISION lo registra. NOTA: DD-02 (objeto min 20) horneada toca un criterio falsable -> asegura que ese cambio de las SPECs viaje en un gate del lote cuando corresponda (seguimiento aparte, no bloquea esta DECISION)."
question: ""
---

# DIRECTIVA - Redacta la DECISION de nombres (metodologia = Aegis, marca-solo)

Cerradas las 2 DIRECTIVAs previas (DD horneadas 01f05db + pipeline al dia 2320acd), este es el paso
acordado: formalizar en una DECISION lo que el Operador decidio tras debate con el Asesor.

**Resumen de lo decidido (detalle vinculante en requested_action):**
- **Aegis** = marca de la **metodologia** (palabra neutra, citable para publicar). Hub = **Aegis-core**.
- Instancia por proyecto = **`aegis/`** (convencion tipo `.git`); ya existe `NOVA/Aegis`.
- Producto = **Zeus-Aegis**; dominio = **Nova-X**.
- Skills: prefijo **`aegis:`** por **namespacing via loader (DECISION-0061)**, NO renombrar archivos. Scripts SIN tocar.
- **MARCA-SOLO (opcion i):** NO se toca `project_name` (genesis-bound) -> cero re-genesis, cero riesgo N=500/#4.
- **i18n del core/templates/spec = Carril B** (post-sello, superficie publicada). Crea/anota su item Carril B.
- Aclara/eleva el uso de 'Aegis' de DECISION-0085 (instancia) a marca de la metodologia.

La ejecucion (adopcion de marca + i18n) es Carril B post-sello; esta DECISION solo fija la direccion.
