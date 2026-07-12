---
decision_id: DECISION-0094
title: "SELLO Pre-registro N=6 (replica employee-run de transferibilidad, Contabilidad/Aegis): diseno congelado + sha256 del artefacto anclado ANTES de construir/medir cualquier unidad"
status: accepted
date: 2026-07-13
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0091, DECISION-0088, DECISION-0093, GOAL-VISION-NOVA-001]
phase: P2
scope: study-seal
approval_ref: "GO operador MSG-20260713-Operador-to-Arquitecto (chat + mailbox): 'GO para el sello del pre-registro N=6 + las 6 unidades medidas de Contabilidad'. Prep seal-ready del Asesor (commit hub 23b8fe5). Ejecucion del sello: Arquitecto (autoridad de ledger del hub); verificacion independiente pendiente (paso s.11.5: Analista u operador recomputan el sha256)."
---

# DECISION-0094 - SELLO Pre-registro N=6 (replica employee-run de transferibilidad, Contabilidad/Aegis)

> Registra la atestacion permanente del PRE-REGISTRO de la replica employee-run de transferibilidad de la
> metodologia gobernada al dominio Contabilidad (instancia Aegis), operada por un empleado real (Julian,
> `jheredia:v1`). Ancla via este `.md` + el intent `decision` del hub (cadena #4). El diseno pre-registrado
> (hipotesis, muestra N=6, metricas, criterio de exito/refutacion) queda CONGELADO **antes** de construir o medir
> cualquiera de las 6 unidades. Es la contraparte, para el brazo de transferibilidad, del SELLO Etapa 1 de
> Nova-Budget (DECISION-0091): fija el diseno antes de ver dato alguno (regla de oro de la metodologia: nada se
> decide despues de ver datos).

## Artefacto sellado (congelado) + hash de sello

- **Artefacto:** `Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md` (17189 bytes, ASCII puro).
  Copia congelada byte-faithful del DRAFT del Asesor `personal/asesor/DRAFT-PREREGISTRO-contabilidad-employee-run.md`
  (seal-ready en el commit del hub `23b8fe5`), mas un preambulo de sellado del Arquitecto que no altera s.0-s.11.
- **sha256 del artefacto congelado (ESTE es el sello):**
  `28fd963b2472b1b6277b45e38e3bdf92686f022b0c41de4ab6a1338597d45828`
- **Recomputo verificable por terceros (byte a byte):**
  `python -c "import hashlib;print(hashlib.sha256(open('Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md','rb').read()).hexdigest())"`
- **Sello ejecutado:** 2026-07-13 ~00:35 local (UTC+2) / `2026-07-12T22:35:57Z`, por el Arquitecto, bajo GO del operador.

## Pre-datacion (por que el sello es creible)

- **Ninguna de las 6 unidades existe aun.** El build de Contabilidad abre post-30-jul (linea roja del Sprint 1);
  ninguna unidad de la muestra se ha construido ni medido. El diseno se congela ANTES de cualquier dato -> no hay
  HARKing posible sobre la muestra, las metricas ni el criterio de exito.
- **Trazabilidad git:** el DRAFT quedo commiteado en `23b8fe5` (2026-07-13) y este sello en el commit de esta
  DECISION; ambos anteriores al build-open. La cadena #4 del hub fecha el intent `decision` de este anclaje.
- **Precondicion externa que NO es un hueco del sello:** el cableado de la instrumentacion F3.3 en Aegis
  (SELLO-PREREGISTRO s.10) es prerequisito de la 1a unidad MEDIDA, no del sello del DISENO. El diseno esta completo
  y se congela aqui; F3.3 se cabla al abrir el build, justo antes de construir la 1a unidad bajo medicion.

## Anexo de seleccion sellado (muestra N=6, fijada por el operador el 2026-07-12 ANTES de construir)

Criterio de seleccion (pre-fijado, no re-elegible mirando resultados): mezcla de dificultad (facil->alta) +
independencia alta/media (no bloquea el resto del modulo). Cobertura: 5 slices (R0/R2/R3/R4x2/R5), rango
facil->alta; R6/R7 fuera por baja independencia (deliberado).

| # | tarea | Objeto/proc | dificultad |
|---|---|---|---|
| 1 | R2-c | Reverso de comprobante manual (`Reverse_Voucher`/`Voucher_Relation`/`vw_Voucher_Adjustment_Map`) | M-A |
| 2 | R3-b | Cerrar periodo mensual (`Close_Accounting_Period` + P03/P04 + audit; NO activa `annual_close`) | Alta |
| 3 | R4-b | Importar saldos iniciales por CSV (`Import_Opening_Balance_Draft_From_File_Stage`, schema/022) | M-A |
| 4 | R5-c | Postear ajuste CHIP post-P05 (`Post_Chip_Adjustment_Voucher`, tipo `chip_adjustment`, D=C, fecha > P05) | Alta |
| 5 | R0-fuentes | CRUD de fuentes contables (`Accounting_Source`/`Accounting_Source_Numbering`/`Get_Next_Accounting_Source_Number`) | Baja |
| 6 | R4-c | Aprobar borrador de saldos iniciales (`Approve_Opening_Balance_Draft` -> `Account_Opening_Balance`) | M |

Las 6 quedan "no construir hasta medicion" (reserva); el resto del modulo avanza a velocidad de producto. La
seleccion NO se re-elige; queda sellada como anexo (fecha de fijacion 2026-07-12 + este sha256).

## Que queda congelado (regla dura post-sello)

- **s.1 Hipotesis** (H-TRANSFER: H1 gate adversarial caza defectos reales / H2 atribucion nominal por-humano /
  H3 perfil de costo en el mismo orden que el brazo gobernado de Nova-Budget) + **H0** nula.
- **s.2 Poder efectivo DECLARADO:** confirmatorio de DIRECCION/PATRON, NO estimador de magnitud (N pequeno por
  diseno; declarado por adelantado, no descubierto despues).
- **s.3 Poblacion medida** (muestra N=6, anexo arriba).
- **s.4 Metricas** (APLICAN M-Q2 defectos con paridad de detector + M-Q1 costo descriptivo; PROPIAS M-ATRIB +
  M-MANUAL; NO APLICAN Q3/Q4 por ausencia de contraste interno -- declarado, no es hueco).
- **s.7 Criterio de exito / refutacion** pre-fijado (un no-transfiere pre-registrado es resultado valido).
- Cualquier cambio de s.1-s.7 exige una **enmienda FECHADA y justificada**, visible en el ledger; jamas silenciosa.

## Verificacion independiente (paso s.11.5, pendiente de cierre)

El sello lo ejecuto el Arquitecto. La ceremonia (SELLO-PREREGISTRO s.11 paso 5) pide que un SEGUNDO firmante
(Analista u operador) recompute el sha256 del artefacto congelado y confirme que cuadra con el anclado aqui
(`28fd963b...`). Ese recomputo cierra la atestacion como pre-datada de forma independiente. Se solicita al cerrar
esta entrada; no bloquea el anclaje (el hash ya esta en la cadena #4 y es reproducible por cualquiera).

## Efecto de esta DECISION

- El diseno del pre-registro N=6 queda CONGELADO: nada de s.1-s.7 se re-abre (regla de oro del sello). Habilita
  construir/medir las 6 unidades bajo medicion cuando abra el build (post-30-jul) con F3.3 cableada, con el diseno
  ya probado como pre-datado.
- **NO toca** el epoch pineado del hub (1.14.0), `protocol.config.json` (sha256 `2E35F26E...`), ni el dataset TFM
  N=500 sellado (Zeus-Protocol): capas separadas, FONDO INTOCABLE intacto. El anclaje es por intent `decision` del
  hub (sin re-genesis). La captura de metricas vivira en el ledger de Aegis con doble ancla al hub (DECISION-0088
  p.5 / 0093), no aqui.
- Referencia viva: `Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md` (documento completo,
  s.0-s.11); esta DECISION es su registro atestado permanente en la cadena #4.
