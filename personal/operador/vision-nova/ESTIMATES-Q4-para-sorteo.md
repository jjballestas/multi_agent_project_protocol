# Estimates S/M/L del pool Q4 - insumo del sorteo del sello (llenar por el Operador)

> Insumo del SELLO Etapa 1 (s.6). Los estimates S/M/L los declara el OPERADOR (dueno de dominio) ANTES
> del sorteo, y se pre-registran (anti-HARKing: se congelan al sellar, no se re-abren). El sorteo
> ligero/completo es ESTRATIFICADO por familia/tamano, asi que necesita el tamano por unidad.
>
> El Asesor prepara aqui la lista + los HECHOS DE ALCANCE de cada SPEC (no el estimate: el esfuerzo real
> en tu stack/equipo lo juzgas tu). La columna "sugerencia" es SOLO referencia de alcance -- ignorable;
> la que cuenta es TU ESTIMATE.
> Fuente: Area_comun/specs/nova/ (9 SPECs revisadas). Fecha: 2026-07-03.
>
> Pool Q4 = 10 unidades nominales (media/baja; P3.1 pattern-setter y P3.5 ALTA/Treasury quedan FUERA).
> RECORDAR: los 4 Get_*_List son un cluster casi isomorfo (n efectivo < 10, ya sellado).

| # | Unidad | Crit. | Q4 | Hechos de alcance (de la SPEC) | Sugerencia (ref.) | TU ESTIMATE |
|---|---|---|---|---|---|---|
| 1 | **P4-004** Apply_Obligation_Adjustment (reintegro 14) | media | DENTRO | 1 proc (Apply_Obligation_Adjustment) + TVP; ~2 endpoints (aplicar + preview); UI (seleccion+monto+simular); SIN borrador (aplica atomico) | M | _[ ]_ |
| 2 | **P3-002** Availability Draft / CDP | media | CONDIC. | maquina de estados draft; 1 proc (Approve_Availability_Certificate_Draft); ~6 endpoints (crear/lineas/ready/validate/approve/discard/get); UI captura+preview+balance; manejo BPIN | M | _[ ]_ |
| 3 | **P3-003** Commitment Draft / RP | media | CONDIC. | draft SM; 1 proc (Approve_Commitment_Draft); ~6 endpoints; herencia de lineas del CDP; UI; terceros (beneficiario/solicitante) | M | _[ ]_ |
| 4 | **P3-004** Obligation Draft | media | CONDIC. | draft SM; 1 proc (Approve_Obligation_Draft); ~6 endpoints; herencia del RP; puente a documento fuente; UI | M | _[ ]_ |
| 5 | **P2-003** UI de exploracion (shell) | baja | DENTRO | FRONTEND puro (React): componentes genericos grid/filtros/detalle/export reutilizables; sin backend propio; cliente OpenAPI | S-M | _[ ]_ |
| 6 | **P6-003** OpenTelemetry / Observabilidad | baja | DENTRO | INFRA transversal: wiring OTel (traces/metrics/logs) en 4 capas + middleware correlation id + health checks; no consume BD | M | _[ ]_ |
| 7 | **Get_Availability_Certificate_List** (BR-C3) | baja | DENTRO | 1 proc de lectura a CREAR sobre vista existente + 1 GET + DTO + grid | S | _[ ]_ |
| 8 | **Get_Commitment_List** (BR-C3) | baja | DENTRO | idem (proc de lectura + GET + DTO + grid) | S | _[ ]_ |
| 9 | **Get_Obligation_List** (BR-C3) | baja | DENTRO | idem | S | _[ ]_ |
| 10 | **Get_Payment_List** (BR-C3) | baja | DENTRO | idem (sobre treasury.Payment_Order_Budget_Line) | S | _[ ]_ |

## Notas para estimar
- "CONDIC." = entra al pool Q4 solo si su DEC esta cerrada al sello Etapa 2 (P3.2/P3.3/P3.4).
- Los estimates son de ESFUERZO (S/M/L), no de criticidad. Un item "baja criticidad" puede ser M de esfuerzo.
- Al sellar (08-jul), estos valores se copian a la s.6 del SELLO y se congelan; el sorteo NIST estratifica por ellos.
- FUERA del pool (no se estiman aqui, referencia): P3.1 Initial Budget Draft (pattern-setter), P3.5 Payment (ALTA/Treasury).
