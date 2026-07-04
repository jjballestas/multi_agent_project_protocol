# DRAFT-SPEC hardening -- Annul_Availability_Certificate + Annul_Commitment (brecha B-04 / RN-08)

> Autor: Asesor (Vision Nova). Carril: DISENO. Estado: DRAFT para que el Arquitecto lo formalice y lo
> asigne a un BUILDER NO-MEDIDO (DBA/equipo del Operador o sesion de agente fuera del estudio).
> Fecha: 2026-07-04. Deadline duro: **<=15-jul** (SELLO s.11.1; si no, PAR-2 CAE completo).
> Fuente: NOVA_PRES_08 (Reversos y Anulaciones, B-04 / RN-08) + PRES_04 (CDP) + PRES_05 (Compromiso).

## 0. Firewall de integridad (LO PRIMERO)
- Estos 2 procs son **nova-hardening, NO dev medido**. Regla 8: el dev de los brazos del estudio JAMAS
  crea el proc. Los construye tu DBA/equipo o una sesion de agente EXPLICITAMENTE fuera del estudio;
  nunca se registran como una fila baseline/gobernado del journal de medicion.
- La **superficie C# / API** sobre estos procs SI es una unidad medida (miembro baseline de PAR-2, y su
  mitad gobernada en Sprint 1). Por eso el proc debe **pre-existir** antes de esa superficie. Separacion
  limpia: proc = hardening (fuera del estudio); superficie = medida.
- Como es hardening, NO le aplica la linea roja del sello: se puede (y conviene) construir YA, adelantado.

## 1. Que falta y por que (B-04 / RN-08)
El patron de anulacion esta PROBADO en los 3 niveles inferiores (Annul_Obligation, reverso de Pago,
anulacion de Radicacion) y FALTA en los 2 superiores: CDP y Compromiso. **Precedente vivo a copiar:
`Annul_Obligation`** (ya existe; el builder extrae su definicion con OBJECT_DEFINITION y la replica un
nivel arriba). Legacy permitia "liberar saldo con documentos hijos vivos" (tesoreria sin piso); NOVA
impone **cascada BLOQUEANTE por validacion**.

## 2. El patron RN-08 (3 efectos coordinados + guarda bloqueante)
Cada anulacion, en UNA transaccion (`SET XACT_ABORT ON`, `UPDLOCK/HOLDLOCK` sobre las filas de saldo):
1. **Presupuestal:** restaura el saldo al eslabon PADRE (libera el monto reservado; sube el acumulador
   de reversado). El padre queda re-disponible.
2. **Documental:** pone el documento anulado en **estado 'A'** (anulado). Nunca se edita un aprobado;
   la anulacion es un cambio de estado + reverso, no un borrado.
3. **Contable:** genera el **comprobante inverso** si el original tuvo comprobante.
GUARDA BLOQUEANTE (cascada): antes de nada, valida que NO existan documentos hijos VIVOS; si los hay,
`THROW` y aborta (no libera saldo). Idempotente: anular dos veces no doble-restaura (si ya esta en 'A',
no-op o THROW controlado).

## 3. Proc 1 -- Annul_Availability_Certificate (anula un CDP)
- **Guarda bloqueante:** NO anular si el CDP tiene **compromisos (RP) activos** encima -> `THROW`.
  (Espejo del guard de aprobacion RN-01 del CDP, THROW 50150; el codigo de anulacion es NUEVO, ver s.5.)
- **Presupuestal:** libera el monto del CDP de vuelta a la **apropiacion vigente** (restaura el saldo
  disponible de la apropiacion; el CDP deja de consumir).
- **Documental:** CDP -> estado 'A'.
- **Contable:** comprobante inverso si aplica.
- Herencia/tenant: `SESSION_CONTEXT(N'tenant_id')` presente o `THROW 50100`; auditoria con usuario real
  + correlation-id (task_id).

## 4. Proc 2 -- Annul_Commitment (anula un RP / Compromiso)
- **Guarda bloqueante:** NO anular si el RP tiene **obligaciones (OBL) vivas** encima -> `THROW`.
  ("anulacion controlada que valide obligaciones vivas y libere el CDP", PRES_05.)
- **Presupuestal:** libera el monto del RP de vuelta al **CDP** (restaura el saldo del CDP, que queda
  re-comprometible).
- **Documental:** RP -> estado 'A'.
- **Contable:** comprobante inverso si aplica.
- Tenant/auditoria: idem s.3.

## 5. THROW codes (nuevos, distintos de los de aprobacion)
- Los codigos de APROBACION estan tomados: CDP=50150, RP=50115. Las anulaciones necesitan **codigos
  NUEVOS** siguiendo la convencion de RN-08 y los 3 Annul inferiores ya probados (el builder extrae la
  convencion de `Annul_Obligation` y asigna el rango contiguo; documenta cada THROW: falta-de-tenant,
  hijos-vivos, ya-anulado, no-existe). Cada THROW -> ProblemDetails (codigo + campo) en la superficie.

## 6. Contrato de aceptacion (para el checker <=15-jul)
1. **Existencia:** ambos procs existen en `DbsFinanciero_SANDBOX` (verificable por OBJECT_DEFINITION con
   el rol readonly; el rol `budget_sandbox_verifier` YA tiene EXECUTE para probarlos -> anadir 2 lineas
   GRANT por enmienda fechada cuando existan).
2. **Guarda bloqueante probada:** intentar anular un CDP CON RP activo -> THROW (no libera saldo);
   intentar anular un RP CON OBL viva -> THROW. Caso negativo es OBLIGATORIO.
3. **Camino feliz:** anular un CDP sin hijos -> saldo restaurado a la apropiacion + estado 'A' +
   comprobante inverso; idem RP -> saldo al CDP. Verificar el saldo del padre ANTES y DESPUES (cuadra al
   centavo).
4. **Idempotencia:** anular dos veces no doble-restaura.
5. **Transaccional:** una sola transaccion; fallo a mitad -> rollback completo (sin saldo liberado a
   medias). Concurrencia: UPDLOCK/HOLDLOCK sobre las filas de saldo.
6. **Tenant + auditoria:** sin SESSION_CONTEXT -> THROW 50100; toda anulacion deja rastro auditado.
7. **Paridad (para PAR-2 despues):** exec del proc vs la superficie API dan el mismo efecto de saldo.

## 7. Entrega y deadline
- **Donde:** sandbox primero (`DbsFinanciero_SANDBOX`), verificar los 7 criterios, luego BD real.
- **Cuando:** construible YA (hardening, sin restriccion del sello). Deadline duro **<=15-jul**; si ambos
  no estan verificados a esa fecha, **PAR-2 CAE completo** (condicional sellada, trigger registrado).
- **Quien:** builder NO-MEDIDO (DBA/equipo del Operador o sesion de agente fuera del estudio). NO Codex
  en un brazo del estudio.
- **Gobernanza:** el Arquitecto registra esto como tarea de hardening FUERA del contraste (o el Operador
  lo lleva en su pista de BD); no es una fila del journal de medicion.

## 8. Nota de carril (Asesor)
Diseno + study-integrity. Los requisitos exactos de dominio (columnas, nombres de acumuladores, el rango
de THROW) los fija el builder contra el precedente vivo `Annul_Obligation` + PRES_04/05/08. La
VERIFICACION empirica (correr los 7 criterios contra el sandbox) es del checker, no mia. El maker es el
builder de hardening; el checker es el Analista o quien el Arquitecto asigne. Nunca auto-verificacion.
