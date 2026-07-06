# ENCARGO DBA - BR-C4 (autorizacion por operacion) - hardening en sandbox

> DRAFT del Asesor (espejo del encargo PAR-2 s.24). Para que el Operador lo entregue a su DBA.
> Los `[PLACEHOLDER]` los completa la fuente de dominio (Operador + DBA); yo defino requisito + criterios
> de aceptacion falsables. NO es dev medido: es HARDENING (el DBA crea la capacidad; el dev gobernado de
> Sprint 1 cablea la superficie C#; el dev JAMAS crea los procs, regla 8).

## 1. Objetivo
Sembrar en `DbsFinanciero_SANDBOX`, antes del 29-jul, la matriz de autorizacion por operacion (BR-C4:
emitir != aprobar != anular) para los documentos de la familia P3, de modo que **P3.2/P3.3/P3.4 conserven
su elegibilidad al pool Q4 (n=10)**. Red de seguridad: si no se entrega verificado <=29-jul, la condicion
ya sellada ejecuta automaticamente la caida a n=7 (opcion a) sin accion adicional.

## 2. Alcance (documentos x operaciones)
| Documento | Unidad Q4 | Operaciones a gobernar |
|---|---|---|
| Availability Certificate (CDP) | P3.2 | crear/capturar borrador, aprobar/emitir, anular |
| Commitment (RP) | P3.3 | crear/capturar borrador, aprobar/emitir, anular |
| Obligation (OBL) | P3.4 | crear/capturar borrador, aprobar/emitir, anular |

Principio BR-C4: para cada `(documento x operacion)` se exige un **permiso/rol distinto**; emitir != aprobar
!= anular (no basta "usuario autenticado con rol presupuesto", que es el supuesto simplificado de DD-01).

## 3. Entregables del DBA
1. **Modelo de autorizacion sembrado:** filas `(documento x operacion -> permiso requerido)` en la tabla de
   permisos `[TABLA-PERMISOS]` + los roles `[ROLES]` creados/asignados.
2. **Guardas en los procs:** cada proc de `[PROCS-BORRADOR/APROBAR/ANULAR]` verifica el permiso del llamante
   (via `SESSION_CONTEXT` del usuario + la matriz) y hace `THROW <codigo>` si el llamante no lo tiene.
3. **Set de codigos THROW asignado y documentado** (rango nuevo; ver s.5, evitar colision).
4. **Verificacion falsable** (F-NOVA-01): smoke real con rollback (s.4).
5. **Superficie de grant** para el verificador: `VIEW DEFINITION` + `SELECT` sobre `[TABLA-PERMISOS]` (y
   cualquier vista/tabla nueva) al rol `budget_sandbox_verifier`.
6. **Entrega como enmienda fechada** (formato s.24/s.25 del sello) con el set THROW real listado.

## 4. Criterios de aceptacion (falsables, se verifican como rol de sandbox, no sysadmin)
- `OBJECT_DEFINITION` de cada proc muestra la guarda de permiso (no solo documentado/smoke).
- **Separacion de operacion demostrada con 3 identidades distintas:** un usuario con permiso de EMITIR
  emite OK pero es **bloqueado (THROW)** al APROBAR y al ANULAR; idem para el aprobador y el anulador.
- Usuario sin ningun permiso: `THROW` en las tres operaciones.
- Idempotencia/rollback donde aplique; cero residuos tras el smoke.
- Guard de entorno: el script aborta si `DB_NAME() NOT LIKE '%SANDBOX%'` (probado contra prod ANTES de
  otorgar, como en el grant previo). JAMAS en produccion.
- Verificado con `nova_budget_verifier` (no `sa`); sin secretos en el script; sin datos reales/PII.

## 5. Placeholders a completar (fuente de dominio: Operador + DBA)
- `[TABLA-PERMISOS]`: nombre real de la tabla de permisos (posible `Security.Permission` u otra).
- `[PROCS-...]`: nombres reales de los procs de borrador/aprobacion/anulacion de CDP/RP/OBL.
- `[ROLES]`: taxonomia de roles (p.ej. emisor/aprobador/anulador presupuesto).
- `[RANGO-THROW]`: **rango 50xxx LIBRE**. Evitar colision con lo ya usado: 50065, 50083-50084, 50100, 50212,
  50230-50261, 50280-50297. **Sugerencia: 50300-50319** para BR-C4.
- `[USUARIOS-PRUEBA]`: los usuarios/roles del smoke de separacion.

## 6. Deadline y gobernanza
- **Entrega verificada <= 29-jul** (antes del sello Etapa 2). Si no llega, la condicion sellada ejecuta n=7
  automaticamente (opcion a); no hay penalidad, es la red de seguridad pre-declarada.
- Al entregar, el Arquitecto registra la **enmienda fechada** del sello (como s.24/s.25) y confirma que
  P3.2/P3.3/P3.4 mantienen elegibilidad Q4 -> n=10. La decision de intentar (b) es del Operador (ya tomada:
  tiene DBA); esto NO altera lo medido (es hardening simetrico para ambos brazos).
