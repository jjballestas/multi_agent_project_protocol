---
spec_id: SPEC-0111
title: Contraste de texto legible en los diagramas manual-mermaid de la seccion Ayuda (front Zeus-protocol)
status: ready
owner: Codex
relates_to: [REQ-040EC397]
project: Zeus-protocol
date: 2026-08-02
file: Area_comun/specs/SPEC-0111-manual-mermaid-text-contrast.md
---

# SPEC-0111 -- Contraste de texto en diagramas manual-mermaid (Ayuda)

Operacionaliza REQ-040EC397 (autor: Operador; sdd_role seed_only_architect_authors_spec -> spec redactado por
el Arquitecto). Repo de producto: `Zeus-protocol` (panel del operador). La gobernanza vive en el hub; el codigo
se implementa en `D:\Agentes\Zeus\Zeus-protocol`.

## Problema (verificado en el codigo, HEAD 7729c4f)
En `public/styles.css`, la regla `.manual-mermaid-node` pinta la caja del nodo con `fill: var(--surface-2)`
(#1c2330, fondo oscuro) pero **no existe regla que fije el `fill` de los elementos `<text>`** dentro de
`.manual-mermaid-svg`. El default SVG de `fill` para texto es NEGRO, por lo que las etiquetas de los nodos de los
diagramas de la seccion Ayuda (bloques Arquitectura, Mapa de la aplicacion, Flujo de accion gobernada) se
renderizan negro sobre fondo oscuro -> casi ilegibles. El `color: var(--text-muted)` que lleva `.manual-mermaid-svg`
no aplica al texto porque el `<text>` no usa `fill: currentColor`.

## Fix (intencion de diseno)
El texto de los diagramas manual-mermaid debe tomar un color CLARO del design system, legible sobre `--surface-2`,
sin alterar cajas, bordes, aristas, flechas ni lifelines. Color elegido por el spec (el valor concreto del seed
quedo redactado por el PII guard): **`var(--text)` (#e6edf3)**, el token de texto primario del panel -> contraste
muy alto (~13:1) sobre `--surface-2`, coherente con el resto de la UI. Implementacion recomendada (no vinculante en
la forma, si en el efecto): una unica regla CSS que fije el fill del texto del SVG, p.ej.

```css
.manual-mermaid-svg text { fill: var(--text); }
```

Esto cubre las etiquetas de nodo y cualquier otra `<text>` del SVG. Las aristas/flechas/lifelines son
`path`/`polygon` (no `<text>`) y NO se ven afectadas.

## Criterios de aceptacion
- **AC1 (legibilidad):** el texto de los nodos (`<text>` dentro de `.manual-mermaid-svg`) se renderiza con un
  color claro del design system (`var(--text)` #e6edf3, o token equivalente), NO negro. En los 3 diagramas de
  Ayuda (Arquitectura, Mapa de la aplicacion, Flujo de accion gobernada) todas las cajas quedan legibles.
- **AC2 (contraste):** el ratio de contraste del texto sobre `--surface-2` (#1c2330) cumple >= WCAG AA (>=4.5:1
  para texto normal; el par elegido da ~13:1). Declarar el par color/fondo y el ratio en el handoff.
- **AC3 (sin regresion visual):** cajas (`fill: var(--surface-2)`, `stroke: #2e4a7a`), aristas/lifelines
  (`stroke: var(--accent)`), flechas (`fill: var(--accent)`) y bordes quedan BYTE-equivalentes en su estilo; el
  cambio se limita al fill del texto. Sin tocar otros paneles/estilos.
- **AC4 (contrato estatico):** `tests/staticContract.test.js` se extiende para ASERTAR que existe la regla de
  fill de texto legible del SVG manual-mermaid (p.ej. match de `.manual-mermaid-svg text` con `fill: var(--text)`),
  ademas de las aserciones existentes (`<svg class="manual-mermaid-svg"`, `.manual-mermaid-svg`). El test debe
  FALLAR sin el fix y PASAR con el.
- **AC5 (gates producto):** `npm test` del repo Zeus-protocol exit 0 en clon limpio; sin nuevos warnings.

## Alcance
- IN: `public/styles.css` (regla de fill de texto del SVG manual-mermaid) + `tests/staticContract.test.js`
  (asercion AC4). Repo Zeus-protocol.
- OUT: cambiar el layout/estructura de los diagramas, el contenido del manual, otros paneles, o cualquier archivo
  del hub (protocolo). No tocar el color de cajas/aristas/flechas.

## Test plan
- Antes: renderizar la seccion Ayuda -> texto de nodos negro/ilegible (repro). Correr `staticContract` extendido
  -> FALLA (no existe la regla de fill).
- Despues: aplicar el fix -> texto legible en las 3 cajas; `staticContract` PASA; `npm test` exit 0; inspeccion
  visual (screenshot) de los 3 diagramas con texto claro legible.

## DoD
Cumple AC1-AC5; sin regresion; gate maker != checker (Analista verifica el RENDER, no solo el string: inspeccion
de imagen de los 3 diagramas + contraste); handoff con el par color/fondo y ratio declarados. Cierre gobernado.
