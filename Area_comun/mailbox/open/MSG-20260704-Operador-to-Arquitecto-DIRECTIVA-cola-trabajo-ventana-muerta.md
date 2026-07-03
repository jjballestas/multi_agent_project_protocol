---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cola-trabajo-ventana-muerta
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-04
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (sella <=08-jul)
  - Area_comun/specs/nova/ (SPECs post DD-hornear 01f05db + THROW reatribuido)
  - personal/Arquitecto/APRENDIZAJES-EXTERNOS-extraccion-reglas.md (R-07, R-08)
one_line_summary: "Cola priorizada de trabajo desbloqueado para la ventana muerta (no camino critico del operador): (1) preparar/ensayar la atestacion del sello 08-jul; (2) re-gate consolidado del estado actual de las SPECs (atesta DD-02 criterio falsable); (3) redactar los 2 DECISION candidatos de F1.6 (R-08 licencia dia-1, R-07 posicionamiento)."
requested_action: "[DIRECTIVA] El Operador quiere el hilo activo en ventana muerta. Cola priorizada (todo desbloqueado, no compite con el reloj del operador GOAL-P1/estimates): (1) PRIMARIO -- PREP/ENSAYO DE LA ATESTACION DEL SELLO (de-riesga el reloj real 08-jul, es tu dominio: tu atestas): ensaya el mecanismo del sello sobre los artefactos ya disponibles -- computa el manifiesto de corpus (s.1 del SELLO: lista + sha256 de los artefactos que YA existen: schema_medicion/defectos + medicion_ledger.py emplazados, el SELLO draft, los NOVA_ESTUDIO_* si estan a la mano), y ensaya (dry-run) el flujo submit_intent de atestacion del sha256, para que el dia del sello sea UN intent atomico limpio. Deja constancia de que falta (la fila GOAL-P1 del ledger existira cuando corra el piloto 3-8 jul; el congelamiento del schema a v1.0 es el dia del sello). NO sellas nada aun; solo pre-armas. (2) SECUNDARIO -- RE-GATE CONSOLIDADO DE LAS SPECs: las 9 SPECs cambiaron desde el ultimo OK (DD-01/02/03 horneadas 01f05db + THROW reatribuido); DD-02 (objeto min 20) es un CRITERIO DE ACEPTACION FALSABLE que aun no viajo por un gate. Rutea al Analista un re-gate que deje el ESTADO ACTUAL de las SPECs plenamente atestado (foco: que DD-02 y las demas horneadas queden verificadas; el THROW/db_verified_at ya esta OK 070b533). Deja un baseline de SPECs atestado antes de Sprint 1. (3) VENTANA MUERTA -- redacta los 2 DECISION candidatos que F1.6 identifico: R-08 (frontera de licencia dia-1 -- GATEA la publicacion de Aegis por DECISION-0087; decidir temprano, nunca retrofit) y R-07 (posicionamiento atestacion != observabilidad). Ambos son Carril B (post-sello) pero R-08 es de entrada (decidir antes de publicar cualquier artefacto). Trabaja la cola en orden; sin prisa, es ventana muerta."
question: ""
---

# DIRECTIVA - Cola de trabajo para la ventana muerta

El Operador quiere el hilo activo mientras corre la ventana muerta (pares gobernados bloqueados hasta
17-jul; el reloj del operador es GOAL-P1 + estimates). Cola priorizada, todo desbloqueado:

1. **PRIMARIO - Prep/ensayo de la atestacion del sello (de-riesga el 08-jul, tu dominio):** computa el
   manifiesto de corpus (s.1) sobre los artefactos ya existentes + ensaya (dry-run) el `submit_intent` de
   atestacion, para que el dia del sello sea un intent atomico limpio. Anota lo que falta (fila GOAL-P1 tras
   el piloto; freeze schema v1.0 el dia del sello). NO sellas; pre-armas.
2. **SECUNDARIO - Re-gate consolidado de las SPECs:** cambiaron desde el ultimo OK (DD horneadas 01f05db +
   THROW reatribuido). DD-02 (objeto min 20) es criterio falsable sin gatear. Rutea al Analista un re-gate que
   deje el estado actual atestado antes de Sprint 1.
3. **VENTANA MUERTA - Redacta 2 DECISION de F1.6:** R-08 (licencia dia-1, gatea la publicacion de Aegis) +
   R-07 (posicionamiento atestacion != observabilidad). Carril B; R-08 es de entrada.

Detalle vinculante en requested_action. Sin prisa; es ventana muerta.
