# Reconciliacion de la hoja de ruta vs estado real del repo (2026-06-14)

> Artefacto de seguimiento versionado (TASK-0112, analysis). Reconcilia la "sintesis_hoja_de_ruta"
> (HTML externo, escrita 2026-06-12 sobre protocol v1.1.0 / runtime v0.11.0) contra el repo vivo.
> Base de verificacion read-only: **HEAD 26b081b** (protocol v1.5.0). Publicado tras el aterrizaje
> dormido de #3 (HEAD 1307635). Reemplaza al adjunto externo como mapa de "que sigue".
> Autor: Claude (architect). Fuente operador: personal/operador/04_Asistente_reconciliacion-hoja-de-ruta.md.

## 1. Desfase de cabecera

La hoja se escribio sobre **protocol v1.1.0 / runtime v0.11.0**; el repo va por **v1.5.0**
(runtime 0.12.0). Entre medias (2026-06-13) entraron 4 releases (1.2.0-1.5.0) por un carril que la
hoja NO lista (mitigacion de contexto + autonomia). Como mapa de "que sigue", la hoja estaba
desactualizada.

## 2. Mapa por fase (HECHO / PARCIAL / EN CURSO / NO) con evidencia (verificado en vivo)

| Fase | Item | Estado | Evidencia (read-only, HEAD 26b081b) |
|------|------|--------|--------------------------------------|
| 0 | E5 - FAILURE_MODES.md (catalogo modos de fallo) | NO | `Area_comun/protocol/FAILURE_MODES.md` no existe |
| 0 | E6 - test "merece un loop?" (gobernador) | NO | sin las 4 condiciones en `TASK_PROTOCOL.md` (0 matches) |
| 0 | #1 - MAST sobre el historial | NO | `protocol_research/` no existe |
| 1 | E1 - Skill registry + digestion | NO | sin `skill_registry` en config (0); sin contrato `SKILL` |
| 2 | E2 - Connectors / MCP | NO | `runtime/adapters/` = base/llm_adapter/replay; sin bloque `connectors` |
| 3 | #2 - PROV-AGENT (eventlog -> W3C PROV) | NO | sin `protocol_research/`; sin exporter PROV |
| 3 | #3 - Cost-attribution por handoff | **EN CURSO** | DECISION-0033 + SPEC-0079 + TASK-0111 (`in_progress`); golden `runtime_cost_attribution_cases` 6/6; aterrizado DORMIDO off-by-default; pendiente revision Codex + activacion bajo GO |
| 3 | #4 - Atestacion de autoria (prev_hash + firma + anclaje) | HECHO, off-by-default | `eventlog.py`: `compute_event_prev_hash`, `agent_signatures_enabled`, `anchor_enabled/anchor_config` (12 matches); `scripts/generate_provenance.py` + `sign_release.py` existen; flags chain/agent_sig/anchor=false; DECISION-0023/0028/0029 |
| 4 | E3 - Scanners (discovery) | NO | sin bloque `discovery_scanners` |
| 5 | E7 - Perfil self-validation (software) | NO | solo `profiles/dotnet_enterprise`; sin `software_runtime` |
| 5 | E4 - Review-risk gate + troceo | PARCIAL | `quality_policy` vivo: `max_review_cycles=3, max_qa_cycles=3, allow_self_review=false, allow_self_qa=false, escalate_to_architect_before_human=true`; falta el troceo por tamano/areas explicito |
| 5 | E8 - Notacion EARS / Gherkin | NO | sin templates EARS/Gherkin en `Area_comun/specs/` |
| 5 | E9 - Git worktrees (aislamiento FS) | **NO (corregido)** | `runtime/vcs.py` SOLO tiene `discard_worktree_changes` = `git restore --staged . && git restore .` (descarte del working-tree), NO `git worktree add` (aislamiento FS). El grep de la hoja dio falso positivo por el nombre de la funcion. **Correccion: PARCIAL -> NO.** |
| 6 | TFM (PRE-REG, H1/H2/H3, #7) | NO | `protocol_research/` no existe |

## 3. Correcciones a la lectura del asistente (verificacion del architect)

1. **E9 = NO**, no PARCIAL: el unico match de "worktree" es `discard_worktree_changes` (git restore),
   no aislamiento FS por git-worktree. Es la unica discrepancia hallada; el resto de afirmaciones del
   asistente (02/04) se sostienen contra el repo vivo.
2. **#3 = EN CURSO**, no NO: aterrizado dormido en esta sesion (off-by-default; pendiente revision Codex
   y activacion bajo GO). Marcarlo HECHO solo tras verificacion EN CALIENTE (drift 0, replay==hot) +
   activacion (flag true + MINOR 1.6.0 + CHANGELOG).
3. **HEAD**: la cabecera de la hoja y los docs del asistente citaban 237f04d; el HEAD real de
   verificacion fue 26b081b; tras el aterrizaje de #3, 1307635.

## 4. Lo que SI se entrego (carril fuera de la hoja, v1.2-1.5)

- v1.2.0 + v1.3.0: narracion minima intra-ejecucion (Addendum DECISION-0005).
- v1.4.0: compaction / tool-result clearing activado y medido (SPEC-0078, `compaction_enabled=true`, warn 16000).
- v1.5.0: architect cierra sus analysis-tasks (DECISION-0032).
- Transversal: slim-views + cold-start (DECISION-0030); enforce/authoritative writer unico
  (DECISION-0022/0028); autonomia supervisada SA.1-4 (DECISION-0024) + piloto SA.4 autorizado pero
  loop OFF (DECISION-0027); #4 atestacion de autoria off-by-default (DECISION-0029).

Lectura: el equipo priorizo "mitigar llenado de contexto" + preparar autonomia sobre el orden
Fase 0->1->2 de la hoja. Efecto colateral util: el nucleo de la tesis (#4) ya esta casi listo, solo
pendiente de ACTIVAR (flags) y medir bajo GATE-DATASET.

## 5. Re-secuencia recomendada (alineada al plan aprobado por el operador)

1. [hecho, este doc] Reconciliar la hoja al estado real.
2. **#3 cost-attribution**: aterrizado dormido; cerrar con revision de Codex + activacion EN CALIENTE bajo GO.
3. **Piloto SA.4 medido** (DECISION-0027: tarea de bajo riesgo, caps 2/1/180000, checkpoint tras turno 1)
   con #3 activo -> revisar metricas. Solo PREPARAR; disparo = micro-GO del operador.
4. **GATE** (piloto estable + decision nueva + GO): ampliar ventana para que el loop ejecute, por el
   metodo y en orden: Fase 0 (E5/E6) -> Fase 1 (E1 Skills) -> Fase 2 (E2 Connectors).

Notas:
- #4 ya construido: cuando interese la via tesis, falta ACTIVAR (`agent_signatures_enabled`/`anchor_enabled`)
  y medir bajo GATE-DATASET (legal/RGPD + Ley 1581), no construir desde cero.
- #1 (MAST) y `protocol_research/` siguen pendientes (win de investigacion mas barato segun la hoja).
- E4/E9 confirmados: E4 PARCIAL (quality_policy sin troceo explicito), E9 NO (sin aislamiento por worktrees).
- Innegociables: mutaciones solo por submit_intent (escritor unico); SA.4 sola en su ventana;
  enforce/authoritative intactos; subagents_enabled false; neutralidad de dominio; ningun numero no medido.
