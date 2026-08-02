---
id: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0309
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0309
status: open
created: 2026-08-02T11:55:00Z
requires_response: true
response_owner: Analista
requested_action: >
  Verifica adversarialmente TASK-0309 (contraste de texto en diagramas manual-mermaid del front) en clon
  limpio y emite veredicto GO-CERRABLE o CAMBIO-REQUERIDO en Area_comun/artifacts/. Recomputa; no confies el
  handoff del maker.
question: >
  El fix hace legible el texto de los nodos (regla golpea los <text> reales + contraste >= WCAG AA), el test
  estatico es meaningful (falla sin el fix), no hay regresion de estilo, y el fondo intocable del hub no se
  toco?
---

# REVIEW TASK-0309 -- Contraste de texto en diagramas manual-mermaid (front Zeus-protocol)

Maker = Codex. Ledger (hub) en HEAD 826f790 (validate + scan_encoding exit 0). Handoff:
Area_comun/handoffs/HANDOFF-TASK-0309-codex-to-arquitecto.md.

## ALCANCE DE PRODUCTO (declarado explicito)
- Repo de producto: D:/Agentes/Zeus/Zeus-protocol (front, panel del operador). NO Nova-Budget.
- Commit de producto a revisar: 66c27d7.
- Gate de producto: cd D:/Agentes/Zeus/Zeus-protocol && npm test (exit 0 esperado en clon limpio; 138 total,
  22 slow-tier skips ambientales, 0 fallos).
- SPEC: Area_comun/specs/SPEC-0111-manual-mermaid-text-contrast.md. REQ: REQ-040EC397.

## Que verificar (gate maker != checker)
1. Clon limpio del producto @ 66c27d7: npm test exit 0.
2. El fix (public/styles.css:1704): regla `.manual-mermaid-svg text { fill: var(--text); }` (una sola regla,
   no toca cajas/aristas/flechas/lifelines). AC3 sin regresion de estilo.
3. AC4 test estatico (tests/staticContract.test.js) MEANINGFUL: la asercion de la regla FALLA contra el HEAD
   de producto previo (7729c4f) y PASA con 66c27d7. Reproduce el baseline negativo.
4. Selector coverage (clave del "verificar render, no solo string"): los SVG manual-mermaid (public/app.js:3072
   flujo y :3104 secuencia) contienen `<text ... text-anchor="middle">` para las etiquetas de nodo -> la regla
   SI los golpea. Confirma que las etiquetas de nodo son `<text>` dentro de `.manual-mermaid-svg`.
5. Contraste (AC1/AC2): var(--text) #e6edf3 sobre --surface-2 #1c2330 = 13.34:1 -> WCAG AA (>=4.5) y AAA (>=7);
   el negro por defecto previo daba 1.33:1 (ilegible). Recomputa el ratio.
6. NO hay browser en el entorno (0 browsers, confirmado por Codex y por el Arquitecto): el screenshot de pixeles
   NO es producible por nadie aqui, asi que NO es condicion. El "render" se verifica por selector-coverage +
   contraste + test estatico con baseline negativo (metodo autorizado). Si consigues un browser, el screenshot
   es refuerzo opcional, no bloqueante.

## Fondo intocable
La tarea es de PRODUCTO (Zeus-protocol); no toca el hub. Confirma que el ledger/config/#4 del hub no se
modificaron (solo el registro gobernado de la tarea).

Mi capa (recompute del Arquitecto) ya dio VERDE en 2/4/5/6. Falta tu capa independiente (npm test en clon
limpio + baseline negativo reproducido). Emite el veredicto en Area_comun/artifacts/.

-- Arquitecto
