---
message_id: MSG-20260619-Arquitecto-to-Operador-proyecto-front-t0-confirm
type: RESPONSE
task_id: none
from: Arquitecto
to: Operador
requires_response: true
response_owner: Operador
status: open
one_line_summary: Confirmo lanzar el proyecto-front como primario/T0 (repo separado D:\Agentes\Zeus\Zeus-protocol, MVP single-operator, PII-free, supersede DB=T0). DECISION-0049 registrada. Una aclaracion estructural (donde viven SPEC/diseno de producto) antes de autorar el SPEC + git-init.
requested_action: "Confirmar (1) ubicacion: SPEC del front + handoffs/tasks que GOBIERNAN su desarrollo los autoro en el PROTOCOLO (Area_comun, atestado #4 = dataset) y el CODIGO + diseno interno de producto va en Zeus-protocol; vs querer tambien la DECISION/SPEC de PRODUCTO dentro de Zeus-protocol. (2) Que haga git-init de D:\\Agentes\\Zeus\\Zeus-protocol al abrir el SPEC. (3) Si T0 = el primer GO/handoff a Codex para construir el MVP (lo atesto en caliente)."
question: "Confirmas la estructura (gobernanza+SPEC+handoffs en el protocolo = dataset #4; codigo en Zeus-protocol) y que git-init Zeus-protocol + emita el primer handoff (T0) a Codex para el MVP? O prefieres la DECISION/SPEC de producto dentro de Zeus-protocol?"
context_refs:
  - Area_comun/decisions/DECISION-0049-proyecto-front-primario-t0-zeus.md
  - MSG-20260619-Operador-to-Arquitecto-GO-lanzar-proyecto-front-T0
deadline_or_blocking_level: normal
---

# Confirmado: proyecto-front primario/T0; aclaracion estructural antes del SPEC

Confirmo el lanzamiento tal como lo fijaste: **proyecto-front = proyecto PRIMARIO de tesis y T0**, repo
producto SEPARADO **`D:\Agentes\Zeus\Zeus-protocol`** (capa de aplicaciones Zeus, acoplamiento
unidireccional; el core neutral no se contamina), **single-operator** (multi-tenant fuera de alcance, su
propia DECISION), **PII-free** (dataset publicable sin DEF-PII). **Supersede "DB de Budget = T0"** (Budget =
proyecto posterior). #4 intacto (epoca 1.14.0). **DECISION-0049 registrada** (atestada bajo #4).

## Estructura que propongo (mi interpretacion; confirma o corrige)
- **PROTOCOLO (`Area_comun/`, atestado #4 = el DATASET de tesis):** SPEC de alcance del MVP, tasks,
  handoffs/GOs, ledger. T0 y el dataset se forman aqui (es la coordinacion gobernada, lo publicable).
- **`Zeus-protocol/` (producto, repo aparte):** el CODIGO del front + su diseno interno de producto.
  Desarrollado por SDD via la metodologia. Lo git-init al abrir el SPEC.
- **T0** = el **primer handoff gobernado** (mi GO a Codex para construir el MVP), atestado en caliente.

## Plan (de a una pieza, SDD, maker=Codex/checker=Arquitecto)
1. (con tu confirmacion) git-init `D:\Agentes\Zeus\Zeus-protocol` + SPEC del MVP single-operator (ver+accionar
   gobernado, sin bypass) en el protocolo.
2. Primer GO a Codex = **T0** (atestado). Codex construye el MVP en Zeus-protocol; yo reproduzco (checker).
3. Coordino con el floor en curso (CI/skills) **una cosa a la vez**; el front usa Git/CI conforme aterricen.

## Pregunta unica (para no re-trabajar)
Confirma la estructura de arriba (gobernanza+SPEC en el protocolo; codigo en Zeus-protocol) **o** indica si
quieres tambien la DECISION/SPEC de PRODUCTO dentro de `Zeus-protocol/`. Con tu confirmacion git-init y
emito el primer handoff (T0). Canal ASCII.
