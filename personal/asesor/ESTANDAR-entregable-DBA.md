# ESTANDAR - Entregable al DBA (formato completo del Asesor)

> Proposito: cada pedido de BD que el Asesor produce debe ser AUTOCONTENIDO, para que el DBA-agente
> (gobernado y verificado directamente por el Operador, que diseno la BD) lo ejecute y devuelva evidencia
> EN UN SOLO CICLO, sin round-trips a mitad de verificacion. El Operador es el intermediario gobernante;
> NO hay canal directo Asesor<->DBA (coordinacion off-ledger = fuga; separacion de credenciales = del DBA).
> Lecciones horneadas (los round-trips que ya pagamos): faltaba VIEW DEFINITION, la connection string,
> el QUOTED_IDENTIFIER, el reset entre corridas. Este formato los PRE-EMPTE.

## Checklist de secciones (todo pedido de BD las lleva)

### 0. Frontera / firewall
- Es HARDENING (fuera del estudio medido, regla 8) o superficie MEDIDA? El proc SQL siempre es hardening;
  la superficie C#/API es la unidad medida. El proc pre-existe; el DBA lo hace, NO el dev medido.
- Sandbox primero (`DbsFinanciero_SANDBOX`), luego prod. NUNCA secretos en scripts/repo/mailbox.

### 1. Objetivo + deadline + relevancia de estudio
- Que, por que, para cuando, y a que gate/PAR/pregunta sirve.

### 2. Objetos a crear/alterar + PRECEDENTE a copiar
- Lista de procs/tablas/triggers. Precedente vivo a replicar (p.ej. `Annul_Obligation`, `Apply_*`).
  El DBA extrae con `OBJECT_DEFINITION`/`sp_helptext` y replica.

### 3. Contrato por objeto
- Inputs (params), GUARDA(S) bloqueante(s), efectos (presupuestal/documental/contable), estado final,
  THROW codes NUEVOS (distintos de los de aprobacion), tenant (`SESSION_CONTEXT`), auditoria (usuario+task_id).

### 4. SUPERFICIE DE PERMISOS COMPLETA (la que pre-empte los round-trips) -- rol `budget_sandbox_verifier`
- [ ] `GRANT EXECUTE` sobre cada proc nuevo/objetivo.
- [ ] `GRANT SELECT` sobre cada vista que la superficie/paridad lee (incl. la vista de saldo).
- [ ] **`GRANT VIEW DEFINITION`** sobre cada proc cuyo THROW hay que re-verificar (F-NOVA-01 falsabilidad:
      leer `OBJECT_DEFINITION`/`sys.sql_modules`). **Este es el que falto en P4.1.** EXECUTE != VIEW DEFINITION.
- [ ] **Triggers:** SQL Server NO acepta `GRANT VIEW DEFINITION` directo sobre un trigger DML -> se otorga
      sobre la **tabla padre** (p.ej. `Budget_Adjustment` resolvio `trg_budget_adjustment__cascade_status`).
      Enumerar proc -> su(s) trigger(s) -> tabla(s) padre.
- Toda ampliacion del grant surface entra por **enmienda fechada** al `sandbox-grant-execute.sql` (sello s.5).

### 5. Session options que el proc/harness necesita
- `SET ANSI_NULLS ON; SET QUOTED_IDENTIFIER ON;` al CREAR el proc (obligatorio con columnas computadas/
  indices/vistas indexadas -- fue el bloqueo del reset) y en la SESION del harness que lo llama.
- `SESSION_CONTEXT(N'tenant_id')` presente o THROW 50100.

### 6. Env wiring (si aplica al harness)
- Variables que el harness necesita, con VALOR ejemplo (SIN el secreto). Ejemplo:
  `NOVA_BUDGET_PARITY_CONNECTION_STRING` (con login de bajo privilegio; password SOLO en env var de usuario
  de Windows / secret store, NUNCA archivo) + `NOVA_BUDGET_SANDBOX_RESET_SQL` (invocacion del reset, no-secreto).
- Regla: el DBA setea el secreto en el entorno; agentes solo CONFIRMAN presencia, nunca manejan el valor.
- Cuidado operativo: procesos abiertos no recargan env vars de usuario -> relanzar el proceso/cron consumidor.

### 7. Reset / aislamiento (si el objeto muta)
- Mecanismo de reset a la linea base sellada ENTRE corridas (proc no-admin scoped por task_id, restaura a
  estado previo `previous_*`, no reactivate ciego). Guard `DB_NAME() LIKE '%SANDBOX%'`.

### 8. Criterios de aceptacion + EVIDENCIA a devolver (el DBA los corre y adjunta)
1. Existencia (objeto creado, verificable por `OBJECT_DEFINITION`).
2. **VIEW DEFINITION visible** para el verifier (`HAS_PERMS_BY_NAME(...,'VIEW DEFINITION')=1`, `OBJECT_DEFINITION` no-NULL).
3. **Set de THROW re-verificado contra el texto DESPLEGADO** -- NO asumir que el set documentado es completo/
   exacto (precedente F-0246-02: un proc hermano divergia). Listar los THROW que REALMENTE aparecen.
4. Guarda bloqueante -- CASO NEGATIVO obligatorio (intentar la operacion con hijos vivos -> THROW, sin mutar).
5. Camino feliz con CUADRE AL CENTAVO (saldo del padre antes/despues; leido de la vista, no recalculado).
6. Idempotencia (repetir no doble-aplica).
7. Transaccional (fallo a mitad -> rollback completo).
8. Tenant (sin `SESSION_CONTEXT` -> THROW 50100).
- Evidencia = query + resultado real (NUNCA el connection string ni el secreto).

### 9. Seguridad
- Guard `IF DB_NAME() NOT LIKE '%SANDBOX%' THROW` (fail-closed, no corre en prod).
- Sin passwords/secretos en el script, repo o mailbox. `TrustServerCertificate=True` solo por localhost/sandbox.

### 10. Lo que NO hacer
- No tocar los procs de aprobacion existentes. La logica de saldos vive en el PROC, no en C# (BD manda).
- No modelar el esquema completo en C# (doble verdad). No anular con hijos vivos.

## Nota de uso
El Asesor produce el pedido con estas 10 secciones llenas (las que apliquen). El Operador lo pasa al
DBA-agente que gobierna. El DBA devuelve la evidencia de la seccion 8. El Asesor la revisa (study-integrity)
y rutea al Arquitecto (enmienda fechada del grant + desbloqueo de la unidad medida que dependia).
