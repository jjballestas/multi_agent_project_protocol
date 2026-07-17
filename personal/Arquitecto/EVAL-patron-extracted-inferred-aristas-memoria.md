# EVAL - Patron de etiquetado epistemico de aristas (EXTRACTED vs INFERRED + confianza)

- Fecha: 2026-07-17. Autor: Arquitecto. Estado: POSICION OBJETABLE (pre-refutacion del Analista).
- Origen: DIRECTIVA MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-evaluar-patron-extracted-inferred-memoria.
- Contexto: SPEC-MEMORIA-HIBRIDA v0.2.0 (s.3 DDL, s.6 round-trip, s.7 PII, s.12 contradicciones, s.13 fases).
- Firewall: soporte a decision del operador; NO citable; DECISION-0081 intacta (cero dependencia externa).

## 1. Que dice hoy la SPEC (hechos verificados)

- `artifact_edges` (SPEC s.3): columnas from/to/edge_type/source_path/source_commit. La distincion
  hecho-del-canon vs deduccion-del-indexador NO existe como campo; es implicita en el edge_type.
- En F1-F3 TODAS las aristas son EXTRACTED por construccion: el indexador solo deriva aristas de
  frontmatter allowlisted (relates_to, linked_decisions, supersedes, implements...; SPEC s.5.1 + s.7).
  NO existe maquinaria de inferencia antes de Fase 4 (s.12 deteccion de contradicciones = F4; s.13).
- La semantica del patron YA esta implicita en s.12: separa (a) pares con edge `contradicts` explicito
  (canon) de (b) candidatos por heuristica textual (computados). Hoy esa separacion no tiene etiqueta
  formal en el modelo de datos ni en el output del reporte.
- Round-trip s.6: `artifact_edges` esta en la particion DERIVADA del dump canonico -> toda arista debe
  ser reconstruible byte-identica desde el canon. Una arista INFERRED solo cumple eso si la heuristica
  es determinista y versionada (mismo patron que `classifier_version` en pii_classification).

## 2. Analisis contra las restricciones duras de la DIRECTIVA

1. **Encaje en el DDL master unico (DECISION-0096, SPEC s.3):** CABE como campos del esquema unico.
   Forma concreta: en `artifact_edges` anadir
   `provenance TEXT NOT NULL DEFAULT 'extracted' CHECK (provenance IN ('extracted','inferred'))` +
   `inference_source TEXT` (id+version de la heuristica; NULL para extracted). CERO segundo esquema.
2. **Confianza continua (REAL 0..1): DESCARTAR.** Tres razones: (a) falsa precision -- una heuristica
   textual v1 no produce probabilidades calibradas, produce "matcheo el patron X"; (b) riesgo al
   round-trip byte-identico (formateo de floats); (c) lo epistemicamente informativo es QUE heuristica
   y QUE version produjo la arista (inference_source), no un numero. Si F4 necesita graduacion:
   tiers discretos (p.ej. hard/soft) dentro del CHECK, decidido en el diseno de F4.
3. **Valor en Fase A (F1): ~CERO con coste no-cero.** Sin productor de aristas INFERRED hasta F4, la
   maquinaria de etiquetado en F1 es peso muerto: mas superficie de tests, mas DDL que portar en el
   supersede del memdb (M6), cero filas que la usen. La deteccion de contradicciones que el patron
   fortalece es F4 por diseno de la propia SPEC.
4. **Coste de diferir: ~CERO.** La DB es cache gitignored reconstruible (I1/I5): anadir columnas en F4
   = bump de `PRAGMA user_version` + rebuild total (s.6), sin migracion de datos. El unico coste real
   de diferir es churn documental del DDL master; se mitiga con la reserva de campo (abajo).
5. **Procedencia del archivo frio (pack.manifest):** el patron NO aplica ahi -- el manifest registra
   artefactos (hechos: sha256, rutas, commits), no aristas derivadas. Mezclarlo seria scope creep.

## 3. RECOMENDACION (objetable)

**DIFERIR a Fase 4, con reserva de campo en el DDL v1 de F1 (papel, cero maquinaria):**

- (a) El DDL v1 que F1 construya incluye las 2 columnas (`provenance` default 'extracted',
  `inference_source` NULL) desde el dia 1. Coste: 2 lineas de DDL + 1 test de default. El indexador
  F1 NO las computa (todo es extracted por defecto). Evita churn del master y deja el hueco listo.
- (b) La MAQUINARIA del patron (etiquetar inferred, inference_source poblado, uso en el reporte de
  conflictos para separar conflicto-duro-del-canon vs candidato-heuristico) = F4, en el diseno de
  `report_memory_conflicts.py` (s.12), que debera priorizar extracted sobre inferred en su output.
- (c) Confianza numerica continua: DESCARTADA (s.2 punto 2). Graduacion discreta si F4 la justifica.
- (d) Nada de esto bloquea el arranque de Fase A ni toca hub/medidas; scope Nova-Payroll (Gate-1).

## 4. Pendiente

Refutacion adversarial del Analista (mandato: argumentar EN CONTRA -- sobre-ingenieria, coste vs valor
en Fase A, riesgo al DDL master; y atacar especificamente la "reserva de campo" de 3a: si tambien la
reserva es peso muerto, la recomendacion colapsa a diferir-limpio sin tocar el DDL v1). El veredicto
se integra a la RESP final al operador.
