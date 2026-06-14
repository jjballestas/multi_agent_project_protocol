# 04_Asistente - Reconciliacion de la hoja de ruta vs estado real del repo

> Insumo del operador (asistente Cowork). Verificacion read-only a HEAD 237f04d (protocol v1.5.0).
> Es el Paso 1 del plan aprobado. El arquitecto puede commitear esto como tracking actualizado.
> Fecha: 2026-06-14. Fuente: sintesis_hoja_de_ruta (escrita 2026-06-12 sobre v1.1.0/runtime v0.11.0).

## 1. Desfase de cabecera
La hoja se escribio sobre **protocol v1.1.0 / runtime v0.11.0**. El repo va por **v1.5.0**.
Entre medias (2026-06-13) entraron 4 releases (1.2.0-1.5.0) por un carril que la hoja NO lista
(mitigacion de contexto + autonomia). La hoja, como mapa de "que sigue", esta desactualizada.

## 2. Mapa por fase (HECHO / PARCIAL / NO) con evidencia

| Fase | Item | Estado | Evidencia (read-only) |
|------|------|--------|------------------------|
| 0 | E5 - FAILURE_MODES.md (catalogo modos de fallo) | NO | `Area_comun/protocol/FAILURE_MODES.md` no existe |
| 0 | E6 - test "merece un loop?" (gobernador) | NO | sin las 4 condiciones en `TASK_PROTOCOL.md` |
| 0 | #1 - MAST sobre el historial | NO | `protocol_research/` no existe |
| 1 | E1 - Skill registry + digestion | NO | sin `skill_registry` en config; sin contrato `SKILL` |
| 2 | E2 - Connectors / MCP | NO | `runtime/adapters/` = base/llm/replay; sin bloque `connectors` |
| 3 | #2 - PROV-AGENT (eventlog -> W3C PROV) | NO | sin `protocol_research/`; sin exporter PROV |
| 3 | #3 - Cost-attribution por handoff | NO | `budget.py`/`metrics.py`/`eventlog.py` existen (sustrato) pero sin imputacion por handoff |
| 3 | #4 - Atestacion de autoria (prev_hash + firma por agente + anclaje) | HECHO, off-by-default | `eventlog.py`: `compute_event_prev_hash`, `agent_signatures_enabled`, `anchor_enabled`/`anchor_config`; `scripts/generate_provenance.py` + `sign_release.py`; DECISION-0023/0028/0029 |
| 4 | E3 - Scanners (discovery) | NO | sin bloque `discovery_scanners` |
| 5 | E7 - Perfil self-validation (software) | NO | solo `profiles/dotnet_enterprise`; sin `software_runtime` |
| 5 | E4 - Review-risk gate + troceo | PARCIAL | `quality_policy.max_review_cycles=3` en config; troceo por tamano/areas a verificar |
| 5 | E8 - Notacion EARS / Gherkin | NO | sin templates EARS/Gherkin en `Area_comun/specs/` |
| 5 | E9 - Git worktrees (aislamiento FS) | PARCIAL / verificar | `runtime/vcs.py` menciona worktree |
| 6 | TFM (PRE-REG, H1/H2/H3, #7) | NO | `protocol_research/` no existe |

## 3. Lo que SI se entrego (carril fuera de la hoja, v1.2-1.5)
- v1.2.0 + v1.3.0: narracion minima intra-ejecucion (Addendum DECISION-0005).
- v1.4.0: compaction / tool-result clearing activado y medido (SPEC-0078, `compaction_enabled=true`, warn 16000).
- v1.5.0: architect cierra sus analysis-tasks (DECISION-0032).
- Transversal: slim-views + cold-start (DECISION-0030); enforce/authoritative writer unico (DECISION-0022/0028);
  autonomia supervisada SA.1-4 (DECISION-0024) + piloto SA.4 autorizado (DECISION-0027, loop aun OFF);
  #4 atestacion de autoria construida off-by-default (DECISION-0029).

Lectura: el equipo priorizo "mitigar llenado de contexto" + preparar autonomia, no el orden Fase 0->1->2 de la hoja.
Efecto colateral util: el nucleo de la tesis (#4) ya esta casi listo, solo pendiente de activar/medir bajo GATE-DATASET.

## 4. Re-secuencia recomendada (alineada al plan aprobado)
1. [este doc] Reconciliar la hoja al estado real.
2. Construir #3 (cost-attribution por handoff) - ver orden 03. Medicion viva antes del piloto.
3. Piloto SA.4 medido (DECISION-0027: tarea bajo riesgo, caps 2/1/180000, checkpoint tras turno 1) con #3 activo -> revisar metricas.
4. GATE (piloto estable + decision nueva + GO): ampliar ventana para que el loop ejecute, por el metodo y en orden:
   Fase 0 (E5/E6) -> Fase 1 (E1 Skills) -> Fase 2 (E2 Connectors).

Notas para no perder de vista:
- #4 ya construido: cuando interese la via tesis, falta ACTIVAR (flags `agent_signatures_enabled`/`anchor_enabled`)
  y medir bajo GATE-DATASET (legal/RGPD + Ley 1581), no construir desde cero.
- #1 (MAST) y `protocol_research/` siguen pendientes y son el win de investigacion mas barato segun la hoja.
- E4/E9 estan parciales: confirmar alcance antes de re-listarlos como "por hacer".

## 5. Sugerencia de tracking
La hoja es un HTML subido, no vive en el repo. Recomiendo que el arquitecto publique este estado como
documento de seguimiento versionado (p.ej. en `Area_comun/artifacts/`), y que futuras fases marquen estado ahi,
para que el mapa deje de depender de un adjunto externo.
