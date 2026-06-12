---
status: open
---

# MSG 2026-06-13 - Claude -> Operador - SPEC-0070 cerrada; TASK-0101 listo para GO a ready

- **De:** Claude (architect) 
- **Para:** Operador humano 
- **Asunto:** SPEC-0070 (prev_hash encadenado) completada; TASK-0101 propuesto → ready (requiere tu GO)
- **Tipo:** Solicitud de accion (promocion de tarea)

---

## Resumen

**SPEC-0070** (prev_hash encadenado en el eventlog, DECISION-0029 pieza 2a) fue completada el
2026-06-13 y committeada en HEAD 31e9a1d.

TASK-0101 ahora referencia `spec_id: SPEC-0070` y esta listo para promoverlo de `proposed` a
`ready+GO` bajo tu authorization.

---

## Contenido de la SPEC

La SPEC-0070 formaliza:

1. **Diseño tecnico:** Campo `prev_hash` en cada evento (flag `event_state.chain_enabled`);
   genesis = SHA256(canonical_json(protocol.config.json)); encadenado SHA256 evento por evento.

2. **Respuesta a Q1 (genesis):** Hash de `protocol.config.json` es raiz de confianza porque es
   versionado, auditado y reproduce el estado de activacion de la cadena.

3. **Respuesta a Q2 (prune/archive):** Se crea `chain_manifest.json` con el hash anterior del
   ultimo evento prunado; evento `chain.archive_boundary` asegura continuidad post-prune;
   validador hibrido reconoce boundary y valida cadena a traves del punto de corte.

4. **10 golden cases:**
   - GC-1: Cadena valida (happy path).
   - GC-2 a GC-5: Alteracion, insercion, borrado, reordenamiento (detectables).
   - GC-6 a GC-7: Legacy sin prev_hash; migracion de log legacy a cadena.
   - GC-8: Genesis mismatch (detectable).
   - GC-9 a GC-10: Post-prune (boundary valido; boundary faltante detectado).

5. **Acceptance Criteria claros:** Flag off-by-default; validador integrado en
   `protocol_replay.py`; neutral/encoding verdes; handoff con evidencia.

6. **Cambios concretos:**
   - `runtime/eventlog.py`: nuevas funciones (chain_enabled, compute_genesis_prev_hash, etc.);
     append_event() carga prev_hash si flag activo.
   - `runtime/protocol_replay.py`: validate_chain() integrado.
   - `protocol.config.json`: nuevo campo `chain_enabled: false` en `event_state`.
   - `examples/chain_cases/`: 10 casos golden con script de ejecucion.

---

## Accion requerida

Para que el trabajo avance:

1. **Revisa SPEC-0070** (`Area_comun/specs/SPEC-0070-prev-hash-encadenado.md`).
   - ¿Hay ambigüedad tecnica o decisión de diseño que deba resolver antes de codificar?
   - ¿Las Q1 y Q2 estan respondidas satisfactoriamente?

2. **Si apruebas la SPEC:**
   - Usa `submit_intent.py` para promover `TASK-0101` de `proposed` a `ready` y enviar el GO a
     Codex vía `claim acquire CLAIM-20260613-task0101-GO-codex`.
   - El operador decide orden de inicio (puede ser ya, o esperar a que termines de revisar las
     otras dos SPECs 0102/0103).

3. **Si encuentras cambios necesarios:**
   - Responde por este hilo especificando el gap.
   - Actualizare la SPEC y reenviare el GO.

---

## Proximos pasos (fuera de este turno)

- **SPEC-0071 (TASK-0102, firma por agente):** Depende de TASK-0101 (basicamente); puedo
  redactarla en paralelo o tras TASK-0101.
- **SPEC-0072 (TASK-0103, anclaje externo):** Idem; es independiente de 0102 pero depende de
  0101.

Recomendacion: Codex puede comenzar TASK-0101 ya; las otras dos SPECs las redacto mientras
Codex codifica.

---

**Handoff autocontenido:** Este mensaje + SPEC-0070 + DECISION-0029 contienen todo el contexto
para promover y ejecutar TASK-0101. No se asume memoria de sesiones previas.

