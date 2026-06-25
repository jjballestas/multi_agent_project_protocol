---
task_id: TASK-0179
title: "Proyecto-front: dictado por voz v2 -- idioma es-CO + captura manual con stop + indicador de grabacion (SPEC-0094)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0094
created_at: 2026-06-25
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: operador-sesion-20260625
linked_decisions: [DECISION-0050, DECISION-0040]
follows: TASK-0177
file: Area_comun/tasks/TASK-0179-codex-front-dictado-voz-idioma-captura.md
---

# TASK-0179 - Dictado por voz v2: idioma + captura manual (SPEC-0094)

> Follow-up de TASK-0177 (dictado por voz). Arregla el idioma (capturaba en ingles) y mejora la UX de captura.
> maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA. Solo presentacion (app.js + index.html + CSS + tests);
> sin nueva ruta de escritura. Repo producto Zeus-protocol. La frontera de egress de SPEC-0093 se MANTIENE.

## Alcance (SPEC-0094 AC1-AC4)
- **AC1 idioma:** `recognition.lang = "es-CO"` (fallback `es-419` -> `es-ES`), independiente de `navigator.language`
  y del `<html lang>`; corregir `public/index.html` `<html lang="en">` -> `"es"`. (Causa raiz: hoy
  `recognition.lang = document.documentElement.lang || ...` y el html declara `lang="en"`.)
- **AC2 inicio inactivo:** microfono arranca inactivo; sin auto-escucha al render.
- **AC3 captura manual:** `continuous=true` (no auto-stop por pausa); indicador de grabacion animado simple (NO
  nivel real de mic) + timer `m:ss` + boton detener (cuadrado); el operador detiene manualmente.
- **AC4 post-stop:** al detener, el texto acumulado se procesa e inserta/concatena en el textarea (Narrativa /
  Intencion, modal Manual + tarjeta).
- **Carries (siguen verdes):** egress off-by-default + aviso opt-in (SPEC-0093 AC3); textarea-only / sin
  submit_intent / texto redactado (SPEC-0093 AC4); AC11 badge / AC12 routing / AC13 tokens.

## DoD
- AC1-AC4 + carries verdes con behavior-tests; `node --test` clon limpio exit 0 (estable); #4 byte-identica; sin
  nueva ruta de escritura. Checker Arquitecto clon limpio + PASADA DEL ANALISTA (la captura sostenida no debilita
  el opt-in/off-by-default; el aviso sigue gateando; stop manual presente; sin fuga; texto redactado).
- REPRO: con el navegador en ingles, dictar en espanol -> texto en espanol; microfono arranca inactivo; al activar
  -> timer + boton detener + indicador; no se corta solo por pausa; al detener -> texto en el textarea; sin
  soporte -> deshabilitado limpio.
