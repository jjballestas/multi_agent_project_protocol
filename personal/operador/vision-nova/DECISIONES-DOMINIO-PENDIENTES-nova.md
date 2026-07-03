# Decisiones de dominio pendientes - NOVA Budget (tracker vivo del Asesor)

> Consolida las preguntas de dominio que las SPECs de NOVA-DEV dejan MARCADAS (no las inventan:
> las sacan a la superficie, comportamiento DoR/anti-vibecoding correcto). AQUI las resuelve el
> Operador. Flujo: Operador llena "Resolucion" -> el Asesor rutea cada una al Arquitecto por
> mailbox -> el Arquitecto la hornea en el campo de la SPEC. Se mide la coordinacion, asi que
> resolverlas en lote antes/al arrancar Sprint 1 reduce idas y vueltas.
>
> Ultima actualizacion: 2026-07-03 (rondas NOVA-DEV 1-7: P3-001..005 + P4-004 + P6-003). El Asesor lo
> actualiza cada ronda. Fuente: Area_comun/specs/nova/ (HEAD b678221).
> Ronda 7 (P6-003 OpenTelemetry, pool Q4, infra transversal): LIMPIA, sin nuevas decisiones de dominio.
> Aislamiento OK (excluye el reporte de negocio P2.2 baseline). N/A a la enumeracion s.5 (no consume BD).
> Ronda 6 (P4-004 Apply_Obligation_Adjustment, pool Q4, aislamiento CRITICO): LIMPIA, sin nuevas
> decisiones de dominio. Aislamiento ejemplar (excluye territorios baseline P4.1/P4.2/P4.3, leyo_codigo_hermano=NO,
> verificacion dedicada en el gate). Hardening: anulacion de acto de ajuste sin validacion aguas abajo (B-02).
> Ronda 4 (P3-004 Obligation) y ronda 5 (P3-005 Payment): SIN nuevas decisiones de dominio (DD-01
> autorizacion reafirmada). P3-005 es criticidad ALTA / frontera Treasury -> FUERA del pool Q4 (solo
> descriptiva). El egreso real (banco/retenciones/comprobante) y el circuito radicacion/liquidacion se
> DIFIEREN a GOAL-P5/hardening (no son decisiones de dominio; ver seccion 3).

## 1. Decisiones de dominio (TU resuelves)

| ID | SPEC / campo | Pregunta | Contexto / comportamiento legacy | Opciones | TU RESOLUCION | Estado |
|---|---|---|---|---|---|---|
| DD-01 | P3-001/002/003, campo 2 (usuario) | Modelo de autorizacion para Sprint 1: mientras NO exista la matriz por operacion (BR-C4), ?se acepta el supuesto "cualquier usuario autenticado con rol presupuesto captura/aprueba/emite"? | La matriz por operacion (emitir != aprobar != anular, maestro s.08-C) aun no esta sembrada en BD (brecha NOVA-PRES-001 s.6 B-05). La SPEC declara el supuesto temporal con via de salida: policy por operacion via BR-C4 post-Sprint-1. | (a) Aceptar el supuesto para Sprint 1 + confirmar que BR-C4 entra post-Sprint-1. (b) Exigir separacion minima ya (p.ej. aprobar requiere rol distinto de capturar) antes de construir. | _[pendiente]_ | ABIERTA |
| DD-02 | P3-003, alcance p.3 y restr. 6d | El "objeto" del compromiso (RP): ?se norma el minimo de 15 caracteres del legacy, se cambia, o se relaja? | Legacy exige >=15 chars en el objeto del RP. La SPEC lo marca "decidir si norma" (B-04). | (a) Mantener >=15 como norma. (b) Otro minimo (indicar N). (c) Solo "no vacio", sin minimo. | _[pendiente]_ | ABIERTA |
| DD-03 | P3-003, restr. 6d | Referencia SECOP vacia: ?cual es el valor por defecto documentado? | El legacy usaba el centinela magico '0' (sin significado) -> prohibido replicarlo. La SPEC exige un default documentado. | (a) Permitir null/vacio explicito (campo opcional). (b) Marca "N/A" declarada. (c) Hacer SECOP obligatorio cuando aplique (indicar cuando). | _[pendiente]_ | ABIERTA |

## 2. Supuestos ya declarados con via de salida (solo CONFIRMAR)

- **Vigencia explicita en UI** (F-NOVA-05, transversal): mientras `is_current` apunte a 2026 (cerrada)
  y 2027 no tenga presupuesto inicial, la UI exige vigencia explicita (sin default). Es una decision de
  producto ya tomada en la SPEC; solo requiere tu visto bueno. La correccion de `is_current`/arranque
  2027 es HARDENING (seccion 3), no decision de dominio.

## 3. (Referencia) Brechas de BD = HARDENING, NO son decisiones de dominio

Estas NO las decides como dominio; van por la cola de hardening (fix de BD/proc). Se listan para que
no se confundan con lo de arriba:
- B-01 (P3-002): `vw_Availability_Certificate_Line_Balance` con `committed_amount=0` (saldo de lectura
  inflado) -> la app compensa usando `vw_Commitment_Availability_Validation`; solicitar recrear la vista.
- B-02/RN-08 (P3-002): el proc no valida saldo por proyecto BPIN -> la app valida contra
  `vw_Investment_Project_Detail_Balance`; solicitar elevar la validacion al proc.
- B-01/RN-10 (P3-003): la BD no fuerza fecha del RP >= fecha del CDP -> validacion en caso de uso;
  solicitar elevar al proc.
- `is_current` -> 2026 cerrada / arranque 2027 (transversal): item de hardening ALTA.
- B-01/B-02 (P3-004): NO existen procs go-forward de radicacion/liquidacion/causacion
  (`Create_Radication`/`Liquidate_Radication`/`Post_Voucher`) ni retenciones -> circuito PayControl
  (GOAL-P5) + hardening; P3-004 solo enlaza el documento fuente por el puente existente, no lo crea.
- B-01..B-05 (P3-005 Payment, frontera Treasury): el egreso real (banco/medio/retenciones/comprobante),
  las notas de tesoreria, la numeracion por series (hoy MAX+1) y la guarda de vigencia abierta del egreso
  -> TODO Tesoreria/PayControl go-forward (GOAL-P5) + hardening. P3-005 cubre solo el CONTROL PRESUPUESTAL.

## 4. GRANT EXECUTE (accion del Operador, no es decision de dominio)

El conector readonly `nova_sql_connector_readonly_s9` tiene SELECT/VIEW DEFINITION pero NO EXECUTE
(Msg 229). Para las pruebas de PARIDAD (ejecutar procs/Get_*) del gate y del SELLO s.5 se necesita
GRANT EXECUTE al rol de verificacion. La verificacion de EXISTENCIA no lo necesita.

---
Se iran agregando filas con P3-004 (Obligation), P3-005 (Payment/Treasury) y el pool Q4 no-P3.
