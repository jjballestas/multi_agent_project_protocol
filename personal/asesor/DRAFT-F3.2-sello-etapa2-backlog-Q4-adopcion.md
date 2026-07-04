# DRAFT F3.2 -- Insumo para el SELLO ETAPA 2 (<=29-jul): aritmetica del backlog + condicionalidad Q4 + regla de adopcion

> Autor: Asesor (Vision Nova). Carril: DISENO. Estado: DRAFT para que el Arquitecto lo gobierne y lo
> incorpore al SELLO ETAPA 2. Fecha: 2026-07-04.
> Depende de: SELLO ETAPA 1 (DECISION-0091, atestado seq 3831; s.5 pool Q4, s.6 sorteo, s.7 plan).
> Los campos [LLENAR-AL-SELLAR-E2] se completan con la RECONCILIACION de la ventana baseline (26-29 jul,
> Analista read-only, s.10 del sello Etapa 1), justo antes del sello Etapa 2.

## 0. Que sella la Etapa 2 (y que NO)
- SELLA: (a) la ARITMETICA del backlog reconciliada de la ventana baseline (3-25 jul) + el pool Q4
  COMPROMETIDO al Sprint 1; (b) las reglas de CONDICIONALIDAD de Q4 (ya pre-declaradas en Etapa 1, aqui
  se consolidan y se cierran las condiciones pendientes); (c) la REGLA DE ADOPCION (transferibilidad +
  migracion a la instancia Aegis, DECISION-0088).
- NO SELLA (por calendario): los RESULTADOS de Q4. Q4 ejecuta post-30-jul (contemporaneo); Etapa 2
  (29-jul) es ANTES de que abra el Sprint 1 (30-jul). Etapa 2 congela el PLAN y las REGLAS, no los datos
  causales. Anti-sobreventa: Etapa 2 no puede afirmar nada de Q4 todavia.

## 1. Aritmetica del backlog (reconciliada)

### 1.1 Ventana baseline medida (3-25 jul) -- reconciliacion
- Toda tarea de producto ejecutada en la ventana debe tener fila en el journal v1.0. La reconciliacion
  (26-29 jul, Analista read-only, s.10) mapea todo commit/rama/log del repo Nova-Budget contra los
  `tarea_id`. Sesiones sin fila = `abandonada` retroactiva; huerfanos se PUBLICAN como metrica de
  integridad del propio estudio.
- [LLENAR-AL-SELLAR-E2]: N_baseline_filas, N_abandonadas_retro, N_huerfanos_publicados, tokens_total
  del brazo baseline, defectos_post clase(b) paridad-true observados hasta el corte.
- Regla dura: GOAL-P1 (fundacion, sha256 d2a13216) EXCLUIDO del contraste (scaffolding sin dominio); su
  fila existe como piloto de maquinaria, con `tag_incidente_maquinaria` fuera de las confirmatorias.

### 1.2 Pool Q4 comprometido al Sprint 1 (de s.5, n>=10 nominal)
- 10 unidades enumeradas nominalmente en Etapa 1 s.5. Composicion por ESTIMATE (no criticidad):
  - Estrato M (estimate M, n=6): NB-P2-3, NB-P3-2, NB-P3-3, NB-P3-4, NB-P4-4, NB-P6-3.
  - Estrato S (estimate S, n=4): NB-BRC3-1, NB-BRC3-2, NB-BRC3-3, NB-BRC3-4 (cluster Get_*_List).
- CONDICIONES DE PERTENENCIA a cerrar en Etapa 2:
  - P3.2/P3.3/P3.4 son "media CONDICIONAL a DEC cerrada". [LLENAR-AL-SELLAR-E2]: confirmar que su
    decision de dominio (DD / policy por operacion) esta CERRADA al 29-jul; si no, CAEN del pool y n baja.
  - Items dependientes de hardening (PAR-2 / Annul_*) entran SOLO por enmienda fechada con entrega
    comprometida (s.5). [LLENAR-AL-SELLAR-E2]: registrar si el hardening del 15-jul entrego los procs.
  - P3.1 NO pertenece al pool (primera_unidad/pattern-setter, excluida del contraste central).

## 2. Condicionalidad de Q4 (consolidada; el hallazgo del sorteo es el eje)

### 2.1 El sorteo ya sellado (Etapa 1 s.6): 2 completo / 8 ligero
- Semilla NIST 1844242; algoritmo `h=SHA-256(tarea_id+"|"+semilla)`, `h[0] mod 2`, por-unidad.
- Resultado: **completo = NB-BRC3-4, NB-P2-3** (2 de 10); ligero = las otras 8.
- Por estrato (honesto, sin corregir): S (n=4) 1 completo / 3 ligero; M (n=6) 1 completo / 5 ligero
  (desbalance 5-1 por azar, reportado sin re-sortear).

### 2.2 Por que Q4 es SUBPOTENCIADO (declaracion de poder efectivo, no relleno)
Tres degradaciones ACUMULATIVAS, todas pre-selladas, que Etapa 2 consolida como una sola lectura honesta:
1. **Brazo completo delgado:** solo 2 de 10 unidades caen en "completo". El contraste ligero-vs-completo
   se apoya en 2 observaciones del brazo completo -> potencia baja por diseno del azar, no por eleccion.
2. **n efectivo < n nominal (cluster BR-C3):** las 4 Get_*_List son casi isomorfas (mismo patron de
   lectura 15-param sobre distintas vistas de saldo). Se tratan como CLUSTER CORRELACIONADO: aleatorizar
   4 tareas de la misma forma prueba la misma forma 4 veces. n efectivo independiente < 10. Ademas dentro
   del cluster solo NB-BRC3-4 es completo -> el unico contraste intra-cluster es 1-vs-3.
3. **Dependiente de ejecucion:** REGLA SELLADA -- si el Sprint 1 no ejecuta >=10, Q4 se reporta
   SUBPOTENCIADO, NO se rellena (s.5). [LLENAR-AL-SELLAR-E2 / post-30-jul]: n realmente ejecutado.
- CONSECUENCIA para Etapa 2: se SELLA la frase de poder efectivo (Q4 = evidencia causal DEBIL, cota, no
  puntual; ITT sobre <=2 completos y un cluster correlacionado). Esto NO invalida el estudio: Q1/Q2 siguen
  siendo las confirmatorias fuertes; Q4 aporta direccion causal con incertidumbre declarada. El veredicto
  de compra se DIFIERE a la replica employee-run (s.7). Anti-sobreventa integrado.

### 2.3 Doble rol Get_*_List (NO doble-conteo)
El cluster BR-C3 es miembro gobernado de PAR-D (Q3 descriptivo/cota) Y fabrica en Q4 (causal). Son
contrastes pre-registrados DISTINTOS; su fase SPEC se excluye del delta (simetria con spec_prepagado de
P2.2). Etapa 2 reafirma la separacion para que nadie lea Q3 y Q4 como la misma evidencia.

## 3. Regla de adopcion (transferibilidad + migracion a Aegis)

### 3.1 Que cuenta como "adoptado" (criterio sellable)
Una segunda instancia de dominio real (Nova-Budget) ADOPTA la metodologia cuando, de forma verificable:
1. corre el PATRON BASELINE CONGELADO (el de P4.1 pattern-setter: aprobacion-via-proc + gateway tipado +
   saldo-de-vista) + maker!=checker DURO + gates atestados;
2. su governance operativa vive en su instancia `Aegis/` (DECISION-0085/0088), NO en el hub;
3. el hub registra la CROSS-ATESTACION: el journal del hub guarda el sha256 de la atestacion de Aegis por
   gate (regla dual, DECISION-0088).

### 3.2 La migracion ES la evidencia (Q5, no cosmetica)
- HOY (ventana del estudio, hasta 30-jul): asiento = HUB (el brazo gobernado es el tratamiento medido; su
  atestacion debe estar en el MISMO #4 que la medicion + sello). No migrar a mitad del estudio.
- POST-sello: migra a NOVA/Aegis (instancia operativa del equipo). meta/estudio/metodologia canonica =
  hub SIEMPRE (nunca migra); governance operativa del producto = su instancia Aegis/ tras adoptar.
- Esa migracion pre-registrada ES la replica employee-run que da la evidencia de transferibilidad de Q5
  (segunda instancia dominio real vs N=500 auto-dogfood de Zeus-Protocol). Arquitectura y estudio se
  alinean. Etapa 2 sella el CRITERIO; la ejecucion es Carril B / post-sello.

### 3.3 Delimitacion (que afirma / NO afirma la adopcion)
- AFIRMA: transferibilidad de la MAQUINARIA (una instancia distinta, dominio real, corre el protocolo con
  atestacion cruzada verificable).
- NO AFIRMA: que el gobierno mejora la calidad (Q4 subpotenciado + maker!=checker ya en ambos brazos). El
  tratamiento medido es el checker FORMAL atestado + la maquinaria, no "separar maker de checker".

## 4. Checklist de Etapa 2 (para el Arquitecto)
- [ ] Reconciliacion baseline 26-29 jul incorporada (1.1).
- [ ] Condiciones de pertenencia del pool cerradas (P3.x DEC; hardening 15-jul) (1.2).
- [ ] Frase de poder efectivo de Q4 sellada (2.2).
- [ ] Criterio de adopcion + regla dual de cross-atestacion sellados (3.1, 3.2).
- [ ] Delimitacion anti-sobreventa reafirmada (2.2, 3.3).
- Atestacion: submit_intent (decision) del sha256 del doc Etapa 2 + manifiesto -> #4 (patron de Etapa 1).

## 5. Nota de carril (Asesor)
Diseno + study-integrity. La reconciliacion empirica (mapear commits vs tarea_id contra la BD/repo
desplegado) es del Analista read-only; yo aporto el marco y la aritmetica. El maker de cualquier SPEC
derivada es Codex; el checker es el Analista. El sello lo ejecuta el Arquitecto (submit_intent); yo no
toco el ledger.
