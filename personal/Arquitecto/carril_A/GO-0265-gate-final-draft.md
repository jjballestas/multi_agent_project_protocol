---
DRAFT (personal) del ruteo de TASK-0265 (gate final adversarial del conjunto) a la Analista.
Se convierte en MSG-<fecha>-Arquitecto-to-Analista-ACTION-GO-TASK-0265 cuando 0286 este DONE.
---

requested_action (contenido para el MSG):

"GO TASK-0265 -- GATE FINAL adversarial del CONJUNTO DECISION-0103. Eres owner+maker de esta
unidad (checker-only, DECISION-0099/0101). Ejecuta la revision adversarial del CONJUNTO COMPLETO
en CLON LIMPIO de HEAD (no en el working tree caliente), verificando cada acceptance contra el
codigo real e intentando ROMPER activamente los mecanismos. ALCANCE EXTENDIDO: el conjunto incluye
las unidades numeradas 0257 (harness/hook), 0258 (obstacles en turn_schema), 0259 (turn_validate
friccion auto-declarable), 0260 (vista de plan + gate turno 0), 0261 (validate_mailbox + friccion),
0262 (plantillas REPORTE/asignacion), 0263 (oferta de mejora), 0264 (regla de arranque escrita), MAS
las nacidas en vuelo por enmienda: 0266 (propagacion harness E4/E5 + H1 verify) y 0286 (gate-red
OBJETIVO post-gate, la hermana de 0259 por E7). Emite VEREDICTO POR UNIDAD (GO/NO-GO con hallazgos
accionables file:line + repro) por mailbox. PRUEBAS ADVERSARIALES MINIMAS (evidencia en el reporte):
(a) commit con estado gobernado ROJO que el hook DEBE rechazar -- OJO: por el hallazgo de 0266, el
hard-gate de estado gobernado es full-mode (HOOK_FULL=1 / hook.full true / CI), el partial local
por defecto solo avisa; prueba el rechazo en el modo enforcing y rompe un archivo que el
trailer-checker NO lea (p.ej. CLAIMS.json); (b) turno runtime con friccion (transicion autoritativa
blocked/qa_failed) y obstacles vacio -> rechazado por turn_validate; (c) mensaje REPORTE con
friction_count>0 y obstacles vacio -> rechazado por validate_mailbox; (d) historico de mailbox sigue
VERDE (grandfathering intacto); (e) propuesta RECHAZADA en el registro de ofertas NO se re-oferta; y
anade (f) gate_green:false + obstacles vacio POST-gate -> rechazado por RunLog.append (0286). Verifica
tambien COHERENCIA CROSS-UNIT: 0259+0286 = C3 runtime completo repartido en sus dos capas correctas
(pre-gate auto-declarable / post-gate objetivo); 0261 valida <-> 0262 plantilla usan el MISMO bloque
obstacles; 0260 gate mecanico <-> 0264 regla escrita coherentes. Residuales honestos declarados (lo
que no pudiste probar y por que). El veredicto NO ratifica por si mismo: la ratificacion y los flips
siguen el flujo normal (Arquitecto ratifica, Codex done-flip). Si alguna unidad sale NO-GO, su
hallazgo vuelve a Codex como remediacion antes de cerrar el batch. Entrega el veredicto + release."

question: "Todas las unidades del conjunto (0257..0264 + 0266 + 0286) pasan tu gate adversarial en
clon limpio de HEAD, con las 6 pruebas adversariales evidenciadas y la coherencia cross-unit (C3
repartido, bloque obstacles compartido, gate<->regla) confirmada?"
