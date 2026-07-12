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
- (H3) el costo/esfuerzo (Q1-Q5) cae en la MISMA DIRECCION esperada que en Nova-Budget.
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
- **MUESTRA SELECCIONADA (N=4), fijada por el OPERADOR el 2026-07-12 ANTES de construir; criterio = mezcla de
  dificultad + independencia alta/media (no bloquea el resto del modulo):**
  1. **R2-c** -- Reverso de comprobante manual (`Reverse_Voucher` / `Voucher_Relation` / `vw_Voucher_Adjustment_Map`;
     crea `manual_accounting_reversal`, invierte D/C, relacion `reverses`; bloquea reverso de source!=accounting /
     no-manual / is_system_generated). Dificultad M-A.
  2. **R3-b** -- Cerrar periodo mensual (`Close_Accounting_Period` + P03/P04 + audit; NO puede activar la escotilla
     `annual_close`). Dificultad Alta.
  3. **R4-b** -- Importar saldos iniciales por CSV (`Import_Opening_Balance_Draft_From_File_Stage`, schema/022
     MIGRADO, staging + validacion tipada por fila). Dificultad M-A.
  4. **R5-c** -- Postear ajuste CHIP post-P05 (`Post_Chip_Adjustment_Voucher`, tipo `chip_adjustment`, cuadre D=C,
     fecha > P05). Dificultad Alta.
- **RESERVA:** estas 4 quedan "no construir hasta medicion"; el resto del modulo (R0, R1, R2-a/b/d, R3-a/c,
  R4-a/c, R5-a/b, R6, R7) avanza a velocidad de producto. La seleccion NO se re-elige mirando resultados; se SELLA
  como anexo (fecha + sha256).
- **Poder:** N=4 = small-n confirmatorio de direccion/patron (s.2), no de magnitud. Nota: N=4 esta en el extremo
  bajo; una 5a unidad rica en defectos (p.ej. R2-b publicar, THROW 52200-52252) reforzaria H1 sin cambiar el
  diseno -- opcional, decision del operador.

## 4. Metricas Q1-Q5 y direccion esperada (definicion IDENTICA a Nova-Budget)
Para que la comparacion de transferibilidad sea valida, Q1-Q5 usan la MISMA definicion del sello Nova-Budget
(SPEC-NOVA-F3.3), calculadas sobre los eventos F3.3 del ledger de AEGIS:
- **Q1 (costo atribuido):** tokens/tiempo por unidad, separando `tokens_adversarial_informal` de
  `tokens_checker_formal`. Direccion esperada: mismo orden de magnitud relativo que Nova-Budget (degradacion de
  cubetas a total-marginal aceptada, igual que en el piloto GOAL-P1).
- **Q2..Q5:** [copiar textual las definiciones y direccion esperada del sello Nova-Budget al sellar -- NO
  redefinir aqui; la validez de la comparacion depende de que sean identicas].
- **defect.reported:** conteo y traza de defectos reales cazados por el gate por unidad. Direccion esperada:
  > 0 en promedio (H1) -- el gate caza lo que el verde del maker no.
- **manual.intervention:** intervenciones humanas (correcciones a mano) por unidad, atribuidas al humano que las
  hizo. Es senal de primera clase, no ruido.

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
  por una identidad equivocada; John=jball, Julian=jheredia, checker=analista); Y (H3) Q1-Q5 en la direccion
  esperada (sin exigir potencia de magnitud).
- **REFUTA / patron NO transfiere si:** el gate no caza nada nuevo en las unidades medidas, O la atribucion se
  confunde (trabajo humano firmado como agente), O Q1-Q5 van en direccion contraria. Se REPORTA honestamente
  (un no-transfiere pre-registrado es un resultado valido, no un fracaso a esconder).

## 8. Como se ancla y sella (sin tocar el hub)
- Captura F3.3 + Q1-Q5 en el ledger de AEGIS (firmados por el actor real). Doble ancla al hub: (a) cross-atestacion
  del `events.jsonl` de Aegis por gate (DECISION-0088 p.5 / 0093); (b) sha256 del artefacto de study_metrics por
  unidad, via intent del hub. El config pineado del hub NO se toca; anclaje por Entrada/intent, no re-genesis.
- Este pre-registro se SELLA (fecha + sha256) ANTES de la 1a unidad medida, como seccion hermana del Sello Etapa 2.

## 9. Prerequisitos de la 1a unidad MEDIDA (del PREP del Arquitecto, s.4)
1. B (TASK-9303) DONE -> `jheredia:v1` operativo. [GO a Codex; en curso.]
2. Gate 2-clones NOMINAL verde (jheredia:v1 maker / analista checker) + cross-atestacion. [A1 primero como
   onboarding; el nominal tras B.]
3. Base congelada ACCOUNTING_BASE_SOLID_20260711 (608b4370) + verifier. [RESUELTO.]
4. SPEC-CONT de las unidades medidas instanciadas. [kit 2/8; en curso.]
5. Instrumentacion F3.3 cableada en Aegis + doble ancla. [PREP hecho; wiring al abrir build.]
6. **Este pre-registro SELLADO** (opcion A) + la seleccion de unidades sellada como anexo (s.3). [ESTE DOC.]
7. **`jball:v1` dada de alta** + convencion de atribucion (s.5). [PENDIENTE re-genesis Aegis, patron B.]
8. Calendario Sprint 1 post-30-jul. [Linea roja.]

## 10. Que falta para sellar (accion operador + Asesor)
- Completar s.3 (N minimo + metodo de seleccion de unidades) y s.4 (copiar Q2-Q5 textual del sello Nova-Budget).
- Dar de alta `jball:v1` (rutear al Arquitecto; puede ir en la misma re-genesis de B).
- El operador SELLA (fecha + sha256) antes de la 1a unidad medida.

-- Preparado por el Asesor para el operador (John). Sellado: pendiente del operador.
