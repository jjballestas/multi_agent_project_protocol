---
name: arquitecto-pipeline-vision-nova
description: >-
  Como el Arquitecto actualiza el PIPELINE vivo de la Vision Nova
  (personal/operador/vision-nova/pipeline-vision-nova.html): marcar items hechos/en curso/
  bloqueados con EVIDENCIA y sello de hora, tras cada verde del Analista, cada release, cada
  cierre de tarea del roadmap Nova, o cuando el operador diga "actualiza el pipeline",
  "marca X", "avance", "tablero", "pipeline". Tambien al detectar que un item del pipeline
  quedo cumplido por un commit/veredicto reciente aunque nadie lo pida (el tablero desactualizado
  es un reporte falso). Trigger words: pipeline, tablero, marcar, hecho, avance, vision nova,
  sprint 1, F0-F6, CB, actualizar pipeline.
---

# Actualizar el pipeline de la Vision Nova

El operador supervisa el plan Nova desde `personal/operador/vision-nova/pipeline-vision-nova.html`
abierto en su navegador. Ese HTML es el REPORTE CANONICO de avance: si esta desactualizado, el
operador decide con datos falsos. Actualizarlo es parte del cierre de cada hito, igual que la
memoria post-commit (DECISION-0026).

## Reglas duras

1. **Solo se edita el bloque `PIPELINE-DATA`** (entre los marcadores `PIPELINE-DATA-START` y
   `PIPELINE-DATA-END`). Nada de tocar HTML/CSS/render.
2. **"hecho" exige evidencia** en el campo `ev`: hash corto de commit, tag de release, ruta de
   artefacto o veredicto (`GO Analista <commit>`). Sin evidencia NO se marca — es el mismo
   principio anti-falso-verde del protocolo. "en_curso" puede llevar nota corta en `ev`.
3. **Sello de hora SIEMPRE**: `updated_at` = hora local real del momento de la edicion
   (formato `YYYY-MM-DD HH:MM`), `updated_by` = "Arquitecto". Un reporte sin hora fresca es un
   reporte viejo disfrazado (regla del operador para todo reporte).
4. **No agregar/quitar/renombrar items** sin orden explicita del operador. Un re-alcance se
   anota en el titulo del item como `[re-alcance: motivo]`, no se borra historia.
5. **Estados validos**: `pendiente | en_curso | hecho | bloqueado`. Un item `bloqueado` lleva
   en `ev` el motivo concreto y quien lo destraba.
6. **El gate del sprint 1 (30 de julio) no se mueve.** Si un prerequisito se atrasa, lo que se
   negocia con el operador es el ALCANCE del item, nunca `sprint1_date`.

## Procedimiento

1. Leer el HTML (solo el bloque de datos) y el estado real que lo respalda (commit, veredicto,
   tag, artefacto) — verificar, no asumir.
2. Editar el bloque `PIPELINE-DATA`: estados + `ev` + `updated_at`/`updated_by`.
3. Commit atomico SOLO de ese archivo (pathspec explicito, arbol compartido):
   `git add -- personal/operador/vision-nova/pipeline-vision-nova.html`
   `git commit -m "pipeline(vision-nova): <items actualizados>" -- personal/operador/vision-nova/pipeline-vision-nova.html`
   y push a main. Esto NO toca el ledger (es reporte del area del operador, no estado gobernado);
   no requiere submit_intent ni claim.
4. Si el avance vino de un verde del Analista: esta actualizacion forma parte del checkpoint
   obligatorio (memoria + prompt + skills + pipeline).

## Cuando NO usar esta skill

- Para el estado de tareas del LEDGER (TASK_INDEX): eso va por submit_intent como siempre; el
  pipeline HTML es la vista del operador, no la fuente de verdad del protocolo.
- Para replanificar (agregar fases, cambiar fechas): eso es del operador; proponer via mensaje,
  no editar.
