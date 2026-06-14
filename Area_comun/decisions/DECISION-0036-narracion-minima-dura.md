---
decision_id: DECISION-0036
title: Narracion minima como regla DURA y uniforme para todos los agentes (afila addendum DECISION-0005)
status: accepted
date: 2026-06-14
ratified_at: 2026-06-14
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0005, DECISION-0018]
phase: P2
---

# DECISION-0036 - Narracion minima DURA y uniforme

> Estado: ACCEPTED (ratificada por el operador 2026-06-14, tras pasada del analista que dio
> RATIFICABLE-con-ajustes; ambos ajustes incorporados). Cambio ADITIVO, documental, neutral. Afila el
> addendum de narracion minima de DECISION-0005 (2026-06-13) para que sea regla DURA y uniforme para TODOS
> los agentes. NO toca #3/flag, #4/chain-auth, SA.4.

## Contexto

El addendum de DECISION-0005 (AGENTS.md s.7) ya pide "minimizar la narracion intra-ejecucion". En la
practica resulto demasiado blando: el arquitecto (Claude, interactivo) narro paso a paso (una frase antes
de cada tool call) pese a la regla y a una memoria personal dedicada. El operador pidio enforcement DURO y
uniforme. La memoria personal de un agente NO se propaga a los demas (cada uno tiene la suya); el unico
lever que bindea a todos es el contrato compartido AGENTS.md.

## Decision

Se afila el addendum de narracion minima de DECISION-0005 en el contrato compartido (AGENTS.md s.7 y su
master AGENTS.template.md), con el siguiente texto de reemplazo:

> - **Minimal narration (DECISION-0005 addendum 2026-06-13; sharpened DECISION-0036 2026-06-14):** during
>   execution every agent emits **zero intra-execution narration** -- no prose announcing or recapping a
>   step before/after a tool call ("now I do X", "I verify Y", "next I will Z"). **Process** reasoning
>   (step announcements/recaps) stays in the agent's internal/reasoning channel, not in user-facing
>   output; chained actions carry no prose between them. User-facing output is reserved for **one
>   self-contained final report/handoff**, which
>   prevails. This binds **all agents uniformly**. Carve-outs (unchanged): substantive content where the
>   reasoning IS the deliverable (analysis, review voices, specs, decisions) and **one** genuine blocking
>   question are always allowed; brevity never sacrifices completeness or auditability. A persistent
>   step-by-step narration pattern is a flaggable process anomaly (DECISION-0018).

## Alcance / No-alcance

- **En alcance:** reemplazar el bullet de narracion minima en AGENTS.md s.7 y AGENTS.template.md s.7;
  DECISION-0036; SemVer MINOR + CHANGELOG. Aplica a Claude, Codex y analista por igual.
- **Fuera de alcance:** no se anade mecanismo automatico (la narracion es output del modelo, no gateable
  por validador hoy); el enforcement es normativo + via peer-flag (DECISION-0018). No se tocan carve-outs
  (contenido sustantivo + pregunta de bloqueo). No toca #3/#4/SA.4 ni neutralidad.

## Versionado y neutralidad (DECISION-0001)

Aditivo (afila una regla existente; no remueve comportamiento ni carve-outs). **MINOR** (v1.9.0). Neutral
de dominio; sin secretos.

## Consecuencias

- Todos los agentes quedan obligados por el mismo texto duro (no depende de la memoria personal de cada
  uno). La memoria personal sigue como refuerzo, pero la fuente de verdad es AGENTS.md.
- Una violacion persistente (narrar paso a paso) es anomalia notificable (DECISION-0018): el peer/operador
  la marca; no se "cae en silencio".
- Se preservan los carve-outs: el contenido sustantivo y la pregunta de bloqueo concreta siguen permitidos.
- **Honesto (necesario-no-suficiente):** afilar la redaccion no es el teeth por si solo -- el detonante fue
  narrar PESE a la regla y a una memoria personal, asi que el binding constraint es el cumplimiento. El
  teeth real es el peer-flag (DECISION-0018) EJERCIDO; este afilado solo elimina la ambiguedad que daba
  cobertura al lapso.

## CHANGELOG (draft)

```markdown
## [1.9.0] - 2026-06-14

**Minimal narration hardened to a uniform hard rule for all agents (DECISION-0036).** Additive,
documentation-only; sharpens the DECISION-0005 narration addendum. Domain-neutral.

### Changed
- AGENTS.md s.7 + AGENTS.template.md s.7: the minimal-narration bullet now requires **zero
  intra-execution narration** (no prose between tool calls; reasoning to the internal channel; output
  reserved for one self-contained final report), binding **all agents uniformly**, with unchanged
  carve-outs (substantive content + one blocking question) and a flaggable-anomaly clause (DECISION-0018).
```

## Acceptance (estructural)
- AGENTS.md s.7 y AGENTS.template.md s.7 contienen el texto afilado (zero intra-execution narration +
  "all agents uniformly" + carve-outs intactos + clausula de anomalia).
- DECISION-0036 registrada por escritor unico; MINOR 1.9.0 + CHANGELOG; protocol_version 1.8.0 -> 1.9.0.
- Neutralidad/validador/encoding verdes; drift 0.
