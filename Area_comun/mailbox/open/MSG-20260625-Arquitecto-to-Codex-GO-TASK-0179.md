---
message_id: MSG-20260625-Arquitecto-to-Codex-GO-TASK-0179
task_id: TASK-0179
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Implementar TASK-0179 (dictado por voz v2, SPEC-0094) en el repo producto Zeus-protocol como maker: (1) idioma -- recognition.lang = 'es-CO' (fallback es-419 -> es-ES) independiente de navigator.language y del <html lang>, y corregir public/index.html <html lang=en> -> es; (2) microfono arranca inactivo (sin auto-escucha); (3) captura manual -- continuous=true (sin auto-stop por pausa) con indicador de grabacion animado SIMPLE (no nivel real de mic) + timer m:ss + boton detener (cuadrado); (4) al detener, el texto acumulado se procesa e inserta/concatena en el textarea (Narrativa/Intencion, modal Manual + tarjeta). MANTENER la frontera de egress de SPEC-0093 (off-by-default + aviso opt-in) y el caracter textarea-only (sin submit_intent / sin nueva ruta de escritura / texto redactado). Behavior-tests por AC; node --test clon limpio exit 0; #4 byte-identica. Mover a in_review via submit_intent (claim file-scoped) cuando este verde. NO forjar commits del Arquitecto: commit como Arquitecto con Co-Authored-By Codex."
question: "Tomas TASK-0179 (dictado voz v2: idioma es-CO + captura manual con stop/indicador, SPEC-0094) y entregas a in_review con behavior-tests verdes? rr=true."
one_line_summary: "GO a Codex: TASK-0179 dictado por voz v2 (idioma es-CO + captura manual con stop + indicador), follow-up de TASK-0177; egress de SPEC-0093 intacto; maker=Codex / checker=Arquitecto + Analista."
context_refs:
  - Area_comun/tasks/TASK-0179-codex-front-dictado-voz-idioma-captura.md
  - Area_comun/specs/SPEC-0094-front-dictado-voz-v2-idioma-captura.md
  - Area_comun/specs/SPEC-0093-front-dictado-voz-intake.md
  - Area_comun/tasks/TASK-0177-codex-front-dictado-voz.md
---

# GO TASK-0179 -- dictado por voz v2 (idioma es-CO + captura manual)

Origen: el operador probo el dictado (TASK-0177) y captura bien en INGLES pero mal en ESPANOL; ademas pidio una
UX de captura manual (referencia: barra de entrada de Claude -- estado inicial inactivo, boton detener, timer e
indicador de grabacion, y procesar el texto al detener).

## Causa raiz (idioma)
En public/app.js: `recognition.lang = document.documentElement.lang || navigator.language || "es-ES"`, y
public/index.html declara `<html lang="en">` (primer termino del fallback) -> el reconocedor queda en ingles.

## Alcance (SPEC-0094 AC1-AC4)
- AC1 idioma: lang fijo `es-CO` (fallback `es-419` -> `es-ES`), independiente del navegador / <html lang>;
  index.html `<html lang>` -> `es`.
- AC2: microfono arranca inactivo (sin auto-escucha al render).
- AC3: captura sostenida `continuous=true` (sin auto-stop por pausa) + indicador animado SIMPLE + timer m:ss +
  boton detener (cuadrado); stop manual.
- AC4: al detener, texto acumulado -> textarea correcto (Narrativa/Intencion, modal Manual + tarjeta).
- Carries verdes: egress off-by-default + aviso opt-in (SPEC-0093 AC3); textarea-only / sin submit_intent / texto
  redactado (SPEC-0093 AC4); AC11/AC12/AC13.

## Frontera (no debilitar)
La captura sigue Web Speech API (egress posible). Sostenida = mas audio por sesion, pero MISMO control: aviso
opt-in en la primera captura + stop manual. El indicador es animado simple (no getUserMedia/Web Audio) -> sin
stream extra de microfono, la frontera no cambia.

## Cierre
maker=Codex / checker=Arquitecto clon limpio (maker!=checker) + **PASADA DEL ANALISTA** (egress sostenido sigue
opt-in/off-by-default; aviso gatea; stop manual; sin fuga; texto redactado). Mueve a in_review con behavior-tests
verdes via submit_intent (claim file-scoped); yo verifico y luego el Analista; cierro in_review->done. rr=true.
