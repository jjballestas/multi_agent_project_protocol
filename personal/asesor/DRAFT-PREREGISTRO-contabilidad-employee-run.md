# DRAFT PRE-REGISTRO -- Replica employee-run de transferibilidad (Contabilidad, instancia Aegis)

> DRAFT del Asesor (2026-07-12) para que el OPERADOR lo SELLE antes de la 1a unidad MEDIDA de Julian.
> Opcion A confirmada por el operador (pre-registro propio, no exploratoria). Encaja como seccion hermana del
> Sello Etapa 2. Base: PREP-INSTRUMENTACION-MEDICION-contabilidad-aegis.md (Arquitecto) + SPEC-NOVA-F3.3 +
> DECISION-0088/0093 + delimitacion sellada de Nova-Budget ("veredicto de compra -> replica employee-run
> PRE-REGISTRADA"). El Arquitecto afina los detalles estadisticos; el Asesor coordina y verifica study-integrity.
> NO toca el estudio Nova-Budget congelado ni el config pineado del hub (1.14.0, 2E35F26E).

## 0. Por que existe (marco)
La delimitacion YA sellada de Nova-Budget difiere el veredicto de compra a "la replica employee-run
PRE-REGISTRADA". Este documento ES ese pre-registro. Fija -- ANTES de ver dato alguno -- que afirma la replica,
que se mide, con que criterio se declara confirmada o refutada, y su poder efectivo declarado con honestidad.
Regla dura de la metodologia: nada se decide despues de ver datos.

## 1. Hipotesis (falsable)
**H-TRANSFER:** la metodologia gobernada produce, en un dominio REAL DISTINTO (Contabilidad) operado por un
EMPLEADO REAL DISTINTO (Julian, no auto-dogfood), el MISMO PATRON cualitativo demostrado en Nova-Budget:
- (H1) el gate adversarial (checker formal, maker!=checker por posesion de llave) CAZA defectos reales que los
  tests-verdes del maker no habrian cazado;
- (H2) la atribucion nominal por-humano funciona (el trabajo del empleado se firma con SU llave `jheredia:v1`,
  distinguible de los agentes y del operador);
- (H3) el perfil de costo/esfuerzo (M-Q1, descriptivo) cae en el MISMO orden de magnitud que el brazo GOBERNADO
  de Nova-Budget (no un contraste marginal; ver s.4).
**H0 (nula):** el patron NO se reproduce (el gate no caza nada nuevo / la atribucion se confunde / las metricas
van en direccion contraria a lo esperado).

## 2. Poder efectivo DECLARADO (honestidad, no se descubre despues)
Este es un confirmatorio de DIRECCION y de PATRON, **NO** un estimador con potencia estadistica de tamano de
efecto. Razon declarada por adelantado (misma disciplina que Q4-subpotenciado de Nova-Budget):
- El operador (John) hace la MAYORIA del desarrollo de Contabilidad; Julian hace un SUBCONJUNTO acotado de
  unidades DELEGADAS para aprender y usar la metodologia -> n de unidades employee-run es PEQUENO por diseno.
- Por tanto la replica CONFIRMA/REFUTA que el patron se REPRODUCE con un empleado real en un dominio real; NO
  pretende medir magnitud de efecto con intervalos de confianza estrechos.
- Cualquier lectura de "tamano del efecto" seria descriptiva, no inferencial. Se declara AQUI, no al reportar.

## 3. Poblacion medida (que unidades entran) -- FIJADA (anexo del sello)
- **DENTRO:** unidades GOBERNADAS MUTADORAS de Contabilidad construidas por Julian como maker (`jheredia:v1`),
  con gate adversarial del Analista.
- **FUERA:** RO (R1 reportes) y frontera del modulo fuente (R8 causacion ingresos/CxC, ademas CONTEMPLADO, no
  construible). R0 (maestros/parametrizacion) queda FUERA de la muestra por baja independencia (lo consume todo
  el modulo) aunque sea mutador.
- **MUESTRA SELECCIONADA (N=6), fijada por el OPERADOR el 2026-07-12 ANTES de construir; criterio = mezcla de
  dificultad (facil a alta) + independencia alta/media (no bloquea el resto del modulo):**
  1. **R2-c** -- Reverso de comprobante manual (`Reverse_Voucher` / `Voucher_Relation` / `vw_Voucher_Adjustment_Map`;
     crea `manual_accounting_reversal`, invierte D/C, relacion `reverses`; bloquea reverso de source!=accounting /
     no-manual / is_system_generated). Dificultad M-A.
  2. **R3-b** -- Cerrar periodo mensual (`Close_Accounting_Period` + P03/P04 + audit; NO puede activar la escotilla
     `annual_close`). Dificultad Alta.
  3. **R4-b** -- Importar saldos iniciales por CSV (`Import_Opening_Balance_Draft_From_File_Stage`, schema/022
     MIGRADO, staging + validacion tipada por fila). Dificultad M-A.
  4. **R5-c** -- Postear ajuste CHIP post-P05 (`Post_Chip_Adjustment_Voucher`, tipo `chip_adjustment`, cuadre D=C,
     fecha > P05). Dificultad Alta.
  5. **R0-fuentes** -- CRUD de fuentes contables (`Accounting_Source` / `Accounting_Source_Numbering` / vistas /
     `Get_Next_Accounting_Source_Number`; crear/mantener/inactivar fuente + numeracion por vigencia; negativos:
     fuente duplicada/inactiva, numeracion faltante, concurrencia de consecutivos). Dificultad BAJA (maestro/CRUD)
     -- aporta el extremo FACIL del rango.
  6. **R4-c** -- Aprobar borrador de saldos iniciales (`Approve_Opening_Balance_Draft` -> materializa
     `Account_Opening_Balance` por cuenta-tercero-vigencia; bloquea re-aprobaciones/duplicados). Dificultad M.
- **RESERVA:** estas 6 quedan "no construir hasta medicion"; el resto del modulo (R0 salvo fuentes, R1, R2-a/b/d,
  R3-a/c, R4-a, R5-a/b, R6, R7) avanza a velocidad de producto. La fuente-CRUD reserva SOLO la superficie admin de
  crear fuentes; el resto del modulo usa las fuentes ya migradas + `Get_Next_...` (proc existente), asi que no se
  bloquea. La seleccion NO se re-elige mirando resultados; se SELLA como anexo (fecha + sha256).
- **Cobertura:** 5 slices (R0/R2/R3/R4x2/R5); rango de dificultad FACIL->ALTA cubierto; R6/R7 fuera por baja
  independencia (deliberado). Los 2 R4 (importar + aprobar) dan dos operaciones de un mismo slice (variacion util).
- **Poder:** N=6 = small-n confirmatorio de direccion/patron (s.2), no de magnitud.

## 4. Metricas de la replica (mapeo con Nova-Budget: VERBATIM donde aplica, N/A honesto donde no)
> AVISO de study-integrity: la replica employee-run NO reproduce el diseno completo del sello Nova-Budget. El sello
> define Q1-Q4 (Q3 descriptivo, Q4 causal); Q3 y Q4 se apoyan en contrastes INTERNOS que Contabilidad NO tiene
> (Q4 = ligero-vs-completo; Q3 = pares PAR-D). Se mide el PATRON de transferibilidad, tomando las definiciones de
> Nova-Budget SOLO donde son comparables. Todo se calcula sobre los eventos F3.3 del ledger de AEGIS.

**APLICAN (definicion identica al sello Nova-Budget s.7 / SPEC-NOVA-F3.3):**
- **M-Q2 (calidad/defectos) -- METRICA CENTRAL, replica el hallazgo Nova-Budget.** Verbatim del sello s.7:
  "defectos post-entrega clase (b) con PARIDAD DE DETECTOR (unica serie confirmatoria limpia) + FUGA DE
  OBSERVACIONES (emitidas vs registradas-con-dueno). Plan B si defectos_post~0 (efecto techo): hallazgos
  pre-integracion por severidad, como metrica DISTINTA." Sobre las unidades de Julian: el checker FORMAL (Analista)
  caza defectos reales que los tests-verdes del maker no. DIRECCION esperada: el gate caza (>0), replicando el
  hallazgo central de Nova-Budget ("el checker formal atrapa lo que el gate informal dejo pasar").
- **M-Q1 (costo) -- DESCRIPTIVO, no marginal.** Cubetas identicas al sello s.8: "4 CUBETAS de tokens: dev /
  adversarial_informal / checker_formal / coordinacion_gobierno; regimen vs arranque separados; degradacion ex-ante
  a tokens_total_atribuibles si el desglose por rol es incapturable". PERO Contabilidad es TODO gobernado -> NO hay
  "costo MARGINAL del paquete de gobierno" (eso exige el contraste ligero-vs-completo, ausente aqui). Se reporta el
  PERFIL de costo absoluto por unidad y se compara DIRECCIONALMENTE con el brazo GOBERNADO de Nova-Budget (mismo
  orden de magnitud). NO es la Q1-marginal del sello.

**PROPIAS de la transferibilidad (no son Q de Nova-Budget):**
- **M-ATRIB (atribucion, H2):** cada unidad medida se firma con `jheredia:v1`, distinguible de los agentes y del
  operador (`jball:v1`). DIRECCION: 0 unidades medidas mal-atribuidas.
- **M-MANUAL (intervencion manual):** `manual.intervention` por unidad (correcciones humanas), atribuidas al
  humano que las hizo. Descriptivo; senal de primera clase, no ruido.

**NO APLICAN (declarado por adelantado, NO es un hueco):**
- **Q3 (par-a-par, descriptivo):** Contabilidad no tiene estructura de pares PAR-D -> N/A.
- **Q4 (causal, ligero-vs-completo):** es el contraste INTERNO de Nova-Budget; Contabilidad es 100% gobernado
  employee-run -> N/A. La replica NO afirma nada causal ligero-vs-completo; afirma TRANSFERIBILIDAD (el patron se
  reproduce con empleado + dominio reales). Coherente con la delimitacion del sello Nova-Budget s.7: "el veredicto
  de compra se DIFIERE a una replica employee-run pre-registrada en Nova Accounting" = ESTE documento.

## 5. Convencion de atribucion (identidades) -- integridad del ledger
El ledger de Aegis debe distinguir sin ambiguedad quien hizo que. Identidades:
- **`jheredia:v1`** = Julian, empleado real, MAKER de sus unidades delegadas (post-B). Su trabajo medido se firma
  con SU llave. (En onboarding A1 firma interino como Codex; NINGUNA unidad MEDIDA nace bajo Codex -- guardrail.)
- **`jball:v1`** = John Ballestas, operador. Dirige agentes + revisa + corrige a mano la mayoria del desarrollo.
  **PENDIENTE DE ALTA** (re-genesis solo-Aegis, patron de B): sin ella, el trabajo de John se firmaria como
  "Codex" y confundiria humano-vs-IA en el ledger. Requisito de integridad de atribucion.
- **`analista:v1`** = checker adversarial (otra maquina/llave; maker!=checker con dientes).
- **agentes (Codex u otros)** = herramienta de generacion que el humano dirige; su uso se declara, no sustituye la
  firma humana de la transicion.
- **Regla:** una CORRECCION MANUAL de un humano se registra como `manual.intervention` firmada por ese humano; el
  hecho de que un agente generara el borrador NO cambia quien firma la transicion ni quien es responsable.

## 6. Degradaciones aceptadas (declaradas por adelantado)
- Cubetas de tokens: si el runtime de Aegis solo da un cumulativo, Q1 degrada a total-marginal atribuible
  (per-cubeta = NA), igual que el piloto Nova-Budget. No es hallazgo, es limitacion sellada.
- Adversarial en sesion separada (dev != adversarial); `tokens_adversarial_informal` taggeados por separado.
- n pequeno (s.2): confirmatorio de direccion/patron, no de magnitud.

## 7. Criterio de exito / refutacion (pre-fijado)
- **CONFIRMA H-TRANSFER si:** (H1) el gate caza >=1 defecto real que el verde del maker no habria cazado, en la
  mayoria de las unidades medidas, con traza; Y (H2) la atribucion nominal es limpia (0 unidades medidas firmadas
  por una identidad equivocada; John=jball, Julian=jheredia, checker=analista); Y (H3) M-Q1/M-Q2 en la direccion
  esperada -- M-Q2 caza defectos, M-Q1 en el mismo orden de magnitud que el gobernado Nova-Budget (sin exigir
  potencia de magnitud).
- **REFUTA / patron NO transfiere si:** el gate no caza nada nuevo en las unidades medidas (M-Q2=0), O la
  atribucion se confunde (trabajo humano firmado como agente), O el perfil de costo M-Q1 se dispara fuera de orden.
  Se REPORTA honestamente (un no-transfiere pre-registrado es un resultado valido, no un fracaso a esconder).

## 8. Como se ancla y sella (sin tocar el hub)
- Captura F3.3 + las metricas de la replica (s.4) en el ledger de AEGIS (firmados por el actor real). Doble ancla al hub: (a) cross-atestacion
  del `events.jsonl` de Aegis por gate (DECISION-0088 p.5 / 0093); (b) sha256 del artefacto de study_metrics por
  unidad, via intent del hub. El config pineado del hub NO se toca; anclaje por Entrada/intent, no re-genesis.
- Este pre-registro se SELLA (fecha + sha256) ANTES de la 1a unidad medida, como seccion hermana del Sello Etapa 2.

## 9. Prerequisitos de la 1a unidad MEDIDA (del PREP del Arquitecto, s.4)
1. B (TASK-9303) DONE -> `jheredia:v1` operativo. [**HECHO 2026-07-12**: gate F-9303-01 (sello frontera), done.]
2. Gate 2-clones NOMINAL verde (jheredia:v1 maker / analista checker) + cross-atestacion. [**HECHO 2026-07-12**:
   TASK-9390 corrida en vivo (jheredia build->in_review, Analista ratify en Aegis-cloneB, jheredia done; negativo
   fallo por llave ausente; validate 0 ambos clones). **Cross-atestacion Entrada 3 anclada por el Arquitecto**
   (hub e22e9f3; aegis_commit d153357a, head_seq 3881, sha256 events.jsonl e8f1b08f, config-epoch 77242D63 epoca 2).]
3. Base congelada ACCOUNTING_BASE_SOLID_20260711 (608b4370) + verifier. [RESUELTO.]
4. SPEC-CONT de las unidades medidas instanciadas. [kit 6/8 (S1-S6A); falta S6B cierre anual + S6C frontera. Las
   6 unidades medidas caen en S2/S3/S4/S5 + R0-fuentes -> cubiertas por el kit vigente.]
5. Instrumentacion F3.3 cableada en Aegis + doble ancla. [PREP hecho; **wiring al abrir el build = UNICO prereq
   tecnico pendiente para sellar** (ver s.10).]
6. **Este pre-registro SELLADO** (opcion A) + la seleccion de unidades sellada como anexo (s.3). [ESTE DOC; ceremonia s.11.]
7. **`jball:v1` dada de alta** + convencion de atribucion (s.5). [**HECHO 2026-07-12**: registrada en el config-epoch
   epoca 2 de Aegis (TASK-9304, gate F-9304-01 sello pre_t0); pubkey `pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=`.]
8. Calendario Sprint 1 post-30-jul. [Linea roja.]

## 10. Que falta para sellar (accion operador + Asesor)
- [HECHO 2026-07-12] s.3 (muestra N=6 fijada: R2-c/R3-b/R4-b/R5-c/R0-fuentes/R4-c) + s.4 (metricas de la replica,
  mapeo honesto: M-Q1/M-Q2 aplican, Q3/Q4 N/A, M-ATRIB/M-MANUAL propias).
- [HECHO 2026-07-12] alta de `jball:v1` (epoca 2) + B done + gate 2-clones nominal verde + cross-atestacion anclada
  -> **`jheredia:v1` OPERATIVO** (ver s.9 items 1/2/7). La atribucion nominal (John=jball, Julian=jheredia,
  checker=analista) esta VIVA y demostrada en el ledger de Aegis.
- **UNICO prereq tecnico pendiente para sellar: instrumentacion F3.3 cableada en Aegis** (los 3 eventos
  cost.attributed/defect.reported/manual.intervention + study_metrics.py + doble ancla al hub). Se cablea al abrir
  el build (post-30-jul); reusa lo construido en Nova-Budget (TASK-0249). NO bloquea el sello del DOCUMENTO, solo
  la 1a unidad MEDIDA (el sello puede ejecutarse en cuanto F3.3 quede cableada, justo antes de construir R-x-1).
- El operador SELLA (fecha + sha256) segun la CEREMONIA de s.11, antes de la 1a unidad medida.

## 11. Ceremonia de sellado (opcion A) -- procedimiento
Sellar = congelar este documento y anclarlo al ledger, de modo que quede probado que se pre-registro ANTES de
construir/medir la 1a unidad. Pasos (los ejecuta el operador o el Asesor bajo su orden, patron del Sello Etapa 1):
1. **Congelar el texto:** cerrar todos los `[LLENAR]`/`[PENDIENTE]` (a esta fecha solo queda la nota de F3.3 en s.10,
   que es una PRECONDICION externa, no un hueco del pre-registro). Fijar el nombre final del artefacto:
   `SELLO-PREREGISTRO-contabilidad-employee-run-N6.md` (copia congelada de este DRAFT).
2. **Anexo de seleccion (s.3) sellado:** las 6 unidades (R2-c/R3-b/R4-b/R5-c/R0-fuentes/R4-c) + criterio de seleccion
   (mezcla de dificultad, independencia alta/media) + fecha de fijacion (2026-07-12, ANTES de construir). Ya fijado; se
   congela con el resto.
3. **sha256 del artefacto congelado:** calcular `sha256` del `.md` sellado (byte a byte). Ese hash ES el sello.
4. **Anclar al ledger (sin re-genesis):** registrar el sha256 via `submit_intent` (evento tipo decision/project_narrative
   con el hash + fecha UTC), como **seccion hermana del Sello Etapa 2** o intent standalone del hub. Doble ancla igual
   que la medicion: (a) en el #4 del hub, (b) cross-atestado si el corpus vive en Aegis. El config pineado NO se toca.
5. **Verificacion independiente:** un segundo firmante (Analista o Arquitecto) recomputa el sha256 del artefacto y
   confirma que cuadra con el anclado -> el pre-registro queda ATESTADO como pre-datado.
6. **Regla dura post-sello:** de aqui en adelante, NADA de s.1-s.7 (hipotesis, muestra, metricas, criterio de exito/
   refutacion) se cambia mirando datos. Un cambio exigiria una enmienda FECHADA y justificada, visible en el ledger.

**Estado del sello: LISTO PARA EJECUTAR** salvo el cableado de F3.3 (s.10). En cuanto F3.3 quede cableada al abrir el
build, se ejecuta esta ceremonia y se construye la 1a unidad medida bajo medicion.

-- Preparado por el Asesor para el operador (John). Ejecucion del sello: pendiente del operador (gated por F3.3 wiring).
