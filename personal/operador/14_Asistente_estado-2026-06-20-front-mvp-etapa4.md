# ESTADO (memoria del asistente) - 2026-06-20 - Front MVP etapa 4 (atestacion) cerrada

> Memoria del ASISTENTE del operador (Jball). NO soy Arquitecto: asesoro, preparo prompts, escribo mailbox
> como Operador cuando me lo indica. No muto estado/ledger, no toco memoria de agentes. Verifico SIEMPRE en
> CANONICO (objetos git), nunca en el working tree del mount (se re-trunca). Supersede al 12_.

## Estado vigente (verificado en canonico)
- **Protocolo:** HEAD `81e99c2`, epoca **1.14.0**, **#4 ON** (4 flags true), validate con/sin secretos exit 0,
  drift 0. Dataset: **93 eventos firmados** (seq 672-764).
- **T0 ocurrio** (DECISION-0049): proyecto-FRONT = primario de tesis. Gobernanza (DECISION/SPEC/handoffs) en
  `Area_comun` (atestada #4 = **dataset publicable, PII-free**); **codigo** en `D:\Agentes\Zeus\Zeus-protocol`.
  Budget = proyecto posterior (gateado por PII/DB). Supersede "DB de Budget = T0".
- **Front MVP (Zeus-protocol):**
  - Floor: connector **Git** done (TASK-0123) + connector **CI** done (TASK-0125). Skills (Fase 1) pendiente.
  - **Etapa 1 andamiaje** done (TASK-0124) · **Etapa 2 observar** done (TASK-0126, RF-1..4 read-only) ·
    **Etapa 3 operar gobernado** done (TASK-0127, RF-5..8 via submit_intent + prueba no-bypass) ·
    **Etapa 4 vista de atestacion** done (TASK-0128).
  - Zeus-protocol HEAD `4d9f1b3`, **node --test 11/11** (extract limpio). **SIN REMOTE** (local en D:; TODO
    crear remote GitHub).
- **Badge honesto (AC duro del operador) IMPLEMENTADO de verdad:** el chip CANONICO/atestado deriva de los
  validadores reales (`validate_chain`/`agent_signatures`/`verify_anchor`/`verify_event_auth`/`drift`),
  estricto `=== true`, `state = git sucio ? working_tree : canonical`, fail-safe a no-verde, cero hardcode.
  Ahora muestra "working_tree" porque D: esta sucio = el front cazando la re-truncacion del mount en vivo.

## Decisiones clave de este tramo
- DECISION-0046 (estado secret-independent: clon limpio sin secretos valida exit 0).
- DECISION-0047 (versionado por EPOCA bajo #4: protocol_version solo cambia en re-genesis-boundary; capacidades
  nuevas FUERA del config pinned; release/capacidad en CHANGELOG/manifest).
- DECISION-0048 (connectors de accion sobre tool_policy, deny-by-default).
- DECISION-0049 (proyecto-front primario + T0; capa Zeus; repo separado; single-operator; PII-free).
- DECISION-0045 (boundary T0 + sello pre-T0 con provenance criptografica; "ningun piloto #4 contra el log vivo").

## Convencion de repos (enviada al Arquitecto para runbook/AGENTS)
Gobernanza/atestacion SIEMPRE en el protocolo (= dataset). Codigo de producto SIEMPRE en su repo bajo
`D:\Agentes\Zeus\`. El runtime de cada agente accede a ambos POR RUTA (ya configurado). **El FRONT es el
PANEL del operador -> VS Code OPCIONAL** (multi-root era andamio). Patron repetible: cada proyecto su repo
bajo Zeus; gobernanza de todos en el unico protocolo (hub permanente).

## Pendiente (gateado a GO del operador)
- **Crear remote GitHub de Zeus-protocol** (hoy local-only).
- **Agente Disenador: APROBADO** por el operador -> onboard via **re-genesis-boundary gobernado** + provisioning
  de clave (etapa 5 roster RF-9). Es ceremonia #4 (ventana de riesgo, operador presente).
- **Completar el front** (objetivo del operador: front COMPLETAMENTE FUNCIONAL, su herramienta de trabajo en
  adelante): etapa 5 roster (RF-9) + etapa 6 multi-proyecto + RF-10 kickoff; skills Fase 1.

## Lecciones (reforzadas)
- Verificar en CANONICO (git show / extract a /tmp), no el working tree del mount (re-truncacion recurrente,
  RUNBOOK windows-sandbox-temp-acl). El badge honesto del front implementa literalmente esta leccion.
- Gatear por el **exit REAL del validador** (no el de `tail`/PIPESTATUS) - error visto en mis scripts y en el
  del Arquitecto; el validador lo destapa.
- N-agente: alta/baja de agente = cambio de firmantes = re-genesis-boundary gobernado + provisioning (RF-9).

## Reglas de operacion del asistente
ASISTENTE no Arquitecto; no submit_intent/flags/state. Mailbox como Operador solo cuando me lo indican.
Tras cada "reporte de Arquitecto", VERIFICAR en canonico antes de aconsejar. Gates del operador: provisioning
real/anchor/re-genesis/flip de #4; uso vivo de connectors (s9); GATE-DATASET; DEF-PII (TASK-0118 diferida).
PII de terceros nunca al event log. Una ventana de riesgo a la vez. Canal ASCII.
