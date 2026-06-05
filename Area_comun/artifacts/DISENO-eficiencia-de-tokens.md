# DISEÑO — Eficiencia de tokens medida

> Entregable de **TASK-0022** (Claude, `analysis`). Implementa [DECISION-0008](../decisions/DECISION-0008-eficiencia-de-tokens.md).
> Fuente de verdad para SPEC-0023/0024/0025. Neutral de dominio. Capa target **v0.7.0** (MINOR, aditivo).

## 0. Resumen
Tres palancas con un gate de medición. **El baseline manda la prioridad:** el 75% del cold-start es
re-leer estado histórico → la **poda** (§2) es el mayor impacto; el frontmatter (§3) es secundario.

## 1. Baseline medido (2026-06-05, divisor 4, tokens≈chars/4 — proxy)

| Escenario | Indicador | **Antes** | Predicho (después) | Δ |
|-----------|-----------|-----------|--------------------|---|
| A cold-start | total lectura AGENTS §0 | **29.169 tok** | ~7.500 | **−74%** |
| A | └ CLAIMS.json | 11.233 (36 claims, 100% released) | ~500 | −96% |
| A | └ TASK_INDEX.json | 10.842 (22 tareas, 95% done) | ~1.500 | −86% |
| C mailbox | overhead frontmatter | ratio 1,9 (65% relleno) | ~35% | ~−45% relleno |

Método: `tokens = chars / divisor`; divisor configurable (`token_cost.chars_per_token`, def 4). Es un
**proxy** del contexto cargado, no facturación. La columna "después" se **rellena con medición real**
tras implementar (no se da por buena la predicción).

## 2. §2 — Poda de estado a histórico (mayor impacto) → SPEC-0024

**Modelo de dos archivos, sin pérdida:**
- `Area_comun/state/CLAIMS.json` (caliente) conserva solo claims **`active`** (+ opcional: los N más
  recientes `released`). El resto va a `Area_comun/state/CLAIMS_ARCHIVE.json` (mismo schema).
- `Area_comun/state/TASK_INDEX.json` (caliente) conserva tareas **no `done`** (+ opcional ventana
  reciente). Las `done` van a `Area_comun/state/TASK_INDEX_ARCHIVE.json`.
- **Archivar ≠ borrar:** trazabilidad intacta; el histórico es consultable.

**Contrato con el validador (clave):**
- El validador lee **caliente ∪ archivo** para sus chequeos (consistencia índice↔task-file,
  referencias `depends_on`/`relates_to`, etc.) → **no pierde cobertura**.
- El ahorro de tokens es a nivel de **coordinación de agentes** (que leen solo lo caliente), no del
  validador (CI puede pagar leer ambos).

**Protocolo (AGENTS §0):** la secuencia de cold-start apunta a los archivos **calientes**; el
histórico se lee **bajo demanda**. Cambio aditivo en docs.

**Migración inicial:** un paso único mueve los `released`/`done` actuales a los `*_ARCHIVE.json`.

## 3. §3 — Frontmatter de mailbox mínimo → SPEC-0025

- **Obligatorio** (lo que el validador parsea): `message_id`, `type`, `task_id`, `from`, `to`,
  `status`, `one_line_summary`; y **condicional**: si `requires_response: true` ⇒ `requested_action`
  + `question` (regla existente, intacta).
- **Opcionales omitibles** cuando son `none`/vacíos: `response_owner`, `requested_action`/`question`
  (si no aplica), `context_refs`/`changed_refs`/`validation_refs`, `deadline_or_blocking_level`,
  `requires_response` (si false por defecto).
- **No emitir campos vacíos.** Un FYI mínimo baja de ~25 líneas de frontmatter a ~7.
- **Compatibilidad hacia atrás:** mensajes históricos con frontmatter completo siguen válidos; el
  validador **no exige** los campos omitidos.

## 4. §1 — Medidor `measure_context_cost` → SPEC-0023
- `scripts/measure_context_cost.py` + `.ps1` (paridad). Lee `protocol.config` →
  `token_cost` (`chars_per_token`, `coldstart_globs`, opcional `budget`).
- Reporta los 3 escenarios (cold-start, peso muerto de estado, overhead frontmatter) de forma
  **determinista**; salida humana + `--json` máquina. Exit 0 (es un reporte); con `--budget` y
  cold-start > presupuesto ⇒ exit configurable (WARNING por defecto).
- Es la herramienta del **gate antes/después**: toda tarea de eficiencia reporta su delta con ella.

## 5. §4 — Presupuesto en CI (opcional)
`validate.yml` corre `measure_context_cost --budget` y **avisa** (no rompe) si el cold-start regresa
sobre el presupuesto declarado. Endurecer a error sería decisión aparte.

## 6. Índice de specs / rollout
| Tarea | spec_id | Tipo | Lever |
|-------|---------|------|-------|
| TASK-0023 | `Area_comun/specs/SPEC-0023-medidor-context-cost.md` | implementation | §1/§4 medidor (+budget CI) |
| TASK-0024 | `Area_comun/specs/SPEC-0024-poda-estado-historico.md` | implementation | §2 poda (mayor impacto) |
| TASK-0025 | `Area_comun/specs/SPEC-0025-frontmatter-minimo.md` | implementation | §3 frontmatter mínimo |

Orden recomendado: **TASK-0023 (medidor) primero** (sin él no hay before/after), luego **0024 (poda)**
—mayor ahorro—, luego **0025 (frontmatter)**. Cada una reporta delta medido; al cerrarlas, **v0.7.0**.

## 7. Neutralidad y versionado
Todo proceso/tooling, **neutral de dominio**. Aditivo ⇒ MINOR v0.7.0. Cambiar campos **obligatorios**
de mensaje o endurecer el presupuesto a error sería MAJOR.
