# ENCARGO DBA - Acceso a BD sandbox para el participante REMOTO (Contabilidad)

> Draft del Arquitecto para que el Operador lo entregue a su DBA. ADJUDICADO por el Operador
> 2026-07-06: COPIA SANITIZADA local (no VPN al sandbox real). Camino critico (mayor lead time
> del onboarding remoto). Defino requisito + criterios de aceptacion falsables; la fuente de
> dominio (nombres reales de instancia/tablas/logins) la completa el DBA.

## 1. Objetivo
Dar al participante remoto (empleado, maquina propia, huso UTC-5) acceso de VERIFICADOR a una
BD sandbox para las pruebas de paridad de Contabilidad (superficie proc-vista, F-NOVA-01), SIN
exponer datos reales de entidades publicas colombianas.

## 2. Decision del Operador (vinculante)
- **COPIA SANITIZADA local restaurada en la maquina del empleado** (NO VPN al sandbox real),
  porque el sandbox actual tiene datos reales. Si el DBA confirma que el sandbox ya es
  100% sintetico/no-sensible, VPN es aceptable como alternativa.
- La paridad del estudio se sostiene: es sobre ESQUEMA/superficie (proc + vista + THROW), no
  sobre filas -> una copia sanitizada (esquema identico, datos sinteticos) es suficiente.

## 3. Entregables del DBA
1. **Copia del sandbox restaurada localmente** en la maquina del empleado (o imagen que el
   empleado restaura), con el ESQUEMA identico al sandbox de referencia (procs, vistas,
   Security.*, tablas base de Contabilidad `maco*/Cont*` cuando el analisis las defina).
2. **Sanitizacion verificable:** cero PII real (NITs, nombres de terceros, valores reales de
   entidades) -> datos sinteticos o enmascarados. Prueba negativa: un muestreo de las tablas
   sensibles no contiene ningun valor real (criterio de aceptacion del DBA).
3. **Login/rol de verificador** patron `budget_sandbox_verifier`: grants MINIMOS
   (EXECUTE sobre los procs de paridad + SELECT sobre las vistas/tablas que consulten +
   VIEW DEFINITION), NUNCA sysadmin, NUNCA sa.
4. **Guard de entorno:** los scripts abortan si `DB_NAME() NOT LIKE '%SANDBOX%'` (mismo patron
   del grant BR-C4). JAMAS contra produccion.
5. **Nota #14 (tenant-isolation, seguridad ALTA, ya atestada):** si la copia va a incluir la
   familia de vistas `vw_Commitment_Availability_Validation`, es el momento de decidir con el
   DBA el fix real del hallazgo #14 -> o la vista expone `tenant_id`, o se cablea RLS
   (`SECURITY POLICY`); el criterio esta en SPEC-NOVA-P4-006 6l/criterio 13. No bloquea el
   acceso, pero es el gap del piso minimo de seguridad (con #5/auth) y la copia remota es
   justo donde el aislamiento cross-tenant importa.

## 4. Criterios de aceptacion (falsables)
- El empleado, con su login verificador, ejecuta un smoke de paridad (1 proc + su vista) y
  obtiene resultado; sin login sysadmin.
- Muestreo de tablas sensibles = 0 valores reales (sanitizacion demostrada).
- Guard de entorno probado (script rechaza una BD sin '%SANDBOX%').
- Sin secretos en scripts ni en el repo; la copia no se commitea.

## 5. Lead time (camino critico)
Es infraestructura fuera del protocolo (restaurar + sanitizar + grants + validar en maquina
ajena) -> el MAYOR lead time del onboarding remoto. Arrancar YA en paralelo al analisis de
Contabilidad; el analisis define despues QUE tablas/procs entran en la copia.
