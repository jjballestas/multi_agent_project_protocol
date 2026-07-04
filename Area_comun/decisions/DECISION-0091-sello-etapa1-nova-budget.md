---
decision_id: DECISION-0091
title: "SELLO Etapa 1 del estudio NOVA Budget: corpus congelado (8 artefactos + hash de manifiesto), schema v1.0, sorteo pre-registrado ejecutado (semilla NIST pulso 1844242)"
status: accepted
date: 2026-07-04
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0078, DECISION-0041, GOAL-VISION-NOVA-001]
phase: P2
scope: study-seal
approval_ref: "DIRECTIVA operador MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-ejecuta-sello-ahora-supersede-standdown: ejecutar el sello AHORA (T ya fijado en commit cbc1ee2, 2026-07-04T03:52:25Z; sellar antes del 08-jul es mas defendible: el sorteo queda locked antes de cualquier dev medido). Revision de integridad previa del Asesor (mecanismo solido, 1 hallazgo menor de wording corregido en commit 89d2823 antes de sellar)."
---

# DECISION-0091 - SELLO Etapa 1 del estudio NOVA Budget

> Registra la atestacion permanente del sello pre-registrado del estudio NOVA (baseline vs gobernado,
> Sprint 1). Ancla via este `.md` + el intent `decision` del hub (cadena #4). El documento vivo del sello
> es `personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md`; esta DECISION es su registro
> formal atestado, con los valores finales que no pueden auto-referenciarse dentro del propio commit del
> sello (T, sha256 del documento, hash de manifiesto).

## Ancla externa (anti semilla-moldeable, anti-HARKing)

- **T (timestamp del pre-commit del sorteo):** commit `cbc1ee2d6a344d4db5b69c2f7823cc0bc0aa8b0c`,
  `2026-07-04T03:52:25Z`. Introdujo la tabla congelada de 10 unidades (tarea_id + par_id + estrato +
  estimate) + el algoritmo exacto del sorteo, ANTES de conocer la semilla.
- **Semilla:** primer pulso del NIST Randomness Beacon (chain 2) estrictamente posterior a T.
  `pulseIndex 1844242`, `timeStamp 2026-07-04T03:53:00.000Z` (el pulso previo, `1844241`, es
  `2026-07-04T03:52:00.000Z`, ANTERIOR a T; verificado que 1844242 es el primero posterior).
  `outputValue`:
  `9CD3E6A0B366DFD164BA63C18CAE7D09B1CD76867DAD8912AEA1061D41E95226A2B0FCB937542D1DC80BC49AA00FE562B030866E9B1706CD76A26A6E5C7379EF`.
  Verificable por terceros: `https://beacon.nist.gov/beacon/2.0/chain/2/pulse/1844242`.
- **Correccion de credibilidad pre-sello (hallazgo del Asesor, remediado en commit `89d2823` ANTES del
  sorteo):** el documento del sello decia "ESTRATIFICADA por familia/tamano" para la asignacion, pero el
  algoritmo real (ya sellado en s.6.1 del documento desde el commit `cbc1ee2`) es paridad SHA-256
  por-unidad, NO ajustada por estrato -- el estrato solo organiza el REPORTE, no balancea la asignacion.
  Se corrigio el wording a "por-unidad, reportada por estrato, NO balanceada" en las 3 menciones (s.5,
  s.6 paso 3, NOTA DE INDEPENDENCIA) antes de correr el sorteo, para no sobre-afirmar balance que el
  algoritmo no garantiza.

## Resultado del sorteo (10 unidades, algoritmo: orden alfabetico, h=SHA-256(tarea_id+"|"+semilla), h[0] mod 2: par->completo / impar->ligero)

| tarea_id | Unidad | estrato | h[0] | asignacion |
|---|---|---|---|---|
| NB-BRC3-1 | Get_Availability_Certificate_List | S | 0x9d (157) | ligero |
| NB-BRC3-2 | Get_Commitment_List | S | 0x11 (17) | ligero |
| NB-BRC3-3 | Get_Obligation_List | S | 0x1b (27) | ligero |
| NB-BRC3-4 | Get_Payment_List | S | 0x3c (60) | completo |
| NB-P2-3 | P2.3 UI de exploracion (shell) | M | 0x7e (126) | completo |
| NB-P3-2 | P3.2 Availability Draft / CDP | M | 0x6b (107) | ligero |
| NB-P3-3 | P3.3 Commitment Draft / RP | M | 0x49 (73) | ligero |
| NB-P3-4 | P3.4 Obligation Draft | M | 0xff (255) | ligero |
| NB-P4-4 | P4.4 Apply_Obligation_Adjustment | M | 0xe5 (229) | ligero |
| NB-P6-3 | P6.3 OpenTelemetry / Observabilidad | M | 0x11 (17) | ligero |

**Total: 2 completo (NB-BRC3-4, NB-P2-3) / 8 ligero.** Estrato S (n=4): 1 completo/3 ligero. Estrato M
(n=6): 1 completo/5 ligero -- desbalance 5-1 real por azar de la semilla, REPORTADO sin corregir (regla
ex-ante de s.6.1 paso 3 del sello: n=6 es insuficiente para forzar paridad sin introducir un criterio
ad-hoc post-semilla). DISJUNCION DURA (s.6 paso 5 del sello): cada tarea se implementa UNA vez en el
brazo asignado.

Hashes SHA-256 completos por unidad (reproducibles con la semilla publicada arriba, concatenacion
`tarea_id + "|" + outputValue`):
```
NB-BRC3-1  9dced029a19554937646ce2c25e15b801c4c9ca1a730a386890f6eae20755039
NB-BRC3-2  11bdb4bc209380bb2767c103c16cb198e093f7cd42fe65c213b26913fe254b33
NB-BRC3-3  1b1409e62cc5f540ff63ac7762f653f1b461b97c38702339be93ba0e34ece7bd
NB-BRC3-4  3c8db091612154effa41a63997ad3873d2a9085ac20521eb5954b0c9a223f7a4
NB-P2-3    7e36c48811198e8edebffe379a1d2fe4ff742cdcecec1a7f94f283590717e3b2
NB-P3-2    6b23a918406abc4550d826dd537426a5642e9dc62d63ea0080811f106faeb4e4
NB-P3-3    4906ca958436ab3ffe149e02f008d604e0cdd65ec4bf9b7f117e5a5f9d22fc6e
NB-P3-4    ff050df100b0b50891c5938b32239072a3647bfe05630ffaf2eb102772f3b7cb
NB-P4-4    e5b20665ed3a42c06c97e44a1c758778f5a618e9ad637b218f5b4c22fe8adc50
NB-P6-3    111503133d717f5a12be246ef19e3892ae2661ce02c0339c5f0d20bbbb5a9620
```

## Corpus sellado (8 artefactos + hash de manifiesto)

Manifiesto basename-keyed, ordenado alfabeticamente (`personal/operador/vision-nova/CORPUS-MANIFEST-etapa1.txt`):

| Artefacto | sha256 |
|---|---|
| NOVA_ESTUDIO_Anexo_Diseno_Completo.json | 4a52ff58f1363f005ee8daaa72800cad065a3d0da3408422fb4c4a59be835c7c |
| NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md | ef1e56e7c1b950559d8e3952231662040a1008999baf6002eb28d7671b2e2a41 |
| NOVA_ESTUDIO_Protocolo_Medicion.md | de38530acfd927bb9c4683224a85863ca8b6ae85de5b8cd0ab09c172185969b1 |
| SELLO-ETAPA-1-nova-budget-DRAFT.md (commit `14ecefa`, ultimo edit antes de este registro) | 46d3fc025e110f96f47453a146ccef63467288adddc0e9f7e3fff900b127a2e7 |
| medicion_journal.csv (fila REAL GOAL-P1, ratificada) | d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5 |
| medicion_ledger.py | 3e92cca5962f88ff3e77286e263ea20d2b5f461e6555454fec776c99e5595344 |
| schema_defectos.json (v1.0 congelado) | 737fd4f5c379b9e96ceb160891ba6117a4d589d96fb8f5b0c612f1e74e36e8dd |
| schema_medicion.json (v1.0 congelado) | 700565a206d7066fdb08e48abceed249014569937c86ac202b3d0f57b154c23e |

**HASH DE MANIFIESTO (sha256 del listado ordenado `basename  sha256` de arriba):**
`bf91b0942417000d717f6999beee6dd341063a86e72c3bffbf04ebac7adef261`

Los 3 documentos `NOVA_ESTUDIO_*` y `medicion_ledger.py` viven fuera del hub (repo Ingenas, gitignored en
este repo); sus sha256 son estables desde el ensayo del 2026-07-04 (sin cambios). El corpus de medicion
(`personal/Arquitecto/TFM-medicion/corpus/`) esta gitignored por diseno (capa separada del N=500 sellado
de Zeus-Protocol, FONDO INTOCABLE, sin tocar).

## Schema v1.0 congelado (hallazgos del piloto GOAL-P1 horneados)

`schema_medicion.json` y `schema_defectos.json` pasaron de `v-piloto-0` a `v1.0` (2026-07-04). Horneados
en `schema_medicion.json._meta.hallazgos_piloto_goalp1_horneados`:
1. `tokens_total_atribuibles` = moneda confirmatoria del brazo baseline (desglose por cubeta NO
   capturable del runtime `codex-exec`; solo el numero cumulativo en STDERR). Q4 total-vs-total intacto;
   Q1 degrada a total-marginal.
2. El mecanismo de captura de tokens lee `err.log` (STDERR), no `out.log`.
3. `tokens_adversarial_informal` NO separable en GOAL-P1 (adversarial in-session); de P2 en adelante,
   sesion separada (taggable); cache no aislable entre brazos -> mismo runtime o declarar cache-confound.

## Precondicion sandbox de mutadores

Sellada por separado (`Area_comun/specs/nova/SANDBOX-MUTADORES-mecanismo-sellado.md`, 2026-07-04):
sandbox `DbsFinanciero_SANDBOX` + rol `budget_sandbox_verifier`, EXECUTE real, aislamiento verificado,
RESET obligatorio entre miembros/brazos. Precondicion de P4-001/002/003/004 -> READY, adelantada.

## Efecto de esta DECISION

- El corpus, el schema y el sorteo del estudio NOVA Etapa 1 quedan CONGELADOS: nada de lo aqui registrado
  se re-abre (regla de oro del sello). Cambios post-sello requieren enmienda fechada via el Operador con
  causa, jamas silenciosa.
- El dev MEDIDO de las unidades del pool Q4 (P2.1/P2.2 ya abiertas como fundacion/PAR-D-anclado desde
  antes; el resto de la tabla arriba) corre en el brazo asignado por esta tabla cuando abra su ventana
  (baseline 3-25-jul; gobernado post-30-jul segun s.3 del sello).
- No toca el epoch pineado (1.14.0), `protocol.config.json` (sha256 `2e35f26e...`), ni el dataset TFM
  N=500 sellado (Zeus-Protocol): capas separadas, FONDO INTOCABLE intacto.
- Referencia viva: `personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md` (documento
  completo, todas las secciones); esta DECISION es su registro atestado permanente en la cadena #4.
