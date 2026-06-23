---
task_id: TASK-0164
title: "Nucleo: claims de grano fino (CLAIMS.json por-fila #<claim-id>) + serializacion fisica del event-log (lock) -- desbloquea operador-vs-agente sin bifurcar el chain #4 (DECISION-0059)"
type: protocol
status: in_progress
owner: Codex
phase: P2
priority: high
linked_decisions: [DECISION-0059, DECISION-0020, DECISION-0022]
created_at: 2026-06-23
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
file: Area_comun/tasks/TASK-0164-codex-claim-grano-fino-lock-fisico.md
---

# TASK-0164 - Claims de grano fino + lock fisico del event-log (DECISION-0059)

> CAMBIO DE NUCLEO bajo #4, ratificado por el operador (DECISION-0059, lock fisico). maker=Codex /
> checker=Arquitecto + PASADA ADVERSARIAL DEL ANALISTA (concurrencia/#4). #4 byte-identica (NO tocar
> protocol.config.json / genesis / agent_registry / keys). Neutralidad de dominio total. ASCII-only.

## Diseno (DECISION-0059)
1. **Claims por-fila (logico).** Agrega `Area_comun/state/CLAIMS.json` a `ROW_SCOPED_LEDGER_PATHS`
   (runtime/submit_intent.py ~63). El `required_scopes` del kind claim (~565) pasa de `["CLAIMS.json"]` a
   `["CLAIMS.json#<claim-id>"]`. Un `claim acquire` reserva su propia fila `CLAIMS.json#<claim-id>`; dos claims con
   claim-id distinto NO solapan (la logica de selector de `scope_covers` ~123-127 ya lo soporta). El chequeo de
   solape (`validate_scope_authority` ~605-611) deja de bloquear claims sobre filas distintas.
2. **Claims sin paths fisicos del runtime.** Los claim-scopes que GENEREN el front y los agentes ya NO deben listar
   `runtime/state/events.jsonl` ni `runtime/state/snapshot.json` (no son recursos logicos; son materializacion).
   Ajusta los generadores de claims del front (Zeus src/server.js, donde arma el CLAIM-FRONT-... scope) y documenta
   que los agentes scopeen solo recursos logicos por-fila + ficheros concretos. (El runbook del Arquitecto se ajusta
   aparte.)
3. **Serializacion FISICA del append (clave #4).** `submit_intent` (y la ruta de escritura del event-log) toma un
   LOCK de archivo (OS; p.ej. `runtime/state/.ledger.lock` via msvcrt/portalocker/filelock cross-platform)
   alrededor de la seccion critica: leer-head -> validar contra el estado actual -> append -> materializar.
   DESPUES de adquirir el lock, RE-LEE el head/estado actual (por si otro escritor avanzo) y revalida. Asi dos
   escritores concurrentes se serializan por milisegundos sin bifurcar la cadena (un solo append a la vez,
   `prev_hash` consistente). El lock se libera siempre (finally).

## DoD / acceptance
- **AC-A (grano fino):** un `claim acquire` con scope `CLAIMS.json#<id-A>` NO solapa un claim activo con scope
  `CLAIMS.json#<id-B>` (id distinto) -> ambos coexisten; SI solapa otro con el mismo `#<id-A>`. Behavior-test
  determinista. `required_scopes` del claim usa la fila.
- **AC-B (compat):** un scope de-archivo-entero `CLAIMS.json` (sin selector) sigue cubriendo cualquier fila (claims
  viejos no rompen). Behavior-test.
- **AC-C (lock fisico / concurrencia #4) [CRITICO]:** prueba de DOS escritores CONCURRENTES (dos submit_intent en
  paralelo sobre recursos logicos DISTINTOS) -> ambos aterrizan, la cadena #4 queda VALIDA (validate_chain +
  agent_signatures + anchor verdes), `protocol_state_drift`=0, sin fork (un solo head lineal, `prev_hash`
  encadenado). Test determinista (puede forzar la concurrencia con dos procesos/hilos + el lock).
- **AC-D (#4 byte-identica + neutralidad):** `protocol.config.json` / genesis / agent_registry / keys SIN tocar;
  `scan_domain_neutrality` 0; cero terminos de dominio.
- Gates: `validate_collaboration_state.py` con y SIN secretos exit 0 en CLON LIMPIO; `scan_encoding` 0; sin
  regresion de los goldens existentes de submit_intent/claims/attestation; drift 0.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. PASADA ADVERSARIAL DEL ANALISTA con
  foco en la concurrencia/#4 (intentar provocar un fork de cadena y demostrar que el lock lo impide).

## Notas
- El front (Zeus) y los agentes deben EMPEZAR a scopear claims por-fila para aprovechar el grano fino; pero por
  compat, un scope viejo no rompe. Prioriza que el CLAIM-FRONT-... del front (aprobar candidata / requirement-intake)
  use `CLAIMS.json#<claim-id>` + las filas de TASK_INDEX/PROJECT_STATE que ya usa, SIN events.jsonl/snapshot.json.
- NO cambies la semantica de quien-puede-que (capabilities); solo el GRANO del scope y la serializacion fisica.
- El mensaje "Canal ocupado" (AC72) se mantiene para la ventana fisica/contencion logica real residual.
