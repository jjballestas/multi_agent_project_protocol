# SANDBOX-MUTADORES - mecanismo sellado (precondicion P4.x)

> Sella el mecanismo de sandbox de mutadores construido por el Operador (2026-07-04), que cierra la
> PRECONDICION BLOQUEANTE <=14-jul declarada en SPEC-NOVA-P4-001/002/003/004 (DECISION-0078, precedente
> DECISION-0041). Documento de mecanismo (namespaced instancia Nova), SIN secreto: solo nombres de env var,
> nunca valores.

## 1. Que resuelve

Los conectores readonly (`nova_sql_connector_readonly_s9`) no tienen `EXECUTE` (Msg 229). Los procs mutadores
de la familia P4.x (`Apply_Budget_Modification`, `Apply_Availability_Adjustment`, `Apply_Commitment_Adjustment`,
`Apply_Obligation_Adjustment`) ESCRIBEN: sus criterios de aceptacion (crear acto/ajuste + numeracion, cada THROW
alcanzable, delta de la vista de saldo) no se ejercen contra un conector readonly. Sin un sandbox con `EXECUTE`
real, los tests de mutacion quedan un-runnable y el patron a congelar (P4-001 pattern-setter, heredado por PAR-1)
no se valida contra comportamiento real -- solo contra `OBJECT_DEFINITION` (lectura estatica), que el estudio
prohibe como degradacion silenciosa.

## 2. Mecanismo (Opcion A: BD sandbox restaurada + rol de verificacion con EXECUTE)

- **BD sandbox:** `DbsFinanciero_SANDBOX`, restaurada desde un seed backup (`DbsFinanciero_SANDBOX_<fecha>.bak`)
  en el contenedor `ingenas-sqlserver`. Es una copia aislada de `DbsFinanciero` (produccion), no la BD real.
- **Login/rol solo-sandbox:** `nova_budget_verifier` / rol `budget_sandbox_verifier`, con `EXECUTE` sobre los
  15 procs `Budget.*` de la familia de mutadores/ajustes + `SELECT` sobre las 89 vistas de validacion/saldo que
  las SPECs citan. El rol NO tiene ningun permiso sobre `DbsFinanciero` (produccion).
- **Env vars (nombres unicamente; el valor NUNCA va al repo):** `SQLSERVER_SANDBOX_DATABASE`,
  `SQLSERVER_SANDBOX_VERIFIER_USER`, `SQLSERVER_SANDBOX_VERIFIER_PASSWORD` (definidas en
  `D:/Agentes/Ingenas/.env`, fuera del hub).
- **Aislamiento VERIFICADO por el Operador (2026-07-04):** conexion real con `nova_budget_verifier` OK; intento
  de abrir `DbsFinanciero` (produccion) con ese login FALLA como se espera; `EXECUTE` sobre
  `Apply_Obligation_Adjustment` OK; `SELECT` sobre `vw_Commitment_Line_Balance` OK; ambas BD (sandbox y
  produccion) ONLINE; los 4 procs `Apply_*` de la familia P4.x existen en el sandbox.

## 3. Requisitos del mecanismo (obligatorios para TODO miembro P4.x)

1. **IDENTICO EN AMBOS BRAZOS.** El brazo baseline y el brazo gobernado del estudio usan EXACTAMENTE este
   sandbox: misma BD (`DbsFinanciero_SANDBOX`), mismo seed, mismo rol de verificacion. Ningun brazo usa un
   sandbox distinto ni un nivel de acceso distinto -- eso romperia la comparabilidad A/B del estudio.
2. **PROCEDIMIENTO DE RESET (critico para mismo estado inicial).** Antes de correr los tests de mutacion de
   CADA miembro, y SIEMPRE entre brazos (baseline -> gobernado o viceversa), re-restaurar
   `DbsFinanciero_SANDBOX` desde el seed backup `DbsFinanciero_SANDBOX_20260704_050932.bak`. Sin este reset, el
   segundo miembro/brazo corre contra una BD ya mutada por el anterior -> confound de estado (saldos, actos
   numerados, deltas de vista ya no comparables). "Identico en ambos brazos" incluye el ESTADO INICIAL, no solo
   la conexion/credenciales.
3. **NO degradado a `OBJECT_DEFINITION`.** Este sandbox habilita `EXECUTE` real: los tests de mutacion de cada
   miembro P4.x corren la llamada real al proc (paridad EXEC-vs-endpoint viable), no una inspeccion estatica de
   la definicion. Si en algun punto el sandbox deja de estar disponible, la unidad se DIFIERE (no se sustituye
   en silencio por lectura de `OBJECT_DEFINITION`; ver DECISION-0078).
4. **Sin secreto en el repo.** Cualquier referencia a este mecanismo en SPECs/handoffs/tests cita los NOMBRES
   de env var de la seccion 2, nunca el valor (usuario/password/connection string van solo en
   `D:/Agentes/Ingenas/.env`, fuera del hub).

## 4. Efecto sobre las SPECs P4.x

Con este mecanismo sellado, la PRECONDICION BLOQUEANTE `sandbox mutadores <=14-jul` declarada en
`SPEC-NOVA-P4-001-apply-budget-modification.md`, `SPEC-NOVA-P4-002-apply-availability-adjustment.md`,
`SPEC-NOVA-P4-003-apply-commitment-adjustment.md` y `SPEC-NOVA-P4-004-apply-obligation-adjustment.md` queda
**READY** (adelantada respecto al plazo <=14-jul). El dev MEDIDO de estas unidades sigue sin abrir pre-sello
(Etapa 1 <=08-jul); este mecanismo solo remueve el bloqueo tecnico para cuando abra.

## 5. Referencias

- DECISION-0078 (mecanismo sandbox mutadores requerido, precedente DECISION-0041).
- `Area_comun/mailbox/archived/` -- ACTION del Operador que construyo el sandbox (2026-07-04), archivada tras
  este sellado.
- Particion del estudio s.1 (definicion de la precondicion "sandbox mutadores": definida y documentada
  <=14-jul, identica en ambos brazos, jamas degradada en silencio a leer `OBJECT_DEFINITION`).
