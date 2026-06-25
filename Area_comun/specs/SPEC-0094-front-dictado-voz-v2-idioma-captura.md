# SPEC-0094 - Front: dictado por voz v2 -- idioma es-CO + captura manual con stop + indicador de grabacion (follow-up SPEC-0093)

- **Estado:** draft. Maker: Codex. Checker: Arquitecto + PASADA DEL ANALISTA (foco: el egress de audio sigue
  opt-in/off-by-default aunque la captura ahora sea sostenida/mas larga).
- **Fecha:** 2026-06-25. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen:** operador (sesion 2026-06-25): el dictado captura bien en ingles pero mal en espanol; ademas pidio
  una UX de captura manual (referencia: barra de entrada de Claude -- estado inicial inactivo, boton detener,
  timer e indicador de grabacion, y procesar el texto al detener). Follow-up de SPEC-0093 / TASK-0177 (entregado).

## Causa raiz (idioma)
En `public/app.js` el reconocedor se inicializa con
`recognition.lang = document.documentElement.lang || navigator.language || "es-ES"`. Como `public/index.html`
declara `<html lang="en">` (primer termino del fallback), el reconocedor queda en ingles sin importar el resto;
por eso captura bien ingles y mal espanol. La UI es integramente en espanol, asi que el `lang="en"` ademas es
incorrecto semanticamente.

## Frontera dura (EGRESS) -- se MANTIENE (no se debilita)
La captura sigue usando **Web Speech API** del navegador (posible egress de audio a un servicio externo del
proveedor). Esta SPEC NO cambia la frontera: sigue **off-by-default + opt-in con AVISO** (VOICE_EGRESS_NOTICE) en
la primera captura; sin aceptar -> no captura; degradacion limpia si no hay soporte. La captura sostenida
(`continuous`) envia *mas* audio durante una sesion, pero el control del operador es el mismo (aviso + stop
manual). El texto sigue siendo **textarea-only**: NO emite submit_intent ni abre nueva ruta de escritura; el
texto sigue redactado en el submit gobernado.

## acceptance_criteria
- **AC1 (idioma espanol robusto)** El reconocedor se inicializa con un locale espanol fijo `es-CO` (fallback
  `es-419` -> `es-ES`), **independiente** de `navigator.language` y del `<html lang>`; ademas `public/index.html`
  corrige `<html lang>` a `es`. Behavior-test: el reconocedor se construye con `lang` espanol (`es-*`) aunque el
  entorno simule un navegador en ingles.
- **AC2 (estado inicial inactivo)** El microfono arranca **inactivo**; no auto-escucha al render. Behavior-test:
  estado inicial idle; no hay captura hasta una activacion explicita.
- **AC3 (captura manual con stop + indicador)** Al activar (tras el aviso/confirmacion de egress de SPEC-0093) la
  captura es **sostenida** (`continuous=true`): NO se detiene sola por una pausa. Mientras graba, el control
  muestra un **indicador de grabacion animado** (no ligado al nivel real del microfono), un **timer** `m:ss` y un
  **boton de detener** (cuadrado). El operador detiene **manualmente**. Behavior-test: en estado escuchando el
  control expone stop + timer y la captura no termina por pausa; el stop manual finaliza la captura.
- **AC4 (post-stop procesa y muestra)** Al detener, el texto reconocido **acumulado** se procesa y se
  inserta/concatena en el textarea correspondiente (Narrativa / Intencion, modal Manual + tarjeta). Behavior-test:
  tras el stop el texto reconocido aparece en el textarea correcto.

## Carries (de SPEC-0093, deben seguir verdes)
- **AC3-egress (SPEC-0093)** off-by-default + aviso opt-in INTACTO; sin aceptar -> no captura; sin soporte ->
  deshabilitado limpio.
- **AC4-no-bypass/PII (SPEC-0093)** textarea-only; sin submit_intent; sin nueva ruta de escritura; texto redactado
  en el submit.
- **AC11** badge-honesto, **AC12** routing, **AC13** conformidad-diseno (tokens del design-system).

## DoD
- AC1-AC4 + carries verdes con behavior-tests; `node --test` clon limpio exit 0 (estable); validate con/sin
  secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica; sin nueva ruta de escritura.
- Checker (Arquitecto) clon limpio; maker!=checker. **PASADA DEL ANALISTA** (foco: la captura sostenida no
  debilita el opt-in/off-by-default; el aviso sigue gateando la primera captura; el stop manual existe; sin fuga;
  texto redactado).
- REPRO: navegador (aunque este en ingles) -> dictar en espanol -> el texto sale en espanol; el microfono arranca
  inactivo; al activar aparece timer + boton detener + indicador; no se corta solo por pausa; al detener el texto
  aparece en el textarea; sin soporte -> deshabilitado limpio.

## Notas
- Indicador "animado simple" por decision del operador (no medidor de nivel real); evita un getUserMedia/Web Audio
  paralelo y no agrega permiso ni stream extra de microfono (la frontera egress no cambia).
