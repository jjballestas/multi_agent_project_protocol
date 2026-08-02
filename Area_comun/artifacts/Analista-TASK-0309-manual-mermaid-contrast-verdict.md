---
artifact_id: Analista-TASK-0309-manual-mermaid-contrast-verdict
reviewer: Analista
task_id: TASK-0309
spec_id: SPEC-0111
req: REQ-040EC397
verdict: OK-CLOSABLE
created: 2026-08-02
---

# Veredicto adversarial -- TASK-0309 (contraste de texto en diagramas manual-mermaid, front Zeus-protocol)

Voz: Analista (checker independiente, maker != checker). Recomputo propio; no confio el handoff
del maker.

## Anclaje canonico
- Repo de producto: Zeus-protocol (https://github.com/jjballestas/Zeus-protocol.git).
- Commit de producto revisado: 66c27d7 (fix). Baseline previo: 7729c4f.
- Hub (gobernanza) HEAD al recomputar: 69118ae; TASK-0309 status=in_review, owner=Codex,
  reviewer=Analista, type=product, project=Zeus-protocol, spec=SPEC-0111.
- Metodo de review: CLON LIMPIO del producto en ruta corta de scratch
  (D:/Aegis_Scratch/zeus/r0309), checkout 66c27d7, gates por EXIT CODE. No verifico en arbol
  caliente.

## Reproduccion (con exit codes)
1. git clone local -> checkout 66c27d7 -> working tree limpio (git status vacio).
2. `npm test` (script = `node --test`, cero dependencias) -> EXIT 0.
   tests 138, pass 116, fail 0, skipped 22, duration ~3.07s.
   El test "help Mermaid blocks render as SVG..." RAN y paso (no skip).
3. Los 22 skips son TODOS `# slow subprocess tier; run npm run test:slow` (ambientales); ninguno
   toca el fix de contraste.
4. Baseline negativo BEHAVIORAL: sustituyo public/styles.css por el contenido de 7729c4f y corro
   `node --test tests/staticContract.test.js` -> EXIT 1, `fail 1`, y el UNICO test que falla es
   exactamente "help Mermaid blocks render..." con AssertionError sobre la regex
   `/\.manual-mermaid-svg\s+text\s*\{[^}]*fill:\s*var\(--text\)\s*;?[^}]*\}/s`. css restaurado limpio.
5. Baseline negativo por REGEX directa (node): la regex del test NO matchea el css de 7729c4f
   (false) y SI matchea el css de 66c27d7 (true).

## Vector por vector

| # | Criterio (instruccion / AC) | Metodo de recomputo | Resultado |
|---|------------------------------|---------------------|-----------|
| 1 | AC5 npm test exit 0 en clon limpio | clon limpio @66c27d7, `node --test`, gate por exit | PASS (0; 138/116/0/22) |
| 2 | AC3 fix = una sola regla, sin regresion de estilo | `git diff 7729c4f..66c27d7` = 2 files, 5 insertions, 0 deletions; cajas/aristas/flechas/lifelines byte-equivalentes | PASS |
| 3 | AC4 test estatico MEANINGFUL (falla sin el fix) | swap css a 7729c4f -> falla SOLO ese test (fail 1) + regex no-match vs match | PASS |
| 4 | Selector coverage: `<text>` reales golpeados | lectura de public/app.js: flow (:3067) y sequence (:3087,:3100) emiten `<text ... text-anchor="middle">` DESNUDOS (sin fill/style/class inline) dentro de `<svg class="manual-mermaid-svg">` | PASS |
| 5 | AC1/AC2 contraste >= WCAG AA | recomputo WCAG propio: #e6edf3 sobre #1c2330 = 13.34:1 (AA>=4.5, AAA>=7); negro previo #000 = 1.33:1 | PASS |
| 6 | Screenshot de pixeles | no hay browser en el entorno; refuerzo opcional NO condicion (autorizado por Arquitecto) | N/A |
| 7 | Fondo intocable del hub (#4/config/ledger) | product commit en repo separado; commits del hub para 0309 tocan solo estado gobernado (mailbox/handoff/CLAIMS/STATE/TASK_INDEX/task/runtime-state); protocol.config.json epoch 1.14.0 y genesis SIN tocar; validate exit 0; scan_encoding exit 0 | PASS |

## Analisis de escape (intento de romper la garantia)
- Especificidad: `.manual-mermaid-svg text` = (0,1,1) vence al default de presentacion SVG (negro,
  0,0,0). Ningun `<text>` lleva `fill=` atributo, `style="fill:..."` inline, ni clase que gane. No
  hay otra regla que fije `fill` sobre `.manual-mermaid-svg text`. Sin escape.
- Sobre-alcance: la regla esta acotada a `.manual-mermaid-svg text` (no `text` global). Aristas
  (`.manual-mermaid-edge`), flechas (`.manual-mermaid-arrow`) y lifelines
  (`.manual-mermaid-lifeline`) son `<path>`/`<polygon>`, no `<text>` -> no afectadas (AC3). Sin
  regresion.
- Tokens verificados en el propio css (no confiados del handoff): `--text: #e6edf3`,
  `--surface-2: #1c2330`, `--surface: #161b22`.

## Residuales declarados (no bloqueantes)
- R1 (render de pixeles): la legibilidad se establece por selector-coverage deterministico +
  contraste computado + regresion estatica con baseline negativo, NO por un screenshot renderizado
  real (no hay browser aqui). Es el sustituto AUTORIZADO por el Arquitecto; lo declaro honesto como
  el limite de esta capa. El DoM path esta probado a nivel de codigo/regex, no a nivel de pixel.
- R2 (labels de mensaje en secuencia): los `<text>` de mensajes (app.js:3100) se posan sobre
  `--surface` (#161b22), no sobre las cajas #1c2330; el contraste alli es AUN MAYOR (fondo mas
  oscuro), reforzando la legibilidad. Solo mejora, no riesgo.

## Recomendacion de cierre
**OK-CLOSABLE.** Los 5 criterios verificables (AC1-AC5) recomputados de forma independiente pasan;
el test estatico es meaningful (baseline negativo reproducido, behavioral y por regex); no hay
regresion de estilo (diff de 5 lineas puras additivas); el contraste 13.34:1 excede WCAG AA/AAA; y
el fondo/config/#4 del hub no se tocaron. Residuales R1/R2 declarados y no bloqueantes.

-- Analista
