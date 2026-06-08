---
id: TASK-0088
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0080]
relates_to: [TASK-0078, TASK-0079, TASK-0086]
phase: P2
spec_id: Area_comun/specs/SPEC-0064-autonomia-supervisada.md
linked_decisions: [DECISION-0024, DECISION-0021, DECISION-0022]
objective: Implementar el lock-lift de SA.4 (SPEC-0064 sec.4) OFF-BY-DEFAULT - condicionar el cerrojo --once del invoker real subprocess para que el modo multi-turno se permita SOLO con supervised_autonomy registrado + real_invoker registrado + --allow-supervised-autonomy + --allow-real-invoker; gobernado por el sobre (caps/PAUSE/reloj/checkpoint). Registro vacio => cerrojo intacto, byte-equivalente. NO poblar el registro ni correr el piloto (eso es el micro-GO posterior del operador).
expected_output: orchestrator.py linea 340 condicionada - hoy "if adapter==llm and invoker==subprocess and not once: reject" es INCONDICIONAL; pasar a: rechazar SALVO que supervised_autonomy_activation_error(config) is None AND real_invoker_activation_error(config) is None AND allow_supervised_autonomy AND allow_real_invoker (en ese caso permitir multi-turno, acotado por caps.max_turns/PAUSE/wall_clock/checkpoint ya existentes). Golden DETERMINISTA (sin red/LLM real): (a) recorded multi-turno sigue OK; (b) subprocess multi-turno PERMITIDO en la ruta del gate solo con registro valido (usar invoker stub/fake determinista o aserir la decision del gate, NO llamar LLM real); (c) off/sin-registro => subprocess+not-once RECHAZADO (mensaje intacto) = byte-equivalente; (d) --once subprocess sigue intacto (DECISION-0021). Paridad .ps1 si aplica + CI.
question_to_resolve: ninguna (alcance fijado por SPEC-0064 sec.4 + GO operador). Si surge ambiguedad o el gate necesita refactor mayor => blocked + nota. Si submit_intent rechaza, NO editar *.json a mano.
closure_criterion: lock-lift condicionado implementado OFF-BY-DEFAULT (registro vacio = byte-equivalente, cerrojo --once intacto; verificable) + golden determinista de paridad (recorded sigue, real permitido solo con registro valido, off rechaza, --once intacto) + regresiones verdes (supervised_autonomy_cases, real_adapter) + validador/neutralidad/encoding verdes + paridad/CI; NO se poblo el registro ni se corrio el piloto; todo emitido por submit_intent (enforce+authoritative ON); handoff autocontenido con la evidencia del gate (allow/reject por config).
sdd_required: true
---

# TASK-0088 (SA.4) - Lock-lift del invoker real multi-turno, OFF-BY-DEFAULT

> READY (encolada por Claude 2026-06-08 VIA submit_intent bajo enforce+authoritative). GO del operador para
> PASOS 1+2 de SA.4 (lock-lift + ensayo de rollback); el piloto (pasos 3+4) es un MICRO-GO POSTERIOR. enforce+
> authoritative ON: TODO por submit_intent. Capa C OFF. SA.4 y Capa C nunca juntos (DECISION-0026).

## Contexto (hallazgo verificado)

El cerrojo `--once` del invoker real esta en `runtime/orchestrator.py` linea 340 y es **incondicional**:
```python
if adapter_name == "llm" and llm_invoker == "subprocess" and not once:
    return {"ok": False, "reason": "subprocess llm invoker requires --once"}
```
El bloque `allow_supervised_autonomy` (lineas 328-332) solo arma los caps, que hoy gobiernan el loop
**recorded**. Los golden `supervised_autonomy_cases` son recorded-only. => SA.4 (invoker real multi-turno bajo
el sobre) NO esta implementado. Esta tarea lo implementa OFF-BY-DEFAULT.

## Alcance (SPEC-0064 sec.4)

1. **Condicionar el cerrojo (linea 340):** rechazar `subprocess && not once` SALVO que TODO se cumpla:
   `allow_supervised_autonomy` AND `allow_real_invoker` AND `supervised_autonomy_activation_error(config) is None`
   AND `real_invoker_activation_error(config) is None`. En ese caso permitir multi-turno; el sobre ya existente
   (caps.max_turns linea 344, PAUSE antes de cada turno, wall_clock, checkpoint humano por K/fix-cycles) lo acota.
2. **OFF-BY-DEFAULT / byte-equivalente:** con `supervised_autonomy.enabled=false` (estado actual) o registro
   incompleto, la linea 340 rechaza EXACTAMENTE como hoy. `--once` subprocess sigue intacto (DECISION-0021).
3. **Golden DETERMINISTA (sin red ni LLM real):** (a) recorded multi-turno sigue OK; (b) la DECISION del gate
   permite subprocess multi-turno solo con registro valido (invoker stub/fake determinista, o aserir el gate;
   NO llamar un LLM real); (c) off/sin-registro => rechazo intacto (byte-equivalente); (d) --once subprocess intacto.
4. **Paridad** .ps1 si aplica + CI. Regresiones (supervised_autonomy_cases, real_adapter) verdes.

## Restricciones (duras)

- **NO poblar** `runtime.real_invoker`/`runtime.supervised_autonomy` (siguen enabled=false) ni correr el piloto:
  eso es el micro-GO posterior del operador (pasos 3+4). Esta tarea entrega el codigo APAGADO.
- enforce+authoritative ON: CERO edicion manual de `state/*.json`, todo por submit_intent/ledger_ops; si rechaza,
  blocked + error + transaccion.
- **Capa C OFF.** Vendor-neutral, ASCII, sin secretos. 1 commit/turno. Release/handoff DECISION-0018/0020.
- Template intacto (no cambiar defaults del master).

## Despues (NO en esta tarea)

Tras ratificar (Claude) + ensayo de rollback verde, el operador da micro-GO para: DECISION-0027 (activacion) +
poblar el registro con sus coordenadas + piloto (1 tarea de bajo riesgo = nota en
`examples/neutrality_scan_cases/README.md`) con caps max_turns=2 / human_checkpoint_every_k=1 /
wall_clock_ms=180000 / budget+deadline / PAUSE.

## Cierre

Claude ratifica adversarialmente (gate permite/rechaza por config; off byte-equivalente; golden + regresiones
verdes) y cierra por submit_intent. Luego Claude ensaya el rollback (registro-off cerrojo; poblar levanta;
despoblar restaura; replay==hot) y reporta al operador para el micro-GO de 3+4.
