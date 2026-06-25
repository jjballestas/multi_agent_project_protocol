---
task_id: TASK-0180
title: "Proyecto-front (RF-14): carga por archivo v2 FASE B - store no-ledger de candidatas + panel de revision + gate humano de PII + consumidor minimo NO-LLM (archivo entero = 1 candidato editable) (AC42 rama-archivo, AC43, AC44; SPEC-0086 ext10; DECISION-0056; REQ-D642E4D8)"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0056, DECISION-0055, DECISION-0051]
origin_reqs: [REQ-D642E4D8]
follows: TASK-0150
created_at: 2026-06-25
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0180-codex-file-intake-v2-faseB.md
---

# TASK-0180 - Carga por archivo v2 FASE B (panel de revision + gate PII humano + consumidor minimo NO-LLM) (SPEC-0086 ext10, AC42/AC43/AC44; DECISION-0056)

> maker=Codex / checker=Arquitecto DESDE CLON LIMPIO + PASADA DEL ANALISTA al cierre (PII gate + sin egress de
> modelo + store fuera del dataset). Codigo en Zeus. OFF-by-default. **Fase B NO enciende el agente extractor**
> (eso es Fase C): el productor de candidatas es un **consumidor determinista NO-LLM** (archivo entero = 1
> candidato editable), que cierra el flujo archivo de extremo a extremo sin ventana de modelo. Continua TASK-0150
> (Fase A: upload + screening + store + emit extraction-task + selector de modo).

## Alcance (Fase B)
1. **Consumidor minimo NO-LLM (activa la rama-archivo de AC42 sin Fase C):** la extraction-task emitida en Fase A
   se consume de forma **determinista, sin modelo**: el contenido del archivo (ya screened/inerte) se vuelve **1
   candidato editable** con `title`/`narrative`/`intent`/`project` prellenados best-effort desde el texto
   (heuristica simple, p.ej. narrativa = cuerpo; title/intent = vacios o derivados triviales editables). NO importa
   SDK de modelo, NO abre socket a host de LLM, NO `fetch`/red salvo el transporte gobernado existente. Test
   estatico falsable + control positivo: el consumidor no introduce egress de modelo.
2. **Store NO-LEDGER de candidatas (AC41 parte-store):** las candidatas viven en un store **gitignored, FUERA del
   dataset atestado**, con **ciclo de vida propio que NO es `task_status`** (el estado `candidate` NO existe en
   VALID_TASK_STATUSES y NO se agrega); el ledger atestado **NUNCA** ve candidatas; no tocan TASK_INDEX/
   PROJECT_STATE; **drift 0 con candidatas presentes**; un clon limpio sin el store valida exit 0. Entregar su
   linea `.gitignore` en el MISMO commit + excluir del git-status del indicador canonico.
3. **Panel de revision (front, AC43 superficie):** vista/pestana que lista las candidatas del archivo y permite
   **editar** cada una (title/narrative/intent/project) y **aprobar / descartar por candidata**. Read/edit local
   puro: **sin SDK/fetch de modelo en el browser**. Conforme al design-system (AC13). Carry AC12 routing / AC11
   badge.
4. **Gate HUMANO DURO de PII + aprobar->intake (AC43):** para **aprobar** una candidata el operador **DECLARA
   explicitamente que reviso PII** (atestacion humana por-candidata). Solo una candidata APROBADA pasa por el
   `requirement-intake` EXISTENTE (execute gobernado AC39) con **re-screening de PII** en la frontera
   candidate->intake (el texto EDITADO se valida por los MISMOS guards al aprobar). El **id/idempotency** del
   requirement deriva del **CONTENIDO EDITADO** (title+narrative+intent+project), NO del archivo (1 archivo -> N
   candidatas -> N requirements; re-aprobar la misma candidata es idempotente). Atribucion D-ACTOR: relay honesto
   author=Operador / relayed_by=Arquitecto (sin tocar registry, #4 byte-identica). Test: aprobar sin declarar PII
   -> bloqueado; editar para inyectar PII/contenido activo -> redactado/rechazado al aprobar.
5. **Estados, purga, procedencia, anti-abuso (AC44):** estados de extraccion explicitos (encolada / corriendo /
   completed-empty / completed-N con cap / failed con razon); **purga del raw** al estado terminal del candidato
   (aprobado/descartado) + TTL para huerfanos (test: el raw no sobrevive al estado terminal; clon limpio sin la
   carpeta valida exit 0); **procedencia PII-free determinista** en el requirement aprobado (sha256 archivo + id
   extraction-task + hash candidato pre-edicion); errores/logs NO ecoan contenido crudo.

## DoD
- AC42(rama-archivo activada por el consumidor minimo) + AC43 + AC44 verdes con tests de COMPORTAMIENTO
  permanentes; carry AC40/AC41(store)/AC39/AC13/AC11/AC12. node --test/CI verde **EN CLON LIMPIO** (gate eol=lf).
- **#4 epoca 1.14.0 BYTE-IDENTICA** (config/genesis/registry/keys sin cambio, version pinned 1.14.0); validate
  con/sin secretos exit 0; **drift 0 con candidatas presentes**; neutralidad/encoding limpio; unica mutacion de
  ledger = `task_upsert`/`requirement-intake` via submit_intent (sin segundo escritor, sin nueva ruta de
  escritura).
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. **PASADA DEL ANALISTA** antes de
  cerrar (gate PII humano efectivo; sin egress de modelo en el consumidor minimo ni en el panel; store fuera del
  dataset; purga del raw; procedencia PII-free). Commit como Arquitecto + Co-Authored-By: Codex.
- REPRO: subir un .md/.txt -> aparece 1 candidato editable en el panel -> editar -> aprobar sin declarar PII =
  bloqueado; declarar PII + aprobar -> aterriza 1 requirement real (id+seq) via el intake gobernado; descartar ->
  purga el raw; clon limpio sin el store valida exit 0; drift 0.

## Fuera de alcance (Fase C)
- El **agente extractor real** (archivo -> 1..N candidatas via modelo, AC41 productor-LLM) + la **frontera de
  egress del agente** + el endurecimiento **AC45/AC46** (guard de egress allowlist deny-all sobre TODO `src/**`),
  que es PREREQUISITO y bloquea el cierre de Fase C. Fase B no enciende ventana de modelo.
- NO encender vivo nada del extractor (OFF; activacion futura gateada + pasada del Analista + GO del operador).
