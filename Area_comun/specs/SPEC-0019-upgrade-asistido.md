---
spec_id: SPEC-0019-upgrade-asistido
task_id: TASK-0019
type: implementation
status: ready
linked_decisions: [DECISION-0006, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0019 — Migración/upgrade asistida entre versiones del protocolo

## Contexto
El drift entre el repo del protocolo y sus instancias está reconocido como riesgo, pero la adopción
de versiones es manual y costosa. DECISION-0006 §4 introduce una herramienta que **asiste** (reporta
deltas) sin **imponer** (no aplica sin confirmación), preservando la adopción-por-decisión de
DECISION-0001. Ver [DISENO-robustez-operacional.md](../artifacts/DISENO-robustez-operacional.md) §4.

## Alcance
- `scripts/upgrade_instance.py` y `scripts/upgrade_instance.ps1` (paridad).
- Fixtures de prueba bajo `examples/upgrade_cases/` (instancia desfasada vs al día).

## No-alcance
- **No** modificar la instancia (sin `--apply` en v0.6.0; read-only sobre la instancia).
- No escanear/copiar el área viva ni perfiles/ejemplos de dominio (solo el conjunto adoptable §1.2).
- No automatizar la política de adopción.

## execution_pipeline
1. CLI: `upgrade_instance --instance <ruta> [--master <ruta>] [--report <archivo>]`. `--master`
   por defecto = raíz del repo desde donde se ejecuta.
2. Leer `protocol_version` de `<instance>/protocol.config.json` y del master.
3. Determinar el **conjunto adoptable** (DISENO §1.2: masters/core genéricos, excluyendo área viva,
   perfiles, ejemplos, privados). Para cada archivo del master en ese conjunto, comparar por
   contenido contra la copia de la instancia ⇒ `nuevo` | `cambiado` | `igual` | `eliminado`.
4. Emitir **reporte de adopción** (markdown): versiones origen/destino, tabla de deltas y acciones
   recomendadas por archivo; enlazar secciones de CHANGELOG entre versiones si está disponible
   (best-effort). Escribir a stdout o a `--report`.
5. Garantizar que la instancia **no** se modifica (solo se lee; a lo sumo se escribe `--report`).
6. Golden fixtures + verificación de paridad `.py`↔`.ps1`.

## acceptance_criteria
- Reporta correctamente `nuevo/cambiado/igual/eliminado` para el conjunto adoptable entre la versión
  de la instancia y la del master.
- **No** escribe en la instancia bajo ninguna ruta de ejecución (verificable: árbol sin cambios).
- Reporte neutral de dominio (rutas/versiones/deltas; sin términos de negocio).
- Paridad `.py`↔`.ps1` (mismo reporte para los mismos fixtures).
- Golden cases: instancia desfasada (deltas no vacíos) y al día (sin deltas) con salida esperada.

## linked_decisions
- `DECISION-0006`: §4 es la fuente de esta spec.
- `DECISION-0001`: la herramienta informa, la instancia adopta por decisión; aditivo ⇒ MINOR.

## test_plan
- Fixture `examples/upgrade_cases/outdated_instance/` (subconjunto de masters de versión previa) ⇒
  reporte con deltas esperados; verificar que el árbol del fixture no cambia tras ejecutar.
- Fixture `examples/upgrade_cases/current_instance/` (igual al master) ⇒ reporte sin deltas.
- Comparar salida `.py` vs `.ps1` para ambos fixtures (paridad).

## closure_criteria
- Herramienta funcional con reporte de adopción; instancia intacta (read-only) demostrado.
- Preserva gobernanza por-decisión (DECISION-0001).
- Handoff mapea cada acceptance/closure a evidencia; revisión cruzada del arquitecto OK; claim liberado.

## Risks
- Comparación por contenido sensible a fin de línea/whitespace ⇒ falsos `cambiado`. Mitigación:
  normalizar EOL antes de comparar.
- Mapeo de CHANGELOG entre versiones frágil. Mitigación: best-effort; si no resuelve, omitir esa
  columna sin fallar.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Reporta deltas del conjunto adoptable | TASK-0019 | fixture outdated | deltas esperados en reporte |
| No modifica la instancia | TASK-0019 | árbol sin cambios tras run | read-only demostrado |
| Paridad .py/.ps1 | TASK-0019 | mismo reporte py vs ps | paridad confirmada |
