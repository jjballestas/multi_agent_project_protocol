# SPEC-0093 - Front: dictado por voz (microfono) en narrativa e intencion del Intake (REQ-003AE958)

- **Estado:** draft. Maker: Codex. Checker: Arquitecto + PASADA DEL ANALISTA (foco: EGRESS de audio + PII).
- **Fecha:** 2026-06-25. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen:** REQ-003AE958 (montado por el operador via "Enviar al Arquitecto"). Relacionada: SPEC-0092 (Intake),
  DECISION-0040 (PII), patron local-vlm loopback-only (no-egress).

## Objetivo
Un icono de microfono en la esquina inferior derecha de los textarea de **Narrativa** e **Intencion de aceptacion**
del Intake (modal Manual / tarjeta) que permita **dictar por voz** y que el texto reconocido aparezca en el
textarea correspondiente.

## Frontera dura (EGRESS) -- AC central
La captura por voz usa el **Web Speech API** del navegador (`SpeechRecognition`), que en algunos navegadores
(Chrome) **transmite audio a un servicio externo del proveedor**. El protocolo es no-egress por defecto. Por tanto:
- **Off-by-default / opt-in explicito:** el dictado NO se activa solo; al presionar el microfono por primera vez se
  muestra un **AVISO claro**: "La captura por voz usa el reconocimiento del navegador y puede enviar audio a un
  servicio externo del proveedor del navegador." El operador confirma antes de la primera captura.
- **Degradacion limpia:** si el navegador no soporta SpeechRecognition, el icono se deshabilita con tooltip
  ("no disponible en este navegador"), sin error.
- El **texto dictado** entra al textarea y sigue el flujo gobernado del Intake (redaccion PII en el submit, como
  cualquier texto). NO se agrega ninguna nueva ruta de escritura de estado.

## acceptance_criteria
- **AC1** Icono de microfono en la esquina inferior derecha de los textarea de Narrativa e Intencion (modal Manual
  y tarjeta de candidata). Behavior-test: el render expone el control de microfono por textarea.
- **AC2** Al presionar el microfono (tras el aviso/confirmacion de egress), inicia la captura; el texto reconocido
  se inserta/concatena en el textarea correspondiente; un segundo toque detiene. Behavior-test del estado de
  captura (idle/escuchando) y de que el texto reconocido va al textarea correcto.
- **AC3 (frontera egress)** Off-by-default: primera captura exige confirmacion del aviso de egress; sin
  confirmacion no captura. Degradacion limpia si no hay soporte. Behavior-test: sin confirmacion -> no captura;
  sin soporte -> deshabilitado.
- **AC4 (no-bypass / PII)** El dictado solo llena el textarea; NO emite submit_intent ni abre ruta de escritura;
  el texto sigue redactado en el submit gobernado. Behavior-test: el dictado no agrega emisores de submit_intent.

## Carries: AC11 badge-honesto, AC12 routing, AC13 conformidad-diseno (tokens).

## DoD
- AC1-AC4 verdes con behavior-tests; node --test clon limpio exit 0 (estable); validate con/sin secretos exit 0;
  drift 0; neutralidad+encoding 0; #4 byte-identica; sin nueva ruta de escritura.
- Checker (Arquitecto) clon limpio; maker!=checker. **PASADA DEL ANALISTA** (foco: el egress de audio queda
  opt-in con aviso, off-by-default, sin fuga; el texto sigue redactado; sin nueva ruta de escritura).
- REPRO: icono de microfono en los 2 textarea; primer toque -> aviso de egress -> confirmar -> dictar -> el texto
  aparece en el textarea; sin soporte -> deshabilitado limpio.

## Notas
- Si el operador prefiere CERO egress, el dictado quedaria pendiente de una STT local (fuera de alcance de esta
  SPEC); por eso el opt-in + aviso es la salida honesta para la version navegador.
