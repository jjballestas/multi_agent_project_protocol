---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cola-arquitecto-sin-idle
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-reanuda-build-goalp1-y-skill (item 1 de esta cola)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (reloj duro <=08-jul)
  - personal/Arquitecto/TFM-medicion/corpus/medicion/ (scripts + schema emplazados, congelar a v1.0 en el sello)
one_line_summary: "Directiva permanente del Operador: NO quedar idle. Cola priorizada del Arquitecto para trabajar EN ORDEN mientras Codex construye P1; avanzar el sello y las SPECs siguientes en paralelo. (1) [ruteado] arranque GOAL-P1 + registrar tarea baseline + skill codegen + activar Codex; (2) coordinar y GATEAR GOAL-P1 con Codex (arch-tests + CI + adversarial informal) y cerrar la fila-piloto de medicion (valida captura de tokens end-to-end); (3) prep/ensayo del sello 08-jul (manifiesto de corpus + sha256 + dry-run submit_intent de atestacion + validar schema v1.0 contra el piloto); (4) preparar las SPECs gobernadas de P2.1 (parametros) y P2.2 (reporte ejecucion, spec_prepagado) para que Codex arranque POST-sello. El dev medido de P2.x NO abre antes del sello (solo GOAL-P1 pre-sello)."
requested_action: "[DIRECTIVA] Regla permanente del Operador: el Arquitecto NO queda sin trabajo -- trabaja la cola EN ORDEN y, mientras Codex construye P1, avanza en PARALELO los items 3 y 4. Cola priorizada: (1) [YA RUTEADO en la DIRECTIVA-reanuda] arranca GOAL-P1: activa Codex maker + confirma/crea repo Nova-Budget + apunta a NOVA-GOAL-001 + registra la(s) tarea(s) baseline en el hub + registra la tarea de la skill codegen-triage. (2) COORDINA Y GATEA GOAL-P1 con Codex: cuando Codex entregue P1, corre el gate de ventana (architecture tests + CI verde + adversarial informal de 12 puntos), y CIERRA la fila-piloto de medicion de GOAL-P1 -- ese cierre valida la CAPTURA DE TOKENS end-to-end (el proposito real del piloto; protocolo de medicion s.4) antes de congelar el schema en el sello. (3) PREP/ENSAYO DEL SELLO 08-jul (de-riesga el reloj duro; es tu dominio, tu atestas): computa el manifiesto de corpus (lista + sha256 de los artefactos que YA existen: schema_medicion/defectos + medicion_ledger.py emplazados en personal/Arquitecto/TFM-medicion/corpus/medicion/, el SELLO draft, los NOVA_ESTUDIO_* a mano), ensaya (dry-run) el flujo submit_intent de atestacion del sha256, y valida el schema de medicion v1.0 contra lo que produjo el piloto GOAL-P1. Deja constancia de lo que falta (la fila GOAL-P1 real existira cuando corra el piloto; el congelamiento del schema a v1.0 es el dia del sello). NO selles nada; pre-arma. (4) PREPARA LAS SPECs GOBERNADAS de las proximas unidades baseline para que Codex arranque JUSTO tras el sello (calendario 08-14 jul): P2.1 read-model de parametros (M) y P2.2 reporte de ejecucion presupuestal (M, spec_prepagado -- SPEC-NOVA-P2-001 preexiste: verifica/porta al hub la derivacion gobernada). Citas verificables contra la BD via el conector readonly s9. IMPORTANTE: el DESARROLLO MEDIDO de P2.x NO abre antes del sello -- solo GOAL-P1 abre pre-sello (excepcion declarada); preparar las SPECs es trabajo de arq+docs, NO arranque de dev. Regla dura mientras dure la ventana: cero peones en brazos medidos; codegen determinista permitido (simetrico por par); metodologia as-is (maker Codex != checker Analista). Cualquier bloqueo -> senala por mailbox con una pregunta concreta, no quedes idle."
question: ""
---

# DIRECTIVA - Cola del Arquitecto (no quedar idle)

Regla permanente del Operador: **el Arquitecto no queda sin trabajo.** Trabaja la cola EN ORDEN;
mientras Codex construye P1, avanza los items 3 y 4 en paralelo.

1. **[ya ruteado]** Arranca GOAL-P1 (Codex + repo Nova-Budget + NOVA-GOAL-001) + registra tarea baseline
   + registra la tarea de la skill codegen-triage.
2. **Coordina y gatea GOAL-P1** con Codex (architecture tests + CI + adversarial informal); cierra la
   fila-piloto de medicion -- valida la captura de tokens end-to-end antes de congelar el schema.
3. **Prep/ensayo del sello 08-jul** (de-riesga el reloj; tu atestas): manifiesto de corpus (lista + sha256
   de artefactos existentes) + dry-run del submit_intent de atestacion + valida el schema v1.0 contra el
   piloto. NO selles; pre-arma.
4. **Prepara las SPECs gobernadas** de P2.1 (parametros) y P2.2 (reporte ejecucion, spec_prepagado) con
   citas contra BD readonly, para que Codex arranque POST-sello. El dev MEDIDO de P2.x NO abre pre-sello
   (solo GOAL-P1). Preparar SPECs = arq+docs, no arranque de dev.

Reglas de ventana: cero peones en brazos medidos; codegen determinista OK (simetrico por par); metodologia
as-is (Codex maker != Analista checker). Bloqueo -> mailbox con pregunta concreta, no idle.
