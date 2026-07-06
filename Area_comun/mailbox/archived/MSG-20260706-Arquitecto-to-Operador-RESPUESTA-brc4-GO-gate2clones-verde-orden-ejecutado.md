---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-brc4-GO-gate2clones-verde-orden-ejecutado
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
one_line_summary: "TRES cierres: (1) BR-C4 verificacion independiente GO -> enmienda s.27 registrada -> Q4 n=10 CONFIRMADO + Assert_Permission horneado en P3-002/003/004; (2) gate 2-clones VERDE (TASK-9302 done, prueba negativa de llave OK) -> Contabilidad tiene gate de apertura cumplido; (3) orden 1002->1001 ejecutado (TASK-1201 F0 in_progress mia, TASK-1101 en cola)."
requested_action: "Ninguna obligatoria. Sugerencia al DBA para su proximo smoke: 1 identidad cross-documento (aprueba CDP, sin permiso OBL) -- hallazgo menor de cobertura, no defecto (detalle en s.27)."
---

# RESPUESTA - BR-C4 GO + gate 2-clones VERDE + orden ejecutado (06:58 local, 2026-07-06)

## 1. BR-C4: verificacion independiente = GO -> n=10 CONFIRMADO (enmienda s.27)

Verifique contra lo DESPLEGADO en sandbox (como nova_budget_verifier via EXECUTE AS, con tu
autorizacion explicita para el docker exec):
- 6/6 procs reales con guarda Assert_Permission visible por OBJECT_DEFINITION.
- Set THROW real == documentado: 50320-50324 (cruce lista-vs-lista); fail-closed sin
  SESSION_CONTEXT (50320) YA implementado por el DBA (mi endurecimiento 3 del encargo).
- 9 permisos + 9 roles por documento x operacion + mapeo rol->permiso 1:1 POR CELDA.
- Smoke vivo: approve-only bloqueado en annul (50324), positivo real en approve, no-access
  bloqueado 3/3.
- **Hallazgo MENOR (cobertura, no defecto):** las identidades de prueba son por-operacion
  (user 29 = Approver de LOS TRES documentos), asi que la separacion entre documentos quedo
  demostrada solo estructuralmente. Sugerencia: 1 identidad cross-doc en el proximo smoke.
- Enmienda fechada **s.27** registrada: P3.2/P3.3/P3.4 elegibles -> **pool Q4 n=10**, la caida
  a n=7 NO se ejecuta. SPECs **P3-002/003/004 enmendadas**: el proc real de captura DEBE
  heredar Assert_Permission (nunca reimplementarla), mapeo ProblemDetails por superficie
  (anti-hallazgo-#10) y F-NOVA-01 re-verifica el proc real (el shim no cuenta).

## 2. Gate e2e DOS CLONES: VERDE (TASK-9302 = done) -> Contabilidad puede abrir

- Ciclo repartido via GitHub real: A (upsert Arquitecto + build-flips Codex) -> B (clon
  fresco, SOLO llave Analista, ratifica) -> A (done-flip Codex). validate 0 en ambos; firmas
  de los 11 eventos validas desde B.
- **Prueba negativa:** firmar como Codex en B FALLO por llave ausente, sin escribir estado --
  la separacion maker/checker es por POSESION de llave, no disciplina.
- **2 lecciones horneadas al runbook (misma entrega):** los secretos HMAC son DE LA INSTANCIA
  y se DISTRIBUYEN a los clones (frescos-por-clon rompen la paridad de replay -- verificado);
  y los slim views SIEMPRE se commitean con el ledger o el clon par ve drift.
- Cross-atestacion: **Entrada 2** anclada en el hub (head seq 3495, commit Aegis 8941efb1).

## 3. Orden 1002 -> 1001: ejecutado (sin dependencia dura que lo impida)

- **TASK-1201** ([DECISION-1002][F0] discovery memoria) = in_progress, owner Arquitecto --
  es mi siguiente bloque de trabajo.
- **TASK-1101** ([DECISION-1001][t1] SPEC interrogacion) = proposed en cola; se promueve al
  cerrar 1201 (promocion de a una).

## Higiene
8 mensajes consumidos archivados en este mismo checkpoint (lote + autorizaciones + ordenes ya
ejecutadas); open/ queda con los 2 ACTIONs del Analista (#10, #11-13) + esta respuesta.

-- Arquitecto
