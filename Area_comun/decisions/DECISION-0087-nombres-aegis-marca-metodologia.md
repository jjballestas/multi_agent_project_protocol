---
decision_id: DECISION-0087
title: "Nombres: 'Aegis' = marca de la metodologia (modo MARCA-SOLO, sin tocar la config genesis-bound); familia de nombres + namespace de skills 'aegis:' via loader + i18n diferida a Carril B"
status: accepted
date: 2026-07-03
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0085, DECISION-0061, DECISION-0050, GOAL-VISION-NOVA-001]
phase: P2
scope: governance
approval_ref: "Naming publico de la metodologia = identidad; aprobado por el Operador (John Ballestas) en debate con el asesor 2026-07-03; esta DECISION lo registra. Directiva MSG-20260703-Operador-to-Arquitecto-DIRECTIVA-redacta-decision-nombres-aegis."
---

# DECISION-0087 - Nombres: la metodologia se marca 'Aegis' (marca-solo)

> Contexto: el protocolo neutral necesita un nombre citable para publicar. El Operador decidio, tras
> debate, marcar la METODOLOGIA como **Aegis** (palabra neutra -- un escudo, sin termino de dominio, no
> rompe la neutralidad del core). El alcance es **MARCA-SOLO (opcion i)**: la marca vive en README/docs/
> spec/namespace/carpetas de instancia, NO en el id tecnico genesis-bound de `protocol.config.json`. Cero
> re-genesis, cero riesgo sobre el N=500 sellado ni la cadena #4. La EJECUCION (adopcion de marca + i18n)
> es Carril B post-sello; esta DECISION solo fija la direccion.

## Decision

1. **Aegis = marca de la METODOLOGIA.** 'Aegis' es el nombre citable/publicable de la metodologia
   multi-agente (task lifecycle, claims, mailbox, handoffs, decisiones, reportes, validador, cadena #4
   atestada). Es una palabra neutra (escudo); NO introduce dominio y NO rompe la neutralidad del core.

2. **Familia de nombres (convencion de habla para desambiguar):**
   - **Aegis-core** = el HUB, la fuente canonica de la metodologia (este repositorio). Se dice
     "Aegis-core" o "el hub" para la fuente.
   - **`aegis/`** = la instancia de la metodologia aplicada a un proyecto (carpeta/repo). Convencion
     reconocible tipo `.git`/`node_modules`: el nombre se repite en cada proyecto y significa "la capa
     Aegis aplicada aqui". Ya existe `NOVA/Aegis` (la instancia aegis de la suite Nova).
   - **Zeus-Aegis** = el PRODUCTO/front (la app que operaria/observaria la metodologia).
   - **Nova-X** = los productos de DOMINIO de la suite Nova (Nova-Budget, Nova-Treasury, ...), per
     DECISION-0085. La marca Aegis (metodologia) es ortogonal a los nombres de producto de dominio.

3. **Skills: prefijo `aegis:` por NAMESPACING via el loader (DECISION-0061), NO renombrando archivos.**
   El prefijo visible en el CLI (p.ej. `aegis:mailbox-hygiene`, al estilo `anthropic-skills:docx`) se
   logra por namespacing en el loader de skills, no editando archivo por archivo.
   **Resolucion del loader** cuando coexistan skills `aegis:` del hub y skills locales de una instancia:
   gana la MAS ESPECIFICA (la skill local de la instancia sombrea a la del hub del mismo nombre), y para
   evitar colision cuando ambas deben coexistir se usa un sub-namespace explicito
   (`aegis:<skill>` para las del hub; `aegis:<instancia>:<skill>` o el id de la instancia como prefijo
   para las locales). La resolucion es deterministica y se documenta en el loader.

4. **Scripts: NO se tocan.** Los scripts (validador, harnesses, `submit_intent`, CI, crons,
   `verification_cmd`, cadena #4) NO se renombran ni re-prefijan: no se ven como skills en el CLI y el
   costo/riesgo es alto (romperia CI, crons, comandos de verificacion y la atestacion #4). La atribucion
   a la marca, si acaso, va por encabezado de archivo o nombre de directorio, nunca por rename masivo.

5. **MARCA-SOLO: NO se toca `project_name` en `protocol.config.json`.** El `project_name`
   (`multi_agent_project_protocol`) esta genesis-bound (la linea 5 entra en el hash de genesis de la
   cadena #4). Renombrarlo exigiria una re-genesis coordinada y pondria en riesgo el N=500 sellado y la
   cadena atestada. Por eso el rename es MARCA-SOLO y ORTOGONAL a lo medido: el dataset es historia
   inmutable; la marca solo anota procedencia. **H1-H3 y el N=500 NO se tocan.** El id tecnico del config
   permanece; 'Aegis' vive fuera del config (README, docs publicados, spec de referencia, namespace de
   skills, carpetas de instancia `aegis/`).

6. **Relacion con DECISION-0085.** Esta DECISION ACLARA/eleva el uso de 'Aegis': en 0085 'Aegis' nombra la
   INSTANCIA de metodologia de la suite Nova (`NOVA/Aegis`); aqui 'Aegis' se eleva a MARCA de la
   metodologia entera. No hay contradiccion: `NOVA/Aegis` sigue siendo "la instancia aegis de Nova", que
   es exactamente el patron de nombre `aegis/` de esta decision.

7. **i18n (publicacion) = programa de CARRIL B, post-sello.** Traducir a INGLES la superficie PUBLICADA
   (core neutral + `*.template.*` + README + spec de referencia) NO es cosmetico: es un programa acotado
   de Carril B, POSTERIOR al sello, limitado a la superficie publicada (el dogfooding en espanol de este
   repo NO se publica). Se crea/anota el item de Carril B correspondiente (ver Consecuencias); la
   EJECUCION (adopcion de marca + i18n) queda para despues del sello.

## Consecuencias

- La metodologia gana nombre citable ('Aegis') para publicacion, SIN tocar el id tecnico ni la cadena #4.
- Cero re-genesis, cero riesgo sobre el N=500 sellado, epoch 1.14.0 y `protocol.config.json` byte-identico.
- El namespace `aegis:` de skills se implementa en el loader (DECISION-0061), no por renames; queda un
  item de implementacion (loader) para cuando se adopte la marca (post-sello, no urgente).
- **Item Carril B (i18n/marca):** se anota un programa de Carril B "Adopcion de marca Aegis + i18n a
  ingles de la superficie publicada (core neutral + templates + README + spec)", GATEADO post-sello,
  acotado a lo publicado; el Operador lo prioriza en el Carril B cuando el Carril A lo permita.
- 0085 no se contradice; `NOVA/Aegis` es la instancia aegis de Nova.
- Seguimiento aparte (no bloquea esta DECISION): DD-02 (objeto RP min 20, horneada en SPEC-NOVA-P3-003,
  commit 01f05db) toca un criterio falsable -> viaja en el proximo gate del lote NOVA-DEV.
