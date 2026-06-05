---
decision_id: DECISION-0008
title: Eficiencia de tokens medida y crecimiento acotado del estado
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0005, DECISION-0001, DECISION-0006, TASK-0022]
phase: P2
---

# DECISION-0008 — Eficiencia de tokens medida y crecimiento acotado del estado

## Contexto

DECISION-0005 introdujo "comunicación compacta token-efficient", pero su eficacia **nunca se
midió**. Una medición sobre el dogfooding de este repo (2026-06-05) muestra que el supuesto está
mal calibrado:

| Indicador medido | Valor | Lectura |
|------------------|-------|---------|
| Overhead frontmatter/cuerpo en mailbox (18 msgs) | **1,92** (66% relleno) | El "mensaje compacto" gasta 2/3 en metadatos |
| `CLAIMS.json` | ~10.846 tok, 34 claims, **1 activo** | **97% es historia `released`** releída en cada coordinación |
| `TASK_INDEX.json` | ~10.525 tok | Tareas `done` nunca se podan |
| Cold-start (AGENTS + estado) | **~25k tok** | Y **crece monótonamente** (append-only) |

**Conclusión:** el costo dominante de "comunicación" no son los mensajes, es la **re-lectura de
estado append-only que crece sin techo**. La compacidad de mensajes optimiza la parte pequeña.

## Principio

**La eficiencia se mide, no se asume; y los artefactos canónicos no crecen sin acotar.** Toda
afirmación de eficiencia se respalda con una medición *antes/después* reproducible.

## Decisión

### 1. Medición reproducible (gate antes/después)
- Herramienta `scripts/measure_context_cost.py` (+ `.ps1`, paridad) que reporta, de forma
  determinista: costo del **cold-start** (lista de lectura de AGENTS §0), **peso muerto** del estado
  (% `released` en claims, % `done` en tareas), y **overhead de frontmatter** del mailbox.
- Metodología explícita (tokens ≈ chars/divisor configurable; es un proxy, no facturación).
- Toda tarea que diga "mejora eficiencia" reporta **baseline → delta** con esta herramienta; el
  CHANGELOG cita el número (p.ej. "cold-start 25k→15k, −40%").

### 2. Crecimiento acotado del estado (poda a histórico)
- Los claims `released` y las tareas `done` se **archivan** fuera de los archivos calientes
  (p.ej. `CLAIMS_ARCHIVE.json`, `TASK_INDEX_ARCHIVE.json`), preservando trazabilidad (no se borran).
- Los archivos calientes (`CLAIMS.json`, `TASK_INDEX.json`) cargan solo lo **activo/reciente**.
- El validador debe seguir verde y la trazabilidad intacta (puede leer el histórico bajo demanda).
- **Aditivo y sin pérdida**: archivar ≠ borrar.

### 3. Frontmatter de mailbox mínimo
- Conjunto **obligatorio** reducido (lo que el validador realmente parsea) + opcionales **omitibles**
  cuando son `none`/vacíos. No emitir campos vacíos.
- **Compatibilidad hacia atrás:** mensajes históricos (frontmatter completo) siguen válidos.

### 4. (Opcional) Presupuesto de tokens en CI
- `measure_context_cost` corre en CI; WARNING (no error) si el cold-start supera un presupuesto
  declarado en `protocol.config`. Endurecer a error sería decisión aparte.

### 5. Versionado y neutralidad (DECISION-0001)
Todo es **aditivo** ⇒ **MINOR, target v0.7.0**: herramienta nueva, archivado sin pérdida, template
adelgazado compatible. Cambiar campos **obligatorios** del mensaje de forma incompatible sería
MAJOR. Neutral de dominio.

## Backlog
- **TASK-0022** (Claude, analysis): diseño + specs (medidor, poda, frontmatter mínimo) + captura del
  **baseline** actual. Desbloquea a Codex.
- Implementación (Codex, tras specs): medidor `measure_context_cost.*`; poda a histórico; frontmatter
  mínimo + validador.

## Consecuencias
- **Positivas:** el cold-start deja de crecer sin control; las afirmaciones de eficiencia se vuelven
  verificables; menos tokens por coordinación a lo largo de la vida del proyecto.
- **Costo:** un medidor y un esquema de archivado a mantener (con paridad `.py`/`.ps1`); disciplina
  de reportar deltas.
- **Seguimiento:** TASK-0022 y su backlog; la capa se publica como **v0.7.0**.

## Alternativas consideradas
- **No medir y solo adelgazar mensajes:** descartado — la medición muestra que el ahorro está en el
  estado, no en los mensajes; sin medir, se optimiza lo que no mueve la aguja.
- **Borrar historia (claims/tasks) en vez de archivar:** descartado — rompe trazabilidad y auditoría.
- **Endurecer presupuesto a error de build ya:** descartado por ahora (frágil); empezar en WARNING.
