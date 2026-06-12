---
decision_id: DECISION-0030
title: Slim-views del estado y politica de cold-start just-in-time (mitigacion de context rot)
status: accepted
date: 2026-06-13
ratified_at: 2026-06-13
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0005, DECISION-0008, DECISION-0009, DECISION-0014, DECISION-0017, DECISION-0022]
phase: P2
---

# DECISION-0030 - Slim-views del estado y politica de cold-start just-in-time

> Estado: PROPOSED (2026-06-13). Redactada por Claude (architect). Requiere GO del operador y
> convergencia de implementacion con Codex (patron DECISION-0014). Aditiva y off-by-default por
> instancia: las slim-views se materializan apagadas hasta que el medidor confirme el delta; el cambio
> de `coldstart_globs` se promueve en un paso medido antes/despues (DECISION-0008). SemVer: MINOR al
> liberar. Nucleo neutral de dominio: sin cambios de frontera.

## Contexto

DECISION-0008 acoto el crecimiento del estado archivando `done`/`released` (archive != delete) y
DECISION-0014 hizo ese mantenimiento sistematico por umbral medido. Ambas reducen el **peso muerto**.
Persiste un problema distinto: el cold-start carga los archivos calientes **completos**
(`TASK_INDEX.json`, `PROJECT_STATE.json`, `CLAIMS.json`) con todos sus campos por entrada, y el agente
re-lee ese estado en cada turno. La medicion de DECISION-0014 mostro re-acumulacion a ~19.5k tokens
incluso tras poda. Es decir: el costo dominante ya no es el peso muerto (acotado) sino **cuanto del peso
vivo se vuelca al contexto en cada arranque**.

Ademas, `runtime/state/events.jsonl` es append-only y crece sin techo (342 eventos al 2026-06-12). Existe
`snapshot.json`, pero no hay politica explicita que prohiba que el log entre al cold-start.

Investigacion externa (2026-06-13) converge en el diagnostico y las palancas:

- **Anthropic - context engineering:** el "context rot" degrada la recuperacion a mas tokens; la atencion
  es un presupuesto finito. Palancas: **just-in-time retrieval** (mantener identificadores ligeros y
  cargar bajo demanda), **compaction / tool-result clearing**, **structured note-taking / memory** y
  **sub-agentes** con ventana limpia que devuelven resumenes destilados (1-2k tokens).
- **OpenAI - Agents SDK:** trimming de las ultimas N turnos, rolling summary, separacion multi-agente,
  estado persistente fuera de la ventana.
- **Referencia `code-review-graph` (tirth8205):** patron "contexto minimo primero" (~100 tokens) +
  retrieval bajo demanda por blast-radius + tool filtering. Ataca el contexto de **codigo**, no el de
  estado del protocolo, por lo que NO es remedio directo aqui; se adopta el patron, no la herramienta.

## Principio

**El cold-start carga vistas compactas derivadas, no fuentes de verdad completas; el detalle se recupera
just-in-time.** Toda reduccion se respalda con medicion antes/despues (DECISION-0008).

## Decision (nucleo)

1. **Slim-views materializadas (proyecciones derivadas, no fuentes de verdad).** El runtime materializa,
   junto a las vistas full, versiones compactas regenerables:
   - `TASK_INDEX.slim.json`: solo tareas en estados calientes; por tarea solo
     `{id, status, owner, phase, priority, title, blocked_by_questions?}`. Se omiten
     `deliverables`, `relevant_files`, `relates_to`, `linked_decisions` (se leen on-demand del
     `TASK-XXXX.md`).
   - `PROJECT_STATE.slim.json`: narrativa recortada a las ventanas `recent_*` ya definidas en
     `maintenance`; `active_tasks` reducido a `{id, status, owner, title}`.
   - `CLAIMS.slim.json`: solo claims `active`, con `{claim_id, task_id, owner, scope}`.
   Regla dura: las slim-views son **derivadas, regenerables y sin perdida** (el full y el archive siguen
   siendo autoritativos). No se editan a mano ni se reclaman por scope.

2. **Politica de cold-start just-in-time.** `coldstart_globs` apunta a las `*.slim.json` + `AGENTS.md` +
   `Area_comun/README.md` + `Area_comun/protocol/TASK_PROTOCOL.md`; **deja de cargar** los archivos full
   y el event log. El agente arranca con IDs/titulos/estado y lee el `TASK-XXXX.md`, `DECISION-XXXX.md` o
   handoff concreto bajo demanda, usando su scope/claim (las rutas y nombres ya dan las senales de
   relevancia).

3. **El event log nunca al cold-start.** `snapshot.json` es la base de arranque; `events.jsonl` se
   consulta solo para auditoria/replay bajo demanda. Se define rotacion/segmentado del log (sigue siendo
   append-only e integro; simplemente jamas entra al contexto de arranque).

4. **Compaction y tool-result clearing en turnos del runtime.** Una vez consumido el resultado de una
   lectura/tool, se descarta el contenido crudo conservando el registro de que ocurrio (apoyado en
   context editing del Developer Platform donde aplique). Los handoffs autocontenidos ya son
   note-taking; se formaliza un **resumen destilado al cerrar cada tarea** (converge con el reporte
   humano de cierre, regla 7 de CLAUDE.md).

5. **Sub-agentes para trabajo profundo.** El orquestador mantiene plan ligero; los sub-agentes exploran o
   implementan con ventana limpia y devuelven solo un resumen (1-2k tokens), aislando el contexto pesado.

6. **Integridad anti-drift (innegociable).** Las slim-views se materializan en el **mismo ciclo**
   `materialize_to_disk` que las full (escritor unico, DECISION-0022) y el verificador de drift las
   cubre: una slim-view nunca puede divergir del estado autoritativo. Si una slim-view no es regenerable
   identica desde el snapshot, el submit aborta con rollback (como ya hace ante drift).

7. **Gate de medicion (antes/despues).** `scripts/measure_context_cost` reporta cold-start con full-views
   vs slim-views; objetivo de referencia: cold-start **< 10k tokens** con slim (vs ~19.5k actual), sin
   perder trazabilidad. El cambio de `coldstart_globs` solo se promueve si el delta se confirma.

## Versionado y neutralidad (DECISION-0001)

Aditivo: vistas derivadas nuevas + politica de carga + rotacion de log. **MINOR.** Las slim-views son
genericas (proyecciones de campos), neutral de dominio; se publican tambien en los masters
(`protocol.config.template.json`, `Area_comun/state/*.template.json`). Sin secretos en el repo.

## Consecuencias

- **Positivas:** el cold-start deja de cargar peso vivo completo; menor context rot y mas presupuesto de
  atencion por turno; trazabilidad intacta (full + archive + log siguen siendo autoritativos y
  auditables bajo demanda).
- **Costo:** materializar y versionar N vistas derivadas; extender el drift checker para cubrirlas; el
  retrieval just-in-time es algo mas lento que precargar (compensa en horizonte largo).
- **Relacion:** complementa DECISION-0008 (acota tamano) y DECISION-0014 (poda sistematica). 0008/0014
  reducen el peso muerto; 0030 reduce cuanto del peso vivo se carga. DECISION-0017 (event log writer)
  queda complementada por la politica de no-cold-start del log.

## Alternativas consideradas

- **Solo seguir podando (0008/0014):** descartada como suficiente; la medicion muestra re-acumulacion del
  peso vivo aunque el peso muerto este acotado.
- **Esperar ventanas de contexto mas grandes:** descartada; el context rot persiste a cualquier tamano
  (atencion finita), y la auditoria exige senal alta, no volumen.
- **Adoptar `code-review-graph` como remedio:** descartada como fix directo (ataca contexto de codigo, no
  de estado del protocolo); se adopta solo el patron "minimo primero + retrieval bajo demanda + tool
  filtering". Reevaluable si los agentes pasan a leer mucho codigo fuente del proyecto real.
- **Slim-views editables / como fuente de verdad:** descartada; romperia el escritor unico y la
  auditabilidad. Deben ser estrictamente derivadas y regenerables.

## Backlog (deriva, pendiente de GO)

- SPEC (Claude): contrato de cada slim-view (campos exactos, estados calientes incluidos), extension del
  drift checker, ajuste de `coldstart_globs`, golden cases.
- Implementacion (Codex, tras SPEC): materializacion de slim-views en `materialize_to_disk`, rotacion de
  `events.jsonl`, medicion antes/despues. Off-by-default; encendido opt-in tras delta confirmado.

## Referencias externas

- Anthropic, "Effective context engineering for AI agents" (2025-09-29).
- Anthropic, "Context management: memory tool + context editing" (Claude Developer Platform).
- OpenAI Agents SDK Cookbook, "Short-Term Memory Management with Sessions" / "Long-Term Memory Notes".
- tirth8205/code-review-graph (GitHub) - patron de retrieval por blast-radius y tool filtering.
