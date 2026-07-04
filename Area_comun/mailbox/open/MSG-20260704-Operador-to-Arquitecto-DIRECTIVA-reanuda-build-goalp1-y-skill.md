---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-reanuda-build-goalp1-y-skill
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-FYI-pausa-total-debate (SUPERSEDIDA: el debate cerro, esto es orden)
  - Area_comun/decisions/DECISION-0088-asiento-coordinacion-build-escalonado-hub-instancia.md (asiento = HUB)
  - Area_comun/decisions/DECISION-0050-repos-arquitectura-acoplamiento.md (repo producto sin governance)
  - personal/asesor/DRAFT-skill-codegen-triage.md (diseno de referencia de la skill; requisitos abajo, no verbatim)
one_line_summary: "FIN DEL DEBATE, ORDEN DEL OPERADOR. Metodologia SE MANTIENE como esta (Arquitecto/Codex/Analista + Operador; sin separar roles en mas firmantes; los ~10 roles del GOAL colapsan sobre los 4 con rol activo explicito por artefacto; maker!=checker duro). Tres acciones: (A) ARRANCA el build de GOAL-P1 (activa Codex maker + confirma/crea repo Nova-Budget + apunta a NOVA-GOAL-001, asiento=HUB); (B) semantica checker GOAL-P1 = OPCION B (baseline fiel, checker_formal=0); (C) crea la skill codegen-triage para Codex (aprobada por el operador). A trabajar el GOAL hasta terminar el desarrollo. La clarificacion codegen!=peon queda como INPUT del sello (08-jul), NO se sella ahora."
requested_action: "[DIRECTIVA] El debate cerro; esto es orden del Operador (2026-07-04). METODOLOGIA SE MANTIENE como esta: firmantes = Operador (dominio) / Arquitecto (arq+docs) / Codex (maker) / Analista (security+QA checker). NO se separan roles en mas firmantes: los ~10 roles del GOAL (Backend/Domain/Gateway/Frontend/MCP/DevOps/Docs/Architect/Security/QA) COLAPSAN sobre los 4, con el ROL ACTIVO EXPLICITO por artefacto (SPEC/commit/handoff declaran el sombrero); maker!=checker se mantiene DURO (Codex hace, Analista verifica; jamas auto-verificacion). ACCION A -- ARRANCA EL BUILD DE GOAL-P1: (1) activa Codex como maker (DECISION-0057, runtime-only); (2) confirma/crea el repo de producto Nova-Budget: remoto https://github.com/jjballestas/Nova-Budget.git (existe, VACIO; verificado con git ls-remote), clon local D:/Agentes/Zeus/NOVA/Nova-Budget, SOLO codigo sin governance (DECISION-0050); (3) apunta el build a NOVA-GOAL-001 = P1 fundacion tecnica (NOVA.sln con los 7 proyectos + apps/nova-web React/TS/Vite + health/OpenAPI/ProblemDetails/logging+correlation-id + architecture tests + CI minimo). Registra en el HUB la(s) tarea(s) baseline de GOAL-P1 con DoD, owner=Codex-maker / checker=Analista. Asiento de coordinacion = HUB durante la ventana del estudio (DECISION-0088). ACCION B -- SEMANTICA CHECKER GOAL-P1 = OPCION B (baseline fiel): la FILA MEDIDA de GOAL-P1 = Codex maker + gate en ventana = architecture tests + CI verde + adversarial informal de 12 puntos (corre en AMBOS brazos, NO es el tratamiento); SIN gate formal del Analista sobre el codigo -> checker_formal=0, fiel al schema sellado. El Analista valida DoD/evidencia sin contar como checker_formal. El escrutinio FORMAL de P1 ya esta sellado como la revision de frontera P1 (26-29 jul, Analista READ-ONLY, fuera del contraste, remediacion a FRONTERA-FIX). Analista-checker-FORMAL aplica a las tareas GOBERNADAS post-30-jul, no al piloto. ACCION C -- CREA LA SKILL codegen-triage para Codex (aprobada por el operador), tarea gobernada owner=Codex-maker / checker=Analista, en 2 capas: (a) NEUTRAL (sin dominio, exportable): decide codegen-vs-frontera -- fuente determinista + funcion mecanica-y-total ('por cada X emite N archivos rellenando huecos') -> CODEGEN; requisito duro = correctitud comprobable por GATE determinista (build/test/arch-test/paridad), no por criterio; BANDERAS ROJAS que mandan al firmante frontera = compone >1 mutacion / llama procs en secuencia / cruza frontera de modulo / toca SESSION_CONTEXT o saldos-cuadres / depende de vista con brecha / logica-seguridad-migracion; el peon queda FUERA del alcance (capa aparte, DECISION-0078); (b) INSTANCIA NOVA (recetas, fuera del core neutral por regla 1 CLAUDE.md): dotnet new template-pack, EF Core scaffold, Roslyn SG, NSwag + gate de instancia. La USA Codex desde GOAL-P1/P2. Diseno de referencia (no verbatim): personal/asesor/DRAFT-skill-codegen-triage.md. NOTA codegen!=peon: el codegen es determinista, cero-tokens, de un solo dev, NO anade agentes (respeta el mono-orquestador), NO es el tratamiento -> Codex PUEDE usar codegen en el build medido, con uso SIMETRICO por par. La CLARIFICACION formal en la definicion del brazo baseline queda como INPUT DEL SELLO (08-jul); NO la selles ahora (el operador la confirma al sellar). RESPONDE con: (a) ruta repo confirmada + Codex activo si/no; (b) id(s) de la(s) tarea(s) baseline de GOAL-P1 en el hub; (c) id de la tarea de la skill codegen-triage; (d) confirmacion de semantica checker B para GOAL-P1."
question: ""
---

# DIRECTIVA - Reanuda el build de GOAL-P1 + skill codegen (fin del debate)

El debate cerro. Orden del Operador: metodologia **se mantiene como esta** (Arquitecto/Codex/Analista +
Operador), sin separar roles en mas firmantes -- los ~10 roles del GOAL colapsan sobre los 4 con rol activo
explicito por artefacto; **maker != checker** duro. Tres acciones:

## A - Arranca el build de GOAL-P1
1. Activa Codex (maker). 2. Confirma/crea el repo Nova-Budget: remoto
https://github.com/jjballestas/Nova-Budget.git (existe, VACIO), clon local D:/Agentes/Zeus/NOVA/Nova-Budget,
solo codigo sin governance (DECISION-0050). 3. Apunta a NOVA-GOAL-001 = P1 fundacion tecnica (NOVA.sln 7
proyectos + nova-web React/TS/Vite + health/OpenAPI/ProblemDetails/correlation-id + architecture tests + CI).
Registra la(s) tarea(s) baseline en el HUB (DoD, owner Codex-maker / checker Analista). Asiento = HUB (DECISION-0088).

## B - Semantica checker GOAL-P1 = opcion B (baseline fiel)
Fila medida = Codex maker + gate architecture-tests + CI + adversarial informal (checker_formal=0, fiel al
schema sellado). El Analista valida DoD/evidencia sin contar como checker_formal. El escrutinio formal de P1
ya esta sellado = frontera P1 read-only 26-29 jul (fuera de contraste -> FRONTERA-FIX). Analista-checker-FORMAL
= solo tareas gobernadas post-30-jul.

## C - Crea la skill codegen-triage para Codex (aprobada)
Tarea gobernada, owner Codex-maker / checker Analista. Dos capas: NEUTRAL (codegen-vs-frontera: mecanico-total
+ gate determinista + banderas rojas de composicion/cruce-modulo/SESSION_CONTEXT/saldos/brecha/logica; peon
fuera de alcance) + INSTANCIA Nova (dotnet new / EF scaffold / Roslyn SG / NSwag + gate). La usa Codex desde
GOAL-P1/P2. Diseno ref (no verbatim): personal/asesor/DRAFT-skill-codegen-triage.md.
**codegen != peon:** determinista, cero-tokens, un dev, NO tratamiento -> Codex lo usa en el build medido,
simetrico por par. La clarificacion formal en la def del brazo baseline = INPUT DEL SELLO (08-jul), NO la selles ahora.

Responde con: ruta repo + Codex activo, id(s) tarea baseline GOAL-P1, id tarea skill, confirmacion checker B.
